# Admin UI, Tier 3 — Modern App Stack (React SPA + Tailwind)

Contents: Dependency policy — always install latest from the official registry; Decision checklist — confirm before choosing this tier; 1. Plugin foundation (unchanged); 2. Admin UI architecture; 2b. Two-surface apps (one bundle in wp-admin and in a shortcode); 3. Styling methodology; 4. Design tokens; 5. Data layer & background jobs; 6. Frontend build tooling; 7. Common frontend libraries; 8. Security baseline; 9. Accessibility; 10. Testing discipline; 11. Monorepo (if building multiple related products); 12. Source in the zip; Licensing note (ties into `references/i18n-distribution.md`).

`references/admin-ui.md` covers two tiers: native wp-admin (Settings
API / `WP_List_Table`) as the default, and `@wordpress/components` +
`wp.element` for a single screen that needs real interactivity. This
file is the **third tier**, for the case neither of those fits: an
admin experience that is genuinely **app-like** — multiple interactive
screens, real-time state, data tables, multi-step flows — where hand-
written CSS naming discipline and a single-screen React escalation
both stop being the bottleneck, and component-based architecture with
its own build pipeline becomes the more scalable unit of reuse.

## Dependency policy — always install latest from the official registry

Every dependency in this tier (Section 5's data layer, Section 6's
Bun tooling, Section 7's library table, including `@shadcn/lint`) is
installed at build time via `bun add` (or `npm install` if Bun isn't
available) against the package's **official registry** — npmjs.com
for everything in Section 7's table, and the WordPress-maintained
`@wordpress/*` scope on npm for the translation bridge. Do not pin an
old version number in a template, code sample, or generated
`package.json` in this skill or in a scaffolded plugin — resolve to
whatever `latest` (or the package's default tag) currently is at
scaffold time. This mirrors the reasoning behind not bundling the
Atomic Framework (`references/frontend-output.md`): a version
baked into this skill goes stale the moment the upstream project
ships a release, and a plugin generated today should get today's
patched, current dependency tree, not whatever was current when this
reference file was last written. The one exception is a genuine
compatibility ceiling the user has explicitly stated (e.g. "this site
still needs React 17") — pin only when told to, and note why in the
generated `package.json`'s comments or README, not silently.

**Reproducible builds (WordPress.org requires buildable source):** "latest" applies at scaffold time only. Right after resolving, commit the lockfile and record the resolved versions in the README. Later installs use the lockfile; upgrades are deliberate.

**CI line (every Tier 3 plugin):** CI runs `@shadcn/lint` (Section 3), ESLint, axe accessibility checks (Section 9), the test suite (Section 10), and `bun audit`, from the committed lockfile. Any failure blocks the build.

## Decision checklist — confirm before choosing this tier

Don't reach for this tier by default. Run the request against these;
if it's mostly single-screen or mostly static, Tier 1 or Tier 2
already covers it more cheaply (no build step, reuses WordPress's own
React runtime). Choose Tier 3 only when the admin UI genuinely has:

- Multiple interactive screens with their own internal navigation
  (not just several `add_submenu_page()` entries, but a connected app
  a user moves through)
- Real-time or frequently-changing state shared across components
- Data tables with client-side filtering/sorting/pagination beyond
  what `WP_List_Table` reasonably handles
- A multi-step flow (wizard, onboarding, configuration builder) with
  state carried between steps
- Enough total screens/components that Tailwind utility repetition
  and prop-drilling would already be a maintenance problem without a
  proper data layer and component library

As with the Alpine.js front-end tier in `references/frontend-output.md`, don't infer this silently — name which criterion above
triggered it and confirm with the user before scaffolding, since it
adds a real build step and a larger dependency surface that Tier 1
and Tier 2 don't carry.

## 1. Plugin foundation (unchanged)

This tier only changes the **admin UI layer**. Everything in
`references/architecture.md` and `fswpdevops-security` (`references/security.md`) still applies exactly as written: bootstrap/lifecycle
hooks, WPCS security baseline (capability checks, nonces,
`$wpdb->prepare()`, `permission_callback` on every REST route), and
`dbDelta()` schema versioning for any custom tables. This tier does
not relax any of that — it only changes how the admin screens are
built and how they talk to the backend.

## 2. Admin UI architecture

- **One React SPA (TypeScript), mounted at a single top-level
  wp-admin page**, not scattered across multiple native PHP-rendered
  submenu pages. Internal routing happens inside the SPA.
- Communicates only through a **clean, versioned JSON REST API**
  (`/wp-json/{plugin-slug}/v1/...`) — see `references/rest-cron.md` for the route/permission-callback pattern this still
  builds on. Breaking changes bump the version; never modify a
  version in place once anything depends on it.
- Document routes inline via `register_rest_route()`'s own
  `args`/schema registration — doubles as validation and
  documentation, no separate spec to maintain.
- The frontend never assumes WordPress-specific globals or markup —
  it only ever talks to the REST contract. This keeps the frontend
  portable if the plugin ever needs a non-WordPress surface later.
- **Exception, kept deliberately native even within this tier:**
  screens that are purely WordPress-specific plumbing — license/
  activation, basic settings with no real interactivity — stay plain
  wp-admin PHP (Tier 1: Settings API, `WP_List_Table`, Dashicons),
  not folded into the SPA. Forcing every screen into the app just to
  be consistent adds cost without benefit for screens this simple.

## 2b. Two-surface apps (one bundle in wp-admin and in a shortcode)

- Mount the same bundle in both places. On the front end, mount inside a **Shadow DOM** root so site CSS cannot leak in and app CSS cannot leak out.
- Tailwind preflight must be scoped to the app: do not let it reset the host page. Load the compiled CSS as a **constructable stylesheet** (`adoptedStyleSheets`) on the shadow root; wp-admin can use the normal enqueue.
- Radix portals render to `document.body` by default, outside the shadow root and unstyled. Pass the `container` prop (shadow root element) to every Portal (Dialog, Select, DropdownMenu, Tooltip, and the rest).
- Units in the shadow root follow `frontend-output.md` (rem on the host's 16px root; never override root font size).
- **Overlay test (required):** a test that opens each overlay type on both surfaces and asserts computed styles (background, font, z-index) are applied.

## 3. Styling methodology

**Tailwind CSS utility classes directly in JSX. No BEM, no custom
semantic class-naming system, and no Atomic Framework classes from
the front-end tiers** — this admin app is a separate styling context.

Why this isn't just a preference swap: BEM exists to solve a specific
problem — in hand-authored, cascade-heavy CSS with no natural
boundaries, you need `.block__element--modifier` discipline to
prevent specificity collisions across a flat, ever-growing
stylesheet. A component-based framework doesn't have that problem in
the first place. The component itself is the scoping mechanism — a
`<SettingsPanel>` component already encapsulates what a BEM block
name would otherwise need to signal — and Tailwind's utilities live
directly in the markup they style, never in a separate cascading
stylesheet that needs a naming system to stay organized. Layering BEM
on top reintroduces the exact overhead (a parallel naming decision
for everything, plus specificity concerns) without a real collision
risk to justify it.

When a utility combination repeats enough to extract, extract a
**component**, not a named CSS class — that's the React-world
equivalent of what BEM extraction would otherwise do.

**Linting:** [`@shadcn/lint`](https://github.com/shadcn-ui/lint)
(package name `@shadcn/lint`, install with `bun add -D @shadcn/lint`
from npm — always latest, per the dependency policy above) is an
agent-first linter for **Tailwind design systems generally**. It does
**not** require shadcn/ui — the shadcn/ui component library itself is
not part of this stack (this stack's own components, per Section 7,
are the ones you build); `@shadcn/lint` is included here purely as a
linting tool for the Tailwind utility classes those components use.
What it actually does: you write rules (e.g. `shadcn/no-restyle`)
declaring which Tailwind utility classes are allowed on which of
*your own* components — for instance, that a `<Button>` owns its own
padding and may only receive layout classes like margin or width from
a caller. When an agent (or a human) writes `<Button className="p-4">`,
the lint error explains the violation using that component's own
variants and suggests the compliant fix (use a `size` prop, or move
the spacing to the parent). Requires a Tailwind v4 project and runs
under either ESLint or Oxlint.

**Whether it applies to a given plugin build:** yes, whenever this
tier's admin app uses Tailwind (Section 3 above) — it's a general
Tailwind-contract linter, not a shadcn/ui-specific one, so it applies
to the plain Tailwind components this stack builds without pulling in
shadcn/ui as a dependency. Run it in CI alongside the accessibility
check in Section 9. Treat a failing run the same as any other CI
gate: fix before merge, not after.

## 4. Design tokens

One token definition file (JSON/JS) as the single source of truth,
compiled to:
- CSS custom properties for runtime theming (light/dark mode, brand
  color swaps without a rebuild)
- The Tailwind config consumed by the build

No color, spacing, or typography value hand-duplicated in more than
one place. This is a separate token file from the Atomic Framework's
own `afw-tokens.css` (user-supplied per `references/frontend-output.md`, not bundled with this skill) — the admin app and the
public-facing output are different styling contexts and don't share a
token source, even if the visual language is meant to feel related.

## 5. Data layer & background jobs

| Need | Choice |
|---|---|
| Frontend data-fetching/caching | TanStack Query |
| Frontend state management | Zustand (lightweight — avoid Redux-level ceremony unless the plugin's state genuinely warrants it) |
| Background jobs / scheduled tasks | Action Scheduler — the de facto WordPress-ecosystem standard (what WooCommerce itself runs on), more reliable than hand-rolled `wp_schedule_event()` for anything beyond trivial timing. For simpler cron needs, `references/rest-cron.md`'s `wp_schedule_event()` pattern is still fine. |
| Outbound HTTP calls | WordPress core's own `wp_remote_post()`/`wp_remote_get()` — don't add Guzzle or another HTTP client, the core API already covers this |

## 6. Frontend build tooling

**Bun** for package management, bundling, and the dev server —
frontend only. This never extends to the backend: the plugin's PHP
core is the runtime that has to work on arbitrary shared hosting, and
that constraint doesn't change based on frontend tooling choice. This
is the one context in this skill (alongside Tier 2's `@wordpress/
scripts` build) where a build step is acceptable — commit the
compiled output, not the build tooling's runtime footprint, into what
ships to the site.

## 7. Common frontend libraries

| Need | Library | License |
|---|---|---|
| Headless primitives (Dialog, Select, DropdownMenu, Tabs, Tooltip) | Radix UI primitives (`@radix-ui/react-*`); shadcn/ui itself is not used | MIT |
| Forms and validation | `react-hook-form` + `zod` | MIT |
| Drag-and-drop | `dnd-kit` | MIT |
| Virtualized long lists | TanStack Virtual | MIT |
| Date/time handling | `date-fns` | MIT |
| Markdown/code editing | CodeMirror | MIT |
| Markdown rendering | `react-markdown` | MIT |
| Translation bridge (React strings → WP i18n) | `@wordpress/i18n` | GPL2 |
| Native wp-admin components (for the deliberately-native screens, Section 2) | `@wordpress/components` | GPL2 |

Check this table before adding a new dependency for something already
covered here — the same discipline `references/i18n-distribution.md` expects everywhere else in this skill.

## 8. Security baseline

Beyond Section 1 (unchanged from `fswpdevops-security` (`references/security.md`)), for any plugin storing sensitive data (API keys,
tokens, credentials) through this tier's admin app:

- Encryption at rest via PHP's native `sodium` extension — bundled
  with PHP core (7.2+), no third-party dependency needed.
- TLS/HTTPS enforced on every outbound call, not just inbound REST
  requests.
- API keys and sensitive content never written to logs, including
  error/debug logs — a separate hygiene rule from encryption-at-rest,
  which only covers storage.
- Continuous dependency auditing (`composer audit` / `npm audit` or
  `bun audit`) on every build, not a one-time check.
- A published vulnerability disclosure policy (`security.txt`, a real
  reporting channel) for any plugin handling production sites at this
  scale.

## 9. Accessibility

**Target: WCAG 2.2 Level AA**, applied to the entire custom admin UI
built under this tier, not just the parts that feel public-facing.

- Automated accessibility testing in CI (`axe-core` or equivalent) on
  every build, alongside `@shadcn/lint` from Section 3.
- A manual pass before release — automated tooling catches roughly a
  third of real issues; keyboard-only navigation, screen reader
  testing, and color-contrast verification need a human.
- Full keyboard operability everywhere, including a non-drag
  alternative wherever drag-and-drop (Section 7) is used.

## 10. Testing discipline

For any plugin with logic where a silent bug would be genuinely
damaging (data integrity, payment handling, destructive operations):
define the concrete test scenarios for that logic explicitly, in
writing, and treat passing them as a gating requirement before
release — not an aspiration checked "when there's time." A vague
"needs test coverage" note doesn't give anyone something to actually
build against; a numbered list of specific scenarios does. This
applies equally whether the logic lives in PHP or in this tier's
React app.

**Default tooling:** `bun test` for units, Playwright for end-to-end and the overlay test (Section 2b), axe for accessibility inside Playwright. jsdom stays the option for plain-JS (vanilla and Alpine) tiers where a full browser is overkill. Gate delivery on the PRD's numbered scenarios (`fswpdevops-architect`).

## 11. Monorepo (if building multiple related products)

If a plugin using this tier is one of several related products (a
companion app, a browser extension, a future standalone product), a
monorepo (TurboRepo or similar) sharing packages — API client
patterns, UI components, design tokens — avoids duplicating code
across them. This is a **development-level** convenience only: each
product still gets its own independent backend, database, and
deployment. Sharing a build tool is not the same as sharing runtime
infrastructure, and conflating the two creates unnecessary coupling
between products that should stay independently deployable.

## 12. Source in the zip

Compiled output ships with its source: `src/`, `package.json`, and the lockfile go in the zip, and `readme.txt` gets a "Source" section stating where the source is, the build command (`bun install --frozen-lockfile && bun run build`), and the tool versions used. Excludes: `node_modules`, tests, `.git`.

## Licensing note (ties into `references/i18n-distribution.md`)

Any PHP hooking into WordPress core is a derivative work of WordPress
itself (GPLv2-or-later) regardless of which admin tier is used. For
this tier's own frontend dependencies specifically:

- Preferred everywhere outside the plugin's own WordPress-hooked
  core: MIT, Apache-2.0, BSD (everything in Section 7's table is MIT
  except the two `@wordpress/*` packages, which are GPL2 and expected
  since that layer is GPL by requirement already).
- Never used, anywhere: AGPL — its network-use clause can force
  open-sourcing of code that merely uses it over a network.
- Avoided as a dependency outside the WordPress-hooked core: other
  GPL-licensed libraries — pulling one in pressures that component
  toward GPL too.

For a plugin distributed with a paid tier, see `references/i18n-distribution.md`'s distribution-target guidance — the protection
model is access control (gated downloads, a license-key API), not
proprietary code, and that doesn't change based on which admin tier
was used to build it.
