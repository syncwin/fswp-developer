# Lean coding (foundational, always applied)

The best code is the code you did not have to write. This skill is a set of decisions made **before** typing, so the result is smaller, simpler, easier to review, and still complete. It never lowers the bar for security, validation, accessibility, or error handling: those are required behavior, not extras.

## The decision ladder (stop at the first rung that answers)

1. **Is it in the approved plan?** If not, do not build it. Note it as a suggestion at most.
2. **Does this project already do it?** Search first (helpers, classes, hooks, options, existing blocks or patterns). Reuse and extend.
3. **Does WordPress already do it?** Core has APIs for options, settings, HTTP, transients, caching, users, capabilities, media, cron, REST, blocks, scripts, and more. Prefer core over custom code. Check the Code Reference before writing a helper.
4. **Does PHP or the standard library do it?** Use the built-in.
5. **Does an installed dependency do it?** Use it; do not add a second one for the same job.
6. **Only then**, write the smallest code that meets the plan, in the project's style.

Also consider whether the requirement can be met with **no code**: a core block or pattern instead of a custom block, `theme.json` instead of CSS, a setting instead of a template edit, a documented filter instead of a fork.

## Rules that keep code small

- **Fewest files and layers that do the job.** No interface with one implementation, no factory for one product, no wrapper that only forwards, no option for a value that never changes, no class where a function will do.
- **Fix causes, not call sites.** Find every caller of the function involved and repair the shared code once.
- **Delete before adding.** When changing behavior, remove the code that becomes dead in the same change.
- **No speculative features, hooks, or settings** "for later". Add them when a real requirement arrives.
- **Plain over clever.** WordPress standards prefer readability over brevity. Small does not mean cryptic.
- **Ask what could break when it grows, not what could be added now.** Leave a `// shortcut:` marker instead of building for it.
- **No new dependency for one function.** Weigh size, maintenance, license, and directory rules.
- **Data over code.** A table, array, or JSON file that drives behavior beats branching logic copied per case.

## Label knowing shortcuts

When you deliberately cut a corner (a loop that is quadratic but the list is capped, a single global lock, a heuristic instead of the exact test), mark it where it lives:

`// shortcut: <the limit>; revisit when <trigger>`

`fswpdevops-reviewer` collects these markers into a ledger. An unlabeled shortcut is a hidden defect.

## Effort levels

| Level | When | What changes |
|---|---|---|
| **Standard** (default) | Normal work | Apply the ladder and the rules above |
| **Quick draft** | The user wants something to react to | Build what was asked; name the simpler alternative in one line |
| **Leanest** | The user asks for minimal or the plan looks speculative | Challenge each optional line of the plan before building, ship the smallest thing that satisfies the rest, list what was deferred. Never cut what the plan states plainly |

## Keep agents narrow

The same idea applies to how work is delegated: each agent gets one job, the smallest toolset that does it, and only the files it needs. The reviewer agent reads only; it never edits. Do not give agents open-ended scope, do not have two agents repeat the same analysis, and pass forward results instead of re-deriving them. Keep chat replies short too: lead with the result, list only decisions and open items.

## Self-check before delivering a change

- Could a reviewer delete any part of this diff without losing a stated requirement?
- Is there any file, class, hook, option, or dependency in the diff that the plan did not require?
- Did I reuse a core function or existing project helper wherever one exists?
- Are all shortcuts labeled?
- Is the diff free of unrelated reformatting?

If the answer to the first two is yes or the last three is no, cut or fix before handing to `fswpdevops-qa`. See `fswpdevops/references/wordpress-shortcuts.md` for common WordPress substitutions.
