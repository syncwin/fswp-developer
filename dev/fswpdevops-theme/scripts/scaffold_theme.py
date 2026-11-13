#!/usr/bin/env python3
"""Scaffold a WordPress theme skeleton. Python 3 standard library only.

Usage:
  scaffold_theme.py --name "My Theme" --slug my-theme --type block|classic|child
      [--parent parent-slug] [--author "Name"] [--author-uri URL] [--theme-uri URL]
      [--description TEXT] [--min-wp 6.4] [--min-php 7.4] [--out DIR] [--zip]

Values you do not pass are left out of the header; nothing is invented.
"""
import argparse
import datetime
import os
import shutil
import sys


def header(a):
    lines = ["Theme Name: " + a.name]
    if a.theme_uri:
        lines.append("Theme URI: " + a.theme_uri)
    if a.author:
        lines.append("Author: " + a.author)
    if a.author_uri:
        lines.append("Author URI: " + a.author_uri)
    lines.append("Description: " + (a.description or a.name))
    if a.type == "child":
        lines.append("Template: " + a.parent)
    lines += ["Version: 0.0.1", "Requires at least: " + a.min_wp]
    if a.tested_up_to:
        lines.append("Tested up to: " + a.tested_up_to)
    lines += ["Requires PHP: " + a.min_php,
              "License: GPL-2.0-or-later", "License URI: https://www.gnu.org/licenses/gpl-2.0.html",
              "Text Domain: " + a.slug]
    return "/*\n" + "\n".join(lines) + "\n*/\n"


def prefix(a):
    return a.slug.replace("-", "_")


def w(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)


THEME_JSON = """{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "layout": { "contentSize": "720px", "wideSize": "1200px" },
    "color": { "palette": [
      { "slug": "base", "name": "Base", "color": "#ffffff" },
      { "slug": "contrast", "name": "Contrast", "color": "#111111" },
      { "slug": "primary", "name": "Primary", "color": "#1d4ed8" }
    ] },
    "typography": { "fluid": true, "fontSizes": [
      { "slug": "small", "name": "Small", "size": "0.875rem" },
      { "slug": "medium", "name": "Medium", "size": "1.125rem" },
      { "slug": "large", "name": "Large", "size": "clamp(1.5rem, 1.2rem + 1.2vw, 2rem)" }
    ] }
  },
  "styles": {
    "color": { "background": "var(--wp--preset--color--base)", "text": "var(--wp--preset--color--contrast)" },
    "elements": { "link": { "color": { "text": "var(--wp--preset--color--primary)" } } }
  },
  "templateParts": [
    { "name": "header", "title": "Header", "area": "header" },
    { "name": "footer", "title": "Footer", "area": "footer" }
  ]
}
"""

INDEX_HTML = """<!-- wp:template-part {"slug":"header","tagName":"header"} /-->
<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group"><!-- wp:query {"queryId":0,"query":{"perPage":10,"postType":"post","inherit":true}} -->
<div class="wp-block-query"><!-- wp:post-template -->
<!-- wp:post-title {"isLink":true} /-->
<!-- wp:post-excerpt /-->
<!-- /wp:post-template -->
<!-- wp:query-pagination /--></div>
<!-- /wp:query --></main>
<!-- /wp:group -->
<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
"""

HEADER_PART = """<!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
<div class="wp-block-group"><!-- wp:site-title /--><!-- wp:navigation /--></div>
<!-- /wp:group -->
"""

FOOTER_PART = """<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group"><!-- wp:paragraph {"fontSize":"small"} --><p class="has-small-font-size"><!-- wp:site-title {"isLink":false} /--></p><!-- /wp:paragraph --></div>
<!-- /wp:group -->
"""


def php_head(a, what):
    return "<?php\n/**\n * " + what + "\n *\n * @package " + a.slug + "\n */\n\ndefined( 'ABSPATH' ) || exit;\n"


