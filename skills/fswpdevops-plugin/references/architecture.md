# Architecture — Folder Anatomy, Naming, Lifecycle

Contents: Plugin folder anatomy; Naming/prefix derivation table; Bootstrap file (`{plugin-slug}.php`); Lifecycle: activate / deactivate / uninstall — know the difference; Main plugin class — composition root, not a god object.

## Plugin folder anatomy

```
{plugin-slug}/
├── {plugin-slug}.php          ← main bootstrap file (plugin header lives here)
├── uninstall.php              ← runs ONLY on delete, never on deactivate
├── readme.txt                 ← WordPress.org format (or README.md for private)
├── LICENSE                    ← GPLv2+ text if targeting WordPress.org
├── includes/
│   ├── class-{prefix}-plugin.php        ← main singleton, wires everything together
│   ├── class-{prefix}-activator.php     ← register_activation_hook target
│   ├── class-{prefix}-deactivator.php   ← register_deactivation_hook target
│   ├── class-{prefix}-cpt.php           ← custom post types/taxonomies (if used)
│   ├── class-{prefix}-db.php            ← custom table schema + dbDelta (if used)
│   ├── class-{prefix}-rest.php          ← REST routes (if used)
│   └── class-{prefix}-cron.php          ← scheduled events (if used)
├── admin/
│   ├── class-{prefix}-admin.php         ← menu registration, Settings API
│   ├── css/admin.css
│   ├── js/admin.js
│   └── views/                           ← partial templates for admin screens
├── public/
│   ├── class-{prefix}-public.php        ← shortcode/block/widget registration + enqueue
│   ├── css/{plugin-slug}.css            ← the plugin's OWN small CSS (composition only)
│   ├── js/{plugin-slug}.js              ← the plugin's OWN small JS
│   └── foundation/                      ← Atomic Framework files, supplied by the user at build time (if used) — see references/frontend-output.md
├── languages/                           ← .pot/.po/.mo files
└── assets/                              ← WordPress.org listing assets (banner, icon, screenshots) — NOT loaded by the plugin itself
```

Only generate the pieces a given plugin actually needs — a simple
settings-only plugin doesn't need `class-{prefix}-cpt.php` or
`public/` at all. Don't scaffold dead files.

## Naming/prefix derivation table

