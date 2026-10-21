import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import type { Component, ComponentsView, Metric } from '../components.svelte';
import { gallery } from './gallery';
import { scanMaterials, stackOf } from './materials';
import { pickOrder, primaryMetric, resolve, segmentRows, templateFor } from './resolve';
import { buildScenes, sceneTexts } from './scene';

const VIEW = JSON.parse(readFileSync(fileURLToPath(new URL('../../../static/data/components.json', import.meta.url)), 'utf-8')) as ComponentsView;

let n = 0;
const m = (x: Partial<Metric>): Metric => ({ metric_id: `cmp_t-m${++n}`, parameter: 'width_nm', value: '500', unit: 'nm', basis: 'design_target', locator: 'p.1', ...x });
const C = (cls: string, metrics: Metric[], extra: Partial<Component> = {}): Component => ({
	component_id: 'cmp_t', source_id: 'eo:t', class: cls, label: 't', row_kind: 'fabricated', verified_on: '2026-10-20', fab_orgs: [],
	source: { id: 'eo:t', title: '', year: '', venue: '', url: '', access: '' }, metrics, ...extra
});
const NUM = /(?<![A-Za-z_\d.])\d+(?:\.\d+)?/g; // numbers, not digits inside identifiers (layer2_thickness_nm)

describe('resolver', () => {
	it('maps classes to templates', () => {
		expect(templateFor('resonator.ring', VIEW.layouts)).toBe('ring_bus');
		expect(templateFor('fiber_chip_coupler.grating', VIEW.layouts)).toBe('gc_1d');
		expect(templateFor('modulator.mzm', VIEW.layouts)).toBeNull();
	});
	it('picks design before measured, skips std, exposes alternatives, converts nm to um', () => {
		const rows = [
			m({ parameter: 'tip_width_nm', value: '300', qualifier: 'approx', basis: 'measured' }),
			m({ parameter: 'tip_width_nm', value: '20', statistic: 'std', basis: 'measured' }),
			m({ parameter: 'tip_width_nm', value: '200' })
		];
		expect(pickOrder(rows)[0].value).toBe('200');
		const r = resolve(C('fiber_chip_coupler.edge', rows), VIEW)!;
		const d = r.dims.tip_width_nm;
		expect(d.label).toBe('200 nm');
		expect(d.num).toBeCloseTo(0.2);
		expect(d.alts.map((a) => a.value)).toEqual(['300', '20']);
		expect(d.basis).toBe('design');
		expect(r.missingRequired).toContain('taper_length_um');
		expect(r.dims.taper_length_um.label).toBe('not reported');
	});
	it('labels ranges and bounds with the stored strings, draws a range at its midpoint', () => {
		const r = resolve(C('resonator.ring', [m({ parameter: 'radius_um', value: '10', value_max: '20', unit: 'um' }), m({ parameter: 'gap_nm', value: '200', qualifier: 'lt' })]), VIEW)!;
		expect(r.dims.radius_um.label).toBe('10-20 µm');
		expect(r.dims.radius_um.num).toBe(15);
		expect(r.dims.gap_nm.label).toBe('< 200 nm');
	});
	it('treats rows that differ by condition as segments, never summed in a label', () => {
		const c = C('fiber_chip_coupler.edge', [
			m({ parameter: 'taper_length_um', value: '250', unit: 'um', condition: 's1' }),
			m({ parameter: 'taper_length_um', value: '150', unit: 'um', condition: 's2' }),
			m({ parameter: 'tip_width_nm', value: '200' })
		]);
		expect(segmentRows(c, 'taper_length_um').map((x) => x.value)).toEqual(['250', '150']);
		const s = buildScenes(resolve(c, VIEW)!).top;
		const labels = s.marks.map((x) => x.dim.label);
		expect(labels).toContain('250 µm');
		expect(labels).toContain('150 µm');
		expect(sceneTexts(s).join(' ')).not.toContain('400');
	});
	it('primary metric: scope filter, measured first, then better value', () => {
		const t = VIEW.layouts!.gc_1d;
		const c = C('fiber_chip_coupler.grating', [
			m({ parameter: 'insertion_loss_db', value: '1.0', unit: 'dB', scope: 'per_coupler', basis: 'simulated' }),
			m({ parameter: 'insertion_loss_db', value: '2.5', unit: 'dB', scope: 'per_coupler', basis: 'measured' }),
			m({ parameter: 'insertion_loss_db', value: '1.9', unit: 'dB', scope: 'per_coupler', basis: 'measured' }),
			m({ parameter: 'insertion_loss_db', value: '0.5', unit: 'dB', scope: 'fiber_to_fiber', basis: 'measured' })
		]);
		expect(primaryMetric(c, 'gc_1d', t).row?.value).toBe('1.9');
	});
});

