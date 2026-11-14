---
name: fswpdevops-maintain
description: Use when changing existing WordPress code in Full-Stack WP DevOps. Change stage for existing WordPress code in Full-Stack WP DevOps. Updates, fixes, refactors, and upgrades existing plugins and themes without breaking them, and builds add-ons for products you do not own (WooCommerce extensions, page-builder elements, extensions of other plugins) using hooks instead of edits to third-party files. Covers reading before changing, parity lists, deprecation, host compatibility, upgrade paths, and patch delivery. Invoked by fswpdevops after an approved change brief; use directly for safe-change or add-on questions.
---

# FSWPDevOps Maintainer

The existing code is the specification. Executes an approved change brief from `fswpdevops-plan` (which already ran the `detect_wp_project` recipe). Follow the project's own conventions unless they are unsafe; house templates are for new projects, not for rewriting someone else's style.

## Mode A: Update an existing plugin or theme

1. **Read first, list touch points.** Apply the lean ladder (`fswpdevops/references/lean-coding.md`): read the files the change touches, their callers, and their tests, and list every place the change must reach. Note the prefix, naming, error-handling style, and how settings and data are stored. Research before building: apply the router's Official first rule.
2. **Reproduce.** For a bug, write down steps and the observed result; confirm the failure before changing anything. For a feature, state the acceptance check.
3. **Smallest change that works.** Fix the cause in shared code, not one call site. Do not reformat untouched code; noisy diffs hide real changes and break blame.
4. **Protect the public surface.** Hook names, function and class names, option keys, meta keys, REST routes and shapes, shortcode attributes, and template overrides are contracts. To change one, deprecate first: keep the old one working, call `_deprecated_function()` / `_deprecated_hook()` (or `_deprecated_argument()`), document the replacement, and remove no sooner than a later major version.
5. **Upgrade path.** If data or schema changes: bump a stored version option, run a migration on load (not only on activation), make it idempotent, and test upgrading from the previous version's data without reactivating.
6. **Compatibility.** Respect the declared `Requires at least` and `Requires PHP`; guard newer functions with `function_exists()`/version checks or raise the minimum deliberately and say so.
7. **Security pass** on the touched code (`fswpdevops-security`): a bug fix must not add a new entry point without authorization, nonce, sanitization, and escaping.
8. **Version and changelog.** Fix = patch, feature = minor, breaking = major. Move the plugin/theme version, the constant, `readme.txt` Stable tag, and the changelog together.
9. **Deliver** as a patch or diff for the repo the user works in, or a zip when they deploy files. Include the parity checklist result.

Themes: prefer a **child theme** or `theme.json`/style-variation changes over editing a parent theme that receives updates. Direct edits to a parent, and edits to third-party plugin files, are lost at the next update.

## Mode B: Add-on for a product you do not own

An add-on is a separate plugin (or a small theme layer) that extends a host. Structure it with `fswpdevops-plugin` (steps 1-3 and 8), then apply these rules:

1. **Extend through the host's public API.** Use documented actions, filters, registries, and REST routes. Never edit host files and avoid calling internals marked private or undocumented; if you must, isolate the call in one adapter class and guard it.
2. **Declare the dependency.** Add `Requires Plugins: host-slug` to the header when the host is on WordPress.org (WordPress 6.5 and later enforces it). Also detect at runtime: check for a class, function, or constant, or a version constant, not the plugin file path.
3. **Load at the right time.** Initialize on `plugins_loaded` (or the host's own ready hook) after confirming the host exists; register on the host's registry hooks, not earlier.
4. **Fail quietly and clearly.** Host missing or too old: do nothing else, show one admin notice explaining what is needed, and never fatal.
5. **Version range.** State the supported host versions in the readme and the plan. Test the lowest and the newest supported.
6. **Compatibility declarations.** Some hosts require you to declare feature support. Example: WooCommerce expects extensions to declare compatibility with High-Performance Order Storage and the block-based cart and checkout. Read the host's developer docs for the current declaration calls.
7. **Data ownership.** Store your data under your own prefix; do not write into the host's tables or options. Uninstall removes only your data.
8. **Licensing and naming.** Follow the host's brand and trademark rules for names; use a descriptive "for X" style rather than implying it is official.

## Verify

Docs move in the same change as the code (`fswpdevops/references/coding-standards.md`, Documentation standard): an `[Unreleased]` line, the touched feature files, the index. Migrating an older project: `git mv docs/<feature>.md docs/features/`, add `docs/features/README.md` and the template headings (the `qa_check.md` recipe WARNs on the legacy layout until then). A pure refactor needs only a `### Changed` or `docs: none` line under `[Unreleased]`.

Hand to `fswpdevops-qa` with the change brief's parity list and compatibility table as the scenario source. `references/safe-change-checklist.md` is the quick pre-delivery list.

Finish with a scratchpad: baseline gate, change made, gate after, open items.
