# Release check

Runs after the gate, checklist, and scenarios are green. Verify the artifact, do not repeat earlier checks.

1. Version matches across header, constant, readme Stable tag, and changelog (auto).
2. The zip has the plugin folder at its root; no `node_modules`, tests, `.git`, or dev files; compiled JS or CSS ships with `src/`, `package.json`, and the lockfile, and readme.txt has a "Source" section.
3. No remote assets, CDN fonts, or placeholder URIs (auto).
4. License headers present; GPL-compatible if targeting WordPress.org.
5. Text domain loads; POT covers PHP and JS strings.
6. `uninstall.php` removes the options, tables, cron events, and transients the plugin created; activation and deactivation are symmetric.
7. Install the final zip on a clean site: activate, deactivate, delete. If no WordPress is available, mark NOT RUN and hand the user this step.
8. Delivery summary lists the manual steps still owed (API keys, cron interval, initial settings) and every NOT RUN item.
