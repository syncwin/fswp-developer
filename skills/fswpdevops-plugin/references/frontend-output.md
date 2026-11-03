# Public-Facing Output — Reusing the Atomic Framework

Confirmed default: front-end output (shortcodes, blocks, widgets this
plugin renders on the site for visitors) reuses the **Atomic Framework** (`afw-tokens.css`, `afw-components.css`,
`afw-foundation-logics.js`, supplied by the user) for visual/
behavioral consistency across the project's front-end tools. Admin screens
do NOT use this (see `admin-ui.md`).

**This skill does not bundle the Atomic Framework.** It's a
separately maintained product, updated on its own release cycle
outside this skill — carrying a static copy here would go stale the
moment that product ships an update, and silently building plugins
against an outdated design system is worse than not bundling at all.

**When a plugin build needs front-end output, ask the user for the
current Atomic Framework files** (`afw-tokens.css`,
`afw-components.css`, `afw-foundation-logics.js`, plus
`alpine.min.js` / `alpine-loader.js` / `alpine-components.js` only if
the Alpine tier below is also confirmed) before scaffolding — don't
assume a path, don't reconstruct them from memory, and don't proceed
without them. Once the user provides a path (or uploads the files),
pass it to `scripts/scaffold_plugin.py` via `--foundation-dir`; the
script copies from there into the generated plugin, same as before —
only the source location changed, not the plugin's own runtime
structure below.

## Key structural point: a plugin owns and enqueues its own assets

Unlike a snippet-based tool that leans on something else being pasted
onto the site separately, a real plugin is self-contained: once
supplied, the Atomic Framework files are copied into the generated
plugin's `public/foundation/` at scaffold time, and the plugin
enqueues them itself, conditionally, only where used. This is a
one-time copy at scaffold time — the generated plugin doesn't reach
back out to wherever the files came from at runtime.

```
public/
├── class-{{prefix}}-public.php
├── css/{{plugin-slug}}.css        ← this plugin's own composition CSS
├── js/{{plugin-slug}}.js          ← this plugin's own JS
└── foundation/                     ← Atomic Framework files, supplied by the user, unmodified
    ├── afw-tokens.css
    ├── afw-components.css
    └── afw-foundation-logics.js
```

At scaffold time, `scripts/scaffold_plugin.py --foundation-dir <path>`
copies the Atomic Framework files from that user-supplied location
into the generated plugin's `public/foundation/`. If `--foundation-dir`
isn't passed and `--features` includes `frontend`, the script stops
and prints a reminder to get the current files from the user first —
it does not fall back to generating placeholder or out-of-date
versions of them.

## Shortcode with conditional, properly-enqueued assets

```php
// public/class-{{prefix}}-public.php
class {{Prefix}}_Public {
    const SHORTCODE = '{{prefix_lower}}_{{code}}';

    public function __construct() {
        add_shortcode( self::SHORTCODE, array( $this, 'render' ) );
    }

    public function render( $atts ) {
        $atts = shortcode_atts( array(), $atts, self::SHORTCODE );

        // Register + enqueue only when the shortcode is actually used on this request.
        wp_enqueue_style( '{{prefix_lower}}-foundation', {{PREFIX}}_PLUGIN_URL . 'public/foundation/afw-tokens.css', array(), {{PREFIX}}_VERSION );
        wp_enqueue_style( '{{prefix_lower}}-components', {{PREFIX}}_PLUGIN_URL . 'public/foundation/afw-components.css', array( '{{prefix_lower}}-foundation' ), {{PREFIX}}_VERSION );
        wp_enqueue_style( '{{plugin-slug}}', {{PREFIX}}_PLUGIN_URL . 'public/css/{{plugin-slug}}.css', array( '{{prefix_lower}}-components' ), {{PREFIX}}_VERSION );

        wp_enqueue_script( '{{prefix_lower}}-foundation-logic', {{PREFIX}}_PLUGIN_URL . 'public/foundation/afw-foundation-logics.js', array(), {{PREFIX}}_VERSION, true );
        wp_enqueue_script( '{{plugin-slug}}', {{PREFIX}}_PLUGIN_URL . 'public/js/{{plugin-slug}}.js', array( '{{prefix_lower}}-foundation-logic' ), {{PREFIX}}_VERSION, true );

        ob_start();
        ?>
        <div class="afw-scope {{prefix_lower}}-{{code}}">
            <!-- markup, using afw-* component classes per afw-components.css -->
        </div>
        <?php
        return ob_get_clean();
    }
}
```

