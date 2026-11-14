---
name: fswpdevops-core
description: Use when contributing a WordPress Core patch with Full-Stack WP DevOps. WordPress Core contribution stage of Full-Stack WP DevOps. Guides a contributor through finding or filing a Trac ticket, setting up the wordpress-develop checkout and test environment, writing a patch or GitHub pull request that follows Core coding standards, inline documentation, backward compatibility and tests, and preparing the ticket comment; also routes block-editor changes to the Gutenberg repository and security reports to the private process. Invoked by fswpdevops for Core patches; use directly for Core workflow questions.
---

# FSWPDevOps Core Contributor

Workflow facts here were checked against the Core Contributor Handbook on 2026-09-28. Core processes change; confirm anything time-sensitive in `fswpdevops/references/official-docs.md` before advising. Nothing here submits anything: the user files tickets and opens pull requests themselves (GitHub automation is reserved, see `fswpdevops/references/github-foundation.md`).

## Route the change first

| The change is in... | Goes to |
|---|---|
| A vulnerability | The private security process linked from the Core handbook. Never a public ticket or PR. Stop and say so. |
| PHP, admin screens, APIs, tests, most Core code | Trac ticket plus patch or pull request against `WordPress/wordpress-develop` (this skill) |
| The block editor (Gutenberg packages, editor UI, Site Editor) | Issues and pull requests on `WordPress/gutenberg`; Core receives updates from there. Read that repository's contributing guide. |
| A plugin or theme bug | Not Core; use `fswpdevops-maintain` and report to that project |
| Docs | The relevant handbook's docs team process |

## Ticket first

1. Search Trac (https://core.trac.wordpress.org/) for the symptom. Read the ticket history and any patches.
2. If no ticket exists, draft one: precise title, WordPress/PHP versions, steps to reproduce, expected vs actual, and why it is a defect (a bug) versus an enhancement. The user files it under the right component.
3. Note workflow keywords on the ticket (for example a request for unit tests) and follow them.

## Environment

Use the development checkout, not a normal site:

1. Clone `WordPress/wordpress-develop` (Git mirror of the canonical repository, which is managed in Subversion).
2. Docker and Node are needed for the standard workflow. From the checkout root: `npm install`, `npm run build:dev`, `npm run env:start`, `npm run env:install`.
3. Run the PHP tests with `npm run test:php`. Pass PHPUnit arguments after a double dash, for example `-- --group formatting`. Tests tagged `@ticket` run by ticket number as a group. Multisite has its own config (`-c tests/phpunit/multisite.xml`); AJAX tests run with `--group ajax`.
4. Non-Docker workflows (Composer, PHPUnit PHAR) exist; see the PHPUnit page in the handbook.

## Writing the change

- Branch from trunk; name the branch with the ticket number (for example `12345-short-description`). Keep the change focused on one ticket.
- **Coding standards:** WordPress PHP, JS, CSS, and HTML standards, including Yoda conditions, tabs, spacing, and escaping/sanitizing rules. Run PHPCS on changed files.
- **Inline documentation:** PHPDoc for new or changed functions, hooks, and classes in Core's style, with `@since` set to the version the ticket's milestone names.
- **Backward compatibility:** Core almost never breaks public behavior. Deprecate (`_deprecated_function()` and friends) rather than remove; keep filters and actions stable; preserve function signatures.
- **Tests:** add or update PHPUnit tests that fail before and pass after, tagged with `@ticket`. A bug patch without a test is usually asked to add one.
- **Security and performance:** same rules as any WordPress code (`fswpdevops-security`, `fswpdevops-performance`), held to a higher bar.
- Do not bundle unrelated formatting or refactoring.

## Submitting (done by the user)

- Attach a `.diff` file to the Trac ticket named after the ticket number, or open a pull request against `WordPress/wordpress-develop` that references the ticket. Pull requests are used for review; they are not merged on GitHub, because committers commit through the canonical repository.
- Post a ticket comment: what the patch does, how you tested it, steps a tester can follow, and any open questions. Draft it for the user using `references/ticket-comment-template.md`.
- Expect review, requests for changes, and a slow cycle. Respond on the ticket, update the patch, and keep it rebased on trunk.

## Verify before handing over

Run `fswpdevops-qa` with the Core checklist: reproduction fails before and passes after, the relevant test group passes, coding standards are clean on changed lines, docs are present, and BC is intact.

Finish with a scratchpad: ticket, patch path, tests run, open items.
