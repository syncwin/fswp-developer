# Recipe: scaffold a theme skeleton

Do these steps with Read, Write and Bash. Values you do not have are left out of the header; nothing is invented. The exact file bodies are in `scaffold_theme_files.md` (block, child, and the files for every type) and `scaffold_theme_classic_files.md` (classic), same folder.

## Inputs
- `name` (required), `slug` (required, becomes the folder and the text domain), `type` (required): `block`, `classic` or `child`.
- `parent`: required for `child` (the parent theme's folder name).
- `author`, `author-uri`, `theme-uri`, `description` (default: the name).
- `tested-up-to`: pass only after testing on that WordPress version; otherwise the line is omitted.
- `min-wp` (default `6.4`), `min-php` (default `7.4`).
- `out`: output folder (default current). `zip` (optional): also zip the theme folder.

## Checks before writing
1. `type` is `child` and no `parent`: stop with "--parent is required for a child theme".
2. Count the letters (`a-z`, `A-Z`) in `slug`. Fewer than 4: stop with "slug needs at least 4 letters: the directory requires a prefix of four or more letters".
3. Lower-case name contains `wordpress` or `theme`, or starts with `twenty`: warn "the directory does not allow WordPress, Theme, or Twenty* in a theme name; consider a different name" and continue.
4. `<out>/<slug>` already exists: stop with "refusing to overwrite <path>".

## Header (`style.css`)
Write `/*`, then these lines in order (skip a line when its value is missing), then `*/`:
`Theme Name: <name>`; `Theme URI: <theme-uri>`; `Author: <author>`; `Author URI: <author-uri>`; `Description: <description or name>`; for child `Template: <parent>`; `Version: 0.0.1`; `Requires at least: <min-wp>`; `Tested up to: <tested-up-to>`; `Requires PHP: <min-php>`; `License: GPL-2.0-or-later`; `License URI: https://www.gnu.org/licenses/gpl-2.0.html`; `Text Domain: <slug>`.
`style.css` holds nothing else. Use `<px>` = slug with `-` turned into `_` for function names.

## Files per type (bodies in `scaffold_theme_files.md` and `scaffold_theme_classic_files.md`)
- **block**: `style.css`, `theme.json`, `templates/index.html`, `parts/header.html`, `parts/footer.html`, `functions.php` (the PHP head only: file doc block with `Theme setup.` and the `ABSPATH` guard).
- **classic**: `style.css`, `functions.php` (head with `Theme setup.`, then `<px>_setup` on `after_setup_theme` with the supports and the `primary` menu, and `<px>_enqueue_styles` on `wp_enqueue_scripts`), `header.php`, `footer.php`, `index.php`, `template-parts/content.php`, `template-parts/content-none.php`.
- **child**: `style.css` (with `Template:`), `functions.php` (head with `Child theme setup.`, then `<px>_enqueue_styles` that enqueues the parent style from the template directory and the child style depending on it).
- **every type**: `readme.txt` (name, min versions, `Stable tag: 0.0.1`, GPL v2 license lines, description, changelog `0.0.1`), plus the documentation standard files: `README.md`, `CHANGELOG.md` (`[Unreleased]` and `[0.0.1] - <today>` with `- Initial <type> theme scaffold.`), `docs/setup.md`, `docs/architecture.md`, `docs/ops.md`, `docs/features/README.md`, `docs/features/templates.md`.

`docs/` files carry `FILL IN:` markers: `fswpdevops-theme` fills them from the approved PRD before delivery, and the docs gate fails on a `FILL IN:` left in a non-planned feature file.

## After writing
1. `zip` requested: zip the theme folder as `<out>/<slug>.zip` with the folder name as the top entry.
2. Report the created path.
3. Run the QA gate (`fswpdevops-qa/references/run_gate.md`), then `theme_check` with the directory option if the target is the WordPress.org Theme Directory (`fswpdevops-qa/references/theme_check.md`).
