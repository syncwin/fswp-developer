# Security policy

## Reporting a vulnerability in this plugin

The package contains instructions and helper scripts (`qa_check.py`, `theme_check.py`, `detect_wp_project.py`, `scaffold_plugin.py`, `scaffold_theme.py`, `setup_toolchain.sh`, `run_gate.sh`). If you find a flaw in one of them, or guidance that would steer generated code toward an insecure pattern, email **support@syncwin.com** with the subject "Security". Include the file, what you saw, and how to reproduce it. Please do not open a public issue first. Expect an acknowledgement, then a fix and a CHANGELOG entry.

## Vulnerabilities in WordPress itself

Do not report those here or in a public ticket. Use the private security process linked from the WordPress Core Contributor Handbook.

## What this plugin does not guarantee

The plugin plans, builds, verifies, and reviews WordPress code with an AI model. Its gate and review reduce risk; they do not prove code is secure, correct, or fit for your use. Read generated code before deploying it, test on staging, keep backups, and get a professional security review for anything handling payments, personal data, or authentication. A check that could not run is reported NOT RUN, never as a pass.
