// Real generated view (static/data/history.json, built by scripts/build_history_view.py).
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { layoutTimeline, OTHER, palette, shownMask, type HistoryView } from './layout';

const hv = JSON.parse(readFileSync(new URL('../../../static/data/history.json', import.meta.url), 'utf-8')) as HistoryView;

describe('history timeline layout', () => {
	for (const w of [1440, 900, 390]) {
		it(`keeps every node inside ${w} px and in date order`, () => {
			const l = layoutTimeline(hv.milestones, hv.eras, w);
			expect(l.mobile).toBe(w <= 700);
			expect(l.bands.length).toBe(hv.eras.length);
			let prev = -Infinity;
			for (const n of l.nodes) {
				expect(n.x).toBeGreaterThanOrEqual(0);
				expect(n.x).toBeLessThanOrEqual(w);
				expect(n.y).toBeGreaterThanOrEqual(prev);
				prev = n.y;
			}
			expect(l.height).toBeGreaterThan(prev);
		});
	}
	it('palette covers every milestone', () => {
		for (const mode of ['thread', 'inst', 'material', 'era'] as const) {
			const p = palette(hv.milestones, hv.eras, mode);
			expect(p.items.length).toBeLessThanOrEqual(mode === 'inst' || mode === 'material' ? 11 : 12);
			for (const m of hv.milestones) expect(p.color.has(p.key(m)) || p.key(m) === OTHER).toBe(true);
			expect(p.items.reduce((s, it) => s + it.n, 0)).toBe(hv.milestones.length);
		}
	});
	// story thumbnail cards (compact view): pick a few milestones spread over the eras
	const cards = new Set(hv.milestones.filter((_, i) => i % 9 === 3).map((m) => m.id));
	for (const w of [1440, 900, 390]) {
		it(`thumbnail rows get room without overlap at ${w} px; plain rows unchanged`, () => {
			const plain = layoutTimeline(hv.milestones, hv.eras, w);
			const l = layoutTimeline(hv.milestones, hv.eras, w, cards);
			expect(l.thumb.filter(Boolean).length).toBe(cards.size);
			expect(l.thumbW / l.thumbH).toBeCloseTo(1.6, 1);
			expect(l.height).toBeGreaterThan(plain.height);
			// vertical extent of every node; nodes in date order must not overlap the next row / node
			const ext = l.nodes.map((n, i) =>
				l.mobile
					? { top: n.y - 7, bot: n.y + (l.thumb[i] ? l.thumbH + 32 : 43) }
					: { top: n.y - (l.thumb[i] ? l.thumbH / 2 : 7), bot: n.y + (l.thumb[i] ? l.thumbH / 2 + 46 : 53) }
			);
			const rows = [...new Set(l.nodes.map((n) => n.y))].sort((a, b) => a - b);
			for (let r = 1; r < rows.length; r++) {
				const prevBot = Math.max(...l.nodes.map((n, i) => (n.y === rows[r - 1] ? ext[i].bot : -Infinity)));
				const top = Math.min(...l.nodes.map((n, i) => (n.y === rows[r] ? ext[i].top : Infinity)));
				expect(top).toBeGreaterThanOrEqual(prevBot);
			}
			// band headers clear the rows around them
			for (const b of l.bands) for (const e of ext) expect(e.bot <= b.y || e.top >= b.y + b.h).toBe(true);
			// the path passes through every node (desktop: on the row line; mobile: the vertical line)
			for (const n of l.nodes) expect(l.path.includes(l.mobile ? `M${n.x},` : `${n.y}`)).toBe(true);
			// with no cards the layout is the plain one
			expect(layoutTimeline(hv.milestones, hv.eras, w, new Set())).toEqual(plain);
			if (!l.mobile) {
				// plain rows keep the 92 px pitch inside an era
				const ys = [...new Set(plain.nodes.map((n) => n.y))].sort((a, b) => a - b);
				expect(ys.slice(1).map((y, i) => y - ys[i])).toContain(92);
			}
		});
	}
	it('stories filter combines with legend and search (AND)', () => {
		const ms = hv.milestones;
		const stories = new Set(ms.slice(0, 5).map((m) => m.id));
		const hay = ms.map(() => 'laser fiber');
		const base = { only: new Set<string>(), key: (m: (typeof ms)[number]) => m.thread, terms: [] as string[], hay, stories };
		expect(shownMask(ms, { ...base, storiesOnly: false }).filter(Boolean).length).toBe(ms.length);
		expect(shownMask(ms, { ...base, storiesOnly: true }).filter(Boolean).length).toBe(5);
		expect(shownMask(ms, { ...base, storiesOnly: true, terms: ['nothing'] }).filter(Boolean).length).toBe(0);
		const th = ms[0].thread;
		const n = ms.slice(0, 5).filter((m) => m.thread === th).length;
		expect(shownMask(ms, { ...base, storiesOnly: true, only: new Set([th]) }).filter(Boolean).length).toBe(n);
	});
});
