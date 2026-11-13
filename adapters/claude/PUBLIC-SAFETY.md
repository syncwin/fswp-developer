# Public Safety

This repository is public. Only what is listed under "May be public" is published.

## May be public
- Source code, skills, recipes, maintainer script sources, and Markdown docs
- Documentation, README, CHANGELOG, LICENSE
- Generic examples with placeholder values, `.env.example` (variable names only)
- The plugin's public support address (in `plugin.json`), listed in `.public-safety-allow`

## Never published
- Secrets: API keys, tokens, passwords, private keys, `.env` files, credentials
- Personal data: personal e-mails, phone numbers, addresses
- Client names and data; internal URLs and hosts
- Local absolute user paths; private notes, logs, memory or progress files

## Where private values live instead
- None: the plugin needs no secrets. Signing keys, certificates and store credentials for apps the user builds stay in the user's own environment and are never written to a repository.

## Checks
- `python dev/aiaddon-review/scripts/scan_secrets.py . --history` (working tree plus full git history, run with the aiaddon checker scripts) before every release
- Allowed false positives: `.public-safety-allow`

## If something leaks
Rotate the credential first, then remove it from history. Never force-push without the owner's explicit OK.
