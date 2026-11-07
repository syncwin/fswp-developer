# WordPress design language (designer)

Mechanics: `fswpdevops-theme` (theme.json structure, templates) and `fswpdevops-block`. This file adds the designer's decisions.

## theme.json tokens
- One source: `settings.color.palette`, `typography.fontSizes` and `fontFamilies`, `spacing.spacingSizes`, `layout` (content and wide size), shadow and border presets, and `styles` for elements and blocks.
- Palette by role slug (base, contrast, accent), not by hue name; prove contrast for every text-on-background pair in each style variation.
- Type scale on a fixed ratio with fluid sizes where useful; spacing on a step scale.
- No hard-coded colours, sizes or fonts in templates, patterns or CSS: use presets (`var(--wp--preset--*)`).
- Style variations for alternate palettes or type; each variation re-proves contrast.
- Custom CSS only for what theme.json cannot express; note the gap.

## Block patterns
- Reusable sections (hero, feature grid, call to action, footer) registered as patterns with a clear name, category and keywords; realistic placeholder text.
- Compose from core blocks and presets; no fixed pixel widths; lock what an editor must not change.
- Template parts for header and footer; one pattern per job.

## Existing sites
Mirror the site's tokens, spacing and tone. Propose changes as plan lines, never silently restyle. Plugin output on the front end inherits the theme's presets.

## Admin UI
Core components and notices, Settings API screens, WordPress colours and spacing; one primary button; accessible messages through `wp.a11y.speak`.

## Evidence
Render the key templates and patterns at three widths (about 375, 768, 1280), in each style variation, with 200% zoom and keyboard-only passes. Record screenshot paths with viewport and variation. A step the environment cannot run is NOT RUN with the command to run it (Playwright or browser devtools). The independent judgement pass is `fswpdevops-critic`.
