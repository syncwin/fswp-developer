# Internationalization & Distribution

Contents: i18n — wrap every user-facing string, always; Distribution target: WordPress.org public repo; Distribution target: private / client plugin; Versioning discipline (either target).

## i18n — wrap every user-facing string, always

```php
__( 'Save Settings', '{{plugin-slug}}' )               // returns translated string
_e( 'Save Settings', '{{plugin-slug}}' )                // echoes it
esc_html__( 'Save Settings', '{{plugin-slug}}' )        // translate + escape, for output
esc_html_e( 'Save Settings', '{{plugin-slug}}' )
esc_attr__( 'Save Settings', '{{plugin-slug}}' )        // for use inside an attribute
_x( 'Post', 'noun', '{{plugin-slug}}' )                 // disambiguated by context
_n( '%d item', '%d items', $count, '{{plugin-slug}}' )  // plural-aware
```

Rules:
- The text-domain string argument must be a **literal string
  matching the plugin slug**, never a variable/constant — WordPress.org's
  translation tooling parses this statically and a dynamic value
  breaks extraction.
- Never concatenate a translated string from pieces
  (`__('Save ') . $type`) — translators need the whole sentence in
  context; use `sprintf( __( 'Save %s', '{{plugin-slug}}' ), $type )`
  instead.
- Load the text domain via `load_plugin_textdomain()` in the main
  class's `run()` (see `architecture.md`) — as of WP 4.6+ this is
  technically only required for plugins hosted outside WordPress.org,
  but include it anyway for portability and pre-4.6 compatibility
  clarity.
- Generate a `.pot` file (`languages/{{plugin-slug}}.pot`) via
  WP-CLI's `wp i18n make-pot .` if the tool is available in the
  target environment; otherwise note in the README that translators
  should run this themselves.

### JavaScript strings (all tiers, including vanilla)

- Every user-facing string in JS or TSX goes through `__()` / `_n()` / `sprintf()` from `@wordpress/i18n` (Tier 3: the React bridge). No hardcoded literals.
- Register with `wp_set_script_translations( '{handle}', '{{plugin-slug}}', {{PREFIX}}_PLUGIN_DIR . 'languages' )` after `wp_register_script()` / `wp_enqueue_script()`, and declare `wp-i18n` as a script dependency.
- `.pot` generation must cover JS: `wp i18n make-pot . languages/{{plugin-slug}}.pot`, and `wp i18n make-json languages` for the JS translation files. Compiled bundles need source maps or the source in the package so strings are extractable.
- Lint rule: ban string literals in JSX text and user-facing attributes (for example `react/jsx-no-literals` for Tier 3; a grep gate for vanilla). `fswpdevops-qa` runs it.

## Distribution target: WordPress.org public repo

If targeting the public repo, these are hard requirements, not
suggestions:

- **`readme.txt`** in the exact WordPress.org format (not
  Markdown) — see `templates-readme.md` for the skeleton:
  `Contributors`, `Tags` (max 5, no brand names as tags), `Requires at
  least`, `Tested up to`, `Stable tag` (must match the plugin header
  `Version` after release), `License`/`License URI`, then `== Description ==`,
  `== Installation ==`, `== Frequently Asked Questions ==`,
  `== Screenshots ==`, `== Changelog ==`.
- **GPL-compatible license** (GPLv2 or later is the safe default) —
  every bundled third-party library must also be GPL-compatible;
  check before bundling anything with a restrictive license.
- **No calling home / telemetry without explicit, clearly-disclosed
  opt-in** — silent phone-home is a repo-rejection reason.
- **No loading remote code** (JS/CSS from a CDN) as a matter of
  policy — bundle everything locally, including the Atomic Framework foundation
  assets (see `frontend-output.md`, already bundled not CDN-loaded).
- Plugin header fields (`Plugin Name`, `Description`, etc.) have
  strict format rules — no marketing fluff, no "the best," no
  trademarked terms without permission.
- Run through the `fswpdevops-qa` checklist's Plugin-Check-equivalent
  section before calling it submission-ready; if the WP-CLI
  `plugin-check` tool (the same one the .org review team uses) is
  available in the environment, run it for real rather than
  approximating by hand.

## Distribution target: private / client plugin

More latitude, but still do these:

- A plain **`README.md`** is fine instead of `readme.txt` — write
  what it does, install steps (upload `.zip` via Plugins → Add New →
  Upload, or place the folder in `wp-content/plugins/`), any config
  the client needs to do post-activation (API keys, initial settings).
- License: still declare one explicitly (even if "proprietary — all
  rights reserved, licensed to {client} only") rather than leaving it
  implicit — avoids ambiguity if the plugin is ever handed to a third
  developer.
- CDN-loaded scripts are permissible here only on an explicit client
  request recorded in the PRD decisions log; still prefer bundling.
  Fonts stay local either way (`frontend-output.md`, Fonts and remote assets).
- Skip `.pot`/translation-readiness rigor unless the client's site is
  actually multilingual — still wrap strings in `__()` (cheap, keeps
  the option open), but don't burn time hand-generating `.pot` files
  for a single-language client site.

## Versioning discipline (either target)

- Bump `Version:` in the plugin header AND `Stable tag:` in
  `readme.txt` together — a mismatch is a common, confusing bug where
  WordPress.org shows a different "latest version" than what's
  actually in the header.
- Add an `@since {{version}}` docblock tag to new public methods/hooks
  so future maintainers (or the user themselves in six months) can
  tell when something was introduced.
- Keep a `== Changelog ==` entry per release, newest first, one line
  per notable change — same discipline as
  `wordpress-mini-app-builder`'s `CHANGELOG.md` habit, just per-plugin
  instead of per-foundation-update.
