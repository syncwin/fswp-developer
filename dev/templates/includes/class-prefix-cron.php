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
