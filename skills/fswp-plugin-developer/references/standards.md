# Standards: versioning, tech stack, code quality, documentation

House-wide rules that apply to every plugin build, update, and iteration — not just first builds. `fswp-architect` collects the inputs these rules need; `fswp-plugin-developer` applies them; `fswp-qa-engineer` checks them.

## 1. Versioning and changelog discipline

- **Every plugin and every skill starts at `0.1.0`**, not `1.0.0`. The `0.y.z` range is itself the beta/pre-release designation (semver.org: "major version zero is for initial development"); MAJOR moves to `1` only on a deliberate, stated decision that the plugin/skill is stable and its public interface (settings, data shape, hooks, shortcode API) won't break casually. This applies to a freshly scaffolded plugin's own header `Version`, its `DB_VERSION`/version constant, and `readme.txt` Stable tag alike — never default any of them to `1.0.0`.
- **Default action on any change: add to the latest existing changelog entry**, not a new one. Small fixes, minor improvements, and tweaks accumulate under the current unreleased/latest entry.
- **Bump the version only when the change justifies a new release** by normal semver practice:
  - PATCH: bug fixes, small corrections, no behavior change for the user.
  - MINOR: new feature, new option, backward-compatible capability.
  - MAJOR: breaking change (removed feature, changed data shape, changed minimum requirements).
  - A version bump means: increment `Version` in the plugin header, `{PREFIX}_VERSION`-style constant, and `Stable tag` in `readme.txt` together (checked by `fswp-qa-engineer`'s version-consistency check either way), open a **new** changelog entry, and close the previous one.
- **Changelog entries stay concise, unique, non-duplicative.** One line per real change, in the user's terms (what changed, not how). Never restate the same fix twice across entries. Group by Added / Changed / Fixed / Removed when an entry has more than a couple of lines.
- Before adding a changelog line, check whether the latest entry already describes this change — update that line rather than adding a near-duplicate.

## 2. Technology stack

- **The stack the user chose (or that was already decided for this project) is not replaced by default.** Once set, it is the standing decision for that project — don't re-propose a different stack on a later iteration just because it's not what a fresh build would default to.
- **Override it only for a clear, stated reason**: it conflicts with an industry standard or established WordPress/PHP practice, a real technical constraint (hosting limits, PHP version ceiling, a library that doesn't exist for the chosen stack), or the actual requirement changed. State the reason plainly when proposing an override; never swap silently.
- **New project, or the existing stack looks wrong for what's being asked:** decide the stack before writing any code. This follows `fswp-architect`'s PRD process — the admin-UI tier (native / `@wordpress/components` / Tier 3) and JS tier (vanilla / Alpine) decisions in PRD sections 7–8 *are* this decision for a WordPress plugin; there is no separate stack question to ask beyond what the PRD already asks and confirms at approval.
- **Per-project, not global.** A stack decision made for one plugin is not a default for the next one — `fswp-architect` runs its questions fresh each time, even for the same client.

## 3. Required project information

Collect this before generating any plugin metadata; **never invent a missing value** — omit the corresponding header/field/link rather than fill it with a placeholder (this is the same rule that already governs `--plugin-uri`/`--author-uri` in the scaffold script).

| Item | Where it's used |
|---|---|
| Company name | Plugin header `Author`, `readme.txt`, about screen |
| Product/plugin name | `Plugin Name` header, `readme.txt` title, about screen |
| Company/product acronym | Prefix for code identifiers (`fswp-architect`'s prefix rule) — internal only, never user-visible text |
| Author name | `Author` header, `readme.txt` |
| Contributors (if any) | `readme.txt` `Contributors:` field |
| Company/product links (website, docs, support, repo, product page) | `Plugin URI`, `Author URI`, `readme.txt` header block, about screen "Links" section |

Ask for whatever isn't already stated as part of `fswp-architect`'s essential-questions round (Step 1); don't add a second round just for this — fold it into the same pass. If a link or contributor genuinely doesn't exist yet, leave that field out of the generated files rather than asking again later.

## 4. Feature documentation

Every plugin, and every internal feature/functionality within it, gets a documentation entry describing what it does and how — detailed enough that if the feature is broken, removed, or changed by accident, the doc alone is enough to restore the intended behavior without re-deriving it from the code.

- **Location:** `docs/<feature-slug>.md` inside the plugin folder (one file per feature), plus a short `docs/README.md` index linking each. For a single-feature plugin, one `docs/overview.md` is enough — don't force a multi-file split that adds no value.
- **Update on every meaningful iteration**, not just at delivery. A change that alters behavior, inputs, outputs, or a dependency updates the matching doc in the same turn as the code change.
- **Each feature doc covers, only where applicable (skip a heading with nothing to say rather than padding it):**
  - What it does (one or two sentences, plain language)
  - How it works (the mechanism — hooks used, data flow, key functions/classes)
  - Inputs (settings, parameters, REST args, shortcode attributes)
  - Outputs (what it renders, returns, or stores)
  - Dependencies (other features/classes it relies on, external services, the JS/admin tier it uses)
  - Constraints (capability required, rate limits, size caps, version requirements)
- **Format: Markdown by default, JSON only where it's genuinely more token-efficient and more reliably agent-parseable.** Decide per feature, not per plugin:
  - **Markdown** (the default) for anything prose-heavy — "what it does," "how it works," the narrative parts of any section above. It reads naturally for both a human and an agent, and costs roughly the same tokens as an equivalent JSON encoding once you account for JSON's mandatory punctuation, so there's no efficiency case for it here.
  - **JSON** only for content that's genuinely structured/enumerable and would otherwise be forced into a markdown table an agent has to re-parse — a settings/options schema, a REST route table (path, method, args, permission), a data-model field list. Embed it as a fenced ` ```json ` block **inside the same feature doc**, right under the heading it supports — never a second parallel file. Two files per feature (one `.md`, one `.json`) costs more tokens to open and reconcile than one file with a fenced block, and breaks the "self-contained, one file per feature" rule above.
  - When genuinely unsure which fits a given section, Markdown wins — it's both the safer default (per this section's own preference) and, per the quality bar (`standards.md` section 6, traits "minimalistic" and "efficient"), the simpler structure carries more weight than a marginal token difference.
- **Format:** headings/subheadings, lists, tables where they help scanning. Fluff-free — no restating the obvious, no marketing language. Self-contained: a reader shouldn't need to open three other files to understand one feature.
- **No duplication** across doc files unless duplication genuinely helps usability (e.g., a shared constraint worth restating in two feature docs a reader is unlikely to read together) — otherwise cross-reference instead of repeating.

## 5. Code quality

Write every plugin the way an experienced enterprise WordPress team would:

- **Secure, efficient, maintainable, modular.** Security baseline (`fswp-security-engineer`) is never optional or scaled down (already the rule); efficiency means no unbounded queries or redundant work, not micro-optimization.
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
- Every `fswp-qa-engineer` finding: state the fact (what failed, where), not a hedge around it.
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

**Trimming existing code** is `fswp-reviewer`'s lean lens (read-only findings), not a build-time activity.
