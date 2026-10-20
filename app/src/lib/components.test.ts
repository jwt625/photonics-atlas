import { describe, expect, it } from 'vitest';
import { fmtValue, fmtWavelength, type Metric } from './components.svelte';

const m = (x: Partial<Metric>): Metric => ({ metric_id: 'cmp_a-m1', parameter: 'insertion_loss_db', value: '0.2', unit: 'dB', basis: 'measured', locator: 'p.3', ...x });

describe('metric formatting', () => {
	it('shows qualifier and range', () => {
		expect(fmtValue(m({ qualifier: 'gt', value: '40' }))).toBe('> 40');
		expect(fmtValue(m({ value: '1.0', value_max: '1.4' }))).toBe('1.0-1.4');
	});
	it('falls back to band when no wavelength', () => {
		expect(fmtWavelength(m({ band: 'o_band' }))).toBe('o_band');
		expect(fmtWavelength(m({ wavelength_nm: '1260', wavelength_max_nm: '1360' }))).toBe('1260-1360');
	});
});
