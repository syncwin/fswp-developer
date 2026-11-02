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
 * Text Domain:       {{plugin-slug}}
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
