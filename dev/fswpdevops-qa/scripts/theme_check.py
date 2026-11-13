#!/usr/bin/env python3
"""Mechanical QA gate for a WordPress theme folder (block, classic, or child). Python 3 stdlib only.

Usage: theme_check.py <theme-dir> [--directory] [--json]

Default mode reports issues as FAIL (real defects) or WARN (worth a look).
--directory applies the WordPress.org Theme Directory requirements strictly:
rules from the official "Required" page become FAIL instead of WARN.
Exit code 1 if any FAIL. SKIP means the check could not run; it is never a pass.
Rules verified against the Themes Team handbook on 2026-09-28.
"""
import json
import os
import re
import struct
import sys

SKIP_DIRS = {"vendor", "node_modules", ".git", "tests", "baseline"}
HARD_CDN = ("cdnjs.cloudflare.com", "cdn.jsdelivr.net", "unpkg.com", "ajax.googleapis.com",
            "use.typekit.net", "kit.fontawesome.com", "maxcdn.bootstrapcdn.com", "stackpath.bootstrapcdn.com")
FONT_CDN = ("fonts.googleapis.com", "fonts.gstatic.com")
BAD_FILES = {"thumbs.db", "desktop.ini", "project.properties", "project.xml", "php.ini", "dwsync.xml",
             "error_log", "web.config", "favicon.ico"}
BAD_EXT = {".kpf", ".sql", ".lubith", ".wie", ".dat", ".sh", ".zip"}
OK_XML = {"wpml-config.xml", "loco.xml", "phpcs.xml"}
results = []
STRICT = False


def add(status, check, detail=""):
    results.append({"status": status, "check": check, "detail": detail})


def rule(ok, check, detail="", directory_only=True):
    """Record a rule: pass, or FAIL in strict/defect mode, WARN otherwise."""
    if ok:
        add("PASS", check)
    else:
        add("FAIL" if (STRICT or not directory_only) else "WARN", check, detail)


