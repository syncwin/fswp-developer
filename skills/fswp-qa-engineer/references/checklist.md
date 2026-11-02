# Manual checklist

Items marked (auto) are enforced by `qa_check.py`; confirm the script passed, do not re-inspect by hand. Everything else needs judgment.

## Structure
- [ ] Plugin header complete: Plugin Name, Version, Requires at least, Requires PHP, License, Text Domain. URI lines present only if real (auto for placeholders).
- [ ] No unused feature classes scaffolded or `require`d.
- [ ] ABSPATH guard on every PHP file (auto).

## Lifecycle
- [ ] Activation is idempotent: options added only when absent (`false === get_option()`); no duplicate cron or rewrite side effects.
- [ ] Deactivation unschedules cron and flushes rewrite rules; deletes no data.
- [ ] `uninstall.php` guarded by `WP_UNINSTALL_PLUGIN` (auto); removes only plugin-owned data, and destructive cleanup only where the user opted in.
- [ ] DB upgrade check runs on `plugins_loaded` or `admin_init`, not only on activation (auto).

## Security
- [ ] Every privileged action has a narrow `current_user_can()`.
- [ ] Every state change verifies a nonce before acting.
- [ ] Every REST route has a real `permission_callback` (auto); each `__return_true` route has a comment and a readme FAQ line (comment auto, FAQ manual).
- [ ] Input is `wp_unslash()`ed then sanitized to type; output escaped at the point of echo (WPCS covers most).
- [ ] Every query with variables uses `$wpdb->prepare()` (WPCS covers most).
- [ ] No `eval`, `extract`, `create_function` (auto). No hardcoded secrets.
- [ ] JSON blob routes: schema, filterable size cap returning 413, object-only, length limits, `$wpdb->insert` false handled (`fswp-security-engineer` `references/security.md` section 9).
- [ ] Saved user data carries `schemaVersion` with a migrate-on-load chain (section 10).

## i18n
- [ ] Every PHP and JS user-facing string wrapped with the correct text domain; no concatenated sentences.
- [ ] `load_plugin_textdomain()` (auto); `wp_set_script_translations()` for own JS (auto); `.pot` covers JS.
- [ ] No hardcoded strings in JS or TSX (lint or grep gate).

## Front end
- [ ] No h1-h3 in shortcode, block, or widget markup (auto).
- [ ] Assets enqueued inside the render callback, idempotent, never via `has_shortcode()` (auto).
- [ ] No remote requests, CDN scripts, or hosted fonts; fonts bundled locally with license (auto). Bundled foundation files are unmodified.
- [ ] Type, spacing, radius in `rem` on a 16px root; no root font-size override (auto). Fluid type checked for WCAG 1.4.4 (200% zoom) by hand.

## Admin
- [ ] Admin assets load only on this plugin's screens (hook-suffix check).
- [ ] Settings use the Settings API or an equivalent nonce, capability, sanitize pattern.
- [ ] Native wp-admin markup; no Atomic Framework classes in admin.
- [ ] Tier 3 only: two-surface overlay test passes; CI runs lint, axe, tests, `bun audit`; source ships in the zip (auto).

## Standards (fswp-plugin-developer references/standards.md)
- [ ] Changelog: this iteration's changes landed in the **latest existing entry**, not a new one, unless the change genuinely justifies a version bump (new feature = MINOR, fix = PATCH, breaking = MAJOR). No duplicate lines describing the same change.
- [ ] If the version was bumped: header `Version`, the version constant, and `readme.txt` Stable tag all moved together (auto, `qa_check.py`), and a new changelog entry was opened for it.
- [ ] Technology stack unchanged from the prior iteration unless a stated reason justified the change (industry standard conflict, technical constraint, requirement change) — check the PRD's section 1b against what was actually built.
- [ ] No invented project metadata: every header/readme/about-screen field traces to something the user stated; anything unstated is absent, not a placeholder.
- [ ] `docs/` has an entry for every feature the PRD lists, each covering what applies from: what it does, how it works, inputs, outputs, dependencies, constraints. Updated for any feature this iteration touched, not just new ones. (auto: presence and stub completion (no `FILL IN:` left) are both checked by `qa_check.py`; only the actual quality of the filled content needs a human read.)

## Distribution
- [ ] WordPress.org target: `readme.txt` valid, Stable tag matches (auto), GPL-compatible, no remote code, no undisclosed phone-home; `fswp-release-manager` consulted.
- [ ] Private target: README with real install steps and post-activation configuration.
- [ ] Changelog entry for this version; zip has the plugin folder at its root.

## Themes (block and classic)
- [ ] Every template and template part the PRD lists exists and renders correctly with real content, empty content, and long titles.
- [ ] `theme.json` validates; settings (palette, typography, spacing, layout) are used instead of hard-coded CSS where possible; styles do not fight the editor.
- [ ] Custom patterns are registered with categories and translated titles; no pattern depends on remote images.
- [ ] Classic themes: every output is escaped at the point of echo; template tags used instead of raw queries; `wp_body_open()`, `wp_head()`, `wp_footer()` present.
- [ ] Keyboard navigation, visible focus, skip link, heading order, color contrast, and reduced-motion respected.
- [ ] No plugin-territory features (custom post types, shortcodes with business logic) inside the theme; they would vanish on theme switch.
- [ ] Child theme: enqueues parent styles correctly and overrides only what it must.

## Updates and add-ons
- [ ] Parity list from the change brief is complete and every item is marked.
- [ ] Existing prefixes, hooks, option names, and public function signatures are unchanged unless the brief says otherwise; removed public items go through deprecation first.
- [ ] Add-on: host missing, inactive, and out-of-range cases handled without fatals; `Requires Plugins` header used where the host is on WordPress.org.
- [ ] New files follow the project's conventions, not house templates, unless the project has none.

## Core patches
- [ ] A Trac ticket exists and is referenced; patch is against trunk unless a maintenance branch is specified.
- [ ] Tests added or updated; the relevant PHPUnit group passes; coding standards clean on changed lines; inline docs follow Core's documentation standard.