Enqueueing **inside the shortcode's render callback**, not
unconditionally on `wp_enqueue_scripts`, keeps assets off pages that
don't use the shortcode. If the same output also needs to work as a
Gutenberg block, register block assets via `block.json`'s
`style`/`script` handles instead, pointing at the same bundled files —
core handles the conditional loading for blocks automatically.

**Enqueue rule.** Enqueue inside the render callback, never gated on `has_shortcode( $post->post_content )`: page builders such as Bricks keep content outside `post_content`, so that check silently skips assets. `wp_enqueue_*` is idempotent per handle, so repeated shortcodes are safe; keep handle names constant.

## Fonts and remote assets

- No third-party requests at runtime: no CDN scripts or styles, no hosted fonts or icon sets, no remote images or analytics.
- Google Fonts specifically sends visitor IPs to Google, a GDPR issue, so local bundling is mandatory, not stylistic.
- Bundle fonts as woff2 under `public/fonts/`, subset to needed glyphs, `font-display: swap`, with the font's license file (for example `OFL.txt`) beside them.
- The only exception is an explicit client request recorded in the PRD decisions log; fonts stay local regardless.

## Units and accessibility

- Type, spacing, and radius output is `rem` on a 16px root, never `px` (hairline borders and shadows may stay `px`).
- If a design system uses a 62.5% root (1rem = 10px), rebase at export time only: output value = px / 16. Never set `html { font-size: 62.5% }` in a plugin; it changes every `rem` on the site.
- Preview iframes and shadow roots never override the root font size; they inherit the host's.
- **WCAG 1.4.4 (Resize Text):** any plugin that generates fluid type flags steps that risk failing 200% zoom. Heuristic: flag a `clamp()` whose max exceeds 2.5x its min, or whose preferred value is viewport-only (`vw` with no `rem` term). Confirm by zooming to 200% in a browser.

## JS tier decision: mechanical checklist, not judgment

The vanilla tier is the default and requires no sign-off. The Alpine
tier is **never inferred silently** — it can only be selected by
running the plugin's requested front-end behavior through the fixed
checklist below, then explicitly confirming with the user before
scaffolding anything. This removes "does this feel like it needs
state" guesswork, which is exactly the kind of soft judgment call
that drifts between two similarly-worded requests.

### Step 1 — Run every requested front-end feature against these five checks

Answer yes/no for each. These are the ONLY triggers for the Alpine
tier — no other reasoning overrides them in either direction:

1. **Cross-component update** — does one interaction have to update
   two or more independent DOM regions at once (not just show/hide
   inside a single component), without a full page reload?
2. **Shared read/write state** — does more than one on-page component
   need to read AND write the same piece of client-side data (e.g. a
   filter value both a search box and a result count depend on)?
3. **Client-side data reshaping without a server round-trip** — does
   already-loaded data need to be filtered, sorted, or paginated in
   the browser, repeatedly, without re-fetching from the server each
   time?
4. **Multi-step flow with carried state** — is there a wizard/stepper
   where a later step's behavior depends on data entered in an
   earlier step, before anything is submitted to the server?
5. **Live REST-driven re-render** — does the page need to re-fetch
   from this plugin's REST route and re-render part of itself
   in response to user input, more than once, without a page
   navigation (e.g. type-ahead search, a "load more" list)?

**If ALL five are "no":** use the vanilla tier. Proceed without
asking — this is the default and needs no confirmation.

**If ANY are "yes":** the Alpine tier is genuinely warranted. Do NOT
scaffold yet — go to Step 2.

### Step 2 — Explain and get explicit confirmation before proceeding

Before generating any front-end code, tell the user plainly:

