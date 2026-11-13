---
name: fswpdevops
description: Full-Stack WP DevOps - the entry point and router for the whole WordPress development lifecycle. Use whenever the user wants to build a custom theme (block or classic) or plugin, update or fix an existing theme or plugin, create an add-on for another product (WooCommerce extension, page-builder element, plugin extension), contribute a patch to WordPress Core, or review, secure, optimize, or ship WordPress code; also when they invoke /fswpdevops. Classifies the work, then sequences fswpdevops-plan, a build skill (fswpdevops-plugin, fswpdevops-theme, fswpdevops-maintain, fswpdevops-core), fswpdevops-qa, fswpdevops-critic (UI work), and fswpdevops-review, backed by role skills for security, blocks, APIs, performance, tooling, and release, on top of the always-applied lean-coding and coding-standards references this skill owns. Not for single-shortcode FluentSnippets tools (that is wordpress-mini-app-builder).
---

# FSWPDevOps Developer (router)

Router only. Each rule lives in the skill or reference that owns it. Everything is self-contained in `skills/`; there are no external skill dependencies. Official WordPress documentation is linked, not copied: `references/official-docs.md`.

## Trigger

`/fswpdevops` is the only trigger this plugin defines. It also activates on a plain-language request to build, update, review, secure, or ship WordPress code, since that is what this router exists to classify. No other command or phrase is treated as a trigger.

## Step 1: Routing table (exact slugs; first matching row wins)

Read top to bottom. A row matches when any trigger phrase appears in the request as whole words (case-insensitive) and none of its `!` phrases does. Checked against `evals/router/cases.json`. Work that changes code starts at the build skill of its row, but Step 2 still puts `fswpdevops-plan` (brief and approval) before it unless an approved brief already exists.

| Order | Trigger phrases | Skill | Then |
|---|---|---|---|
| 0 | critique; critic; ux review; usability; visual hierarchy; design review | `fswpdevops-critic` | `fswpdevops-review` |
| 1 | core patch; trac; wordpress core; wordpress-develop; core contribution; gutenberg repository | `fswpdevops-core` | `fswpdevops-qa`, `fswpdevops-review` |
| 2 | review; code review; audit; over-engineered; over-engineering; security issues; code quality; tech debt | `fswpdevops-review` | (none) |
| 3 | release; package; publish; submit; wordpress.org; plugin directory; theme directory; zip; svn; version bump; ship it | `fswpdevops-release` | (none) |
| 4 | toolchain; wp-env; playground; blueprint; wp-cli; github actions; ci pipeline; set up ci; docker; local environment | `fswpdevops-ci` | (none) |
| 5 | performance; slow; slow query; queries; caching; transient; core web vitals; page speed; autoload; lcp | `fswpdevops-performance` | (none) |
| 6 | design tokens; spacing; looks better; typography; color palette; style variation; visual design; design language | `fswpdevops-design` | `fswpdevops-critic` |
| 7 | block.json; custom block; gutenberg block; interactivity api; block pattern; block variation; block binding | `fswpdevops-block` | `fswpdevops-qa` |
| 8 | rest api; rest route; endpoint; abilities api; application password; register_rest_route | `fswpdevops-api` | `fswpdevops-qa` |
| 9 | security; secrets; vulnerability; vulnerabilities; sanitize; escaping; nonce; capability check; xss; csrf; sql injection; threat model; api keys | `fswpdevops-security` | (none) |
| 10 | plan; prd; change brief; what would it take; estimate; scope the work | `fswpdevops-plan` | `fswpdevops-plugin`, `fswpdevops-theme`, `fswpdevops-maintain` |
| 11 | fix; bug; refactor; upgrade; migrate; migration; regression; deprecated; crash; fatal error; existing plugin; existing theme; add-on; addon; woocommerce extension | `fswpdevops-maintain` | `fswpdevops-qa`, `fswpdevops-review` |
| 12 | new theme; build me a theme; create a theme; block theme; classic theme; child theme; theme.json; site editor | `fswpdevops-theme` | `fswpdevops-qa`, `fswpdevops-critic`, `fswpdevops-review` |
| 13 | new plugin; build me a plugin; create a plugin; scaffold; shortcode; custom post type; settings page; uninstall; activation hook | `fswpdevops-plugin` | `fswpdevops-qa`, `fswpdevops-critic`, `fswpdevops-review` |
| 14 | qa; gate; run the gate; phpcs; phpstan; tests; phpunit; lint; verify; scenarios | `fswpdevops-qa` | `fswpdevops-review` |

**Tie-break rules** (the row order encodes them): judging finished UI -> `fswpdevops-critic`; judging finished code -> `fswpdevops-review`; changing how a screen looks -> `fswpdevops-design`; a request to plan or estimate without changing code -> `fswpdevops-plan`; fixing, upgrading or extending existing code or an add-on -> `fswpdevops-maintain`; a new theme -> `fswpdevops-theme`; a new plugin -> `fswpdevops-plugin`; a patch to WordPress itself -> `fswpdevops-core`; checking only, no changes -> `fswpdevops-qa`. A request that fits two rows runs the earlier row first, then the later one if the user wants it. Design details of the work types are in `references/work-types.md`.

