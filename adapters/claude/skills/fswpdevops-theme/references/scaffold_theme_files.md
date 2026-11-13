# Theme scaffold file contents

Exact file bodies for `scaffold_theme.md`. Replace the angle-bracket tokens: `<name>`, `<slug>` (also the text domain and folder), `<px>` (slug with `-` turned into `_`, the function prefix), `<description>`, `<type>` (block, classic or child), `<parent>`, `<min-wp>`, `<min-php>`, `<date>` (today, YYYY-MM-DD). Everything between the fences is the file; files use LF and tabs for PHP indentation as shown.

## Block theme files

The classic theme files are in `scaffold_theme_classic_files.md`.

### `theme.json`

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "layout": { "contentSize": "720px", "wideSize": "1200px" },
    "color": { "palette": [
      { "slug": "base", "name": "Base", "color": "#ffffff" },
      { "slug": "contrast", "name": "Contrast", "color": "#111111" },
      { "slug": "primary", "name": "Primary", "color": "#1d4ed8" }
    ] },
    "typography": { "fluid": true, "fontSizes": [
      { "slug": "small", "name": "Small", "size": "0.875rem" },
      { "slug": "medium", "name": "Medium", "size": "1.125rem" },
      { "slug": "large", "name": "Large", "size": "clamp(1.5rem, 1.2rem + 1.2vw, 2rem)" }
    ] }
  },
  "styles": {
    "color": { "background": "var(--wp--preset--color--base)", "text": "var(--wp--preset--color--contrast)" },
    "elements": { "link": { "color": { "text": "var(--wp--preset--color--primary)" } } }
  },
  "templateParts": [
    { "name": "header", "title": "Header", "area": "header" },
    { "name": "footer", "title": "Footer", "area": "footer" }
  ]
}
```

### `templates/index.html`

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group"><!-- wp:query {"queryId":0,"query":{"perPage":10,"postType":"post","inherit":true}} -->
<div class="wp-block-query"><!-- wp:post-template -->
<!-- wp:post-title {"isLink":true} /-->
<!-- wp:post-excerpt /-->
<!-- /wp:post-template -->
<!-- wp:query-pagination /--></div>
<!-- /wp:query --></main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### `parts/header.html`

```html
<!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
<div class="wp-block-group"><!-- wp:site-title /--><!-- wp:navigation /--></div>
<!-- /wp:group -->
```

### `parts/footer.html`

```html
<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:paragraph {"fontSize":"small"} --><p class="has-small-font-size"><!-- wp:site-title {"isLink":false} /--></p><!-- /wp:paragraph --></div>
<!-- /wp:group -->
```

### `functions.php (block theme)`

```php
<?php
/**
 * Theme setup.
 *
 * @package <slug>
 */

defined( 'ABSPATH' ) || exit;
```

## Child theme files

### `functions.php (child theme)`

```php
<?php
/**
 * Child theme setup.
 *
 * @package <slug>
 */

defined( 'ABSPATH' ) || exit;

/**
 * Enqueues the parent and child stylesheets.
 *
 * @since 0.0.1
 */
function <px>_enqueue_styles() {
	$parent = wp_get_theme( get_template() );
	wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css', array(), $parent->get( 'Version' ) );
	wp_enqueue_style( '<slug>', get_stylesheet_uri(), array( 'parent-style' ), wp_get_theme()->get( 'Version' ) );
}
add_action( 'wp_enqueue_scripts', '<px>_enqueue_styles' );
```

## Files written for every type

`style.css` is only the header block built by `scaffold_theme.md`; no other CSS is written.

### `readme.txt`

```text
=== <name> ===
Requires at least: <min-wp>
Requires PHP: <min-php>
Stable tag: 0.0.1
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

== Description ==
<description>

== Changelog ==
= 0.0.1 =
* Initial version.
```

### `README.md`

```markdown
# <name>

<description>

More: [setup](docs/setup.md), [architecture](docs/architecture.md), [ops](docs/ops.md), [features](docs/features/README.md), [changelog](CHANGELOG.md).
```

### `CHANGELOG.md`

```markdown
# Changelog

Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/); versions: [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html). Pre-1.0 is beta.

## [Unreleased]

## [0.0.1] - <date>

### Added
- Initial <type> theme scaffold.
```

### `docs/setup.md`

```markdown
# Setup

1. Use a local WordPress site.
2. Put `<slug>` in `wp-content/themes/` and activate it.
3. Quality gate: `run_gate` and `docs_gate` from the fswpdevops-qa skill (recipes in its `references/`).
```

### `docs/architecture.md`

```markdown
# Architecture

- Type: <type> theme. Templates, parts, patterns and `theme.json` define the site.
- FILL IN: template hierarchy, style variations, patterns and any PHP as they appear.
```

### `docs/ops.md`

```markdown
# Ops

- Release: move `[Unreleased]` in CHANGELOG.md into the new version; `style.css` Version and readme `Stable tag` move together.
- Troubleshooting: FILL IN as issues are found.
```

### `docs/features/README.md`

```markdown
# Features

One file per feature. Keep this table current (status, since version).

| Feature | Status | Since | File |
|---|---|---|---|
| Templates and styles | beta | 0.0.1 | [templates.md](templates.md) |
```

### `docs/features/templates.md`

```markdown
# Templates and styles

**Status:** beta | **Since:** 0.0.1 | **Updated:** 0.0.1

## Context
FILL IN: what the site looks like and does, who it is for.

## Behaviour
FILL IN: each template type, what the visitor sees with real and with empty content, states, edge cases.

## How it works
FILL IN: templates, parts, patterns, `theme.json` settings and styles, any PHP hooks, config.

## UI
FILL IN: text description of layout, header, footer, navigation and responsive behaviour (no screenshots needed).

## Limits & known issues
None yet.

## History
- 0.0.1: first version
```
