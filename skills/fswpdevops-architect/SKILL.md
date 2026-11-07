---
name: fswpdevops-architect
description: Planning stage of Full-Stack WP DevOps. Classifies the work (new plugin, new theme, update to an existing plugin or theme, add-on for another product, or WordPress Core patch), triages existing code with a bundled detection script, asks one round of essential questions, does competitive research, and produces one reviewable PRD or change brief with a single approval gate. Also covers Migration mode and multi-session handoff docs. Invoked by fswpdevops before any code is written; use directly for PRD, change-brief, or handoff-doc questions.
license: MIT
metadata:
  displayName: "FSWPDevOps Architect"
  version: "0.7.0"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps Architect

No code is written until this stage ends with an approved PRD or change brief. Goal: every decision made in one question round and one reviewable document, zero back-and-forth afterward.

## Step 0: Work type and triage

- Confirm the work type from `fswpdevops/references/work-types.md`: **New plugin**, **New theme**, **Update**, **Add-on**, **Core patch**.
- **Update, Add-on, Core patch, or any unknown codebase:** run `python3 tools/detect_wp_project.py (copy `scripts/` to `./tools/` once per session, E9) <path>` first. It reports project type (plugin, theme, block theme, Core checkout, site, unknown), main file and header fields, version and minimum-version hints, tooling (Composer, npm, PHPCS, PHPStan, tests), and hooks/REST routes/blocks found. Quote the findings in the plan. The script only reads files.
- Plugin- or theme-shaped requests count even without the word "plugin" or "theme" (post types, REST integrations, admin dashboards, custom templates, site-wide styling, anything needing activation or uninstall behavior). Single-shortcode tools delivered as FluentSnippets files belong to `wordpress-mini-app-builder`, not here.

Before planning any change, apply the lean ladder (`fswpdevops/references/lean-coding.md`): read the touched code and list every touch point (callers, hooks, templates, tests, config, upgrade paths). The plan's file list is that list; plan the first ladder rung that works and name what you skipped.

## Step 0a: No PRD yet

If the user asks to start building and no PRD or change brief exists: ask them to provide one before starting. Do not begin implementation, and do not silently jump to Step 1 in its place. If the user explicitly insists ("just build it", "skip the PRD"), the requirement is waived: go straight to Step 1 and author the document from that question round.

## Step 0b: User-supplied PRD, AGENTS.md, architecture docs

Read them before writing code and check them against `fswpdevops-plugin/references/standards.md` and the other house rules.

- **No real conflict:** proceed with the supplied documentation plus house standards; house rules fill gaps.
- **Real conflict** (the document asks for something a house rule forbids, such as a security shortcut or naming scheme): name both sides plainly and ask which governs. Never quietly blend them.
- A supplied PRD still goes through Step 4; it is not exempt.

## Step 1: One round of essential questions

Use the structured question tool when available (Claude Code: AskUserQuestion; claude.ai: ask_user_input_v0); otherwise one compact numbered list. At most 3-4 questions, chosen by work type:

| Work type | Ask about |
|---|---|
| New plugin | Distribution target (WordPress.org, private zip, both); feature surface (post type, custom table, REST, cron, admin screen, front-end output); front-end design system (the user's own, if any, or neutral); static vs live behavior; code prefix/acronym for this project |
| New theme | Block theme or classic; distribution (WordPress.org theme directory, private, client site); starting point (from scratch, child of an existing theme); which content types and page layouts are required; code prefix/acronym for this project |
| Update | Goal (bug, feature, compatibility, refactor); how it is delivered (patch to a repo, zip, direct edits); what must not change |
| Add-on | Host product and supported version range; what the add-on adds; what should happen if the host is missing |
| Core patch | Ticket number or bug description; target component; whether a Trac ticket exists yet |

Everything open-ended (field names, business rules, edge cases, working name) is inferred and listed under PRD "Assumptions", not asked. No second round unless the first round's answers created a genuinely blocking fork.

**Prefix/acronym:** for new plugin and new theme work, ask what short acronym or prefix the project's code should use; if the user has none, propose 2-3 candidates derived from the project's own name and let them choose. There is no built-in default and this tool's own name or brand is never used as a stand-in. Full rule, the exact question wording, and the exceptions (theme's 4-letter minimum, product slug vs. code prefix, reserved names): `fswpdevops/references/brand-naming.md`. Never `WP` or `Plugin` as a prefix. On Update and Add-on work, do not ask; keep the project's existing prefix. Default minimum versions: WordPress 6.4, PHP 7.4; raise only for a specific need (for example PHP 8.1 for enums). Confirm current requirements in the official docs when it matters.