def block(a, root):
    w(root, "style.css", header(a))
    w(root, "theme.json", THEME_JSON)
    w(root, "templates/index.html", INDEX_HTML)
    w(root, "parts/header.html", HEADER_PART)
    w(root, "parts/footer.html", FOOTER_PART)
    w(root, "functions.php", php_head(a, "Theme setup."))


def classic(a, root):
    s = a.slug
    w(root, "style.css", header(a))
    px = prefix(a)
    w(root, "functions.php", php_head(a, "Theme setup.") + """
/**
 * Registers theme supports and menus.
 *
 * @since 0.0.1
 */
function """ + px + """_setup() {
	load_theme_textdomain( '""" + s + """', get_template_directory() . '/languages' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' ) );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'editor-styles' );
	register_nav_menus( array( 'primary' => esc_html__( 'Primary menu', '""" + s + """' ) ) );
}
add_action( 'after_setup_theme', '""" + px + """_setup' );

/**
 * Enqueues the theme stylesheet.
 *
 * @since 0.0.1
 */
function """ + px + """_enqueue_styles() {
	wp_enqueue_style( '""" + s + """', get_stylesheet_uri(), array(), wp_get_theme()->get( 'Version' ) );
}
add_action( 'wp_enqueue_scripts', '""" + px + """_enqueue_styles' );
""")
    w(root, "header.php", """<?php
defined( 'ABSPATH' ) || exit;
?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link screen-reader-text" href="#content"><?php esc_html_e( 'Skip to content', '""" + s + """' ); ?></a>
<header>
	<a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php bloginfo( 'name' ); ?></a>
	<?php wp_nav_menu( array( 'theme_location' => 'primary', 'container' => 'nav' ) ); ?>
</header>
<main id="content">
""")
    w(root, "footer.php", """<?php defined( 'ABSPATH' ) || exit; ?>
</main>
<footer><p><?php bloginfo( 'name' ); ?></p></footer>
<?php wp_footer(); ?>
</body>
</html>
""")
    w(root, "index.php", """<?php
defined( 'ABSPATH' ) || exit;
get_header();
if ( have_posts() ) {
	while ( have_posts() ) {
		the_post();
		get_template_part( 'template-parts/content', get_post_type() );
	}
	the_posts_pagination();
} else {
	get_template_part( 'template-parts/content', 'none' );
}
get_footer();
""")
    w(root, "template-parts/content.php", """<?php defined( 'ABSPATH' ) || exit; ?>
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
	<?php the_excerpt(); ?>
	<?php wp_link_pages(); ?>
</article>
""")
    w(root, "template-parts/content-none.php", "<?php defined( 'ABSPATH' ) || exit; ?>\n<p><?php esc_html_e( 'Nothing found.', '" + s + "' ); ?></p>\n")


