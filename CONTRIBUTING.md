# Contributing

Questions and proposals: **support@syncwin.com**.

- By submitting a contribution you confirm you wrote it or have the right to submit it, and you license it under the MIT License in `LICENSE`.
- Write your own text and code. Do not paste in third-party skills, documentation text, or code; link to official sources instead and add a line to `CREDITS.md` if an outside project shaped the idea.
- The shipped plugin is text only: no hooks, scripts or non-text files under `adapters/claude`.
- Keep each `SKILL.md` under 500 lines; move detail into `references/`.
- Update the root `CHANGELOG.md` and copy it to `adapters/claude/CHANGELOG.md`; bump `version` in `adapters/claude/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` together (semantic versioning: breaking = major, new capability = minor, wording = patch).
- Keep each recipe in `adapters/claude/skills/*/references/` in step with its maintainer script in `dev/`; test script changes with `python dev/fswpdevops-qa/scripts/qa_check.py <a-plugin>`, `theme_check.py <a-theme> [--directory]`, `bash dev/fswpdevops-qa/scripts/run_gate.sh` where PHP is available, and a throwaway `scaffold_plugin.py` or `scaffold_theme.py` run.
- Run `claude plugin validate . --strict` before a pull request.
- GitHub workflows and integrations are reserved; see `adapters/claude/skills/fswpdevops/references/github-foundation.md` before proposing any.
