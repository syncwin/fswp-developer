# REST API Endpoints & Cron/Background Jobs

## REST API routes

```php
// includes/class-{{prefix}}-rest.php
class {{Prefix}}_REST {
    const NAMESPACE = '{{prefix_lower}}/v1';

    public function __construct() {
        add_action( 'rest_api_init', array( $this, 'register_routes' ) );
    }

    public function register_routes() {
        register_rest_route( self::NAMESPACE, '/{{noun}}', array(
            array(
                'methods'             => WP_REST_Server::READABLE, // GET
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
                'methods'             => WP_REST_Server::CREATABLE, // POST
                'callback'            => array( $this, 'create_item' ),
                'permission_callback' => array( $this, 'create_item_permission' ),
                'args'                => $this->create_item_args(),
            ),
        ) );
    }

    // READ: public data can use a permissive callback...
    public function get_items_permission( $request ) {
        return true; // fine ONLY if the data is genuinely meant to be public
    }

    // WRITE: never __return_true for anything that changes state.
    public function create_item_permission( $request ) {
        return current_user_can( 'edit_posts' );
    }

    public function create_item_args() {
        return array(
            'title' => array(
                'required'          => true,
                'type'              => 'string',
                'sanitize_callback' => 'sanitize_text_field',
            ),
        );
    }

    public function get_items( WP_REST_Request $request ) {
        $per_page = $request->get_param( 'per_page' );
        // ...query...
        return new WP_REST_Response( $data, 200 );
    }

    public function create_item( WP_REST_Request $request ) {
        $title = $request->get_param( 'title' ); // already sanitized via 'args'
        // ...insert...
        return new WP_REST_Response( array( 'id' => $new_id ), 201 );
    }
}
```

### REST rules (non-negotiable)

- **`permission_callback` is mandatory on every route.** Missing it
  triggers a core `_doing_it_wrong` notice and is a real security gap.
  `__return_true` is only correct for routes serving genuinely public
  read data — never for writes, never for anything returning
  user-specific or privileged data.
- Declare `args` with `sanitize_callback`/`validate_callback` per
  parameter rather than reading `$request->get_param()` and
  sanitizing ad hoc inline — this makes the REST route
  self-documenting (shows correctly in `/wp-json` discovery) and
  ensures sanitization can't be accidentally skipped on one code path.
- Authentication for a logged-in user hitting your own site's REST
  API is the WordPress nonce (`X-WP-Nonce` header, from
  `wp_create_nonce( 'wp_rest' )`, verified automatically by core) —
  don't invent a separate auth scheme for same-site requests.
- For third-party/external API consumers, use Application Passwords
  (built into core since 5.6) rather than rolling a custom API-key
  system, unless the user specifically wants a custom key scheme.

### Public routes and size-capped JSON bodies

- Any `__return_true` route needs a code comment on the same registration stating why it is public, and a one-line entry in the readme FAQ. `fswp-qa-engineer` fails a route without the comment.
- JSON body routes declare the schema and enforce the size cap (413) from `fswp-security-engineer` `references/security.md` section 9:

```php
register_rest_route( '{{plugin-slug}}/v1', '/documents', array(
    'methods'             => 'POST',
    'permission_callback' => function () { return current_user_can( 'edit_posts' ); },
    'callback'            => array( $this, 'save_document' ),
    'args'                => array(
        'name'    => array( 'type' => 'string', 'required' => true, 'maxLength' => 191,
                            'sanitize_callback' => 'sanitize_text_field' ),
        'payload' => array( 'required' => true,
                            'validate_callback' => array( $this, 'validate_payload' ) ),
    ),
) );
// validate_payload(): strlen() against the filterable cap -> WP_Error status 413;
// json_decode( ..., true ) must be an associative array; then check schemaVersion.
```

## Cron / scheduled & background jobs

```php
// includes/class-{{prefix}}-cron.php
class {{Prefix}}_Cron {
    const HOOK = '{{prefix_lower}}_{{job}}_cron';

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
        // Keep this fast and idempotent — WP-Cron fires on page load
        // traffic, not a true system cron, so a job that hangs delays
        // the visitor's page. For genuinely heavy work, this should
        // kick off a background task (e.g. Action Scheduler library)
        // rather than doing the work inline here.
    }
}
```

Call `{{Prefix}}_Cron::schedule()` from the **activator**, and
`{{Prefix}}_Cron::unschedule()` from the **deactivator** — an
unscheduled-on-deactivate job that never gets cleaned up is a common
zombie-cron bug that keeps firing on sites where the plugin was
deactivated but not deleted.

For a custom interval beyond WP's built-in `hourly`/`twicedaily`/
`daily`, register it via the `cron_schedules` filter before scheduling:

```php
function {{prefix_lower}}_add_cron_schedule( $schedules ) {
	$schedules['{{prefix_lower}}_every_15_min'] = array(
		'interval' => 15 * MINUTE_IN_SECONDS,
		'display'  => __( 'Every 15 Minutes', '{{plugin-slug}}' ),
	);
	return $schedules;
}
add_filter( 'cron_schedules', '{{prefix_lower}}_add_cron_schedule' );
```

For anything resembling a queue (bulk processing, retries, rate
limiting against an external API), prefer the **Action Scheduler**
library (used by WooCommerce, battle-tested at scale) over hand-rolled
WP-Cron chaining — mention this option to the user rather than
building a bespoke queue unless they specifically want to avoid the
dependency.
