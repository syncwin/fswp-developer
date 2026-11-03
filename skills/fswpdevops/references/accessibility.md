# Accessibility reference

Standards: WCAG 2.2 AA is the working target. WordPress Core follows WCAG 2.2 AA for new work; see the Accessibility handbook on make.wordpress.org for Core's rules (linked in `fswpdevops/references/official-docs.md`).

## Checklist by surface

**Every surface**
- Keyboard: all functions reachable and operable, no traps, logical order, visible focus (never `outline: none` without a replacement).
- Names, roles, states: native semantics first; ARIA only to fill gaps; keep `aria-expanded`, `aria-pressed`, `aria-selected`, `aria-current` accurate.
- Text alternatives: `alt` on images (empty when decorative); accessible names for icon buttons and links ("Read more" alone is not enough out of context).
- Contrast and color: 4.5:1 text, 3:1 large text and UI parts and focus indicators; information never by color alone.
- Structure: one `h1`, no skipped heading levels, landmarks (`header`, `nav`, `main`, `footer`), label repeated `nav`s.
- Motion and time: `prefers-reduced-motion`, pause controls for anything that moves more than five seconds, no flashing.
- Responsive: reflow to 320px wide, zoom to 200% and text resize without loss, adequate touch targets.

**Forms**
- `<label for>` or wrapping label for each control; group related controls with `fieldset`/`legend`.
- Required state in text, not just an asterisk color; errors in text, tied with `aria-describedby`, announced on submit.
- Autocomplete attributes for personal data fields.

**Admin screens (plugins)**
- Use core admin markup, classes, and Settings API patterns; they carry tested semantics.
- Announce dynamic changes with `wp.a11y.speak( message, 'polite' )`.
- Do not rely on color badges alone; add text.
- Tables: `<th scope>`; use `WP_List_Table` for lists.
- Modals: focus moves in, is trapped while open, returns on close, Escape closes.

**Front end (themes and blocks)**
- Skip link that becomes visible on focus and moves focus to main content.
- Menus operable by keyboard including submenus; `aria-current="page"` on the current item.
- Editor-provided content (headings, alt text) is not overridden by the theme.
- For themes tagged accessibility-ready, read and meet that tag's requirements before claiming it.

**Blocks**
- Editor UI uses `@wordpress/components`, which handles most keyboard and ARIA needs.
- Front-end interactivity (Interactivity API) keeps ARIA state bound to store state.

## Testing without special tools

1. Tab through the whole page/screen; every stop must be visible and meaningful.
2. Use it with the mouse unplugged, then at 200% zoom and 320px width.
3. Check contrast with a browser dev-tools checker.
4. Run an automated scanner (axe DevTools or Lighthouse); treat it as finding roughly a third of issues.
5. If possible, test once with a screen reader (NVDA on Windows, VoiceOver on macOS/iOS).

Report accessibility as PASS, FAIL, or NOT RUN in `fswpdevops-qa`; automated-only runs are labeled as such.
