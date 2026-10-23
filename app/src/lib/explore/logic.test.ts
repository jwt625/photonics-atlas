import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { describe, expect, it } from 'vitest';
import type { Component, Metric } from '../components.svelte';
import { platformFamily } from './colors';
import {
	logDtick,
	applyExFilters,
	buildScatter,
	buildStrip,
	buildVsWavelength,
	candidates,
	classPlatformMatrix,
	conflict,
	defaultExFilters,
	pairRows,
	qualOf,
	toMw,
	yearStack,
	type AxisSpec
} from './logic';

let n = 0;
const m = (x: Partial<Metric>): Metric => ({ metric_id: `cmp_t-m${++n}`, parameter: 'insertion_loss_db', value: '1', unit: 'dB', basis: 'measured', locator: 'p.1', ...x });
const comp = (x: Partial<Component> & { metrics: Metric[] }): Component => ({
	component_id: `cmp_t${++n}`,
	source_id: 'eo:t2026',
	class: 'fiber_chip_coupler.grating',
	label: 'test',
	row_kind: 'fabricated',
	platform: 'soi',
	verified_on: '2026-10-20',
	fab_orgs: [],
	source: { id: 'eo:t2026', title: 'T', year: '2026', venue: 'V', url: '', access: '' },
	...x
});

const IL: AxisSpec = { label: 'IL', params: ['insertion_loss_db'], scopes: ['per_coupler', 'per_facet', 'loopback_half'] };
const BW: AxisSpec = { label: 'BW', params: ['bw_1db_nm'] };

describe('platform families', () => {
	it('maps the platform enum onto families, unknown to other', () => {
		expect(platformFamily('soi_rib')).toBe('soi');
		expect(platformFamily('sion')).toBe('sin');
		expect(platformFamily('lnoi_loaded_sin')).toBe('ln');
		expect(platformFamily('bto_on_sin')).toBe('eo');
		expect(platformFamily('inp_membrane')).toBe('iii_v');
		expect(platformFamily('polymer')).toBe('glass');
		expect(platformFamily('other')).toBe('other');
		expect(platformFamily(undefined)).toBe('other');
		expect(platformFamily('plasmonic_mim')).toBe('other');
		expect(platformFamily('gap_on_insulator')).toBe('iii_v');
		expect(platformFamily('iii_v_on_si_epi')).toBe('iii_v');
	});
	it('every platform enum value of components.schema.yaml has a family, except the declared neutral ones (D229a)', () => {
		const y = readFileSync(fileURLToPath(new URL('../../../../data/schema/components.schema.yaml', import.meta.url)), 'utf-8');
		const enumLine = y.match(/^\s*platform: \[([^\]]+)\]/m);
		expect(enumLine).not.toBeNull();
		const vals = enumLine![1].split(',').map((v) => v.trim());
		expect(vals).toContain('gap_on_insulator');
		const neutral = new Set(['other', 'plasmonic_mim', 'al2o3']);
		expect(vals.filter((v) => !neutral.has(v) && platformFamily(v) === 'other')).toEqual([]);
	});
});

describe('condition compatibility', () => {
	it('stated wavelengths must agree', () => {
		expect(conflict(m({ wavelength_nm: '1550' }), m({ wavelength_nm: '1551' }))).toBeNull();
		expect(conflict(m({ wavelength_nm: '1310' }), m({ wavelength_nm: '1550' }))).toBe('wavelength');
		expect(conflict(m({ wavelength_nm: '1500', wavelength_max_nm: '1600' }), m({ wavelength_nm: '1550' }))).toBeNull();
	});
	it('bands must overlap, a wavelength must fall in the other band', () => {
		expect(conflict(m({ band: 'o_band' }), m({ band: 'c_band' }))).toBe('band');
		expect(conflict(m({ band: 'c_band' }), m({ band: 'cl_band' }))).toBeNull();
		expect(conflict(m({ band: 'c_band' }), m({ band: 'l_band' }))).toBe('band');
		expect(conflict(m({ wavelength_nm: '1310' }), m({ band: 'o_band' }))).toBeNull();
		expect(conflict(m({ wavelength_nm: '1550' }), m({ band: 'o_band' }))).toBe('band');
		expect(conflict(m({ band: 'unspecified' }), m({ band: 'o_band' }))).toBeNull();
	});
	it('a row without the condition is compatible; TE vs TM and temperature conflict', () => {
		expect(conflict(m({}), m({ wavelength_nm: '1550', polarization: 'te' }))).toBeNull();
		expect(conflict(m({ polarization: 'te' }), m({ polarization: 'tm' }))).toBe('polarization');
		expect(conflict(m({ polarization: 'te' }), m({ polarization: 'both' }))).toBeNull();
		expect(conflict(m({ temperature_k: '300' }), m({ temperature_k: '4' }))).toBe('temperature');
	});
});

