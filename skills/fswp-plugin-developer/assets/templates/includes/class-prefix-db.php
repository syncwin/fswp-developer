<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_DB' ) ) :

class {{Prefix}}_DB {

    const DB_VERSION = '0.1.0';

    public static function maybe_upgrade() {
        if ( get_option( '{{prefix}}_db_version' ) !== self::DB_VERSION ) {
            self::create_tables();
            update_option( '{{prefix}}_db_version', self::DB_VERSION );
        }
    }

    private static function create_tables() {
        global $wpdb;
        $table_name      = $wpdb->prefix . '{{prefix}}_{{noun}}';
        $charset_collate = $wpdb->get_charset_collate();

        $sql = "CREATE TABLE {$table_name} (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            post_id BIGINT UNSIGNED NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            value VARCHAR(191) NOT NULL,
            PRIMARY KEY  (id),
            KEY post_id (post_id)
        ) {$charset_collate};";

        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta( $sql );
    }
}

endif;
