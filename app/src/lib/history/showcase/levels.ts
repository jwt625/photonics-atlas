// Pure geometry of an energy-level diagram (plot `kind: levels`, LevelsDiagram.svelte): energy axis, level lines and
// bands, split brackets, transition arrows, and how much of each is drawn at plot progress r. No DOM.
import { axisTicks, makeScale, staggerK, type Scale } from './plot';
import { seg } from './progress';
import type { Level, Plot, Split, Transition } from './types';

export const PAD = { l: 52, r: 14, t: 26, b: 18 };
const BRACKET_W = 76; // room right of the right column for split brackets and their labels
const LEFT: [number, number] = [0.06, 0.5];
const RIGHT: [number, number] = [0.58, 1];

export interface LevelG {
	lv: Level;
	band: boolean;
	x0: number;
	x1: number;
	/** top and bottom px (equal for a line) */
	yTop: number;
	yBot: number;
	/** reveal 0..1 (line grows from x0, band fades and grows) */
	k: number;
	col: 'full' | 'left' | 'right';
}
export interface SplitG {
	sp: Split;
	x: number;
	ya: number;
	yb: number;
	k: number;
}
export interface ArrowG {
	tr: Transition;
	kind: 'pump' | 'nonradiative' | 'emission' | 'other';
	x: number;
	/** start and end px (y down) */
	y0: number;
	y1: number;
	/** current tip after reveal */
	yTip: number;
	k: number;
	/** arrowhead triangle at the tip, or null before it shows */
	head: [number, number][] | null;
}
export interface LevelsGeom {
	Y: Scale;
	ticks: number[];
	axisK: number;
	levels: LevelG[];
	splits: SplitG[];
	arrows: ArrowG[];
	/** plot area */
	x0: number;
	x1: number;
	yTop: number;
	yBot: number;
}

export const lo = (e: Level['energy']): number => (Array.isArray(e) ? Math.min(e[0], e[1]) : e);
export const hi = (e: Level['energy']): number => (Array.isArray(e) ? Math.max(e[0], e[1]) : e);

function energyRange(plot: Plot): [number, number] {
	const r = plot.y?.range;
	if (r && r.length === 2 && r[1] > r[0]) return r;
	const ls = plot.levels ?? [];
	if (!ls.length) return [0, 1];
	const a = Math.min(...ls.map((l) => lo(l.energy)));
	const b = Math.max(...ls.map((l) => hi(l.energy)));
	const pad = (b - a || 1) * 0.06;
	return [a - pad, b + pad];
}

const kindOf = (k: string | undefined): ArrowG['kind'] => (k === 'pump' || k === 'nonradiative' || k === 'emission' ? k : 'other');