describe('row selection and pairing', () => {
	it('skips std rows, wrong scopes and non-numeric values', () => {
		const c = comp({
			metrics: [
				m({ value: '0.1', statistic: 'std', scope: 'per_coupler' }),
				m({ value: '3', scope: 'fiber_to_fiber' }),
				m({ value: 'x', scope: 'per_coupler' }),
				m({ value: '2', scope: 'per_coupler' })
			]
		});
		expect(candidates(c, IL, false).map((v) => v.v)).toEqual([2]);
	});
	it('measured-only drops modelled performance rows but keeps geometry', () => {
		const c = comp({ metrics: [m({ parameter: 'radius_um', unit: 'um', basis: 'design_target' }), m({ basis: 'simulated', scope: 'per_coupler' })] });
		expect(candidates(c, { label: 'R', params: ['radius_um'], geometry: true }, true)).toHaveLength(1);
		expect(candidates(c, IL, true)).toHaveLength(0);
	});
	it('pairs only compatible rows, preferring measured, unbounded, explicit, source order', () => {
		const c = comp({
			metrics: [
				m({ value: '5', scope: 'per_coupler', wavelength_nm: '1310', basis: 'simulated' }),
				m({ value: '4', scope: 'per_coupler', wavelength_nm: '1550' }),
				m({ value: '3', scope: 'per_coupler' }),
				m({ parameter: 'bw_1db_nm', unit: 'nm', value: '30', wavelength_nm: '1550' })
			]
		});
		const r = pairRows(candidates(c, BW, false), candidates(c, IL, false));
		expect(r.status).toBe('ok');
		expect(r.y?.v).toBe(4); // explicit 1550 match beats the row without a wavelength
	});
	it('reports incomparable when every pair conflicts', () => {
		const c = comp({ metrics: [m({ scope: 'per_coupler', band: 'o_band' }), m({ parameter: 'bw_1db_nm', unit: 'nm', value: '30', band: 'c_band' })] });
		expect(pairRows(candidates(c, BW, false), candidates(c, IL, false)).status).toBe('incomparable');
	});
	it('qualifiers map to bounds', () => {
		expect(qualOf(m({ qualifier: 'le' }))).toBe('lt');
		expect(qualOf(m({ qualifier: 'gt' }))).toBe('gt');
		expect(qualOf(m({ qualifier: 'approx' }))).toBeNull();
	});
	it('converts dBm to mW', () => {
		expect(toMw(m({ parameter: 'output_power_dbm', value: '10', unit: 'dBm' }), 10)?.v).toBeCloseTo(10);
	});
});

