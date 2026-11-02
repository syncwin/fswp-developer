<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_Public' ) ) :

class {{Prefix}}_Public {

    const SHORTCODE = '{{prefix}}_{{code}}';

    public function __construct() {
        add_shortcode( self::SHORTCODE, array( $this, 'render' ) );
    }

    public function render( $atts ) {
        $atts = shortcode_atts( array(), $atts, self::SHORTCODE );

        $this->enqueue_assets();

        ob_start();
        ?>
        <div class="afw-scope {{prefix}}-{{code}}">
            <!-- app markup using afw-* component classes -->
        </div>
        <?php
        return ob_get_clean();
    }

    private function enqueue_assets() {
        // Remove the afw-* enqueues below if this plugin doesn't use
        // the Atomic Framework for its front-end output (e.g. a
        // client project with its own brand) — see references/frontend-output.md.
        wp_enqueue_style( '{{prefix}}-foundation', {{PREFIX}}_PLUGIN_URL . 'public/foundation/afw-tokens.css', array(), {{PREFIX}}_VERSION );
        wp_enqueue_style( '{{prefix}}-components', {{PREFIX}}_PLUGIN_URL . 'public/foundation/afw-components.css', array( '{{prefix}}-foundation' ), {{PREFIX}}_VERSION );
        wp_enqueue_style( '{{plugin-slug}}', {{PREFIX}}_PLUGIN_URL . 'public/css/{{plugin-slug}}.css', array( '{{prefix}}-components' ), {{PREFIX}}_VERSION );

        wp_enqueue_script( '{{prefix}}-foundation-logic', {{PREFIX}}_PLUGIN_URL . 'public/foundation/afw-foundation-logics.js', array(), {{PREFIX}}_VERSION, true );
        wp_enqueue_script( '{{plugin-slug}}', {{PREFIX}}_PLUGIN_URL . 'public/js/{{plugin-slug}}.js', array( '{{prefix}}-foundation-logic' ), {{PREFIX}}_VERSION, true );
    }
}

endif;
