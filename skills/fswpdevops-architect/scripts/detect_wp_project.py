#!/usr/bin/env python3
"""Read-only WordPress project detector. Standard library only.

Usage: detect_wp_project.py <path> [--json]

Reports what kind of WordPress project a folder is and what tooling and
extension points it has, so planning starts from facts. It never writes.
"""
import json
import os
import re
import sys

SKIP = {".git", "node_modules", "vendor", "build", "dist", ".cache"}
MAX_FILES = 4000
MAX_BYTES = 400_000


def walk(root):
    n = 0
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP]
        for f in fns:
            n += 1
            if n > MAX_FILES:
                return
            yield os.path.join(dp, f)


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read(MAX_BYTES)
    except OSError:
        return ""


def header_fields(text, keys):
    out = {}
    head = text[:8192]
    for k in keys:
        m = re.search(r"^[ \t/*#@]*" + re.escape(k) + r":[ \t]*(.+)$", head, re.M | re.I)
        if m:
            out[k] = m.group(1).strip()
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if not args or not os.path.isdir(args[0]):
        print("usage: detect_wp_project.py <folder> [--json]", file=sys.stderr)
        return 2
    root = os.path.abspath(args[0])
    files = list(walk(root))
    rel = [os.path.relpath(f, root) for f in files]
    relset = set(rel)
    report = {"path": root, "type": "unknown", "evidence": [], "tooling": {}, "entry_points": {}}

    if {"wp-includes/version.php", "wp-settings.php"} <= relset or \
       os.path.isfile(os.path.join(root, "src", "wp-includes", "version.php")):
        vp = os.path.join(root, "src", "wp-includes", "version.php")
        if not os.path.isfile(vp):
            vp = os.path.join(root, "wp-includes", "version.php")
        m = re.search(r"\$wp_version\s*=\s*'([^']+)'", read(vp))
        is_dev = os.path.isdir(os.path.join(root, "tests", "phpunit"))
        report["type"] = "core-checkout" if is_dev else "wordpress-install"
        report["core_version"] = m.group(1) if m else None
        report["evidence"].append("wp-includes/version.php found")
    elif os.path.isfile(os.path.join(root, "style.css")) and re.search(
            r"Theme Name:", read(os.path.join(root, "style.css"))[:8192], re.I):
        css = read(os.path.join(root, "style.css"))
        info = header_fields(css, ["Theme Name", "Version", "Requires at least", "Requires PHP",
                                   "Text Domain", "Template", "License"])
        block = os.path.isfile(os.path.join(root, "theme.json")) and \
            os.path.isdir(os.path.join(root, "templates"))
        report["type"] = "child-theme" if info.get("Template") else ("block-theme" if block else "classic-theme")
        report["header"] = info
        report["evidence"].append("style.css with Theme Name header")
        if os.path.isfile(os.path.join(root, "theme.json")):
            try:
                tj = json.loads(read(os.path.join(root, "theme.json")))
                report["theme_json_version"] = tj.get("version")
            except ValueError:
                report["evidence"].append("theme.json is not valid JSON")
        for d in ("templates", "parts", "patterns", "styles"):
            if os.path.isdir(os.path.join(root, d)):
                report["entry_points"][d] = len(os.listdir(os.path.join(root, d)))
    else:
        for f in sorted(os.listdir(root)):
            if f.endswith(".php"):
                txt = read(os.path.join(root, f))
                if re.search(r"Plugin Name:", txt[:8192], re.I):
                    info = header_fields(txt, ["Plugin Name", "Version", "Requires at least",
                                               "Requires PHP", "Text Domain", "License",
                                               "Requires Plugins"])
                    report["type"] = "plugin"
                    report["main_file"] = f
                    report["header"] = info
                    report["evidence"].append(f + " has a Plugin Name header")
                    if info.get("Requires Plugins"):
                        report["type"] = "plugin (add-on: declares required plugins)"
                    break

    t = report["tooling"]
    t["composer"] = "composer.json" in relset
    t["npm"] = "package.json" in relset
    t["phpcs"] = any(n in relset for n in (".phpcs.xml", ".phpcs.xml.dist", "phpcs.xml", "phpcs.xml.dist"))
    t["phpstan"] = any(n in relset for n in ("phpstan.neon", "phpstan.neon.dist"))
    t["phpunit"] = any(n in relset for n in ("phpunit.xml", "phpunit.xml.dist"))
    t["wp_env"] = ".wp-env.json" in relset
    t["git"] = os.path.isdir(os.path.join(root, ".git"))
    t["readme_txt"] = "readme.txt" in relset
    report["block_json_files"] = sum(1 for r in rel if r.endswith("block.json"))

    hooks, rest, cpts, shortcodes, ajax = set(), set(), set(), set(), set()
    php = [f for f in files if f.endswith(".php")]
    for f in php[:1500]:
        s = read(f)
        for m in re.finditer(r"\badd_(?:action|filter)\(\s*['\"]([\w\-/.]+)['\"]", s):
            hooks.add(m.group(1))
        for m in re.finditer(r"register_rest_route\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]", s):
            rest.add("/" + m.group(1).strip("/") + "/" + m.group(2).strip("/"))
        for m in re.finditer(r"register_post_type\(\s*['\"]([\w\-]+)['\"]", s):
            cpts.add(m.group(1))
        for m in re.finditer(r"add_shortcode\(\s*['\"]([\w\-]+)['\"]", s):
            shortcodes.add(m.group(1))
        for m in re.finditer(r"wp_ajax_(?:nopriv_)?([\w\-]+)", s):
            ajax.add(m.group(1))
    ep = report["entry_points"]
    ep["hooks_used"] = len(hooks)
    ep["hook_sample"] = sorted(hooks)[:15]
    ep["rest_routes"] = sorted(rest)
    ep["post_types"] = sorted(cpts)
    ep["shortcodes"] = sorted(shortcodes)
    ep["ajax_actions"] = sorted(ajax)
    report["php_files"] = len(php)
    report["files_scanned"] = len(files)
    if len(files) >= MAX_FILES:
        report["evidence"].append("file limit reached; results are partial")

    if as_json:
        print(json.dumps(report, indent=2))
    else:
        print("Path:", root)
        print("Type:", report["type"])
        for k in ("header", "core_version", "theme_json_version", "main_file"):
            if k in report:
                print(k + ":", report[k])
        print("Tooling:", ", ".join(k for k, v in t.items() if v) or "none detected")
        print("block.json files:", report["block_json_files"])
        for k, v in ep.items():
            if v and k != "hook_sample":
                print(k + ":", v)
        for e in report["evidence"]:
            print("note:", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
