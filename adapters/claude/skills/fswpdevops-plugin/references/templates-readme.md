# Readme templates

One readme per distribution choice: `readme.txt` for WordPress.org (wporg or both) and `README-private.md` for private builds (private or both). Each section is the exact file content with the placeholders from `scaffold_plugin.md` still in it. The maintainer copies are in the repo's `dev/templates/`.

## Contents

- `readme.txt` -> `readme.txt`
- `README-private.md` -> `README.md`

## `readme.txt` -> `readme.txt`

When: distribution wporg or both.

```text
=== {{PLUGIN_NAME}} ===
Contributors: {{author-wporg-username}}
Tags: {{tag1}}, {{tag2}}, {{tag3}}
Requires at least: 6.4
Tested up to: {{latest-tested-wp-version}}
Requires PHP: 7.4
Stable tag: 0.0.1
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

{{ONE_LINE_DESCRIPTION}}

== Description ==

{{Longer description — what it does, who it's for, key features as a
bulleted list. No marketing superlatives ("the best," "amazing") —
WordPress.org review rejects promotional language in this section.}}

= Key Features =

* {{Feature 1}}
* {{Feature 2}}
* {{Feature 3}}

== Installation ==

1. Upload the plugin folder to `/wp-content/plugins/`, or install
   directly via Plugins → Add New → Upload Plugin.
2. Activate the plugin through the 'Plugins' menu in WordPress.
3. {{Any required post-activation configuration step, e.g. "Go to
   Settings → {{Plugin Name}} to configure."}}

== Frequently Asked Questions ==

= {{Question}} =

{{Answer}}

== Screenshots ==

1. {{Description of screenshot 1 — corresponds to assets/screenshot-1.png}}

== Changelog ==

= 0.0.1 =
* Initial release.
```

## `README-private.md` -> `README.md`

When: distribution private or both.

```markdown
# {{PLUGIN_NAME}}

{{ONE_LINE_DESCRIPTION}}

## Installation

1. Upload the `{{plugin-slug}}` folder to `wp-content/plugins/`, or
   install via Plugins → Add New → Upload Plugin using the provided
   `.zip`.
2. Activate **{{PLUGIN_NAME}}** in Plugins.
3. {{Any required post-activation configuration — API keys, initial
   settings, etc.}}

## What this plugin does

{{Feature summary in plain language for the client/team.}}

## Configuration

{{Settings screen location, any constants that need to be set in
wp-config.php, any external service setup required.}}

## License

Proprietary — built for {{client/project name}}. Not licensed for
redistribution outside this project unless otherwise agreed.

## Support / Maintenance notes

{{Anything a future developer touching this plugin should know —
non-obvious decisions, known limitations, where the Atomic Framework foundation
assets came from if bundled, cron schedule if any.}}
```
