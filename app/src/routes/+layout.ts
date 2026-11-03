import { dataUrl } from '../lib/paths';
import type { Summary } from '../lib/types';

export const prerender = true;
export const trailingSlash = 'never';

// Fetched at prerender and inlined in every page's HTML, so the dashboard and header paint with real numbers on first
// bytes. Query parameters and hash state stay client-side.
export const load = async ({ fetch }: { fetch: typeof globalThis.fetch }): Promise<{ summary: Summary }> => {
	const res = await fetch(dataUrl('data/parts/summary.json'));
	if (!res.ok) throw new Error(`summary.json: HTTP ${res.status}`);
	return { summary: (await res.json()) as Summary };
};
