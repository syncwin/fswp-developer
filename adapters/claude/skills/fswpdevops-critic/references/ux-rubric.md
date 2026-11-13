# UX rubric (WordPress)

Judge against the plan's intent, the audience and the site's existing design language, not taste. Each finding: observation, evidence, why (heuristic, WCAG id, law), fix, severity.

## Heuristics (Nielsen, ten)
Visibility of system status; match to the real world; user control and undo; consistency and standards; error prevention; recognition over recall; flexibility and efficiency; minimalist design; error recovery in plain language; help.

## Visual design
One focal point per template; heading hierarchy follows content; type and spacing come from theme.json presets; alignment to the layout grid; colour by palette slug; density suited to content. Generic-template check: would it look the same with another brand name on it?

## Block editor UX
Patterns have clear names, categories and realistic placeholder content; controls an editor should not change are locked or removed; the editor view matches the front end; empty states in blocks explain the next step.

## Admin screens
Core components and patterns first (notices, tables, settings API screens); one primary button per screen; success and error notices announced; destructive actions confirmed; no custom look that fights wp-admin.

## Accessibility (WCAG 2.2 AA)
Contrast 4.5:1 text, 3:1 large text and UI parts; target at least 24 CSS px; focus visible and not obscured (2.4.11); no drag-only action (2.5.7); consistent help (3.2.6); no repeated entry (3.3.7); accessible authentication (3.3.8); reflow at 320 px and 200% zoom; reduced motion; skip link and landmarks; colour never the only signal.

## Performance as UX
Feedback within about 400 ms; Core Web Vitals lab targets (LCP 2.5 s, INP 200 ms, CLS 0.1) as input, not the verdict; reserved space for images and embeds.

## Laws of UX (explain, never generate)
Hick, Fitts, Jakob, Miller, proximity and common region, Von Restorff, Postel, Peak-End, Goal-gradient, Aesthetic-usability.

## Severity map (NN/g 0-4 to house labels)
4 = Critical; 3 = Important; 2 and 1 = Minor; 0 = not a problem. Weigh frequency, impact and persistence.

## Result vocabulary
PASS, FAIL, NOT RUN, NEEDS MANUAL EVIDENCE. Nothing is PASS without evidence.
