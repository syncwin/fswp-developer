# Recipe: plugin house-rules check (qa_check)

Do these checks with Read, Glob and Grep on a plugin folder `<dir>`. Each check is a status plus a one-line detail. Statuses: PASS, FAIL, WARN (worth a look, never fails the run), SKIP (could not run; it is never a pass, report it as NOT RUN). The run FAILs when any check is FAIL.

## Scope
- Skip these folders: `vendor`, `node_modules`, `tests`, `baseline`, `.git`, `foundation` (the bundled design framework; only the fonts check, 14, looks inside `foundation`).
- `php` = all `.php` files outside the skipped folders; `allphp` = their text joined. If there are none: FAIL "PHP files" ("no .php files found") and stop.
- `code` = `allphp` with block comments, `//` comments (not preceded by `:`, `'` or `"`) and whole-line `#` comments removed. Only check 5 uses it; the other checks read the raw text.

## Checks

**1. ABSPATH guard on every PHP file.** Every file except `uninstall.php` and `index.php` must contain `ABSPATH` in its first 1500 characters. FAIL lists up to 8 offenders.

**Main file and versions.** The main file is the first PHP file with a `Plugin Name:` header line (at the start of a line, optionally after `*`) in its first 3000 characters. None: FAIL "Main plugin file" ("no file with a 'Plugin Name:' header"). Otherwise, using the first 3000 characters as the header:
- Collect `header Version` (`Version:` value), every `define( 'X_VERSION', 'value' )` constant (name ending `_VERSION`, anywhere in `allphp`), and, when `readme.txt` exists, `readme Stable tag` (`Stable tag:` value; missing counts as none). No `readme.txt`: SKIP "readme.txt Stable tag" ("readme.txt not present (fine for private builds)").
- FAIL "Version consistency" (detail: the map of name to value) when any collected value is missing or there is more than one distinct value; otherwise PASS with the version.
- No version constant found: WARN "Version constant" ("no PREFIX_VERSION constant found").
- `Plugin URI` or `Author URI` whose value contains `example.com`, `example.org` or `example.net`: FAIL "Placeholder URI" (field and value).
- `Author:` value `Unknown`: WARN "Author header" ("still 'Unknown'").

**2. No example.com placeholders.** Any PHP file or `readme.txt` containing `example.com`, `example.org` or `example.net`: FAIL, up to 8 files.

**3. No remote assets, CDN scripts, or CDN fonts.** In `.php`, `.js`, `.css`, `.html`, `.jsx`, `.ts`, `.tsx` files, FAIL (up to 6 distinct hits, `file (reason)`) on any of:
- these hosts: `fonts.googleapis.com`, `fonts.gstatic.com`, `cdnjs.cloudflare.com`, `cdn.jsdelivr.net`, `unpkg.com`, `ajax.googleapis.com`, `use.typekit.net`, `kit.fontawesome.com`, `use.fontawesome.com`, `stackpath.bootstrapcdn.com`, `maxcdn.bootstrapcdn.com`, `code.jquery.com`;
- `wp_enqueue_script`, `wp_enqueue_style`, `wp_register_script` or `wp_register_style` with an `http://` or `https://` string argument before the statement ends (`remote enqueue`);
- a CSS `@import` of an `http://` or `https://` URL.

**4. REST permission callbacks.** For every `register_rest_route(` call (take the text to its matching closing parenthesis, aware of strings and comments), at `file:line`:
- no `permission_callback` in the call: FAIL "Every REST route has permission_callback" (up to 6 locations);
- the call uses `__return_true`: look at the line holding it and the 3 lines above; if none of them has a comment marker (`//`, `/*`, a `*` followed by space, `#`), FAIL "__return_true routes are commented as public" (up to 6). A public route needs a comment saying why.
Report both checks, PASS when they have no offenders.

**5. DB upgrade hook.** When `code` contains `dbDelta(` or `CREATE TABLE`: PASS "DB upgrade check outside activation" only if `code` also has `plugins_loaded`, `admin_init` or `'init'` and one of `maybe_upgrade`, `db_version`, `DB_VERSION` (case-insensitive); else FAIL ("dbDelta used but no version check on plugins_loaded/admin_init"). No tables: SKIP "DB upgrade check" ("no custom tables detected").

**6. Shortcode assets enqueued inside the callback, not site-wide.** FAIL with the problems joined by `; ` when:
- `has_shortcode(` is used anywhere (it misses builder content; enqueue inside the shortcode callback);
- a function registered with `add_action( 'wp_enqueue_scripts', 'fn' )` (also `array( $this, 'fn' )` or `[ $this, 'fn' ]`) has a body that calls `wp_enqueue_script` or `wp_enqueue_style` with no `if (` in it while `add_shortcode(` exists in the plugin ("<file>: 'fn' enqueues unconditionally site-wide while a shortcode exists").