Everything derives mechanically from the confirmed prefix (e.g. `Acme`
or a client's `ACME`) and plugin name:

| Element | Pattern | Example (prefix `Acme`, "Event Manager") |
|---|---|---|
| Plugin slug (folder + main file) | lowercase-kebab of prefix + name | `acme-event-manager` |
| Main class | `{Prefix}_Plugin` | `{Prefix}_Plugin (example: Acme_Plugin)` |
| Feature classes | `{Prefix}_{Feature}` | `{Prefix}_CPT`, `{Prefix}_DB`, `{Prefix}_REST`, `{Prefix}_Cron`, `{Prefix}_Admin`, `{Prefix}_Public` (example with prefix `Acme`: `Acme_CPT`, `Acme_DB`, ...) |
| Functions (if any procedural helpers) | `{prefix_lower}_{verb}` | `acme_get_event()` |
| Text domain | same as plugin slug | `acme-event-manager` |
| Option key(s) | `{prefix_lower}_{purpose}` | `acme_settings`, `acme_db_version` |
| DB table (no `wp_` hardcode — use `$wpdb->prefix`) | `{$wpdb->prefix}{prefix_lower}_{noun}` | `wp_acme_events` |
| Custom post type slug | `{prefix_lower}_{noun}` (max 20 chars, WP hard limit) | `acme_event` |
| Hook names (custom actions/filters) | `{prefix_lower}_{event}` | `acme_event_created` |
| Nonce actions | `{prefix_lower}_{action}_nonce` | `acme_save_settings_nonce` |
| REST namespace | `{prefix_lower}/v1` | `acme/v1` |
| Cron hook | `{prefix_lower}_{job}_cron` | `acme_cleanup_cron` |

Never reuse a bare, generic prefix (`Plugin`, `Admin`, `Settings`,
`Utils`) for any global symbol — PHP has no namespacing enforcement in
WordPress's loading model, and colliding with another active plugin's
function/class name is a fatal white-screen bug, not a warning.

### The prefix is for code identifiers only — never for user-visible text

The table above governs PHP/JS/DB identifiers (classes, functions,
option keys, hook names, slugs, text domains) where collision-safety
matters. It does **not** apply to anything a site owner or visitor
actually reads:

- The plugin header's `Plugin Name:` field — the clean product name
  only (e.g. "Event Manager", not "Acme Event Manager").
- The wp-admin menu label / page `<h1>` and any submenu labels.
- Front-end shortcode/block output — headings, button labels, any
  visible copy.
- `readme.txt`'s `=== Name ===` line and its `Contributors`/display copy.

If the confirmed prefix is also the client or company's own brand name
and they've explicitly asked for it to appear in the product name
(e.g. an internal tool deliberately called "ACME Toolkit"), that's a
product-naming decision made in the PRD step, not a mechanical
consequence of the code prefix — don't default to prepending the
prefix to the visible name just because it exists.

## Bootstrap file (`{plugin-slug}.php`)

This file's ONLY job is: declare the plugin header, define constants,
require the autoloader, and boot the main class. No business logic
here — keeps the one file WordPress reads for every plugin on every
page load as light as possible.

```php
<?php
/**
 * Plugin Name:       {{PLUGIN_NAME}}
{{PLUGIN_URI_LINE}}
 * Description:       {{ONE_LINE_DESCRIPTION}}
 * Version:           0.1.0
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            {{AUTHOR}}
{{AUTHOR_URI_LINE}}
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:        {{plugin-slug}}
 * Domain Path:       /languages
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Block direct access.
}

define( '{{PREFIX}}_VERSION', '0.1.0' );
define( '{{PREFIX}}_PLUGIN_FILE', __FILE__ );
define( '{{PREFIX}}_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
define( '{{PREFIX}}_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

require_once {{PREFIX}}_PLUGIN_DIR . 'includes/class-{{prefix}}-activator.php';
require_once {{PREFIX}}_PLUGIN_DIR . 'includes/class-{{prefix}}-deactivator.php';
require_once {{PREFIX}}_PLUGIN_DIR . 'includes/class-{{prefix}}-plugin.php';

register_activation_hook( __FILE__, array( '{{Prefix}}_Activator', 'activate' ) );
register_deactivation_hook( __FILE__, array( '{{Prefix}}_Deactivator', 'deactivate' ) );

function {{prefix}}_run() {
    $plugin = new {{Prefix}}_Plugin();
    $plugin->run();
}
{{prefix}}_run();
```

Manual `require_once` per class (as above) is the default — it's
transparent, has zero build step, and matches most WordPress.org
plugins. Offer Composer PSR-4 autoloading (`composer.json` +
`vendor/autoload.php`) only if the user explicitly wants a
Composer-based workflow or the plugin has enough classes (10+) that
manual requires get unwieldy; document the choice either way in the
delivered README.

## Lifecycle: activate / deactivate / uninstall — know the difference

This is the most commonly botched part of real plugins (mini-apps
have no equivalent, since a shortcode snippet has no lifecycle):

| Hook | Fires when | Typical job |
|---|---|---|
| `register_activation_hook()` | Plugin is activated | Create/upgrade DB tables (`dbDelta()`), set default options, schedule cron, flush rewrite rules if CPTs were just registered |
| `register_deactivation_hook()` | Plugin is deactivated | Unschedule cron jobs, flush rewrite rules — **never** delete data here, deactivation is often temporary (e.g. during a debugging session) |
| `uninstall.php` | Plugin is deleted via wp-admin | Delete options, drop custom tables, delete CPT posts/meta if the user opted into full cleanup — this is the ONLY place destructive cleanup belongs |

```php
// includes/class-{{prefix}}-activator.php
class {{Prefix}}_Activator {
    public static function activate() {
        self::maybe_create_tables();
        if ( false === get_option( '{{prefix}}_settings' ) ) {
            add_option( '{{prefix}}_settings', array( /* defaults */ ) );
        }
        flush_rewrite_rules(); // only if a CPT was registered this request
    }

    private static function maybe_create_tables() {
        // see references/data-cpt.md for dbDelta() pattern + version guard
    }
}
```

```php
// uninstall.php — sibling to the main plugin file, WordPress calls this directly
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;
delete_option( '{{prefix}}_settings' );
delete_option( '{{prefix}}_db_version' );
$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}{{prefix}}_{{table}}" );
// Only delete CPT posts/postmeta if the plugin's own settings had an
// explicit "delete all data on uninstall" opt-in the user enabled —
// never silently destroy user content by default.
```

## Main plugin class — composition root, not a god object

```php
// includes/class-{{prefix}}-plugin.php
class {{Prefix}}_Plugin {
    public function run() {
        load_plugin_textdomain( '{{plugin-slug}}', false, dirname( plugin_basename( {{PREFIX}}_PLUGIN_FILE ) ) . '/languages' );

        if ( is_admin() ) {
            require_once {{PREFIX}}_PLUGIN_DIR . 'admin/class-{{prefix}}-admin.php';
            new {{Prefix}}_Admin();
        }

        require_once {{PREFIX}}_PLUGIN_DIR . 'public/class-{{prefix}}-public.php';
        new {{Prefix}}_Public();

        // Only require+instantiate the feature classes this plugin actually uses:
        // require_once {{PREFIX}}_PLUGIN_DIR . 'includes/class-{{prefix}}-cpt.php';
        // new {{Prefix}}_CPT();
    }
}
```

Each feature class hooks itself in its own constructor (`add_action`/
`add_filter`) rather than the main class reaching into every feature's
internals — keeps features independently removable.
