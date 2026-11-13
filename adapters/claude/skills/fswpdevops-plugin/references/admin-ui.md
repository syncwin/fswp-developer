# Admin UI — WP-Native Styling

Contents: Menu registration; Settings API (for a settings page — don't hand-roll form handling); List/manage screens: `WP_List_Table`; Icons & visual language; When the admin UI needs to be genuinely React-driven: `@wordpress/components` + `wp.element`.

Confirmed default: admin screens use **WordPress's own admin
conventions**, not the Atomic Framework. Reasons this is the right
default, not just a stylistic preference: wp-admin gets its own core
CSS updates the plugin shouldn't fight, screen-reader/accessibility
behavior is already wired into core admin classes, and users expect a
plugin's settings page to look like it belongs in wp-admin, not like a
separate branded product.

## Menu registration

```php
// admin/class-{{prefix}}-admin.php
class {{Prefix}}_Admin {
    public function __construct() {
        add_action( 'admin_menu', array( $this, 'register_menu' ) );
        add_action( 'admin_enqueue_scripts', array( $this, 'enqueue_assets' ) );
    }

    public function register_menu() {
        add_menu_page(
            __( '{{Plugin Name}}', '{{plugin-slug}}' ),
            __( '{{Plugin Name}}', '{{plugin-slug}}' ),
            'manage_options',
            '{{plugin-slug}}',
            array( $this, 'render_dashboard' ),
            'dashicons-admin-generic',
            26
        );

        add_submenu_page(
            '{{plugin-slug}}',
            __( 'Settings', '{{plugin-slug}}' ),
            __( 'Settings', '{{plugin-slug}}' ),
            'manage_options',
            '{{plugin-slug}}-settings',
            array( $this, 'render_settings' )
        );
    }

    public function enqueue_assets( $hook ) {
        // Only load on this plugin's own screens — never site-wide in admin.
        if ( strpos( $hook, '{{plugin-slug}}' ) === false ) {
            return;
        }
        wp_enqueue_style( '{{plugin-slug}}-admin', {{PREFIX}}_PLUGIN_URL . 'admin/css/admin.css', array(), {{PREFIX}}_VERSION );
        wp_enqueue_script( '{{plugin-slug}}-admin', {{PREFIX}}_PLUGIN_URL . 'admin/js/admin.js', array( 'jquery' ), {{PREFIX}}_VERSION, true );
    }
}
```

## Settings API (for a settings page — don't hand-roll form handling)

The Settings API gives you nonces, sanitize callbacks, and the native
`form-table` styling for free — prefer it over a manual `$_POST`
handler unless the admin UI is genuinely more complex than a
settings form (see `WP_List_Table` below for that case).

```php
public function register_settings() {
    register_setting( '{{prefix_lower}}_settings_group', '{{prefix_lower}}_settings', array(
        'sanitize_callback' => array( $this, 'sanitize_settings' ),
    ) );

    add_settings_section( '{{prefix_lower}}_main', __( 'General', '{{plugin-slug}}' ), '__return_false', '{{plugin-slug}}-settings' );

    add_settings_field(
        '{{prefix_lower}}_example_field',
        __( 'Example Field', '{{plugin-slug}}' ),
        array( $this, 'render_example_field' ),
        '{{plugin-slug}}-settings',
        '{{prefix_lower}}_main'
    );
}

public function sanitize_settings( $input ) {
    $output = array();
    $output['example_field'] = isset( $input['example_field'] )
        ? sanitize_text_field( wp_unslash( $input['example_field'] ) )
        : '';
    return $output;
}
```

Render form with `settings_fields()` + `do_settings_sections()` inside
a standard `<div class="wrap">` + `<h1>` + `<form method="post"
action="options.php">` shell — this is the one context where a plain
`<h1>` is correct (native wp-admin page title), unlike front-end output.

## List/manage screens: `WP_List_Table`

For anything showing rows of plugin-managed data (custom table rows,
a CPT-adjacent list, log entries) with sorting/pagination/bulk
actions, extend core's `WP_List_Table` rather than hand-building an
HTML table — it gives you sortable columns, bulk-action UI, and
pagination markup consistent with every other list screen in wp-admin
for free.

```php
if ( ! class_exists( 'WP_List_Table' ) ) {
    require_once ABSPATH . 'wp-admin/includes/class-wp-list-table.php';
}

class {{Prefix}}_List_Table extends WP_List_Table {
    public function get_columns() {
        return array(
            'cb'         => '<input type="checkbox" />',
            'name'       => __( 'Name', '{{plugin-slug}}' ),
            'created_at' => __( 'Created', '{{plugin-slug}}' ),
        );
    }

    public function prepare_items() {
        global $wpdb;
        $table = $wpdb->prefix . '{{prefix_lower}}_{{noun}}';
        $per_page = 20;
        $current_page = $this->get_pagenum();

        $total_items = (int) $wpdb->get_var( "SELECT COUNT(*) FROM {$table}" );
        $this->items = $wpdb->get_results(
            $wpdb->prepare( "SELECT * FROM {$table} ORDER BY created_at DESC LIMIT %d OFFSET %d", $per_page, ( $current_page - 1 ) * $per_page ),
            ARRAY_A
        );

        $this->set_pagination_args( array( 'total_items' => $total_items, 'per_page' => $per_page ) );
        $this->_column_headers = array( $this->get_columns(), array(), array() );
    }
}
```

## Icons & visual language

- Icons: Dashicons (`dashicons-*` classes) — already loaded in every
  wp-admin screen, no enqueue needed.
- Buttons: native `.button` / `.button-primary` classes.
- Notices: `<div class="notice notice-success is-dismissible">` (core
  handles the dismiss behavior automatically once `is-dismissible` is
  present and the notice is inside `.wrap`).
## When the admin UI needs to be genuinely React-driven: `@wordpress/components` + `wp.element`

A handful of settings fields never needs this — use the Settings API
above. But once an admin screen has real client-side state (a live
data table with filtering/sorting, a multi-step setup wizard, a
dashboard that polls a REST endpoint and re-renders), reach for
**`@wordpress/components` + `wp.element`**, not a bundled copy of
React and not the Atomic Framework/Alpine front-end tiers — admin screens stay on
this WP-native path exclusively.

**Why this specific choice for admin, over Alpine or a bundled React:**
`wp.element` is a thin wrapper around React that ships inside
WordPress core itself (the block editor is built on it) — enqueuing
your admin script with `wp-element` as a dependency reuses the
*same* React instance every other admin screen and the block editor
are already running, at zero extra bundle cost to your plugin.
Bundling your own React here would risk two React copies fighting
over the DOM if the admin page also has block-editor UI present (e.g.
a metabox context); Alpine is the wrong tool for the same reason it's
optional on the front-end (no build step needed here — WordPress
already ships one) plus `@wordpress/components` gives you data tables,
tab panels, notices, and form controls that are pixel-matched to core
admin styling for free, which a hand-rolled Alpine table wouldn't be.

```php
public function enqueue_react_admin_assets( $hook ) {
    if ( strpos( $hook, '{{plugin-slug}}' ) === false ) {
        return;
    }
    $asset_file = include {{PREFIX}}_PLUGIN_DIR . 'admin/build/index.asset.php';
    wp_enqueue_script(
        '{{plugin-slug}}-admin-app',
        {{PREFIX}}_PLUGIN_URL . 'admin/build/index.js',
        $asset_file['dependencies'], // includes wp-element, wp-components, wp-i18n, wp-api-fetch
        $asset_file['version'],
        true
    );
    wp_enqueue_style( 'wp-components' ); // core's own component stylesheet
    wp_localize_script( '{{plugin-slug}}-admin-app', '{{prefix}}Admin', array(
        'restUrl'   => esc_url_raw( rest_url( '{{prefix}}/v1' ) ),
        'restNonce' => wp_create_nonce( 'wp_rest' ),
    ) );
}
```

```jsx
// admin/src/index.js — built via @wordpress/scripts (wp-scripts start / build)
import { createRoot } from '@wordpress/element';
import { Panel, PanelBody, Button, Notice } from '@wordpress/components';
import { __ } from '@wordpress/i18n';
import apiFetch from '@wordpress/api-fetch';

function App() {
    // useState/useEffect from '@wordpress/element' — same hooks API as React
    return (
        <Panel header={ __( '{{Plugin Name}}', '{{plugin-slug}}' ) }>
            <PanelBody title={ __( 'Settings', '{{plugin-slug}}' ) }>
                <Button variant="primary">{ __( 'Save', '{{plugin-slug}}' ) }</Button>
            </PanelBody>
        </Panel>
    );
}

createRoot( document.getElementById( '{{prefix}}-admin-root' ) ).render( <App /> );
```

**Build tooling, only for this admin bundle:** `@wordpress/scripts`
(`wp-scripts`) handles the JSX/webpack build and is the only place a
build step is acceptable in this skill's otherwise build-free output —
because it's building an admin-only bundle, committed as compiled
`admin/build/` output, not something the end user ever runs. Install
`@wordpress/scripts` and every other `@wordpress/*` package
(`@wordpress/element`, `@wordpress/components`, `@wordpress/i18n`,
`@wordpress/api-fetch`) at `latest` from the npm registry — never pin
an old version in `package.json`, the same policy `references/modern-app-stack.md`'s dependency section spells out for Tier 3. `npx
@wordpress/create-block` conventions apply for `package.json` scripts
(`build`, `start`). Use `apiFetch` from `@wordpress/api-fetch` against
this plugin's own REST routes (`references/rest-cron.md`)
rather than raw `fetch()` — it automatically attaches the REST nonce.

**Still default to the plain Settings API** for anything that's just
a handful of fields — this React path is for admin screens with real
interactivity, not the default admin experience.


