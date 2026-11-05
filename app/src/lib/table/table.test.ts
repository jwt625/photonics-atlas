// Filter and pivot logic on the real generated views (DevLog-013 D502-D504).
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import type { Component, ComponentsView, Metric } from '../components.svelte';
import { applyFilters, chipText, dateYear, EMPTY, facets, inRange, isActive, matches, nextSort, numStats, safeDecode, sortRows, type Col } from './filters';
import { cellKey, cellNums, cellRep, cellText, cellTip, defaultParams, MAX_GEOM, MAX_PERF, normScope, paramLabel, pivot, rankParams, repRow, rowNum, rowPass, rowWavelength } from './pivot';

const cv = JSON.parse(readFileSync(new URL('../../../static/data/components.json', import.meta.url), 'utf-8')) as ComponentsView;
const comps = cv.components;
const params = cv.parameters;

const platform: Col<Component> = { key: 'platform', label: 'Platform', kind: 'enum', get: (c) => c.platform };
const fab: Col<Component> = { key: 'fab', label: 'Fab', kind: 'enum', get: (c) => c.fab_orgs };
const year: Col<Component> = { key: 'year', label: 'Year', kind: 'num', get: (c) => c.source.year };
const label: Col<Component> = { key: 'label', label: 'Component', kind: 'text', get: (c) => c.label };

const m = (o: Partial<Metric>): Metric => ({ metric_id: 'x-m1', parameter: 'insertion_loss_db', value: '1', unit: 'dB', basis: 'measured', locator: 'p.1', ...o });

describe('filters', () => {
	it('multi-select: any selected value, the empty option, facet counts add up', () => {
		const f = facets(comps, platform);
		const nNone = comps.filter((c) => !c.platform).length;
		expect(f.reduce((t, x) => t + x.n, 0)).toBe(comps.length);
		expect(f.find((x) => x.value === EMPTY)?.n).toBe(nNone);
		const sel = f.slice(0, 2).map((x) => x.value);
		const got = applyFilters(comps, [platform], { platform: { t: 'enum', sel } });
		expect(got.length).toBe(comps.filter((c) => sel.includes(c.platform as string)).length);
		expect(applyFilters(comps, [platform], { platform: { t: 'enum', sel: [EMPTY] } }).length).toBe(nNone);
	});
	it('a list-valued cell counts once per distinct value and matches on any', () => {
		const f = facets(comps, fab);
		const top = f.find((x) => x.value !== EMPTY)!;
		expect(top.n).toBe(comps.filter((c) => new Set(c.fab_orgs).has(top.value)).length);
		expect(applyFilters(comps, [fab], { fab: { t: 'enum', sel: [top.value] } }).length).toBe(top.n);
	});
	it('facets ignore the column itself and respect the others', () => {
		const filters = { platform: { t: 'enum' as const, sel: ['soi'] }, fab: { t: 'enum' as const, sel: [facets(comps, fab)[0].value] } };
		const forPlatform = applyFilters(comps, [platform, fab], filters, 'platform');
		expect(forPlatform.length).toBe(applyFilters(comps, [fab], { fab: filters.fab }).length);
	});
	it('range: bounds inclusive, empty cells out, a stored range matches on overlap', () => {
		const got = applyFilters(comps, [year], { year: { t: 'num', min: 2020, max: 2021 } });
		expect(got.length).toBe(comps.filter((c) => Number(c.source.year) >= 2020 && Number(c.source.year) <= 2021).length);
		const r: Col<{ v: [number, number][] }> = { key: 'v', label: 'v', kind: 'num', get: (x) => x.v };
		expect(matches(r, { t: 'num', min: 2, max: null }, { v: [[1, 3]] })).toBe(true);
		expect(matches(r, { t: 'num', min: 4, max: null }, { v: [[1, 3]] })).toBe(false);
		expect(matches(r, { t: 'num', min: 4, max: null }, { v: [] })).toBe(false);
		expect(isActive({ t: 'num', min: null, max: null })).toBe(false);
	});
	it('text: case and accent insensitive contains', () => {
		const q = comps[0].label.slice(2, 8).toUpperCase();
		expect(applyFilters(comps, [label], { label: { t: 'text', q } }).some((c) => c.component_id === comps[0].component_id)).toBe(true);
	});
	it('stats: domain and histogram cover every value', () => {
		const s = numStats(comps, year)!;
		const ys = comps.map((c) => Number(c.source.year)).filter((y) => Number.isFinite(y) && y > 0);
		expect([s.min, s.max]).toEqual([Math.min(...ys), Math.max(...ys)]);
		expect(s.hist.reduce((a, b) => a + b, 0)).toBe(s.cells);
		expect(s.log).toBe(false);
	});
	it('sort: empty last in both directions, ties by tie then input order, three-state cycle', () => {
		const rows = [{ v: 2 }, { v: null }, { v: 1 }, { v: 2 }];
		const c: Col<{ v: number | null }> = { key: 'v', label: 'v', kind: 'num', get: (x) => x.v };
		expect(sortRows(rows, c, 1).map((r) => r.v)).toEqual([1, 2, 2, null]);
		expect(sortRows(rows, c, -1).map((r) => r.v)).toEqual([2, 2, 1, null]);
		const s1 = nextSort(null, c);
		expect(s1).toEqual({ key: 'v', dir: -1 });
		const s2 = nextSort(s1, c);
		expect(s2).toEqual({ key: 'v', dir: 1 });
		expect(nextSort(s2, c)).toBeNull();
	});
	it('chips say what is filtered', () => {
		expect(chipText(year, { t: 'num', min: 2020, max: null })).toBe('>= 2020');
		expect(chipText(platform, { t: 'enum', sel: ['a', 'b', 'c'] })).toBe('3 selected');
	});
});

