# fswpdevops agent guide

Full-Stack WP DevOps Claude plugin: WordPress plugin, theme, block, Core and add-on lifecycle.

**Structure:** `skills/fswpdevops*` (router + 13 role skills), `agents/fswpdevops-code-reviewer.md`, `docs/`, `prompts/`, `HANDOFF.md` (older handoff notes).

## Commands
- Detect project: `python skills/fswpdevops-architect/scripts/detect_wp_project.py <dir>`
- QA gate: `bash skills/fswpdevops-qa/scripts/run_gate.sh <plugin-dir> [min-php, default 7.4] [--fix]`
- Single checks: `python skills/fswpdevops-qa/scripts/qa_check.py <plugin-dir> [--json]`, `python skills/fswpdevops-qa/scripts/theme_check.py`
- Scaffold: `skills/fswpdevops-plugin/scripts/scaffold_plugin.py`, `skills/fswpdevops-theme/scripts/scaffold_theme.py`
- Validate: `claude plugin validate . --strict`
- Evals (real model calls): `claude plugin eval . --trust-plugin --ablation none --scaffold --allow-tools Read Glob Grep Skill -j 4 --no-publish`. Rebuild cases with `python A:\Automation\plugin-evals\regen_evals.py <plugin> <router> <fixture ids>`. Write results outside the repo (`D:\SyncWin\AI Outputs\<plugin>\eval-results`); the packager includes repo files.
- No `evals/` folder yet; use validate until cases exist.

## Workflow
1. Read the skill or script you change, plus its neighbours.
2. Make the smallest change; run the closest check, then the full gate.
3. Update `CHANGELOG.md` for behavior changes; log ideas in `IMPROVEMENTS.md`.

## Rules
- Run the closest check and the full gate before committing. Never delete or weaken tests or evals. Report failed, skipped or timed-out runs honestly; NOT RUN is never a pass.
- Follow neighbouring files. Keep each `SKILL.md` under 500 lines; move detail into `references/`.
- On release, bump `version` in `.claude-plugin/plugin.json` and every skill's `metadata.version` together; add a `CHANGELOG.md` entry per behavior change.
- No commits, pushes or PRs unless asked. Work on a branch and open a PR; never push to main.
- No new dependencies without asking (scripts stay on the Python standard library).
- Never commit secrets. Never pick names or slugs without user confirmation.
- Say "WP", not "WordPress", in plugin and skill names (trademark policy, `docs/trademarks.md`). Foundational rules live once in `skills/fswpdevops/references/`.

## Model routing
Opus plans, decides, writes self-contained briefs with a report word limit, and reviews every result. Haiku for search, reading and mechanical edits. Sonnet for coding, tests and multi-step work. Do 1-2 tool calls inline.

## Docs
README.md, CONTRIBUTING.md, CHANGELOG.md, HANDOFF.md, docs/; ideas and feedback in `IMPROVEMENTS.md`.
