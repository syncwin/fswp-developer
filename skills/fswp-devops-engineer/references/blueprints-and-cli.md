# Playground Blueprints and command-line operations

Confirm current step names and flags in the Playground and command-line handbooks before authoring; both evolve.

## Blueprint JSON

Top level: `$schema`, `landingPage`, `preferredVersions` (`php`, `wp`), `phpExtensionBundles`, `features` (for example networking), `login`, `steps`. Common steps: `login`, `installPlugin`, `installTheme`, `activatePlugin`, `activateTheme`, `setSiteOptions`, `defineWpConfigConsts`, `writeFile`, `mkdir`, `runPHP`, `runPHPWithOptions`, `wp-cli`, `importWxr`, `resetData`. Resources for steps are declared as objects with a `resource` type (for example `wordpress.org/plugins`, `url`, `literal`, `vfs`).

Authoring checklist: valid JSON; pinned PHP and WordPress versions when reproducibility matters; plugin or theme installed from the smallest source that works; a `landingPage` that shows the thing under test; no secrets; sample content added with `importWxr` or `runPHP` kept small. Validate against the schema before sharing.

Limits to state honestly: Playground is a sandbox in WebAssembly, not a full server. Do not use it as evidence for real cron timing, outgoing mail, large-file handling, or server-specific behavior.

## Command-line site operations

| Job | Commands (verify flags in the handbook) |
|---|---|
| Plugins and themes | `wp plugin list/install/activate/deactivate/update/delete`, same for `wp theme` |
| Options and content | `wp option get/update`, `wp post create/list/delete`, `wp user create/list` |
| Database | `wp db export`, `wp db import`, `wp db query`, `wp db check` |
| Safe replacements | `wp search-replace 'old' 'new' --dry-run`, then run without `--dry-run`; add `--all-tables` only when you mean it; serialized data is handled by the tool, never by raw SQL replace |
| Cron and cache | `wp cron event list/run`, `wp cache flush`, `wp transient delete --all`, `wp rewrite flush` |
| Multisite | `--url=<site>` to target a site; `wp site list`; `wp network` commands |
| Diagnostics | `wp core version`, `wp core verify-checksums`, `wp plugin verify-checksums`, `wp doctor check` if the package is installed, `wp profile stage` if installed |
| Scaffolding | `wp scaffold plugin`, `wp scaffold plugin-tests`, `wp scaffold block`, `wp scaffold child-theme` (check availability) |
| i18n | `wp i18n make-pot`, `wp i18n make-json`, `wp i18n make-mo` |
| Scripting | `wp eval-file script.php`, a `wp-cli.yml` for defaults, `--skip-plugins --skip-themes` when debugging load errors |

Safety rules: export the database before destructive commands; dry-run first; never run as root outside a disposable environment unless required; do not paste secrets into command history; production changes need the user's explicit go-ahead.

Reproducible test flow in wp-env: `npx @wordpress/env run cli wp plugin activate my-plugin`, exercise, `... run cli wp plugin deactivate`, `... run cli wp plugin uninstall my-plugin --deactivate`, then inspect options and tables to confirm uninstall left nothing behind.
