# Recipe: run the full QA gate (plugin or theme)

Do these steps with Bash, Read, Glob and Grep on `<dir>`. Report one table `CHECK | RESULT | DETAIL`. Every result is PASS, FAIL or NOT RUN; NOT RUN is never a pass. The gate FAILs when any row FAILs. A failed run is reported as is; fixes happen in the router's fix loop, not while gating.

## Inputs
- `<dir>`: the plugin or theme folder.
- `min-php`: default `7.4`.
- `fix` (optional): run the formatter once first (step 0); review the diff before delivering.
- Tools folder `T`: `$FSWP_TOOLS`, default `~/.fswp-tools`, filled by `setup_toolchain.md`.

## Trust rule for tools (fail closed)
A phar (`phpcs.phar`, `phpcbf.phar`, `phpstan.phar`) runs only when its SHA-256 equals the hash pinned in `setup_toolchain.md` (never a checksum file next to the binary). A phar that is present but fails that comparison makes its rows FAIL ("checksum missing/mismatched: re-run setup_toolchain"); an absent tool stays NOT RUN. Compute the hash with `sha256sum` (or `shasum -a 256`).

## Steps
0. **Fix** (only with `fix`, `php` available and `phpcbf.phar` verified): `php T/phpcbf.phar --standard=WordPress --extensions=php --ignore='*/vendor/*,*/node_modules/*,*/foundation/*' <dir>`, output discarded. If `phpcbf.phar` exists but is not verified, add a row `phpcbf --fix` FAIL ("phpcbf.phar checksum missing/mismatched: re-run setup_toolchain").
1. **House rules**: a folder whose `style.css` has a `Theme Name:` header is a theme; follow `theme_check.md`, row `theme_check (house rules)`. Otherwise follow `qa_check.md`, row `qa_check (house rules)`. PASS when the run has no FAIL (detail: the summary line); FAIL shows the first 3 `[FAIL]` lines.
2. **Documentation standard**: follow `docs_gate.md`, one row `docs_gate (documentation standard)`: FAIL with up to 3 FAIL or NOT RUN details when anything FAILs; NOT RUN ("static checks passed; ...") when all static checks pass but the diff checks are NOT RUN; otherwise PASS ("all documentation checks passed").
3. **php -l**: with `php` on PATH, run `php -l` on every `.php` file outside `vendor` and `node_modules`; any output other than "No syntax errors" is FAIL (first 2), else PASS ("all files parse"). No `php`: NOT RUN ("php missing; run setup_toolchain").
4. **PHPCS WordPress-Extra (WPCS)** and **PHP compatibility `<min-php>`+**, with `php` and a verified `phpcs.phar`:
   - `php T/phpcs.phar --standard=WordPress-Extra --extensions=php --ignore='*/vendor/*,*/node_modules/*,*/foundation/*' --report=summary <dir>`. Read the line "A TOTAL OF n ERRORS AND m WARNINGS": no such line is PASS ("no violations"); 0 errors is PASS ("0 errors, m warnings (review them)"); otherwise FAIL ("n errors, m warnings; run with fix, then re-check").
   - `php T/phpcs.phar --standard=PHPCompatibilityWP --runtime-set testVersion "<min-php>-" --extensions=php --ignore='*/vendor/*,*/node_modules/*' --report=summary <dir>`: exit 0 is PASS ("no violations"), else FAIL (last 3 lines).
   - `phpcs.phar` present but not verified: both rows FAIL ("phpcs.phar checksum missing/mismatched: re-run setup_toolchain"). Absent or no `php`: both rows NOT RUN ("phpcs missing (run setup_toolchain)").
5. **PHPStan level 5 (WP stubs)**, with `php`, a verified `phpstan.phar` and `T/wordpress-stubs/wordpress-stubs.php`:
   - Make a temporary bootstrap file: `<?php`, then for every constant defined with `define( 'NAME'` in the plugin's PHP (unique, sorted): `if ( ! defined('NAME') ) { define('NAME', '<value>'); }` where the value is `<dir>/` for names ending `_DIR`, `<dir>/plugin.php` for `_FILE`, `http://localhost/` for `_URL`, and empty otherwise.
   - Make a temporary config:
     ```
     parameters:
       level: 5
       bootstrapFiles:
         - T/wordpress-stubs/wordpress-stubs.php
         - <bootstrap file>
       excludePaths:
         - <dir>/vendor (?)
         - <dir>/node_modules (?)
         - <dir>/public/foundation (?)
       scanDirectories:
         - <dir>
     ```
   - `php T/phpstan.phar analyse -c <config> --no-progress --memory-limit=1G <dir>`: exit 0 is PASS ("no errors"), else FAIL (first 2 lines mentioning `Found`, `[ERROR]`, `Invalid` or `error`). Delete both temporary files.
   - `phpstan.phar` present but not verified: FAIL ("phpstan.phar checksum missing/mismatched: re-run setup_toolchain"). Phar or stubs missing: NOT RUN ("phpstan or stubs missing (run setup_toolchain)").
6. **Plugin Check (WP-CLI)**: always NOT RUN here. Detail "run inside a WordPress install: wp plugin check <slug>" when `wp` and its `plugin check` command exist, otherwise "needs WordPress + wp-cli + Plugin Check plugin".

## Output
The table, rows in the order above, then the verdict. Always list every NOT RUN with the exact command the user can run.
