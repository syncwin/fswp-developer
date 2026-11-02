<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_Admin' ) ) :

class {{Prefix}}_Admin {

    public function __construct() {
        add_action( 'admin_menu', array( $this, 'register_menu' ) );
        add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_assets' ) );
        add_action( 'admin_init', array( $this, 'register_settings' ) );
    }

    public function register_menu() {
        add_menu_page(
            __( '{{PLUGIN_NAME}}', '{{plugin-slug}}' ),
            __( '{{PLUGIN_NAME}}', '{{plugin-slug}}' ),
            'manage_options',
            '{{plugin-slug}}',
            array( $this, 'render_settings_page' ),
            'dashicons-admin-generic',
            26
        );
    }

    public function enqueue_assets( $hook ) {
        if ( strpos( $hook, '{{plugin-slug}}' ) === false ) {
            return;
        }
        wp_enqueue_style( '{{plugin-slug}}-admin', {{PREFIX}}_PLUGIN_URL . 'admin/css/admin.css', array(), {{PREFIX}}_VERSION );
        wp_enqueue_script( '{{plugin-slug}}-admin', {{PREFIX}}_PLUGIN_URL . 'admin/js/admin.js', array(), {{PREFIX}}_VERSION, true );
    }

    public function register_settings() {
        register_setting( '{{prefix}}_settings_group', '{{prefix}}_settings', array(
            'sanitize_callback' => array( $this, 'sanitize_settings' ),
        ) );

        add_settings_section( '{{prefix}}_main', __( 'General', '{{plugin-slug}}' ), '__return_false', '{{plugin-slug}}' );

        add_settings_field(
            '{{prefix}}_example_field',
            __( 'Example Field', '{{plugin-slug}}' ),
            array( $this, 'render_example_field' ),
            '{{plugin-slug}}',
            '{{prefix}}_main'
        );
    }

    public function sanitize_settings( $input ) {
        $output                   = array();
        $output['example_field'] = isset( $input['example_field'] )
            ? sanitize_text_field( wp_unslash( $input['example_field'] ) )
            : '';
        return $output;
    }

    public function render_example_field() {
        $settings = get_option( '{{prefix}}_settings', array() );
        $value    = isset( $settings['example_field'] ) ? $settings['example_field'] : '';
        printf(
            '<input type="text" name="%1$s[example_field]" value="%2$s" class="regular-text" />',
            esc_attr( '{{prefix}}_settings' ),
            esc_attr( $value )
        );
    }

    public function render_settings_page() {
        if ( ! current_user_can( 'manage_options' ) ) {
            return;
        }
        ?>
        <div class="wrap">
            <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
            <form method="post" action="options.php">
                <?php
                settings_fields( '{{prefix}}_settings_group' );
                do_settings_sections( '{{plugin-slug}}' );
                submit_button();
                ?>
            </form>
        </div>
        <?php
    }
}

endif;
