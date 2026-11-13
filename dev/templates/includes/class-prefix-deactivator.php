<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

if ( ! class_exists( '{{Prefix}}_Deactivator' ) ) :

class {{Prefix}}_Deactivator {

    public static function deactivate() {
{{DEACT_CRON}}

        flush_rewrite_rules();

        // Never delete options/tables/content here — that belongs in
        // uninstall.php only, since deactivation is often temporary.
    }
}

endif;
