import { describe, expect, it } from 'vitest';
import { levelsLayout } from './levels';
import { AXES_END, axesK, axisTicks, barK, cleanPoints, extent, legendCorner, linTicks, logOf, logTicks, makeScale, plain, plotLabel, revealed, rich, stagger, styleOf, term, toBars, toggleLog, withAlternates, type LogState } from './plot';
import {
	chapterAt,
	chapterIndexAt,
	chapterIndexBefore,
	chapterLocal,
	chapterTarget,
	checkChapters,
	defaultAssembledAt,
	ease,
	keywordStates,
	essentialDimText,
	labelLeft,
	orbitLimits,
	plainKeyword,
	stepTipLines,
	partIntro,
	PLAY,
	playAt,
	playDuration,
	playPlan,
	plotRange,
	scrollDeltaFor,
	scrollProgress,
	seg
} from './progress';
import { elementBox, pathPoints } from './trace';
import type { Chapter, Plot, Series } from './types';

const CH: Chapter[] = [
	{ id: 'rod', p: [0, 0.2], keyword: 'Ruby rod', parts: ['rod'] },
	{ id: 'lamp', p: [0.2, 0.5], keyword: 'Flash lamp', parts: ['lamp', 'rod'] },
	// gap 0.5 .. 0.6
	{ id: 'fire', p: [0.6, 1], keyword: '694.3 nm', parts: ['can'] }
];

describe('scroll progress', () => {
	it('maps the section through the viewport to [0, 1]', () => {
		// section 5000 px tall, viewport 1000 px: run 4000 px
		expect(scrollProgress(0, 5000, 0, 1000)).toBe(0);
		expect(scrollProgress(-2000, 5000, 0, 1000)).toBe(0.5);
		expect(scrollProgress(-4000, 5000, 0, 1000)).toBe(1);
		// before and after the run: clamped
		expect(scrollProgress(300, 5000, 0, 1000)).toBe(0);
		expect(scrollProgress(-9000, 5000, 0, 1000)).toBe(1);
		// viewport offset (scroll container below the header)
		expect(scrollProgress(100, 5000, 100, 1000)).toBe(0);
		expect(scrollProgress(-1900, 5000, 100, 1000)).toBe(0.5);
	});
	it('handles a section not taller than the viewport', () => {
		expect(scrollProgress(10, 800, 0, 1000)).toBe(0);
		expect(scrollProgress(-10, 800, 0, 1000)).toBe(1);
	});
	it('scrollDeltaFor inverts scrollProgress', () => {
		for (const p of [0, 0.13, 0.5, 0.87, 1]) {
			const secTop = 1234;
			const d = scrollDeltaFor(p, secTop, 5000, 0, 1000);
			// scrolling by d moves the section up by d
			expect(scrollProgress(secTop - d, 5000, 0, 1000)).toBeCloseTo(p, 9);
		}
	});
});

