// Gallery of the layout viewer: showcase components per template (D105), or, while a template has no showcase rows,
// the components with the most reported template dimensions (clearly labelled as a fallback).
import type { Component, ComponentsView, LayoutTemplate, ShowcaseRow } from '../components.svelte';
import { primaryMetric, resolve, type Primary, type Resolved } from './resolve';

export interface Card {
	c: Component;
	r: Resolved;
	role: string;
	show?: ShowcaseRow;
	primary: Primary;
}
export interface Group {
	id: string;
	t: LayoutTemplate;
	served: number;
	withGeometry: number;
	/** No showcase rows anywhere yet: cards are the components with the most reported template dimensions. */
	fallback: boolean;
	cards: Card[];
	/** Showcase roles with no row for this template (D112: shown as gaps, never filled). */
	gaps: string[];
}

const ROLE_ORDER: Record<string, number> = { hero: 0, typical: 1 };

export function gallery(view: ComponentsView, perTemplate = 4): Group[] {
	const byId = new Map(view.components.map((c) => [c.component_id, c]));
	const out: Group[] = [];
	for (const [id, t] of Object.entries(view.layouts ?? {})) {
		const served = view.components.filter((c) => t.applies_to.includes(c.class));
		const res = served.map((c) => resolve(c, view)).filter((r): r is Resolved => r !== null);
		const withGeometry = res.filter((r) => r.reported > 0).length;
		const rows = (view.showcase ?? []).filter((s) => s.template === id && byId.has(s.component_id));
		const anyShowcase = (view.showcase ?? []).length > 0;
		let cards: Card[];
		if (anyShowcase) {
			cards = rows
				.slice()
				.sort((a, b) => (ROLE_ORDER[a.role] ?? 9) - (ROLE_ORDER[b.role] ?? 9) || Number(a.rank ?? 99) - Number(b.rank ?? 99) || a.component_id.localeCompare(b.component_id))
				.flatMap((s) => {
					const c = byId.get(s.component_id) as Component;
					const r = resolve(c, view);
					return r ? [{ c, r, role: s.role, show: s, primary: primaryMetric(c, id, t) }] : [];
				});
		} else {
			cards = res
				.filter((r) => r.reported > 0)
				.map((r) => ({ c: r.comp, r, role: 'fallback', primary: primaryMetric(r.comp, id, t) }))
				.sort((a, b) => b.r.reported - a.r.reported || (b.primary.row ? 1 : 0) - (a.primary.row ? 1 : 0) || a.c.component_id.localeCompare(b.c.component_id))
				.slice(0, perTemplate);
		}
		const gaps = anyShowcase ? ['hero', 'typical'].filter((role) => !rows.some((s) => s.role === role)) : [];
		out.push({ id, t, served: served.length, withGeometry, fallback: !anyShowcase, cards, gaps });
	}
	return out;
}
