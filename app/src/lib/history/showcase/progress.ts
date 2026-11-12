// Pure helpers of the showcase runtime (DevLog-017): scroll position -> progress p, chapter lookup, keyword fades,
// step targets. No DOM; tested in progress.test.ts. Scene modules may use the easing helpers too.
import type { Chapter, Dim, Part, PickInfo, ProcessStep, ShowcaseSpec } from './types';

/** Text after a number for its unit: " mm", " GHz"; angle and percent units attach without a space ("26°", "5%");
 *  "deg" / "degree(s)" print as "°". Used everywhere a value meets its unit (labels, tooltips, panel). */
export function unitSuffix(unit?: string | null): string {
	const u = (unit ?? '').trim();
	if (!u) return '';
	// unit exponent shorthand (cm^-3, cm^2) becomes markup, so every place that renders markup shows a superscript
	const uu = /^deg(rees?)?$/i.test(u) ? '\u00b0' : u.replace(/\^(-?\d+)/g, '^{$1}');
	return /^(\u00b0|%|\u2032|\u2033)/.test(uu) ? uu : ' ' + uu;
}
export const withUnit = (v: number | string, unit?: string | null): string => `${v}${unitSuffix(unit)}`;

export const clamp01 = (x: number): number => (x < 0 ? 0 : x > 1 ? 1 : Number.isFinite(x) ? x : 0);

/** Local progress of p inside [a, b], clamped to [0, 1]. */
export const seg = (p: number, a: number, b: number): number => (b > a ? clamp01((p - a) / (b - a)) : p >= b ? 1 : 0);

/** Smooth ease in-out (cubic). */
export const ease = (t: number): number => {
	const x = clamp01(t);
	return x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2;
};

/** Ease out (cubic). */
export const easeOut = (t: number): number => 1 - (1 - clamp01(t)) ** 3;

export const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;

/**
 * Story progress from the section geometry, all in the same coordinate frame (e.g. getBoundingClientRect):
 * p = 0 when the section top reaches the top of the scroll viewport, p = 1 when its bottom reaches the viewport bottom
 * (the sticky stage is then about to leave). Sections not taller than the viewport give 0 above and 1 below.
 */
export function scrollProgress(secTop: number, secHeight: number, viewTop: number, viewHeight: number): number {
	const run = secHeight - viewHeight;
	if (!(run > 0)) return viewTop >= secTop ? 1 : 0;
	return clamp01((viewTop - secTop) / run);
}

/** Scroll offset (added to the current scrollTop) that brings the section to progress p; inverse of scrollProgress. */
export function scrollDeltaFor(p: number, secTop: number, secHeight: number, viewTop: number, viewHeight: number): number {
	const run = Math.max(0, secHeight - viewHeight);
	return secTop + clamp01(p) * run - viewTop;
}

/** Index of the chapter whose [p0, p1) holds p (the last chapter also owns p1), or -1 in a gap / outside. */
export function chapterIndexAt(chapters: readonly Chapter[], p: number): number {
	for (let i = 0; i < chapters.length; i++) {
		const [a, b] = chapters[i].p;
		if (p >= a && (p < b || (i === chapters.length - 1 && p <= b))) return i;
	}
	return -1;
}

export function chapterAt(chapters: readonly Chapter[], p: number): Chapter | null {
	const i = chapterIndexAt(chapters, p);
	return i < 0 ? null : chapters[i];
}

/** The chapter under p or, in a gap, the last chapter that started before p (-1 before the first). */
export function chapterIndexBefore(chapters: readonly Chapter[], p: number): number {
	let k = -1;
	for (let i = 0; i < chapters.length; i++) if (p >= chapters[i].p[0]) k = i;
	return k;
}

/** Local progress q in [0, 1] of p inside a chapter. */
export function chapterLocal(c: Chapter, p: number): number {
	return seg(p, c.p[0], c.p[1]);
}

export const FADE = 0.2; // share of a chapter used for the keyword change: the previous one leaves in the first half,
// the new one comes in over the last 60 % (short overlap)

/**
 * Opacity and vertical offset (px, positive = below) of each chapter keyword at p. Inside the first FADE of a chapter's
 * range the previous keyword rises out (first half) and the new one rises in (from 40 % to 100 % of FADE); a keyword
 * holds to the end of its chapter and through a following gap. Before the first chapter nothing shows.
 */
export function keywordStates(chapters: readonly Chapter[], p: number, rise = 28): { o: number; dy: number }[] {
	return chapters.map((c, i) => {
		const len = c.p[1] - c.p[0];
		const inK = seg(p, c.p[0] + 0.4 * FADE * len, c.p[0] + FADE * len);
		const next = chapters[i + 1];
		const outK = next ? seg(p, next.p[0], next.p[0] + 0.5 * FADE * (next.p[1] - next.p[0])) : 0;
		const o = Math.min(easeOut(inK), 1 - outK);
		const dy = inK < 1 ? (1 - easeOut(inK)) * rise : -outK * rise;
		return { o: Math.max(0, o), dy };
	});
}

