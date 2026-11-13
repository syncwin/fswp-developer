# Recipe: theme house-rules check (theme_check)

Do these checks with Read, Glob and Grep on a theme folder `<dir>` (block, classic or child). Rules verified against the Themes Team handbook on 2026-09-28.

## Modes
- **Default**: real defects FAIL, directory-only rules WARN.
- **Directory mode** (the user asks for WordPress.org Theme Directory readiness): every rule tagged (D) below FAIL instead of WARN.
- Tags: (F) always FAIL when broken. (D) WARN by default, FAIL in directory mode. Plain WARN and SKIP never fail the run. SKIP is not a pass; report it as NOT RUN.
- The run FAILs when any check is FAIL.

## Scope
Skip these folders: `vendor`, `node_modules`, `.git`, `tests`, `baseline`. The theme folder name is the slug. Header fields come from the first 8192 characters of `style.css`: a line `^[ \t/*]*<Key>:[ \t]*(.+)$` (case-insensitive), value trimmed.

## Checks
1. **Theme type** (PASS, detail = type): `child` when `Template` is set; `block` when `theme.json` and a `templates/` folder both exist; otherwise `classic`.
2. **style.css present**: missing is FAIL. With it missing, every header below counts as missing.
3. **Core headers** (F): `Theme Name`, `Version`, `License`, `Text Domain` all present ("style.css core headers (Theme Name, Version, License, Text Domain)"; detail lists the missing ones).
4. **Directory headers** (D): `Author`, `Description`, `Requires at least`, `Tested up to`, `Requires PHP`, `License URI` all present (detail "missing: ... ('Tested up to' is only valid after a real test)").
5. **License is GPL-compatible** (F, only when `License` is set): the value contains `gpl` (any case).
6. **Text Domain equals the theme folder name** (D): passes when there is no Text Domain or it equals the slug.
7. **Theme name avoids WordPress / Theme / Twenty\*** (D): fails when the lower-case name contains `wordpress`, contains the whole word `theme`, or starts with `twenty`.
8. **Structure**:
   - block: `templates/index.html` exists (F) and `theme.json` exists (F).
   - classic: `index.php` exists (F).
   - child: PASS "Child theme declares parent" (detail the parent).
   - all types: `readme.txt` present, required by the directory (D).
9. **theme.json** (when present): it must parse as JSON and declare a `version` (F, "theme.json parses and declares version", detail `version=<value>`); a parse error is FAIL "theme.json parses" with the message.
10. **Screenshot**: the first of `screenshot.png`, `screenshot.jpg`, `screenshot.jpeg`.
    - Present: read the image size from the file header (PNG IHDR width and height; JPEG start-of-frame marker). Width at most 1200, height at most 900, and width/height within 0.02 of 4:3 (D, "Screenshot within 1200x900 and 4:3", detail `<w>x<h>`). Header unreadable: SKIP "Screenshot size" ("could not read image header").
    - Missing: (D) "screenshot.png present".
11. **Forbidden code** (F, "No eval / create_function / extract / shell execution"): in PHP files after removing `//` and `/* */` comments, a call to `eval`, `create_function`, `extract`, `goto`, `shell_exec`, `passthru`, `proc_open` or `popen`, or a backtick-quoted shell command on one line. Detail: up to 5 files.
12. **No plugin-territory features** (D): PHP using `register_post_type(`, `add_shortcode(`, `register_block_type(` or `register_block_type_from_metadata(`, `add_role(`, `user_contactmethods`, `upload_mimes`. Detail lists the labels (custom post types, shortcodes, custom blocks, custom roles, user contact methods, custom mime types), sorted.
13. **No closures as action or filter callbacks** (F): an `add_action(` or `add_filter(` whose arguments contain `function (` before the statement ends ("they cannot be removed"). PASS when none.
14. **No echo of raw request data** (F): `echo $_GET`, `$_POST`, `$_REQUEST` or `$_SERVER` anywhere in PHP (up to 5 files).
15. **Global functions carry a unique prefix of 4+ letters** (D): collect lower-case top-level `function name(` declarations from PHP files except `header.php` and `footer.php`. With any, each must start with the slug (hyphens as `_`) or with the slug's first segment letters (letters only, at least 4 of them). Detail: up to 5 offenders.
16. **Classic theme required calls** (D, classic only; "missing: ..."): across the PHP text, case-insensitive, all of `wp_head()`, `body_class()`, `wp_footer()`, `wp_body_open()`, `post_class()`, `wp_link_pages()`, `language_attributes()`, `add_theme_support( 'title-tag' )`, `add_theme_support( 'automatic-feed-links' )`, and a `<!DOCTYPE`. Also (D) a skip link: `skip-link`, `#content` or `#main` appears.
17. **No disallowed, hidden, or VCS files** (D): walking everything except `.git`, `.svn`, `.hg`, `.bzr` and `node_modules`, flag a file named (any case) `thumbs.db`, `desktop.ini`, `project.properties`, `project.xml`, `php.ini`, `dwsync.xml`, `error_log`, `web.config` or `favicon.ico`; a file with extension `.kpf`, `.sql`, `.lubith`, `.wie`, `.dat`, `.sh` or `.zip`; any file whose name starts with `.`; any `.xml` file other than `wpml-config.xml`, `loco.xml`, `phpcs.xml`. Also flag a `.git`, `.svn`, `.hg`, `.bzr` or `__MACOSX` entry in the theme root. Detail: up to 6.
18. **Remote resources** in `.php`, `.html`, `.css`, `.js`, `.json` files:
    - (F) "No CDN scripts or styles": `cdnjs.cloudflare.com`, `cdn.jsdelivr.net`, `unpkg.com`, `ajax.googleapis.com`, `use.typekit.net`, `kit.fontawesome.com`, `maxcdn.bootstrapcdn.com`, `stackpath.bootstrapcdn.com` (up to 5 files).
    - WARN "Hosted fonts referenced (directory tolerates Google Fonts; bundling locally is safer)" for `fonts.googleapis.com` or `fonts.gstatic.com`; otherwise PASS "No hosted-font references".
19. **package.json version** (F, only when `package.json` exists): its `version` equals the `style.css` `Version` (detail `<pkg> vs <css>`). Unparsable JSON: WARN "package.json parses".

## Output
One line per check: `[PASS|FAIL|WARN|SKIP] <check> :: <detail>`, then `N pass, N fail, N warn, N skipped (SKIP = not run, not a pass)`, with ` [directory mode]` appended in directory mode.
