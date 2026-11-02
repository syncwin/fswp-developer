#!/usr/bin/env python3
"""
Scaffold a WordPress plugin folder from this skill's templates.

Usage:
    python scaffold_plugin.py \
        --name "Event Manager" \
        --prefix acme \
        --description "Manage and display events with a front-end shortcode." \
        --author "SyncWin" \
        --features cpt,db,rest,cron,admin,frontend \
        --foundation-dir /path/to/current/atomic-framework \
        --out ./output

--features is a comma-separated subset of: cpt,db,rest,cron,admin,frontend
Only requested features get their class files generated; unused
scaffolding is not created (a "settings-only" plugin should pass
--features admin, for example).

--js-tier defaults to "vanilla" (zero extra dependency) and should
stay there unless the 5-point checklist in
references/frontend-output.md triggered on this plugin's requested
behavior AND the user has explicitly confirmed adding the Alpine.js
tier. This script does not make that decision — pass --js-tier alpine
only after that confirmation has happened in conversation.

--admin-tier defaults to "native" (Settings API / WP_List_Table, zero
build step). "react" is the @wordpress/components + wp.element
escalation for a single screen with real interactivity. "app" is the
full React SPA + Tailwind + TanStack Query + Zustand stack from
references/modern-app-stack.md, only for an admin experience with
multiple interactive screens / real-time state / data tables / a
multi-step flow — see that file's decision criteria before passing
this. This script does not scaffold the "app" tier's build tooling
itself; it only records the choice and prints the relevant reference
pointer, since that stack's setup (Bun, TanStack, Zustand, shadcn-ui,
the REST contract) is project-specific enough to be assembled by hand
following the reference file, not templated mechanically.

This script only performs mechanical placeholder substitution and file
copying. It does NOT decide architecture, security details, or content —
follow the reference files in ../references/ for that; this just saves
retyping the skeleton by hand.
"""
import argparse
import os
import re
import shutil
import sys

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "templates")

# The Atomic Framework (the design system) is NOT bundled with this
# skill — it's a separately maintained product on its own release
# cycle. --foundation-dir must point at a user-supplied copy of the
# current files; see references/frontend-output.md.
FOUNDATION_FILES = ["swwp-tokens.css", "swwp-components.css", "swwp-foundation-logics.js"]
ALPINE_FILES = ["alpine.min.js", "alpine-loader.js", "alpine-components.js"]

FEATURE_FILES = {
    "cpt": [("includes/class-prefix-cpt.php", "includes/class-{prefix}-cpt.php")],
    "db": [("includes/class-prefix-db.php", "includes/class-{prefix}-db.php")],
    "rest": [("includes/class-prefix-rest.php", "includes/class-{prefix}-rest.php")],
    "cron": [("includes/class-prefix-cron.php", "includes/class-{prefix}-cron.php")],
    "admin": [
        ("admin/class-prefix-admin.php", "admin/class-{prefix}-admin.php"),
        ("admin/css/admin.css", "admin/css/admin.css"),
        ("admin/js/admin.js", "admin/js/admin.js"),
    ],
    "frontend": [
        ("public/class-prefix-public.php", "public/class-{prefix}-public.php"),
        ("public/css/plugin-slug.css", "public/css/{slug}.css"),
        ("public/js/plugin-slug.js", "public/js/{slug}.js"),
    ],
}

ALWAYS_FILES = [
    ("plugin-slug.php", "{slug}.php"),
    ("uninstall.php", "uninstall.php"),
    ("includes/class-prefix-activator.php", "includes/class-{prefix}-activator.php"),
    ("includes/class-prefix-deactivator.php", "includes/class-{prefix}-deactivator.php"),
]


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    return s


