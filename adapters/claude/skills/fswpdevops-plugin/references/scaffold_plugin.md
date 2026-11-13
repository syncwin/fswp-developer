# Recipe: scaffold a plugin folder

Do these steps with Read, Write and Bash. It only does mechanical placeholder substitution and file writing; architecture, security and content come from the other references. The template files are in `templates-core.md`, `templates-features.md`, `templates-ui.md` and `templates-readme.md` (same folder).

## Inputs
- `name` (required): human-readable plugin name, for example `Event Manager`.
- `prefix` (required): short unique prefix chosen for this project. Ask the user; there is no default.
- `description`: one line. Default `<name> plugin.`
- `author`: default `Unknown`.
- `plugin-uri`, `author-uri`: real URLs only. When not given, the header line is left out (never a placeholder domain).
- `noun`: primary domain noun for CPT, table and shortcode naming. Default `item`.
- `features`: comma-separated subset of `cpt,db,rest,cron,admin,frontend`. Default `admin,frontend`. Anything else: stop with "Unknown feature(s): ... valid: cpt, db, rest, cron, admin, frontend". Only requested features get their files; nothing unused is created (a settings-only plugin passes `admin`).
- `distribution`: `wporg`, `private` or `both`. Default `private`.
- `js-tier`: `vanilla` (default) or `alpine`. Use `alpine` only after the 5-point checklist in `frontend-output.md` triggered and the user confirmed it; this recipe does not decide that.
- `admin-tier`: `native` (default), `react` or `app`. It only records the choice. `app` is assembled by hand from `modern-app-stack.md` after its decision checklist; say so.
- `foundation-dir`: folder holding the user's current Atomic Framework files. Required whenever `features` includes `frontend`.
- `out`: output folder (the plugin folder is created inside it). Default the current folder.
- `zip` (optional): also produce `<slug>.zip` next to the folder.

## Derived values
- `slug` = lowercase of `<prefix>-<name>` with every run of characters outside `a-z0-9` replaced by one `-`, trimmed of leading and trailing `-`.
- `PREFIX` = prefix upper case. `Prefix` = prefix upper case too (class names are `ACME_Admin`). `prefix` = prefix lower case.
- `noun` = the noun slugified the same way as `slug`, with `-` turned into `_`.
- Plugin root = `<out>/<slug>/`.

## Placeholder substitution
Apply to each template's text in this order.

1. Block tokens, each on a line of its own (the whole line including its newline is replaced):
   - `{{FEATURE_LOADERS}}` becomes the loader block below, with trailing newlines removed, then one newline.
   - `{{ACT_DB}}`, `{{ACT_CRON}}`, `{{ACT_CPT}}`, `{{DEACT_CRON}}` become their block below, or nothing (the line disappears) when the feature is not requested.
   - `{{PLUGIN_URI_LINE}}` becomes ` * Plugin URI:        <plugin-uri>` plus newline, or nothing. `{{AUTHOR_URI_LINE}}` likewise with ` * Author URI:        <author-uri>`.
2. Single tokens: `{{PLUGIN_NAME}}` = name; `{{ONE_LINE_DESCRIPTION}}` = description; `{{AUTHOR}}` = author; `{{plugin-slug}}` = slug; `{{PREFIX}}` = PREFIX; `{{Prefix}}` = Prefix; `{{prefix}}` = prefix; `{{noun}}`, `{{code}}` and `{{job}}` = noun; `{{Plural Name}}` = name + `s`; `{{Singular Name}}` = name; `{{plural_name}}` = slug with `-` as spaces + `s`.
3. Any other `{{...}}` (readme.txt and README-private.md such as `{{Feature 1}}`, `{{tag1}}`, `{{Question}}`) stays for you to fill from the approved PRD. Never leave one in a delivered file, and never invent a value.

Let `R(f)` be the line `        require_once {{PREFIX}}_PLUGIN_DIR . 'includes/class-{{prefix}}-<f>.php';`.

Loader block (`{{FEATURE_LOADERS}}`), pieces appended in this order for the requested features:
- `db`: `R(db)`, then `        add_action( 'plugins_loaded', array( '{{Prefix}}_DB', 'maybe_upgrade' ) );`, then a blank line.
- `admin`: `        if ( is_admin() ) {`, `            require_once {{PREFIX}}_PLUGIN_DIR . 'admin/class-{{prefix}}-admin.php';`, `            new {{Prefix}}_Admin();`, `        }`, blank line.
- `frontend`: `        require_once {{PREFIX}}_PLUGIN_DIR . 'public/class-{{prefix}}-public.php';`, `        new {{Prefix}}_Public();`, blank line.
- then for `cpt`, `rest`, `cron` in that order, each when requested: `R(<f>)`, `        new {{Prefix}}_<CPT|REST|Cron>();`, blank line.

Activation and deactivation blocks:
- `{{ACT_DB}}` (db): `R(db)`, `        {{Prefix}}_DB::maybe_upgrade();`, blank line.
- `{{ACT_CRON}}` (cron): `R(cron)`, `        {{Prefix}}_Cron::schedule();`, blank line.
- `{{ACT_CPT}}` (cpt): `R(cpt)`, `        ( new {{Prefix}}_CPT() )->register();`, `        flush_rewrite_rules();`.
- `{{DEACT_CRON}}` (cron): `R(cron)`, `        {{Prefix}}_Cron::unschedule();`, blank line.