describe('chapters', () => {
	it('finds the chapter under p, with gaps and the closed last end', () => {
		expect(chapterIndexAt(CH, 0)).toBe(0);
		expect(chapterIndexAt(CH, 0.199)).toBe(0);
		expect(chapterIndexAt(CH, 0.2)).toBe(1);
		expect(chapterIndexAt(CH, 0.55)).toBe(-1);
		expect(chapterIndexAt(CH, 1)).toBe(2);
		expect(chapterAt(CH, 0.7)?.id).toBe('fire');
		expect(chapterIndexBefore(CH, 0.55)).toBe(1);
		expect(chapterIndexBefore(CH, -0.1)).toBe(-1);
	});
	it('local progress and step targets stay inside the chapter', () => {
		expect(chapterLocal(CH[1], 0.35)).toBeCloseTo(0.5, 9);
		expect(chapterLocal(CH[1], 0.1)).toBe(0);
		expect(chapterLocal(CH[1], 0.9)).toBe(1);
		for (const c of CH) {
			const t = chapterTarget(c);
			expect(t).toBeGreaterThanOrEqual(c.p[0]);
			expect(t).toBeLessThan(c.p[1]);
			expect(chapterIndexAt(CH, t)).toBe(CH.indexOf(c));
		}
	});
	it('keywords: one fully shown at each step target, cross-fade inside, hold through gaps', () => {
		for (const c of CH) {
			const ks = keywordStates(CH, chapterTarget(c));
			const i = CH.indexOf(c);
			expect(ks[i].o).toBeCloseTo(1, 6);
			ks.forEach((k, j) => j !== i && expect(k.o).toBe(0));
		}
		// gap: the previous keyword holds
		expect(keywordStates(CH, 0.55)[1].o).toBe(1);
		// mid cross-fade: both partially visible, in range
		const mid = keywordStates(CH, 0.227);
		expect(mid[0].o).toBeGreaterThan(0);
		expect(mid[1].o).toBeGreaterThan(0);
		for (const k of mid) expect(k.o).toBeLessThanOrEqual(1);
	});
	it('keyword states are a pure function of p (same in both scroll directions)', () => {
		const ps = Array.from({ length: 101 }, (_, i) => i / 100);
		const fwd = ps.map((p) => keywordStates(CH, p));
		const back = [...ps].reverse().map((p) => keywordStates(CH, p)).reverse();
		expect(back).toEqual(fwd);
	});
	it('part introduction, plot range, assembled default, checks', () => {
		expect(partIntro(CH, 'rod')).toBe(0);
		expect(partIntro(CH, 'lamp')).toBe(0.2);
		expect(partIntro(CH, 'none')).toBe(0);
		expect(defaultAssembledAt(CH)).toBe(0.6);
		expect(plotRange({ chapters: CH, plots: [{ id: 'spec', x: { label: 'x' }, y: { label: 'y' }, series: [] }] }, 'spec')).toEqual([0.6, 1]);
		expect(plotRange({ chapters: [...CH.slice(0, 2), { ...CH[2], plot: 'spec' }], plots: [] }, 'spec')).toEqual([0.6, 1]);
		expect(plotRange({ chapters: CH, plots: [{ id: 'lamp', x: { label: 'x' }, y: { label: 'y' }, series: [] }] }, 'lamp')).toEqual([0.2, 0.5]);
		expect(checkChapters(CH)).toEqual([]);
		expect(checkChapters([CH[1], CH[0]]).length).toBeGreaterThan(0);
		expect(checkChapters([{ id: 'x', p: [0.5, 0.4], keyword: '' }]).length).toBe(1);
	});
	it('easing helpers', () => {
		expect(seg(0.5, 0, 1)).toBe(0.5);
		expect(seg(2, 0, 1)).toBe(1);
		expect(ease(0)).toBe(0);
		expect(ease(1)).toBe(1);
		expect(ease(0.5)).toBeCloseTo(0.5, 9);
	});
});

