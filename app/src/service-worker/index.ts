// Repeat visits come from here, not the network (DevLog-012). One cache per deploy: pages are precached on install, code
// and data are stored on first use, so a visitor downloads nothing they do not need. The browser updates this worker in the
// background, so a deploy shows from the next load after it was noticed.
import { version } from '$app/env';
import { assets, prerendered } from '$app/manifest';
import { asset, resolve } from '$app/paths';
import { self as sw } from '$app/service-worker';

// CacheStorage is per origin, and other apps share this origin under their own paths: touch only this app's caches
const PREFIX = 'photonics-atlas-';
const CACHE = PREFIX + version;
const DATA = asset('/data/' as '/favicon.svg');
const PRECACHE = [...prerendered.map((f) => resolve(f.path as '/')), ...assets.map((f) => asset(f.path)).filter((p) => !p.startsWith(DATA))];
const hashed = (path: string) => path.includes('/_app/immutable/');

/** Pages ignore the query (client-side state) and a trailing slash: the root is stored and asked for with and without. */
const pageKey = (url: URL) => url.origin + (url.pathname.replace(/\/$/, '') || '/');

/** A navigation may not be answered with a redirected response: GitHub Pages redirects the root to a trailing slash. */
async function unredirected(res: Response): Promise<Response> {
	return res.redirected ? new Response(await res.blob(), { status: res.status, statusText: res.statusText, headers: res.headers }) : res;
}

sw.addEventListener('install', (e) => {
	e.waitUntil(
		(async () => {
			const cache = await caches.open(CACHE);
			await Promise.all(
				PRECACHE.map(async (p) => {
					// Pages keep their URL across deploys and the host sends max-age=600: a plain fetch could pin the previous
					// deploy's page into this deploy's cache.
					const res = await fetch(p, { cache: 'reload' });
					if (!res.ok) throw new Error(`${p}: HTTP ${res.status}`);
					await cache.put(pageKey(new URL(p, location.origin)), await unredirected(res));
				})
			);
			await sw.skipWaiting();
		})()
	);
});

sw.addEventListener('activate', (e) => {
	e.waitUntil(
		(async () => {
			// The newest previous cache stays: a returning visitor's first load after a deploy runs the old page, whose hashed
			// files the host may no longer have. pa-: this app's earlier name.
			const keys = await caches.keys();
			const mine = keys.filter((k) => k.startsWith(PREFIX) && k !== CACHE).sort();
			for (const k of [...mine.slice(0, -1), ...keys.filter((k) => k.startsWith('pa-'))]) await caches.delete(k);
			await sw.clients.claim();
		})()
	);
});

async function respond(e: FetchEvent, url: URL): Promise<Response> {
	const key = e.request.mode === 'navigate' ? pageKey(url) : url.href;
	const cache = await caches.open(CACHE).catch(() => null);
	const hit = await cache?.match(key);
	if (hit) return hit;
	if (hashed(url.pathname)) {
		// in the previous deploy's cache: a file of the old page, or one this deploy did not change, so no new download
		const old = await caches.match(key);
		if (old) {
			if (cache) e.waitUntil(cache.put(key, old.clone()).catch(() => {}));
			return old;
		}
	}
	const res = await fetch(e.request);
	// in the background: a large file reaches the page as it downloads
	if (res.ok && cache && (hashed(url.pathname) || url.pathname.startsWith(DATA))) e.waitUntil(cache.put(key, res.clone()).catch(() => {}));
	return res;
}

sw.addEventListener('fetch', (e) => {
	const url = new URL(e.request.url);
	if (e.request.method !== 'GET' || url.origin !== location.origin) return;
	e.respondWith(respond(e, url));
});
