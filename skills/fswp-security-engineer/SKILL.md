---
name: fswp-security-engineer
description: Shared WordPress security baseline for Full-Stack WP Developer. The rules for validating and sanitizing input, escaping output by context, capability checks, nonces, prepared SQL, safe file handling, REST and AJAX authorization, and secrets, for plugins, themes, add-ons, and Core patches. Use whenever code reads request data, prints data, queries the database, handles uploads, or exposes an endpoint; loaded by the build, extend, and review skills.
metadata:
  version: '0.3.0'
  author: "@wasimness"
  company: SyncWin
  license: MIT
---

# FSWP Security Engineer

Security is not scaled down for small projects. Five habits cover most real vulnerabilities:

1. **Authorize** the action: `current_user_can()` with the narrowest capability that fits (an object capability such as `edit_post` when acting on a specific item).
2. **Verify intent** on state changes: a nonce (`wp_nonce_field` + `check_admin_referer`, `check_ajax_referer`, or the REST cookie nonce). A nonce proves the user meant it; it is not authorization.
3. **Validate and sanitize input** as early as possible, to the expected type, after `wp_unslash()`.
4. **Escape output late**, at the point of echo, for its context.
5. **Parameterize SQL**: `$wpdb->prepare()` for every query with a variable. Placeholders are `%d`, `%f`, `%s`, and `%i` for identifiers (table or column names), and are never quoted by hand. Prefer core query functions to raw SQL.

## Sanitize by data type (input)

| Data | Use |
|---|---|
| Plain text | `sanitize_text_field()`; multi-line `sanitize_textarea_field()` |
| Key, slug, class | `sanitize_key()`, `sanitize_title()`, `sanitize_html_class()` |
| Email, URL | `sanitize_email()` / `is_email()`, `esc_url_raw()` for storage |
| Integer, float | `absint()`, `(int)`, `(float)`; validate range |
| Choice from a list | Compare against an allow-list; never trust the value |
| Rich HTML | `wp_kses( $html, $allowed )` or `wp_kses_post()` for post-like content |
| File name | `sanitize_file_name()` |
| Arrays | Sanitize every element; drop unknown keys |

## Escape by context (output)

| Context | Use |
|---|---|
| Text in HTML | `esc_html()` (translatable: `esc_html__()`, `esc_html_e()`) |
| Attribute value | `esc_attr()` |
| URL in `href`/`src` | `esc_url()` |
| Inline JS data | `wp_json_encode()` with `wp_add_inline_script`, or `esc_js()` for legacy handlers |
| Textarea content | `esc_textarea()` |
| Allowed HTML | `wp_kses_post()` or `wp_kses()` |

Escape values you built yourself too. Never rely on "it was sanitized when saved".

## Checks to apply to every change

- Every privileged handler, REST route, and AJAX action has a capability check; `nopriv` handlers are treated as public internet input.
- REST routes have a real `permission_callback`. `__return_true` is only for genuinely public data and carries a comment saying why.
- No `eval`, `create_function`, `extract` on input, `unserialize` on user-influenced data (use JSON), shell functions on input, or dynamic `include` from input.
- Uploads: `wp_handle_upload` or `wp_check_filetype_and_ext`, size limits, never store in a web-executable path with a user-chosen extension.
- Outbound requests from input use `wp_safe_remote_*`; redirects from input use `wp_safe_redirect`.
- Secrets never live in source, and never appear in REST responses, logs, or error messages.
- Every PHP file that is not a class-only file starts with `defined( 'ABSPATH' ) || exit;`.

## Depth

`references/security.md` holds the house rules that go beyond this table (JSON blob routes with size caps, versioned data envelopes, storing sensitive settings, lifecycle safety). Official documentation: the security sections of the Plugin Handbook and the Common APIs handbook (`fswp-developer/references/official-docs.md`). To report a vulnerability in WordPress itself, use the private security process linked from the Core Contributor Handbook, never a public ticket.
