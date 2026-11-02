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
