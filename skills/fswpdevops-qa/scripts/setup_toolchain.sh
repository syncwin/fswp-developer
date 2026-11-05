#!/usr/bin/env bash
# Installs the PHP QA toolchain into $FSWP_TOOLS (default ~/.fswp-tools) using only apt and GitHub.
# No Composer or Packagist needed. Safe to re-run. Anything that fails is reported, never hidden.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; T="${FSWP_TOOLS:-$HOME/.fswp-tools}"; mkdir -p "$T"; cd "$T"
say() { printf '%s\n' "$*"; }
# Supply chain: versions and SHA-256 / commit SHAs are pinned in toolchain.lock (in the repo, next to this script).
# No trust on first use: a phar is verified against the lock before it is kept; a clone must match the pinned commit.
LOCK="$HERE/toolchain.lock"
[ -f "$LOCK" ] || { say "toolchain.lock missing"; exit 1; }
sha() { if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }
lock() { awk -v k="$1" -v n="$2" '$1==k && $2==n' "$LOCK"; }
fetch() { # fetch <file>: download the pinned release, keep it only if the SHA-256 matches the lock
  read -r _ _ ver want url < <(lock phar "$1")
  [ -n "${want:-}" ] || { say "REJECTED $1: not in toolchain.lock"; return 1; }
  if [ -f "$1" ] && [ "$(sha "$1")" = "$want" ]; then return 0; fi
  rm -f "$1"
  curl -fsSL --proto '=https' --tlsv1.2 -o "$1.part" "$url" || { rm -f "$1.part"; say "download failed: $1"; return 1; }
  [ "$(sha "$1.part")" = "$want" ] || { rm -f "$1.part"; say "REJECTED $1: SHA-256 does not match toolchain.lock"; return 1; }
  mv "$1.part" "$1"; say "installed $1 $ver (sha256 verified against toolchain.lock)"
}
clonepin() { # clonepin <dir>: shallow clone of the pinned tag; the commit must equal the lock
  read -r _ _ tag want url < <(lock git "$1")
  [ -n "${want:-}" ] || { say "REJECTED $1: not in toolchain.lock"; return 1; }
  if [ -d "$1/.git" ] && [ "$(git -C "$1" rev-parse HEAD 2>/dev/null)" = "$want" ]; then return 0; fi
  rm -rf "$1.part"
  git clone --depth 1 -q --branch "$tag" "$url" "$1.part" 2>/dev/null || { rm -rf "$1.part"; say "clone failed: $1"; return 1; }
  [ "$(git -C "$1.part" rev-parse HEAD)" = "$want" ] || { rm -rf "$1.part"; say "REJECTED $1: commit does not match toolchain.lock"; return 1; }
  rm -rf "$1"; mv "$1.part" "$1"; say "cloned $1 $tag (commit verified)"
}

if ! command -v php >/dev/null 2>&1 && [ "$(id -u)" = 0 ] && command -v apt-get >/dev/null 2>&1; then
  apt-get update -qq >/dev/null 2>&1
  apt-get install -y -qq php-cli php-xml php-mbstring >/dev/null 2>&1
fi
command -v php >/dev/null 2>&1 && say "php:      $(php -r 'echo PHP_VERSION;')" || { say "php:      NOT AVAILABLE (PHP checks will be NOT RUN)"; exit 0; }

fetch phpcbf.phar
fetch phpcs.phar
for d in WordPress-Coding-Standards PHPCSUtils PHPCSExtra PHPCompatibility PHPCompatibilityWP PHPCompatibilityParagonie; do clonepin "$d"; done
if [ -f phpcs.phar ]; then
  paths=""; for d in WordPress-Coding-Standards PHPCSUtils PHPCSExtra PHPCompatibility PHPCompatibilityWP PHPCompatibilityParagonie; do [ -d "$d" ] && paths="$paths,$T/$d"; done
  php phpcs.phar --config-set installed_paths "${paths#,}" >/dev/null 2>&1
  say "phpcs:    $(php phpcs.phar --version 2>/dev/null | head -1) (WordPress, PHPCompatibilityWP)"
else say "phpcs:    NOT AVAILABLE"; fi

fetch phpstan.phar
clonepin wordpress-stubs
[ -f phpstan.phar ] && [ -f wordpress-stubs/wordpress-stubs.php ] && say "phpstan:  $(php phpstan.phar --version 2>/dev/null | head -1) (with wordpress-stubs, no extension)" || say "phpstan:  NOT AVAILABLE"
command -v wp >/dev/null 2>&1 && say "wp-cli:   $(wp --version 2>/dev/null)" || say "wp-cli:   NOT AVAILABLE (Plugin Check will be NOT RUN)"
