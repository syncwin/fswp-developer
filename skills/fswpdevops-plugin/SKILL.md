---
name: fswpdevops-plugin
description: Plugin build stage of Full-Stack WP DevOps. House standards and code templates for real WordPress plugins (not shortcode snippets) - folder anatomy, activation/uninstall lifecycle, custom post types and tables, admin UI tiers, front-end output on the Atomic Framework, REST and cron, i18n, distribution, and the Tier 3 React admin stack - plus a scaffold script. Also the base structure for add-ons. Invoked by fswpdevops after an approved PRD; consult directly for a specific plugin build pattern.
license: MIT
metadata:
  displayName: "FSWPDevOps Plugin Developer"
  version: "0.5.0"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps Plugin Developer

**Foundational (always applied):** `fswpdevops/references/lean-coding.md` (write less, reuse first), `fswpdevops/references/coding-standards.md` (coding standards, docs, i18n, accessibility), and `fswpdevops-security` (input, output, authorization).

Executes an **approved PRD** (`fswpdevops-architect`). Prefix, distribution target, feature surface, and JS tier are already decided; do not re-ask. For each step, load the domain skill for the general procedure and this skill's reference for house depth, templates, and stricter rules. Precedence: `fswpdevops/references/precedence.md`.

For changes to an existing plugin, use `fswpdevops-maintainer` instead; it calls back here for structure patterns only.

## Layers

```
1  BOOTSTRAP   plugin-slug.php, uninstall.php, includes/class-plugin.php (no business logic)
2  LIFECYCLE   Activator / Deactivator (activation hook, dbDelta, upgrade check)
3  DOMAIN      CPTs, tables, REST routes, cron: only what the PRD lists
4a ADMIN UI    native wp-admin by default; @wordpress/components for one React screen;
               React SPA + Tailwind + TanStack Query + Zustand only for app-like admin
4b PUBLIC UI   Atomic Framework (user-supplied), vanilla JS by default, Alpine opt-in
```

Admin never uses Atomic Framework or Alpine classes. Never scaffold unused feature classes.

## Workflow

| Step | Do | House reference | Domain skill |
|---|---|---|---|
| 1 Scaffold | Derive slug, prefix, class names, text domain; run `scripts/scaffold_plugin.py --help` first. Pass `--plugin-uri` and `--author-uri` only if real (the line is dropped otherwise, never a placeholder domain). **Run `fswpdevops-qa/scripts/run_gate.sh <dir> <min-php> --fix` once right after scaffolding**: templates carry `{{...}}` placeholders that the formatter cannot safely reflow before substitution. | `architecture.md` | none |
| 2 Bootstrap + lifecycle | Bootstrap declares the header, autoload, and hands off to the main class | `architecture.md` | none |
| 3 Security | Full baseline on every file, every plugin size | `fswpdevops-security` | `fswpdevops-security` |
| 4 Domain | CPTs, tables (`dbDelta`, schema versions), REST, cron | `data-cpt.md`, `rest-cron.md` | `fswpdevops-api`; `fswpdevops-performance` when the PRD needs it |
| 5 Blocks (if in PRD) | Custom blocks, patterns, Interactivity | none | `fswpdevops-block` |
| 6 Admin UI | Settings API, `WP_List_Table`, Dashicons; escalate only per checklist | `admin-ui.md`, `modern-app-stack.md` | none |
| 7 Public output | Ask the user for the current Atomic Framework files first; conditional enqueue inside the callback | `frontend-output.md` | none |
| 8 i18n + distribution | Every PHP and JS string; readme; license; versioning | `i18n-distribution.md` | `fswpdevops-release` for WordPress.org |

Stop at the end of step 8 and hand to `fswpdevops-qa`.

## Add-on structure

When `fswpdevops-maintainer` runs in add-on mode it reuses steps 1-3 and 8 here. The extra add-on rules (host detection, `Requires Plugins`, load order, graceful absence) live in `fswpdevops-maintainer`.

## Standards (every build, every iteration)

`references/standards.md` governs versioning/changelog discipline, the technology-stack decision, required project metadata (never invent a missing value), per-feature documentation in `docs/`, code-quality bar, and the minimal-code discipline (decide-before-you-write order, root-cause fixes, `shortcut:` markers). Read it before the first build and before any iteration on an existing plugin — it is not a one-time setup step.

## Security posture

Never scaled down for small plugins: capability checks on every privileged action, nonces on every state change, sanitize input and escape output, `$wpdb->prepare()` on every query, a real `permission_callback` on every REST route, safe lifecycle, no plaintext secrets. Full rules: `fswpdevops-security`.

## Alpine tier

Never inferred. Selected only by the 5-point checklist in `references/frontend-output.md`, and only after the user explicitly confirms having seen which check triggered it and what the vanilla alternative looks like.

## Atomic Framework (user-supplied, not bundled)

It is a separately maintained product; a bundled copy would drift. Whenever the build includes `frontend`, ask for the current `afw-tokens.css`, `afw-components.css`, `afw-foundation-logics.js` (plus `alpine.min.js`, `alpine-loader.js`, `alpine-components.js` only if the Alpine tier was confirmed). The scaffold copies them via `--foundation-dir` and stops with a reminder if it is missing.

## Dependencies

Everything except the Atomic Framework (Tier 2 `@wordpress/*`, Tier 3 stack) is resolved at `latest` from its official registry **at scaffold time**, then pinned: commit the lockfile and record resolved versions in the README. Latest-at-scaffold plus a committed lockfile satisfies WordPress.org's reproducible-source rule. Exception: a user-stated compatibility ceiling. Details: `references/modern-app-stack.md`.

## Deliver

Installable `{plugin-slug}.zip` (plugin folder at the zip root) plus `readme.txt` and/or private `README.md` with real install steps, and a short summary: prefix and feature decisions, manual steps still owed (API keys, cron interval, initial settings). Compiled output ships with its source (`references/modern-app-stack.md`).

## Bundled

- `scripts/scaffold_plugin.py`: `--features cpt,db,rest,cron,admin,frontend` (any subset), `--js-tier vanilla|alpine`, `--admin-tier native|react|app`, `--distribution wporg|private|both`, `--plugin-uri`, `--author-uri`, `--foundation-dir`, `--zip`.
- `assets/templates/`: plugin skeleton with `{{PREFIX}}`, `{{Prefix}}`, `{{prefix}}`, `{{PLUGIN_NAME}}`, `{{plugin-slug}}` placeholders.
