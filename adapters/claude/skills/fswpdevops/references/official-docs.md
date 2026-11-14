# Official documentation map

The source of truth for WordPress behavior. This plugin links to these pages instead of copying them, so answers stay current and documentation licensing stays out of the package. When a skill says "check the docs", start here. Use web search or fetch for anything newer than your knowledge, especially version requirements and recently added APIs.

Reachability: entries marked (checked) were fetched successfully on 2026-09-28 and their content was used to write or verify the skills named beside them. Others are the canonical paths as documented; confirm on first use, and search the site if one has moved.

## Handbooks

| Topic | URL |
|---|---|
| Developer hub | https://developer.wordpress.org/ |
| Plugin Handbook (checked) | https://developer.wordpress.org/plugins/ |
| Theme Handbook (checked) | https://developer.wordpress.org/themes/ |
| Block Editor Handbook | https://developer.wordpress.org/block-editor/ |
| REST API Handbook | https://developer.wordpress.org/rest-api/ |
| Common APIs (Options, Settings, HTTP, Transients, Database, and more) | https://developer.wordpress.org/apis/ |
| Advanced Administration (security, performance, multisite, debugging) | https://developer.wordpress.org/advanced-administration/ |
| Code Reference (functions, hooks, classes) | https://developer.wordpress.org/reference/ |
| Coding Standards index | https://developer.wordpress.org/coding-standards/ |
| PHP coding standards (checked; `fswpdevops/references/coding-standards.md`) | https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/ |
| JavaScript, CSS, HTML, inline documentation standards | https://developer.wordpress.org/coding-standards/wordpress-coding-standards/ (sub-pages: javascript, css, html; inline docs under /inline-documentation-standards/) |
| Command-line handbook | https://make.wordpress.org/cli/handbook/ |

## Themes

| Topic | URL |
|---|---|
| Block themes vs classic themes | https://developer.wordpress.org/themes/getting-started/ |
| Core concepts, template hierarchy | https://developer.wordpress.org/themes/core-concepts/ |
| Advanced topics (child themes, testing) | https://developer.wordpress.org/theme/advanced-topics/ (checked link from the handbook) |
| Releasing a theme | https://developer.wordpress.org/themes/releasing-your-theme/ |
| theme.json reference | https://developer.wordpress.org/block-editor/reference-guides/theme-json-reference/ |
| Theme review requirements (checked; `fswpdevops-release`) | https://make.wordpress.org/themes/handbook/review/required/ |
| style.css header (checked) | https://developer.wordpress.org/themes/classic-themes/basics/main-stylesheet-style-css/ |

## Plugins

| Topic | URL |
|---|---|
| Plugin basics, hooks, security, privacy (checked index) | https://developer.wordpress.org/plugins/ |
| Detailed plugin guidelines (checked) | https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/ |
| Plugin header requirements (checked) | https://developer.wordpress.org/plugins/plugin-basics/header-requirements/ |
| readme.txt standard (checked) | https://developer.wordpress.org/plugins/wordpress-org/how-your-readme-txt-works/ |
| Internationalization | https://developer.wordpress.org/plugins/internationalization/ |

## Blocks and APIs

| Topic | URL |
|---|---|
| block.json metadata (checked; `fswpdevops-block`) | https://developer.wordpress.org/block-editor/reference-guides/block-api/block-metadata/ |
| Interactivity API | https://developer.wordpress.org/block-editor/reference-guides/interactivity-api/ |
| @wordpress/env | https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/ |
| Playground | https://wordpress.github.io/wordpress-playground/ |
| Abilities API | Search developer.wordpress.org and make.wordpress.org/core for "Abilities API"; it is recent and paths change |

## Core contribution

| Topic | URL |
|---|---|
| Core Contributor Handbook (checked) | https://make.wordpress.org/core/handbook/ |
| Git workflow and patches (checked) | https://make.wordpress.org/core/handbook/contribute/git/ |
| GitHub pull requests for code review | https://make.wordpress.org/core/handbook/contribute/git/github-pull-requests-for-code-review/ |
| PHPUnit for Core (checked) | https://make.wordpress.org/core/handbook/testing/automated-testing/phpunit/ |
| PHPCS for Core | https://make.wordpress.org/core/handbook/testing/automated-testing/phpcs/ |
| Writing PHPUnit tests | https://make.wordpress.org/core/handbook/testing/automated-testing/writing-phpunit-tests/ |
| Trac (bug tracker) | https://core.trac.wordpress.org/ |
| Core source mirror | https://github.com/WordPress/wordpress-develop |
| Block editor source | https://github.com/WordPress/gutenberg |
| Core news and dev notes | https://make.wordpress.org/core/ |

## Accessibility and trademarks

| Topic | URL |
|---|---|
| Accessibility handbook | https://make.wordpress.org/accessibility/handbook/ |
| Trademark policy (checked) | https://wordpressfoundation.org/trademark-policy/ |

## Using these pages

The plugin summarizes these pages in its own words and links to them; page text is not pasted into generated files or the user's code comments. Code examples in the handbooks are for understanding, not for copying wholesale; the implementation is written for the user's requirements.