**Project information (same round, never a second):** company name, product name, author, contributors, and links (website, docs, support, repo). Ask only for what is not already stated. Never invent a missing value: an unstated link or contributor is left out of every generated file.

**Technology-stack decision:** for new work, decide admin-UI tier and JS tier before drafting the PRD (`fswpdevops-plugin/references/standards.md` section 2). For existing work, the existing stack stands unless there is a stated reason to change it.

**Admin UI question (new plugins with an admin screen):** ask "React admin SPA vs native/BEM?" in the same round. Default is native; offer the React SPA only for an app-like admin (several interactive screens, real-time state, data tables, multi-step flows) and record the answer in the PRD. If React: follow `fswpdevops-plugin/references/modern-app-stack.md` (decision checklist first).

## Step 2: Competitive research

Apply the router's Official first rule and cite the source for each choice. 2-3 leading products in the category (WordPress.org directory or SaaS). Capture table-stakes features, common complaints, and conventions worth matching. A handful of searches; 3-5 bullets in the document. Skip for Core patches; research the ticket history instead.

## Step 3: The document

- **New plugin, new theme:** PRD from `references/prd-template.md` (theme variant notes inside).
- **Update, Add-on:** change brief from `references/change-brief-template.md`: current behavior, requested behavior, parity list (what must keep working), compatibility table, risks, test plan.
- **Core patch:** ticket-first brief from `references/change-brief-template.md` plus the steps in `fswpdevops-core`.

Run front-end behavior through the 5-point JS-tier checklist (`fswpdevops-plugin/references/frontend-output.md`) and state the tier. **Derived counts** (tokens, blocks, routes, screens) come from the data or code, never from memory.

## Step 4: Approval gate (the only one)

Present the document. Decisions are visible and already made; the user approves or corrects once. If the JS tier is Alpine, name it and get an explicit yes. No scaffolding or edits before approval; approved corrections are folded in first.

## Migration mode

For rebuilding an existing plugin on a new stack. Before any code changes:

1. **Baseline:** capture screenshots of every screen and state, plus reference exports (settings, data, generated files) from the old version. Store under `baseline/`.
2. **Parity matrix:** every old feature, setting, hook, shortcode, REST route, and stored option mapped to: kept / changed (why) / dropped (why). Nothing unlisted ships silently.
3. **Export diffing:** after the rebuild, regenerate the same exports and diff them against the baseline. Differences must be intended and listed.
4. **Visual-regression gate:** compare new screenshots to baseline for each screen; unexplained differences block delivery (feeds `fswpdevops-qa`).
5. **Data path:** an upgrade from the old version's stored data must work without reactivation (see `fswpdevops-qa`).

## Step 5: Handoff docs (multi-session builds)

When the build will span sessions, write both files into the plugin repo root (not the zip):

- `AGENTS.md`: what it is; commands (build, test, QA gate); architecture map; house rules and conventions; decisions and constraints; gotchas and do-not-touch; definition of done.
- `HANDOFF.md`: current state; code map (file: responsibility); **verified / not-verified table** (each PRD scenario with PASS / FAIL / NOT RUN and evidence); open items; next step.

Update both at every stop, and before ending any session that did not finish.

Finish with a scratchpad: work type, answers, PRD or change-brief path, approval status.
