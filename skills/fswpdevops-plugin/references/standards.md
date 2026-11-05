# Standards: versioning, tech stack, code quality, documentation

Contents: 1. Versioning and changelog discipline (points to the Documentation standard); 2. Technology stack; 3. Required project information; 4. Feature documentation; 5. Code quality; 6. Quality bar (applies to everything built or written — code, docs, PRDs, changelogs, readme, admin copy); 7. Minimal-code discipline.

House-wide rules that apply to every plugin build, update, and iteration — not just first builds. `fswpdevops-architect` collects the inputs these rules need; `fswpdevops-plugin` applies them; `fswpdevops-qa` checks them.

## 1. Versioning and changelog discipline

- **Standard:** versioning, `CHANGELOG.md` and per-feature docs follow `fswpdevops/references/coding-standards.md` ("Documentation standard"). This file adds only the plugin-specific mechanics below.
- **Every plugin and every skill starts at `0.0.1`**, not `1.0.0`. The `0.y.z` range is itself the beta/pre-release designation (semver.org: "major version zero is for initial development"); MAJOR moves to `1` only when the owner says the plugin/skill is stable and its public interface (settings, data shape, hooks, shortcode API) won't break casually. This applies to a freshly scaffolded plugin's own header `Version`, its `DB_VERSION`/version constant, and `readme.txt` Stable tag alike - never default any of them to `1.0.0`.
- **Default action on any change: add a line under `## [Unreleased]`** in `CHANGELOG.md`; small fixes and tweaks accumulate there until a release.
- **Bump the version only at a release**, by normal semver practice (PATCH fixes, MINOR backward-compatible features, MAJOR breaking). A release moves `[Unreleased]` into `## [X.Y.Z] - date` and increments `Version` in the plugin header, the `{PREFIX}_VERSION`-style constant, and `Stable tag` in `readme.txt` together (checked by `fswpdevops-qa`'s version-consistency check).
- **Changelog entries stay concise, unique, non-duplicative.** One line per real change, in the user's terms. Before adding a line, check whether `[Unreleased]` already describes the change.

## 2. Technology stack

- **The stack the user chose (or that was already decided for this project) is not replaced by default.** Once set, it is the standing decision for that project — don't re-propose a different stack on a later iteration just because it's not what a fresh build would default to.
- **Override it only for a clear, stated reason**: it conflicts with an industry standard or established WordPress/PHP practice, a real technical constraint (hosting limits, PHP version ceiling, a library that doesn't exist for the chosen stack), or the actual requirement changed. State the reason plainly when proposing an override; never swap silently.
- **New project, or the existing stack looks wrong for what's being asked:** decide the stack before writing any code. This follows `fswpdevops-architect`'s PRD process — the admin-UI tier (native / `@wordpress/components` / Tier 3) and JS tier (vanilla / Alpine) decisions in PRD sections 7–8 *are* this decision for a WordPress plugin; there is no separate stack question to ask beyond what the PRD already asks and confirms at approval.
- **Per-project, not global.** A stack decision made for one plugin is not a default for the next one — `fswpdevops-architect` runs its questions fresh each time, even for the same client.

## 3. Required project information

Collect this before generating any plugin metadata; **never invent a missing value** — omit the corresponding header/field/link rather than fill it with a placeholder (this is the same rule that already governs `--plugin-uri`/`--author-uri` in the scaffold script).

| Item | Where it's used |
|---|---|
| Company name | Plugin header `Author`, `readme.txt`, about screen |
| Product/plugin name | `Plugin Name` header, `readme.txt` title, about screen |
| Company/product acronym | Prefix for code identifiers (`fswpdevops-architect`'s prefix rule) — internal only, never user-visible text |
| Author name | `Author` header, `readme.txt` |
| Contributors (if any) | `readme.txt` `Contributors:` field |
| Company/product links (website, docs, support, repo, product page) | `Plugin URI`, `Author URI`, `readme.txt` header block, about screen "Links" section |

Ask for whatever isn't already stated as part of `fswpdevops-architect`'s essential-questions round (Step 1); don't add a second round just for this — fold it into the same pass. If a link or contributor genuinely doesn't exist yet, leave that field out of the generated files rather than asking again later.

## 4. Feature documentation

Defined once in `fswpdevops/references/coding-standards.md` ("Documentation standard"): `docs/features/<feature-slug>.md` per feature using the feature-file template, `docs/features/README.md` index table, updated in the same change as the code. The doc alone must be enough to restore the intended behaviour if the feature is broken, removed, or changed by accident.

- A single-feature plugin still has one feature file plus the index.
- Structured data (settings/options schema, REST route table, data-model fields) goes in a table or fenced ` ```json ` block inside the same feature file, under "How it works"; never a second parallel file.
- Fluff-free, self-contained, no duplication across files (cross-reference instead).

## 5. Code quality

Write every plugin the way an experienced enterprise WordPress team would:

- **Secure, efficient, maintainable, modular.** Security baseline (`fswpdevops-security`) is never optional or scaled down (already the rule); efficiency means no unbounded queries or redundant work, not micro-optimization.
- **DRY, without inventing abstractions the plugin doesn't need.** A shared helper used twice is worth extracting; an interface or factory for one implementation is not.
- **Prefer less code for the same result**, as long as it doesn't cost clarity, security, maintainability, or a required behavior. Don't golf it at the expense of readability.
- **No overengineering.** Build what the PRD asks for at the simplest structure that holds up — no speculative extension points, no config for values that will never change, no premature generalization across features that aren't actually related yet.
- **Comments explain the non-obvious** — why a workaround exists, a non-default choice, a constraint that isn't visible in the code itself (a WordPress core quirk, a rate limit, a security reason for an odd-looking check). Never comment what the code already says plainly (`// increment counter` above `$count++;`).
- **Preserve existing required functionality when iterating.** Improving an implementation is welcome; dropping a behavior the PRD or a prior iteration established is not, unless the user explicitly agreed to remove it.
- **Minimize dependencies.** Every new dependency is justified against what's already available (WordPress core, an already-included library) before adding another one — same discipline as the Tier 3 library table's "check this table before adding a new dependency" rule.

## 6. Quality bar (applies to everything built or written — code, docs, PRDs, changelogs, readme, admin copy)

Every artifact this plugin produces is judged against the same ten traits, in this order of precedence when two pull in different directions:

1. **Essential** — say what's needed, nothing added because it seemed nice to have. A PRD section, a code comment, or a doc heading with nothing real to say is cut, not padded.
2. **Minimalistic** — the smallest structure that fully carries the content. Fewer files, fewer abstractions, fewer words, same information.
3. **Efficient** — least work for the same correct result: least code, least tokens, least re-reading required, least redundant tool calls.
4. **Organized** — one clear place for each piece of information (the reference tables and precedence rules already enforce this at the skill level); a reader finds a fact without searching twice.
5. **Factual** — every claim traces to something stated, verified, or directly observed in the code/PRD. Nothing invented (the standing rule in section 3 is this trait applied to project metadata specifically).
6. **Trustworthy** — nothing hidden or glossed over: FAIL is reported as FAIL, an assumption is labeled an assumption, a stricter house rule is labeled as such (precedence.md), a limitation is stated plainly rather than talked around.
7. **Authoritative** — grounded in the actual standard (WPCS, the Plugin Handbook, WCAG, OWASP), cited by name where it matters, not a personal guess dressed as a rule.
8. **Expert** — reflects real WordPress/PHP practice, not generic advice that would apply to any language or platform.
9. **Experience (user's)** — every choice is judged by whether it makes the plugin easier to install, configure, use, and maintain for the person who ends up with it — not by what's easiest to write.
10. **Easiest** — of the remaining valid options, the one that asks the least of the reader or user wins, provided it doesn't cost any of the traits above it.

**Applied concretely:**
- PRDs, docs, and changelog entries: short declarative sentences, no filler phrasing, no restating a heading's own name as its first sentence.
- Code: `references/standards.md` section 5 already sets the code-quality bar (DRY without overengineering, comments only for the non-obvious) — this section doesn't repeat it, it's the same rule.
- Every `fswpdevops-qa` finding: state the fact (what failed, where), not a hedge around it.
- This plugin's own skill files follow the same bar — a section here that could be cut without losing an instruction gets cut, not kept for length.

## 7. Minimal-code discipline

This sequences the work; it does not lower the quality bar in section 5. Before writing something new, stop at the first question that resolves it:

1. Does the approved PRD ask for it? If not, do not build it.
2. Does this project already have a helper, class, or pattern for it? Reuse it.
3. Does WordPress core or the PHP standard library already do it? Use that.
4. Does a dependency that is already installed (section 2, `modern-app-stack.md`) cover it? Use it rather than adding another.
5. Only then write the smallest code that meets the PRD.

**Fix causes, not call sites.** A bug report names one failing path. Before patching it, find every caller of the function involved and repair the shared code once. A single guard in the shared function is a smaller change than one per caller, and patching only the reported path leaves sibling callers broken.

**Label knowing shortcuts.** When you deliberately take a shortcut (a quadratic loop over a small list, one global lock, a heuristic in place of the exact check), put `// shortcut: <the limit>; revisit when <trigger>` at that spot. Unlabeled shortcuts become permanent by accident. This is the one case where a comment may state something the code already shows.

**Abstractions must earn their place.** No interface with one implementation, no factory that makes one thing, no option for a value that never changes. Fewest files that do the job. Plain and explicit beats clever, because the next reader lacks this session's context.

**Effort levels.** Default: apply the questions above. If the user asks for a "quick draft", build what was asked and name any simpler alternative in one line. If they ask for the "leanest possible", challenge speculative PRD lines before building them, but never trim something the PRD states plainly. Security, validation, and error handling do not scale down at any level.

**Trimming existing code** is `fswpdevops-reviewer`'s lean lens (read-only findings), not a build-time activity.
