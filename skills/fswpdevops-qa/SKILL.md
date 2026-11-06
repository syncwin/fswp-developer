---
name: fswpdevops-qa
description: Verification stage of Full-Stack WP DevOps. Runs the mechanical gate for plugins and themes (house-rule scripts, PHP lint, PHPCS with WordPress standards, PHP compatibility, PHPStan with WordPress stubs), the manual checklist, PRD or change-brief scenario tests, and the pre-release check. Reports PASS, FAIL, or NOT RUN and never implies a skipped check passed. Invoked by fswpdevops after a build and again before delivery; use directly to audit any plugin or theme folder.
license: MIT
metadata:
  displayName: "FSWPDevOps QA Engineer"
  version: "0.6.1"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps QA Engineer

Verify the built folder, do not fix during gating. Report first, then fix in the router's fix loop.

## 1. Mechanical gate

```
bash scripts/setup_toolchain.sh              # once per environment (apt + GitHub only, no Composer) — versions, SHA-256 and commit SHAs are pinned in scripts/toolchain.lock; the gate FAILS (not NOT RUN) when an installed phar mismatches, re-run setup_toolchain.sh
bash scripts/run_gate.sh <dir> [min-php] [--fix]
```

`run_gate.sh` detects a theme (a `style.css` with a Theme Name header) and runs `scripts/theme_check.py`; otherwise it runs `scripts/qa_check.py`. Both use Python's standard library only and always work. Then it adds, where PHP and the tools exist: `php -l`, PHPCS `WordPress-Extra` (errors fail, warnings are listed), PHP compatibility for the minimum PHP, and PHPStan level 5 with WordPress stubs.

- `docs_gate.py <dir> [--base REF] [--static]` (standard library only; `run_gate.sh` runs it as a row): the documentation standard in `fswpdevops/references/coding-standards.md`. FAILS when `README.md` or `docs/{setup,architecture,ops}.md` is missing, `CHANGELOG.md` is not Keep a Changelog 1.1.0 (needs `## [Unreleased]`, six categories only), the `docs/features/` index and files disagree or break the template, or plugin/theme code changed against the base (default `origin/main`, then `main`) without a new `[Unreleased]` line or without a changed `docs/features/<slug>.md` for the touched feature (a new `### Changed` or `docs: none` line under `[Unreleased]` waives the feature-file part for refactors). No git or no base: the diff checks are NOT RUN (never a pass).
- `--fix` runs `phpcbf` (WordPress standard) first. Use it after scaffolding and after large edits; review the diff.
- **Plugin Check** needs a WordPress install and the command line (`wp plugin check <slug>`); it is NOT RUN elsewhere. Tell the user to run it before a WordPress.org plugin submission. For themes, the equivalent is the Theme Check plugin or the directory's automated review.
- `theme_check.py <dir> [--directory]`: without the flag, real defects FAIL and directory-only rules WARN; with `--directory`, the WordPress.org Theme Directory requirements FAIL (missing headers, screenshot size and ratio, disallowed files, plugin-territory code, required classic-theme calls).
- `qa_check.py` also checks plugin header and readme rules from the handbook (description length, unique Plugin URI, at most 5 tags, no `Stable tag: trunk`, numeric `Tested up to`, short-description length) as warnings.
- `qa_check.py` enforces, for plugins: ABSPATH guards, version match (header, constant, readme Stable tag), no example.com or CDN or hosted fonts, `permission_callback` on every route with commented `__return_true`, DB upgrade check, enqueue inside callbacks, banned functions, uninstall guard, rem-only units, JS translations, source shipped with compiled output, font licenses. `theme_check.py` checks the header, license, entry templates, `theme.json` validity, banned functions, unescaped-echo heuristic, remote assets, text domain, screenshot and readme.

**Reporting rule:** every check is PASS, FAIL, or NOT RUN, with the tool versions used. NOT RUN is never a pass and never summarized as "clean". If PHP or a tool is missing, say so and name the command that would run it.

## 1a. Scope check

Compare the diff or file list with the approved brief. Files, hooks, options, or dependencies the plan did not ask for are reported as scope creep (see `fswpdevops/references/lean-coding.md`). Count lines added versus removed and comment on disproportion.

## 2. Manual checklist

`references/checklist.md`: only the items a script cannot judge. Run it after the mechanical gate is green.

Tier 3 React admin SPA: also confirm the axe-core CI run, the manual accessibility pass, written gating test scenarios and the dependency license rule from `fswpdevops-plugin/references/modern-app-stack.md` (sections 9, 10, licensing note).

## 3. Scenario tests

Every numbered scenario in the PRD (`fswpdevops-architect`) gets PASS, FAIL, or NOT RUN with evidence. Always include:

- Fresh install with no prior options or tables: no notices or fatals.
- Deactivate then reactivate: no duplicate schedules or options.
- **Upgrade from a previous version's stored data without reactivating**: schema and options migrate on load.
- Uninstall: only plugin-owned data removed.
- Migration mode: export diffs and visual-regression gate against `baseline/` (`fswpdevops-architect`).

**By work type, add:**

- **Theme:** every template type the PRD lists renders with real content and with empty content; editor and front end match; keyboard-only navigation works; theme switch away and back leaves no fatal.
- **Update:** every item in the change brief's parity list re-checked and marked; upgrade from the previous version's stored data works; nothing outside the brief changed (diff read).
- **Add-on:** host active and in range (works); host inactive (add-on stays quiet, shows a notice, no fatal); host below the supported version (refuses cleanly).
- **Core patch:** the ticket's reproduction fails before and passes after; the relevant PHPUnit group passes; PHPCS clean on changed lines; see `fswpdevops-core`.

Where PHP can run, exercise activation and migration logic with a small PHP script; otherwise trace by reading and label it "traced, not run".

## 4. Release check

After everything above is green: `references/release-check.md`.

## Output

One table: check | PASS/FAIL/NOT RUN | detail. Then FAIL list with file and line, then what the user must run themselves. For multi-session builds, copy the table into `HANDOFF.md`.

Finish with a scratchpad: the gate table, scope findings, skipped checks and why.