def feature_blocks(features: set) -> dict:
    """Code generated from the selected features, so the scaffold never requires a missing file."""
    R = "        require_once {{PREFIX}}_PLUGIN_DIR . 'includes/class-{{prefix}}-%s.php';\n"
    L = []
    if "db" in features:
        L += [R % "db", "        add_action( 'plugins_loaded', array( '{{Prefix}}_DB', 'maybe_upgrade' ) );\n\n"]
    if "admin" in features:
        L += ["        if ( is_admin() ) {\n", "            require_once {{PREFIX}}_PLUGIN_DIR . 'admin/class-{{prefix}}-admin.php';\n", "            new {{Prefix}}_Admin();\n", "        }\n\n"]
    if "frontend" in features:
        L += ["        require_once {{PREFIX}}_PLUGIN_DIR . 'public/class-{{prefix}}-public.php';\n", "        new {{Prefix}}_Public();\n\n"]
    for f, cls in (("cpt", "CPT"), ("rest", "REST"), ("cron", "Cron")):
        if f in features:
            L += [R % f, "        new {{Prefix}}_%s();\n\n" % cls]
    return {
        "loaders": "".join(L).rstrip("\n"),
        "act_db": (R % "db") + "        {{Prefix}}_DB::maybe_upgrade();\n\n" if "db" in features else "",
        "act_cron": (R % "cron") + "        {{Prefix}}_Cron::schedule();\n\n" if "cron" in features else "",
        "act_cpt": (R % "cpt") + "        ( new {{Prefix}}_CPT() )->register();\n        flush_rewrite_rules();\n" if "cpt" in features else "",
        "deact_cron": (R % "cron") + "        {{Prefix}}_Cron::unschedule();\n\n" if "cron" in features else "",
    }


def substitute(text: str, ctx: dict) -> str:
    for tok, key in (("{{FEATURE_LOADERS}}", "loaders"), ("{{ACT_DB}}", "act_db"), ("{{ACT_CRON}}", "act_cron"),
                     ("{{ACT_CPT}}", "act_cpt"), ("{{DEACT_CRON}}", "deact_cron")):
        text = text.replace(tok + "\n", ctx.get(key, "") + ("\n" if key == "loaders" else ""))
    text = text.replace("{{PLUGIN_URI_LINE}}\n", ctx["plugin_uri_line"])
    text = text.replace("{{AUTHOR_URI_LINE}}\n", ctx["author_uri_line"])
    text = text.replace("{{PLUGIN_NAME}}", ctx["plugin_name"])
    text = text.replace("{{ONE_LINE_DESCRIPTION}}", ctx["description"])
    text = text.replace("{{AUTHOR}}", ctx["author"])
    text = text.replace("{{plugin-slug}}", ctx["slug"])
    text = text.replace("{{PREFIX}}", ctx["prefix_upper"])
    text = text.replace("{{Prefix}}", ctx["prefix_title"])
    text = text.replace("{{prefix}}", ctx["prefix_lower"])
    text = text.replace("{{noun}}", ctx["noun"])
    text = text.replace("{{code}}", ctx["noun"])
    text = text.replace("{{job}}", ctx["noun"])
    text = text.replace("{{Plural Name}}", ctx["plugin_name"] + "s")
    text = text.replace("{{Singular Name}}", ctx["plugin_name"])
    text = text.replace("{{plural_name}}", ctx["slug"].replace("-", " ") + "s")
    return text


def write_file(rel_src: str, rel_dst: str, ctx: dict, out_dir: str):
    src_path = os.path.join(TEMPLATE_DIR, rel_src)
    dst_rel = rel_dst.format(prefix=ctx["prefix_lower"], slug=ctx["slug"])
    dst_path = os.path.join(out_dir, ctx["slug"], dst_rel)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = substitute(content, ctx)
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(content)
    return dst_path


