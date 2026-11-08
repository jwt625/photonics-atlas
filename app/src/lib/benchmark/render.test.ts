import { describe, expect, it } from 'vitest';
import { fmtNum, leaders, rankRow, readState, renderBenchmark, writeState } from './render.js';
import type { BenchmarkView } from './render.js';

const col = (id: string, family: string, extra = {}) => ({
	id, family, foundry: id.split('.')[0], label: id.split('.')[0], orgs: [], processes: [], n_rows: 1, ...extra
});
const cell = (r: number, extra = {}) => ({ r, v: r, basis: 'measured', source_id: 'lit:a', n: 1, n_src: 1, ...extra });
const cols = [col('a.siph', 'siph'), col('b.siph', 'siph'), col('c.siph', 'siph'), col('d.sin', 'sin', { pinned: true })];
const row = (better: 'lower' | 'higher', cells: Record<string, ReturnType<typeof cell>>) => ({
	id: 'r', label: 'Row', unit: 'dB', better, fmt: 'auto', sub: '', note: '', cells
});
const view = (rows: ReturnType<typeof row>[]): BenchmarkView => ({
	generated_on: '2026-11-07',
	families: [{ id: 'siph', label: 'SiPh', tip: '' }, { id: 'sin', label: 'SiN', tip: '' }],
	columns: cols,
	categories: [{ id: 'c', label: 'Cat', rows }],
	sources: { 'lit:a': { title: 'T', url: 'https://doi.org/x' }, 'pc:2026-11-07': { title: 'Private communication (unpublished)' } },
	rules: { basis: ['measured'], min_rows_per_column: 3, min_columns_per_row: 2, telecom_window_nm: [1260, 1630], min_temperature_k: 250 },
	rows_not_shown: []
});

describe('benchmark ranking', () => {
	it('ranks best and second, ties share a rank', () => {
		const r = row('lower', { 'a.siph': cell(1), 'b.siph': cell(1), 'c.siph': cell(2), 'd.sin': cell(3) });
		expect(rankRow(r, cols, 'all')).toEqual({ 'a.siph': 1, 'b.siph': 1, 'c.siph': 2 });
		expect(rankRow(r, cols, 'family')).toEqual({ 'a.siph': 1, 'b.siph': 1, 'c.siph': 2, 'd.sin': 1 });
		expect(rankRow(row('higher', r.cells), cols, 'all')).toEqual({ 'd.sin': 1, 'c.siph': 2 });
	});
	it('leading column = most row bests', () => {
		const v = view([row('lower', { 'a.siph': cell(1), 'b.siph': cell(2) }), row('higher', { 'a.siph': cell(5), 'c.siph': cell(1) })]);
		const { wins, lead } = leaders(v, cols, 'all');
		expect(wins['a.siph']).toBe(2);
		expect([...lead]).toEqual(['a.siph']);
	});
});

describe('benchmark rendering', () => {
	it('formats numbers', () => {
		expect(fmtNum(0.01684)).toBe('0.0168');
		expect(fmtNum(265.4)).toBe('265');
		expect(fmtNum(2.5e6, 'sci')).toBe('2.5×10<sup>6</sup>');
	});
	it('shows ranges low to high and marks private values and pinned columns', () => {
		const html = renderBenchmark(
			view([row('lower', {
				'a.siph': cell(2, { v: 2.7, vmax: 1.3 }),
				'b.siph': cell(0.6, { q: 'approx', basis: 'private_communication', source_id: 'pc:2026-11-07', date: '2026-11-07' })
			})]),
			{ rank: 'all', hidden: [] }
		);
		expect(html).toContain('1.3–2.7');
		expect(html).toContain('~0.6<sup class="bm-pc">†</sup>');
		expect(html).toContain('private communication, unpublished (2026-11-07)');
		expect(html).toContain('pinned: shown whatever its fill');
	});
	it('round-trips the hash state', () => {
		const st = { rank: 'family' as const, hidden: ['sin'] };
		expect(readState(writeState(st))).toEqual(st);
		expect(writeState({ rank: 'all', hidden: [] })).toBe('');
	});
});
