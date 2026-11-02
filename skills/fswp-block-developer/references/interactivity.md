# Interactivity API depth

Purpose: declarative front-end behavior for server-rendered blocks, with state shared across blocks. Confirm current directive names and the minimum WordPress version in the Interactivity API reference before use; the API has grown across releases.

## Wiring

- Block opts in with `"supports": { "interactivity": true }` and `"viewScriptModule"` in block.json.
- The root element gets `data-wp-interactive="vendor/block"` (the store namespace). Everything under it can use directives.
- Server-render the initial state so the first paint is correct: `wp_interactivity_state( 'vendor/block', array( ... ) )`, and per-element context with `wp_interactivity_data_wp_context( array( ... ) )`.
- Core processes directives on the server for the initial HTML; the browser then hydrates.

## Directives you will use most

| Directive | Does |
|---|---|
| `data-wp-context` | Local state for this subtree (JSON) |
| `data-wp-on--click`, `--keydown`, ... | Run an action on an event |
| `data-wp-bind--attr` | Set an attribute from state (`hidden`, `aria-expanded`, `value`) |
| `data-wp-class--name` | Toggle a class |
| `data-wp-style--prop` | Set an inline style property |
| `data-wp-text` | Set text content |
| `data-wp-init`, `data-wp-watch` | Run when a node initializes or when tracked state changes |
| `data-wp-each` | Render a list from state |

## Store patterns

```js
import { store, getContext, getElement } from '@wordpress/interactivity';

const { state } = store( 'vendor/block', {
	state: {
		get isOpen() { return getContext().open; },
	},
	actions: {
		toggle() {
			const ctx = getContext();
			ctx.open = ! ctx.open;
		},
		*load() { // generator for async work
			const ctx = getContext();
			ctx.loading = true;
			try {
				const res = yield fetch( ctx.url );
				ctx.data = yield res.json();
			} finally {
				ctx.loading = false;
			}
		},
	},
	callbacks: {
		announce() { /* runs from data-wp-watch */ },
	},
} );
```

Use generator functions for async actions so the runtime can restore scope after each `yield`.

## Rules

- Namespace stores; never store secrets or anything that must stay private (state and context are printed into the page).
- Keep state serializable and small; derive values with getters instead of storing copies.
- Use native elements plus ARIA state bindings for accessibility; test keyboard and focus.
- Load only where the block renders (`viewScriptModule` handles this).
- Prefer no JavaScript at all when core blocks (for example Details) or CSS can do the job.

## Performance

Fewer directive nodes, small contexts, no work in watchers that runs every state change, and lazy-load heavy code with dynamic `import()` from an action.
