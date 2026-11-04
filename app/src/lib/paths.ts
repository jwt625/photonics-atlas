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

// On a first visit, code and data load before the service worker takes over, so they would miss its cache and the next
// visit would wait on the network. Request them again through the worker when it does, including what is still in flight
// at that moment: the HTTP cache answers, no download.
function handOverToWorker(): void {
	const seen = new Set<string>();
	const root = location.origin + link('/');
	const again = (entries: PerformanceEntryList) => {
		for (const { name } of entries) {
			if (seen.has(name) || !name.startsWith(root)) continue;
			seen.add(name);
			fetch(name).catch(() => {});
		}
	};
	again(performance.getEntriesByType('resource'));
	new PerformanceObserver((list) => again(list.getEntries())).observe({ type: 'resource' });
}
if (browser) {
	try {
		if ('serviceWorker' in navigator && !navigator.serviceWorker.controller) navigator.serviceWorker.addEventListener('controllerchange', handOverToWorker, { once: true });
	} catch {
		/* no service worker here, e.g. a sandboxed frame */
	}
}

export async function getJson<T>(file: string): Promise<T> {
	const res = await fetch(dataUrl(file));
	if (!res.ok) throw new Error(`${file}: HTTP ${res.status}`);
	return (await res.json()) as T;
}