/** Layout of a levels plot in a w x h box at plot progress r. */
export function levelsLayout(plot: Plot, w: number, h: number, r: number): LevelsGeom {
	const ls = (plot.levels ?? []).filter((l) => l && l.id != null && (Number.isFinite(lo(l.energy)) && Number.isFinite(hi(l.energy))));
	const [e0, e1] = energyRange(plot);
	const yBot = Math.max(PAD.t + 10, h - PAD.b);
	const yTop = PAD.t;
	const Y = makeScale(e0, e1, yBot, yTop, false);
	const ticks = axisTicks(plot.y, e0, e1, false, Math.max(2, Math.floor(h / 60))).major;
	const x0 = PAD.l + 6;
	const splits = (plot.splits ?? []).filter((s) => Array.isArray(s.between) && s.between.length === 2);
	const hasRight = splits.length > 0;
	const x1 = Math.max(x0 + 40, w - PAD.r - (hasRight ? BRACKET_W : 0));
	const W = x1 - x0;
	const inSplit = new Set(splits.flatMap((s) => s.between));
	const lowest = ls.length ? ls.reduce((m, l) => (lo(l.energy) < lo(m.energy) ? l : m)) : null;
	const colOf = (l: Level): LevelG['col'] => (l === lowest ? 'full' : hasRight && inSplit.has(l.id) ? 'right' : 'left');
	const span = (c: LevelG['col']): [number, number] => (c === 'full' ? [0, 1] : c === 'right' ? RIGHT : hasRight ? LEFT : [0.06, 0.94]);

	// levels appear bottom-up
	const order = [...ls].sort((a, b) => lo(a.energy) - lo(b.energy));
	const levels: LevelG[] = ls.map((lv) => {
		const col = colOf(lv);
		const [f0, f1] = Array.isArray(lv.x) && lv.x.length === 2 ? lv.x : span(col);
		const band = lv.kind === 'band' || Array.isArray(lv.energy);
		return {
			lv,
			band,
			col,
			x0: x0 + f0 * W,
			x1: x0 + f1 * W,
			yTop: Y.map(hi(lv.energy)),
			yBot: Y.map(lo(lv.energy)),
			k: staggerK(r, 0.12, 0.55, order.indexOf(lv), order.length)
		};
	});
	const byId = new Map(levels.map((g) => [g.lv.id, g]));

	const splitG: SplitG[] = [];
	splits.forEach((sp, i) => {
		const a = byId.get(sp.between[0]);
		const b = byId.get(sp.between[1]);
		if (!a || !b) return;
		const ya = (a.yTop + a.yBot) / 2;
		const yb = (b.yTop + b.yBot) / 2;
		splitG.push({ sp, x: Math.max(a.x1, b.x1) + 8, ya: Math.min(ya, yb), yb: Math.max(ya, yb), k: staggerK(r, 0.5, 0.62, i, splits.length) });
	});

	// transitions: one slot each, in the column of their upper (non-ground) level
	const trs = (plot.transitions ?? []).filter((t) => byId.has(t.from) && byId.has(t.to));
	const colTr = (t: Transition): 'left' | 'right' => {
		const a = byId.get(t.from)!;
		const b = byId.get(t.to)!;
		const c = a.col !== 'full' ? a.col : b.col;
		return c === 'right' ? 'right' : 'left';
	};
	const groups = { left: trs.filter((t) => colTr(t) === 'left'), right: trs.filter((t) => colTr(t) === 'right') };
	const arrows: ArrowG[] = trs.map((tr, i) => {
		const c = colTr(tr);
		const g = groups[c];
		const j = g.indexOf(tr);
		// slot inside the overlap of both levels' extents
		const a = byId.get(tr.from)!;
		const b = byId.get(tr.to)!;
		const sx0 = Math.max(a.x0, b.x0);
		const sx1 = Math.min(a.x1, b.x1);
		const x = sx1 > sx0 ? sx0 + ((j + 1) / (g.length + 1)) * (sx1 - sx0) : (a.x0 + a.x1) / 2;
		const mid = (l: Level) => (lo(l.energy) + hi(l.energy)) / 2;
		const up = mid(b.lv) > mid(a.lv);
		// a band endpoint is its edge facing the other level
		// from_energy / to_energy (drawn scale) put an end inside a band; else a band end is its edge facing the other level
		const y0 = Number.isFinite(tr.from_energy) ? Y.map(tr.from_energy!) : a.band ? (up ? a.yTop : a.yBot) : a.yTop;
		const y1 = Number.isFinite(tr.to_energy) ? Y.map(tr.to_energy!) : b.band ? (up ? b.yBot : b.yTop) : b.yTop;
		const k = staggerK(r, 0.6, 1, i, trs.length);
		const yTip = y0 + (y1 - y0) * k;
		const dir = Math.sign(y1 - y0) || 1;
		const head: [number, number][] | null =
			k > 0.02
				? [
						[x, yTip],
						[x - 4, yTip - dir * 9],
						[x + 4, yTip - dir * 9]
					]
				: null;
		return { tr, kind: kindOf(tr.kind), x, y0, y1, yTip, k, head };
	});

	return { Y, ticks, axisK: seg(r, 0, 0.15), levels, splits: splitG, arrows, x0, x1, yTop, yBot };
}
