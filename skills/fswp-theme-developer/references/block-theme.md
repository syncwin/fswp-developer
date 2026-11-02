# Block theme notes

## Layout of a block theme

```
theme-slug/
  style.css            header comment only (Theme Name, Version, Requires at least, Requires PHP, License, Text Domain)
  theme.json           version, settings, styles, customTemplates, templateParts
  functions.php        optional; enqueue extras, register pattern categories, keep it short
  templates/           index.html required; add single.html, page.html, archive.html, search.html, 404.html, front-page.html
  parts/               header.html, footer.html, sidebar.html
  patterns/            *.php pattern files with a header comment
  styles/              *.json style variations
  assets/              fonts, images, css/js the theme owns
```

## theme.json guidance

- Add `"$schema"` for editor validation and set `"version"` to the current documented schema version.
- `settings.color.palette`, `settings.typography.fontSizes` (fluid sizes where suitable), `settings.spacing.spacingSizes`, `settings.layout.contentSize` and `wideSize`.
- Fonts: `settings.typography.fontFamilies[].fontFace[]` with `src` pointing to bundled files (`file:./assets/fonts/name.woff2`). Never load fonts from a CDN.
- Turn off what you do not support (custom colors, gradients, drop caps) so editors stay on-brand; do not disable accessibility-relevant features without a reason.
- Element styles (`styles.elements.link`, `button`, `heading`) and block styles (`styles.blocks["core/query"]`) beat custom CSS. Use `style.css` or an extra stylesheet only for what `theme.json` cannot express.
- Custom templates and template parts must be declared so the editor lists them.

## Templates and parts

- Templates are block markup in `.html` files. Use `<!-- wp:template-part {"slug":"header","tagName":"header"} /-->` for shared parts and `wp:query` with `wp:post-template` for loops.
- Give templates real landmarks (`header`, `main`, `footer`) and exactly one `h1` per page context.
- Test every template with empty content, very long titles, and no featured image.

## Patterns

- One file per pattern in `patterns/`. The header comment supplies Title and Slug (`theme-slug/pattern-name`); Categories must exist (register your own with `register_block_pattern_category`).
- Use translated strings inside pattern PHP (`esc_html_e`) and theme presets (`var(--wp--preset--color--primary)`) instead of hard-coded values.
- Remove core patterns you do not want with `remove_theme_support( 'core-block-patterns' )`.

## Testing

Open the Site Editor, edit and save a template, confirm the front end matches, then reset customizations. Switch to a default theme and back to check nothing fatals. Run `fswp-qa-engineer`.
