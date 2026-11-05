#!/usr/bin/env bash
# Runs every available gate check on a plugin folder. Usage: run_gate.sh <plugin-dir> [min-php, default 7.4] [--fix]
# --fix runs phpcbf (WordPress standard) first to auto-format; review the diff before delivering.
# Prints a PASS / FAIL / NOT RUN table. NOT RUN is never a pass. Exit 1 if anything FAILs.
set -uo pipefail
D="${1:?plugin dir}"; MINPHP="${2:-7.4}"; FIX=0; for a in "$@"; do [ "$a" = "--fix" ] && FIX=1; done; [ "$MINPHP" = "--fix" ] && MINPHP=7.4
T="${FSWP_TOOLS:-$HOME/.fswp-tools}"; HERE="$(cd "$(dirname "$0")" && pwd)"
rows=(); fail=0
sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }
# Fail closed: a phar only runs when it matches the SHA-256 pinned in the repo's toolchain.lock (never a file next to the binary).
# A phar that is present but unverified (missing/mismatched checksum) FAILS the gate; an absent tool stays NOT RUN.
okphar() { local want; want="$(awk -v f="$1" '$1=="phar" && $2==f {print $4}' "$HERE/toolchain.lock" 2>/dev/null)"; [ -f "$T/$1" ] && [ -n "$want" ] && [ "$want" = "$(sha "$T/$1")" ]; }
if [ "$FIX" = 1 ] && command -v php >/dev/null 2>&1 && okphar phpcbf.phar; then php "$T/phpcbf.phar" --standard=WordPress --extensions=php --ignore='*/vendor/*,*/node_modules/*,*/foundation/*' "$D" >/dev/null 2>&1; fi
row() { rows+=("$1|$2|$3"); if [ "$2" = FAIL ]; then fail=1; fi; return 0; }

if [ -f "$D/style.css" ] && grep -qi "Theme Name:" "$D/style.css"; then CHK=theme_check.py; LABEL="theme_check.py (house rules)"; else CHK=qa_check.py; LABEL="qa_check.py (house rules)"; fi
out=$(python3 "$HERE/$CHK" "$D" 2>&1); rc=$?
[ $rc -eq 0 ] && row "$LABEL" PASS "$(printf '%s' "$out" | tail -1)" || row "$LABEL" FAIL "$(printf '%s' "$out" | grep '^\[FAIL\]' | head -3 | tr -d '\r' | tr '\n' ';')"

# Documentation standard (docs_gate.py): README + docs, CHANGELOG [Unreleased], docs/features index and files. Diff checks need git + a base branch.
out=$(python3 "$HERE/docs_gate.py" "$D" 2>&1); rc=$?
dg=$(printf '%s' "$out" | grep -E ' (FAIL|NOT RUN) ' | head -3 | tr -d '\r' | sed 's/  */ /g' | tr '\n' ';')
if [ $rc -ne 0 ]; then row "docs_gate.py (documentation standard)" FAIL "$dg"
elif printf '%s' "$out" | grep -q ' NOT RUN '; then row "docs_gate.py (documentation standard)" "NOT RUN" "static checks passed; $dg"
else row "docs_gate.py (documentation standard)" PASS "all documentation checks passed"; fi

if command -v php >/dev/null 2>&1; then
  bad=$(find "$D" -name '*.php' -not -path '*/vendor/*' -not -path '*/node_modules/*' -exec php -l {} \; 2>&1 | grep -v '^No syntax errors' | grep -v '^$')
  [ -z "$bad" ] && row "php -l" PASS "all files parse" || row "php -l" FAIL "$(printf '%s' "$bad" | head -2 | tr '\n' ';')"
else row "php -l" "NOT RUN" "php missing; run scripts/setup_toolchain.sh"; fi

