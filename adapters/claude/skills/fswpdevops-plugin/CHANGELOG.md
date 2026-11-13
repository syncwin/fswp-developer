# Changelog — fswp-plugin-developer

## 0.3.0 — 2026-09-28

Author: @wasimness (SyncWin).

- Renamed from wp-build-plugin; cron example now uses a named prefixed callback instead of a closure (closures cannot be removed as hook callbacks).

## 0.4.0 — 2026-09-28

Author: @wasimness (SyncWin).

- Scaffold help text now uses a generic placeholder prefix (`acme`) instead of a fixed brand token, matching the ask-first prefix rule. The shared cross-plugin Alpine.js loader handle is now `fswp-alpine-loader` (a fixed, tool-owned constant, not a per-project brand). "SWWP design system" references renamed to their real name, the Atomic Framework. Also updated for the plugin-wide rename (plugin slug and router skill unified as `fswp-developer`, single `/fswp` trigger, author identity `@wasimness`).
