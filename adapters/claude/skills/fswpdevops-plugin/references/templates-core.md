# Core plugin templates

Always generated. Each section is one template: the text between the fences is the exact file content, with the placeholders described in `scaffold_plugin.md` still in it. Write it to the target path (relative to the plugin folder) after substituting the placeholders. The maintainer copies of these files are in the repo's `dev/templates/`.

## Contents

- `plugin-slug.php` -> `{slug}.php`
- `uninstall.php` -> `uninstall.php`
- `includes/class-prefix-plugin.php` -> `includes/class-{prefix}-plugin.php`
- `includes/class-prefix-activator.php` -> `includes/class-{prefix}-activator.php`
- `includes/class-prefix-deactivator.php` -> `includes/class-{prefix}-deactivator.php`

## `plugin-slug.php` -> `{slug}.php`

When: always.

```php
<?php
/**
 * Plugin Name:       {{PLUGIN_NAME}}
{{PLUGIN_URI_LINE}}
 * Description:       {{ONE_LINE_DESCRIPTION}}
 * Version:           0.0.1
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            {{AUTHOR}}
{{AUTHOR_URI_LINE}}
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       {{plugin-slug}}
 * Domain Path:       /languages
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Block direct access.
}

define( '{{PREFIX}}_VERSION', '0.0.1' );
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

## `uninstall.php` -> `uninstall.php`

When: always.

```php
<?php
/**
 * Fires only when the plugin is deleted via wp-admin (not on deactivate).
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;

// Options this plugin owns.
delete_option( '{{prefix}}_settings' );
delete_option( '{{prefix}}_db_version' );

// Custom table(s), if any — remove this block if the plugin has no custom table.
$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}{{prefix}}_{{noun}}" );

// CPT content: only delete if the plugin's own settings had an explicit
// "delete all data on uninstall" opt-in that the user enabled. Never
// silently destroy user-authored content by default. Example gated pattern:
//
// $settings = get_option( '{{prefix}}_settings' );
// if ( ! empty( $settings['delete_data_on_uninstall'] ) ) {
//     $posts = get_posts( array( 'post_type' => '{{prefix}}_{{noun}}', 'numberposts' => -1, 'post_status' => 'any' ) );
//     foreach ( $posts as $post ) {
//         wp_delete_post( $post->ID, true );
//     }
// }
```

## `includes/class-prefix-plugin.php` -> `includes/class-{prefix}-plugin.php`

When: always (written last, after the feature blocks are computed).

```php
<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_Plugin' ) ) :

final class {{Prefix}}_Plugin {

    public function run() {
        load_plugin_textdomain( '{{plugin-slug}}', false, dirname( plugin_basename( {{PREFIX}}_PLUGIN_FILE ) ) . '/languages' );

{{FEATURE_LOADERS}}
    }
}

endif;
```

## `includes/class-prefix-activator.php` -> `includes/class-{prefix}-activator.php`

When: always.

```php
<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_Activator' ) ) :

class {{Prefix}}_Activator {

    public static function activate() {
{{ACT_DB}}

        if ( false === get_option( '{{prefix}}_settings' ) ) {
            add_option( '{{prefix}}_settings', array() );
        }

{{ACT_CRON}}

{{ACT_CPT}}
    }
}

endif;
```

## `includes/class-prefix-deactivator.php` -> `includes/class-{prefix}-deactivator.php`

When: always.

```php
<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_Deactivator' ) ) :

class {{Prefix}}_Deactivator {

    public static function deactivate() {
{{DEACT_CRON}}

        flush_rewrite_rules();

        // Never delete options/tables/content here — that belongs in
        // uninstall.php only, since deactivation is often temporary.
    }
}

endif;
```
