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
