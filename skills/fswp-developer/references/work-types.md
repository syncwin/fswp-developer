# Work types

Every request is one of six shapes. Pick the shape first; it decides how `fswp-architect` triages, which build skill runs, and what `fswp-qa-engineer` must prove.

| Shape | Starting point | Plan produces | Extra verify focus |
|---|---|---|---|
| New plugin | Nothing | PRD | Activation, uninstall, security baseline |
| New theme | Nothing | PRD (theme variant) | Template hierarchy, theme.json validity, accessibility, escaping in templates |
| Update | Existing plugin/theme code | Change brief with a parity list | Nothing that worked before breaks; upgrade path from stored data |
| Add-on | Someone else's product (host) | Change brief with a host-compatibility table | Host version range, graceful behavior when the host is missing or inactive |
| Core patch | WordPress source checkout | Ticket-first brief | Core test suite, coding standards, backward compatibility |
| Review only | Any code | None | None; go to `fswp-reviewer` |

## Rules that hold for all shapes

- Do not start writing code before the plan's approval gate (the user may explicitly waive it).
- On Update and Add-on work the existing code is the spec. Read it before proposing structure, and follow its conventions unless they are unsafe.
- A theme and a plugin serve different jobs. Presentation (templates, styles, block settings) belongs in a theme; features that must survive a theme switch (post types, integrations, business logic) belong in a plugin. If a request mixes them, say where each part goes and why.
- Mixed requests are split into ordered pieces (for example: a plugin for the data plus a theme for the display), each going through the sequence.
