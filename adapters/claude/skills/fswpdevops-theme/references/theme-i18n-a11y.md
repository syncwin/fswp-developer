# Theme i18n and accessibility

## Internationalization

- One text domain equal to the theme slug, declared in `style.css` and used in every call.
- PHP: `__()`, `_e()`, `_x()`, `_n()`, and the escaping forms `esc_html__()`, `esc_attr__()`. Never concatenate translatable sentences or put variables inside the string; use placeholders with `sprintf()` and add a translator comment.
- Block markup and patterns: strings in pattern PHP files go through the translation functions; HTML template files hold structure, not copy that needs translating (use patterns for copy).
- Load translations: block themes rely on core loading the theme's `languages/` folder; classic themes call `load_theme_textdomain()` on `after_setup_theme`.

## Accessibility (aim for WCAG 2.2 AA)

- Skip link to main content, visible focus on every interactive element, logical heading order, one `h1`.
- Landmarks: header, nav (labelled when more than one), main, footer.
- Color contrast checked for text, UI components, and focus indicators in every style variation.
- Every image has meaningful alt text or is marked decorative; icon-only buttons have accessible names.
- Navigation works by keyboard, including submenus; no keyboard traps; touch targets large enough.
- Respect `prefers-reduced-motion`; do not autoplay motion.
- Zoom to 200% and reflow at 320px width without horizontal scroll.
- If the target is the directory's accessibility-ready tag, read its requirements first (`fswpdevops-release`).
