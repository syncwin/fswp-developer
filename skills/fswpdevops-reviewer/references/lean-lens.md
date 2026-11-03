# Lean lens

Purpose: make working code smaller and simpler without changing behavior. This is an optimization pass, not a release gate, so it does not use confidence scores and does not block shipping.

## Two modes

**Line mode** (reviewing a diff or a file): tag each finding on one line.

`L<start>-<end> [category] <what to cut or replace> -> <replacement> (saves ~N lines)`

**Audit mode** (whole plugin/theme): scan every source file, list findings ranked by lines saved, largest first, and finish with the totals.

## Categories

| Category | Look for |
|---|---|
| single-use abstraction | Interface with one implementation, factory for one product, wrapper that only forwards, base class with one child |
| speculative option | Setting, filter, or parameter for a value that never varies |
| reinvented core | Hand-written code for something WordPress or PHP already provides (sanitizers, HTTP helpers, JSON, array utilities, caching) |
| redundant dependency | A package used for one function core or the language covers |
| dead or duplicate | Unreachable branches, unused functions and hooks, copy-pasted blocks that should be one function |
| premature performance | Caching, batching, or async around something measured as cheap |
| needless indirection | Layers a reader must open three files to follow |
| over-defensive | Checks for states that cannot happen inside trusted code (never applies to input validation or capability checks) |

## Rules

- Never propose removing security checks, input validation, escaping, capability checks, nonces, or error handling. Those are not "lean" candidates.
- Never propose changes that alter public behavior, hook names, option names, or REST shapes without labeling them breaking.
- Prefer deletion over rewrite; prefer core functions over new helpers.
- Record deliberate shortcuts: collect every `// shortcut:` marker into a ledger (file, line, stated limit, revisit trigger) and flag any whose trigger has probably been reached.

## Output for audit mode

```
1. includes/class-x-manager.php L1-84  single-use abstraction -> call the two functions directly (~80 lines)
...
Shortcut ledger: 3 markers, 1 likely due (file:line, reason)
Total if all applied: ~N lines, M dependencies
```
