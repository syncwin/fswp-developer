#!/usr/bin/env bash
# Installs the PHP QA toolchain into $FSWP_TOOLS (default ~/.fswp-tools) using only apt and GitHub.
# No Composer or Packagist needed. Safe to re-run. Anything that fails is reported, never hidden.
set -uo pipefail
T="${FSWP_TOOLS:-$HOME/.fswp-tools}"; mkdir -p "$T"; cd "$T"
say() { printf '%s\n' "$*"; }
# Supply chain: every downloaded phar is checksummed into $T/SHA256SUMS on first fetch (review it); a later
# fetch that does not match is rejected. FSWP_REFRESH=1 re-records after you reviewed an upgrade.
sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }
recorded() { awk -v f="$1" '$2==f {print $1}' SHA256SUMS 2>/dev/null; }
record() { { grep -v " $1" SHA256SUMS 2>/dev/null || true; echo "$2 $1"; } > SHA256SUMS.tmp; mv SHA256SUMS.tmp SHA256SUMS; }
fetch() { # fetch <file> <url>
  if [ -f "$1" ]; then [ -n "$(recorded "$1")" ] || { record "$1" "$(sha "$1")"; say "recorded checksum of existing $1 (review SHA256SUMS)"; }; return 0; fi
  curl -fsSL --proto '=https' --tlsv1.2 -o "$1.part" "$2" || { rm -f "$1.part"; return 1; }
  new="$(sha "$1.part")"; old="$(recorded "$1")"
  if [ -n "$old" ] && [ "$old" != "$new" ] && [ "${FSWP_REFRESH:-0}" != 1 ]; then rm -f "$1.part"; say "REJECTED $1: checksum differs from SHA256SUMS (FSWP_REFRESH=1 after review)"; return 1; fi
  record "$1" "$new"; mv "$1.part" "$1"; say "downloaded $1 sha256=$new (recorded; compare with the upstream release on first fetch)"
}

if ! command -v php >/dev/null 2>&1 && [ "$(id -u)" = 0 ] && command -v apt-get >/dev/null 2>&1; then
  apt-get update -qq >/dev/null 2>&1
  apt-get install -y -qq php-cli php-xml php-mbstring >/dev/null 2>&1
fi
command -v php >/dev/null 2>&1 && say "php:      $(php -r 'echo PHP_VERSION;')" || { say "php:      NOT AVAILABLE (PHP checks will be NOT RUN)"; exit 0; }

fetch phpcbf.phar https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/latest/download/phpcbf.phar
fetch phpcs.phar https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/latest/download/phpcs.phar
for r in WordPress/WordPress-Coding-Standards PHPCSStandards/PHPCSUtils PHPCSStandards/PHPCSExtra PHPCompatibility/PHPCompatibility PHPCompatibility/PHPCompatibilityWP PHPCompatibility/PHPCompatibilityParagonie; do
  d="$(basename "$r")"; [ -d "$d" ] || git clone --depth 1 -q "https://github.com/$r.git" "$d" 2>/dev/null || say "clone failed: $r"
done
if [ -f phpcs.phar ]; then
  paths=""; for d in WordPress-Coding-Standards PHPCSUtils PHPCSExtra PHPCompatibility PHPCompatibilityWP PHPCompatibilityParagonie; do [ -d "$d" ] && paths="$paths,$T/$d"; done
  php phpcs.phar --config-set installed_paths "${paths#,}" >/dev/null 2>&1
  say "phpcs:    $(php phpcs.phar --version 2>/dev/null | head -1) (WordPress, PHPCompatibilityWP)"
else say "phpcs:    NOT AVAILABLE"; fi

fetch phpstan.phar https://github.com/phpstan/phpstan/releases/latest/download/phpstan.phar
[ -d wordpress-stubs ] || git clone --depth 1 -q https://github.com/php-stubs/wordpress-stubs.git wordpress-stubs 2>/dev/null || say "clone failed: wordpress-stubs"
[ -f phpstan.phar ] && [ -f wordpress-stubs/wordpress-stubs.php ] && say "phpstan:  $(php phpstan.phar --version 2>/dev/null | head -1) (with wordpress-stubs, no extension)" || say "phpstan:  NOT AVAILABLE"
command -v wp >/dev/null 2>&1 && say "wp-cli:   $(wp --version 2>/dev/null)" || say "wp-cli:   NOT AVAILABLE (Plugin Check will be NOT RUN)"
