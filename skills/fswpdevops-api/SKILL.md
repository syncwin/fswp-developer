---
name: fswpdevops-api
description: Domain skill for WordPress REST API and Abilities API work in Full-Stack WP DevOps. Covers registering routes with schemas, argument validation and sanitization, permission callbacks, controller classes, exposing post types and meta, authentication (cookie nonce, application passwords), pagination and errors, and registering abilities with input and output schemas and safety annotations. Use for any custom endpoint or machine-readable capability in a plugin or theme.
license: MIT
metadata:
  displayName: "FSWPDevOps API Developer"
  version: "0.5.0"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps API Developer

**Foundational (always applied):** `fswpdevops/references/lean-coding.md` (write less, reuse first), `fswpdevops/references/coding-standards.md` (coding standards, docs, i18n, accessibility), and `fswpdevops-security` (input, output, authorization).

Official reference: REST API Handbook (`fswpdevops/references/official-docs.md`). Security rules in `fswpdevops-security` apply to every route.

## Register a route

```php
function vp_register_routes() {
	register_rest_route( 'vendor-prefix/v1', '/items/(?P<id>\d+)', array(
		'methods'             => WP_REST_Server::READABLE,
		'callback'            => 'vp_get_item',
		'permission_callback' => function ( WP_REST_Request $r ) {
			return current_user_can( 'edit_post', (int) $r['id'] );
		},
		'args'                => array(
			'id' => array( 'type' => 'integer', 'required' => true, 'sanitize_callback' => 'absint' ),
		),
	) );
}
add_action( 'rest_api_init', 'vp_register_routes' );
```

## Rules

- **Namespace and version:** `vendor-prefix/v1`. Never register in core's `wp/v2` namespace.
- **`permission_callback` is mandatory.** Return a capability check, not just login status. Use `__return_true` only for genuinely public data, with a comment explaining why. Check object-level access (`edit_post`, ownership) whenever an ID is in the request.
- **Declare `args`** with `type`, `required`, `enum`, `minimum/maximum`, `validate_callback`, and `sanitize_callback`. The request is untrusted even after validation; use `$request->get_param()` values as typed.
- **Return data with `rest_ensure_response()`**; errors as `new WP_Error( 'vp_code', __( 'Message', 'text-domain' ), array( 'status' => 404 ) )`. Use accurate status codes (400 invalid, 401 unauthenticated, 403 forbidden, 404 missing, 409 conflict, 413 too large).
- **Schema:** implement `get_item_schema()` (or `schema` callback) so clients and the index can describe the resource; shape responses with `prepare_item_for_response()`.
- **Collections:** support `page`/`per_page` with a hard cap, set `X-WP-Total` and `X-WP-TotalPages`, and never return unbounded lists.
- **Never return** secrets, password hashes, raw options, or other users' private data.
- **Controllers:** for more than a couple of routes, extend `WP_REST_Controller` (`register_routes`, `get_items`, `get_item`, `create_item`, permission checks per method) and register the class once.
- **Expose core objects:** custom post types and taxonomies with `'show_in_rest' => true` (and `rest_base`); meta with `register_meta()`/`register_post_meta()` and `'show_in_rest' => true` plus a schema and an `auth_callback`.
- **Caching and performance:** cheap `GET` handlers; cache expensive results (`fswpdevops-performance`); avoid queries in loops.

## Authentication

| Client | Method |
|---|---|
| Same-site JS (admin, blocks, front end) | Cookie auth with the `X-WP-Nonce` header (`wp_create_nonce( 'wp_rest' )`, or `wp_localize_script` / `@wordpress/api-fetch` which adds it) |
| External server or app | Application Passwords over HTTPS, or a vetted OAuth plugin |
| Public read | No auth, only when the data is public |

Nonces do not replace capability checks. CORS: do not open `Access-Control-Allow-Origin: *` on authenticated routes.

## Client side

Use `@wordpress/api-fetch` in blocks and admin screens. Handle errors by `code` and `message`, not by parsing text.

## Abilities API

A Core API for registering discrete, machine-readable capabilities (name, input schema, output schema, permission check, execute callback) that tools and AI agents can discover and call. It is recent: confirm the minimum WordPress version and the exact function names in the developer documentation before using it (search "Abilities API"). Use it only when the PRD needs agent-callable functions; plain REST is right for ordinary client-server calls.

When registering an ability:

- Register the category first, then the ability, on the documented hooks.
- Give it JSON Schemas for input and output, and a `permission_callback` that checks a real capability.
- Set the safety annotations honestly: **read-only** abilities must not write, **destructive** ones must be flagged. A callback that writes while annotated read-only is a defect, and `fswpdevops-reviewer` treats it as one.
- Expose over REST only what should be callable remotely.

Audit and verification procedures: `references/abilities.md`.

To propose which existing endpoints should become abilities, list each route with its method, current permission check, side effects, and a suggested annotation; do not register anything until approved.
