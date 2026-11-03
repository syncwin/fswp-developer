# Full-Stack WP DevOps

A Claude plugin covering the whole WordPress development lifecycle. Say what you want built or changed; it classifies the work, plans it, builds it, runs a mechanical QA gate, and hands the result to an independent reviewer.

**It handles:** custom themes (block, classic, child), custom plugins, updates to existing themes and plugins, add-ons for products you do not own, and patches for WordPress Core.

Trigger with `/fswpdevops`, or just describe the job in plain language. Every skill name starts with `fswpdevops-` to avoid colliding with other skills, and names a role rather than an activity (`fswpdevops-plugin`, not `fswp-plugin-development`).

## How it works

```
classify → fswpdevops-architect → build role (plugin | theme | maintain | core) → fswpdevops-qa → fswpdevops-reviewer → fix loop → fswpdevops-release → deliver
```

Always on during any build: `fswpdevops/references/lean-coding.md` (write less, reuse first), `fswpdevops/references/coding-standards.md` (coding standards, docs, i18n, accessibility), `fswpdevops-security` (input, output, authorization).

| Skill | Role |
|---|---|
| `fswpdevops` | Router: classifies the work and sequences the rest |
| `fswpdevops-architect` | Triage, one question round, research, PRD or change brief, one approval gate |
| `fswpdevops-plugin` | New plugins: scaffold script, lifecycle, data, REST, admin UI, front-end, i18n |
| `fswpdevops-theme` | New themes: block, classic, child; scaffold script; theme.json, templates, patterns |
| `fswpdevops-maintainer` | Safe changes to existing plugins/themes; add-on structure and host compatibility |
| `fswpdevops-core` | Trac ticket, wordpress-develop setup, patch or PR, tests, ticket comment |
| `fswpdevops-qa` | Plugin and theme gates, PHPCS, PHPStan, checklist, scenarios, scope check |
| `fswpdevops-reviewer` | Independent security, quality, and lean review (agent `fswpdevops-code-reviewer`) |
| `fswpdevops-release` | WordPress.org guidelines, headers, readme, versioning, packaging |
| `fswpdevops-security` | Sanitize/escape tables, authorization, nonces |
| `fswpdevops/references/coding-standards.md` | PHP/JS/CSS/HTML standards, PHPDoc, i18n, accessibility |
| `fswpdevops-api` | REST routes, schemas, permissions, Abilities API |
| `fswpdevops-block` | Blocks, block.json, patterns, Interactivity API |
| `fswpdevops-performance` | Queries, caching, assets, cron |
| `fswpdevops-ci` | wp-env, Playground, command line, PHPCS/PHPStan setup |
| `fswpdevops/references/lean-coding.md` | Decide what not to write, before every build |

Official WordPress documentation is linked, not copied: `skills/fswpdevops/references/official-docs.md`. Verified pages (fetched and read on 2026-09-28) are marked "(checked)" there; others are canonical paths, confirmed on first real use.

## Install

- **claude.ai, desktop app, mobile (auto-updates):** Settings → Customize → Plugins → Add → Add marketplace → `syncwin/fswpdevops`, then install Full-Stack WP DevOps.
- **Claude Code terminal (instead of the app):** `claude plugin marketplace add syncwin/fswpdevops`, then `claude plugin install fswpdevops@syncwin-fswpdevops`.

Or locally: unzip and run `claude --plugin-dir ./fswpdevops`. No external dependencies; PHP-based checks report NOT RUN with the exact command to run when PHP is missing.

## Tools you can run yourself

```bash
python3 skills/fswpdevops-architect/scripts/detect_wp_project.py <folder>          # what kind of project is this?
python3 skills/fswpdevops-theme/scripts/scaffold_theme.py --help         # block, classic, or child theme
python3 skills/fswpdevops-plugin/scripts/scaffold_plugin.py --help       # plugin skeleton
bash skills/fswpdevops-qa/scripts/setup_toolchain.sh                      # once: PHPCS + PHPStan without Composer
bash skills/fswpdevops-qa/scripts/run_gate.sh <folder> [min-php] [--fix]  # full gate for a plugin or theme
python3 skills/fswpdevops-qa/scripts/theme_check.py <theme-dir> [--directory]
```

## Honest limits

- AI-assisted output is not a guarantee of security or correctness. Read the code, test on staging, and get a professional audit for sensitive plugins. See `SECURITY.md`.
- Live-site checks (Plugin Check, activation on a real install) need a real WordPress; otherwise NOT RUN.
- GitHub integration is planned, not implemented (`docs/github-integration.md`).
- `fswpdevops-ci`'s Blueprint and command-line references, and most `official-docs.md` links, are canonical paths as documented rather than freshly fetched; confirm on first real use since WordPress moves quickly.

## License, credits, contact

MIT (`LICENSE`), one license for the whole package. Ideas we learned from are credited, not copied, in `CREDITS.md`. Naming and trademark notes: `docs/trademarks.md`. WordPress and WP are trademarks of the WordPress Foundation; this project is independent of it.

Support: **support@syncwin.com** · Author: @wasimness, SyncWin (https://syncwin.com)
