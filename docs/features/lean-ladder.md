# Lean ladder

Status: shipped in 0.6.0.

## Context
Over-building is the commonest waste in agent-written code. One shared rule now covers planning, building and reviewing.

## Behaviour
- Read the touched code and list every touch point before planning.
- Climb six rungs and stop at the first that works: skip it, reuse the project (existing hooks first), core WordPress or PHP (Settings API, WP_List_Table, wp_remote_*, Action Scheduler if present), installed dependency, one line, minimum code.
- Never cut: input validation, escaping, capability checks, data-loss handling, security, accessibility.
- Shortcuts are recorded as `// shortcut: <limit>, upgrade when <trigger>`.
- Review lens modes: line, audit, debt.

## How it works
Single source: `skills/fswpdevops/references/lean-coding.md`. Used by `fswpdevops-plan`, the plugin, theme and block skills, `fswpdevops-maintain`, and the lean lens of `fswpdevops-review`.

## Limits
Guidance for the model; no script enforces it.

## History
- 0.6.0: merged into the existing lean-coding reference.

Method adapted from [Ponytail](https://github.com/dietrichgebert/ponytail) by Dietrich Gebert (MIT); text is original.