describe('plot geometry', () => {
	it('scales linear and log', () => {
		const lin = makeScale(0, 10, 0, 100, false);
		expect(lin.map(5)).toBe(50);
		const lg = makeScale(1, 1000, 0, 300, true);
		expect(lg.map(10)).toBeCloseTo(100, 9);
	});
	it('ticks and extents', () => {
		expect(linTicks(0, 10, 5)).toEqual([0, 2, 4, 6, 8, 10]);
		expect(logTicks(1, 1000)).toEqual([1, 10, 100, 1000]);
		const s = [{ name: 'a', points: [[1, -1], [5, 30], [20, 0.5]] as [number, number][] }];
		expect(extent(s, 0, true)).toEqual([1, 100]);
		const [lo, hi] = extent(s, 1, false);
		expect(lo).toBeLessThan(-1);
		expect(hi).toBeGreaterThan(30);
		expect(cleanPoints(s[0], false, true).length).toBe(2);
	});
	it('reveals axes first, then series staggered and overlapping', () => {
		expect(axesK(0.1)).toBeCloseTo(0.4, 9);
		expect(revealed(0.2, 2, 0, 10).n).toBe(0);
		expect(revealed(1, 2, 0, 10).n).toBe(10);
		expect(revealed(1, 2, 1, 10).n).toBe(10);
		// mid-way both series are partly drawn (no waiting for the previous series)
		const mid = [0, 1, 2].map((i) => revealed(0.6, 3, i, 10).n);
		expect(mid[0]).toBeGreaterThan(mid[1]);
		expect(mid[1]).toBeGreaterThan(0);
		// starts at even fractions, every window ends by r = 1
		const ws = [0, 1, 2, 3].map((i) => stagger(AXES_END, 1, i, 4));
		for (let i = 1; i < 4; i++) expect(ws[i][0] - ws[i - 1][0]).toBeCloseTo(ws[1][0] - ws[0][0], 9);
		expect(ws[3][1]).toBeCloseTo(1, 9);
		expect(stagger(0, 1, 0, 1)).toEqual([0, 1]);
	});
	it('bars: tuple and object forms, extents, growth', () => {
		const s = { name: 'b', points: [] as [number, number][], bars: [[3, 1, 2] as [number, number, number], { from: 5, to: 6, height: 0.5, line: 'R1' }, { from: NaN, to: 1, height: 1 }] };
		const bs = toBars(s);
		expect(bs).toEqual([
			{ from: 1, to: 3, height: 2 },
			{ from: 5, to: 6, height: 0.5, line: 'R1' }
		]);
		const [lo, hi] = extent([s], 0, false);
		expect(lo).toBeLessThan(1);
		expect(hi).toBeGreaterThan(6);
		expect(extent([s], 1, false)[1]).toBeGreaterThanOrEqual(2);
		expect(barK(AXES_END, 1, 0, 0, 2)).toBe(0);
		expect(barK(1, 1, 0, 1, 2)).toBe(1);
		expect(barK(0.6, 1, 0, 0, 2)).toBeGreaterThan(barK(0.6, 1, 0, 1, 2));
		// a series without points or bars does not crash the helpers
		expect(cleanPoints({ name: 'x' } as unknown as Series, false, false)).toEqual([]);
		expect(styleOf({ name: 'x' } as unknown as Series)).toBe('both');
	});
	it('axis ticks: scale none, step, explicit list', () => {
		expect(axisTicks({ label: 'y', scale: 'none' }, 0, 1, false, 5)).toEqual({ major: [], minor: [] });
		const st = axisTicks({ label: 'x', ticks: 1 }, 6925, 6950, false, 5);
		expect(st.minor.length).toBe(26);
		expect(st.major).toEqual([6925, 6930, 6935, 6940, 6945, 6950]);
		expect(axisTicks({ label: 'y', ticks: [0, 5, 10, 15, 20, 30] }, 0, 20, false, 5).major).toEqual([0, 5, 10, 15, 20]);
	});
	it('rich text and term symbols', () => {
		expect(rich('10^3 cm^-1')).toEqual([
			{ t: '10', k: '' },
			{ t: '3', k: 'sup' },
			{ t: ' cm', k: '' },
			{ t: '\u22121', k: 'sup' }
		]);
		expect(plain(rich('cm^{-1}'))).toBe('cm\u207b\u00b9');
		expect(term('4A2')).toEqual([
			{ t: '4', k: 'sup' },
			{ t: 'A', k: '' },
			{ t: '2', k: 'sub' }
		]);
		expect(term('2\u0100')).toEqual([
			{ t: '2', k: 'sup' },
			{ t: '\u0100', k: '' }
		]);
		expect(term('\u0112')).toEqual([{ t: '\u0112', k: '' }]);
		expect(plain(term('4F2'))).toBe('\u2074F\u2082');
	});
});

