# Precedence

1. **Official WordPress documentation and coding standards** (`official-docs.md`). Ground truth. Nothing else overrides them.
2. **Domain skills** (`fswp-security-engineer`, `fswp-api-developer`, `fswp-block-developer`, `fswp-performance-engineer`, `fswp-devops-engineer`, `fswp-release-manager`). Own the general procedure in their domain.
3. **Build-skill house rules** (`fswp-plugin-developer`, `fswp-theme-developer`, `fswp-maintainer`). Add depth, templates, and stricter defaults.

A house rule may raise the bar and never lower it. When one is stricter than the official default, call it a house rule in the delivery summary so the user knows it is a SyncWin addition, not a WordPress requirement.

**Version drift.** WordPress moves quickly. Before relying on an API introduced recently, check the minimum WordPress and PHP versions in the docs and in the project's PRD. If the project's minimum is lower, guard the newer API and say so.

**Conflicts.** If two sources genuinely disagree, official docs decide. If still unresolved, follow the stricter one and flag the conflict to the user instead of silently choosing.
