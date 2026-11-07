# Changelog

## [Unreleased]

### Added
- GitHub Actions workflow `release-plugin.yml` builds `fswpdevops.plugin` and attaches it to each release for a one-click download link (README).

## [0.7.0] - 2026-11-07

### Added
- `fswpdevops-designer`: WordPress design language (theme.json tokens, block patterns, native-first, states, respects a site's existing design language); `references/design-language.md`.
- `fswpdevops-critic`: read-only design and UX critique stage (heuristics, hierarchy, consistency, block editor UX, states, a11y, copy) with severity, evidence, fix, confidence >= 80 and a one-line verdict; runs after the build and before the reviewer; `references/ux-rubric.md`.
- `evals/evals.json` with trigger evals for both skills.

## [0.6.1] - 2026-11-06

### Changed
- Standing rule: research before building. Check current official docs and widely recommended, secure practice before choosing an approach, file, tool, config or dependency; cite the source; mark anything unverified; never guess; keep research scoped to the task.

## [0.6.0] - 2026-11-06

### Added
- Lean ladder (adapted from Ponytail, MIT) merged into `lean-coding.md`: read and list touch points, six rungs with WordPress rungs (core APIs before custom code, existing plugin hooks before new ones), never-cut list. The lean lens gains a debt mode for shortcut notes. Wired into architect, plugin, theme, block, maintainer and reviewer.

### Changed
- Shortcut marker format is now `// shortcut: <limit>, upgrade when <trigger>`.

## [0.5.4] - 2026-11-06

### Added
- Architect asks "React admin SPA vs native/BEM?" in the question round; reviewer quality lens, security and qa skills point to the matching sections (a11y, security, licensing, tests) of `fswpdevops-plugin/references/modern-app-stack.md`, which already holds the full methodology (no duplicate reference file).

## [0.5.3] - 2026-11-05

### Added
- Documentation standard for every plugin, theme and add-on the plugin builds (single source: coding-standards.md): README.md and docs/ (setup, architecture, ops), CHANGELOG.md (Keep a Changelog 1.1.0, SemVer 2.0.0, starts at 0.0.1, [Unreleased] on top, pre-1.0 = beta), and docs/features/ with an index table and a lean feature-file template (status, context, behaviour, how it works, UI, limits, history).
- fswpdevops-qa/scripts/docs_gate.py (stdlib): FAILS when plugin or theme code changed without a CHANGELOG [Unreleased] line, without a changed feature file for the touched feature, or with a stale docs/features index; also checks changelog format and the feature-file template. A row of run_gate.sh; NOT RUN without git.
- docs_gate.py: a new [Unreleased] `### Changed` line or a `docs: none` line waives the feature-file part for refactors (the changelog line is still required).
- run_gate.sh picks a working Python (python3, python, py -3).
- Plugin and theme scaffolds write the standard files (README, CHANGELOG 0.0.1, docs, docs/features index and feature files).

### Changed
- Feature docs moved from docs/<feature>.md to docs/features/<feature>.md (migrate an existing project: `git mv docs/<feature>.md docs/features/`, then add the index and the template headings; until then qa_check.py only WARNs) (qa_check.py item 13, checklist, standards.md updated); planned features may keep FILL IN markers.
- Versions start at 0.0.1 (was 0.1.0): scaffold templates, readme Stable tag and theme header. Changelog discipline now means lines under [Unreleased] until a release.
- Reviewer quality lens, release checklist, release check, plugin and maintainer skills point to the standard.

### Fixed
- run_gate.sh detail column no longer garbled by carriage returns in script output.

## [0.5.2] - 2026-11-05

### Added
- Secure-by-default baseline in fswpdevops-security (threat model, secret scanning, least privilege, supply chain, signed releases, release gate); threat-model sections in the PRD and change brief; CI outline with lockfile installs, audits and pinned actions; Critical or Important security findings block release.

### Fixed
- QA toolchain downloads (phpcs, phpcbf, phpstan) were unpinned "latest" binaries run without verification; setup now records SHA-256 checksums and the gate fails closed (refuses to run) when a tool does not match.
- Review fixes: toolchain pinned in `skills/fswpdevops-qa/scripts/toolchain.lock` (release versions, official SHA-256 digests, git tags with commit SHAs) with no trust on first use; setup verifies before use; the gate now FAILS (non-zero, "re-run setup_toolchain.sh") when an installed phar has a missing or mismatched checksum instead of reporting NOT RUN; clones use `--branch <tag>` and a commit check; the old SHA256SUMS record() is removed.

## [0.5.1] - 2026-11-03
### Fixed
Cleared all 30 validator warnings: a "use" cue in six stage descriptions, a closing scratchpad line in every skill, contents lists in the long plugin and security references, and the foundational-rules line now lives only in the router.

## [0.5.0] - 2026-11-03
### Changed (breaking: plugin and skill names)
Renamed to **Full-Stack WP DevOps** (`fswpdevops`, trigger `/fswpdevops`), matching Full-Stack DevOps (`fsdevops`). Repository `syncwin/fswpdevops` (the old URL redirects); marketplace `syncwin-fswpdevops`. Every skill starts with the router name, so typing `fswpdevops` lists them all.

| 0.4.4 | 0.5.0 |
|---|---|
| `fswp-developer` (`/fswp`) | `fswpdevops` (`/fswpdevops`) |
| `fswp-architect` | `fswpdevops-architect` |
| `fswp-plugin-developer` | `fswpdevops-plugin` |
| `fswp-theme-developer` | `fswpdevops-theme` |
| `fswp-block-developer` | `fswpdevops-block` |
| `fswp-api-developer` | `fswpdevops-api` |
| `fswp-core-contributor` | `fswpdevops-core` |
| `fswp-maintainer` | `fswpdevops-maintainer` |
| `fswp-qa-engineer` | `fswpdevops-qa` |
| `fswp-reviewer` | `fswpdevops-reviewer` |
| `fswp-security-engineer` | `fswpdevops-security` |
| `fswp-performance-engineer` | `fswpdevops-performance` |
| `fswp-devops-engineer` | `fswpdevops-ci` |
| `fswp-release-manager` | `fswpdevops-release` |
| agent `fswp-code-reviewer` | agent `fswpdevops-code-reviewer` |

Unchanged on purpose (code identifiers in generated projects and tool paths): the `fswp-alpine-loader` script handle and the `~/.fswp-tools` / `FSWP_TOOLS` toolchain folder.
# Changelog — Full-Stack WP Developer

Each skill also keeps its own `CHANGELOG.md`. Semantic versioning: breaking = major, new capability = minor, wording = patch.

## [0.4.4] - 2026-11-03
### Changed
- Metadata to the AI Extender standard: author company, plugin metadata block, release stage, listing links, and display name, version, author, company and license on every skill and agent. No behaviour change.

## 0.4.3 — 2026-11-02

- Scaffolded docs stubs use a `FILL IN:` marker instead of TODO; `qa_check.py` still fails on any unfilled stub.
- Skill versions follow the plugin version.

## 0.4.2 (2026-11-02)

- Plugin icon (`assets/icon.png`, `assets/icon.svg`).

## 0.4.1 — 2026-11-02

- Published at `syncwin/fswp-developer` with the marketplace `syncwin-fswp-developer`; README install steps for the app and Claude Code.

## 0.4.0 — 2026-09-28

Author: @wasimness (SyncWin). Contact: support@syncwin.com.

**Breaking: router skill and plugin slug are now the same name.** Both are `fswp-developer`. There is one `fswp-developer` in the package: the plugin manifest name and the router skill folder/frontmatter name are identical, not just prefix-matched.

**Breaking: single trigger.** `/fswp` is now the only defined trigger. The phrase-based triggers `FSWP + [project]`, `SWWP + [project]`, and `WPE + [project]` are retired; a plain-language WordPress request still works, as it always has.

**Breaking: skill merge.** `fswp-lean-engineer` and `fswp-standards-engineer` are no longer separate skills. Both were foundational, always-on writing disciplines rather than domains with their own workflow, so they are now base-layer references owned by the router: `fswp-developer/references/lean-coding.md` (plus `wordpress-shortcuts.md`) and `fswp-developer/references/coding-standards.md` (plus `i18n.md`, `accessibility.md`). Every build and maintenance skill now points to these references instead of naming a skill. `fswp-security-engineer` stays a separate skill: it carries real house depth (`references/security.md`) and is loaded independently by `fswp-reviewer`, which is a meaningful reason to keep it apart from the router.

**Changed**
- The Atomic Framework's code-level tokens now use its own acronym, `afw-`/`AFW`, instead of the spelled-out `atomic-`/`Atomic`: asset file names (`afw-tokens.css`, `afw-components.css`, `afw-foundation-logics.js`), CSS classes (`.afw-tabs`, `.afw-scope`), the JS namespace (`window.AFW.Utils`), the Alpine component name (`afwTabs`), and the version constant (`{{PREFIX}}_AFW_VERSION`). The human-readable name "Atomic Framework" is unchanged in prose.

**Added**
- `fswp-developer/references/brand-naming.md`: there is no built-in brand acronym. For new plugin and new theme work, `fswp-architect` asks the project owner for a short code-level prefix/acronym in the same question round as the rest of planning (proposing candidates derived from the project's own name if they have none); Update and Add-on work keeps the existing project's prefix and is never asked. The reference documents the exceptions (theme's 4-letter prefix minimum, product slug vs. code prefix, reserved `wp`/`WordPress` names, dependency-mandated names).
- The shared cross-plugin Alpine.js loader handle used by `fswp-plugin-developer` is now `fswp-alpine-loader`: a fixed, tool-owned constant (not tied to any one project's brand) so multiple plugins scaffolded by this tool can share one Alpine instance on the same site.
- "SWWP design system" — a name tied to retired branding — is renamed to its real name, the **Atomic Framework**, everywhere it's mentioned. Class prefix example: `.afw-*`; shared JS utility namespace: `window.AFW.Utils`.

**Changed**
- Plugin display name is "Full-Stack WP Developer" (no publisher suffix); SyncWin is represented in `plugin.json` `author`/`homepage` and `marketplace.json` `owner` instead of in the visible name.
- Author identity changed from "Wasim Akram" to `@wasimness` everywhere an author is credited: both manifests, every skill's `metadata.author`, `LICENSE`, `CREDITS.md`, `SECURITY.md`, `CONTRIBUTING.md`, `README.md`, `CHANGELOG.md`, `HANDOFF.md`. The company field (`SyncWin`) is unchanged.
- Example prefix in `fswp-plugin-developer`'s scaffold help text and architecture reference changed from a fixed brand token to a generic placeholder (`acme`), matching the ask-first prefix rule above.
- Install commands and every internal cross-reference updated for the plugin-slug/router-name unification.

Name mapping (0.3.0 → 0.4.0):

| 0.3.0 | 0.4.0 |
|---|---|
| Plugin slug `full-stack-wp-developer` | `fswp-developer` |
| Router skill `fswp-developer` | `fswp-developer` (now identical to the plugin slug) |
| `fswp-lean-engineer` | `fswp-developer/references/lean-coding.md` |
| `fswp-standards-engineer` | `fswp-developer/references/coding-standards.md` |
| Triggers `FSWP +` / `SWWP +` / `WPE +` | `/fswp` |
| "SWWP design system" | "Atomic Framework" |

## 0.3.0 — 2026-09-28

Author: @wasimness (SyncWin). Contact: support@syncwin.com.

**Breaking: skill renaming.** Every skill name now starts with `fswp-` to avoid colliding with other skills, and names a role rather than an activity (`fswp-plugin-developer`, not `fswp-plugin-development`).

Name mapping (0.2.0 → 0.3.0):

| 0.2.0 | 0.3.0 |
|---|---|
| `fswp-developer` (router) | `fswp-developer` |
| `wp-plan` | `fswp-architect` |
| `wp-build-plugin` | `fswp-plugin-developer` |
| `wp-build-theme` | `fswp-theme-developer` |
| `wp-extend` | `fswp-maintainer` |
| `wp-core-contribute` | `fswp-core-contributor` |
| `wp-verify` | `fswp-qa-engineer` |
| `wp-review` | `fswp-reviewer` |
| `wp-security` | `fswp-security-engineer` |
| `wp-rest-api` | `fswp-api-developer` |
| `wp-block-development` | `fswp-block-developer` |
| `wp-performance` | `fswp-performance-engineer` |
| `wp-dev-tooling` | `fswp-devops-engineer` |
| `wp-directory-guidelines` | `fswp-release-manager` |
| `wp-reviewer` (agent) | `fswp-code-reviewer` |
| — | `fswp-developer/references/lean-coding.md` (new) |
| — | `fswp-developer/references/coding-standards.md` (new) |

The plugin slug (`fswp-developer`) and triggers (`FSWP +`, `SWWP +`, `WPE +`) are unchanged; only skill names moved.

**Added**
- `fswp-developer/references/lean-coding.md`: the write-less discipline (Ponytail-learned principles, credited not copied) as its own always-on role skill with a decision ladder, effort levels, shortcut-marker convention, and agent-scope guidance, plus `references/wordpress-shortcuts.md` (core/PHP substitutes for common custom code).
- `fswp-developer/references/coding-standards.md`: PHP/JS/CSS/HTML coding standards, PHPDoc, i18n, and accessibility as one always-on role skill, with `references/i18n.md` and `references/accessibility.md`. The PHP standards table is verified against the official coding-standards page.
- `fswp-api-developer/references/abilities.md`: register, audit, and verify procedures for the Abilities API.
- `fswp-block-developer/references/block-json.md` (full property table, verified against the Block Editor Handbook), `patterns-variations.md`, `interactivity.md`.
- `fswp-devops-engineer/references/blueprints-and-cli.md`: Playground Blueprint steps and the WP-CLI command table.
- `fswp-release-manager`: rebuilt as the release role with `references/plugin-guidelines.md` (all 18 guidelines), `references/theme-requirements.md` (all 14 requirement areas), and `references/headers-and-readme.md`, all checked against the official pages on 2026-09-28.
- `fswp-qa-engineer/scripts/theme_check.py` rewritten against the verified Theme Directory requirements, with a `--directory` strict mode; `qa_check.py` gained plugin header and readme.txt rule checks (description length, unique Plugin URI, tag count, `Stable tag: trunk` ban, numeric `Tested up to`) and a scope check against the approved plan.
- `fswp-reviewer`: an API risk map and an AI-generated-code risk section in the security lens; comment-accuracy, test-gap, and class/type-design checks in the quality lens.
- `fswp-developer/references/official-docs.md` now marks which pages were actually fetched and used ("(checked)") versus canonical paths not yet re-verified.

**Changed**
- `fswp-theme-developer/scripts/scaffold_theme.py`: named, prefixed callback functions instead of anonymous ones (matches the coding standard and the directory's prefixing rule), a `--tested-up-to` flag that is only set after a real test, warnings when the name contains "WordPress"/"Theme"/"Twenty*" or the slug has fewer than four letters, and `wp_link_pages()` added to the classic content template.
- `fswp-plugin-developer/references/rest-cron.md`: the cron-schedule example now registers a named function instead of a closure, since closures cannot be removed with `remove_action`/`remove_filter`.
- Every build and maintenance skill (`fswp-plugin-developer`, `fswp-theme-developer`, `fswp-maintainer`, `fswp-core-contributor`, `fswp-block-developer`, `fswp-api-developer`) now states up front that `fswp-developer/references/lean-coding.md`, `fswp-developer/references/coding-standards.md`, and `fswp-security-engineer` are always on.

## 0.2.0 — 2026-09-28

**Breaking: renamed and rescoped.** The plugin is "Full-Stack WP Developer" (slug `fswp-developer`) and covers themes, plugins, updates, add-ons, and Core patches.

Name mapping (0.1.x → 0.2.0):

| 0.1.x | 0.2.0 |
|---|---|
| `wordpress-plugin-engineer` | `fswp-developer` (router) |
| `wordpress-plugin-plan` | `wp-plan` |
| `wordpress-plugin-build` | `wp-build-plugin` |
| `wordpress-plugin-verify` | `wp-verify` |
| `wordpress-plugin-review` | `wp-review` |
| `wordpress-plugin-reviewer` (agent) | `wp-reviewer` |
| 18 forked `wordpress-*` skills | Removed; replaced by independent skills |

Trigger: `/fswp` (single trigger; earlier `FSWP +`/`SWWP +`/`WPE +` phrase-based triggers are retired).

**Added:** `wp-build-theme`, `wp-extend`, `wp-core-contribute`; domain skills `wp-security`, `wp-rest-api`, `wp-block-development`, `wp-performance`, `wp-dev-tooling`, `wp-directory-guidelines`; `wp-plan/scripts/detect_wp_project.py`; `wp-verify/scripts/theme_check.py`; `official-docs.md`; GitHub foundation only (`.github/`, `github-foundation.md`, `docs/github-integration.md`); contact `support@syncwin.com`.

**Changed:** licensing simplified to a single MIT license; all 18 forked GPL skills removed; review lenses and the minimal-code section rewritten from scratch in our own words, ideas credited in `CREDITS.md`.

**Removed:** `scripts/sync-native-skills.sh`, `NATIVE_VERSIONS.md`, `provenance.md`, `THIRD_PARTY_NOTICES.md`, vendored third-party `LICENSE`/`NOTICE` files.

## 0.1.0 — Unreleased (previous name: WordPress Plugin Engineer)

Initial plan / build / verify / review pipeline for plugins with 18 forked WordPress-native skills.
