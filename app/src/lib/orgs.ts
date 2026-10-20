import type { Org } from './types';

export type SortDir = 'asc' | 'desc';
export const CORPORA = ['eo', 'pk', 'ofc2026', 'lin'] as const;

/** Case- and accent-insensitive match on name, id, aliases and printed strings. */
export function fold(s: string): string {
	return s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase();
}

export function matches(o: Org, q: string): boolean {
	if (!q) return true;
	const f = fold(q);
	if (fold(o.name).includes(f) || o.id.includes(f)) return true;
	return o.aliases.some((a) => fold(a.alias).includes(f)) || o.printed.some((p) => fold(p.printed).includes(f));
}

export function sortKey(o: Org, key: string): string | number {
	if (key.startsWith('rows.')) return o.rows[key.slice(5)] ?? 0;
	if (key === 'aliases') return o.aliases.length;
	if (key === 'events') return o.events.length;
	const v = (o as unknown as Record<string, unknown>)[key];
	return typeof v === 'string' ? fold(v) : Number(v ?? 0);
}

export function sortOrgs(list: Org[], key: string, dir: SortDir): Org[] {
	const s = dir === 'asc' ? 1 : -1;
	return [...list].sort((a, b) => {
		const x = sortKey(a, key), y = sortKey(b, key);
		if (x === y) return a.name.localeCompare(b.name);
		return x < y ? -s : s;
	});
}