describe('materials', () => {
	it('parses materials in text order without matching inside formulas', () => {
		expect(scanMaterials('Si 220 nm inverse taper under x-cut TFLN 500 nm').map((x) => x.mat)).toEqual(['si', 'ln']);
		expect(scanMaterials('Si-rich PECVD SiNx 300 nm').map((x) => x.mat)).toEqual(['sin']);
		expect(scanMaterials('Si3N4 on SiO2').map((x) => x.mat)).toEqual(['sin', 'sio2']);
	});
	it('stack from platform and cladding text', () => {
		const s = stackOf(C('waveguide_platform.transition', [], { platform: 'lnoi_loaded_si', core_material: 'Si 220 nm under TFLN', cladding: 'none (air-cladded reference)' }));
		expect([s.core, s.layer2, s.cladding]).toEqual(['si', 'ln', 'air']);
		expect(stackOf(C('laser.dfb', [], { platform: 'inp' })).box).toBe('none');
	});
});

describe('honesty (D104)', () => {
	const served = VIEW.components.filter((c) => templateFor(c.class, VIEW.layouts));
	it('covers the served components', () => expect(served.length).toBeGreaterThan(300));
	it('no visible label shows a number that is not in the component metric rows', () => {
		const bad: string[] = [];
		for (const c of served) {
			const allowed = new Set(c.metrics.flatMap((x) => [...(x.value + ' ' + (x.value_max ?? '')).matchAll(NUM)].map((k) => k[0])));
			const sc = buildScenes(resolve(c, VIEW)!);
			for (const s of [sc.top, sc.xsec]) for (const t of sceneTexts(s)) for (const k of t.matchAll(NUM)) if (!allowed.has(k[0])) bad.push(`${c.component_id}: "${t}"`);
		}
		expect(bad).toEqual([]);
	});
	it('every mark of a reported dimension carries its row (value, basis, locator)', () => {
		for (const c of served) {
			const sc = buildScenes(resolve(c, VIEW)!);
			for (const s of [sc.top, sc.xsec]) for (const mk of s.marks) {
				if (mk.dim.row) {
					expect(mk.dim.row.locator).toBeTruthy();
					expect(mk.dim.tip).toContain(mk.dim.row.locator);
				} else expect(mk.dim.label).toBe('not reported');
			}
		}
	});
	it('scene geometry is finite', () => {
		for (const c of served) {
			const sc = buildScenes(resolve(c, VIEW)!);
			for (const s of [sc.top, sc.xsec]) for (const sh of s.shapes) for (const ring of sh.rings) for (const p of ring) expect(Number.isFinite(p[0]) && Number.isFinite(p[1]), c.component_id + ' ' + sh.role).toBe(true);
		}
	});
});

describe('gallery', () => {
	it('lists every template; showcase roles missing are gaps, not filled', () => {
		const g = gallery(VIEW);
		expect(g.map((x) => x.id).sort()).toEqual(Object.keys(VIEW.layouts!).sort());
		if ((VIEW.showcase ?? []).length) {
			for (const x of g) {
				expect(x.fallback).toBe(false);
				for (const cd of x.cards) expect(['hero', 'typical']).toContain(cd.role);
				for (const gap of x.gaps) expect(x.cards.some((cd) => cd.role === gap)).toBe(false);
			}
		}
	});
	it('falls back to geometry-rich components when the showcase table is empty', () => {
		const g = gallery({ ...VIEW, showcase: [] });
		expect(g.every((x) => x.fallback && x.gaps.length === 0)).toBe(true);
		for (const x of g) for (const cd of x.cards) expect(cd.r.reported).toBeGreaterThan(0);
	});
});
