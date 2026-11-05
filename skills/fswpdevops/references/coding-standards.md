# Coding standards, i18n, and accessibility (foundational, always applied)

WordPress coding standards are mandatory for Core and recommended for plugins and themes; they cover style plus interoperability, translatability, and security practices. This reference states them as working rules. It was checked against the PHP coding standards page on developer.wordpress.org (2026-09-28). The other standards pages are listed in `fswpdevops/references/official-docs.md`; open them before enforcing a detail you are unsure about.

## PHP essentials (verified)

| Area | Rule |
|---|---|
| Tags | Full `<?php ?>` only; no short tags; prefer omitting the closing tag at end of file |
| Indentation | Real tabs at line start; spaces only for mid-line alignment |
| Spacing | Spaces inside parentheses and around operators: `if ( $a === $b ) {`; none between `!` and its operand except one space after: `! $foo` |
| Braces | Always, even for one statement; `elseif`, never `else if` |
| Arrays | **Long syntax** `array( 1, 2 )`; multi-item arrays one item per line with trailing comma |
| Conditions | Yoda style for `==`, `!=`, `===`, `!==`: `if ( 'x' === $var )`; no assignments in conditions; strict comparisons |
| Ternary | Test for true; the short `?:` form is not allowed |
| Quotes | Single quotes unless interpolating |
| Names | Functions, variables, hooks: lowercase with underscores. Classes, traits, interfaces, enums: `Capitalized_Words_With_Underscores`. Constants: `UPPER_CASE` |
| Files | Lowercase, hyphens. Class file: `class-my-class.php`. One class, trait, interface, or enum per file |
| Includes | `require_once` (no parentheses) for required files |
| Namespaces | Encouraged in plugins and themes with a unique `Vendor\Project` prefix; `wp` and `WordPress` are reserved; hook names and `define()` constants still need manual prefixes |
| Visibility | Always declare; no `var`. Modifier order: `abstract`/`final`, visibility, `static` |
| Types | Type declarations only as far as the minimum PHP version allows (return types 7.0, nullable and `void` 7.1, property types 7.4, union types 8.0) |
| Never | `eval()`, `create_function()`, `goto`, backtick shell, `extract()`, the `/e` regex flag, `@` error suppression as a habit |
| Closures | Fine as callbacks for functions like `preg_replace_callback`, but **not** as action or filter callbacks, because they cannot be removed with `remove_action()`. Use named functions or methods |
| Database | Prefer core functions to raw SQL; `$wpdb->prepare()` with `%d`, `%f`, `%s`, and `%i` (identifiers), placeholders unquoted; SQL keywords uppercase |
| Function flags | Prefer descriptive string values or an `$args` array to bare booleans |
| Dynamic hooks | Interpolate with braces: `do_action( "{$status}_{$type}", $id )` |

Automated check: PHPCS with the WordPress standard (`fswpdevops-ci`). Match the existing file's style when editing older code that predates a rule; do not reformat unrelated lines.

## Prefixing

Everything global needs a unique prefix: functions, classes (or a namespace), constants, options, post meta and user meta keys, transients, script and style handles, hook names, REST namespaces, cron hooks, custom post type and taxonomy slugs, shortcode tags, block namespaces. Themes need at least four letters. Never `wp_`, `_`, or a common word.

## PHP inline documentation

- File header DocBlock where useful (`@package`), a DocBlock for every function, class, method, property, constant that is not obvious, and for every hook you fire.
- Function DocBlock: a short summary, optional description, then `@since` (version introduced), `@param type $name Description.`, `@return type Description.`; `@see`, `@link`, `@throws`, `@global` where they apply.
- Hook DocBlock immediately above `do_action`/`apply_filters`: `Fires...`/`Filters...` summary, `@since`, and one `@param` per argument.
- Comments explain **why**, not what the code plainly says. Wrong comments are worse than none: update them with the code. Use `// translators:` comments for placeholders.

## JavaScript, CSS, HTML

- **JavaScript:** tabs; single quotes; spaces inside brackets and parentheses; `===`; always semicolons; `const`/`let`, no `var` in new code; ESLint with `@wordpress/eslint-plugin` (via `@wordpress/scripts`); no jQuery in new code unless needed; JSDoc for functions.
- **CSS:** tabs; each selector on its own line; one declaration per line; lowercase hex, short form where possible; unitless line-height and 0; logical grouping of properties (display, position, box model, color and type, other); selectors as flat and low-specificity as practical; `rem`/relative units for type and spacing; comments for sections; Stylelint via `@wordpress/scripts`. Block themes: prefer `theme.json` over custom CSS.
- **HTML:** lowercase tags and attributes, double-quoted attribute values, valid and well-formed nesting, semantic elements before `div`, and the escaping rules for anything dynamic.

## Internationalization (i18n)

See `fswpdevops/references/i18n.md` for the full function table and JS workflow. Non-negotiable rules:

