# Use WordPress instead of writing it

Common cases where custom code is usually unnecessary. Confirm the function in the Code Reference and the minimum version before use.

| You were about to write | Use instead |
|---|---|
| A settings page framework | Settings API (`register_setting`, `add_settings_section`, `add_settings_field`) |
| Your own HTTP client | `wp_remote_get/post`, `wp_safe_remote_*`, `wp_remote_retrieve_*` |
| A cache layer | `wp_cache_*` and transients (`set_transient`), keyed and expiring |
| A queue or scheduler | `wp_schedule_event`, `wp_schedule_single_event`; Action Scheduler if already installed |
| Input cleanup functions | `sanitize_*`, `absint`, `wp_kses*`, `esc_*` |
| A JSON API | REST API routes with schema; `wp_send_json_*` for simple AJAX |
| Post-like data storage | A custom post type with meta, before a custom table |
| A modal, tabs, or toggles in admin | `@wordpress/components` in a React screen; core admin CSS classes for classic screens |
| Image resizing | `add_image_size`, `wp_get_attachment_image` with `srcset` |
| A translation loader | `load_plugin_textdomain`, `wp_set_script_translations`, block.json `textdomain` |
| A block for layout only | Core Group, Columns, Grid, Stack blocks plus a pattern |
| Custom CSS for colors and type | `theme.json` settings and styles |
| A slider or accordion script | Core Details block, or the Interactivity API for the small behavior needed |
| Nonce or capability plumbing | `wp_nonce_field`, `check_admin_referer`, `current_user_can` |
| Date formatting | `wp_date`, `date_i18n` (respect site timezone) |
| Manual redirects | `wp_safe_redirect` then `exit` |
| Custom uninstall cleanup | `uninstall.php` guarded by `WP_UNINSTALL_PLUGIN`, using `delete_option` and `$wpdb` on your own names only |

## Questions that shrink a design

- What is the smallest number of stored fields that supports the required screens?
- Which of these hooks would core already run for me?
- If this feature were removed, what would still work? (That is the boundary of the change.)
- Can the user get this with a setting or a core block today?
