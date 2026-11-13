# Admin and front-end templates

Admin and front-end class, CSS and JS files, generated only when the features admin or frontend are requested. They follow the same conventions as the core templates (`templates-core.md`).

## Contents

- `admin/class-prefix-admin.php` -> `admin/class-{prefix}-admin.php`
- `admin/css/admin.css` -> `admin/css/admin.css`
- `admin/js/admin.js` -> `admin/js/admin.js`
- `public/class-prefix-public.php` -> `public/class-{prefix}-public.php`
- `public/css/plugin-slug.css` -> `public/css/{slug}.css`
- `public/js/plugin-slug.js` -> `public/js/{slug}.js`

## `admin/class-prefix-admin.php` -> `admin/class-{prefix}-admin.php`

When: feature admin.

```php
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
```

## `admin/css/admin.css` -> `admin/css/admin.css`

When: feature admin.

```css
/* Admin styles for {{plugin-slug}} — compose with native wp-admin classes, don't fight core styling. */
```

## `admin/js/admin.js` -> `admin/js/admin.js`

When: feature admin.

```js
// Admin JS for {{plugin-slug}}.
```

## `public/class-prefix-public.php` -> `public/class-{prefix}-public.php`

When: feature frontend.

```php
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
```

## `public/css/plugin-slug.css` -> `public/css/{slug}.css`

When: feature frontend.

```css
/* Plugin's own front-end composition CSS for {{plugin-slug}} — layered on top of swwp-components.css atoms, not redefining them. */
```

## `public/js/plugin-slug.js` -> `public/js/{slug}.js`

When: feature frontend.

```js
// Front-end JS for {{plugin-slug}} — use window.AFW.Utils where available instead of reimplementing.
```
