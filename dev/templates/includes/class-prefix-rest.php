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
