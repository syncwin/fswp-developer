# Contributing

Questions and proposals: **support@syncwin.com**.

- By submitting a contribution you confirm you wrote it or have the right to submit it, and you license it under the MIT License in `LICENSE`.
- Write your own text and code. Do not paste in third-party skills, documentation text, or code; link to official sources instead and add a line to `CREDITS.md` if an outside project shaped the idea.
- Keep each `SKILL.md` under 500 lines; move detail into `references/`.
- Update the skill's `CHANGELOG.md` and the root `CHANGELOG.md`; bump versions together (semantic versioning: breaking = major, new capability = minor, wording = patch).
- Run `python3 skills/fswp-qa-engineer/scripts/qa_check.py <a-plugin>` or `theme_check.py <a-theme> [--directory]` against any script change, and `bash skills/fswp-qa-engineer/scripts/run_gate.sh` where PHP is available.
- GitHub workflows and integrations are reserved; see `skills/fswp-developer/references/github-foundation.md` before proposing any.