1. One text domain per plugin or theme, equal to its slug, declared in the header (plus `Domain Path` if not `/languages`). Literal strings only: no variables as the domain or the text.
2. Wrap every user-facing string: `__()`, `_e()`, `_x()`, `_n()`, and escaping forms `esc_html__()`, `esc_attr__()`, `esc_html_e()`.
3. Never concatenate sentences or split them across calls. Use `sprintf()`/`printf()` with placeholders, and add a `/* translators: %s: ... */` comment above.
4. Plurals with `_n()`; ambiguous words with `_x()` context.
5. JavaScript uses `@wordpress/i18n` and `wp_set_script_translations()`; block.json `textdomain` translates block metadata.
6. Generate the `.pot` with the command-line `wp i18n make-pot`; WordPress.org-hosted plugins and themes get translations from translate.wordpress.org.
7. Support RTL: logical CSS properties, and provide RTL styles or use `wp_style_add_data( $handle, 'rtl', 'replace' )`.

## Accessibility (a11y)

See `fswpdevops/references/accessibility.md`. Targets: WCAG 2.2 level AA for everything the plugin or theme outputs; WordPress admin-UI patterns for admin screens; the directory's accessibility-ready requirements when a theme uses that tag. Non-negotiable rules:

1. Everything works by keyboard alone, in a logical order, with a visible focus indicator.
2. Every form control has a programmatic label; errors are announced and tied to their fields.
3. Meaningful images have `alt`; decorative images have empty `alt`; icon-only controls have accessible names.
4. Use native elements (`button`, `a`, `label`, `fieldset`) before ARIA; add ARIA only when no native element fits, and keep state (`aria-expanded`, `aria-current`) in sync.
5. Headings in order, landmarks present, a skip link where there is something to skip.
6. Color contrast at least 4.5:1 for text and 3:1 for large text and UI components; never color alone to convey meaning.
7. Respect `prefers-reduced-motion`; no autoplay motion; content reflows at 320px and works at 200% zoom.
8. Live updates use `wp.a11y.speak()` (admin) or an appropriate live region.

## Documentation standard (single source; other skills link here)

Every plugin, theme, add-on or Core-patch project this plugin builds has these files from the first scaffold and keeps them current. A change that touches code updates the matching docs in the same change, never later. `fswpdevops-qa/scripts/docs_gate.py` enforces it.

- **`README.md` + `docs/`**: short. `README.md` = what it is, install, link to `docs/`. `docs/setup.md` (install, dev environment, tests), `docs/architecture.md` (files, hooks, data, extension points), `docs/ops.md` (build, release, config, troubleshooting, uninstall). WordPress.org `readme.txt` stays as well; its `== Changelog ==` mirrors released sections of `CHANGELOG.md`.
- **`CHANGELOG.md`**: Keep a Changelog 1.1.0 + Semantic Versioning 2.0.0. Starts at `0.0.1`. Top section `## [Unreleased]`; released sections `## [X.Y.Z] - YYYY-MM-DD`; categories only `### Added`, `### Changed`, `### Deprecated`, `### Removed`, `### Fixed`, `### Security`. One line per user-visible change, written for users. Pre-1.0 (`0.y.z`) = beta. `1.0.0` only when the owner says so.
- **`docs/features/`**: one file per feature, `docs/features/<feature-slug>.md` (slug = lowercase, hyphens; the folder under `includes/`, `inc/`, `src/`, `modules/`, `features/` or `blocks/`), plus `docs/features/README.md`, an index table:

  `| Feature | Status | Since | File |` (one row per feature; Status and Since equal the feature file's)

- **Feature file template.** Lean, no fluff, ASCII only, understandable with no visual reference, so a new agent or user can learn the feature from it alone:

```
# <Title>

**Status:** planned|beta|stable|deprecated | **Since:** X.Y.Z | **Updated:** X.Y.Z

## Context
Why it exists, who uses it.

## Behaviour
What the user sees and does; states; edge cases; errors; permissions and capabilities.

## How it works
Flow, hooks, classes and files, data (options, tables, meta), APIs and routes, config.

## UI
Text description, no screenshots needed: layout, controls, states.

## Limits & known issues

## History
- X.Y.Z: one-line change
```
- **When code changes** (any plugin or theme PHP, JS/TS under `src/` or `blocks/`, block-theme templates, parts, `theme.json`): add a line under `## [Unreleased]`; update the feature file of every touched feature (body, `Updated`, a History line) and the index row if Status or Since changed; add file + index row for a new feature. Shared code (files directly in `includes/`, `admin/`, the main plugin file) needs the changelog line only. Pure refactors skip the feature-file update: a new `### Changed` line or a line containing `docs: none` under `[Unreleased]` waives it (the changelog line is still required).
- **Release** (`fswpdevops-release`): `[Unreleased]` becomes `## [X.Y.Z] - date`, a fresh empty `[Unreleased]` stays on top; header `Version`, version constant, `Stable tag` and `readme.txt` changelog move together.
- **Evidence for AI+ contract adoption** (no `contract.yaml` here yet): `changelog_unreleased_updated`, `feature_docs_updated`, `feature_index_current`, `docs_gate_exit_code` = the rows and exit code of `docs_gate.py`.

## How other skills use this

Every build and maintenance skill follows it while writing. `fswpdevops-qa` runs PHPCS for the machine-checkable parts. `fswpdevops-reviewer` reports violations that affect behavior, translation, accessibility, or maintainability, not pure style nits.
