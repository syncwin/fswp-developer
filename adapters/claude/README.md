# Full-Stack WP DevOps (Claude plugin)

Plans, builds, updates, verifies, reviews and releases WordPress themes, plugins, add-ons and Core patches. It works in Claude Code, Cowork and the desktop app.

## Install

```
/plugin marketplace add syncwin/fswpdevops
/plugin install fswpdevops@syncwin-fswpdevops
```

## Use

Then type `/fswpdevops` or ask to build, fix, test, review or release WordPress code. The `fswpdevops` skill is the router: it picks a skill from its routing table and sequences plan, build, QA gate, critique, independent review and release.

The plugin is text only: no hooks, scripts or Python. What used to be scripts are recipes Claude follows with Read, Glob, Grep and Bash:

| Recipe | Where |
|---|---|
| Detect the WordPress project | `skills/fswpdevops-plan/references/detect_wp_project.md` |
| Scaffold a plugin (with its template files) | `skills/fswpdevops-plugin/references/scaffold_plugin.md`, `templates-*.md` |
| Scaffold a theme | `skills/fswpdevops-theme/references/scaffold_theme.md`, `scaffold_theme_files.md` |
| Plugin house-rules check | `skills/fswpdevops-qa/references/qa_check.md` |
| Theme house-rules check | `skills/fswpdevops-qa/references/theme_check.md` |
| Documentation gate | `skills/fswpdevops-qa/references/docs_gate.md` |
| Full QA gate | `skills/fswpdevops-qa/references/run_gate.md` |
| Install the pinned PHP QA toolchain | `skills/fswpdevops-qa/references/setup_toolchain.md` |

## Skills

`fswpdevops` (router), `fswpdevops-plan`, `fswpdevops-plugin`, `fswpdevops-theme`, `fswpdevops-maintain`, `fswpdevops-core`, `fswpdevops-qa`, `fswpdevops-design`, `fswpdevops-critic`, `fswpdevops-review`, `fswpdevops-release`, `fswpdevops-security`, `fswpdevops-api`, `fswpdevops-block`, `fswpdevops-performance`, `fswpdevops-ci`; agent `fswpdevops-code-review` (read-only reviewer).

See the root README for install and layout. Contact: see the author entry in `.claude-plugin/plugin.json`.
