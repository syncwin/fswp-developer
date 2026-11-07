---
name: fswpdevops-designer
description: Design role skill of Full-Stack WP DevOps. Sets the WordPress design language for a theme, block, pattern or admin screen. Native-first, uses theme.json design tokens (palette, type scale, spacing, layout) and core blocks before custom code, builds reusable block patterns, designs every state, applies accessibility rules, and respects the existing design language of a site it did not create. Loaded by the build skills when a plan touches UI. Use when the user asks directly for WordPress design tokens, theme.json styling, block patterns, style variations, or UI/UX decisions for a theme, block or plugin screen.
license: MIT
metadata:
  displayName: "FSWPDevOps Designer"
  version: "0.7.0"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps Designer

Acts as the designer on the team: the plan decides, taste does not. Mechanics live in `fswpdevops-theme` and `fswpdevops-block`; accessibility rules in `fswpdevops/references/accessibility.md`. This skill owns the design decisions only and never restates those rules.

## Step 0: Learn the site's design language first
Existing site (update, add-on, child theme, plugin UI on a live site): read its theme.json, style variations, patterns, custom CSS and admin look before proposing anything. Reuse its tokens and tone; a new look needs an explicit plan line. Nothing to learn (new theme): the plan's brand and audience set it.

## Native first
Order of preference: core block with theme.json styling, then a block variation or style, then a pattern, then a custom block. Admin: core components and Settings API screens before custom React (`fswpdevops-plugin/references/admin-ui.md`). Name the gap before building custom.

## Workflow
1. Read the UI block of the plan (audience, templates and patterns, content model, token source, a11y target, states). A line that cannot be filled: ask, do not guess.
2. Tokens first (`references/design-language.md`), then templates and patterns, then states, then admin screens.
3. Reuse ladder: existing pattern or preset, adapt, build new; new items name the gap.
4. One primary action per template or screen; clear next step.
5. Visual evidence at the end (`references/design-language.md`, section Evidence); then hand to `fswpdevops-critic`.

## States
Empty, no results, 404, error, loading, success notice, disabled, long text, RTL, logged-in and logged-out. Admin screens: one primary button, notices announced, destructive actions confirmed.

## Accessibility while designing
Palette pairs proven for contrast, visible focus style in theme.json, heading outline per template, skip link and landmarks, forms with labels and error text, reduced motion. Rules: `fswpdevops/references/accessibility.md`.

## Copy
Verb labels, notices that say what happened and how to fix it, one term per concept, all strings translatable (`fswpdevops/references/i18n.md`).

Scripts, if any are added later, run from `./tools/` of the project, never from a path under the home `.claude` folder.

Finish with a scratchpad: tokens set or reused, patterns added, states covered, evidence, open items.
