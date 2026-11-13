# Classic theme scaffold file contents

Exact file bodies for the classic type in `scaffold_theme.md`. Tokens (`<slug>`, `<px>`, ...) are described in `scaffold_theme_files.md`. Everything between the fences is the file; PHP files use LF and tabs as shown.

## Classic theme files

### `functions.php (classic theme)`

```php
<?php
/**
 * Theme setup.
 *
 * @package <slug>
 */

defined( 'ABSPATH' ) || exit;

/**
 * Registers theme supports and menus.
 *
 * @since 0.0.1
 */
function <px>_setup() {
	load_theme_textdomain( '<slug>', get_template_directory() . '/languages' );
	add_theme_support( 'title-tag' );
	add_theme_support( 'automatic-feed-links' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support( 'html5', array( 'search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script' ) );
	add_theme_support( 'responsive-embeds' );
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'editor-styles' );
	register_nav_menus( array( 'primary' => esc_html__( 'Primary menu', '<slug>' ) ) );
}
add_action( 'after_setup_theme', '<px>_setup' );

/**
 * Enqueues the theme stylesheet.
 *
 * @since 0.0.1
 */
function <px>_enqueue_styles() {
	wp_enqueue_style( '<slug>', get_stylesheet_uri(), array(), wp_get_theme()->get( 'Version' ) );
}
add_action( 'wp_enqueue_scripts', '<px>_enqueue_styles' );
```

### `header.php`

```php
<?php
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
<a class="skip-link screen-reader-text" href="#content"><?php esc_html_e( 'Skip to content', '<slug>' ); ?></a>
<header>
	<a href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php bloginfo( 'name' ); ?></a>
	<?php wp_nav_menu( array( 'theme_location' => 'primary', 'container' => 'nav' ) ); ?>
</header>
<main id="content">
```

### `footer.php`

```php
<?php defined( 'ABSPATH' ) || exit; ?>
</main>
<footer><p><?php bloginfo( 'name' ); ?></p></footer>
<?php wp_footer(); ?>
</body>
</html>
```

### `index.php`

```php
<?php
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
```

### `template-parts/content.php`

```php
<?php defined( 'ABSPATH' ) || exit; ?>
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
	<h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
	<?php the_excerpt(); ?>
	<?php wp_link_pages(); ?>
</article>
```

### `template-parts/content-none.php`

```php
<?php defined( 'ABSPATH' ) || exit; ?>
<p><?php esc_html_e( 'Nothing found.', '<slug>' ); ?></p>
```
