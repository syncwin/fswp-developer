# fswpdevops agent guide

Full-Stack WP DevOps Claude plugin: WordPress plugin, theme, block, Core and add-on lifecycle.

**Structure:** `adapters/claude/` is the shipped plugin (text only: `.claude-plugin/plugin.json`, `skills/fswpdevops*` router + 14 role skills with recipes in `references/`, `agents/fswpdevops-code-review.md`, `evals/` (trigger evals and `router/cases.json`), `prompts/`, README, CHANGELOG, LICENSE, PUBLIC-SAFETY.md); `dev/` holds maintainer-only Python and shell tools plus `templates/` (never shipped); `docs/`, `.claude-plugin/marketplace.json` (source `./adapters/claude`), `HANDOFF.md` (older handoff notes). `main` is the only branch.

## Commands
- Strict validation (must pass): `python <aiaddon>/dev/aiaddon-review/scripts/validate_extension.py adapters/claude --strict --target directory --require-meta author,company`
- Router check: `python <aiaddon>/dev/aiaddon-review/scripts/route_check.py adapters/claude`
- Secret and private-data scan: `python <aiaddon>/dev/aiaddon-review/scripts/scan_secrets.py . --history`; false positives only in `.public-safety-allow`
- Recipes (what the old scripts did) live in `adapters/claude/skills/*/references/`: `detect_wp_project.md`, `scaffold_plugin.md` (+ `templates-core|features|ui|readme.md`), `scaffold_theme.md` (+ `scaffold_theme_files.md`), `qa_check.md`, `theme_check.md`, `docs_gate.md`, `run_gate.md`, `setup_toolchain.md`. The originals stay in `dev/` as maintainer tooling: `python dev/fswpdevops-plan/scripts/detect_wp_project.py <dir>`, `bash dev/fswpdevops-qa/scripts/run_gate.sh <plugin-dir> [min-php, default 7.4] [--fix]`, `python dev/fswpdevops-qa/scripts/qa_check.py <plugin-dir> [--json]`, `python dev/fswpdevops-qa/scripts/theme_check.py <theme-dir> [--directory]`, `python dev/fswpdevops-qa/scripts/docs_gate.py <dir> [--base REF] [--static]`, `dev/fswpdevops-plugin/scripts/scaffold_plugin.py`, `dev/fswpdevops-theme/scripts/scaffold_theme.py`, `dev/fswpdevops-qa/scripts/setup_toolchain.sh` (pins in `toolchain.lock`). `dev/templates/` holds the plugin template files; the `templates-*.md` references must stay byte-identical to them inside the fences. Keep recipe and script behaviour in step.
- Validate: `claude plugin validate . --strict`
- Evals (real model calls): copy `adapters/claude` to a scratch folder, then run `claude plugin eval <scratch copy> --trust-plugin --ablation none --scaffold --allow-tools Read Glob Grep Skill -j 4 --no-publish` (model-run case folders, if any, live in `dev/evals/` and are copied into the scratch copy's `evals/`; there are none yet). Rebuild cases with `python <owner-tools>/plugin-evals/regen_evals.py <plugin> <router> <fixture ids>`. Write results outside the repo (`<owner-outputs>/<plugin>/eval-results`, a local folder outside the repo); the packager includes repo files.

## Workflow
1. Read the skill or script you change, plus its neighbours.
2. Make the smallest change; run the closest check, then the full gate.
3. Update `CHANGELOG.md` for behavior changes; log ideas in `IMPROVEMENTS.md`.

## Rules
- **Directory compliance:** the shipped plugin (`adapters/claude`) has no hooks, no scripts or other non-text files, and text-only frontmatter (`name`, `description`). Features that were scripts are recipes in `skills/*/references/`; Python and shell in `dev/` is maintainer tooling only.
- **Never publish secrets or private data** (keys, tokens, passwords, personal contact data, client names, internal URLs, local paths); the secret scan blocks every commit and release.
- Naming standard (validator `P019` to `P023`): router skill name == plugin name; every other skill, agent and command is prefixed `fswpdevops-`; action-style slugs (`-review`, not `-reviewer`). Router standard (`P024` to `P028`): routing table, tie-breaks, default question, Skill-tool loading, router evals.
- Run the closest check and the full gate before committing. Never delete or weaken tests or evals. Report failed, skipped or timed-out runs honestly; NOT RUN is never a pass.
- Follow neighbouring files. Keep each `SKILL.md` under 500 lines; move detail into `references/`.
- On release, bump `version` in `adapters/claude/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` together (skills carry no `metadata` block: directory policy wants text-only frontmatter); add a `CHANGELOG.md` entry per behavior change and copy it to `adapters/claude/CHANGELOG.md`.
- No commits, pushes or PRs unless asked. Work on a branch and open a PR; never push to main.
- No new dependencies without asking (scripts stay on the Python standard library).
- Never commit secrets. Never pick names or slugs without user confirmation.
- Say "WP", not "WordPress", in plugin and skill names (trademark policy, `docs/trademarks.md`). Foundational rules live once in `adapters/claude/skills/fswpdevops/references/`.

## Model routing
Opus plans, decides, writes self-contained briefs with a report word limit, and reviews every result. Haiku for search, reading and mechanical edits. Sonnet for coding, tests and multi-step work. Do 1-2 tool calls inline.

## Docs
README.md, CONTRIBUTING.md, CHANGELOG.md, HANDOFF.md, docs/; ideas and feedback in `IMPROVEMENTS.md`.