/** p a step button jumps to: the chapter's settled end state. */
export function chapterTarget(c: Chapter): number {
	const [a, b] = c.p;
	return Math.max(a, Math.min(b - 0.002, a + 0.98 * (b - a)));
}

/** p of the first chapter that lists a part (where it appears), or 0 when no chapter lists it. */
export function partIntro(chapters: readonly Chapter[], id: string): number {
	for (const c of chapters) if (c.parts?.includes(id)) return c.p[0];
	return 0;
}

/** Where a plot assembles: the chapter that names it (chapter.plot or same id), else the last chapter for the first plot. */
export function plotRange(spec: Pick<ShowcaseSpec, 'chapters' | 'plots'>, plotId: string): [number, number] | null {
	const cs = spec.chapters;
	const c = cs.find((c) => c.plot === plotId) ?? cs.find((c) => c.id === plotId && !c.plot);
	if (c) return c.p;
	const anyNamed = cs.some((c) => c.plot || spec.plots?.some((pl) => pl.id === c.id));
	if (!anyNamed && spec.plots?.[0]?.id === plotId && cs.length) return cs[cs.length - 1].p;
	return null;
}

/** Default p from which orbit and explode are offered: start of the last chapter. */
export function defaultAssembledAt(chapters: readonly Chapter[]): number {
	return chapters.length ? chapters[chapters.length - 1].p[0] : 0;
}

/** Problems with a chapter list (empty = fine): ranges inside [0, 1], ordered, non-overlapping. */
export function checkChapters(chapters: readonly Chapter[]): string[] {
	const out: string[] = [];
	let prev = 0;
	chapters.forEach((c, i) => {
		const [a, b] = c.p ?? [NaN, NaN];
		if (!(a >= 0 && b <= 1 && a < b)) out.push(`${c.id}: bad range [${a}, ${b}]`);
		if (i && a < prev) out.push(`${c.id}: overlaps the previous chapter`);
		prev = b;
	});
	return out;
}

export const DEG = Math.PI / 180;

/** Free-orbit limits in radians / world units from degrees (spec.orbit or handle.orbit). Default polar [2, 88] deg from
 *  +y: top view allowed, never below the horizon (no view from under the floor). Invalid ranges fall back. */
export function orbitLimits(o?: { polar?: [number, number]; azimuth?: [number, number]; distance?: [number, number] }): {
	polar: [number, number];
	azimuth: [number, number] | null;
	distance: [number, number] | null;
} {
	const ok = (r?: [number, number]): r is [number, number] => Array.isArray(r) && r.length === 2 && r.every(Number.isFinite) && r[0] <= r[1];
	const polar: [number, number] = ok(o?.polar) ? [Math.max(0, o.polar[0]) * DEG, Math.min(180, o.polar[1]) * DEG] : [2 * DEG, 88 * DEG];
	return {
		polar,
		azimuth: ok(o?.azimuth) ? [o.azimuth[0] * DEG, o.azimuth[1] * DEG] : null,
		distance: ok(o?.distance) && o.distance[0] >= 0 ? o.distance : null
	};
}

// ------------------------------------------------------------------------------------------- autoplay (Play button)
/** Autoplay pacing, ms: move to the next chapter's end state, then a near-zero dwell (owner 2026-11-11: no pause between
 *  stages). Reduced motion has no move, so each chapter is held for reducedDwell instead. */
export const PLAY = { move: 3500, dwell: 80, plotDwell: 80, reducedDwell: 1500 };

export interface PlayLeg {
	/** start time, ms */
	t0: number;
	from: number;
	to: number;
	move: number;
	dwell: number;
}

/**
 * Autoplay plan from p0: one leg per remaining chapter (to its settled end state, chapterTarget), then a last leg to
 * p = 1. `plotChapter(i)` marks chapters whose plot gets the longer dwell. reduced: moves take 0 ms (jump + dwell).
 */
export function playPlan(
	chapters: readonly Chapter[],
	p0: number,
	plotChapter: (i: number) => boolean = () => false,
	reduced = false,
	pace: { move: number; dwell: number; plotDwell: number; reducedDwell?: number } = PLAY
): PlayLeg[] {
	const legs: PlayLeg[] = [];
	let t = 0;
	let from = clamp01(p0);
	chapters.forEach((c, i) => {
		const to = chapterTarget(c);
		if (to <= from + 0.002) return;
		const move = reduced ? 0 : pace.move;
		const dwell = reduced ? (pace.reducedDwell ?? pace.dwell) : plotChapter(i) ? pace.plotDwell : pace.dwell;
		legs.push({ t0: t, from, to, move, dwell });
		t += move + dwell;
		from = to;
	});
	if (from < 1) legs.push({ t0: t, from, to: 1, move: reduced ? 0 : Math.min(pace.move, 800), dwell: 0 });
	return legs;
}

export const playDuration = (legs: readonly PlayLeg[]): number => (legs.length ? legs[legs.length - 1].t0 + legs[legs.length - 1].move + legs[legs.length - 1].dwell : 0);

/** Play easing: mostly linear with a light ease, so motion keeps going through chapter ends instead of stopping. */
const playEase = (k: number): number => 0.75 * k + 0.25 * ease(k);

