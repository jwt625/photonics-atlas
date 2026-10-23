import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import type { Component, ComponentsView, Metric } from '../components.svelte';
import { gallery } from './gallery';
import { scanMaterials, stackOf } from './materials';
import { compactLabel, pickOrder, primaryFor, primaryMetric, resolve, segmentRows, templateFor } from './resolve';
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
	it('primary metric: a measured row of another scope beats a simulated row of the template scope (D221)', () => {
		const t = VIEW.layouts!.edge_taper;
		const c = C('fiber_chip_coupler.edge', [
			m({ parameter: 'insertion_loss_db', value: '0.7', qualifier: 'lt', unit: 'dB', scope: 'per_coupler', basis: 'measured' }),
			m({ parameter: 'insertion_loss_db', value: '0.15', qualifier: 'lt', unit: 'dB', scope: 'per_facet', basis: 'simulated' })
		]);
		const p = primaryMetric(c, 'edge_taper', t);
		expect(p.row?.basis).toBe('measured');
		expect(p.scopeMatch).toBe(false);
		const only = primaryMetric(C('fiber_chip_coupler.edge', [c.metrics[1]]), 'edge_taper', t);
		expect([only.row?.basis, only.scopeMatch]).toEqual(['simulated', true]);
	});
	it('primary metric: primary_by_class overrides the template primary for that class only (D229a)', () => {
		const crossing = { parameter: 'crossing_loss_db', scope: 'per_component', better: 'lower' as const };
		const t = { ...VIEW.layouts!.mmi, primary_by_class: { 'crossing.mmi': crossing } };
		expect(primaryFor('crossing.mmi', t)).toEqual(crossing);
		expect(primaryFor('splitter.mmi', t)).toEqual(t.primary);
		expect(primaryFor('crossing.mmi', VIEW.layouts!.dc)).toEqual(VIEW.layouts!.dc.primary);
		const rows = [
			m({ parameter: 'excess_loss_db', value: '0.1', unit: 'dB', scope: 'per_component', basis: 'measured' }),
			m({ parameter: 'crossing_loss_db', value: '0.3', unit: 'dB', scope: 'per_component', basis: 'measured' }),
			m({ parameter: 'crossing_loss_db', value: '0.2', unit: 'dB', scope: 'per_component', basis: 'measured' })
		];
		const x = primaryMetric(C('crossing.mmi', rows), 'mmi', t);
		expect([x.param, x.row?.value, x.spec.parameter, x.n]).toEqual(['crossing_loss_db', '0.2', 'crossing_loss_db', 2]);
		const sp = primaryMetric(C('splitter.mmi', rows), 'mmi', t);
		expect([sp.param, sp.row?.value]).toEqual(['excess_loss_db', '0.1']);
		const none = primaryMetric(C('crossing.mmi', [rows[0]]), 'mmi', t);
		expect([none.param, none.row]).toEqual(['crossing_loss_db', null]);
	});
	it('gallery cards use the class-specific primary (D229a)', () => {
		const crossing = { parameter: 'crossing_loss_db', scope: 'per_component', better: 'lower' as const };
		const layouts = { mmi: { ...VIEW.layouts!.mmi, primary_by_class: { 'crossing.mmi': crossing } } };
		const geo = [m({ parameter: 'mmi_width_um', value: '6', unit: 'um' }), m({ parameter: 'mmi_length_um', value: '30', unit: 'um' })];
		const loss = [m({ parameter: 'excess_loss_db', value: '0.4', unit: 'dB', scope: 'per_component', basis: 'measured' }), m({ parameter: 'crossing_loss_db', value: '0.05', unit: 'dB', scope: 'per_component', basis: 'measured' })];
		const comps = [C('crossing.mmi', [...geo, ...loss], { component_id: 'cmp_t_x' }), C('splitter.mmi', [...geo, ...loss], { component_id: 'cmp_t_s' })];
		for (const showcase of [[], [{ component_id: 'cmp_t_x', template: 'mmi', role: 'hero' }, { component_id: 'cmp_t_s', template: 'mmi', role: 'typical' }]]) {
			const g = gallery({ ...VIEW, layouts, components: comps, showcase } as ComponentsView)[0];
			const by = Object.fromEntries(g.cards.map((cd) => [cd.c.component_id, cd.primary]));
			expect([by.cmp_t_x.param, by.cmp_t_x.row?.value]).toEqual(['crossing_loss_db', '0.05']);
			expect([by.cmp_t_s.param, by.cmp_t_s.row?.value]).toEqual(['excess_loss_db', '0.4']);
		}
	});
	it('compact card labels rescale exactly, keep qualifiers, leave small values as stored (D224)', () => {
		expect(compactLabel(m({ parameter: 'q_intrinsic', value: '566000000', unit: '1' }))).toBe('5.66e8');
		expect(compactLabel(m({ parameter: 'q_intrinsic', value: '40000000', unit: '1', qualifier: 'gt' }))).toBe('> 4e7');
		expect(compactLabel(m({ parameter: 'q_intrinsic', value: '3500000.0', unit: '1' }))).toBe('3.5e6');
		expect(compactLabel(m({ parameter: 'length_um', value: '390000', unit: 'um' }))).toBe('390 mm');
		expect(compactLabel(m({ parameter: 'width_nm', value: '10000', unit: 'nm' }))).toBe('10 µm');
		expect(compactLabel(m({ parameter: 'linewidth_hz', value: '150000', unit: 'Hz' }))).toBe('150 kHz');
		expect(compactLabel(m({ parameter: 'insertion_loss_db', value: '0.56', unit: 'dB' }))).toBe('0.56 dB');
	});
});

