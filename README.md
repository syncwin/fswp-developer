# Full-Stack WP Developer

A Claude plugin covering the whole WordPress development lifecycle. Say what you want built or changed; it classifies the work, plans it, builds it, runs a mechanical QA gate, and hands the result to an independent reviewer.

**It handles:** custom themes (block, classic, child), custom plugins, updates to existing themes and plugins, add-ons for products you do not own, and patches for WordPress Core.

Trigger with `/fswp`, or just describe the job in plain language. Every skill name starts with `fswp-` to avoid colliding with other skills, and names a role rather than an activity (`fswp-plugin-developer`, not `fswp-plugin-development`).

## How it works

```
classify → fswp-architect → build role (plugin | theme | maintain | core) → fswp-qa-engineer → fswp-reviewer → fix loop → fswp-release-manager → deliver
```

Always on during any build: `fswp-developer/references/lean-coding.md` (write less, reuse first), `fswp-developer/references/coding-standards.md` (coding standards, docs, i18n, accessibility), `fswp-security-engineer` (input, output, authorization).

| Skill | Role |
|---|---|
| `fswp-developer` | Router: classifies the work and sequences the rest |
| `fswp-architect` | Triage, one question round, research, PRD or change brief, one approval gate |
| `fswp-plugin-developer` | New plugins: scaffold script, lifecycle, data, REST, admin UI, front-end, i18n |
| `fswp-theme-developer` | New themes: block, classic, child; scaffold script; theme.json, templates, patterns |
| `fswp-maintainer` | Safe changes to existing plugins/themes; add-on structure and host compatibility |
| `fswp-core-contributor` | Trac ticket, wordpress-develop setup, patch or PR, tests, ticket comment |
| `fswp-qa-engineer` | Plugin and theme gates, PHPCS, PHPStan, checklist, scenarios, scope check |
| `fswp-reviewer` | Independent security, quality, and lean review (agent `fswp-code-reviewer`) |
| `fswp-release-manager` | WordPress.org guidelines, headers, readme, versioning, packaging |
| `fswp-security-engineer` | Sanitize/escape tables, authorization, nonces |
| `fswp-developer/references/coding-standards.md` | PHP/JS/CSS/HTML standards, PHPDoc, i18n, accessibility |
| `fswp-api-developer` | REST routes, schemas, permissions, Abilities API |
| `fswp-block-developer` | Blocks, block.json, patterns, Interactivity API |
| `fswp-performance-engineer` | Queries, caching, assets, cron |
| `fswp-devops-engineer` | wp-env, Playground, command line, PHPCS/PHPStan setup |
| `fswp-developer/references/lean-coding.md` | Decide what not to write, before every build |

Official WordPress documentation is linked, not copied: `skills/fswp-developer/references/official-docs.md`. Verified pages (fetched and read on 2026-09-28) are marked "(checked)" there; others are canonical paths, confirmed on first real use.

## Install

- **claude.ai, desktop app, mobile (auto-updates):** Settings → Customize → Plugins → Add → Add marketplace → `syncwin/fswp-developer`, then install Full-Stack WP Developer.
- **Claude Code terminal (instead of the app):** `claude plugin marketplace add syncwin/fswp-developer`, then `claude plugin install fswp-developer@syncwin-fswp-developer`.

Or locally: unzip and run `claude --plugin-dir ./fswp-developer`. No external dependencies; PHP-based checks report NOT RUN with the exact command to run when PHP is missing.

## Tools you can run yourself

```bash
python3 skills/fswp-architect/scripts/detect_wp_project.py <folder>          # what kind of project is this?
python3 skills/fswp-theme-developer/scripts/scaffold_theme.py --help         # block, classic, or child theme
python3 skills/fswp-plugin-developer/scripts/scaffold_plugin.py --help       # plugin skeleton
bash skills/fswp-qa-engineer/scripts/setup_toolchain.sh                      # once: PHPCS + PHPStan without Composer
bash skills/fswp-qa-engineer/scripts/run_gate.sh <folder> [min-php] [--fix]  # full gate for a plugin or theme
python3 skills/fswp-qa-engineer/scripts/theme_check.py <theme-dir> [--directory]
```

## Honest limits

- AI-assisted output is not a guarantee of security or correctness. Read the code, test on staging, and get a professional audit for sensitive plugins. See `SECURITY.md`.
- Live-site checks (Plugin Check, activation on a real install) need a real WordPress; otherwise NOT RUN.
- GitHub integration is planned, not implemented (`docs/github-integration.md`).
- `fswp-devops-engineer`'s Blueprint and command-line references, and most `official-docs.md` links, are canonical paths as documented rather than freshly fetched; confirm on first real use since WordPress moves quickly.

## License, credits, contact

MIT (`LICENSE`), one license for the whole package. Ideas we learned from are credited, not copied, in `CREDITS.md`. Naming and trademark notes: `docs/trademarks.md`. WordPress and WP are trademarks of the WordPress Foundation; this project is independent of it.

Support: **support@syncwin.com** · Author: @wasimness, SyncWin (https://syncwin.com)
