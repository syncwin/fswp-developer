# block.json reference (verified 2026-09-28 against the Block Editor Handbook)

Recommended since WordPress 5.8 as the canonical way to register blocks for PHP and JavaScript. Benefits: assets listed in `style`/`script`/`viewStyle`/`viewScript` load only when the block is on the page; the Block Type REST endpoint sees server-registered blocks; the plugin directory can detect the blocks.

| Property | Notes | Since |
|---|---|---|
| `$schema` | `https://schemas.wp.org/trunk/block.json` enables editor validation | 5.8 |
| `apiVersion` | Current is 3; default 1 if omitted | 3 in 6.3 |
| `name` | Required. `namespace/block-name`, lowercase alphanumerics and dashes, begins with a letter | |
| `title` | Required, translatable | |
| `category` | `text`, `media`, `design`, `widgets`, `theme`, `embed`, or a registered custom category | |
| `parent` | Block may only be a direct child of the listed blocks | |
| `ancestor` | Block may sit anywhere inside the listed blocks | 6.0 |
| `allowedBlocks` | Which blocks may be direct children | 6.5 |
| `icon` | A Dashicon slug (SVG can be given in JavaScript) | |
| `description`, `keywords` | Translatable | |
| `version` | Block version; used for asset cache-busting; WordPress version is used if omitted | 5.8 |
| `textdomain` | Text domain for translating the metadata | 5.7 |
| `attributes` | Data the block stores; give `type`, `default`, and `source`/`selector` when parsed from markup | |
| `providesContext` / `usesContext` | Share attributes with descendants and read ancestor context | |
| `selectors` | Custom CSS selectors for theme.json global styles | 6.3 |
| `supports` | Editor features (align, color, spacing, typography, anchor, interactivity, and more) | |
| `styles` | Block style variants (a class on the wrapper) | |
| `example` | Preview data for the inserter | |
| `variations` | Preconfigured versions of the block; a PHP file returning an array can generate them | 5.9; PHP file 6.7 |
| `blockHooks` | Auto-insert this block next to another block type (`before`, `after`, `firstChild`, `lastChild`) | 6.4 |
| `editorScript` | Editor only | |
| `script` | Editor and front end | |
| `viewScript` | Front end only, classic script | 5.9 |
| `viewScriptModule` | Front end only, script module (Interactivity API) | 6.5 |
| `editorStyle` | Editor only | |
| `style` | Editor and front end | |
| `viewStyle` | Front end only | 6.5 |
| `render` | `file:./render.php`, exposes `$attributes`, `$content`, `$block` | 6.1 |

Asset values: `file:./relative.js` paths (prefix `file:` is required), or handles/IDs of assets you registered yourself with `wp_register_script`, `wp_register_script_module`, `wp_register_style`. A build step writes `name.asset.php` next to each script and WordPress reads its `dependencies` and `version` automatically (this is what `@wordpress/scripts` generates).

Client-side properties that stay in JavaScript: `edit`, `save`, `transforms`, `deprecated`, and a few others.

Always check the current handbook page for new properties before assuming this table is complete.
