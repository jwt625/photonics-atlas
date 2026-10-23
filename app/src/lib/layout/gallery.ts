// Gallery of the layout viewer: showcase components per template (D105), or, while a template has no showcase rows,
// the components with the most reported template dimensions (clearly labelled as a fallback).
import type { Component, ComponentsView, LayoutTemplate, ShowcaseRow } from '../components.svelte';
import { familyShort, platformFamily } from '../explore/colors';
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
	/** Showcase roles with no row for this template, and platform-qualified gaps declared in the template (D112, D223):
	 *  shown as gaps, never filled. */
	gaps: Gap[];
	/** cards and gaps in one role-ordered list (hero, typical, then the rest; cards before gaps within a role) */
	items: Item[];
}
export type Item = { kind: 'card'; role: string; card: Card } | { kind: 'gap'; role: string; gap: Gap };
export interface Gap {
	role: string;
	/** Platform family short label for a platform-qualified gap (e.g. SOI); empty for a role gap. */
	platform: string;
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
		const gaps: Gap[] = anyShowcase ? ['hero', 'typical'].filter((role) => !rows.some((s) => s.role === role)).map((role) => ({ role, platform: '' })) : [];
		// Platform-qualified gaps (component_layouts.yaml `gaps`): shown while no card of that role has that platform family.
		if (anyShowcase)
			for (const g of t.gaps ?? [])
				if (!gaps.some((x) => x.role === g.role) && !cards.some((cd) => cd.role === g.role && platformFamily(cd.c.platform) === g.platform_family))
					gaps.push({ role: g.role, platform: familyShort(g.platform_family) });
		const items: Item[] = [...cards.map((card) => ({ kind: 'card' as const, role: card.role, card })), ...gaps.map((gap) => ({ kind: 'gap' as const, role: gap.role, gap }))]
			.map((x, i) => ({ x, i }))
			.sort((a, b) => (ROLE_ORDER[a.x.role] ?? 9) - (ROLE_ORDER[b.x.role] ?? 9) || a.i - b.i)
			.map((y) => y.x);
		out.push({ id, t, served: served.length, withGeometry, fallback: !anyShowcase, cards, gaps, items });
	}
	return out;
}
