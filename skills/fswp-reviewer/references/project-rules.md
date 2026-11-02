# Project rules (optional)

Some projects have house rules no general lens can know: a registry file whose entries stay in a fixed order, a class that must always get a matching doc update, a schema file that always needs a regression test. `docs/review-rules.json` lets the owner state those checks per path without editing the lenses.

## Loading

Before applying the lenses, look for `docs/review-rules.json` in the reviewed folder. If absent, skip this step; nothing else changes.

## Format

```json
{
  "rules": [
    { "paths": ["includes/class-*-rest.php"], "check": "Every route documents its auth model in a comment and has a test in tests/." },
    { "paths": ["uninstall.php"], "check": "Must remove every option named in docs/options.md." }
  ]
}
```

- `paths`: globs relative to the folder root. A file may match several rules; all of them apply.
- `check`: a specific, checkable statement, written like a lens entry, not a vague reminder.

## Applying

Rule violations are extra findings, scored and reported exactly like lens findings (same 80+ bar and format). Rules never disable or soften a lens the caller asked for. A rule that matches no reviewed file changes nothing; do not invent a finding to justify it.

## Ownership

The project owner writes this file. This skill reads it and never creates or proposes one unprompted. A malformed file (invalid JSON, missing `paths` or `check`) is reported once as a note, not silently ignored and not treated as a review failure.
