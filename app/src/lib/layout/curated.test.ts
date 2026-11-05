// Curated layouts against the served view (DevLog-013 D505-D507): every source resolves, labels from rows are the stored
// strings, assumed shapes are dashed, and an output stays small enough to fetch per card.
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import type { ComponentsView } from '../components.svelte';
import { curatedScene, srcText, type CuratedLayout } from './curated.svelte';
import { MATERIALS } from './materials';
import { rowLabel } from './resolve';

const data = (f: string) => fileURLToPath(new URL('../../../static/data/' + f, import.meta.url));
const VIEW = JSON.parse(readFileSync(data('components.json'), 'utf-8')) as ComponentsView;
const dir = data('layouts');
const files = existsSync(dir) ? readdirSync(dir).filter((f) => f.endsWith('.json') && f !== 'index.json') : [];
const css = readFileSync(fileURLToPath(new URL('./layout.css', import.meta.url)), 'utf-8');

describe('curated layouts', () => {
	it('has at least the worked example', () => expect(files.length).toBeGreaterThan(0));
	it('index lists exactly the files', () => {
		const idx = JSON.parse(readFileSync(data('layouts/index.json'), 'utf-8'));
		expect(Object.keys(idx).sort()).toEqual(files.map((f) => f.replace(/\.json$/, '')).sort());
	});
	for (const f of files) {
		const l = JSON.parse(readFileSync(data('layouts/' + f), 'utf-8')) as CuratedLayout;
		const c = VIEW.components.find((x) => x.component_id === l.component_id);
		describe(l.component_id, () => {
			it('names a component in the view, with sources and a cross-section', () => {
				expect(c).toBeTruthy();
				expect(l.sources.length).toBeGreaterThan(0);
				// a cross-section unless a view is withheld with a stated reason (D510)
				expect(l.views.some((v) => v.kind === 'xsec') || l.not_drawn.length > 0).toBe(true);
			});
			it('stays below 400 KB', () => expect(statSync(data('layouts/' + f)).size).toBeLessThan(400_000));
			if (!c) return;
			for (const v of l.views) {
				const s = curatedScene(l, v, c);
				it(`${v.id}: draws shapes of known materials`, () => {
					expect(s.shapes.length).toBeGreaterThan(0);
					for (const sh of s.shapes) {
						expect(MATERIALS[sh.mat], sh.mat).toBeTruthy();
						expect(css, sh.mat).toContain(`--m-${sh.mat}:`);
					}
				});
				it(`${v.id}: every source resolves and assumed means dashed`, () => {
					for (const sh of v.shapes) {
						expect(sh.src.length).toBeGreaterThan(0);
						for (const x of sh.src) expect(srcText(c, x), x).not.toMatch(/^row m\d+$/);
						if (sh.src.some((x) => x.startsWith('assumed:'))) expect(s.shapes.find((y) => y.rings === sh.r)?.schematic).toBe(true);
					}
				});
				it(`${v.id}: row labels are the stored strings, free labels state a source`, () => {
					for (const m of v.marks) {
						if (m.row) {
							const row = c.metrics.find((x) => x.metric_id.endsWith('-' + m.row));
							expect(row, m.row).toBeTruthy();
							expect(m.text).toBe('');
							expect(s.marks.some((sm) => sm.dim.label === rowLabel(row!))).toBe(true);
						} else {
							expect(m.src.length).toBeGreaterThan(0);
							expect(m.src.some((x) => x.startsWith('assumed:')), `assumed value labelled: ${m.text}`).toBe(false);
						}
					}
				});
			}
		});
	}
});
