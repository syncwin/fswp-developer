# GitHub foundation (reserved, not implemented)

GitHub integration is planned and deliberately not built yet. This file records the extension points so it can be added without restructuring. Until the owner adds it, do not call GitHub APIs, create repos, open issues or PRs, or claim any of this works.

## What exists now

- Repository hygiene for the plugin's own repo: `.gitignore`, `.gitattributes`, `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, `docs/github-integration.md`.
- Every stage already produces artifacts that map cleanly onto GitHub objects (below).

## Intended extension points

| Stage | Artifact today | Later maps to |
|---|---|---|
| `fswp-architect` | PRD or change brief | Issue body or GitHub Discussion |
| Build skills | Feature branch name convention `fswp/<type>-<slug>` in the plan | Branch |
| `fswp-qa-engineer` | PASS / FAIL / NOT RUN table | Check run or PR status comment |
| `fswp-reviewer` | Findings in the fixed format | PR review comments |
| `fswp-core-contributor` | Ticket-linked patch or PR text | PR to a fork of wordpress-develop, with the Trac ticket link |
| Deliver | Zip and summary | Release with attached zip, tag from plugin version |

## Rules for whoever implements it

- Ask before any write action (push, PR, release). Never force-push.
- Never store tokens in the repo; use the platform's connector or the user's credential store.
- Core work: WordPress accepts patches and reviews through Trac tickets; a GitHub PR to the mirror must reference the ticket and is not merged on GitHub.
- Add the connector as an optional tool in the router's Degradation section, so the plugin keeps working without it.
