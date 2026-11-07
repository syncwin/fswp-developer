---
name: fswpdevops
description: Full-Stack WP DevOps - the entry point and router for the whole WordPress development lifecycle. Use whenever the user wants to build a custom theme (block or classic) or plugin, update or fix an existing theme or plugin, create an add-on for another product (WooCommerce extension, page-builder element, plugin extension), contribute a patch to WordPress Core, or review, secure, optimize, or ship WordPress code; also when they invoke /fswpdevops. Classifies the work, then sequences fswpdevops-architect, a build skill (fswpdevops-plugin, fswpdevops-theme, fswpdevops-maintainer, fswpdevops-core), fswpdevops-qa, fswpdevops-critic (UI work), and fswpdevops-reviewer, backed by role skills for security, blocks, APIs, performance, tooling, and release, on top of the always-applied lean-coding and coding-standards references this skill owns. Not for single-shortcode FluentSnippets tools (that is wordpress-mini-app-builder).
license: MIT
metadata:
  displayName: "Full-Stack WP DevOps"
  version: "0.7.0"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps Developer (router)

Router only. Each rule lives in the skill or reference that owns it. Everything is self-contained in `skills/`; there are no external skill dependencies. Official WordPress documentation is linked, not copied: `references/official-docs.md`.

## Trigger

`/fswpdevops` is the only trigger this plugin defines. It also activates on a plain-language request to build, update, review, secure, or ship WordPress code, since that is what this router exists to classify. No other command or phrase is treated as a trigger.

## Step 1: Classify the work

| The user wants to... | Work type | Build skill |
|---|---|---|
| Make a new plugin | New plugin | `fswpdevops-plugin` |
| Make a new theme (block or classic) | New theme | `fswpdevops-theme` |
| Change, fix, or upgrade a plugin or theme that exists | Update | `fswpdevops-maintainer` |
| Build on a product they do not own | Add-on | `fswpdevops-maintainer` (add-on mode) with `fswpdevops-plugin` for structure |
| Fix a bug or add a feature in WordPress itself | Core patch | `fswpdevops-core` |
| Review or audit code they already have | Review only | `fswpdevops-reviewer` (skip to step 3) |

Unclear or mixed? Ask one question. Details: `references/work-types.md`.

## Step 2: Sequence (never skip or reorder)

1. **`fswpdevops-architect`**: triage the code (Update, Add-on, Core), one question round, research, PRD or change brief, the single approval gate. Includes the brand-prefix decision (`references/brand-naming.md`).
2. **Build skill** from the table. `references/lean-coding.md`, `references/coding-standards.md`, and `fswpdevops-security` are foundational and always applied. Load other role skills only for the domains the plan lists (`references/domain-map.md`).
3. **`fswpdevops-qa`**: mechanical gate, tool checks, checklist, scenarios, scope check. Every result is PASS, FAIL, or NOT RUN; NOT RUN is never reported as a pass.
4. **`fswpdevops-critic`** (only when the change has UI): read-only design and UX critique of rendered front end, block editor and admin screens, after the build and before the reviewer; structured findings with severity, evidence and fix. Builders fix what it finds.
5. **`fswpdevops-reviewer`**: independent read-only review. In Claude Code delegate to the `fswpdevops-code-reviewer` agent so build reasoning stays out; without agents, run it as a separate pass and disclose it as a self-review.
6. **Fix loop**: fix every Critical and Important finding from steps 3 to 5, then re-run 3 to 5 on the changed files only.
7. **Ship**: `fswpdevops-release` when the target is a directory or a release; then deliver the zip, patch, or PR-ready diff with a short summary.

## Selection rules

- **One owner per domain** (`references/domain-map.md`). Do not re-derive its rules elsewhere.
- **Official first, at every stage (research before building).** Before choosing an approach, file, tool, config or dependency, check current official docs and widely recommended, secure practice; cite the source in the docs or brief; mark anything unverified; never guess. Keep research scoped to what the task needs (smallest complete change). Precedence: developer.wordpress.org documentation and coding standards, then role skills, then build-skill house rules; house rules may be stricter, never looser (`references/precedence.md`).
- **Triage runs once** at the start of Update, Add-on, and Core work (`fswpdevops-architect/scripts/detect_wp_project.py`).
- **Never invent facts about the user's project.** Names, links, versions, and credentials not given are left out.

## Foundational, always applied

Every build and maintenance skill applies these without being asked, because they are base-layer behavior rather than a domain:

- **`references/lean-coding.md`**: write less. Before adding anything, ask whether the plan requires it, whether the project, WordPress core, or PHP already provides it, and whether a setting or core block would do instead of code.
- **`references/coding-standards.md`** (with `references/i18n.md` and `references/accessibility.md`): PHP/JS/CSS/HTML standards, inline documentation, translation, and accessibility.
- **`references/brand-naming.md`**: use the `sw` brand acronym in generated code wherever it does not conflict with WordPress conventions, a framework, a dependency, or a naming requirement.
- **`fswpdevops-security`**: input, output, authorization. Kept as its own skill, not folded in here, because its house depth (`references/security.md`) is substantial and it is also loaded independently during review.

Keep replies short: lead with the result, list decisions and open items only. Load only what the current task needs; do not re-analyze what has not changed; use the reviewer agent once per pass with a single lens and a narrow scope (code folder and plan, never the build transcript).

## Degradation

Works on claude.ai without a dependency system and often without PHP. `qa_check.py` and `theme_check.py` (Python, standard library only) always run. PHP-based checks report NOT RUN with the exact command the user can run. Live-site checks need a real WordPress and are NOT RUN elsewhere. Without agents, review runs as a disclosed self-review.

## Stable contract

External workflows may rely on these; they change only with an old-to-new mapping in `CHANGELOG.md`:

- Plugin slug `fswpdevops`; this router skill is `fswpdevops` because every skill name in this plugin begins with `fswpdevops-` to avoid collisions.
- Trigger: `/fswpdevops`, and plain-language WordPress build/update/review requests.
- Skills: `fswpdevops-architect`, `fswpdevops-plugin`, `fswpdevops-theme`, `fswpdevops-maintainer`, `fswpdevops-core`, `fswpdevops-qa`, `fswpdevops-reviewer`, `fswpdevops-release`, `fswpdevops-security`, `fswpdevops-api`, `fswpdevops-block`, `fswpdevops-designer`, `fswpdevops-critic`, `fswpdevops-performance`, `fswpdevops-ci`; agent `fswpdevops-code-reviewer`.
- Foundational references (not separate skills): `references/lean-coding.md`, `references/coding-standards.md`.
- Result vocabulary: PASS, FAIL, NOT RUN.
- 0.1.x, 0.2.x, and 0.3.x names map to these in `CHANGELOG.md`.

## Reference index

| File | Read it for |
|---|---|
| `references/work-types.md` | Classifying the request and what each work type changes |
| `references/domain-map.md` | Which skill or reference owns which domain |
| `references/precedence.md` | Reconciling official docs, role skills, and house rules |
| `references/official-docs.md` | Canonical developer.wordpress.org and make.wordpress.org links, with what was verified |
| `references/lean-coding.md`, `references/wordpress-shortcuts.md` | Foundational: writing less |
| `references/coding-standards.md`, `references/i18n.md`, `references/accessibility.md` | Foundational: how code is written |
| `references/brand-naming.md` | The `sw` brand-acronym rule and its exceptions |
| `references/github-foundation.md` | Reserved GitHub integration points (not implemented) |

Finish with a scratchpad: request, work type, decisions, gate results, open items.