describe('per-plot axis state and alternates (MCVD round 3)', () => {
	const loss: Plot = { id: 'loss', x: { label: 'wavelength', unit: 'nm' }, y: { label: 'attenuation', unit: 'dB/km', log: true }, series: [] };
	const patent: Plot = { id: 'loss_patent', alt_of: 'loss', label: 'Patent FIG. 4', x: { label: 'wavelength' }, y: { label: 'insertion loss', log: true }, series: [] };
	const profile: Plot = { id: 'profile', x: { label: 'radius' }, y: { label: 'index difference' }, series: [] };
	it('log choices belong to a plot id: no carry-over between plots, either scroll direction', () => {
		let st: LogState = {};
		// chapter 9 (loss) then 10 (profile): each starts from its own spec default
		expect(logOf(st, loss)).toEqual({ x: false, y: true });
		expect(logOf(st, profile)).toEqual({ x: false, y: false });
		// user switches loss to linear y, scrolls on to profile and back
		st = toggleLog(st, loss, 'y');
		expect(logOf(st, profile)).toEqual({ x: false, y: false });
		expect(logOf(st, loss)).toEqual({ x: false, y: false });
		// toggling profile does not touch loss
		st = toggleLog(st, profile, 'x');
		expect(logOf(st, loss)).toEqual({ x: false, y: false });
		expect(logOf(st, profile)).toEqual({ x: true, y: false });
		// the alternate has its own default
		expect(logOf(st, patent)).toEqual({ x: false, y: true });
	});
	it('alternates: main first, then plots with alt_of; labels', () => {
		const ps = [loss, profile, patent];
		expect(withAlternates(ps, 'loss').map((q) => q.id)).toEqual(['loss', 'loss_patent']);
		expect(withAlternates(ps, 'profile').map((q) => q.id)).toEqual(['profile']);
		expect(withAlternates(ps, 'nope')).toEqual([]);
		expect(plotLabel(patent)).toBe('Patent FIG. 4');
		expect(plotLabel(loss)).toBe('loss');
		// an alternate never takes the default "first plot across the last chapter" slot by itself
		expect(plotRange({ chapters: CH, plots: [loss, patent] }, 'loss')).toEqual([0.6, 1]);
	});
	it('orbit limits: default keeps the camera above the horizon; overrides in degrees', () => {
		const d = orbitLimits();
		expect(d.polar[0]).toBeGreaterThan(0);
		expect(d.polar[1]).toBeLessThan(Math.PI / 2);
		expect(d.azimuth).toBeNull();
		const o = orbitLimits({ polar: [10, 120], azimuth: [-45, 45], distance: [50, 900] });
		expect(o.polar[0]).toBeCloseTo((10 * Math.PI) / 180, 9);
		expect(o.polar[1]).toBeCloseTo((120 * Math.PI) / 180, 9);
		expect(o.azimuth![1]).toBeCloseTo(Math.PI / 4, 9);
		expect(o.distance).toEqual([50, 900]);
		expect(orbitLimits({ polar: [90, 10] }).polar).toEqual(d.polar);
	});
	it('dashed style is kept', () => {
		expect(styleOf({ name: 'g', style: 'dashed', points: [] })).toBe('dashed');
	});
});

describe('ruby pass 2 helpers', () => {
	it('essential dim label text', () => {
		const d = (label: string, value: number, unit: string, extra = {}) => ({ label, value, unit, essential: true, ...extra });
		expect(essentialDimText([d('diameter', 10, 'mm'), d('length', 20, 'mm'), { label: 'x', value: 1, unit: 'mm' }])).toBe('10 mm x 20 mm');
		expect(essentialDimText([d('diameter', 10, 'mm', { label_short: 'dia.' }), d('length', 20, 'mm', { show_label: true })])).toBe('dia. 10 mm, length 20 mm');
		expect(essentialDimText([d('wavelength', 694.3, 'nm')])).toBe('694.3 nm');
		expect(essentialDimText(undefined)).toBe('');
	});
	it('transition end inside a band (to_energy)', () => {
		const pl: Plot = {
			id: 'l',
			kind: 'levels',
			y: { label: 'E', range: [0, 20] },
			levels: [
				{ id: 'g', energy: 0 },
				{ id: 'b', kind: 'band', energy: [15, 19] }
			],
			transitions: [{ from: 'g', to: 'b', kind: 'pump', to_energy: 17 }]
		};
		const g = levelsLayout(pl, 600, 500, 1);
		expect(g.arrows[0].y1).toBeCloseTo(g.Y.map(17), 9);
		const band = g.levels.find((l) => l.lv.id === 'b')!;
		expect(g.arrows[0].y1).toBeGreaterThan(band.yTop);
		expect(g.arrows[0].y1).toBeLessThan(band.yBot);
	});
});

describe('process step tooltip (D992)', () => {
	it('every param carries basis, source and locator', () => {
		const lines = stepTipLines({
			source: 'patent',
			params: [
				{ label: 'collapse temperature', value: 1460, unit: 'C', basis: 'stated', source: 'patent US 4,217,027 Example 1', locator: 'col. 9:12' },
				{ label: 'tube', value: '12 I.D. x 14 O.D.', unit: 'mm', basis: 'stated', locator: 'US 4,217,027 col. 6:60-61' },
				{ label: 'bare', value: 3 }
			]
		});
		expect(lines).toEqual([
			'collapse temperature: 1460 C',
			'  stated, patent US 4,217,027 Example 1, col. 9:12',
			'tube: 12 I.D. x 14 O.D. mm',
			'  stated, patent, US 4,217,027 col. 6:60-61',
			'bare: 3',
			'  patent'
		]);
	});
});

