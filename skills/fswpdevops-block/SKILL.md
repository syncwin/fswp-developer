---
name: fswpdevops-block
description: Domain skill for WordPress block editor work in Full-Stack WP DevOps. Covers building custom Gutenberg blocks (block.json, static and dynamic rendering, attributes, supports, InnerBlocks, variations, deprecations, block bindings), block patterns, and the Interactivity API (data-wp directives, stores, server-side state), with the @wordpress/scripts build workflow. Use for any custom block, pattern, or front-end interactivity in a plugin or theme.
license: MIT
metadata:
  displayName: "FSWPDevOps Block Developer"
  version: "0.5.0"
  author: "@wasimness"
  company: "SyncWin"
---

# FSWPDevOps Block Developer

**Foundational (always applied):** `fswpdevops/references/lean-coding.md` (write less, reuse first), `fswpdevops/references/coding-standards.md` (coding standards, docs, i18n, accessibility), and `fswpdevops-security` (input, output, authorization).

Use core blocks first; write a custom block only when core blocks and patterns cannot express the requirement. Official references: Block Editor Handbook links in `fswpdevops/references/official-docs.md`. Check the minimum WordPress version for each API against the project's declared minimum.

## Anatomy

```
blocks/my-block/
  block.json      name, title, category, attributes, supports, render, editorScript, viewScriptModule, style
  edit.js         editor UI (uses useBlockProps)
  save.js         static markup, or omit for dynamic blocks
  render.php      server render for dynamic blocks
  view.js         front-end behavior (module)
  style.scss / editor.scss
```

Register from metadata: `register_block_type( __DIR__ . '/build/my-block' )` on `init` (use a named function for the `init` callback). Set `"apiVersion": 3` (current since WordPress 6.3) and add `"$schema": "https://schemas.wp.org/trunk/block.json"`. Field-by-field reference, verified against the Block Editor Handbook: `references/block-json.md`.

## Decisions

| Question | Choose |
|---|---|
| Output depends only on saved attributes | **Static** block (`save.js`) |
| Output depends on live data, must change without re-saving, or contains logic | **Dynamic** block (`render.php`); `save` returns `null` or only InnerBlocks |
| Nested content | `InnerBlocks` with `allowedBlocks` and `template` |
| Bind an attribute to data (post meta, custom source) | Block Bindings API (`register_block_bindings_source`) where the minimum WordPress version allows |
| Alternate presets of an existing block | Block variations or styles, not a new block |
| Reusable layout | A pattern, not a block |

## Rules

- Attributes: give every attribute a `type` and `default`; source them from markup or comments consistently; validate in `render.php`.
- Use `supports` (color, spacing, typography, align, anchor) instead of writing controls.
- Editor markup must use `useBlockProps()`; dynamic PHP uses `get_block_wrapper_attributes()`.
- `render.php` (block.json `render`, WordPress 6.1+) receives `$attributes`, `$content`, and `$block` (a `WP_Block`). It loads once per block instance on the page, so never declare functions or classes inside it; call shared code from another file.
- **Scripts vs modules:** `viewScript` is for classic scripts (and anything depending on WordPress scripts); `viewScriptModule` (6.5+) is for script modules such as the Interactivity API. They are not interchangeable, so do not mix dependencies across the two.
- Escape everything in `render.php` (`fswpdevops-security`); attributes are user input.
- Changing saved markup of a shipped static block breaks existing content. Add a `deprecated` entry with the old `save`, attributes, and a `migrate` function, then change the block.
- Translate strings (`__()` with the text domain) in JS and PHP; `wp_set_script_translations` or block.json `textdomain`.
- Load front-end scripts only where the block renders (block.json `viewScriptModule`/`script` do this).

## Patterns

More detail on patterns, variations, block hooks, and bindings: `references/patterns-variations.md`. Interactivity API depth (server rendering, async actions, `data-wp-each`, watchers, performance): `references/interactivity.md`.

Register in PHP with `register_block_pattern()` (and `register_block_pattern_category()`), or as files in a theme's `patterns/`. Patterns use presets and translated text; no remote images; give them a clear title, categories, and keywords.

## Interactivity API

Server-rendered markup plus small reactive behavior, no framework needed.

- Enable with `"supports": { "interactivity": true }` and `"viewScriptModule": "file:./view.js"`.
- Markup directives: `data-wp-interactive="namespace"`, `data-wp-context='{"open":false}'`, `data-wp-on--click="actions.toggle"`, `data-wp-bind--hidden="!context.open"`, `data-wp-class--is-open="context.open"`, `data-wp-text="state.label"`.
- Store in `view.js`: `import { store, getContext } from '@wordpress/interactivity'; store( 'namespace', { state: {...}, actions: { toggle() { const c = getContext(); c.open = ! c.open; } } } );`
- Seed server state with `wp_interactivity_state( 'namespace', array(...) )` so first paint is correct and no flash occurs. Keep state serializable.
- Namespace everything to avoid collisions; never put secrets in state or context (both are printed into the page).
- For accessibility, tie `aria-expanded` and focus handling to state, and test keyboard use.

## Build and test

`npx @wordpress/create-block` for a starting point; `@wordpress/scripts` for `build`, `start`, `lint-js`, `lint-style`, `test-unit-js`. Ship the built files together with `src/`, `package.json`, and the lockfile (directory rule for compiled code). Test in the editor (insert, edit, save, reload, switch to code view) and on the front end. Hand to `fswpdevops-qa`.