**7. No eval, create_function, extract.** FAIL when `eval(`, `create_function(` or `extract(` appears in `allphp` not directly preceded by a letter, `_`, `>` or `:` (so method calls and longer names do not count).

**8. Lifecycle basics.**
- `uninstall.php` exists: PASS "uninstall.php guarded by WP_UNINSTALL_PLUGIN" when it contains `WP_UNINSTALL_PLUGIN`, else FAIL. Missing: FAIL "uninstall.php present" ("missing").
- `load_plugin_textdomain` anywhere in `allphp`: PASS, else WARN "load_plugin_textdomain called".

**9. No h1 to h3 in shortcode or block markup.** PHP files under a `public/` folder matching `<h1`, `<h2` or `<h3` followed by whitespace or `>`: FAIL (up to 6). Headings belong to the page, not the widget.

**10. Units.** Over the plugin's own `.css` files:
- FAIL "No 62.5% root font-size rebasing in plugin CSS" when an `html { ... font-size: 62.5% }` rule exists.
- WARN "Type/spacing/radius in rem, not px" when `font-size`, `line-height`, `gap`, `padding`, `margin` or `border-radius` has a value with a two-or-more-digit `px` number (up to 6 files).

**11. JS translations registered.** Own JS = `.js`, `.jsx`, `.ts`, `.tsx` files whose path does not contain `.min.`, `build` or `dist`. Present: PASS when `wp_set_script_translations` appears in the PHP, else WARN ("own JS present but no wp_set_script_translations()"). None: SKIP.

**12. Source ships with compiled output.** When a `build/` or `dist/` folder exists in the root: PASS only if `src/` exists, `package.json` exists and one lockfile exists (`bun.lock`, `bun.lockb`, `package-lock.json`, `yarn.lock` or `pnpm-lock.yaml`); else FAIL "Source, package.json and lockfile ship with compiled output". No such folder: SKIP.

**13. Feature documentation present and filled.** Applies when the root has an `includes/` or `admin/` folder, or any PHP matches `add_shortcode`, `register_rest_route` or `register_post_type`; otherwise SKIP ("no feature classes detected").
- `docs/features/` missing while `docs/` holds other Markdown files besides `README.md`, `setup.md`, `architecture.md`, `ops.md`: WARN (legacy `docs/<feature>.md`; move with `git mv docs/<f>.md docs/features/` and add the index and template).
- `docs/features/` missing otherwise: FAIL ("no docs/features/ folder found (scaffold generates stubs; they were removed or build skipped them)").
- Exists with no feature file (Markdown other than `README.md`): FAIL ("docs/features/ exists but has no feature files").
- Otherwise FAIL "docs/features/ feature documentation completed" listing every file that contains `FILL IN:` and does not contain `**Status:** planned`; else PASS ("<n> doc file(s), all filled").

**14. Bundled fonts carry a license.** When `.woff2`, `.woff`, `.ttf` or `.otf` files exist (this check also looks in `foundation`): PASS if any file anywhere in the tree has a name matching `OFL`, `LICENSE` or `licen[cs]e` (case-insensitive), else WARN "Bundled fonts include a license file". No fonts: no result.

**15. Header and readme rules (official plugin handbook, verified 2026-09-28).**
- With a main file (header fields read case-insensitively from the first 3000 characters): `Description` of 140 characters or more ("Description is N chars (keep under 140)"); `Plugin URI` containing `wordpress.org` ("must be unique to the plugin, not a WordPress.org URL"); any of `Requires at least`, `Requires PHP`, `License`, `Text Domain` missing ("header field missing: X"). WARN "Plugin header fields follow the handbook" with the problems, else PASS.
- With a `readme.txt`: more than 5 comma-separated `Tags:`; `Stable tag: trunk` ("prohibited for new plugins"); `Tested up to:` that is not a plain version number (`7.0` or `7.0.1`); the file over 10240 bytes ("move older changelog to changelog.txt"); the first descriptive line in the header block (before the first `== ` heading, ignoring `Key: value` lines and the title) longer than 150 characters ("short description over 150 chars"). WARN "readme.txt follows the WordPress.org standard" with the issues, else PASS.

## Output
One line per check: `[PASS|FAIL|WARN|SKIP] <check> :: <detail>`, then a summary line `N pass, N fail, N warn, N skipped (SKIP = not run, not a pass)`. The run fails when any check is FAIL. Report SKIP as NOT RUN in the gate table.
