// Curated layouts (DevLog-013 D505-D508): drawings computed by scripts/layouts/cells/*.py after the source figures were
// read. A shape states its source; row-sourced labels render the stored value, never a retyped one.
import { getJson } from '../paths';
import type { Component, Metric } from '../components.svelte';
import { MATERIALS } from './materials';
import { BASIS, resolveDim, rowLabel, type Dim } from './resolve';
import type { Label, Mark, Pt, Scene, Shape } from './scene';

interface RawShape {
	r: Pt[][];
	m: string;
	role: string;
	src: string[];
	layer?: string;
	a?: number;
	lod?: number;
	line?: boolean;
}
interface RawMark {
	dir: 'h' | 'v';
	a: number;
	b: number;
	pos: number;
	px: number;
	from: [number, number];
	row: string;
	text: string;
	src: string[];
	inset?: boolean;
}
interface RawLabel {
	at: Pt;
	text: string;
	anchor: 'start' | 'middle' | 'end';
	dx: number;
	dy: number;
	tip: string;
	row?: string;
}
export interface RawView {
	id: string;
	title: string;
	kind: string;
	like?: string;
	window?: [number, number, number, number];
	shapes: RawShape[];
	marks: RawMark[];
	labels: RawLabel[];
	notes: string[];
}
export interface CuratedLayout {
	component_id: string;
	sources: string[];
	summary: string;
	thumb: { view?: string; window?: [number, number, number, number] };
	checks: string[];
	views: RawView[];
	/** Why some views are not published (DevLog-013 D510). */
	not_drawn: string[];
}
export interface CuratedEntry {
	sources: string[];
	summary: string;
	drawn: boolean;
	not_drawn: string[];
}

class CuratedState {
	index = $state.raw<Record<string, CuratedEntry> | null>(null);
	got = $state.raw<Record<string, CuratedLayout>>({});
	failed = $state.raw<Record<string, string>>({});
}
export const curated = new CuratedState();
let indexStarted = false;
const started = new Set<string>();

export async function loadCuratedIndex(): Promise<void> {
	if (indexStarted) return;
	indexStarted = true;
	try {
		curated.index = await getJson<Record<string, CuratedEntry>>('data/layouts/index.json');
	} catch {
		curated.index = {}; // no curated drawings: every component keeps its template scene
	}
}
export async function loadCurated(id: string): Promise<void> {
	if (started.has(id)) return;
	started.add(id);
	try {
		const d = await getJson<CuratedLayout>(`data/layouts/${id}.json`);
		curated.got = { ...curated.got, [id]: d };
	} catch (e) {
		curated.failed = { ...curated.failed, [id]: e instanceof Error ? e.message : String(e) };
	}
}

const rowOf = (c: Component, short: string): Metric | undefined => c.metrics.find((m) => m.metric_id.endsWith('-' + short));

/** One source entry in words (row: parameter, stored value, basis, locator). */
export function srcText(c: Component, s: string): string {
	const i = s.indexOf(':');
	const k = s.slice(0, i), v = s.slice(i + 1);
	if (k === 'row') {
		const m = rowOf(c, v);
		return m ? `${m.parameter} ${rowLabel(m)} [${m.basis}, ${m.locator}]` : `row ${v}`;
	}
	if (k === 'text') return 'stated: ' + v;
	if (k === 'fig') return 'read from ' + v;
	return 'assumed: ' + v;
}

function shapeOf(c: Component, s: RawShape): Shape {
	const mat = MATERIALS[s.m] ?? s.m;
	return {
		rings: s.r,
		mat: s.m,
		role: s.role,
		schematic: s.src.some((x) => x.startsWith('assumed:')),
		tip: [s.line ? s.role : `${s.role}: ${mat}`, ...s.src.map((x) => srcText(c, x))].join('\n'),
		alpha: s.a,
		line: s.line,
		layer: s.layer,
		lod: s.lod
	};
}

function rowDim(c: Component, short: string): Dim | null {
	const m = rowOf(c, short);
	if (!m) return null;
	return { ...resolveDim(c, m.parameter, ['top'], false, '', m), alts: [] };
}

function freeDim(c: Component, text: string, src: string[]): Dim {
	const isFig = src.some((x) => x.startsWith('fig:'));
	return {
		param: '', views: ['top'], required: false, row: null, alts: [], num: null, unit: '', label: text,
		basis: isFig ? 'figure' : 'other', badge: isFig ? BASIS.extracted_from_figure.badge : 'T', tip: src.map((x) => srcText(c, x)).join('\n'), free: true
	};
}

/** A curated view as a renderable scene. `like` views share another view's shapes. */
export function curatedScene(l: CuratedLayout, v: RawView, c: Component): Scene {
	const base = v.like ? (l.views.find((x) => x.id === v.like) ?? v) : v;
	const shapes = [...base.shapes, ...(v.like ? v.shapes : [])].map((s) => shapeOf(c, s));
	const marks: Mark[] = v.marks.flatMap((m) => {
		const dim = m.row ? rowDim(c, m.row) : freeDim(c, m.text, m.src);
		return dim ? [{ dir: m.dir, a: m.a, b: m.b, from: m.from, pos: m.pos, px: m.px, dim, inset: m.inset }] : [];
	});
	const labels: Label[] = v.labels.map((x) => {
		const dim = x.row ? rowDim(c, x.row) : undefined;
		return { at: x.at, text: x.text + (dim ? ' ' + dim.label : ''), anchor: x.anchor, dx: x.dx, dy: x.dy, tip: x.tip, dim: dim ?? undefined, muted: !dim };
	});
	const partial = shapes.some((s) => s.schematic && !s.line);
	return { view: v.kind === 'xsec' ? 'xsec' : 'top', title: v.title, shapes, marks, labels, notes: v.notes, stretch: false, schematic: false, partial, window: v.window };
}

export function layersOf(scenes: Scene[]): { layer: string; mat: string; schematic: boolean }[] {
	const out = new Map<string, { layer: string; mat: string; schematic: boolean }>();
	for (const s of scenes) for (const sh of s.shapes) if (!sh.line && sh.layer && !out.has(sh.layer)) out.set(sh.layer, { layer: sh.layer, mat: sh.mat, schematic: sh.schematic });
	return [...out.values()];
}
