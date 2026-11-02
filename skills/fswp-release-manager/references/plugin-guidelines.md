# Plugin directory guidelines (18), in plain language

Source: Detailed Plugin Guidelines, checked 2026-09-28. Violations can lead to a plugin or its data being removed; repeat violations can lead to a ban. Questions go to the plugins team at plugins@wordpress.org.

| # | Guideline | What it means for you |
|---|---|---|
| 1 | GPL-compatible | All code, data, and images in the plugin; "GPLv2 or later" recommended; third-party parts must be compatible |
| 2 | Developers are responsible | You answer for every file's contents and license, and must follow the terms of any service or API you use. No circumventing guidelines or restoring removed code |
| 3 | A stable version is available in the directory | Users download from the directory; do not distribute elsewhere while leaving the directory copy stale |
| 4 | Code is mostly human readable | No obfuscation or unclear naming; compiled or minified code needs public, maintained source and build tools, either in the package or linked in the readme |
| 5 | No trialware | No features locked, quota-limited, or expiring inside the plugin; sandbox-only API access counts as a trial. Paid services are fine when all plugin code is present; upsells are fine within guideline 11 |
| 6 | Software as a Service is allowed | The service must provide real functionality and be clearly documented in the readme (link Terms of Use). Not allowed: services that only validate licenses while everything runs locally, moving arbitrary code to a server to fake a service, storefront-only plugins |
| 7 | No tracking without consent | No contact with external servers without explicit opt-in; document data collection in the readme. Examples of prohibited: automatic data collection, misleading users into submitting data, offloading unrelated assets, undocumented use of external data, tracking ad mechanisms. Services are covered by the consent users give when they register and configure them |
| 8 | No executable code from third-party systems | Do not install or update plugins or themes from other servers, install premium versions of the same plugin, call CDNs except for fonts (all non-service JS and CSS ships locally), use remote lists without permission, or connect admin pages through iframes |
| 9 | Nothing illegal, dishonest, or morally offensive | Includes keyword stuffing and black-hat SEO, promising traffic, buying or pressuring reviews, sockpuppets, copying others' plugins as original, implying legal compliance guarantees, using server resources without permission (botnets, mining), code-of-conduct violations, falsifying identity |
| 10 | No external links or credits on the public site without permission | "Powered by" credits must be optional and off by default, with a clear opt-in; the plugin cannot require credits to function |
| 11 | Do not hijack the admin dashboard | Keep upgrade prompts and notices few, contextual, and dismissible (or self-dismissing); errors explain the fix; avoid ads in the dashboard; own-site and social links are fine |
| 12 | Readmes must not spam | No unnecessary affiliate links (disclose and link directly, no cloaking), competitor tags, more than 5 tags, keyword stuffing; write for people |
| 13 | Use WordPress's default libraries | Do not bundle your own jQuery, PHPMailer, SimplePie, etc.; use the versions WordPress ships |
| 14 | Avoid frequent commits | The repository is for releases; every commit rebuilds the zip; use clear commit messages; exception: readme-only updates declaring support for the latest WordPress |
| 15 | Increment the version for every release | Users are alerted to updates only when the version increases; trunk readme must show the current version |
| 16 | A complete plugin at submission | Names cannot be reserved; unused approved names can be reassigned |
| 17 | Respect trademarks, copyrights, and project names | Do not begin a slug or name with someone else's brand unless you can prove you represent it; use "for Brand" phrasing |
| 18 | The directory may act to maintain it | Guidelines can change; plugins can be disabled or changed in the interest of public safety |

## Pre-submission pass

1. Walk the table above against the package, one row at a time; write PASS / FAIL / NOT RUN.
2. Run the Plugin Check tool in a real WordPress and fix what it reports.
3. Read the readme as a stranger: does it describe external services, data sent, and what is stored?
4. Confirm the slug is original and not another brand's first word.
