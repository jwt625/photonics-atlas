// Real generated view (static/data/history.json, built by scripts/build_history_view.py).
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { layoutTimeline, OTHER, palette, type HistoryView } from './layout';

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
});