def child(a, root):
    w(root, "style.css", header(a))
    px = prefix(a)
    w(root, "functions.php", php_head(a, "Child theme setup.") + """
/**
 * Enqueues the parent and child stylesheets.
 *
 * @since 0.0.1
 */
function """ + px + """_enqueue_styles() {
	$parent = wp_get_theme( get_template() );
	wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css', array(), $parent->get( 'Version' ) );
	wp_enqueue_style( '""" + a.slug + """', get_stylesheet_uri(), array( 'parent-style' ), wp_get_theme()->get( 'Version' ) );
}
add_action( 'wp_enqueue_scripts', '""" + px + """_enqueue_styles' );
""")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--type", choices=["block", "classic", "child"], required=True)
    p.add_argument("--parent")
    p.add_argument("--author")
    p.add_argument("--author-uri")
    p.add_argument("--theme-uri")
    p.add_argument("--description")
    p.add_argument("--tested-up-to", help="Only pass after testing on that WordPress version; otherwise the line is omitted")
    p.add_argument("--min-wp", default="6.4")
    p.add_argument("--min-php", default="7.4")
    p.add_argument("--out", default=".")
    p.add_argument("--zip", action="store_true")
    a = p.parse_args()
    if a.type == "child" and not a.parent:
        sys.exit("--parent is required for a child theme")
    letters = "".join(ch for ch in a.slug if ch.isalpha())
    if len(letters) < 4:
        sys.exit("slug needs at least 4 letters: the directory requires a prefix of four or more letters")
    low = a.name.lower()
    if "wordpress" in low or "theme" in low or low.startswith("twenty"):
        print("warning: the directory does not allow WordPress, Theme, or Twenty* in a theme name; consider a different name", file=sys.stderr)
    root = os.path.join(a.out, a.slug)
    if os.path.exists(root):
        sys.exit("refusing to overwrite " + root)
    {"block": block, "classic": classic, "child": child}[a.type](a, root)
    w(root, "readme.txt", "=== " + a.name + " ===\nRequires at least: " + a.min_wp + "\nRequires PHP: " + a.min_php +
      "\nStable tag: 0.0.1\nLicense: GPLv2 or later\nLicense URI: https://www.gnu.org/licenses/gpl-2.0.html\n\n== Description ==\n" +
      (a.description or a.name) + "\n\n== Changelog ==\n= 0.0.1 =\n* Initial version.\n")
    # Documentation standard (fswpdevops/references/coding-standards.md): README.md, CHANGELOG.md at 0.0.1,
    # docs/{setup,architecture,ops}.md and docs/features/ (index + one feature file). FILL IN: markers are
    # filled from the approved PRD before delivery; docs_gate.py fails on one left in a non-planned feature.
    w(root, "README.md", "# " + a.name + "\n\n" + (a.description or a.name) + "\n\nMore: [setup](docs/setup.md), [architecture](docs/architecture.md), "
      "[ops](docs/ops.md), [features](docs/features/README.md), [changelog](CHANGELOG.md).\n")
    w(root, "CHANGELOG.md", "# Changelog\n\nFormat: [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/); versions: "
      "[SemVer 2.0.0](https://semver.org/spec/v2.0.0.html). Pre-1.0 is beta.\n\n## [Unreleased]\n\n## [0.0.1] - "
      + datetime.date.today().isoformat() + "\n\n### Added\n- Initial " + a.type + " theme scaffold.\n")
    w(root, "docs/setup.md", "# Setup\n\n1. Use a local WordPress site.\n2. Put `" + a.slug + "` in `wp-content/themes/` and activate it.\n"
      "3. Quality gate: `run_gate.sh` and `docs_gate.py` from the fswpdevops-qa skill.\n")
    w(root, "docs/architecture.md", "# Architecture\n\n- Type: " + a.type + " theme. Templates, parts, patterns and `theme.json` define the site.\n"
      "- FILL IN: template hierarchy, style variations, patterns and any PHP as they appear.\n")
    w(root, "docs/ops.md", "# Ops\n\n- Release: move `[Unreleased]` in CHANGELOG.md into the new version; `style.css` Version and readme `Stable tag` move together.\n"
      "- Troubleshooting: FILL IN as issues are found.\n")
    w(root, "docs/features/README.md", "# Features\n\nOne file per feature. Keep this table current (status, since version).\n\n"
      "| Feature | Status | Since | File |\n|---|---|---|---|\n| Templates and styles | beta | 0.0.1 | [templates.md](templates.md) |\n")
    w(root, "docs/features/templates.md", """# Templates and styles

**Status:** beta | **Since:** 0.0.1 | **Updated:** 0.0.1

## Context
FILL IN: what the site looks like and does, who it is for.

## Behaviour
FILL IN: each template type, what the visitor sees with real and with empty content, states, edge cases.

## How it works
FILL IN: templates, parts, patterns, `theme.json` settings and styles, any PHP hooks, config.

## UI
FILL IN: text description of layout, header, footer, navigation and responsive behaviour (no screenshots needed).

## Limits & known issues
None yet.

## History
- 0.0.1: first version
""")
    print("created", root)
    if a.zip:
        print("zip:", shutil.make_archive(root, "zip", a.out, a.slug))


if __name__ == "__main__":
    main()