- Which checklist item(s) triggered it (quote the specific behavior
  they asked for that maps to the check — not just "this needs
  state").
- What adding Alpine means in concrete terms: one extra ~17KB script,
  loaded via the dual-guard pattern (Step 3 below) so it's safe
  alongside other plugins, versus zero extra dependency on vanilla.
- What the vanilla alternative would look like if they'd rather not
  add the dependency (usually: more hand-wired `data-*` attributes
  and event listeners, or a feature reduction — e.g. filtering
  triggers a full page reload instead of live in-browser filtering).

Then ask a direct yes/no: proceed with the Alpine tier, or stay
vanilla and accept the reduced version of the feature. Do not
scaffold the Alpine tier until the user has explicitly confirmed —
this is a sign-off gate of the same kind as the prefix/distribution-
target/feature-surface confirmations in `SKILL.md`, not a detail to
mention after the fact.

### Step 3 — If confirmed, use the safe dual-guard loading pattern (mandatory)

WordPress sites often run several plugins from several vendors on the
same page. Two independent protections are required, not one:

1. **Same handle across every Atomic-Framework-built plugin.** Always enqueue the
   loader under the literal handle `fswp-alpine-loader` — never
   `{{prefix}}-alpine-loader`. WordPress's dependency system dedupes
   by handle, so if two of your own plugins are active on the same
   site, only one script tag for it ever prints.
2. **Runtime guard for anything outside your control.** The bundled
   `alpine-loader.js` checks `window.Alpine` before injecting
   `alpine.min.js`, so a genuinely unrelated third-party plugin that
   already loaded its own Alpine copy won't cause a double-init.

```php
private function enqueue_alpine_tier() {
    wp_enqueue_script(
        'fswp-alpine-loader', // literal, shared handle — do not prefix per plugin
        {{PREFIX}}_PLUGIN_URL . 'public/foundation/alpine-loader.js',
        array(),
        {{PREFIX}}_AFW_VERSION, // version of the SUPPLIED Atomic Framework files, not this plugin — see note below
        true
    );
    wp_enqueue_script(
        '{{prefix}}-alpine-components',
        {{PREFIX}}_PLUGIN_URL . 'public/foundation/alpine-components.js',
        array( 'fswp-alpine-loader' ),
        {{PREFIX}}_VERSION,
        true
    );
}
```
`{{PREFIX}}_AFW_VERSION` is a constant this plugin should
define alongside `{{PREFIX}}_VERSION` in the bootstrap file, set to
whatever version the user's supplied Atomic Framework files actually
are (ask them, or read it from the files/directory they provide if it's
recorded there — e.g. a version comment at the top of
`afw-tokens.css`). Never hardcode a specific Alpine version number
here: since this skill no longer bundles the framework (see the top of
this file), any version string baked into the template would silently
go stale the moment the user's copy is updated. If no version
information is available, fall back to `{{PREFIX}}_VERSION` so cache-
busting still works on every plugin release, even if it doesn't track
the framework's own version precisely.

The `alpine.min.js` vendor file itself is never directly
`wp_enqueue_script`'d — it's injected by the loader at runtime, which
is what makes the `window.Alpine` guard possible (a statically
enqueued script has already executed by the time you could check).

### Markup contract — same classes, different attributes per tier

Both tiers style identically via the same `.afw-tabs`,
`.afw-accordion`, `.afw-modal`, `.afw-menu` classes (see
`afw-components.css`). They differ only in behavior-wiring attributes:

```html
<!-- Vanilla tier: plain ARIA + data-attributes, wired by initTabs() -->
<div class="afw-tabs">
  <div class="afw-tabs__list" role="tablist">
    <button class="afw-tabs__tab" role="tab" aria-selected="true" aria-controls="panel-1">One</button>
    <button class="afw-tabs__tab" role="tab" aria-selected="false" aria-controls="panel-2">Two</button>
  </div>
  <div id="panel-1" class="afw-tabs__panel" role="tabpanel">...</div>
  <div id="panel-2" class="afw-tabs__panel" role="tabpanel" hidden>...</div>
</div>

<!-- Alpine tier: x-data wires the same classes to Alpine.data('afwTabs') -->
<div class="afw-tabs" x-data="afwTabs('one')">
  <div class="afw-tabs__list" role="tablist">
    <button class="afw-tabs__tab" role="tab" data-tab-key="one" :aria-selected="isActive('one')" @click="select('one')">One</button>
    <button class="afw-tabs__tab" role="tab" data-tab-key="two" :aria-selected="isActive('two')" @click="select('two')">Two</button>
  </div>
  <div class="afw-tabs__panel" x-show="isActive('one')">...</div>
  <div class="afw-tabs__panel" x-show="isActive('two')">...</div>
</div>
```
Never mix both attribute sets on the same element — pick one tier per
plugin and use it consistently across that plugin's output.



Zero `<h1>`/`<h2>`/`<h3>` inside shortcode/block output — a plugin's
front-end markup is embedded into an arbitrary page/post and must not
assume it owns the page's heading hierarchy. Use `<div>`/`<span>`
with `.afw-*` classes for visual heading-like treatment instead, and
let the *page* content (title, intro copy) provide the real headings.

## When NOT to reuse the Atomic Framework here

If the plugin is being built for a client/context where the Atomic Framework
visual identity is inappropriate (a client with their own brand who
will see this front-end output), skip the foundation bundle entirely
and write plain, minimally-styled semantic markup with BEM classes
prefixed to the plugin's own prefix instead — ask if this is unclear
from context. Never ship Atomic-Framework-branded visual output to a client project that has not asked for it.
