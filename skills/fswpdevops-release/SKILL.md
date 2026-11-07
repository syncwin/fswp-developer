---
name: fswpdevops-release
description: Release and distribution role for Full-Stack WP DevOps. Prepares plugins and themes for shipping - the WordPress.org plugin directory guidelines and theme review requirements (verified against the official pages), required plugin and theme headers, readme.txt rules, versioning and tagging, packaging, changelog discipline, and private-distribution basics. Use when the target is WordPress.org, when checking distribution readiness, or before any release.
license: MIT
metadata:
  displayName: "FSWPDevOps Release Manager"
  version: "0.7.0"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps Release Manager

The published rules are authoritative and change; the summaries here were checked against the official pages on 2026-09-28 (plugin guidelines, theme review requirements, plugin header requirements, readme standard, theme style.css requirements). Before advising on a submission, re-open the pages in `fswpdevops/references/official-docs.md` and follow them where they differ.

## Pick the path

| Target | Read |
|---|---|
| WordPress.org plugin directory | `references/plugin-guidelines.md`, `references/headers-and-readme.md` |
| WordPress.org theme directory | `references/theme-requirements.md`, `references/headers-and-readme.md` |
| Private or commercial distribution | Same hygiene, minus directory-only rules; the GPL question below still applies |

## Release checklist (all targets)

1. Version bumped everywhere it lives: main file header, version constant, `readme.txt` Stable tag (plugins) or `style.css` Version (themes), `package.json`, changelog.
2. `CHANGELOG.md`: move `[Unreleased]` into `## [X.Y.Z] - date` (fresh empty `[Unreleased]` on top), written for users, not commit noise; feature files and index match X.Y.Z; `readme.txt` changelog mirrors released sections. Pre-1.0 = beta; `1.0.0` only when the owner says. Standard: `fswpdevops/references/coding-standards.md`.
3. `fswpdevops-qa` gate and release check are green; every NOT RUN item is listed for the user. **Security gate:** reviewer security lens has no Critical or Important findings, secret scan and dependency audit ran (or are listed NOT RUN), `fswpdevops-security` §Secure by default is satisfied.
4. License headers present and every bundled asset's license documented (fonts, images, libraries).
5. No development files in the zip: no `.git`, `node_modules`, tests, editor configs, `.sh` or `.xml` files in themes, zip files inside the package. Compiled assets ship with their source and build steps.
6. Zip has the plugin or theme folder at its root, named with the slug, built from a clean checkout of the tag, with a SHA-256 checksum next to it (private distribution: sign it with the owner's key, never store keys in the repo).
7. Install the final zip on a clean site: activate, use, deactivate, delete (or mark NOT RUN and hand to the user).
8. For WordPress.org: submission notes, contact email that reaches a human, and answers ready for reviewer questions.

## Licensing in one paragraph

WordPress is GPL-licensed. Plugins and themes that run inside it are expected to be GPL-compatible; the directories require it for everything in the package. How you charge (free, paid, subscription, service) is separate from the license of the code. State the license in headers and readme, and keep a resource list for third-party files. This is guidance, not legal advice.

## WordPress.org release flow (plugins)

The plugin directory is a release repository in Subversion: `trunk/` for the current code, `tags/x.y.z/` for each release, `assets/` for banners, icons, and screenshots. The directory reads the Stable tag from the readme, finds the matching tag folder, and takes the version number from the main plugin file's header. Commit only release-ready code, with meaningful messages; avoid rapid trivial commits; increment the version for every release. GitHub automation of this flow is reserved (`fswpdevops/references/github-foundation.md`), not built.

## Themes

Uploaded through the theme directory's upload page and reviewed by the themes team; the required list is in `references/theme-requirements.md`. Themes with three or more distinct issues can be closed and resubmitted after fixes.

Finish with a scratchpad: version, package path, checks run, open items.
