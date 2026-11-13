# Handoff — Full-Stack WP DevOps

Read this first in a new session.

## What this is
A single MIT-licensed Claude plugin for the whole WordPress lifecycle: new themes, new plugins, updates, add-ons, Core patches. Display name "Full-Stack WP DevOps"; plugin slug and router skill are both `fswpdevops` (identical name, not just a shared prefix). 13 other role skills, all prefixed `fswpdevops-`, plus 1 agent. No external skill dependencies, no forked third-party skills. Trigger: `/fswpdevops` only — no phrase-based aliases.

## Layout
```
.claude-plugin/plugin.json, marketplace.json     (name: fswpdevops, displayName: "Full-Stack WP DevOps")
skills/  fswpdevops (router; owns the foundational references below)
         fswpdevops-plan  fswpdevops-plugin  fswpdevops-theme  fswpdevops-maintain  fswpdevops-core
         fswpdevops-qa  fswpdevops-review  fswpdevops-security  fswpdevops-api  fswpdevops-block
         fswpdevops-performance  fswpdevops-ci  fswpdevops-release
  fswpdevops/references/  lean-coding.md + wordpress-shortcuts.md   (foundational: write less)
                               coding-standards.md + i18n.md + accessibility.md  (foundational: how code is written)
                               brand-naming.md  (ask-first project prefix, no built-in default)
agents/fswpdevops-code-review.md
docs/  github-integration.md  trademarks.md
.github/  issue and PR templates (foundation only)
LICENSE  CREDITS.md  SECURITY.md  CONTRIBUTING.md  CHANGELOG.md
```

## Rules to keep
- **Names.** Plugin slug and router skill are both `fswpdevops` — literally the same name, not just the same prefix. Every other skill starts with `fswpdevops-` and names a role (`fswpdevops-plugin`, not `fswp-plugin-development`).
- **One license (MIT).** Never vendor or copy third-party skills or handbook text; write independently and link to official docs. Credit ideas in `CREDITS.md`.
- **Foundational vs. skill.** `fswp-lean-engineer` and `fswp-standards-engineer` are gone on purpose — they're always-on writing disciplines, not domains, so they live as `fswpdevops/references/*.md`. Don't recreate them as standalone skills; add depth to the reference files instead. `fswpdevops-security` stayed separate deliberately (real house depth, loaded independently by review) — that's the bar for "keep it separate" going forward.
- **No fixed brand acronym.** There is no default prefix like "sw" baked into this tool. For new plugin/theme work, `fswpdevops-plan` asks the project owner for their own short code-level prefix in the same question round as everything else (proposing candidates from the project's name if they have none). Update/Add-on work keeps the existing project's prefix and never asks. Full rule: `fswpdevops/references/brand-naming.md`.
- **Atomic Framework**, not "SWWp design system." That's the real name of the reusable, user-supplied front-end system; its code-level tokens use the acronym `afw-`/`AFW` (`afw-tokens.css`, `afw-components.css`, `afw-foundation-logics.js`) referenced by `fswpdevops-plugin`. It is never bundled; always ask for the current files.
- **Display name has no publisher suffix.** SyncWin appears in `plugin.json` author/homepage and `marketplace.json` owner, not in the visible plugin name. Author identity is `@wasimness`, company `SyncWin`.
- Names/slugs use "WP", not "WordPress" (descriptions may say WordPress to describe compatibility). See `docs/trademarks.md`.
- Result vocabulary is PASS / FAIL / NOT RUN. Never report NOT RUN as a pass.
- Never invent project facts (names, links, versions).
- Contact: support@syncwin.com.

## Verified vs. not verified
- Verified this session: `detect_wp_project.py`, `theme_check.py`, `scaffold_theme.py`, and `scaffold_plugin.py` all run and pass with a generic example prefix (`acme`); every `.py`/`.sh` script passes a syntax check; the router/plugin name unification and the Atomic Framework rename were grepped clean across the whole tree.
- Verified in an earlier session (2026-09-28): official pages for coding standards, block.json, plugin headers, readme.txt, theme style.css, plugin guidelines, theme requirements, trademark policy, Core handbook Git/PHPUnit pages.
- **NOT RUN / still open:** PHP-based tools (PHPCS, PHPStan, `php -l`) — no PHP in this environment. `claude plugin validate` and a real Claude Code install test have not been run. Playwright MCP was unavailable this session (TinyFish was used for fetches instead). Most `official-docs.md` links and all of `fswpdevops-ci`'s Blueprint/CLI table are canonical paths, not freshly re-fetched.

## Next steps
1. Run `claude plugin validate` and a local install test.
2. Publish the repo, fill the `<github-user>` placeholder in README, then add GitHub integration (`docs/github-integration.md`).
3. Have counsel confirm the name/trademark position and the MIT-only decision before a paid launch.

---

## Handoff checklist prompt — paste this to start a new chat

```
Continue work on the "Full-Stack WP DevOps" Claude plugin (slug fswpdevops).
It's attached/uploaded as a zip — read HANDOFF.md in it first for full context,
current structure, the rules that must be kept (naming, no fixed brand acronym,
Atomic Framework naming, MIT-only licensing, /fswpdevops as the only trigger), and the
open items under "Next steps" and "NOT RUN / still open."

Once you've read HANDOFF.md, here's what I want to do next: [describe the task].
```
