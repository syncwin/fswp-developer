# Lean coding (foundational, always applied)

The best code is the code you did not have to write. This is the lean ladder: decisions made **before** typing, so the result is smaller, simpler, easier to review, and still complete. Be lazy about the solution, never about completeness. Method adapted from [Ponytail](https://github.com/dietrichgebert/ponytail) by Dietrich Gebert (MIT); wording is original (see `CREDITS.md`).

## Before writing: read and list touch points

Read the task and the code it touches. List every place the change must reach: callers, hooks that fire or listen, templates, tests, fixtures, config, exports, `readme.txt`, uninstall and upgrade paths. Ask what could break for users (data loss, exposure, callers that stop working). That list is the scope.

## The ladder (take the first rung that fully works)

1. **Does it need to exist?** If the plan does not require it, skip it and say "skipped: X, add when Y". A vague request gets the smallest version that does the core job.
2. **Reuse the project.** Search helpers, classes, hooks, options, blocks and patterns first. Prefer an existing plugin hook over a new one.
3. **Core WordPress or PHP provides it.** Core before custom code: Settings API, `WP_List_Table`, `wp_remote_*`, transients, capabilities, REST, cron (Action Scheduler when installed), core blocks and patterns, `theme.json` instead of CSS, a documented filter instead of a fork. See `wordpress-shortcuts.md`.
4. **An installed dependency provides it.** Never add one for a few lines; weigh size, maintenance, licence and directory rules.
5. **One readable line.**
6. **Minimum working code** in the project's style. Add a small test for non-trivial logic (branches, loops, parsers, money, security).

## Never cut

Input validation and sanitizing at trust boundaries, escaping, capability checks and nonces, error handling that prevents data loss, security, accessibility, and anything the user explicitly asked for. Moved or merged code keeps its validation.

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

`// shortcut: <limit>, upgrade when <trigger>`

`fswpdevops-reviewer` collects these markers into a ledger (debt mode). An unlabeled shortcut is a hidden defect.

## Effort levels

| Level | When | What changes |
|---|---|---|
| **Standard** (default) | Normal work | Apply the ladder and the rules above |
| **Quick draft** | The user wants something to react to | Build what was asked; name the simpler alternative in one line |
| **Leanest** | The user asks for minimal or the plan looks speculative | Challenge each optional line of the plan before building, ship the smallest thing that satisfies the rest, list what was deferred. Never cut what the plan states plainly |

## Site and script rules (shared)

- **E1, native first.** Use WordPress and the site's installed plugins' native features first and check their official docs; write custom code only when nothing native exists.
- **E7, learn the site before building.** Before any build, learn the site's existing stack and settings (active theme, plugins, builder, global styles) so nothing breaks and the site's setup and design language are respected.
- **E9, script paths.** Skills that run scripts copy them once per session into the working folder (e.g. `./tools/`) and run from there; never put a `/root/.claude` or `~/.claude` path in a shell command.

## Keep agents narrow

The same idea applies to how work is delegated: each agent gets one job, the smallest toolset that does it, and only the files it needs. The reviewer agent reads only; it never edits. Do not give agents open-ended scope, do not have two agents repeat the same analysis, and pass forward results instead of re-deriving them. Keep chat replies short too: lead with the result, list only decisions and open items.

## Self-check before delivering a change

- Could a reviewer delete any part of this diff without losing a stated requirement?
- Is there any file, class, hook, option, or dependency in the diff that the plan did not require?
- Did I reuse a core function or existing project helper wherever one exists?
- Are all shortcuts labeled?
- Is the diff free of unrelated reformatting?

If the answer to the first two is yes or the last three is no, cut or fix before handing to `fswpdevops-qa`. See `fswpdevops/references/wordpress-shortcuts.md` for common WordPress substitutions.
