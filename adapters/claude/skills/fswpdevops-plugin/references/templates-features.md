# Feature class templates

The four optional feature classes (cpt, db, rest, cron); each is generated only when requested and loaded by the generated plugin class.

## Contents

- `includes/class-prefix-cpt.php` -> `includes/class-{prefix}-cpt.php`
- `includes/class-prefix-db.php` -> `includes/class-{prefix}-db.php`
- `includes/class-prefix-rest.php` -> `includes/class-{prefix}-rest.php`
- `includes/class-prefix-cron.php` -> `includes/class-{prefix}-cron.php`

## `includes/class-prefix-cpt.php` -> `includes/class-{prefix}-cpt.php`

When: feature cpt.

```php
<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_CPT' ) ) :

class {{Prefix}}_CPT {

    const POST_TYPE = '{{prefix}}_{{noun}}';

    public function __construct() {
        add_action( 'init', array( $this, 'register' ) );
    }

    public function register() {
        $labels = array(
            'name'               => _x( '{{Plural Name}}', 'post type general name', '{{plugin-slug}}' ),
            'singular_name'      => _x( '{{Singular Name}}', 'post type singular name', '{{plugin-slug}}' ),
            'add_new'            => __( 'Add New', '{{plugin-slug}}' ),
            'add_new_item'       => __( 'Add New {{Singular Name}}', '{{plugin-slug}}' ),
            'edit_item'          => __( 'Edit {{Singular Name}}', '{{plugin-slug}}' ),
            'new_item'           => __( 'New {{Singular Name}}', '{{plugin-slug}}' ),
            'view_item'          => __( 'View {{Singular Name}}', '{{plugin-slug}}' ),
            'search_items'       => __( 'Search {{Plural Name}}', '{{plugin-slug}}' ),
            'not_found'          => __( 'No {{plural_name}} found.', '{{plugin-slug}}' ),
            'not_found_in_trash' => __( 'No {{plural_name}} found in Trash.', '{{plugin-slug}}' ),
        );

        register_post_type( self::POST_TYPE, array(
            'labels'          => $labels,
            'public'          => true,
            'show_in_rest'    => true,
            'menu_icon'       => 'dashicons-admin-generic',
            'supports'        => array( 'title', 'editor', 'thumbnail', 'custom-fields' ),
            'has_archive'     => true,
            'rewrite'         => array( 'slug' => '{{prefix}}-{{noun}}' ),
            'capability_type' => 'post',
        ) );
    }
}

endif;
```

## `includes/class-prefix-db.php` -> `includes/class-{prefix}-db.php`

When: feature db.

```php
<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_DB' ) ) :

class {{Prefix}}_DB {

    const DB_VERSION = '0.0.1';

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
```

## `includes/class-prefix-rest.php` -> `includes/class-{prefix}-rest.php`

When: feature rest.

```php
<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_REST' ) ) :

class {{Prefix}}_REST {

    const NAMESPACE_KEY = '{{prefix}}/v1';

    public function __construct() {
        add_action( 'rest_api_init', array( $this, 'register_routes' ) );
    }

    public function register_routes() {
        register_rest_route( self::NAMESPACE_KEY, '/{{noun}}', array(
            array(
                'methods'             => WP_REST_Server::READABLE,
                'callback'            => array( $this, 'get_items' ),
                'permission_callback' => array( $this, 'get_items_permission' ),
                'args'                => array(
                    'per_page' => array(
                        'default'           => 10,
                        'sanitize_callback' => 'absint',
                    ),
                ),
            ),
            array(
                'methods'             => WP_REST_Server::CREATABLE,
                'callback'            => array( $this, 'create_item' ),
                'permission_callback' => array( $this, 'create_item_permission' ),
                'args'                => array(
                    'title' => array(
                        'required'          => true,
                        'type'              => 'string',
                        'sanitize_callback' => 'sanitize_text_field',
                    ),
                ),
            ),
        ) );
    }

    public function get_items_permission( $request ) {
        return true; // Fine only if this data is genuinely meant to be public.
    }

    public function create_item_permission( $request ) {
        return current_user_can( 'edit_posts' );
    }

    public function get_items( WP_REST_Request $request ) {
        $per_page = $request->get_param( 'per_page' );
        // ...query using $wpdb->prepare() or WP_Query...
        return new WP_REST_Response( array(), 200 );
    }

    public function create_item( WP_REST_Request $request ) {
        $title = $request->get_param( 'title' );
        // ...insert...
        return new WP_REST_Response( array( 'id' => 0 ), 201 );
    }
}

endif;
```

## `includes/class-prefix-cron.php` -> `includes/class-{prefix}-cron.php`

When: feature cron.

```php
<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_Cron' ) ) :

class {{Prefix}}_Cron {

    const HOOK = '{{prefix}}_{{job}}_cron';

    public function __construct() {
        add_action( self::HOOK, array( $this, 'run_job' ) );
    }

    public static function schedule() {
        if ( ! wp_next_scheduled( self::HOOK ) ) {
            wp_schedule_event( time(), 'daily', self::HOOK );
        }
    }

    public static function unschedule() {
        $timestamp = wp_next_scheduled( self::HOOK );
        if ( $timestamp ) {
            wp_unschedule_event( $timestamp, self::HOOK );
        }
    }

    public function run_job() {
        // Keep fast and idempotent. For heavy work, prefer Action
        // Scheduler over doing it inline here.
    }
}

endif;
```
