#!/usr/bin/env bash
# Installs the PHP QA toolchain into $FSWP_TOOLS (default ~/.fswp-tools) using only apt and GitHub.
# No Composer or Packagist needed. Safe to re-run. Anything that fails is reported, never hidden.
set -uo pipefail
T="${FSWP_TOOLS:-$HOME/.fswp-tools}"; mkdir -p "$T"; cd "$T"
say() { printf '%s\n' "$*"; }

if ! command -v php >/dev/null 2>&1 && [ "$(id -u)" = 0 ] && command -v apt-get >/dev/null 2>&1; then
  apt-get update -qq >/dev/null 2>&1
  apt-get install -y -qq php-cli php-xml php-mbstring >/dev/null 2>&1
fi
command -v php >/dev/null 2>&1 && say "php:      $(php -r 'echo PHP_VERSION;')" || { say "php:      NOT AVAILABLE (PHP checks will be NOT RUN)"; exit 0; }

[ -f phpcbf.phar ] || curl -fsSL -o phpcbf.phar https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/latest/download/phpcbf.phar || rm -f phpcbf.phar
[ -f phpcs.phar ] || curl -fsSL -o phpcs.phar https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/latest/download/phpcs.phar || rm -f phpcs.phar
for r in WordPress/WordPress-Coding-Standards PHPCSStandards/PHPCSUtils PHPCSStandards/PHPCSExtra PHPCompatibility/PHPCompatibility PHPCompatibility/PHPCompatibilityWP PHPCompatibility/PHPCompatibilityParagonie; do
  d="$(basename "$r")"; [ -d "$d" ] || git clone --depth 1 -q "https://github.com/$r.git" "$d" 2>/dev/null || say "clone failed: $r"
done
if [ -f phpcs.phar ]; then
  paths=""; for d in WordPress-Coding-Standards PHPCSUtils PHPCSExtra PHPCompatibility PHPCompatibilityWP PHPCompatibilityParagonie; do [ -d "$d" ] && paths="$paths,$T/$d"; done
  php phpcs.phar --config-set installed_paths "${paths#,}" >/dev/null 2>&1
  say "phpcs:    $(php phpcs.phar --version 2>/dev/null | head -1) (WordPress, PHPCompatibilityWP)"
else say "phpcs:    NOT AVAILABLE"; fi

[ -f phpstan.phar ] || curl -fsSL -o phpstan.phar https://github.com/phpstan/phpstan/releases/latest/download/phpstan.phar || rm -f phpstan.phar
[ -d wordpress-stubs ] || git clone --depth 1 -q https://github.com/php-stubs/wordpress-stubs.git wordpress-stubs 2>/dev/null || say "clone failed: wordpress-stubs"
[ -f phpstan.phar ] && [ -f wordpress-stubs/wordpress-stubs.php ] && say "phpstan:  $(php phpstan.phar --version 2>/dev/null | head -1) (with wordpress-stubs, no extension)" || say "phpstan:  NOT AVAILABLE"
command -v wp >/dev/null 2>&1 && say "wp-cli:   $(wp --version 2>/dev/null)" || say "wp-cli:   NOT AVAILABLE (Plugin Check will be NOT RUN)"