describe('points and omitted counts', () => {
	const cs = [
		comp({ metrics: [m({ scope: 'per_coupler', value: '2' }), m({ parameter: 'bw_1db_nm', unit: 'nm', value: '30' })] }),
		comp({ metrics: [m({ scope: 'per_coupler', value: '2', basis: 'simulated', qualifier: 'lt' })] }),
		comp({ metrics: [m({ parameter: 'bw_1db_nm', unit: 'nm', value: '30' })] }),
		comp({ metrics: [] }),
		comp({ metrics: [m({ scope: 'per_coupler', value: '0' }), m({ parameter: 'bw_1db_nm', unit: 'nm', value: '30' })] })
	];
	it('counts missing x / y / both and nonpositive on log axes', () => {
		const r = buildScatter(cs, BW, IL, { measuredOnly: false, yLog: true });
		expect(r.omitted).toMatchObject({ total: 5, plotted: 1, missingX: 1, missingY: 1, missingBoth: 1, nonpositive: 1 });
	});
	it('wavelength axis uses the row wavelength, else a compatible center wavelength', () => {
		const w = [
			comp({ metrics: [m({ scope: 'per_coupler', wavelength_nm: '1310' })] }),
			comp({ metrics: [m({ scope: 'per_coupler', band: 'c_band' }), m({ parameter: 'center_wavelength_nm', unit: 'nm', value: '1550' })] }),
			comp({ metrics: [m({ scope: 'per_coupler', band: 'o_band' }), m({ parameter: 'center_wavelength_nm', unit: 'nm', value: '1550' })] }),
			comp({ metrics: [m({ scope: 'per_coupler', band: 'o_band' })] })
		];
		const r = buildVsWavelength(w, IL, { measuredOnly: false });
		expect(r.pts.map((p) => p.x)).toEqual([1310, 1550]);
		expect(r.omitted).toMatchObject({ plotted: 2, incomparable: 1, missingX: 1 });
	});
	it('strip plot puts present families in fixed order and marks modelled points', () => {
		const s = buildStrip(
			[
				comp({ platform: 'sin', metrics: [m({ parameter: 'prop_loss_db_per_cm', unit: 'dB/cm', value: '0.1' })] }),
				comp({ platform: 'soi', metrics: [m({ parameter: 'prop_loss_db_per_cm', unit: 'dB/cm', value: '1', basis: 'author_estimate' })] })
			],
			{ label: 'P', params: ['prop_loss_db_per_cm'] },
			{ measuredOnly: false }
		);
		expect(s.stats.map((x) => x.group)).toEqual(['soi', 'sin']);
		expect(s.pts.find((p) => p.group === 'soi')?.sim).toBe(true);
		expect(s.stats[0].median).toBeNull();
		expect(s.stats[1].median).toBe(0.1);
	});
	it('strip median uses unqualified measured values only; scopes restrict the rows', () => {
		const P = { label: 'L', params: ['insertion_loss_db'], scopes: ['per_facet', 'loopback_half'] };
		const s = buildStrip(
			[
				comp({ platform: 'sin', metrics: [m({ scope: 'per_facet', value: '1' })] }),
				comp({ platform: 'sin', metrics: [m({ scope: 'per_facet', value: '2', basis: 'derived' })] }),
				comp({ platform: 'sin', metrics: [m({ scope: 'loopback_half', value: '3', qualifier: 'lt' })] }),
				comp({ platform: 'sin', metrics: [m({ scope: 'per_coupler', value: '4' })] })
			],
			P,
			{ measuredOnly: false }
		);
		expect(s.omitted).toMatchObject({ total: 4, plotted: 3, missingY: 1 });
		expect(s.stats[0]).toMatchObject({ n: 1, total: 3, median: 1 });
	});
});

describe('filters and counts', () => {
	const cs = [
		comp({ class: 'laser.dfb', platform: 'inp', source: { id: 'ofc2026:a', title: '', year: '2024', venue: '', url: '', access: '' }, metrics: [m({ basis: 'simulated' })] }),
		comp({ class: 'fiber_chip_coupler.edge', platform: 'soi', source: { id: 'pk:b', title: '', year: '2026', venue: '', url: '', access: '' }, metrics: [m({})] }),
		comp({ class: 'fiber_chip_coupler.grating', platform: '', metrics: [m({})] })
	];
	it('filters by class family, platform family, corpus, year and basis', () => {
		const f = defaultExFilters();
		expect(applyExFilters(cs, f)).toHaveLength(3);
		expect(applyExFilters(cs, { ...f, classes: ['fiber_chip_coupler'] })).toHaveLength(2);
		expect(applyExFilters(cs, { ...f, families: ['iii_v'] })).toHaveLength(1);
		expect(applyExFilters(cs, { ...f, families: ['other'] })).toHaveLength(1);
		expect(applyExFilters(cs, { ...f, corpora: ['pk', 'eo'] })).toHaveLength(2);
		expect(applyExFilters(cs, { ...f, yearMin: 2025 })).toHaveLength(2);
		expect(applyExFilters(cs, { ...f, measuredOnly: true })).toHaveLength(2);
	});
	it('year stack fills the year range and heat matrix counts each component once', () => {
		const y = yearStack(cs);
		expect(y.years).toEqual([2024, 2025, 2026]);
		expect(y.counts.get('fiber_chip_coupler')?.get(2026)).toBe(2);
		const h = classPlatformMatrix(cs, 'family');
		expect(h.rows[0]).toBe('fiber_chip_coupler');
		expect(h.z.flat().reduce((a, b) => a + b, 0)).toBe(3);
	});
});

describe('log axis ticks (UI audit 20)', () => {
	it('1-2-5 labels within three decades, decades beyond, none without positive values', () => {
		expect(logDtick([0.5, 3, 40])).toBe('D2');
		expect(logDtick([1e4, 5e8])).toBe(1);
		expect(logDtick([0, -1, null])).toBeUndefined();
	});
});