def read(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def walk(root, exts=None):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if exts is None or f.lower().endswith(exts):
                yield os.path.join(d, f)


def image_size(path):
    try:
        with open(path, "rb") as fh:
            b = fh.read(64 * 1024)
        if b[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", b[16:24])
        if b[:2] == b"\xff\xd8":
            i = 2
            while i < len(b) - 9:
                if b[i] != 0xFF:
                    i += 1
                    continue
                m = b[i + 1]
                if m in (0xC0, 0xC1, 0xC2):
                    h, w = struct.unpack(">HH", b[i + 5:i + 9])
                    return w, h
                i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    except (OSError, struct.error):
        pass
    return None


def main():
    global STRICT
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    STRICT = "--directory" in sys.argv
    if not args or not os.path.isdir(args[0]):
        print("usage: theme_check.py <theme-dir> [--directory] [--json]", file=sys.stderr)
        return 2
    root = args[0]
    css = read(os.path.join(root, "style.css"))
    head = css[:8192]

    def field(k):
        m = re.search(r"^[ \t/*]*" + re.escape(k) + r":[ \t]*(.+)$", head, re.M | re.I)
        return m.group(1).strip() if m else ""

    is_child = bool(field("Template"))
    is_block = os.path.isfile(os.path.join(root, "theme.json")) and os.path.isdir(os.path.join(root, "templates"))
    kind = "child" if is_child else ("block" if is_block else "classic")
    add("PASS", "Theme type detected", kind)

    # Headers
    if not css:
        add("FAIL", "style.css present")
    required = ["Theme Name", "Author", "Description", "Version", "Requires at least", "Tested up to",
                "Requires PHP", "License", "License URI", "Text Domain"]
    missing = [k for k in required if not field(k)]
    hard_missing = [k for k in missing if k in ("Theme Name", "Version", "License", "Text Domain")]
    rule(not hard_missing, "style.css core headers (Theme Name, Version, License, Text Domain)", ", ".join(hard_missing), False)
    soft = [k for k in missing if k not in hard_missing]
    rule(not soft, "style.css directory headers (Author, Description, Requires at least, Tested up to, Requires PHP, License URI)",
         "missing: " + ", ".join(soft) + " ('Tested up to' is only valid after a real test)")
    lic = field("License").lower()
    if lic:
        rule("gpl" in lic, "License is GPL-compatible", field("License"), False)
    slug = os.path.basename(os.path.abspath(root))
    dom = field("Text Domain")
    rule((not dom) or dom == slug, "Text Domain equals the theme folder name", "%s vs %s" % (dom, slug))
    name = field("Theme Name").lower()
    rule(not ("wordpress" in name or re.search(r"\btheme\b", name) or name.startswith("twenty")),
         "Theme name avoids WordPress / Theme / Twenty*", field("Theme Name"))

    # Structure
    if kind == "block":
        rule(os.path.isfile(os.path.join(root, "templates", "index.html")), "templates/index.html exists", "", False)
        rule(os.path.isfile(os.path.join(root, "theme.json")), "theme.json exists", "", False)
    elif kind == "classic":
        rule(os.path.isfile(os.path.join(root, "index.php")), "index.php exists", "", False)
    else:
        add("PASS", "Child theme declares parent", field("Template"))
    rule(os.path.isfile(os.path.join(root, "readme.txt")), "readme.txt present (required by the directory)")

    tj = os.path.join(root, "theme.json")
    if os.path.isfile(tj):
        try:
            data = json.loads(read(tj))
            rule(bool(data.get("version")), "theme.json parses and declares version", "version=%s" % data.get("version"), False)
        except ValueError as e:
            add("FAIL", "theme.json parses", str(e))

    # Screenshot
    shot = next((os.path.join(root, "screenshot." + e) for e in ("png", "jpg", "jpeg") if os.path.isfile(os.path.join(root, "screenshot." + e))), None)
    if shot:
        sz = image_size(shot)
        if sz:
            w, h = sz
            ok = w <= 1200 and h <= 900 and abs(w / h - 4 / 3) < 0.02
            rule(ok, "Screenshot within 1200x900 and 4:3", "%dx%d" % (w, h))
        else:
            add("SKIP", "Screenshot size", "could not read image header")
    else:
        rule(False, "screenshot.png present")

    php = list(walk(root, (".php",)))
    src = {f: read(f) for f in php}
    alltext = "\n".join(src.values())

    # Forbidden or risky code
    banned = re.compile(r"\b(eval|create_function|extract|goto|shell_exec|passthru|proc_open|popen)\s*\(|`[^`\n]+`")
    bad = [os.path.relpath(f, root) for f, t in src.items() if banned.search(re.sub(r"//.*|/\*.*?\*/", "", t, flags=re.S))]
    rule(not bad, "No eval / create_function / extract / shell execution", ", ".join(bad[:5]), False)

    territory = [(r"register_post_type\s*\(", "custom post types"), (r"add_shortcode\s*\(", "shortcodes"),
                 (r"register_block_type(?:_from_metadata)?\s*\(", "custom blocks"), (r"\badd_role\s*\(", "custom roles"),
                 (r"user_contactmethods", "user contact methods"), (r"upload_mimes", "custom mime types")]
    found = sorted({label for pat, label in territory if re.search(pat, alltext)})
    rule(not found, "No plugin-territory features in the theme (CPT, blocks, shortcodes, roles, contact methods, mime types)", ", ".join(found))

    closure = re.search(r"add_(?:action|filter)\s*\([^;]*?function\s*\(", alltext, re.S)
    rule(not closure, "No closures as action/filter callbacks (they cannot be removed)", "", False) if closure else add("PASS", "No closures as action/filter callbacks")

    unesc = sorted({os.path.relpath(f, root) for f, t in src.items() if re.search(r"echo\s+\$_(GET|POST|REQUEST|SERVER)\b", t)})
    rule(not unesc, "No echo of raw request data", ", ".join(unesc[:5]), False)

    # Prefix heuristic: top-level functions should share a 4+ letter prefix
    funcs = set()
    for f, t in src.items():
        if os.path.basename(f) in ("header.php", "footer.php"):
            continue
        for m in re.finditer(r"^function\s+([a-z0-9_]+)\s*\(", t, re.M):
            funcs.add(m.group(1))
    if funcs:
        letters = re.sub(r"[^a-z]", "", slug.replace("-", "_").split("_")[0].lower())
        unp = sorted(fn for fn in funcs if not fn.startswith(slug.replace("-", "_")) and not (len(letters) >= 4 and fn.startswith(letters)))
        rule(not unp, "Global functions carry a unique prefix of 4+ letters", ", ".join(unp[:5]))

    # Classic requirements
    if kind == "classic":
        need = {"wp_head()": r"wp_head\s*\(", "body_class()": r"body_class\s*\(", "wp_footer()": r"wp_footer\s*\(",
                "wp_body_open()": r"wp_body_open\s*\(", "post_class()": r"post_class\s*\(",
                "wp_link_pages()": r"wp_link_pages\s*\(", "language_attributes()": r"language_attributes\s*\(",
                "title-tag support": r"add_theme_support\s*\(\s*['\"]title-tag", "automatic-feed-links support": r"add_theme_support\s*\(\s*['\"]automatic-feed-links",
                "DOCTYPE": r"<!DOCTYPE"}
        miss = [k for k, pat in need.items() if not re.search(pat, alltext, re.I)]
        rule(not miss, "Classic theme required calls present", "missing: " + ", ".join(miss))
        rule(bool(re.search(r"skip-link|#content|#main", alltext)), "Skip link present (accessibility)", "", True)

    # Files
    badfiles = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in {".git", ".svn", ".hg", ".bzr", "node_modules"} or False]
        for f in files:
            lf = f.lower()
            ext = os.path.splitext(lf)[1]
            if lf in BAD_FILES or ext in BAD_EXT or f.startswith(".") or (ext == ".xml" and lf not in OK_XML):
                badfiles.append(os.path.relpath(os.path.join(d, f), root))
    vcs = [x for x in (".git", ".svn", ".hg", ".bzr", "__MACOSX") if os.path.exists(os.path.join(root, x))]
    rule(not badfiles and not vcs, "No disallowed, hidden, or VCS files", ", ".join((badfiles + vcs)[:6]))

    # Remote resources
    hard, fonts = [], []
    for f in walk(root, (".php", ".html", ".css", ".js", ".json")):
        t = read(f)
        if any(c in t for c in HARD_CDN):
            hard.append(os.path.relpath(f, root))
        if any(c in t for c in FONT_CDN):
            fonts.append(os.path.relpath(f, root))
    rule(not hard, "No CDN scripts or styles", ", ".join(hard[:5]), False)
    if fonts:
        add("WARN", "Hosted fonts referenced (directory tolerates Google Fonts; bundling locally is safer)", ", ".join(fonts[:5]))
    else:
        add("PASS", "No hosted-font references")

    # package.json version
    pj = os.path.join(root, "package.json")
    if os.path.isfile(pj):
        try:
            pv = json.loads(read(pj)).get("version")
            rule(pv == field("Version"), "package.json version matches style.css", "%s vs %s" % (pv, field("Version")), False)
        except ValueError:
            add("WARN", "package.json parses")

    fails = [r for r in results if r["status"] == "FAIL"]
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print("[%s] %s%s" % (r["status"], r["check"], (" :: " + r["detail"]) if r["detail"] else ""))
        c = {k: sum(1 for r in results if r["status"] == k) for k in ("PASS", "FAIL", "WARN", "SKIP")}
        print("\n%d pass, %d fail, %d warn, %d skipped (SKIP = not run, not a pass)%s" %
              (c["PASS"], c["FAIL"], c["WARN"], c["SKIP"], " [directory mode]" if STRICT else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
