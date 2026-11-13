# Recipe: detect the WordPress project (read-only)

Do these steps with Read, Glob and Grep. Never write. The result is the triage report that planning starts from. Run it once on `<dir>` at the start of Update, Add-on and Core work.

## Inputs
- `<dir>`: the project folder. Not a folder: stop with "usage: folder required".

## Scan limits
- Skip these folders everywhere: `.git`, `node_modules`, `vendor`, `build`, `dist`, `.cache`.
- Look at no more than 4000 files. If you hit that limit, add the note "file limit reached; results are partial".
- Read at most the first 400,000 bytes of any file. Header fields are read from the first 8192 characters only.
- A header field is a line matching `^[ \t/*#@]*<Key>:[ \t]*(.+)$` (case-insensitive); the value is the trimmed text after the colon.

## Step 1: project type (first match wins)
1. **WordPress core**: both `wp-includes/version.php` and `wp-settings.php` exist, or `src/wp-includes/version.php` exists.
   - Version: from `src/wp-includes/version.php` (else `wp-includes/version.php`), the value of `$wp_version = '...'`.
   - Type `core-checkout` if the folder `tests/phpunit` exists, otherwise `wordpress-install`. Evidence note: "wp-includes/version.php found".
2. **Theme**: a root `style.css` has `Theme Name:` in its first 8192 characters.
   - Read the header fields Theme Name, Version, Requires at least, Requires PHP, Text Domain, Template, License.
   - Type: `child-theme` when `Template` is set; else `block-theme` when `theme.json` exists and a `templates/` folder exists; else `classic-theme`. Evidence note: "style.css with Theme Name header".
   - If `theme.json` exists, report its `version` value as `theme_json_version`; when it is not valid JSON, add the note "theme.json is not valid JSON".
   - Entry points: for each of `templates`, `parts`, `patterns`, `styles` that exists, the number of entries in it.
3. **Plugin**: otherwise take the `.php` files directly in the root (sorted by name). The first one with `Plugin Name:` in its first 8192 characters is the main file.
   - Read the header fields Plugin Name, Version, Requires at least, Requires PHP, Text Domain, License, Requires Plugins. Type `plugin`; evidence note "<file> has a Plugin Name header".
   - When `Requires Plugins` is set, the type is `plugin (add-on: declares required plugins)`.
4. None of these: type `unknown`.

## Step 2: tooling flags
Report which are present (by file name among the scanned files): `composer` (`composer.json`), `npm` (`package.json`), `phpcs` (`.phpcs.xml`, `.phpcs.xml.dist`, `phpcs.xml` or `phpcs.xml.dist`), `phpstan` (`phpstan.neon` or `phpstan.neon.dist`), `phpunit` (`phpunit.xml` or `phpunit.xml.dist`), `wp_env` (`.wp-env.json`), `git` (a `.git` folder in `<dir>`), `readme_txt` (`readme.txt`). Also count the files whose path ends in `block.json`.

## Step 3: extension points (from the first 1500 `.php` files)
Collect, with Grep over the PHP files:
- **Hooks**: `add_action(` or `add_filter(` followed by a quoted hook name (letters, digits, `_`, `-`, `/`, `.`). Report the number of distinct hooks and a sample of the first 15 in sorted order.
- **REST routes**: `register_rest_route( 'ns', 'route'`; report each as `/<ns>/<route>` with the outer slashes trimmed, sorted.
- **Post types**: `register_post_type( 'slug'`, sorted.
- **Shortcodes**: `add_shortcode( 'tag'`, sorted.
- **AJAX actions**: `wp_ajax_<name>` and `wp_ajax_nopriv_<name>`; report `<name>`, sorted.
- Also report the number of PHP files and the number of files scanned.

## Output
Print, omitting empty entries:
```
Path: <absolute dir>
Type: <type>
header / core_version / theme_json_version / main_file: <values that exist>
Tooling: <names that are present, comma separated, or "none detected">
block.json files: <n>
<entry point name>: <value>      (templates, parts, patterns, styles, hooks_used, rest_routes, post_types, shortcodes, ajax_actions; the hook sample is not printed here)
note: <each evidence note>
```
When the user wants machine-readable output, give the same fields as one JSON object (`path`, `type`, `evidence`, `tooling`, `entry_points` including `hook_sample`, `header`, `core_version`, `theme_json_version`, `main_file`, `block_json_files`, `php_files`, `files_scanned`).