**Default when no row matches:** do not guess and never answer or start the task itself in the routing step. Ask one closed question with these options and stop: "Is this (a) a new plugin or theme, (b) a fix, upgrade or add-on for existing WordPress code, (c) a check or review of code you have, (d) setup, tooling or release, (e) a patch to WordPress Core, or (f) something else, such as a single shortcode snippet or a blog post, which this plugin does not handle?"

**How to load the chosen skill:** call the Skill tool with the full slug `fswpdevops:<skill>` (for example `fswpdevops:fswpdevops-maintain`) and follow it. On a surface without the Skill tool, read that skill's `SKILL.md` by relative path from the plugin root (`skills/<skill>/SKILL.md`) and follow it.

## Step 2: Sequence (never skip or reorder)

1. **`fswpdevops-plan`**: triage the code (Update, Add-on, Core), one question round, research, PRD or change brief, the single approval gate. Includes the brand-prefix decision (`references/brand-naming.md`).
2. **Build skill** from the table. `references/lean-coding.md`, `references/coding-standards.md`, and `fswpdevops-security` are foundational and always applied. Load other role skills only for the domains the plan lists (`references/domain-map.md`).
3. **`fswpdevops-qa`**: mechanical gate, tool checks, checklist, scenarios, scope check. Every result is PASS, FAIL, or NOT RUN; NOT RUN is never reported as a pass.
4. **`fswpdevops-critic`** (only when the change has UI): read-only design and UX critique of rendered front end, block editor and admin screens, after the build and before the reviewer; structured findings with severity, evidence and fix. Builders fix what it finds.
5. **`fswpdevops-review`**: independent read-only review. In Claude Code delegate to the `fswpdevops-code-review` agent so build reasoning stays out; without agents, run it as a separate pass and disclose it as a self-review.
6. **Fix loop**: fix every Critical and Important finding from steps 3 to 5, then re-run 3 to 5 on the changed files only.
7. **Ship**: `fswpdevops-release` when the target is a directory or a release; then deliver the zip, patch, or PR-ready diff with a short summary.

## Selection rules

- **One owner per domain** (`references/domain-map.md`). Do not re-derive its rules elsewhere.
- **Official first, at every stage (research before building).** Before choosing an approach, file, tool, config or dependency, check current official docs and widely recommended, secure practice; cite the source in the docs or brief; mark anything unverified; never guess. Keep research scoped to what the task needs (smallest complete change). Precedence: developer.wordpress.org documentation and coding standards, then role skills, then build-skill house rules; house rules may be stricter, never looser (`references/precedence.md`).
- **Site and script rules (E1 native first, E7 learn the site first, E9 script paths):** `references/lean-coding.md`.
- **Triage runs once** at the start of Update, Add-on, and Core work (`fswpdevops-plan/references/detect_wp_project.md`).
- **Never invent facts about the user's project.** Names, links, versions, and credentials not given are left out.

## Foundational, always applied

Every build and maintenance skill applies these without being asked, because they are base-layer behavior rather than a domain:

- **`references/lean-coding.md`**: write less. Before adding anything, ask whether the plan requires it, whether the project, WordPress core, or PHP already provides it, and whether a setting or core block would do instead of code.
- **`references/coding-standards.md`** (with `references/i18n.md` and `references/accessibility.md`): PHP/JS/CSS/HTML standards, inline documentation, translation, and accessibility.
- **`references/brand-naming.md`**: use the `sw` brand acronym in generated code wherever it does not conflict with WordPress conventions, a framework, a dependency, or a naming requirement.
- **`fswpdevops-security`**: input, output, authorization. Kept as its own skill, not folded in here, because its house depth (`references/security.md`) is substantial and it is also loaded independently during review.

Keep replies short: lead with the result, list decisions and open items only. Load only what the current task needs; do not re-analyze what has not changed; use the reviewer agent once per pass with a single lens and a narrow scope (code folder and plan, never the build transcript).

## Degradation

Works on claude.ai without a dependency system and often without PHP. The house-rules checks (`qa_check.md`, `theme_check.md`, `docs_gate.md` in `fswpdevops-qa/references/`) need no tools and always run. PHP-based checks report NOT RUN with the exact command the user can run. Live-site checks need a real WordPress and are NOT RUN elsewhere. Without agents, review runs as a disclosed self-review.

## Stable contract

External workflows may rely on these; they change only with an old-to-new mapping in `CHANGELOG.md`:

- Plugin slug `fswpdevops`; this router skill is `fswpdevops` because every skill name in this plugin begins with `fswpdevops-` to avoid collisions.
- Trigger: `/fswpdevops`, and plain-language WordPress build/update/review requests.
- Skills: `fswpdevops-plan`, `fswpdevops-plugin`, `fswpdevops-theme`, `fswpdevops-maintain`, `fswpdevops-core`, `fswpdevops-qa`, `fswpdevops-review`, `fswpdevops-release`, `fswpdevops-security`, `fswpdevops-api`, `fswpdevops-block`, `fswpdevops-design`, `fswpdevops-critic`, `fswpdevops-performance`, `fswpdevops-ci`; agent `fswpdevops-code-review`.
- Foundational references (not separate skills): `references/lean-coding.md`, `references/coding-standards.md`.
- Result vocabulary: PASS, FAIL, NOT RUN.
- 0.1.x to 0.7.x names map to these in `CHANGELOG.md`.

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
