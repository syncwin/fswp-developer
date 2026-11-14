---
name: fswpdevops-performance
description: Use for WordPress performance work in Full-Stack WP DevOps. Domain skill for WordPress performance in Full-Stack WP DevOps. Covers measuring first (Query Monitor, profiling, Server-Timing), database and query patterns, object cache and transients, autoloaded options, asset loading, remote calls, cron and background work, and front-end vitals for plugins, themes, and Core patches. Use when code is slow, when writing queries or loops, or when the PRD lists performance requirements.
---

# FSWPDevOps Performance Engineer

Measure, then change. Do not add caching or clever code to something that has not been shown slow. Record the before and after numbers in the change brief or PR text.

## Measure

- **Query Monitor** (plugin) for queries, hooks, HTTP calls, and slow code per request.
- The command-line profiler (`wp profile stage`, `wp profile hook`) for load stages and hook cost, where the command line is available.
- `SAVEQUERIES` and `Server-Timing` headers in a development environment.
- Browser DevTools and Lighthouse for LCP, INP, and CLS on the front end.

## Database

- Bound every query: set `posts_per_page` (never -1 on unbounded data), `no_found_rows => true` when pagination is not needed, and `fields => 'ids'` when you only need IDs.
- Avoid queries inside loops (N+1): fetch in one query, or prime caches with `update_post_meta_cache`/`update_object_term_cache` defaults or `_prime_post_caches`.
- `meta_query` and `tax_query` on large tables are expensive; prefer a taxonomy for filterable values, or a custom indexed table for heavy data. Add indexes in `dbDelta` for columns you filter or sort by.
- Use `$wpdb->prepare()` always; select only needed columns.

## Options, transients, object cache

- Autoloaded options load on every request. Store large or rarely used values with autoload off (`add_option( $k, $v, '', false )` / `update_option( $k, $v, false )`, or `wp_set_option_autoload()`).
- Transients (`set_transient`) for expensive results with an expiry. Use `wp_cache_get/set` with a group for per-request or persistent object cache; design for the cache being absent.
- Cache invalidation is part of the feature: clear on the events that change the data.
- Never let logs, per-request meta, or transients grow without a cap or expiry.

## Assets

- Enqueue only where needed, inside the render callback or a conditional; no site-wide loading for one page.
- Use `wp_enqueue_script( $handle, $src, $deps, $ver, array( 'strategy' => 'defer', 'in_footer' => true ) )`.
- Version assets for cache-busting; ship minified builds with source; avoid large libraries for small jobs; no render-blocking third-party requests.
- Images: correct sizes and `srcset` (core does this for attachments), lazy-load below the fold, prioritize the LCP image.

## Requests and background work

- Remote calls: set a timeout, cache the response, handle failure, and never call on every page view.
- Do heavy or slow work in cron or a queued job, not in a page request. `wp_schedule_event` depends on site traffic unless a real system cron triggers `wp-cron.php`; batch work and make jobs idempotent.
- Avoid heavy work on hot hooks (`init`, `wp_head`, `the_content`, `pre_get_posts`).
- The Heartbeat API and admin-ajax polling can flood servers; throttle.

## Front-end vitals

Reserve space for late content (CLS), keep main-thread JS small (INP), avoid layout thrash, and prefer CSS over JS for effects. Themes: fewer, smaller stylesheets; remove unused block styles only when you are sure.

## Report

State the metric, method, before, after, and the trade-off. If it was not measured, say "not measured".

Finish with a scratchpad: measurements before and after, changes, open items.
