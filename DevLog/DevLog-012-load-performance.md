# DevLog-012: Load performance

| | |
|---|---|
| Date | 2026-11-03 |
| Status | Implemented locally; deployment pending |
| Scope | app/ (SvelteKit static site), deploy unchanged; views from scripts/build_views.py unchanged |

## Requirement

Any tab, page or subpage starts showing and loading within 100 ms (10 ms preferred). Data may fill in afterwards, but
something real is on screen by then and the main thread stays responsive.

## Baseline: deployed site, 2026-11-03

`node app/scripts/perf.mjs https://outside5sigma.com/photonics-atlas`, real Chromium, 1440 x 900, no throttling, edge SJC. paint = first contentful paint (cold, warm) or click to active tab painted (spa).

| Route | cold paint | warm paint | spa paint | spa data on screen | worst task | blocked |
|---|---|---|---|---|---|---|
| / | 776 | 192 | 40 | 40 | 495 | 445 |
| /orgs | 792 | 176 | 439 | 439 | 316 | 293 |
| /components | 896 | 608 | 326 | 2813 | 970 | 1309 |
| /supply | 624 | 208 | 457 | 894 | 349 | 343 |
| /people | 696 | 152 | 352 | 911 | 69 | 20 |
| /layout | 644 | 188 | 583 | 583 | 138 | 88 |
| /explore | 1264 | 200 | 478 | 652 | 371 | 359 |
| /about | 624 | 192 | 330 | 330 | 123 | 73 |

All times ms. Network by curl: TLS done 86 ms, HTML TTFB 186-190 ms; `cf-cache-status: DYNAMIC`, so Cloudflare does not
cache; GitHub Pages sets `max-age=600` on everything including hashed chunks.

## Causes

1. `ssr = false`: HTML body is empty. Nothing paints until the CSS, about 20 module chunks and the registry load.
2. Tab click waits for the route chunk over the network (about one TTFB) with no feedback.
3. `/components` renders all 18165 value rows (about 200k nodes): 1.3 s frozen. `comp` is also a deep `$state` proxy.
4. Plotly full bundle: 4.6 MB raw, one long task on eval, and up to 13 synchronous renders on /explore.
5. components.json: 9.5 MB parsed in one task. /orgs/hub fetches 15 MB of views for one organization.
6. Pages render nothing at all while data is loading (`{:else if view}` with no else).

## Plan

- [x] Prerender real HTML (SSR at build): header, nav, page frame. CSS inlined, so paint needs no second request.
- [x] Summary (`parts/summary.json`, about 2 KB) inlined in every page: dashboard and header paint with real numbers.
- [x] Instant tab feedback from `navigating`: active tab and a skeleton overlay on the click, whatever the network does.
- [x] Route code preloaded on viewport; data loading starts on nav hover.
- [x] Service worker: precached shell and code, data cached after first use, per deploy version.
- [x] Value table and org table windowed (300 rows, +300 on scroll), same pattern as /people.
- [x] Components and people views split into parts at build time (`app/scripts/shard-data.mjs`, gitignored output);
      canonical JSON in static/data stays as is. Table grows part by part; other consumers still see only complete data.
- [x] Layout gallery cards from the showcase part, independent of the full download.
- [x] Plotly cartesian bundle; charts render when scrolled near, one per task.
- [x] Skeletons on every page while data loads.
- [ ] Deploy and rerun perf.mjs against the live site.
- [ ] Cloudflare cache rule (outside this repo; see Follow-ups).

## Follow-ups

- First-visit paint cannot beat the first response: TLS done 86 ms, HTML TTFB 186-190 ms, and Cloudflare reports
  `cf-cache-status: DYNAMIC`. A Cloudflare Cache Rule on this path (cache everything, edge TTL) is the remaining lever; it
  has to be set in the dashboard and purged on deploy. Not done.
- `/explore/` and the like with a trailing slash return 404 on the deployed site (pre-existing, not changed here).

## Progress

- 2026-11-03: baseline measured, plan written.
- 2026-11-03: implemented. Local timing with `app/scripts/perf-serve.mjs --delay=190` (base path, gzip, max-age=600, fixed
  190 ms per response standing in for the measured first-byte time; HTTP/1.1, so module and data rounds are slower than the
  real HTTP/2): first-visit paint 240-256 ms, repeat paint 88-120 ms, tab click to paint 5-44 ms (at 4x CPU 8-53 ms).
- 2026-11-03: repeat paint floor. A one-line page from localhost in the same browser paints at 64-88 ms; ours is 72-116 ms
  with the worker answering in about 1 ms, so 10-30 ms is the app.
- 2026-11-03: redeploy test found stale pages: the new worker's install fetch was answered by the HTTP cache, pinning the
  previous deploy's HTML in the new cache. Fixed (`cache: 'reload'` for unhashed files). A deploy now shows on the second
  load after it, the old cache is removed.

## Audit (fresh context, 2026-11-03)

| # | Finding | Outcome |
|---|---|---|
| 1 | Stale HTML precached from the HTTP cache | Fixed (same as the redeploy test) |
| 2 | Root page stored as `/base/`, looked up as `/base`: dashboard never served by the worker | Confirmed by reading; was masked by the HTTP cache in my offline test. Fixed; verified offline with HTTP cache disabled |
| 3 | `/orgs/hub` without an id showed a skeleton forever | Fixed; message back |
| 4 | Spinner stuck on a failed Plotly load or render; failed import memoized | Fixed |
| 5 | Partial counts on /components read as totals | Fixed: counts appear only when all parts are in |
| 6 | `?v=` does not version what the host serves; a load spanning a deploy could silently drop rows | Fixed: loaders check totals and show an error asking for a reload; comment corrected |
| 7 | Ctrl+F and print reach only rendered rows on windowed tables | Accepted trade-off, same as /people; in-page search covers all rows |
| 8 | Theme icon wrong for light theme before hydration | Fixed: icon follows the attribute through CSS |
| - | Possible duplicate downloads from removed preload links (speculative) | Passed locally at first, then confirmed on the live site: hydration removed the links, cancelling parts 0-9 (`ERR_ABORTED`), which restarted about 200 ms later. Fixed: links stay through hydration |
| - | Worker on the dev server (speculative) | Disabled on `vite dev` |

Found while verifying: first-visit data bypassed the worker, so the next visit waited on the network. The page now
re-requests it through the worker when the worker takes over (HTTP cache, no download).
