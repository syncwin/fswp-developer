# Quality lens

Look for defects that pass a linter and fail in production. Score by likelihood and consequence.

## 1. Failure handling

- **Ignored results.** `$wpdb->insert/update/query` returning false or `0`, `wp_insert_post`/`wp_update_user`/`update_option` results, `wp_remote_*` returning `WP_Error`, `file_put_contents` returning false: is each checked, and is the failure visible to the user or log?
- **Swallowed errors.** Empty `catch`, `catch (Throwable $e) {}` with a default return, `@` suppression, an error logged with no user-facing outcome. A catch block should name what it expects and act on it.
- **Quiet fallbacks.** A default value substituted after an error with no signal, a "try A, then B, then C" chain that hides why A failed, retries that end without reporting exhaustion.
- **Wrong success.** A handler that returns 200/`wp_send_json_success` when the work failed; a settings save that shows "saved" after a failed write.
- **Error messages** that expose internals to visitors, or say nothing helpful to admins.

## 2. Data and lifecycle

- Activation not idempotent; upgrade logic only on activation (updates do not re-run it); schema changes without a version option and migration on load.
- Uninstall removing too much (user content) or too little (options, tables, cron events, transients).
- Stored options with no default handling, autoloaded large values, unbounded growth (logs, transients without expiry, meta per request).
- Multisite and network activation assumptions; `switch_to_blog` without restore.

## 3. Performance

- Unbounded queries (`posts_per_page => -1`, no LIMIT), queries inside loops (N+1), `meta_query` on unindexed meta at scale, `get_option` for big arrays on every request.
- Assets enqueued on every page instead of where used; blocking scripts; large images without sizes; missing cache for repeated remote calls.
- Work done on hot hooks (`init`, `wp_head`, `the_content`) that could be deferred, cached, or scheduled.

## 4. Architecture and scope

- Code the brief did not ask for; dead code; features half-wired.
- Global functions and options without a unique prefix; collisions with core or other plugins.
- Business logic in template files, presentation logic in data classes, or hooks that do too many jobs.
- Public APIs (hooks, function signatures, option names, REST shapes) changed without a deprecation path.

## 5. Internationalization and accessibility

- User-facing strings not translatable, wrong or missing text domain, concatenated sentences, variables inside `__()`, missing translator comments for placeholders.
- Missing labels, focus handling, keyboard paths, or contrast in admin screens and front-end output; icon-only controls without accessible names; motion without a reduced-motion path.

## 6. PHP correctness patterns

- Loose comparison surprises (`==`, `in_array` without strict, `0 == "a"` on old PHP), `empty()` on `"0"`, `isset` vs `null`.
- `foreach` by reference left dangling; array functions that reindex keys unexpectedly; modifying an array while iterating.
- Return-type and exception contracts that differ between similar functions; nullable values dereferenced.
- Resource lifecycles: files, transactions, or locks opened and not released on error paths.
- Time and locale: `date()` vs `wp_date()`, hard-coded timezones, string sorting with locale.
- Version drift: functions unavailable at the declared minimum WordPress/PHP.

## 7. Tests

Behavior with real branching (parsing, permissions, migrations) shipped with no test or scenario. Report only when the risk is concrete.

## 8. Comments and documentation accuracy

- A comment or DocBlock that no longer matches the code (renamed parameters, changed return, removed behavior) is a defect: it misleads the next editor.
- Missing `@since`, `@param`, `@return` on new public functions and hooks (per `fswpdevops/references/coding-standards.md`).
- Comments that restate the code without adding a reason; TODOs with no owner or trigger; commented-out code left behind.
- User-facing docs (readme, `docs/`) that claim behavior the code does not have.

## 9. Test coverage gaps

- Branching logic, permission rules, migrations, parsers, and money or data-changing paths with no test or scenario.
- Tests that assert nothing meaningful, mirror the implementation, or would still pass if the feature were broken.
- Missing negative cases: bad input, missing permission, empty data, large data, host plugin absent.
- Report a gap only when the untested path carries real risk; name the scenario that should exist.

## 10. Class and type design

- Objects that can be constructed in an invalid state; public properties that any caller can mutate; methods that must be called in a fixed order.
- One class doing several jobs (data, rendering, and hooks together) so nothing can be reused or tested alone.
- Loose types: arrays of mixed shapes passed around where a small value object or documented array shape would prevent misuse; return values that are sometimes an array, sometimes false, sometimes `WP_Error`, with no documented contract.
- Static and global state that hides dependencies; singletons used where a function would do.
- Type declarations beyond what the declared minimum PHP version supports.
