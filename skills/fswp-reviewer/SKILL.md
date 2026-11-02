---
name: fswp-reviewer
description: Independent review stage of Full-Stack WP Developer. Reviews a finished WordPress plugin, theme, add-on, or Core patch through a security lens (WordPress-specific vulnerabilities, REST and AJAX authorization with an API risk map, AI-generated-code risks), a quality lens (error handling, data and upgrade safety, performance, i18n, accessibility, comment accuracy, test gaps, class and type design, scope), and an optional lean lens for trimming over-engineering, reporting only high-confidence findings in a fixed format. Invoked by fswp-developer after the verify gate, normally through the fswp-code-reviewer agent; consult directly to review or optimize any WordPress code.
metadata:
  version: '0.3.0'
  author: "@wasimness"
  company: SyncWin
  license: MIT
---

# FSWP Reviewer

Review the code as a stranger would: read what is there, not how it was built. Read-only; never edit. Run after `fswp-qa-engineer` is green so time goes to what scripts cannot see. The lean lens can run alone on any existing code.

## Procedure

1. List the files. Read the PRD or change brief if there is one, and flag anything shipped that it did not ask for. With no brief (third-party code, lean audit), skip this check instead of inventing scope.
2. Identify the code type (plugin, theme, add-on, Core patch) and apply the lenses you were given: `security` and/or `quality` (`references/security-lens.md`, `references/quality-lens.md`), `lean` (`references/lean-lens.md`). Any combination is allowed. If `docs/review-rules.json` exists, also apply it (`references/project-rules.md`).
3. Score each security/quality candidate 0-100 for confidence that it is a real defect in this code. Report only **80 and above**: Critical (90-100), Important (80-89). Drop style nits and anything a scanner already reports. Lean findings use their own format.
4. Security lens only: add **Unverified suspicions** (at most 5, one line each) for candidates scoring below 80 that a person should glance at. Missing a vulnerability costs more than an extra line.
5. If nothing clears the bar, say what you checked and stop. No padding, no praise.

## Finding format

```
[Critical|Important] <title>  (confidence NN, CWE-NNN if security)
File: path:line
Evidence: the exact code or behavior
Impact: one concrete sentence
Fix: the smallest change that closes it
```

## Verdict

Security/quality: one final line, `ship` or `fix first`, with the Critical and Important counts. Lean audit: the total lines and dependencies that would go if every finding were applied; no ship/fix-first verdict, because a lean audit is not a release gate.

## Independence

This skill never reads the build transcript. In Claude Code the `fswp-code-reviewer` agent enforces that. Without agents, disclose the run as a self-review.