describe('scenes (UI audit 2026-10-22)', () => {
	const sc = (id: string) => buildScenes(resolve(VIEW.components.find((c) => c.component_id === id)!, VIEW)!);
	const labelsOf = (s: ReturnType<typeof sc>['xsec']) => s.marks.map((x) => x.dim.param + '=' + x.dim.label);
	it('D220: heterogeneous laser rows naming the Si waveguide are drawn on a Si layer, not as III-V layers', () => {
		const x = sc('cmp_ofc2026_m1g3_qd_dfb_memristor').xsec;
		expect(x.shapes.some((s) => s.role === 'active layer')).toBe(false);
		const si = x.shapes.filter((s) => s.mat === 'si' && s.role.includes('waveguide'));
		expect(si.length).toBe(1);
		expect(labelsOf(x)).toEqual(expect.arrayContaining(['core_thickness_nm=300 nm', 'etch_depth_nm=170 nm', 'width_nm=1500 nm', 'ridge_width_um=4 µm']));
		const mem = sc('cmp_ofc2026_w4e5_membrane_sel_la70um').xsec;
		expect(mem.shapes.some((s) => s.role === 'III-V membrane')).toBe(true);
	});
	it('D222: transition section at the lower-layer input draws the upper layer at its tip width', () => {
		const x = sc('cmp_wu2025_vac_si_sin').xsec;
		const up = x.shapes.find((s) => s.role.startsWith('upper layer'))!;
		const xs = up.rings[0].map((p) => p[0]);
		expect(Math.max(...xs) - Math.min(...xs)).toBeCloseTo(0.35);
		expect(labelsOf(x)).toContain('tip_width_nm=350 nm');
		expect(labelsOf(x)).not.toContain('width_nm=1000 nm');
	});
	it('D229: overlay SSC cladding sits on the overlay and the solid band equals the labelled thickness', () => {
		const x = sc('cmp_li2026aa_ssc').xsec;
		const cl = x.shapes.find((s) => s.role === 'cladding')!;
		const ys = cl.rings[0].map((p) => p[1]);
		expect(Math.min(...ys)).toBeCloseTo(4.2);
		expect(Math.max(...ys) - Math.min(...ys)).toBeCloseTo(2);
		expect(x.shapes.filter((s) => s.role.startsWith('cladding ')).every((s) => s.schematic)).toBe(true);
	});
	it('D225: views with no reported length are schematic (no TRUE SCALE claim)', () => {
		expect(sc('cmp_ofc2026_tu2d3_gc_1d_si').top.schematic).toBe(true);
		expect(sc('cmp_kieninger2020_mmi').top.schematic).toBe(true);
		expect(sc('cmp_li2025b_y_splitter').xsec.schematic).toBe(true);
		const r = sc('cmp_ofc2026_m1e6_sin_ring_r75um').top;
		expect(r.schematic).toBe(false);
	});
	it('D226: a heater without a reported offset is dashed and labelled not reported', () => {
		const x = sc('cmp_liu2026d_tops_or').xsec;
		expect(x.shapes.find((s) => s.role === 'heater')!.schematic).toBe(true);
		expect(x.labels.some((l) => l.dim?.param === 'heater_offset_um' && l.text === 'offset not reported')).toBe(true);
	});
	it('D228: a length far above the width is drawn with a break, labelled with the stored length', () => {
		const t = sc('cmp_wang2024b_spiral_1p75um').top;
		expect(t.shapes.some((s) => s.role === 'break')).toBe(true);
		expect(labelsOf(t)).toContain('length_um=390000 µm');
		expect(t.partial).toBe(true);
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
				for (const gap of x.gaps.filter((y) => !y.platform)) expect(x.cards.some((cd) => cd.role === gap.role)).toBe(false);
			}
		}
	});
	it('platform-qualified gaps (D223): shown while no card of that role has the platform family', () => {
		const layouts = { ...VIEW.layouts!, gc_1d: { ...VIEW.layouts!.gc_1d, gaps: [{ role: 'hero', platform_family: 'soi' }] } };
		const gc = gallery({ ...VIEW, layouts }).find((x) => x.id === 'gc_1d')!;
		expect(gc.gaps).toContainEqual({ role: 'hero', platform: 'SOI' });
		const lnGap = gallery({ ...VIEW, layouts: { ...layouts, gc_1d: { ...layouts.gc_1d, gaps: [{ role: 'hero', platform_family: 'ln' }] } } }).find((x) => x.id === 'gc_1d')!;
		expect(lnGap.gaps.some((g) => g.platform)).toBe(false);
	});
	it('dc companions are shown without a primary row (UI audit 19)', () => {
		const c = VIEW.components.find((x) => x.component_id === 'cmp_larocque2024_dc_michelson');
		if (!c) return;
		const p = primaryMetric(c, 'dc', VIEW.layouts!.dc);
		if (!p.row) expect(p.companions.map((x) => x.param)).toContain('split_ratio_pct');
	});
	it('cards and gaps share one role-ordered list (UI audit 18): hero before typical, no item lost', () => {
		const ord: Record<string, number> = { hero: 0, typical: 1 };
		for (const x of gallery(VIEW)) {
			expect(x.items.length).toBe(x.cards.length + x.gaps.length);
			const r = x.items.map((it) => ord[it.role] ?? 9);
			expect(r).toEqual([...r].sort((a, b) => a - b));
		}
		const dc = gallery(VIEW).find((x) => x.id === 'dc')!;
		if (dc.gaps.some((g) => g.role === 'hero')) expect(dc.items[0]).toMatchObject({ kind: 'gap', role: 'hero' });
	});
	it('falls back to geometry-rich components when the showcase table is empty', () => {
		const g = gallery({ ...VIEW, showcase: [] });
		expect(g.every((x) => x.fallback && x.gaps.length === 0)).toBe(true);
		for (const x of g) for (const cd of x.cards) expect(cd.r.reported).toBeGreaterThan(0);
	});
});
