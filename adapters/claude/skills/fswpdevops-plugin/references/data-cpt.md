# Custom Post Types, Taxonomies & Custom Database Tables

Contents: Custom Post Type; Custom database table.

Pick the right storage for the data, don't default to custom tables
just because they feel "more real":

- **Use a Custom Post Type** when the data is content-like (has a
  title, editable body, author, revisions, and benefits from WP's
  existing admin list/edit screens, REST support, and search) —
  events, portfolio items, testimonials, products.
- **Use a custom DB table** when the data is structured/relational,
  high-volume, queried in ways posts/postmeta handle poorly (e.g. many
  joins, aggregate queries, log-style inserts), or has no natural
  "post" shape (a votes table, an analytics log, a queue).
- Many plugins need both: a CPT for the content, a custom table for
  something like per-CPT-item analytics or votes.

## Custom Post Type

```php
// includes/class-{{prefix}}-cpt.php
class {{Prefix}}_CPT {
    const POST_TYPE = '{{prefix_lower}}_{{noun}}'; // e.g. acme_event — max 20 chars

    public function __construct() {
        add_action( 'init', array( $this, 'register' ) );
    }

    public function register() {
        $labels = array(
            'name'          => _x( '{{Plural Name}}', 'post type general name', '{{plugin-slug}}' ),
            'singular_name' => _x( '{{Singular Name}}', 'post type singular name', '{{plugin-slug}}' ),
            'add_new_item'  => __( 'Add New {{Singular Name}}', '{{plugin-slug}}' ),
            'edit_item'     => __( 'Edit {{Singular Name}}', '{{plugin-slug}}' ),
            // ...fill the rest per the Handbook's full labels array.
        );

        register_post_type( self::POST_TYPE, array(
            'labels'        => $labels,
            'public'        => true,
            'show_in_rest'  => true,       // required for block editor + REST access
            'menu_icon'     => 'dashicons-calendar-alt',
            'supports'      => array( 'title', 'editor', 'thumbnail', 'custom-fields' ),
            'has_archive'   => true,
            'rewrite'       => array( 'slug' => '{{prefix_lower}}-{{noun}}' ),
            'capability_type' => 'post', // define custom capabilities only if roles genuinely differ from post editing
        ) );
    }
}
```

**Flush rewrite rules exactly once, on activation** (`flush_rewrite_rules()`
in the activator, never on every `init` — that's a well-known
performance bug) so the new archive/single URLs resolve.

### Taxonomy (if the CPT needs categorization)

```php
register_taxonomy( '{{prefix_lower}}_{{noun}}_category', self::POST_TYPE, array(
    'labels'       => array( 'name' => __( '{{Noun}} Categories', '{{plugin-slug}}' ) ),
    'hierarchical' => true,
    'show_in_rest' => true,
) );
```

### Meta boxes / custom fields

Prefer `show_in_rest` + REST-exposed post meta (registered via
`register_post_meta()` with `show_in_rest => true`) so the block
editor and REST clients see the field natively, over a classic
meta-box UI, unless the user specifically wants the classic-editor
meta-box pattern.

```php
register_post_meta( self::POST_TYPE, '{{prefix_lower}}_start_date', array(
    'type'              => 'string',
    'single'            => true,
    'show_in_rest'      => true,
    'sanitize_callback' => 'sanitize_text_field',
    'auth_callback'     => function() { return current_user_can( 'edit_posts' ); },
) );
```

## Custom database table

Only via `dbDelta()`, never a raw `CREATE TABLE` query — `dbDelta()`
handles both creation and future schema migrations safely, but is
picky about exact SQL formatting (two spaces before `KEY`, no
trailing commas after the last column, `PRIMARY KEY` on its own
convention line — deviating silently breaks the diffing).

```php
// includes/class-{{prefix}}-db.php
class {{Prefix}}_DB {
    const DB_VERSION = '0.0.1';

    public static function maybe_upgrade() {
        if ( get_option( '{{prefix_lower}}_db_version' ) !== self::DB_VERSION ) {
            self::create_tables();
            update_option( '{{prefix_lower}}_db_version', self::DB_VERSION );
        }
    }

    private static function create_tables() {
        global $wpdb;
        $table_name      = $wpdb->prefix . '{{prefix_lower}}_{{noun}}';
        $charset_collate = $wpdb->get_charset_collate();

        $sql = "CREATE TABLE {$table_name} (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            post_id BIGINT UNSIGNED NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            value VARCHAR(191) NOT NULL,
            PRIMARY KEY  (id),
            KEY post_id (post_id)
        ) {$charset_collate};";

        require_once ABSPATH . 'wp-admin/includes/upgrade.php';
        dbDelta( $sql );
    }
}
```

Call `{{Prefix}}_DB::maybe_upgrade()` from the activator (creation on
first install) **and** from an `admin_init`/`plugins_loaded` hook
(so an existing install picks up schema changes on plugin update,
not only fresh activation — a very commonly missed case).

### Schema versioning discipline

- Bump `DB_VERSION` any time the schema changes, and make
  `create_tables()`'s SQL always describe the *current, full* desired
  schema — `dbDelta()` diffs against it, it isn't a migration script
  you hand-write incrementally.
- If a column needs data transformation (not just addition), write an
  explicit one-time migration function gated on the old version
  number, run once, and only then bump `DB_VERSION`.
- Always use `$wpdb->prefix`, never hardcode `wp_` — multisite and
  custom table-prefix installs will silently write to the wrong table
  otherwise.
