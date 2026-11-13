# Brand naming: ask per project, then apply consistently

There is no fixed default acronym. Every project (plugin, theme, add-on, or Core patch) has its own owner and its own brand, so the code-level prefix is decided per project, not inherited from this tool. `sw` was one example of a personal brand acronym, not a built-in default — do not use it unless a user states it for that specific project.

## When to ask

`fswpdevops-plan` asks for the brand acronym in the same question round as the rest of the planning questions (never a separate round), for **new plugin** and **new theme** work only:

> "What short acronym or prefix should this project's code use (for function names, constants, etc.)? If you don't have one, I'll suggest a couple of options based on the project name."

- If the user gives one, use it for the rest of the project, applying the exceptions below.
- If they have none, propose 2-3 short candidates derived from the project's own name (not from SyncWin, not from this tool), and let them pick or provide their own.
- **Update and Add-on work never asks this.** The existing project's established prefix is kept for continuity; changing it is a breaking change and is only done if the user explicitly requests a rename.
- **Core patches** do not use a project prefix; WordPress Core naming rules apply instead (`fswpdevops-core`).

Once chosen for a project, record it in that project's plan/PRD and apply it everywhere below without asking again for that project.

## Where the acronym applies

Use `{{acronym}}` below as a stand-in for whatever the user chose, applied wherever it can be used without affecting functionality, compatibility, WordPress conventions, third-party tools, APIs, framework rules, or a naming requirement imposed by a dependency.

| Element | Pattern | Notes |
|---|---|---|
| PHP function/hook prefix | `{{acronym}}_` (lowercase) | e.g. `acme_register_routes()`, hook `acme_after_save` |
| Constants | `{{ACRONYM}}_` (uppercase) | e.g. `ACME_VERSION` |
| Class prefix (no namespace) | `{{Acronym}}_` | e.g. `Acme_Plugin` |
| Namespace | `{{Acronym}}\ProjectName` | The acronym alone is often a thin namespace; add the project name for uniqueness |
| CSS custom properties / class prefix | `--{{acronym}}-` / `.{{acronym}}-` | |
| JS global/namespace | `{{acronym}}` | e.g. `window.acme = {}` for legacy scripts; ES module names don't need it |
| REST namespace | `{{acronym}}/v1` | Still versioned per the REST API rules |
| Transient/option keys | `{{acronym}}_` | |
| Cron hooks | `{{acronym}}_` | |

## Where it conflicts and the official rule wins instead

- **Theme global prefix minimum.** The Theme Directory requires at least four letters for the theme's public-namespace prefix. A shorter acronym (like a 2-letter one) becomes the acronym plus enough of the project name to reach four letters (for example `sw` + `demo` → `swdemo`), not the bare acronym.
- **Plugin/theme slug and Text Domain.** These name the *product*, not the brand, so they follow the project's own name (`event-manager`, text domain `event-manager`), not the acronym. The acronym still prefixes the code inside it.
- **Reserved namespaces.** `wp` and `WordPress` are reserved for WordPress itself; never shadow them, regardless of the chosen acronym.
- **Dependency-mandated names.** A library's required hook, filter, config key, or file name (for example a page builder's expected element ID format) is used as that tool documents it, never renamed to fit the acronym.
- **WordPress.org username and Contributors field.** These are the actual WordPress.org account, not a brand acronym; leave them as the user states them.
- **Existing project prefix (Update and Add-on work).** The project's own established prefix is kept for continuity; never replaced with a new acronym mid-project without an explicit request.

## Shared, tool-owned constants

A small number of identifiers are shared across every project this tool scaffolds (for example the Alpine.js loader handle in `fswpdevops-plugin`), so more than one plugin on the same site can coordinate without conflicting. Those use a fixed name tied to this tool (`fswp-`), not the per-project acronym, because they are not part of any one project's brand.