describe('ruby pass 3', () => {
	it('plain keyword and label placement', () => {
		expect(plainKeyword('Line *694.3 nm*')).toBe('Line 694.3 nm');
		expect(labelLeft(100, 120, 390)).toBe(110); // fits on the right
		expect(labelLeft(300, 210, 390)).toBe(80); // flips left
		const x = labelLeft(195, 380, 390); // wider than either side: clamped inside
		expect(x).toBeGreaterThanOrEqual(4);
		expect(x + 380).toBeLessThanOrEqual(386);
	});
});

describe('plot legend corner', () => {
	it('picks the emptiest corner, top-left on ties', () => {
		const area = { x0: 0, x1: 300, y0: 0, y1: 200 };
		expect(legendCorner([], area, 80, 30)).toMatchObject({ x: 6, y: 6, hits: 0 });
		// a peak in the top-left and top-right: the legend goes to a bottom corner
		const pts: [number, number][] = [[20, 10], [40, 20], [260, 15], [280, 25]];
		const c = legendCorner(pts, area, 80, 30);
		expect(c.hits).toBe(0);
		expect(c.y).toBeGreaterThan(100);
	});
});

describe('autoplay plan', () => {
	const plot2 = (i: number) => i === 2;
	it('moves to each chapter end, dwells, ends at 1; monotonic', () => {
		const legs = playPlan(CH, 0, plot2);
		expect(legs.map((l) => l.to)).toEqual([chapterTarget(CH[0]), chapterTarget(CH[1]), chapterTarget(CH[2]), 1]);
		expect(legs[0].dwell).toBe(PLAY.dwell);
		expect(legs[2].dwell).toBe(PLAY.plotDwell);
		const T = playDuration(legs);
		let prev = -1;
		for (let t = 0; t <= T + 100; t += 50) {
			const v = playAt(legs, t);
			expect(v).toBeGreaterThanOrEqual(prev - 1e-12);
			prev = v;
		}
		expect(playAt(legs, T + 1)).toBe(1);
		// dwell: p holds at the chapter end state
		const endMove = legs[0].t0 + legs[0].move;
		expect(playAt(legs, endMove + 10)).toBeCloseTo(legs[0].to, 9);
		expect(playAt(legs, endMove + legs[0].dwell - 10)).toBeCloseTo(legs[0].to, 9);
	});
	it('starts from the current p (skips finished chapters); reduced motion jumps', () => {
		const legs = playPlan(CH, 0.3);
		expect(legs[0].from).toBe(0.3);
		expect(legs[0].to).toBe(chapterTarget(CH[1]));
		const red = playPlan(CH, 0, () => false, true);
		expect(red.every((l) => l.move === 0)).toBe(true);
		expect(playAt(red, 1)).toBe(chapterTarget(CH[0]));
		expect(playPlan(CH, 1)).toEqual([]);
		expect(playAt([], 5)).toBe(1);
	});
});

