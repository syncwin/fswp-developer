# Security Standards (WPCS baseline)

Contents: 1. Direct access guard — every PHP file; 2. Capability checks — before any privileged action; 3. Nonces — every state-changing form, AJAX call, and REST write; 4. Sanitize on input, escape on output — every single time, no exceptions; 5. Database queries — always `$wpdb->prepare()`; 6. File operations & uploads; 7. Never do these, regardless of framing; 8. REST-specific: `permission_callback` is mandatory; 9. JSON blob storage (LONGTEXT JSON payloads); 10. Versioned data envelope.

Apply every one of these to every file, regardless of feature surface.
This is the single most heavily-weighted section of a real WordPress.org
Plugin Check review, and the most common source of real-world plugin
vulnerabilities.

## 1. Direct access guard — every PHP file

```php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
```
At the very top, before anything else, in every `.php` file that isn't
`uninstall.php` (which has its own `WP_UNINSTALL_PLUGIN` guard) or the
main bootstrap (which has this too, redundantly but harmlessly).

## 2. Capability checks — before any privileged action

Never rely on a nonce alone to gate a privileged action; a nonce
proves the request came from your form, not that the requester is
allowed to do the thing.

```php
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( esc_html__( 'You do not have permission to do this.', '{{plugin-slug}}' ) );
}
```
Pick the narrowest capability that fits (`manage_options` for
site-wide settings, `edit_posts`/`edit_others_posts` for content
actions, a custom capability if the plugin defines roles) — don't
default everything to `manage_options` out of laziness if a narrower
one is correct.

## 3. Nonces — every state-changing form, AJAX call, and REST write

```php
// Rendering the form:
wp_nonce_field( '{{prefix}}_save_settings', '{{prefix}}_nonce' );

// Handling the submission:
if ( ! isset( $_POST['{{prefix}}_nonce'] ) ||
     ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['{{prefix}}_nonce'] ) ), '{{prefix}}_save_settings' ) ) {
    wp_die( esc_html__( 'Security check failed.', '{{plugin-slug}}' ) );
}
```
For AJAX: `check_ajax_referer( '{{prefix}}_action', 'nonce' )`. For
REST: nonces aren't the mechanism (see `rest-cron.md`'s
`permission_callback` instead).

## 4. Sanitize on input, escape on output — every single time, no exceptions

**Input** (the moment you read `$_POST`/`$_GET`/`$_REQUEST`/a REST
param): always `wp_unslash()` first (WordPress magic-quotes-escapes
superglobals), then sanitize to the expected type.

| Expected type | Function |
|---|---|
| Plain text (single line) | `sanitize_text_field()` |
| Multi-line text / textarea | `sanitize_textarea_field()` |
| Email | `sanitize_email()` |
| URL | `esc_url_raw()` (for storage) |
| Integer | `absint()` or `intval()` |
| Key/slug from a fixed whitelist | `sanitize_key()` + `in_array()` check against the whitelist |
| HTML you intentionally allow (rich text) | `wp_kses_post()` |
| Arbitrary HTML with a custom allowed-tag list | `wp_kses( $value, $allowed_tags )` |

**Output** (the moment a value is echoed into markup): escape at the
point of output, not earlier — escaping-then-storing corrupts data.

| Context | Function |
|---|---|
| Inside a text node | `esc_html()` |
| Inside an HTML attribute | `esc_attr()` |
| Inside a `href`/`src` | `esc_url()` |
| A translatable string with output escaping | `esc_html__()` / `esc_html_e()` / `esc_attr__()` |
| JS value embedded in an inline `<script>` | `wp_json_encode()`, never string-concatenate |

## 5. Database queries — always `$wpdb->prepare()`

```php
global $wpdb;
$table = $wpdb->prefix . '{{prefix}}_events';
$row = $wpdb->get_row(
    $wpdb->prepare( "SELECT * FROM {$table} WHERE id = %d", $event_id )
);
```
Never string-concatenate user input into SQL, including for `LIKE`
clauses (use `$wpdb->esc_like()` first, then still wrap in
`prepare()`). Table/column names can't be parameterized by
`prepare()` — validate those against a hardcoded whitelist if they're
ever dynamic, never take them from user input directly.

## 6. File operations & uploads

- Never `include`/`require` a path built from user input.
- Use `wp_handle_upload()` for any file upload rather than hand-rolled
  `move_uploaded_file()`.
- Validate MIME type via `wp_check_filetype()`, not just the file
  extension the browser reports.

## 7. Never do these, regardless of framing

- `eval()`, `create_function()`, `extract()` on request data.
- Disabling `WP_DEBUG`/error output by suppressing errors instead of
  fixing them (`@` operator hiding a real bug).
- Loading remote scripts/styles from a third-party CDN inside `wp-admin`
  without the user's explicit ask — see `frontend-output.md` for
  the one sanctioned pattern (front-end Atomic Framework foundation assets, bundled
  locally, not CDN-loaded, for a real plugin).
- Storing API keys/secrets in the database in plaintext if they're
  high-sensitivity — prefer `wp-config.php` constants for anything like
  a payment-gateway secret key, with the DB option as a fallback only.

## 8. REST-specific: `permission_callback` is mandatory

Every `register_rest_route()` call MUST set a `permission_callback` —
omitting it (or setting `__return_true` on anything non-public) is the
single most common real-world WordPress REST vulnerability. See
`rest-cron.md`.

## 9. JSON blob storage (LONGTEXT JSON payloads)

For any REST route or table that stores a client-supplied JSON document:

- **Schema first:** declare `args` for the route (type, required, `maxLength` on every name field, `validate_callback`). Validate the shape, not just that it parses.
- **Size cap, filterable, enforced before decoding:** `$max = (int) apply_filters( '{{prefix_lower}}_max_payload_bytes', 262144 );` then `if ( strlen( $raw ) > $max ) return new WP_Error( '{{prefix_lower}}_payload_too_large', __( 'Payload too large.', '{{plugin-slug}}' ), array( 'status' => 413 ) );`.
- **Object-only:** `json_decode( $raw, true )` must return an associative array; reject scalars, `null`, and lists (a top-level array of values is not an object).
- **Length limits:** names and keys capped with `mb_strlen()`; match the column width (191 for an indexed utf8mb4 VARCHAR).
- **Write failures are real:** `$wpdb->insert()` / `update()` return `false` on failure. Check `false === $result`, log `$wpdb->last_error` (never echo it), return a `WP_Error` with status 500. Never report success on a failed write.
- Store with `wp_json_encode()`; never `unserialize()` user data; sanitize string leaves per the schema before storing.

## 10. Versioned data envelope

Saved user data is stored as `{ "schemaVersion": N, "data": { ... } }`.

- **Migration chain:** an ordered map of `N -> N+1` functions. On load, run the chain from the stored version to current, then validate the result against the current schema (Tier 3: `zod`).
- **Migrate on load, rewrite on next save.** Never write during a read. The old shape stays on disk until the user saves.
- **Unknown future version:** refuse to load and show a clear error; never downgrade or guess.
- PHP treats the blob as opaque but rejects any `schemaVersion` above the highest it knows.
