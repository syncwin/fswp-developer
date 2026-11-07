# Domain map

Load one owner per domain. Roles marked "always on" are loaded by every build skill.

| Need | Owner | Notes |
|---|---|---|
| Deciding what NOT to write; effort levels; agent scope | `fswpdevops/references/lean-coding.md` | Always on |
| Coding standards (PHP, JS, CSS, HTML), inline docs, i18n, accessibility | `fswpdevops/references/coding-standards.md` | Always on |
| Escaping, sanitizing, nonces, capabilities, SQL safety, secrets | `fswpdevops-security` | Always on; house depth in its `references/security.md` |
| Plugin structure, lifecycle, admin UI, data, cron, scaffold | `fswpdevops-plugin` | Templates and `scaffold_plugin.py` |
| Theme structure: block, classic, hybrid, child; theme.json, templates, patterns | `fswpdevops-theme` | `scaffold_theme.py` |
| Changing existing code; add-ons for products you do not own | `fswpdevops-maintainer` | Parity, deprecation, host compatibility |
| Core patches, Trac, wordpress-develop, Core tests | `fswpdevops-core` | Ticket-first |
| Design language: theme.json tokens, patterns, native-first, states, respecting a site's existing look | `fswpdevops-designer` | `references/design-language.md` |
| Design and UX critique of finished UI (read-only) | `fswpdevops-critic` | `references/ux-rubric.md` |
| Custom blocks, block.json, dynamic rendering, patterns, Interactivity API | `fswpdevops-block` | `references/block-json.md` verified against the handbook |
| REST routes, schemas, permissions, Abilities API register/audit/verify | `fswpdevops-api` | |
| Queries, caching, assets, autoload, cron, profiling | `fswpdevops-performance` | |
| Local environments, Playground and Blueprints, command line, PHPCS, PHPStan, tests | `fswpdevops-ci` | |
| WordPress.org submission, headers, readme, versioning, packaging, licensing | `fswpdevops-release` | Plugin guidelines and theme requirements verified |
| Triage of an existing repo | `fswpdevops-architect` (`scripts/detect_wp_project.py`) | |
| Gate, checklist, scenarios, scope check | `fswpdevops-qa` | `qa_check.py`, `theme_check.py` |
| Independent review, API risk map, lean audit | `fswpdevops-reviewer` | Agent `fswpdevops-code-reviewer` |
| Public-facing output on the Atomic Framework | `fswpdevops-plugin` (`references/frontend-output.md`) | House-only; user supplies the Atomic Framework files |
| Admin UI (native, React screen, Tier 3 app) | `fswpdevops-plugin` (`references/admin-ui.md`, `modern-app-stack.md`) | |

If the domain itself is unclear (a repo that could be theme, plugin, or Core checkout), run the triage script first; its report names the project type.
