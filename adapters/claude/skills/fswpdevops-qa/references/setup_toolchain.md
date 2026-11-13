# Recipe: install the pinned PHP QA toolchain

Do these steps with Bash. They install PHPCS, the WordPress and compatibility standards, PHPStan and the WordPress stubs into the tools folder `T` using only `apt`, `curl`, `git` and GitHub, with no Composer or Packagist. Safe to rerun; skip what is already correct. Report anything that fails and never hide it.

## Inputs
- `T`: `$FSWP_TOOLS`, default `~/.fswp-tools`. Create it and work inside it.

## The pins (supply chain)
Versions, SHA-256 hashes and commit SHAs below are the source of truth for this recipe and for `run_gate.md`. No trust on first use: a phar is kept only when its SHA-256 matches, a clone only when its commit matches. Sources: phar hashes are the official GitHub release asset digests for PHPCSStandards/PHP_CodeSniffer 4.0.4 and phpstan/phpstan 2.3.5 (`phpstan.phar` also re-hashed locally after download: identical); commit SHAs are the dereferenced tag commits from the GitHub API, 2026-11-05. To upgrade: change version and hash from the new official release, review, commit.

| Phar | Version | SHA-256 | URL |
|---|---|---|---|
| `phpcbf.phar` | 4.0.4 | `0b3b8c5571543e94452f6edec0d7e924b287a64c13b73d8dcf3d25f0ee004948` | `https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/download/4.0.4/phpcbf.phar` |
| `phpcs.phar` | 4.0.4 | `4b010cd21d8bc8a17e2504792e3c77ef8259126f24caf7eafe7eddef1fa871e9` | `https://github.com/PHPCSStandards/PHP_CodeSniffer/releases/download/4.0.4/phpcs.phar` |
| `phpstan.phar` | 2.3.5 | `4b3ed7850a20b092331bd1040e4f54a1d3c0559b4cf006431073997ebcb4324b` | `https://github.com/phpstan/phpstan/releases/download/2.3.5/phpstan.phar` |

| Folder | Tag | Commit | Repository |
|---|---|---|---|
| `WordPress-Coding-Standards` | 3.4.1 | `ec2ff942335f33683a5957a85d138753876a05cf` | `https://github.com/WordPress/WordPress-Coding-Standards.git` |
| `PHPCSUtils` | 1.2.3 | `5f35d9408c54d7b529501f3c688b6eae562aea1f` | `https://github.com/PHPCSStandards/PHPCSUtils.git` |
| `PHPCSExtra` | 1.5.1 | `39467533fdb742446d68c1d10ac33d625ee0311c` | `https://github.com/PHPCSStandards/PHPCSExtra.git` |
| `PHPCompatibility` | 9.3.5 | `9fb324479acf6f39452e0655d2429cc0d3914243` | `https://github.com/PHPCompatibility/PHPCompatibility.git` |
| `PHPCompatibilityWP` | 2.1.8 | `7c8d18b4d90dac9e86b0869a608fa09158e168fa` | `https://github.com/PHPCompatibility/PHPCompatibilityWP.git` |
| `PHPCompatibilityParagonie` | 1.3.4 | `244d7b04fc4bc2117c15f5abe23eb933b5f02bbf` | `https://github.com/PHPCompatibility/PHPCompatibilityParagonie.git` |
| `wordpress-stubs` | v7.1.2 | `6926c5156431a3ff909d43faa16a92a0bc0c2428` | `https://github.com/php-stubs/wordpress-stubs.git` |

## Steps
1. **PHP**: if `php` is not on PATH, the user is root and `apt-get` exists, run `apt-get update -qq` then `apt-get install -y -qq php-cli php-xml php-mbstring`. Report `php: <version>`. Still no `php`: report "php: NOT AVAILABLE (PHP checks will be NOT RUN)" and stop (this is not a failure of the recipe).
2. **Fetch a phar** (`phpcbf.phar`, `phpcs.phar`, later `phpstan.phar`): if the file exists and its SHA-256 equals the pin, keep it. Otherwise delete it, download the pinned URL with `curl -fsSL --proto '=https' --tlsv1.2` to `<file>.part`, compare the SHA-256: a mismatch deletes the part and reports "REJECTED <file>: SHA-256 does not match the pin"; a match renames it into place and reports "installed <file> <version> (sha256 verified)". A failed download reports "download failed: <file>".
3. **Clone a pin** (the six standards, later `wordpress-stubs`): if `<dir>/.git` exists and `git rev-parse HEAD` equals the pinned commit, keep it. Otherwise `git clone --depth 1 --branch <tag> <repository>` into `<dir>.part`; the cloned `HEAD` must equal the pinned commit (else delete it and report "REJECTED <dir>: commit does not match the pin"); then replace `<dir>` with it and report "cloned <dir> <tag> (commit verified)". A failed clone reports "clone failed: <dir>".
4. **PHPCS**: fetch `phpcbf.phar` and `phpcs.phar`; clone `WordPress-Coding-Standards`, `PHPCSUtils`, `PHPCSExtra`, `PHPCompatibility`, `PHPCompatibilityWP`, `PHPCompatibilityParagonie`. When `phpcs.phar` exists, run `php phpcs.phar --config-set installed_paths <T/dir for each cloned standard, comma separated>` and report "phpcs: <version> (WordPress, PHPCompatibilityWP)"; otherwise "phpcs: NOT AVAILABLE".
5. **PHPStan**: fetch `phpstan.phar` and clone `wordpress-stubs`. When both are in place report "phpstan: <version> (with wordpress-stubs, no extension)", otherwise "phpstan: NOT AVAILABLE".
6. **WP-CLI**: report `wp-cli: <version>` when `wp` exists, otherwise "wp-cli: NOT AVAILABLE (Plugin Check will be NOT RUN)".