def main():
    parser = argparse.ArgumentParser(description="Scaffold a WordPress plugin from this skill's templates.")
    parser.add_argument("--name", required=True, help="Human-readable plugin name, e.g. 'Event Manager'")
    parser.add_argument("--prefix", required=True, help="Short unique prefix chosen for this project (ask the user; no built-in default), e.g. acme")
    parser.add_argument("--description", default="", help="One-line plugin description")
    parser.add_argument("--author", default="", help="Author name")
    parser.add_argument("--plugin-uri", default="", help="Real plugin URI; header line is omitted if not given (never a placeholder domain)")
    parser.add_argument("--author-uri", default="", help="Real author URI; header line is omitted if not given")
    parser.add_argument("--noun", default="item", help="Primary domain noun for CPT/table/shortcode naming (e.g. 'event')")
    parser.add_argument("--features", default="admin,frontend", help="Comma-separated subset of: cpt,db,rest,cron,admin,frontend")
    parser.add_argument("--distribution", choices=["wporg", "private", "both"], default="private")
    parser.add_argument("--out", default=".", help="Output directory (plugin folder is created inside this)")
    parser.add_argument("--zip", action="store_true", help="Also produce an installable {slug}.zip next to the plugin folder")
    parser.add_argument("--js-tier", choices=["vanilla", "alpine"], default="vanilla", help="Front-end JS tier (only relevant with --features frontend). Default: vanilla, zero extra dependency. 'alpine' should only be passed AFTER running the 5-point checklist in references/frontend-output.md and getting explicit user confirmation — this flag does not make that decision for you.")
    parser.add_argument("--admin-tier", choices=["native", "react", "app"], default="native", help="Admin UI tier (only relevant with --features admin). Default: native (Settings API / WP_List_Table). 'react' = @wordpress/components + wp.element for one interactive screen. 'app' = full React SPA + Tailwind + TanStack Query + Zustand per references/modern-app-stack.md, only for a genuinely multi-screen app-like admin. This flag records the choice; 'app' scaffolding is assembled by hand from that reference file, not templated here.")
    parser.add_argument("--foundation-dir", default=None, help="Path to a user-supplied, current copy of the Atomic Framework files (swwp-tokens.css, swwp-components.css, swwp-foundation-logics.js, and the alpine-*.js files if --js-tier alpine). Required whenever --features includes 'frontend' — this skill does not bundle the framework itself (see references/frontend-output.md). Ask the user for these files before scaffolding rather than guessing a path.")
    args = parser.parse_args()

    slug = slugify(f"{args.prefix}-{args.name}")
    ctx = {
        "plugin_name": args.name,
        "description": args.description or f"{args.name} plugin.",
        "author": args.author or "Unknown",
        "plugin_uri_line": f" * Plugin URI:        {args.plugin_uri}\n" if args.plugin_uri else "",
        "author_uri_line": f" * Author URI:        {args.author_uri}\n" if args.author_uri else "",
        "slug": slug,
        "prefix_upper": args.prefix.upper(),
        "prefix_title": args.prefix.upper(),
        "prefix_lower": args.prefix.lower(),
        "noun": slugify(args.noun).replace("-", "_"),
    }

    features = set(f.strip().lower() for f in args.features.split(",") if f.strip())
    unknown = features - set(FEATURE_FILES.keys())
    if unknown:
        print(f"Unknown feature(s): {', '.join(unknown)} — valid: {', '.join(FEATURE_FILES.keys())}", file=sys.stderr)
        sys.exit(1)

    ctx.update(feature_blocks(features))

    generated = []
    for src, dst in ALWAYS_FILES:
        generated.append(write_file(src, dst, ctx, args.out))

    for feature in features:
        for src, dst in FEATURE_FILES[feature]:
            generated.append(write_file(src, dst, ctx, args.out))

    # Feature documentation stubs (references/standards.md section 4).
    # Skeleton only — never invented content. fswp-plugin-developer fills each TODO from
    # the approved PRD before delivery; qa_check.py flags any TODO left in.
    FEATURE_DOCS = {
        "cpt": ("Custom post type", "PRD section 5 (Data model)"),
        "db": ("Custom database table", "PRD section 5 (Data model)"),
        "rest": ("REST API", "PRD section 6 (API surface)"),
        "cron": ("Scheduled jobs", "PRD section 5 (Data model) / cron entries"),
        "admin": ("Admin experience", "PRD section 7 (Admin experience)"),
        "frontend": ("Front-end output", "PRD section 8 (Front-end experience)"),
    }
    docs_dir = os.path.join(args.out, ctx["slug"], "docs")
    if features:
        os.makedirs(docs_dir, exist_ok=True)
        index_lines = [f"# {ctx['plugin_name']} — feature documentation", "",
                       "One file per feature. Fill every TODO from the approved PRD before delivery.", ""]
        for feature in sorted(features):
            title, prd_ref = FEATURE_DOCS[feature]
            index_lines.append(f"- [{title}]({feature}.md)")
            doc_path = os.path.join(docs_dir, f"{feature}.md")
            with open(doc_path, "w", encoding="utf-8") as fh:
                fh.write(f"""# {title}

<!-- TODO: fill from {prd_ref} before delivery. Remove this comment once done. -->

## What it does

TODO: one or two sentences, plain language.

## How it works

TODO: the mechanism — hooks used, data flow, key functions/classes.

## Inputs

TODO: settings, parameters, REST args, or shortcode attributes. Remove this heading if none apply.

## Outputs

TODO: what it renders, returns, or stores. Remove this heading if none apply.

## Dependencies

TODO: other features/classes it relies on, external services, the JS/admin tier it uses. Remove this heading if none apply.

## Constraints

TODO: capability required, rate limits, size caps, version requirements. Remove this heading if none apply.
""")
            generated.append(doc_path)
        index_path = os.path.join(docs_dir, "README.md")
        with open(index_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(index_lines) + "\n")
        generated.append(index_path)

    if "frontend" in features:
        if not args.foundation_dir:
            print("STOPPED: --features includes 'frontend' but no --foundation-dir")
            print("was given. This skill does not bundle the Atomic Framework — it's")
            print("a separately maintained product. Ask the user for their current")
            print("swwp-tokens.css, swwp-components.css, swwp-foundation-logics.js")
            print("(and alpine.min.js/alpine-loader.js/alpine-components.js if")
            print("--js-tier alpine), then re-run with --foundation-dir pointing at")
            print("them. See references/frontend-output.md for detail.")
            sys.exit(1)

        missing = [f for f in FOUNDATION_FILES if not os.path.isfile(os.path.join(args.foundation_dir, f))]
        if args.js_tier == "alpine":
            missing += [f for f in ALPINE_FILES if not os.path.isfile(os.path.join(args.foundation_dir, f))]
        if missing:
            print(f"STOPPED: --foundation-dir is missing required file(s): {', '.join(missing)}")
            print("Ask the user for a complete, current set before proceeding.")
            sys.exit(1)

        foundation_dst_dir = os.path.join(args.out, ctx["slug"], "public", "foundation")
        os.makedirs(foundation_dst_dir, exist_ok=True)
        for fname in FOUNDATION_FILES:
            src_path = os.path.join(args.foundation_dir, fname)
            dst_path = os.path.join(foundation_dst_dir, fname)
            shutil.copyfile(src_path, dst_path)
            generated.append(dst_path)

        if args.js_tier == "alpine":
            for fname in ALPINE_FILES:
                src_path = os.path.join(args.foundation_dir, fname)
                dst_path = os.path.join(foundation_dst_dir, fname)
                shutil.copyfile(src_path, dst_path)
                generated.append(dst_path)
            print("NOTE: js-tier=alpine selected. Enqueue alpine-loader.js under")
            print("the literal shared handle 'fswp-alpine-loader' (never prefixed")
            print("per plugin) — see references/frontend-output.md for the")
            print("full dual-guard enqueue snippet, required to avoid double-")
            print("initializing Alpine if another plugin on the same site uses it.")

    # Main plugin class always required — assemble its require/instantiate
    # lines based on requested features.
    main_class_path = write_file(
        "includes/class-prefix-plugin.php",
        "includes/class-{prefix}-plugin.php",
        ctx,
        args.out,
    )
    generated.append(main_class_path)

    # readme(s)
    if args.distribution in ("wporg", "both"):
        generated.append(write_file("readme.txt", "readme.txt", ctx, args.out))
    if args.distribution in ("private", "both"):
        generated.append(write_file("README-private.md", "README.md", ctx, args.out))

    if "admin" in features and args.admin_tier == "app":
        print("NOTE: admin-tier=app selected. This tier's own build tooling")
        print("(Bun, React SPA, Tailwind, TanStack Query, Zustand, Radix primitives,")
        print("@shadcn/lint) is not templated by this script — follow")
        print("references/modern-app-stack.md to assemble it, confirming")
        print("first via that file's decision checklist that the admin UI is")
        print("genuinely app-like enough to justify it over --admin-tier react.")

    plugin_dir = os.path.join(args.out, slug)
    os.makedirs(os.path.join(plugin_dir, "languages"), exist_ok=True)

    if args.zip:
        zip_base = os.path.join(args.out, slug)
        shutil.make_archive(zip_base, "zip", root_dir=args.out, base_dir=slug)
        print(f"Zipped: {zip_base}.zip")

    print(f"Scaffolded plugin at: {plugin_dir}")
    print("Files generated:")
    for g in generated:
        print(f"  - {os.path.relpath(g, args.out)}")
    print("\nNext: fill in domain logic per the skill's reference files,")
    print("uncomment the relevant require/instantiate lines in the main")
    print("plugin class and activator/deactivator, then run the FULL gate with --fix")
    print("(required once, right after scaffolding — the templates rely on phpcbf's")
    print("WordPress-standard formatting, which is applied to the generated plugin,")
    print("never to these raw templates):")
    print(f"  bash <this-skill>/../fswp-qa-engineer/scripts/run_gate.sh {plugin_dir} <min-php> --fix")
    print("then the fswp-qa-engineer checklist before delivering.")


if __name__ == "__main__":
    main()
