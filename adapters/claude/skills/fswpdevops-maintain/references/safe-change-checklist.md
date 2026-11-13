# Safe-change checklist

Before delivering a change to existing code:

- [ ] Change brief approved; the diff touches only files the brief lists.
- [ ] Reproduction (bug) or acceptance check (feature) passes after the change and failed before.
- [ ] Every parity item was re-tested and marked.
- [ ] No public name changed without a deprecation shim and a note.
- [ ] Prefix and naming match the project; no unrelated reformatting.
- [ ] New inputs are authorized, nonce-checked, sanitized; new outputs are escaped; new queries are prepared and bounded.
- [ ] Upgrade from the previous version's stored data works without reactivation.
- [ ] Minimum WordPress/PHP unchanged, or raised on purpose and stated.
- [ ] Add-on: host active, inactive, and below-range cases handled with no fatal.
- [ ] Version, constant, readme Stable tag, and changelog moved together.
- [ ] Rollback is possible: the previous version's data still loads.

## Reading an unfamiliar codebase quickly

1. The `fswpdevops-plan/references/detect_wp_project.md` recipe for type, tooling, hooks, routes, post types.
2. Main file header and bootstrap: what loads, in which order.
3. Follow one request end to end (a route or a template) to learn the conventions.
4. Search for the string the user sees in the UI to find the code behind it.
5. `git log -p` on the file you will touch, if history exists, to see why it looks this way.