describe('levels diagram geometry', () => {
	// shape of the maiman1960 spec's `kind: levels` plot
	const LV: Plot = {
		id: 'levels',
		kind: 'levels',
		y: { label: 'Energy', unit: '10^3 cm^-1', range: [0, 20], ticks: [0, 5, 10, 15, 20] },
		levels: [
			{ id: '4A2', label: '4A2', kind: 'line', energy: 0 },
			{ id: '4F2', label: '4F2', kind: 'band', energy: [15.3, 19.2] },
			{ id: '2E', label: '2E', kind: 'line', energy: 13.07 },
			{ id: '2Abar', label: '2\u0100', kind: 'line', energy: 14.25 },
			{ id: 'Ebar', label: '\u0112', kind: 'line', energy: 12.15 }
		],
		splits: [{ between: ['2Abar', 'Ebar'], value: 29, unit: 'cm^-1' }],
		transitions: [
			{ from: '4A2', to: '4F2', kind: 'pump' },
			{ from: '4F2', to: '2E', kind: 'nonradiative' },
			{ from: '2E', to: '4A2', kind: 'emission' },
			{ from: '2Abar', to: '4A2', label: 'R2', kind: 'emission' },
			{ from: 'Ebar', to: '4A2', label: 'R1', kind: 'emission' },
			{ from: 'nope', to: '4A2', kind: 'emission' }
		]
	};
	const W = 600;
	const H = 500;
	it('places levels by energy, columns by role', () => {
		const g = levelsLayout(LV, W, H, 1);
		const by = Object.fromEntries(g.levels.map((l) => [l.lv.id, l]));
		expect(by['4A2'].col).toBe('full');
		expect(by['2Abar'].col).toBe('right');
		expect(by['Ebar'].col).toBe('right');
		expect(by['2E'].col).toBe('left');
		expect(by['4F2'].band).toBe(true);
		// y down: higher energy is higher on screen
		expect(by['4F2'].yTop).toBeLessThan(by['4F2'].yBot);
		expect(by['2E'].yTop).toBeLessThan(by['4A2'].yTop);
		expect(g.Y.map(20)).toBeCloseTo(g.yTop, 6);
		expect(g.Y.map(0)).toBeCloseTo(g.yBot, 6);
		expect(g.ticks).toEqual([0, 5, 10, 15, 20]);
		for (const l of g.levels) {
			expect(l.x0).toBeGreaterThanOrEqual(0);
			expect(l.x1).toBeLessThanOrEqual(W);
			expect(l.k).toBe(1);
		}
	});
	it('split bracket spans the two levels; transitions end on the right edges', () => {
		const g = levelsLayout(LV, W, H, 1);
		const by = Object.fromEntries(g.levels.map((l) => [l.lv.id, l]));
		expect(g.splits).toHaveLength(1);
		expect(g.splits[0].ya).toBeCloseTo(by['2Abar'].yTop, 6);
		expect(g.splits[0].yb).toBeCloseTo(by['Ebar'].yTop, 6);
		expect(g.splits[0].x).toBeGreaterThan(by['2Abar'].x1);
		expect(g.arrows).toHaveLength(5); // unknown level dropped
		const [pump, nr, em, r2, r1] = g.arrows;
		expect(pump.kind).toBe('pump');
		expect(pump.y0).toBeCloseTo(by['4A2'].yTop, 6);
		expect(pump.y1).toBeCloseTo(by['4F2'].yBot, 6); // up into the band: its lower edge
		expect(nr.y0).toBeCloseTo(by['4F2'].yBot, 6); // down out of the band: its lower edge
		expect(nr.kind).toBe('nonradiative');
		expect(em.y1).toBeCloseTo(by['4A2'].yTop, 6);
		for (const a of [r2, r1]) expect(a.x).toBeGreaterThanOrEqual(by['2Abar'].x0);
		for (const a of [pump, nr, em]) expect(a.x).toBeLessThanOrEqual(by['2E'].x1);
		expect(new Set(g.arrows.map((a) => a.x)).size).toBe(5);
		for (const a of g.arrows) expect(a.yTip).toBeCloseTo(a.y1, 6);
	});
	it('assembles by r: axis, then levels bottom-up, then arrows', () => {
		const g0 = levelsLayout(LV, W, H, 0);
		expect(g0.axisK).toBe(0);
		expect(g0.levels.every((l) => l.k === 0)).toBe(true);
		expect(g0.arrows.every((a) => a.k === 0 && a.head === null)).toBe(true);
		const g = levelsLayout(LV, W, H, 0.3);
		const by = Object.fromEntries(g.levels.map((l) => [l.lv.id, l]));
		expect(by['4A2'].k).toBeGreaterThan(by['4F2'].k);
		expect(g.arrows.every((a) => a.k === 0)).toBe(true);
		const g2 = levelsLayout(LV, W, H, 0.8);
		expect(g2.arrows[0].k).toBeGreaterThan(g2.arrows[4].k);
		// pure: same r, same geometry
		expect(JSON.stringify(levelsLayout(LV, W, H, 0.8))).toBe(JSON.stringify(g2));
	});
	it('a levels plot without series or levels does not crash', () => {
		const g = levelsLayout({ id: 'x', kind: 'levels', y: { label: 'E' } }, W, H, 1);
		expect(g.levels).toEqual([]);
		expect(g.arrows).toEqual([]);
	});
});

describe('trace geometry (ported from ipatent)', () => {
	it('path points and element boxes', () => {
		expect(pathPoints('M 0 0 L 10 0 H 20 V 5 Z')).toEqual([
			[0, 0],
			[10, 0],
			[20, 0],
			[20, 5]
		]);
		expect(elementBox({ shapes: [{ t: 'r', d: [1, 2, 11, 12] }, { t: 'c', d: [20, 20, 5] }] })).toEqual([1, 2, 25, 25]);
		expect(elementBox({ shapes: [] })).toBeNull();
	});
});
