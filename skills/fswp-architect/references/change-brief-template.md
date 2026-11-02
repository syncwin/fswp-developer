# Change brief (Update, Add-on, Core patch)

Fill every section; write "none" rather than leaving one blank.

1. **Summary**: one sentence on what changes and why.
2. **Target**: project, current version, path or repo, work type (Update / Add-on / Core patch). For Core: Trac ticket number or "to be filed", component, target branch (normally trunk).
3. **Triage findings**: output of `detect_wp_project.py` (project type, min versions, tooling, entry points).
4. **Current behavior**: what happens today, with the file and line where it happens.
5. **Requested behavior**: what should happen after the change.
6. **Parity list**: every behavior, option, hook, shortcode, route, and stored value that must keep working. Each is kept, changed (why), or removed (why). Nothing unlisted ships silently.
7. **Compatibility**: supported WordPress and PHP range; for add-ons the host product and version range, and what happens when the host is inactive or too old.
8. **Design**: the smallest change that works, the files touched, new hooks or options with prefixed names. Prefer extending through hooks over editing host or third-party code.
9. **Data and upgrade path**: option or table changes, migration on version bump, behavior when old data is present.
10. **Security and performance notes**: new inputs, outputs, queries, or assets and how each is protected or bounded.
11. **Test plan**: scenarios with expected results (each becomes a PASS / FAIL / NOT RUN row in `fswp-qa-engineer`), including a regression check for each parity item.
12. **Assumptions and open questions**.
13. **Delivery**: patch/diff, zip, or PR text; version bump and changelog line.
