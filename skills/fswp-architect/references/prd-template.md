# PRD template

```markdown
# PRD: {{Plugin Name}}

## 1. Overview
One paragraph: what it does, who for, why now. Mode: New / Extend / Migration.

## 1a. Project information
Company name, product/plugin name, acronym, author, contributors, links (website/docs/support/repo/product page). Only what was stated — no invented values; state which are missing rather than guessing.

## 1b. Technology stack
New project or stack reconsidered: state the decision (admin-UI tier, JS tier) and why. Existing, unchanged project: state "unchanged from prior iteration" rather than re-deciding.

## 2. Goals / Non-goals
Non-goals say what v1 will NOT do.

## 3. Competitive scan
3-5 bullets: what leaders do well, what they get wrong, conventions to match.

## 4. Features
Must-have (v1) / Deferred / Out of scope.

## 5. Data model
CPTs, taxonomies, tables, stored options, with fields. Stored user data carries a schemaVersion (fswp-security-engineer references/security.md section 10). Empty if none.

## 6. API surface
REST routes: method, path, purpose, auth level, size cap. Any __return_true route named with its justification. Empty if none.

## 7. Admin experience
Screens; Settings API vs @wordpress/components vs Tier 3 (with reasoning); what each screen does.

## 8. Front-end experience
What renders publicly; JS-tier checklist result and recommended tier.

## 9. Non-functional requirements
Inherited, not re-litigated: security baseline, i18n including JS strings, distribution-target requirements, unit policy (rem), accessibility (WCAG 1.4.4 for fluid type).

## 10. WordPress.org compliance (only when target is "both")
| Requirement | WordPress.org build | Private build | Difference |
|---|---|---|---|

## 11. Design fidelity and polish policy
Allowed: (e.g. spacing/token-level tweaks matching the design system). Not allowed: (e.g. new components, restyled atoms, unrequested animation).

## 12. Testing scenarios (numbered, gating)
T1..Tn: each with steps, expected result, and how it is verified. Includes: fresh install, deactivate/reactivate, update from a previous version's data without reactivating, uninstall cleanup, one per feature. Delivery is blocked until every scenario is PASS or explicitly NOT RUN with a reason.

## 13. Migration baseline and parity (Migration mode only)
Baseline location, parity matrix, export diffs, visual-regression tolerance.

## 14. Assumptions
Every inferred detail, named so it can be corrected in one pass.

## 15. Decisions log
| # | Decision | Reason | Date | Changed later? |
|---|---|---|---|---|

## 16. Build plan
bootstrap, lifecycle, security, domain, admin, front-end, i18n/distribution, gate, review, release.
```
