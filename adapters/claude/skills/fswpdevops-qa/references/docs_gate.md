# Recipe: documentation gate (plugins and themes)

Do these checks with Read, Glob, Grep and Bash (`git`) on a project folder `<dir>`. They enforce the documentation standard in `fswpdevops/references/coding-standards.md` ("Documentation standard"). Each check is PASS, FAIL or NOT RUN; NOT RUN (no git, no base branch) is never a pass. The gate FAILs when any check FAILs.

## Inputs
- `<dir>`: the project folder (not a folder: stop with "Not a folder").
- `base` (optional): the ref to diff against. Default: the first of `origin/main`, `origin/master`, `main`, `master` that exists and has a merge-base with `HEAD`.
- `static` (optional): skip the diff checks and report NOT RUN ("--static").

Definitions used below:
- Semver pattern: `X.Y.Z` with optional `-prerelease` and `+build`.
- Categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`. Statuses: `planned`, `beta`, `stable`, `deprecated`.
- Feature file sections, in this order: `Context`, `Behaviour`, `How it works`, `UI`, `Limits & known issues`, `History`.
- The `[Unreleased]` section is the text under `## [Unreleased]` up to the next `## [` heading. Its body lines are the non-empty lines that do not start with `#`.

## Static checks
1. **Required files**: `README.md`, `docs/setup.md`, `docs/architecture.md`, `docs/ops.md`. One row each, "exists: <path>", FAIL when missing.
2. **CHANGELOG.md format (Keep a Changelog 1.1.0)**: missing file is FAIL ("CHANGELOG.md missing"). Otherwise FAIL (first 3 problems) for any of: no `## [Unreleased]` section; a `## ` heading other than `[Unreleased]...` that is not `## [X.Y.Z] - YYYY-MM-DD` (optionally followed by ` [YANKED]`); a `### ` heading that is not one of the categories.
3. **docs/features/README.md index current**: missing is FAIL. Otherwise parse the table rows (lines starting with `|` that have exactly four cells, whose first cell is not `Feature` and not just dashes, colons and spaces). The fourth cell must contain a `<name>.md` link target; a row without one is a problem ("row '<x>' has no file"). Record status and since from cells 2 and 3. Problems (first 4 shown): a feature file in `docs/features/` (any `*.md` except `README.md`) missing from the index ("<f> not in index"); an indexed file that does not exist ("index lists missing file <f>"); the header row is not `| Feature | Status | Since | File |` (compared case-insensitively with whitespace collapsed); any non-ASCII character in the index.
4. **docs/features/*.md valid (N file(s))**: for every feature file (first 4 problems shown): no non-ASCII text; a status line exactly of the form `**Status:** <status> | **Since:** <semver> | **Updated:** <semver>` with a status from the list ("bad Status line"); every section heading present as a line `## <Section>`; when the status line is valid: the index status and since equal the file's, the `Updated` version appears in the text after `## History` ("Updated X has no History line"), and a feature that is not `planned` has no `FILL IN:` left.

## Diff checks (skipped with `static`)
5. Not a git repository: NOT RUN "diff checks" ("not a git repository"). No base found: NOT RUN "diff checks" ("no base branch found; pass a base ref"). Otherwise let `mb` be the merge-base of the base ref and `HEAD`.
6. **Changed files**: `git diff --name-only --relative <mb>` plus `git ls-files --others --exclude-standard` (untracked), with `/` separators. **Code files** among them:
   - skip anything with a parent folder named `vendor`, `node_modules`, `tests`, `test`, `languages`, `build`, `dist`, `foundation`, `docs` or `.git`, and `*.min.js`;
   - `.php` is code; `.js`, `.jsx`, `.ts`, `.tsx` count only when a parent folder is `src` or `blocks`; `theme.json` is code; `.html` counts only under `templates/` or `parts/`.
   - No code files: PASS "code changed vs <base>" ("no code changes: no changelog or feature entry needed") and stop.
7. **CHANGELOG [Unreleased] updated**: compare the current `CHANGELOG.md` to `git show <mb>:./CHANGELOG.md`.
   - No `[Unreleased]` section now: FAIL ("N code file(s) changed; no [Unreleased] section").
   - A new released version heading exists and the old `[Unreleased]` had body lines: PASS ("release: Unreleased moved into a version").
   - The current `[Unreleased]` has body lines the old one lacked: PASS ("new entry present").
   - Otherwise FAIL ("N code file(s) changed (e.g. <first>); no new line under [Unreleased]").
8. **Feature docs for touched features**: the feature slug of a code file is the first folder after the first `includes`, `inc`, `src`, `modules`, `features` or `blocks` folder in its path, lower-cased with `_` turned into `-`, and only when at least two path parts follow that folder (a file directly in it has no slug). Ignore generic slugs: `core`, `shared`, `common`, `utils`, `util`, `l10n`, `generated`, `data`, `domain`, `presentation`, `ui`, `widgets`, `theme`, `models`, `services`, `helpers`, `lib`, `assets`, `admin`, `public`.
   - A waiver applies when slugs exist and `[Unreleased]` gained a line under `### Changed`, or a line containing `docs: none` (any case): PASS ("waived: [Unreleased] has a '### Changed' or 'docs: none' line (refactor, no feature-doc change)") and the index check below is skipped.
   - No slugs: PASS ("no feature-scoped code touched (shared code needs the changelog only)").
   - Otherwise, for each slug `docs/features/<slug>.md`: missing is a problem ("missing: <path> (for <code file>)"); present but not in the changed files is stale ("unchanged: ..."); present, changed and absent from `<mb>` is newly created. Any missing or stale: FAIL with both lists; otherwise PASS ("N feature file(s) updated").
9. **docs/features index updated**: when feature files were newly created and `docs/features/README.md` is not among the changed files: FAIL ("new feature file(s) ...; index unchanged").

## Output
A table `Check | Result | Detail`, one row per check. Overall FAIL if any row is FAIL. The `run_gate` recipe reports this gate as one row: FAIL with up to 3 FAIL or NOT RUN details, NOT RUN "static checks passed; ..." when only the diff checks were NOT RUN, otherwise PASS.
