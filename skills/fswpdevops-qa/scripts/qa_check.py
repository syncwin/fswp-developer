#!/usr/bin/env python3
"""Mechanical QA gate for a WordPress plugin folder. Python 3 stdlib only.

Usage: qa_check.py <plugin-dir> [--json]
Exit code 1 if any check FAILs. WARN and SKIP never fail the run.
SKIP means the check could not run; it is never a pass.
"""
import json, os, re, sys

SKIP_DIRS = {"vendor", "node_modules", "tests", "baseline", ".git", "foundation"}
CDN = ("fonts.googleapis.com", "fonts.gstatic.com", "cdnjs.cloudflare.com", "cdn.jsdelivr.net",
       "unpkg.com", "ajax.googleapis.com", "use.typekit.net", "kit.fontawesome.com",
       "use.fontawesome.com", "stackpath.bootstrapcdn.com", "maxcdn.bootstrapcdn.com", "code.jquery.com")
results = []


def add(status, check, detail=""):
    results.append({"status": status, "check": check, "detail": detail})


def walk(root, exts, include_foundation=False):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in (SKIP_DIRS - ({"foundation"} if include_foundation else set()))]
        for f in files:
            if f.lower().endswith(exts):
                yield os.path.join(d, f)


def read(p):
    try:
        with open(p, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def matching(text, i, o, c):
    """Index just past the bracket that closes the one at text[i]; string/comment aware."""
    depth, n, k = 0, len(text), i
    while k < n:
        ch = text[k]
        if ch in "'\"":
            q = ch; k += 1
            while k < n and text[k] != q:
                k += 2 if text[k] == "\\" else 1
        elif text.startswith("//", k) or ch == "#":
            k = text.find("\n", k); k = n if k < 0 else k
            continue
        elif text.startswith("/*", k):
            k = text.find("*/", k); k = n if k < 0 else k + 1
        elif ch == o:
            depth += 1
        elif ch == c:
            depth -= 1
            if depth == 0:
                return k + 1
        k += 1
    return n


def rel(root, p):
    return os.path.relpath(p, root)


def run(root):
    php = list(walk(root, (".php",)))
    if not php:
        add("FAIL", "PHP files", "no .php files found")
        return
    src = {p: read(p) for p in php}
    allphp = "\n".join(src.values())
    code = re.sub(r"/\*.*?\*/", "", allphp, flags=re.S)
    code = re.sub(r"(?<![:'\"])//[^\n]*|(?m:^\s*#[^\n]*)", "", code)  # comments never count as code

    # 1. ABSPATH guard
    bad = [rel(root, p) for p, t in src.items()
           if os.path.basename(p) not in ("uninstall.php", "index.php") and "ABSPATH" not in t[:1500]]
    add("FAIL" if bad else "PASS", "ABSPATH guard on every PHP file", ", ".join(bad[:8]))

    # main file + version consistency
    main = next((p for p, t in src.items() if re.search(r"^\s*\*?\s*Plugin Name:", t[:3000], re.M)), None)
    if not main:
        add("FAIL", "Main plugin file", "no file with a 'Plugin Name:' header")
    else:
        hdr = src[main][:3000]
        ver = re.search(r"Version:\s*([^\s*]+)", hdr)
        ver = ver.group(1) if ver else None
        consts = re.findall(r"define\(\s*'([A-Z0-9_]+_VERSION)'\s*,\s*'([^']+)'", allphp)
        rd = read(os.path.join(root, "readme.txt"))
        stable = re.search(r"Stable tag:\s*(\S+)", rd)
        vals = {"header Version": ver}
        for n, v in consts:
            vals[n] = v
        if os.path.exists(os.path.join(root, "readme.txt")):
            vals["readme Stable tag"] = stable.group(1) if stable else None
        else:
            add("SKIP", "readme.txt Stable tag", "readme.txt not present (fine for private builds)")
        distinct = set(v for v in vals.values() if v)
        if None in vals.values() or len(distinct) > 1:
            add("FAIL", "Version consistency", str(vals))
        else:
            add("PASS", "Version consistency", next(iter(distinct), ""))
        if not consts:
            add("WARN", "Version constant", "no PREFIX_VERSION constant found")
        for f in ("Plugin URI", "Author URI"):
            m = re.search(f + r":\s*(\S+)", hdr)
            if m and re.search(r"example\.(com|org|net)", m.group(1)):
                add("FAIL", "Placeholder URI", f"{f}: {m.group(1)}")
        if re.search(r"Author:\s*Unknown", hdr):
            add("WARN", "Author header", "still 'Unknown'")

    # 2. example.com placeholders anywhere in shipped PHP/readme
    ex = [rel(root, p) for p, t in src.items() if re.search(r"example\.(com|org|net)", t)]
    if os.path.exists(os.path.join(root, "readme.txt")) and re.search(r"example\.(com|org|net)", read(os.path.join(root, "readme.txt"))):
        ex.append("readme.txt")
    add("FAIL" if ex else "PASS", "No example.com placeholders", ", ".join(ex[:8]))

    # 3. remote URLs / CDN fonts
    hits = []
    for p in list(walk(root, (".php", ".js", ".css", ".html", ".jsx", ".ts", ".tsx"))):
        t = read(p)
        for h in CDN:
            if h in t:
                hits.append(f"{rel(root, p)} ({h})")
        if re.search(r"wp_(enqueue|register)_(script|style)\([^;]*['\"]https?://", t):
            hits.append(f"{rel(root, p)} (remote enqueue)")
        if re.search(r"@import\s+(url\()?['\"]?https?://", t):
            hits.append(f"{rel(root, p)} (CSS @import remote)")
    add("FAIL" if hits else "PASS", "No remote assets, CDN scripts, or CDN fonts", "; ".join(sorted(set(hits))[:6]))

    # 4. REST permission_callback
    missing, unjust = [], []
    for p, t in src.items():
        for m in re.finditer(r"register_rest_route\s*\(", t):
            end = matching(t, m.end() - 1, "(", ")")
            call = t[m.start():end]
            loc = f"{rel(root, p)}:{t[:m.start()].count(chr(10)) + 1}"
            if "permission_callback" not in call:
                missing.append(loc)
            elif "__return_true" in call:
                line_no = t[:m.start()].count("\n")
                lines = t.split("\n")
                rt = next((i for i in range(line_no, min(end and t[:end].count("\n") + 1, len(lines))) if "__return_true" in lines[i]), line_no)
                window = lines[max(0, rt - 3):rt + 1]
                if not any(re.search(r"//|/\*|\*\s|#", w) for w in window):
                    unjust.append(loc)
    add("FAIL" if missing else "PASS", "Every REST route has permission_callback", ", ".join(missing[:6]))
    add("FAIL" if unjust else "PASS", "__return_true routes are commented as public", ", ".join(unjust[:6]))

    # 5. DB upgrade hook
    if re.search(r"dbDelta\s*\(|CREATE TABLE", code):
        ok = re.search(r"(plugins_loaded|admin_init|'init')", code) and re.search(r"maybe_upgrade|db_version|DB_VERSION", code, re.I)
        add("PASS" if ok else "FAIL", "DB upgrade check outside activation", "" if ok else "dbDelta used but no version check on plugins_loaded/admin_init")
    else:
        add("SKIP", "DB upgrade check", "no custom tables detected")

    # 6. Enqueue rules
    has_sc = "add_shortcode(" in allphp
    problems = []
    if "has_shortcode(" in allphp:
        problems.append("has_shortcode() used (misses builder content; enqueue inside the shortcode callback)")
    for p, t in src.items():
        for m in re.finditer(r"add_action\(\s*'wp_enqueue_scripts'\s*,\s*(?:array\(\s*\$this\s*,\s*|\[\s*\$this\s*,\s*)?'([A-Za-z0-9_]+)'", t):
            fn = re.search(r"function\s+" + re.escape(m.group(1)) + r"\s*\([^)]*\)\s*\{", t)
            if fn:
                body = t[fn.end() - 1: matching(t, fn.end() - 1, "{", "}")]
                if re.search(r"wp_enqueue_(script|style)", body) and not re.search(r"\bif\s*\(", body) and has_sc:
                    problems.append(f"{rel(root, p)}: '{m.group(1)}' enqueues unconditionally site-wide while a shortcode exists")
    add("FAIL" if problems else "PASS", "Shortcode assets enqueued inside callback, not site-wide", "; ".join(problems))

    # 7. Banned functions
    banned = [f for f in ("eval(", "create_function(", "extract(") if re.search(r"(?<![A-Za-z_>:])" + re.escape(f), allphp)]
    add("FAIL" if banned else "PASS", "No eval/create_function/extract", ", ".join(banned))

    # 8. Lifecycle basics
    un = os.path.join(root, "uninstall.php")
    if os.path.exists(un):
        add("PASS" if "WP_UNINSTALL_PLUGIN" in read(un) else "FAIL", "uninstall.php guarded by WP_UNINSTALL_PLUGIN")
    else:
        add("FAIL", "uninstall.php present", "missing")
    add("PASS" if "load_plugin_textdomain" in allphp else "WARN", "load_plugin_textdomain called")

    # 9. Front-end markup headings
    hh = [rel(root, p) for p, t in src.items() if os.sep + "public" + os.sep in p and re.search(r"<h[1-3][\s>]", t)]
    add("FAIL" if hh else "PASS", "No h1-h3 in shortcode/block markup", ", ".join(hh[:6]))

    # 10. Units
    css_own = [p for p in walk(root, (".css",))]
    rootfont = [rel(root, p) for p in css_own if re.search(r"html\s*\{[^}]*font-size:\s*62\.5%", read(p))]
    add("FAIL" if rootfont else "PASS", "No 62.5% root font-size rebasing in plugin CSS", ", ".join(rootfont))
    pxs = [rel(root, p) for p in css_own if re.search(r"(font-size|line-height|gap|padding|margin|border-radius)\s*:\s*[^;]*\b\d{2,}px", read(p))]
    add("WARN" if pxs else "PASS", "Type/spacing/radius in rem, not px", ", ".join(pxs[:6]))

    # 11. JS i18n
    own_js = [p for p in walk(root, (".js", ".jsx", ".ts", ".tsx")) if not re.search(r"(\.min\.|build|dist)", p)]
    if own_js:
        ok = "wp_set_script_translations" in allphp
        add("PASS" if ok else "WARN", "JS translations registered", "" if ok else "own JS present but no wp_set_script_translations()")
    else:
        add("SKIP", "JS translations registered", "no own JS files")

    # 12. Source in the zip for compiled output
    compiled = any(os.path.isdir(os.path.join(root, d)) for d in ("build", "dist"))
    if compiled:
        has_src = os.path.isdir(os.path.join(root, "src")) and os.path.exists(os.path.join(root, "package.json")) and \
            any(os.path.exists(os.path.join(root, l)) for l in ("bun.lock", "bun.lockb", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"))
        add("PASS" if has_src else "FAIL", "Source, package.json and lockfile ship with compiled output")
    else:
        add("SKIP", "Source ships with compiled output", "no build/ or dist/ folder")

    # 13. Feature documentation present (docs/features/) and stubs actually filled in
    has_features = any(os.path.isdir(os.path.join(root, d)) for d in ("includes", "admin")) or \
        any(re.search(r"add_shortcode|register_rest_route|register_post_type", t) for t in src.values())
    docs_dir = os.path.join(root, "docs", "features")
    if has_features:
        if not os.path.isdir(docs_dir):
            add("FAIL", "docs/features/ feature documentation present", "no docs/features/ folder found (scaffold generates stubs; they were removed or build skipped them)")
        else:
            doc_files = [f for f in os.listdir(docs_dir) if f.endswith(".md") and f != "README.md"]
            if not doc_files:
                add("FAIL", "docs/features/ feature documentation present", "docs/features/ exists but has no feature files")
            else:
                unfilled = [f for f in doc_files if "FILL IN:" in read(os.path.join(docs_dir, f))
                            and "**Status:** planned" not in read(os.path.join(docs_dir, f))]
                add("FAIL" if unfilled else "PASS", "docs/features/ feature documentation completed",
                    f"unfilled stub(s): {', '.join(unfilled)}" if unfilled else f"{len(doc_files)} doc file(s), all filled")
    else:
        add("SKIP", "docs/features/ feature documentation present", "no feature classes detected")

    # 14. Bundled fonts carry a license
    fonts = [p for p in walk(root, (".woff2", ".woff", ".ttf", ".otf"), True)]
    if fonts:
        lic = any(re.search(r"(OFL|LICENSE|licen[cs]e)", f, re.I) for d, _, fs in os.walk(root) for f in fs)
        add("PASS" if lic else "WARN", "Bundled fonts include a license file")

    # 15. Header and readme rules from the official plugin handbook (verified 2026-09-28)
    if main:
        hdr = src[main][:3000]
        def hf(k):
            m = re.search(r"^[ \t/*]*" + re.escape(k) + r":[ \t]*(.+)$", hdr, re.M | re.I)
            return m.group(1).strip() if m else ""
        problems = []
        d = hf("Description")
        if d and len(d) >= 140:
            problems.append("Description is %d chars (keep under 140)" % len(d))
        uri = hf("Plugin URI")
        if "wordpress.org" in uri.lower():
            problems.append("Plugin URI must be unique to the plugin, not a WordPress.org URL")
        for k in ("Requires at least", "Requires PHP", "License", "Text Domain"):
            if not hf(k):
                problems.append("header field missing: " + k)
        add("WARN" if problems else "PASS", "Plugin header fields follow the handbook", "; ".join(problems))
    rdp = os.path.join(root, "readme.txt")
    if os.path.exists(rdp):
        rd = read(rdp)
        issues = []
        tags = re.search(r"^Tags:\s*(.+)$", rd, re.M)
        if tags and len([t for t in tags.group(1).split(",") if t.strip()]) > 5:
            issues.append("more than 5 tags")
        st = re.search(r"^Stable tag:\s*(\S+)", rd, re.M)
        if st and st.group(1).lower() == "trunk":
            issues.append("Stable tag: trunk is prohibited for new plugins")
        tu = re.search(r"^Tested up to:\s*(.+)$", rd, re.M)
        if tu and not re.fullmatch(r"\d+(\.\d+){1,2}", tu.group(1).strip()):
            issues.append("Tested up to must be a version number only")
        if len(rd.encode("utf-8")) > 10240:
            issues.append("readme is over ~10 KB (move older changelog to changelog.txt)")
        head_end = re.search(r"^== ", rd, re.M)
        if head_end:
            block = rd[:head_end.start()].strip().splitlines()
            shortd = [l for l in block[1:] if l.strip() and not re.match(r"^[A-Za-z ]+:", l)]
            if shortd and len(shortd[0]) > 150:
                issues.append("short description over 150 chars")
        add("WARN" if issues else "PASS", "readme.txt follows the WordPress.org standard", "; ".join(issues))


def main():
    if len(sys.argv) < 2 or not os.path.isdir(sys.argv[1]):
        print(__doc__); sys.exit(2)
    run(sys.argv[1])
    fails = [r for r in results if r["status"] == "FAIL"]
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"[{r['status']:4}] {r['check']}" + (f" :: {r['detail']}" if r["detail"] else ""))
        c = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS", "FAIL", "WARN", "SKIP")}
        print(f"\n{c['PASS']} pass, {c['FAIL']} fail, {c['WARN']} warn, {c['SKIP']} skipped (SKIP = not run, not a pass)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