describe('pivot', () => {
	it('parameter labels drop the unit tail only', () => {
		expect(paramLabel('insertion_loss_db')).toBe('insertion loss');
		expect(paramLabel('prop_loss_db_per_cm')).toBe('prop loss');
		expect(paramLabel('responsivity_a_per_w')).toBe('responsivity');
		expect(paramLabel('q_intrinsic')).toBe('q intrinsic');
		expect(paramLabel('per_db')).toBe('per');
		for (const p of Object.keys(params)) expect(paramLabel(p).length).toBeGreaterThan(0);
	});
	it('representative row: measured first, then no condition, no qualifier, metric order; never a spread if avoidable', () => {
		const sim = m({ metric_id: 'x-m1', basis: 'simulated' });
		const cond = m({ metric_id: 'x-m2', condition: 'at 25 C' });
		const qual = m({ metric_id: 'x-m3', qualifier: 'lt' });
		const plain = m({ metric_id: 'x-m9' });
		const std = m({ metric_id: 'x-m0', statistic: 'std' });
		expect(repRow([sim, cond, qual, plain, std])).toBe(plain);
		expect(repRow([sim, cond, qual])).toBe(qual);
		expect(repRow([sim, cond])).toBe(cond);
		expect(repRow([std, sim])).toBe(sim);
	});
	it('columns of a family: only what it reports, performance first, coverage order, default set capped', () => {
		const fam = comps.filter((c) => c.class.startsWith('fiber_chip_coupler.'));
		const r = rankParams(fam, params);
		const first = r.findIndex((x) => x.kind === 'geometry');
		expect(r.slice(first).every((x) => x.kind === 'geometry')).toBe(true);
		for (const x of r) expect(x.n).toBe(fam.filter((c) => c.metrics.some((y) => y.statistic !== 'std' && cellKey(y) === x.key)).length);
		const perf = r.filter((x) => x.kind === 'performance');
		expect(perf.map((x) => x.n)).toEqual([...perf.map((x) => x.n)].sort((a, b) => b - a));
		const d = defaultParams(r, fam.length);
		const rank = new Map(r.map((x) => [x.key, x]));
		expect(d.some((k) => rank.get(k)?.param === 'insertion_loss_db')).toBe(true);
		expect(d.filter((k) => rank.get(k)?.kind === 'performance').length).toBeLessThanOrEqual(MAX_PERF);
		expect(d.filter((k) => rank.get(k)?.kind === 'geometry').length).toBeLessThanOrEqual(MAX_GEOM);
		// different families get different columns
		const pdR = rankParams(comps.filter((c) => c.class.startsWith('photodetector.')), params);
		expect(defaultParams(pdR, 100).some((k) => k.startsWith('responsivity_a_per_w@'))).toBe(true);
		expect(d.some((k) => k.startsWith('responsivity_a_per_w@'))).toBe(false);
	});
	it('scope split: one column per scope when a parameter has several, none when it has one; no-scope rows and "unspecified" share one', () => {
		const c1 = { metrics: [m({ scope: 'per_coupler' }), m({ metric_id: 'x-m2', scope: 'fiber_to_fiber' }), m({ metric_id: 'x-m3' }), m({ metric_id: 'x-m4', scope: 'unspecified' }), m({ metric_id: 'x-m5', parameter: 'width_nm' }), m({ metric_id: 'x-m6', parameter: 'excess_loss_db', scope: 'per_component' })] } as unknown as Component;
		const r = rankParams([c1], params);
		const il = r.filter((x) => x.param === 'insertion_loss_db');
		expect(il.map((x) => x.scope).sort()).toEqual(['', 'fiber_to_fiber', 'per_coupler']);
		expect(il.every((x) => x.split)).toBe(true);
		expect(r.find((x) => x.param === 'width_nm')?.split).toBe(false);
		expect(r.find((x) => x.param === 'excess_loss_db')?.split).toBe(false);
		expect(normScope('unspecified')).toBe('');
		const [row] = pivot([c1], {}, params);
		expect(row.cells.get('insertion_loss_db@')?.rows.length).toBe(2);
		expect(row.cells.get('insertion_loss_db@per_coupler')?.rows.length).toBe(1);
		// real data: no cell mixes scopes
		for (const pr of pivot(comps, {}, params)) for (const [k, c] of pr.cells) for (const x of c.rows) expect(cellKey(x)).toBe(k);
	});
	it('pivot: one row per component, every stored row but spreads in exactly one cell', () => {
		const rows = pivot(comps, {}, params);
		expect(rows.length).toBe(comps.length);
		for (const r of rows.slice(0, 300)) {
			expect([...r.cells.values()].reduce((t, c) => t + c.rows.length, 0)).toBe(r.c.metrics.filter((x) => x.statistic !== 'std').length);
		}
	});
	it('a spread is not a value: a std-only parameter has no cell, no column', () => {
		const c1 = { metrics: [m({ parameter: 'width_nm', statistic: 'std' })] } as unknown as Component;
		expect(rankParams([c1], params)).toEqual([]);
		expect(pivot([c1], {}, params)[0].cells.size).toBe(0);
	});
	it('range filter: the cell shows, and sorts by, the rows that matched; the full list stays', () => {
		const a = m({ metric_id: 'x-m1', value: '5' }), b = m({ metric_id: 'x-m2', value: '0.5', basis: 'simulated' });
		const cell = { rep: a, rows: [a, b] };
		expect(cellRep(cell, undefined)).toBe(a);
		expect(cellRep(cell, { t: 'num', min: 0, max: 1 })).toBe(b);
		expect(cellRep(cell, { t: 'num', min: 4, max: null })).toBe(a);
		const tip = cellTip(cell, b)!.split('\n');
		expect(tip[0].startsWith('0.5')).toBe(true);
		expect(tip.length).toBe(2);
	});
	it('bounds: "> 60" cannot match Max 60, "< 60" cannot match Min 60, both match where they overlap', () => {
		const gt = rowNum(m({ value: '60', qualifier: 'gt' }))!, lt = rowNum(m({ value: '60', qualifier: 'lt' }))!, ge = rowNum(m({ value: '60', qualifier: 'ge' }))!;
		expect(inRange(gt, null, 60)).toBe(false);
		expect(inRange(gt, null, 61)).toBe(true);
		expect(inRange(gt, 100, null)).toBe(true);
		expect(inRange(ge, null, 60)).toBe(true);
		expect(inRange(lt, 60, null)).toBe(false);
		expect(inRange(lt, 59, null)).toBe(true);
		expect(inRange(rowNum(m({ value: '60', qualifier: 'approx' }))!, 60, 60)).toBe(true);
		const c: Col<{ v: unknown[] }> = { key: 'v', label: 'v', kind: 'num', get: (x) => x.v as never };
		const st = numStats([{ v: [gt] }, { v: [1] }], c)!;
		expect([st.min, st.max]).toEqual([1, 60]);
	});
	it('year semantics: integer years match by year; a list of years is not a span', () => {
		expect(dateYear('2023-06-14')).toBe(2023);
		expect(dateYear('2023')).toBe(2023);
		expect(dateYear('')).toBeNull();
		const c: Col<{ d: string }> = { key: 'd', label: 'd', kind: 'num', get: (x) => dateYear(x.d) };
		for (const d of ['2023', '2023-01-01', '2023-12-31']) expect(matches(c, { t: 'num', min: 2023, max: 2023 }, { d })).toBe(true);
		const y: Col<{ ys: number[] }> = { key: 'y', label: 'y', kind: 'num', get: (x) => x.ys };
		const vendor = { ys: [2019, 2024] };
		expect(matches(y, { t: 'num', min: 2021, max: 2022 }, vendor)).toBe(false);
		expect(matches(y, { t: 'num', min: 2024, max: 2024 }, vendor)).toBe(true);
	});
	it('a selected facet stays listed at 0, so it can be unticked', () => {
		const f = facets([{ v: 'a' }], { key: 'v', label: 'v', kind: 'enum', get: (x: { v: string }) => x.v }, ['b']);
		expect(f.map((x) => [x.value, x.n])).toEqual([['a', 1], ['b', 0]]);
	});
	it('a malformed hash does not throw', () => {
		expect(safeDecode('%E0%A4%A')).toBe('%E0%A4%A');
		expect(safeDecode('a%20b')).toBe('a b');
	});
	it('basis filter: only those rows feed cells, a component without one leaves the table', () => {
		const f = { basis: { t: 'enum' as const, sel: ['measured'] } };
		const rows = pivot(comps, f, params);
		expect(rows.length).toBe(comps.filter((c) => c.metrics.some((x) => x.basis === 'measured' && x.statistic !== 'std')).length);
		for (const r of rows.slice(0, 300)) for (const c of r.cells.values()) expect(c.rows.every((x) => x.basis === 'measured')).toBe(true);
	});
	it('wavelength filter: geometry rows stay and do not keep a component; band-only rows use band edges', () => {
		expect(rowWavelength(m({ band: 'c_band' }))).toEqual([1530, 1565]);
		expect(rowWavelength(m({ band: 'unspecified' }))).toBeNull();
		expect(rowWavelength(m({ wavelength_nm: '1550', wavelength_max_nm: '1560', band: 'o_band' }))).toEqual([1550, 1560]);
		// a center wavelength counts by its own value, whatever else the row carries
		const cw = m({ parameter: 'center_wavelength_nm', value: '1310', unit: 'nm' });
		expect(rowWavelength(cw)).toEqual([1310, 1310]);
		expect(rowPass(cw, { wl: { t: 'num', min: 1300, max: 1320 } }, params)).toBe('hit');
		expect(rowPass(cw, { wl: { t: 'num', min: 1500, max: 1600 } }, params)).toBe('fail');
		const f = { wl: { t: 'num' as const, min: 1500, max: 1600 } };
		expect(rowPass(m({ wavelength_nm: '1550' }), f, params)).toBe('hit');
		expect(rowPass(m({ wavelength_nm: '1310' }), f, params)).toBe('fail');
		expect(rowPass(m({}), f, params)).toBe('fail');
		expect(rowPass(m({ parameter: 'width_nm' }), f, params)).toBe('exempt');
		const rows = pivot(comps, f, params);
		const want = comps.filter((c) => c.metrics.some((x) => x.statistic !== 'std' && rowPass(x, f, params) === 'hit')).length;
		expect(rows.length).toBe(want);
		expect(want).toBeLessThan(comps.length);
	});
	it('cell numbers keep ranges and bounds; cell text keeps the stored form where it fits', () => {
		const cell = { rep: m({}), rows: [m({ value: '1', value_max: '2' }), m({ value: '5' })] };
		expect(cellNums(cell)).toEqual([[1, 2], 5]);
		expect(cellText(m({ value: '566000000' }))).toBe('5.66e8');
		expect(cellText(m({ value: '3500000.0' }))).toBe('3.5e6');
		expect(cellText(m({ value: '1.4e6' }))).toBe('1.4e6');
		expect(cellText(m({ value: '120000' }))).toBe('120000');
		expect(cellText(m({ value: '0.52', qualifier: 'lt' }))).toBe('< 0.52');
		expect(cellText(m({ value: '1.0', value_max: '1.4' }))).toBe('1.0-1.4');
	});
});
