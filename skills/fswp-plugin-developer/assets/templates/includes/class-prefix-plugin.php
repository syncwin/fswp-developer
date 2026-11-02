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
