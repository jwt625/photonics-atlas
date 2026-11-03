// Repeat visits come from here, not the network (DevLog-012). One cache per deploy: pages and code are precached on
// install, data files on first use. The browser updates this worker in the background, so a deploy shows from the next
// load after it was noticed.
import { version } from '$app/env';
import { assets, immutable, prerendered } from '$app/manifest';
import { asset, resolve } from '$app/paths';
import { self as sw } from '$app/service-worker';

const CACHE = `pa-${version}`;
const DATA = asset('/data/' as '/favicon.svg');
const PRECACHE = [
	...immutable.map((f) => asset(f.path as '/favicon.svg')),
	...prerendered.map((f) => resolve(f.path as '/')),
	...assets.map((f) => asset(f.path)).filter((p) => !p.startsWith(DATA))
];

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
					// deploy's page into this deploy's cache. Hashed files can use the HTTP cache.
					const res = await fetch(p, { cache: p.includes('/immutable/') ? 'default' : 'reload' });
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
			for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
			await sw.clients.claim();
		})()
	);
});

async function respond(req: Request, url: URL): Promise<Response> {
	const key = req.mode === 'navigate' ? pageKey(url) : url.href;
	const cache = await caches.open(CACHE).catch(() => null);
	const hit = await cache?.match(key);
	if (hit) return hit;
	const res = await fetch(req);
	if (res.ok && cache && url.pathname.startsWith(DATA)) await cache.put(key, res.clone()).catch(() => {});
	return res;
}

sw.addEventListener('fetch', (e) => {
	const url = new URL(e.request.url);
	if (e.request.method !== 'GET' || url.origin !== location.origin) return;
	e.respondWith(respond(e.request, url));
});
