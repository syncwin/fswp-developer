# Headers and readme (verified 2026-09-28)

## Plugin header (main PHP file)

| Field | Notes |
|---|---|
| Plugin Name | Required |
| Plugin URI | Unique to this plugin; cannot be a WordPress.org URL; different for free and pro versions |
| Description | Under 140 characters |
| Version | Compared with PHP `version_compare()` (1.02 is greater than 1.1) |
| Requires at least | Lowest WordPress version. Since WordPress 5.8 requirements are read from this header, not the readme |
| Requires PHP | Minimum PHP |
| Author, Author URI | Multiple authors comma-separated |
| License, License URI | For example GPL v2 or later |
| Text Domain, Domain Path | Text domain matches the slug; Domain Path locates translations |
| Network | `true` only if the plugin can only be network-activated; omit otherwise |
| Update URI | For plugins updated outside WordPress.org, so a same-named directory plugin cannot overwrite it |
| Requires Plugins | Comma-separated WordPress.org slugs of dependencies (slugs only, not paths) |

## Plugin readme.txt

Header: `=== Plugin Name ===`, `Contributors` (WordPress.org usernames, case sensitive), `Donate link` (optional), `Tags` (1 to 5, no competitor names), `Tested up to` (major version, digits only), `Stable tag` (the released plugin version; not `trunk`, which is prohibited for new plugins), `License`, `License URI` (optional), then a short description of at most 150 characters, no markup. Sections: Description, Installation (omit if nothing custom), FAQ, Screenshots, Changelog, Upgrade Notice, plus a Source section when shipping compiled assets. Keep the file under about 10 KB (move older changelog to `changelog.txt`).

How it is parsed: the directory reads trunk's readme Stable tag, then uses the readme in `tags/<that version>/`; the displayed version number comes from the main plugin file header. The tag's readme must also carry the right Stable tag.

## Theme headers (`style.css`)

Required for the directory: Theme Name, Author, Description, Version, Requires at least, Tested up to, Requires PHP, License, License URI, Text Domain. Optional: Theme URI, Author URI, Tags, Domain Path. Child theme: `Template` (the parent's folder name) is required. The directory reads Version from this file to detect updates. Themes need only support the three latest WordPress versions.

## Do not claim what you did not test

"Tested up to" is a claim. Only write it after testing on that version; otherwise leave it out of a draft and tell the user it is owed.
