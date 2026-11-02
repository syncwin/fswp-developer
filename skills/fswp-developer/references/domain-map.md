# Domain map

Load one owner per domain. Roles marked "always on" are loaded by every build skill.

| Need | Owner | Notes |
|---|---|---|
| Deciding what NOT to write; effort levels; agent scope | `fswp-developer/references/lean-coding.md` | Always on |
| Coding standards (PHP, JS, CSS, HTML), inline docs, i18n, accessibility | `fswp-developer/references/coding-standards.md` | Always on |
| Escaping, sanitizing, nonces, capabilities, SQL safety, secrets | `fswp-security-engineer` | Always on; house depth in its `references/security.md` |
| Plugin structure, lifecycle, admin UI, data, cron, scaffold | `fswp-plugin-developer` | Templates and `scaffold_plugin.py` |
| Theme structure: block, classic, hybrid, child; theme.json, templates, patterns | `fswp-theme-developer` | `scaffold_theme.py` |
| Changing existing code; add-ons for products you do not own | `fswp-maintainer` | Parity, deprecation, host compatibility |
| Core patches, Trac, wordpress-develop, Core tests | `fswp-core-contributor` | Ticket-first |
| Custom blocks, block.json, dynamic rendering, patterns, Interactivity API | `fswp-block-developer` | `references/block-json.md` verified against the handbook |
| REST routes, schemas, permissions, Abilities API register/audit/verify | `fswp-api-developer` | |
| Queries, caching, assets, autoload, cron, profiling | `fswp-performance-engineer` | |
| Local environments, Playground and Blueprints, command line, PHPCS, PHPStan, tests | `fswp-devops-engineer` | |
| WordPress.org submission, headers, readme, versioning, packaging, licensing | `fswp-release-manager` | Plugin guidelines and theme requirements verified |
| Triage of an existing repo | `fswp-architect` (`scripts/detect_wp_project.py`) | |
| Gate, checklist, scenarios, scope check | `fswp-qa-engineer` | `qa_check.py`, `theme_check.py` |
| Independent review, API risk map, lean audit | `fswp-reviewer` | Agent `fswp-code-reviewer` |
| Public-facing output on the Atomic Framework | `fswp-plugin-developer` (`references/frontend-output.md`) | House-only; user supplies the Atomic Framework files |
| Admin UI (native, React screen, Tier 3 app) | `fswp-plugin-developer` (`references/admin-ui.md`, `modern-app-stack.md`) | |

If the domain itself is unclear (a repo that could be theme, plugin, or Core checkout), run the triage script first; its report names the project type.