## Steps
1. Check the inputs. `frontend` without `foundation-dir`: stop with "STOPPED: --features includes 'frontend' but no foundation dir. This plugin does not bundle the Atomic Framework (a separately maintained product). Ask the user for their current swwp-tokens.css, swwp-components.css and swwp-foundation-logics.js (and alpine.min.js, alpine-loader.js, alpine-components.js for js-tier alpine), then rerun." Also stop when `foundation-dir` lacks any required file ("--foundation-dir is missing required file(s): ...; ask for a complete, current set"). Required: the three `swwp-*` files, plus the three `alpine-*` files for `alpine`.
2. Write the always-on files (substituted): `templates-core.md` sections `plugin-slug.php`, `uninstall.php`, `includes/class-prefix-activator.php`, `includes/class-prefix-deactivator.php`.
3. For each requested feature write its files: `cpt`, `db`, `rest`, `cron` (one class file each, `templates-features.md`); `admin` (class, `admin/css/admin.css`, `admin/js/admin.js`) and `frontend` (class, `public/css/<slug>.css`, `public/js/<slug>.js`), both in `templates-ui.md`. The target paths are in each section heading.
4. Documentation standard files (`fswpdevops/references/coding-standards.md`). Write each only if it does not exist yet, with LF endings. Skeleton only: `fswpdevops-plugin` fills every `FILL IN:` from the approved PRD before delivery, and the docs gate and QA check fail on a `FILL IN:` left in a non-planned feature file.
   - `README.md`: `# <name>`, blank line, `<description>`, blank line, `## Install`, blank line, "Copy the `<slug>` folder to `wp-content/plugins/` and activate it.", blank line, "More: [setup](docs/setup.md), [architecture](docs/architecture.md), [ops](docs/ops.md), [features](docs/features/README.md), [changelog](CHANGELOG.md)."
   - `CHANGELOG.md`: `# Changelog`, blank, "Format: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/); versions: [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html). Pre-1.0 is beta.", blank, `## [Unreleased]`, blank, `## [0.0.1] - <today as YYYY-MM-DD>`, blank, `### Added`, `- Initial scaffold (<sorted features joined by ", ", or core>).`
   - `docs/setup.md`: `# Setup`, blank, "1. Use a local WordPress site.", "2. Put `<slug>` in `wp-content/plugins/` and activate it.", "3. Quality gate: `run_gate` and `docs_gate` from the fswpdevops-qa skill (recipes in its `references/`)."
   - `docs/architecture.md`: `# Architecture`, blank, "- Main file `<slug>.php`; classes in `includes/`" plus ", `admin/`" when admin and ", `public/`" when frontend, then ".", "- Activation, deactivation and `uninstall.php` own all setup and cleanup.", "- FILL IN: hooks, data (options, tables, meta) and extension points as they appear."
   - `docs/ops.md`: `# Ops`, blank, "- Release: move `[Unreleased]` in CHANGELOG.md into the new version; header `Version`, version constant and readme `Stable tag` move together.", "- Uninstall removes only plugin-owned data.", "- Troubleshooting: FILL IN as issues are found."
   - `docs/features/<feature>.md` for each requested feature (sorted), titles: cpt "Custom post type" (PRD section 5, Data model), db "Custom database table" (PRD section 5), rest "REST API" (PRD section 6, API surface), cron "Scheduled jobs" (PRD section 5 / cron entries), admin "Admin experience" (PRD section 7), frontend "Front-end output" (PRD section 8). Body, with `<title>` and `<prd>` filled:

     ```
     # <title>

     **Status:** beta | **Since:** 0.0.1 | **Updated:** 0.0.1

     <!-- Stub: fill from <prd> before delivery, then remove this comment. -->

     ## Context
     FILL IN: why this feature exists and who uses it.

     ## Behaviour
     FILL IN: what the user sees and does; states; edge cases; errors; permissions and capabilities.

     ## How it works
     FILL IN: flow, hooks, classes and files, data (options, tables, meta), APIs and routes, config.

     ## UI
     FILL IN: text description of layout, controls and states (no screenshots needed). Write "None" for a feature with no UI.

     ## Limits & known issues
     None yet.

     ## History
     - 0.0.1: first version
     ```
   - `docs/features/README.md`: `# Features`, blank, "One file per feature. Keep this table current (status, since version).", blank, header `| Feature | Status | Since | File |`, separator `|---|---|---|---|`, then one row per feature (sorted): `| <title> | beta | 0.0.1 | [<feature>.md](<feature>.md) |`.
5. `frontend`: create `public/foundation/` and copy the three `swwp-*` files into it; for `alpine` also copy the three `alpine-*` files and tell the user: enqueue `alpine-loader.js` under the literal shared handle `fswp-alpine-loader` (never prefixed per plugin), using the dual-guard enqueue snippet in `frontend-output.md`, so Alpine is not initialised twice when another plugin uses it.
6. Write `includes/class-<prefix>-plugin.php` (`templates-core.md`, after the block tokens are computed).
7. Readme: `wporg` or `both` writes `readme.txt`; `private` or `both` writes `README-private.md` as `README.md`, replacing the step 4 README (the maintainer script does the same).
8. `admin` with `admin-tier=app`: tell the user the app tier's build tooling (Bun, React SPA, Tailwind, TanStack Query, Zustand, Radix primitives, @shadcn/lint) is not templated; follow `modern-app-stack.md` after confirming its decision checklist justifies it over `react`.
9. Create the empty folder `languages/`.
10. `zip` requested: zip the plugin folder as `<out>/<slug>.zip` with the folder name as the top entry.
11. Report: the plugin path and the list of generated files. Next: fill in domain logic per the references, uncomment nothing blindly (the generated loaders already match the requested features), then run the full gate with the fix option once, right after scaffolding (the templates rely on the WordPress-standard formatting that `phpcbf` applies to the generated plugin, never to the raw templates; see `fswpdevops-qa/references/run_gate.md`), then the `fswpdevops-qa` checklist before delivering.
