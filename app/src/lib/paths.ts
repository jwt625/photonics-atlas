import { asset, resolve } from '$app/paths';
import { browser, version } from '$app/env';

/** App-internal link honoring the configured base path (BASE_PATH). */
export function link(path: string): string {
	return resolve(path as '/');
}

/** URL of a file in static/ honoring the base path. */
export function staticUrl(file: string): string {
	return asset(file as 'favicon.svg');
}

/** URL of a data file, tied to the build in browser and worker caches. The host ignores the query, so a load that spans a
 *  deploy can still mix files: the loaders of split views check their totals. */
export function dataUrl(file: string): string {
	return `${staticUrl(file)}?v=${version}`;
}

// On a first visit, data is fetched before the service worker takes over, so it would miss the worker's cache and the next
// visit would wait on the network. Fetch it again through the worker when it does: the HTTP cache answers, no download.
const fetched = new Set<string>();
if (browser && 'serviceWorker' in navigator && !navigator.serviceWorker.controller) {
	navigator.serviceWorker.addEventListener('controllerchange', () => {
		for (const u of fetched) fetch(u).catch(() => {});
	});
}

export async function getJson<T>(file: string): Promise<T> {
	fetched.add(dataUrl(file));
	const res = await fetch(dataUrl(file));
	if (!res.ok) throw new Error(`${file}: HTTP ${res.status}`);
	return (await res.json()) as T;
}
