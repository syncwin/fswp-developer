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