/** p at time t (ms) of a plan: a near-linear move, then hold at the chapter end; after the plan, its last p. */
export function playAt(legs: readonly PlayLeg[], t: number): number {
	if (!legs.length) return 1;
	let cur = legs[0].from;
	for (const L of legs) {
		if (t < L.t0) break;
		const k = L.move > 0 ? playEase(seg(t, L.t0, L.t0 + L.move)) : 1;
		cur = L.from + (L.to - L.from) * k;
	}
	return cur;
}

/** Canvas label text of a part's essential dims: "10 mm x 20 mm" when the units agree and no dim shows its name, else
 *  comma separated; a dim with label_short / show_label is prefixed with that name ("dia. 10 mm, length 20 mm"). */
export function essentialDimText(dims: readonly Dim[] | undefined): string {
	const ds = (dims ?? []).filter((x) => x.essential);
	const name = (d: Dim) => d.label_short || (d.show_label ? d.label : '');
	const one = (d: Dim) => [name(d), withUnit(d.value, d.unit)].filter(Boolean).join(' ');
	if (ds.length < 2) return ds.map(one).join('');
	const same = ds.every((d) => (d.unit ?? '') === (ds[0].unit ?? '')) && !ds.some(name);
	return ds.map(one).join(same ? ' x ' : ', ');
}

/** Tooltip lines of a process step: each param as "label: value unit", followed by its provenance
 *  "basis, source, locator" (param source, else the step's source), as plot points print theirs (D992). */
export function stepTipLines(step: Pick<ProcessStep, 'params' | 'source'>): string[] {
	return (step.params ?? []).flatMap((q) => {
		const prov = [q.basis, q.source ?? step.source, q.locator].filter(Boolean).join(', ');
		return [`${q.label}: ${withUnit(q.value, q.unit)}`, ...(prov ? [`  ${prov}`] : [])];
	});
}

/** Keyword as plain text (buttons, tooltips, aria): the *emphasis* markers removed. */
export const plainKeyword = (t: string): string => String(t ?? '').replace(/\*/g, '');

export const LABEL_GAP = 10;
/** Left edge (pane px) of a canvas label of width w anchored at x: right of the anchor when it fits, else left of it,
 *  else clamped inside the pane (the label then wraps to the pane width). */
export function labelLeft(x: number, w: number, paneW: number, pad = 4): number {
	if (x + LABEL_GAP + w <= paneW - pad) return x + LABEL_GAP;
	if (x - LABEL_GAP - w >= pad) return x - LABEL_GAP - w;
	return Math.max(pad, Math.min(paneW - pad - w, x - w / 2));
}

/** Tooltip lines of a part: name, role, then extra lines (a PickInfo detail), then its essential dims. */
export function partTipLines(q: Pick<Part, 'name' | 'role' | 'dims'>, extra: readonly string[] = []): string[] {
	const dims = (q.dims ?? []).filter((d) => d.essential).map((d) => `${d.label}: ${withUnit(d.value, d.unit)}`);
	return [q.name, q.role ?? '', ...extra, ...dims].filter(Boolean);
}

/** Detail lines of a pick result (PickInfo.detail as a list; nothing for a plain id). */
export function pickDetail(hit: string | PickInfo | null): string[] {
	if (!hit || typeof hit === 'string' || hit.detail == null) return [];
	return (Array.isArray(hit.detail) ? hit.detail : [hit.detail]).filter(Boolean);
}

/** p of a story's thumbnail frame: spec.thumb_p, else the settled end of the last chapter before the first plot chapter
 *  (model assembled, no plot on screen), else the end of the last chapter. */
export function thumbP(spec: Pick<ShowcaseSpec, 'chapters' | 'plots' | 'thumb_p'>): number {
	if (typeof spec.thumb_p === 'number' && Number.isFinite(spec.thumb_p)) return clamp01(spec.thumb_p);
	const cs = spec.chapters ?? [];
	if (!cs.length) return 0;
	let first = Infinity;
	for (const pl of spec.plots ?? []) {
		if (pl.alt_of) continue;
		const r = plotRange(spec, pl.id);
		if (!r) continue;
		const i = cs.findIndex((c) => c.p[0] === r[0] && c.p[1] === r[1]);
		if (i >= 0) first = Math.min(first, i);
	}
	if (!Number.isFinite(first)) return chapterTarget(cs[cs.length - 1]);
	return chapterTarget(cs[Math.max(0, first - 1)]);
}

/** Parts greyed as not drawn: those missing from the module's visible() list (null = all drawn; undefined = no hook),
 *  else the chapter's parts_hidden. */
export function hiddenParts(ids: readonly string[], visible: readonly string[] | null | undefined, chapterHidden?: readonly string[]): Set<string> {
	if (visible === null) return new Set(); // the module says: everything drawn
	if (Array.isArray(visible)) {
		const v = new Set(visible);
		return new Set(ids.filter((id) => !v.has(id)));
	}
	return new Set((chapterHidden ?? []).filter((id) => ids.includes(id)));
}
