#!/usr/bin/env python3
"""Documentation gate for WordPress plugins and themes. Standard library only.

Usage: python docs_gate.py <dir> [--base REF] [--static]
Checks the documentation standard (fswpdevops/references/coding-standards.md, "Documentation standard"):
  static: README.md, docs/{setup,architecture,ops}.md, CHANGELOG.md format, docs/features/ index and files.
  diff:   code changed against the base without a CHANGELOG [Unreleased] entry, or without a changed
          feature file for the touched feature, FAILS. Base = --base, else origin/main, origin/master, main, master.
Prints PASS / FAIL / NOT RUN per check; exit 1 if any FAIL. NOT RUN (no git, no base) is never a pass.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

CATEGORIES = {"Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"}
STATUSES = {"planned", "beta", "stable", "deprecated"}
SECTIONS = ["Context", "Behaviour", "How it works", "UI", "Limits & known issues", "History"]
GENERIC = {"core", "shared", "common", "utils", "util", "l10n", "generated", "data", "domain", "presentation",
           "ui", "widgets", "theme", "models", "services", "helpers", "lib", "assets", "admin", "public"}
SEMVER = r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?"


# --- profile: what counts as code and how a path maps to a feature slug ---
SKIP_DIRS = {"vendor", "node_modules", "tests", "test", "languages", "build", "dist", "foundation", "docs", ".git"}
FEATURE_ROOTS = ("includes", "inc", "src", "modules", "features", "blocks")


def is_code(p):
    """Plugin or theme PHP, JS/TS under src/ or blocks/, and block-theme templates, parts and theme.json."""
    parts = p.split("/")
    if SKIP_DIRS & set(parts[:-1]) or p.endswith(".min.js"):
        return False
    if p.endswith(".php"):
        return True
    if p.endswith((".js", ".jsx", ".ts", ".tsx")):
        return "src" in parts[:-1] or "blocks" in parts[:-1]
    return p.endswith("theme.json") or (p.endswith(".html") and ("templates" in parts[:-1] or "parts" in parts[:-1]))


def feature_slug(p):
    """First folder under includes/, inc/, src/, modules/, features/ or blocks/: includes/<feature>/x.php -> <feature>."""
    parts = p.split("/")
    idx = [i for i, x in enumerate(parts[:-1]) if x in FEATURE_ROOTS]
    if not idx:
        return None
    rest = parts[idx[0] + 1:]
    return rest[0].lower().replace("_", "-") if len(rest) >= 2 else None
# --- end profile ---


def git(root, *args):
    try:
        p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=60)
        return p.returncode, p.stdout
    except (OSError, subprocess.TimeoutExpired):
        return 127, ""


def read(p):
    try:
        return Path(p).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def unreleased(text):
    m = re.search(r"^## \[Unreleased\][^\n]*\n(.*?)(?=^## \[|\Z)", text, re.M | re.S)
    return None if m is None else m.group(1)


def body_lines(section):
    return {l.strip() for l in section.splitlines() if l.strip() and not l.lstrip().startswith("#")}


def static_checks(root, add):
    for f in ("README.md", "docs/setup.md", "docs/architecture.md", "docs/ops.md"):
        ok = (root / f).is_file()
        add("PASS" if ok else "FAIL", f"exists: {f}", "" if ok else "missing")

    cl = read(root / "CHANGELOG.md")
    if cl is None:
        add("FAIL", "CHANGELOG.md format", "CHANGELOG.md missing")
    else:
        bad = []
        if unreleased(cl) is None:
            bad.append("no '## [Unreleased]' section")
        for m in re.finditer(r"^## (.+)$", cl, re.M):
            h = m.group(1).strip()
            if h.startswith("[Unreleased]"):
                continue
            if not re.fullmatch(r"\[" + SEMVER + r"\] - \d{4}-\d{2}-\d{2}(?: \[YANKED\])?", h):
                bad.append(f"bad version heading '## {h}' (want '## [X.Y.Z] - YYYY-MM-DD')")
        for m in re.finditer(r"^### (.+)$", cl, re.M):
            if m.group(1).strip() not in CATEGORIES:
                bad.append(f"bad category '### {m.group(1).strip()}'")
        add("FAIL" if bad else "PASS", "CHANGELOG.md format (Keep a Changelog 1.1.0)", "; ".join(bad[:3]))

    fdir = root / "docs" / "features"
    idx = read(fdir / "README.md")
    files = sorted(p for p in fdir.glob("*.md") if p.name != "README.md") if fdir.is_dir() else []
    rows = {}
    if idx is None:
        add("FAIL", "docs/features/README.md index", "missing")
    else:
        problems = []
        for line in idx.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if line.strip().startswith("|") and len(cells) == 4 and cells[0].lower() != "feature" \
                    and not set(cells[0]) <= set("-: "):
                m = re.search(r"([A-Za-z0-9._-]+\.md)", cells[3])
                if m:
                    rows[m.group(1)] = (cells[1], cells[2])
                else:
                    problems.append(f"row '{cells[0]}' has no file")
        for p in files:
            if p.name not in rows:
                problems.append(f"{p.name} not in index")
        for name in rows:
            if not (fdir / name).is_file():
                problems.append(f"index lists missing file {name}")
        if "| feature | status | since | file |" not in re.sub(r"\s+", " ", idx.lower()):
            problems.append("table header must be '| Feature | Status | Since | File |'")
        if any(ord(c) > 127 for c in idx):
            problems.append("non-ASCII text in index")
        add("FAIL" if problems else "PASS", "docs/features/README.md index current", "; ".join(problems[:4]))

    problems = []
    for p in files:
        t = read(p)
        if t is None:
            problems.append(f"{p.name} unreadable")
            continue
        if any(ord(c) > 127 for c in t):
            problems.append(f"{p.name}: non-ASCII text")
        m = re.search(r"^\*\*Status:\*\*\s*(\w+)\s*\|\s*\*\*Since:\*\*\s*(" + SEMVER + r")\s*\|\s*\*\*Updated:\*\*\s*("
                      + SEMVER + r")\s*$", t, re.M)
        if not m or m.group(1) not in STATUSES:
            problems.append(f"{p.name}: bad Status line")
        for s in SECTIONS:
            if not re.search(r"^## " + re.escape(s) + r"\s*$", t, re.M):
                problems.append(f"{p.name}: missing '## {s}'")
        if m:
            if p.name in rows and rows[p.name] != (m.group(1), m.group(2)):
                problems.append(f"{p.name}: index says {'/'.join(rows[p.name])}, file says {m.group(1)}/{m.group(2)}")
            if m.group(3) not in t.split("## History", 1)[-1]:
                problems.append(f"{p.name}: Updated {m.group(3)} has no History line")
            if m.group(1) != "planned" and "FILL IN:" in t:
                problems.append(f"{p.name}: unfilled 'FILL IN:' on a {m.group(1)} feature")
    add("FAIL" if problems else "PASS", f"docs/features/*.md valid ({len(files)} file(s))", "; ".join(problems[:4]))


def find_base(root, want):
    for ref in ([want] if want else ["origin/main", "origin/master", "main", "master"]):
        rc, _ = git(root, "rev-parse", "--verify", "-q", ref + "^{commit}")
        if rc == 0:
            rc, out = git(root, "merge-base", ref, "HEAD")
            if rc == 0 and out.strip():
                return ref, out.strip()
    return None, None


def diff_checks(root, add, want_base):
    rc, _ = git(root, "rev-parse", "--is-inside-work-tree")
    if rc != 0:
        add("NOT RUN", "diff checks", "not a git repository")
        return
    ref, mb = find_base(root, want_base)
    if not mb:
        add("NOT RUN", "diff checks", "no base branch found; pass --base <ref>")
        return
    _, a = git(root, "diff", "--name-only", "--relative", mb)
    _, b = git(root, "ls-files", "--others", "--exclude-standard")
    changed = sorted({l.strip().replace("\\", "/") for l in (a + b).splitlines() if l.strip()})
    code = [f for f in changed if is_code(f)]
    if not code:
        add("PASS", f"code changed vs {ref}", "no code changes: no changelog or feature entry needed")
        return

    new = read(root / "CHANGELOG.md") or ""
    _, old = git(root, "show", mb + ":./CHANGELOG.md")
    nu, ou = unreleased(new), unreleased(old)
    heads = lambda t: set(re.findall(r"^## \[(" + SEMVER + r")\]", t, re.M))
    name = "CHANGELOG [Unreleased] updated"
    if nu is None:
        add("FAIL", name, f"{len(code)} code file(s) changed; no [Unreleased] section")
    elif heads(new) - heads(old) and ou and body_lines(ou):
        add("PASS", name, "release: Unreleased moved into a version")
    elif body_lines(nu) - (body_lines(ou) if ou else set()):
        add("PASS", name, "new entry present")
    else:
        add("FAIL", name, f"{len(code)} code file(s) changed (e.g. {code[0]}); no new line under [Unreleased]")

    fdir = root / "docs" / "features"
    known = {p.stem for p in fdir.glob("*.md") if p.name != "README.md"} if fdir.is_dir() else set()
    slugs = {}
    for f in code:
        s = feature_slug(f)
        if s and s not in GENERIC:
            slugs.setdefault(s, []).append(f)
    name = "feature docs for touched features"
    if not slugs:
        add("PASS", name, "no feature-scoped code touched (shared code needs the changelog only)")
        return
    miss, stale, created = [], [], []
    for s, fs in sorted(slugs.items()):
        rel = f"docs/features/{s}.md"
        if not (root / rel).is_file():
            miss.append(f"{rel} (for {fs[0]})")
        elif rel not in changed:
            stale.append(f"{rel} (for {fs[0]})")
        elif git(root, "cat-file", "-e", mb + ":./" + rel)[0] != 0:
            created.append(rel)
    if miss or stale:
        add("FAIL", name, ("missing: " + ", ".join(miss) + "; " if miss else "")
            + ("unchanged: " + ", ".join(stale) if stale else ""))
    else:
        add("PASS", name, f"{len(slugs)} feature file(s) updated")
    if created and "docs/features/README.md" not in changed:
        add("FAIL", "docs/features index updated", "new feature file(s) " + ", ".join(created) + "; index unchanged")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--base")
    ap.add_argument("--static", action="store_true", help="skip the git diff checks")
    a = ap.parse_args()
    root = Path(a.dir).resolve()
    if not root.is_dir():
        sys.exit(f"Not a folder: {root}")
    rows = []
    add = lambda r, c, d="": rows.append((c, r, d))
    static_checks(root, add)
    if a.static:
        add("NOT RUN", "diff checks", "--static")
    else:
        diff_checks(root, add, a.base)
    print(f"{'Check':<50} {'Result':<8} Detail")
    for c, r, d in rows:
        print(f"{c:<50} {r:<8} {d}")
    return 1 if any(r == "FAIL" for _, r, _ in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
