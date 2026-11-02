---
name: fswp-theme-developer
description: Theme build stage of Full-Stack WP Developer. Builds custom WordPress themes - block themes (theme.json, templates, template parts, patterns, style variations), classic themes (template hierarchy, functions.php, theme supports), hybrids, and child themes - with accessibility, escaping, and directory readiness built in, plus a scaffold script. Invoked by fswp-developer after an approved PRD for a new theme; consult directly for a specific theme pattern. For changes to an existing theme use fswp-maintainer.
metadata:
  version: '0.3.0'
  author: "@wasimness"
  company: SyncWin
  license: MIT
---

# FSWP Theme Developer

**Foundational (always applied):** `fswp-developer/references/lean-coding.md` (write less, reuse first), `fswp-developer/references/coding-standards.md` (coding standards, docs, i18n, accessibility), and `fswp-security-engineer` (input, output, authorization).

Executes an approved theme PRD (`fswp-architect`). A theme controls presentation. Features that must survive a theme switch (post types, integrations, business logic) belong in a plugin (`fswp-plugin-developer`); say so instead of hiding them in `functions.php`.

## Decide the type first

| Type | Choose when | Core files |
|---|---|---|
| Block theme | Site Editor editing wanted; new builds by default | `style.css` (header only), `theme.json`, `templates/index.html`, `parts/`, `patterns/`, `styles/` |
| Classic theme | Needs PHP templates and custom logic per template, or must support old WordPress | `style.css`, `index.php`, `functions.php`, template files |
| Hybrid | Classic templates plus `theme.json` for settings and editor styles | Classic files + `theme.json` |
| Child theme | Adjust a parent without forking it | `style.css` with `Template:` header, `functions.php`, overrides only |

Default to a block theme for new builds unless the PRD needs otherwise. Block themes need WordPress 5.9 or newer; check the current `theme.json` schema version and its minimum WordPress version in the docs before pinning `Requires at least`.

## Workflow

1. **Scaffold**: `python3 scripts/scaffold_theme.py --help`, then generate the skeleton (block, classic, or child). Run `fswp-qa-engineer/scripts/run_gate.sh <dir> <min-php> --fix` once.
2. **Design tokens**: define palette, typography, spacing, layout widths, and border/shadow presets in `theme.json` (block/hybrid) or in CSS custom properties (classic). Use presets in templates and patterns instead of hard-coded values.
3. **Templates**: build the hierarchy the PRD needs (front page, home, single, page, archive, search, 404, plus any custom templates). Reuse template parts for header, footer, and repeated sections.
4. **Patterns**: register reusable layouts as files in `patterns/` (header comment: Title, Slug, Categories, optional Keywords, Viewport Width, Block Types). No remote images.
5. **Style variations**: JSON files in `styles/` for alternate looks; keep them small overrides of `theme.json`.
6. **Custom blocks or interactivity** the theme really needs: `fswp-block-developer`. Otherwise prefer core blocks.
7. **Assets**: enqueue with `wp_enqueue_scripts` (classic) or `theme.json`/`add_editor_style` (block); bundle fonts locally (`fontFace` entries) with their licenses; no CDN links.
8. **Security, i18n, accessibility**: escape every output, translate every string, meet the accessibility rules (`fswp-security-engineer`, `fswp-developer/references/coding-standards.md`, `references/theme-i18n-a11y.md`). Use named, prefixed functions for hooks (never closures), a prefix of at least four letters, and `array()` syntax per the coding standards.
9. **Directory readiness** if the target is the WordPress.org theme directory: `fswp-release-manager` (`references/theme-requirements.md`), then run `python3 ../fswp-qa-engineer/scripts/theme_check.py <dir> --directory`. Themes may not contain custom post types, blocks, shortcodes, roles, contact methods, or mime types: those belong in a plugin. Theme names may not contain "WordPress", "Theme", or "Twenty".

Stop and hand to `fswp-qa-engineer`.

## Classic theme essentials

`add_theme_support()` for `title-tag` and `automatic-feed-links` (both required by the directory), plus `post-thumbnails`, `html5`, `responsive-embeds`, `wp-block-styles`, and `editor-styles`; `language_attributes()`, `body_class()`, `post_class()`, `wp_link_pages()`, and `edit_theme_options` for option permissions; `register_nav_menus`; `wp_head()`, `wp_body_open()`, `wp_footer()` present; `get_template_part()` for repeated parts; template tags over direct queries; `wp_reset_postdata()` after secondary loops; content width and image sizes declared.

## Child themes

Enqueue the parent stylesheet and the child stylesheet with correct dependencies; override single templates rather than copying the parent; keep the child's version independent of the parent's; do not copy the parent's `functions.php`.

## Deliver

Installable `{theme-slug}.zip` with the theme folder at the root, `readme.txt`, `screenshot.png` (at most 1200x900, 4:3 ratio), license notes for every bundled asset, and a summary of manual steps owed. References: `references/block-theme.md`, `references/theme-i18n-a11y.md`.