if command -v php >/dev/null 2>&1 && okphar phpcs.phar; then
  out=$(php "$T/phpcs.phar" --standard=WordPress-Extra --extensions=php --ignore='*/vendor/*,*/node_modules/*,*/foundation/*' --report=summary "$D" 2>&1)
  errs=$(printf '%s' "$out" | sed -n 's/.*A TOTAL OF \([0-9]*\) ERRORS\? AND \([0-9]*\) WARNING.*/\1/p'); warns=$(printf '%s' "$out" | sed -n 's/.*A TOTAL OF \([0-9]*\) ERRORS\? AND \([0-9]*\) WARNING.*/\2/p')
  if [ -z "$errs" ]; then row "PHPCS WordPress-Extra (WPCS)" PASS "no violations"; elif [ "$errs" = 0 ]; then row "PHPCS WordPress-Extra (WPCS)" PASS "0 errors, ${warns} warnings (review them)"; else row "PHPCS WordPress-Extra (WPCS)" FAIL "${errs} errors, ${warns} warnings; run with --fix, then re-check"; fi
  out=$(php "$T/phpcs.phar" --standard=PHPCompatibilityWP --runtime-set testVersion "${MINPHP}-" --extensions=php --ignore='*/vendor/*,*/node_modules/*' --report=summary "$D" 2>&1); rc=$?
  [ $rc -eq 0 ] && row "PHP compatibility ${MINPHP}+" PASS "no violations" || row "PHP compatibility ${MINPHP}+" FAIL "$(printf '%s' "$out" | tail -3 | tr '\n' ' ')"
elif [ -f "$T/phpcs.phar" ] && command -v php >/dev/null 2>&1; then row "PHPCS WordPress-Extra (WPCS)" FAIL "phpcs.phar checksum missing/mismatched: re-run setup_toolchain.sh"; row "PHP compatibility ${MINPHP}+" FAIL "phpcs.phar checksum missing/mismatched: re-run setup_toolchain.sh"
else row "PHPCS WordPress-Extra (WPCS)" "NOT RUN" "phpcs missing (run setup_toolchain.sh)"; row "PHP compatibility ${MINPHP}+" "NOT RUN" "phpcs missing (run setup_toolchain.sh)"; fi

if command -v php >/dev/null 2>&1 && okphar phpstan.phar && [ -f "$T/wordpress-stubs/wordpress-stubs.php" ]; then
  boot=$(mktemp --suffix=.php); echo '<?php' > "$boot"
  for c in $(grep -rhoE "define\( *'[A-Z0-9_]+'" "$D" --include=*.php | sed -E "s/define\( *'([A-Z0-9_]+)'/\1/" | sort -u); do
    case "$c" in *_DIR) v="$D/";; *_FILE) v="$D/plugin.php";; *_URL) v="http://localhost/";; *) v="";; esac
    printf "if ( ! defined('%s') ) { define('%s', '%s'); }\n" "$c" "$c" "$v" >> "$boot"
  done
  cfg=$(mktemp --suffix=.neon); printf 'parameters:\n  level: 5\n  bootstrapFiles:\n    - %s/wordpress-stubs/wordpress-stubs.php\n    - %s\n  excludePaths:\n    - %s/vendor (?)\n    - %s/node_modules (?)\n    - %s/public/foundation (?)\n  scanDirectories:\n    - %s\n' "$T" "$boot" "$D" "$D" "$D" "$D" > "$cfg"
  out=$(php "$T/phpstan.phar" analyse -c "$cfg" --no-progress --memory-limit=1G "$D" 2>&1); rc=$?
  [ $rc -eq 0 ] && row "PHPStan level 5 (WP stubs)" PASS "no errors" || row "PHPStan level 5 (WP stubs)" FAIL "$(printf '%s' "$out" | grep -E 'Found|\[ERROR\]|Invalid|error' | head -2 | tr '\n' ' ')"
  rm -f "$cfg" "$boot"
elif [ -f "$T/phpstan.phar" ] && command -v php >/dev/null 2>&1 && ! okphar phpstan.phar; then row "PHPStan level 5 (WP stubs)" FAIL "phpstan.phar checksum missing/mismatched: re-run setup_toolchain.sh"
else row "PHPStan level 5 (WP stubs)" "NOT RUN" "phpstan or stubs missing (run setup_toolchain.sh)"; fi

if command -v wp >/dev/null 2>&1 && wp plugin check --help >/dev/null 2>&1; then row "Plugin Check (WP-CLI)" "NOT RUN" "run inside a WordPress install: wp plugin check <slug>"; else row "Plugin Check (WP-CLI)" "NOT RUN" "needs WordPress + wp-cli + Plugin Check plugin"; fi

if [ "$FIX" = 1 ] && [ -f "$T/phpcbf.phar" ] && ! okphar phpcbf.phar; then row "phpcbf --fix" FAIL "phpcbf.phar checksum missing/mismatched: re-run setup_toolchain.sh"; fi
printf '\n%-32s %-8s %s\n' CHECK RESULT DETAIL
for r in "${rows[@]}"; do IFS='|' read -r a b c <<<"$r"; printf '%-32s %-8s %s\n' "$a" "$b" "$c"; done
exit $fail
