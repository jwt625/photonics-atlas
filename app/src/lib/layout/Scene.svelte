<script lang="ts">
	// SVG renderer of one layout scene, always at true scale (both axes equal; DevLog-013 D508). Wheel zooms about the
	// pointer, drag pans, double click fits. Thumbnails and the compact panel do not capture the wheel. Dimension marks
	// carry the stored value + unit and a basis badge; dashed shapes are not from the source. Hover tips come from the
	// shapes and the metric rows.
	import './layout.css';
	import type { Dim } from './resolve';
	import type { Label, Mark, Pt, Scene } from './scene';

	let { scene, height = 300, compact = false, thumb = false, hidden = new Set<string>() }: { scene: Scene; height?: number; compact?: boolean; thumb?: boolean; hidden?: Set<string> } = $props();

	let W = $state(0);
	let wrap = $state<HTMLDivElement>();
	const uid = 'lv' + Math.random().toString(36).slice(2, 8);
	const M = $derived(thumb ? { l: 6, r: 6, t: 6, b: 16 } : compact ? { l: 40, r: 44, t: 18, b: 22 } : { l: 70, r: 80, t: 34, b: 34 });

	const bounds = $derived.by(() => {
		if (scene.window) {
			const [x0, y0, x1, y1] = scene.window;
			return { x0, x1, y0, y1 };
		}
		let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
		for (const s of scene.shapes) for (const r of s.rings) for (const [x, y] of r) {
			if (x < x0) x0 = x;
			if (x > x1) x1 = x;
			if (y < y0) y0 = y;
			if (y > y1) y1 = y;
		}
		if (!thumb) for (const l of scene.labels) {
			const [x, y] = l.at;
			x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y);
		}
		if (!Number.isFinite(x0)) return { x0: 0, x1: 1, y0: 0, y1: 1 };
		if (x1 - x0 < 1e-9) [x0, x1] = [x0 - 0.5, x1 + 0.5];
		if (y1 - y0 < 1e-9) [y0, y1] = [y0 - 0.5, y1 + 0.5];
		return { x0, x1, y0, y1 };
	});
	const pw = $derived(Math.max(40, W - M.l - M.r));
	const ph = $derived(Math.max(30, height - M.t - M.b));
	const s0 = $derived(Math.min(pw / (bounds.x1 - bounds.x0), ph / (bounds.y1 - bounds.y0)));

	// view state: zoom factor and offset from the fitted centre, in um; survives a resize
	let k = $state(1);
	let shift = $state<[number, number]>([0, 0]);
	const sx = $derived(s0 * k);
	const cx = $derived((bounds.x0 + bounds.x1) / 2 + shift[0]);
	const cy = $derived((bounds.y0 + bounds.y1) / 2 + shift[1]);
	const px0 = $derived(M.l + pw / 2);
	const py0 = $derived(M.t + ph / 2);
	const X = (x: number) => px0 + (x - cx) * sx;
	const Y = (y: number) => py0 - (y - cy) * sx;
	const zoomed = $derived(k !== 1 || shift[0] !== 0 || shift[1] !== 0);
	const fit = () => ((k = 1), (shift = [0, 0]));

	function zoomAt(px: number, py: number, f: number) {
		const nk = Math.min(Math.max(k * f, 0.25), 2e5);
		const wx = cx + (px - px0) / sx, wy = cy - (py - py0) / sx;
		const ns = s0 * nk;
		shift = [wx - (px - px0) / ns - (bounds.x0 + bounds.x1) / 2, wy + (py - py0) / ns - (bounds.y0 + bounds.y1) / 2];
		k = nk;
	}
	let hover = $state<[number, number] | null>(null);
	let drag: { x: number; y: number; sh: [number, number] } | null = null;
	$effect(() => {
		const el = wrap;
		if (!el || thumb || compact) return;
		const onWheel = (e: WheelEvent) => {
			e.preventDefault();
			const r = el.getBoundingClientRect();
			zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0022)));
		};
		el.addEventListener('wheel', onWheel, { passive: false });
		return () => el.removeEventListener('wheel', onWheel);
	});
	function onDown(e: PointerEvent) {
		if (thumb || e.button !== 0) return;
		drag = { x: e.clientX, y: e.clientY, sh: shift };
		(e.currentTarget as Element).setPointerCapture(e.pointerId);
	}
	function onMove(e: PointerEvent) {
		if (thumb) return;
		const r = (e.currentTarget as Element).getBoundingClientRect();
		hover = [cx + (e.clientX - r.left - px0) / sx, cy - (e.clientY - r.top - py0) / sx];
		if (drag) shift = [drag.sh[0] - (e.clientX - drag.x) / sx, drag.sh[1] + (e.clientY - drag.y) / sx];
	}

	// Inset (true scale, both axes equal) in the top-right corner: template scenes only.
	const ins = $derived.by(() => {
		if (!scene.inset || W === 0 || thumb || zoomed) return null;
		const s = Math.min(ph * 0.62, pw * 0.34, compact ? 110 : 220);
		const bx = W - s - 4, by = M.t - (compact ? 14 : 22) + 14;
		const isx = s / (2 * scene.inset.half);
		const [icx, icy] = scene.inset.c;
		return { s, bx, by, isx, zoom: isx / sx, X: (x: number) => bx + s / 2 + (x - icx) * isx, Y: (y: number) => by + s / 2 - (y - icy) * isx };
	});

	const path = (rings: Pt[][], line: boolean, fx: (x: number) => number, fy: (y: number) => number) =>
		rings.map((r) => 'M' + r.map(([x, y]) => `${fx(x).toFixed(2)},${fy(y).toFixed(2)}`).join('L') + (line ? '' : 'Z')).join(' ');

	// bounding boxes once per scene, so a zoomed view skips what is outside it
	const boxes = $derived(
		scene.shapes.map((s) => {
			let a = Infinity, b = -Infinity, c = Infinity, d = -Infinity;
			for (const r of s.rings) for (const [x, y] of r) {
				if (x < a) a = x;
				if (x > b) b = x;
				if (y < c) c = y;
				if (y > d) d = y;
			}
			return [a, b, c, d];
		})
	);
	const drawn = $derived.by(() => {
		if (!W) return [];
		const xa = cx - (px0 + 8) / sx, xb = cx + (W - px0 + 8) / sx, ya = cy - (height - py0 + 8) / sx, yb = cy + (py0 + 8) / sx;
		return scene.shapes.flatMap((s, i) => {
			const [a, b, c, d] = boxes[i];
			if (b < xa || a > xb || d < ya || c > yb) return [];
			if (s.layer && hidden.has(s.layer)) return [];
			if (s.lod !== undefined && s.lod * sx < 1.1) return [];
			return [{ s, d: path(s.rings, !!s.line, X, Y) }];
		});
	});

	interface MR {
		m: Mark;
		lines: [number, number, number, number][];
		ticks: [number, number][];
		tx: number;
		ty: number;
		anchor: 'start' | 'middle' | 'end';
		v: boolean;
	}
	function markRender(m: Mark, fx: (x: number) => number, fy: (y: number) => number): MR {
		if (m.dir === 'h') {
			const x1 = fx(m.a), x2 = fx(m.b), yl = fy(m.pos) - m.px;
			const up = m.px >= 0;
			const e = up ? -3 : 3;
			const lines: MR['lines'] = [
				[x1, fy(m.from[0]), x1, yl + e],
				[x2, fy(m.from[1]), x2, yl + e],
				x2 - x1 < 10 ? [x1 - 8, yl, x2 + 8, yl] : [x1, yl, x2, yl]
			];
			return { m, lines, ticks: [[x1, yl], [x2, yl]], tx: (x1 + x2) / 2, ty: up ? yl - 4 : yl + 11, anchor: 'middle', v: false };
		}
		const y1 = fy(m.b), y2 = fy(m.a), xl = fx(m.pos) + m.px;
		const right = m.px >= 0;
		const e = right ? 3 : -3;
		const lines: MR['lines'] = [
			[fx(m.from[1]), y1, xl + e, y1],
			[fx(m.from[0]), y2, xl + e, y2],
			y2 - y1 < 10 ? [xl, y1 - 8, xl, y2 + 8] : [xl, y1, xl, y2]
		];
		return { m, lines, ticks: [[xl, y1], [xl, y2]], tx: right ? xl + 5 : xl - 5, ty: m.atEnd ? y1 + 10 : (y1 + y2) / 2 + 3.5, anchor: right ? 'start' : 'end', v: true };
	}
	/** Push apart vertical-mark labels that share a column. */
	function declutter(rs: MR[]): MR[] {
		const cols = new Map<string, MR[]>();
		for (const r of rs) if (r.v) {
			const key = Math.round(r.tx) + r.anchor;
			cols.set(key, [...(cols.get(key) ?? []), r]);
		}
		for (const col of cols.values()) {
			col.sort((a, b) => a.ty - b.ty);
			for (let i = 1; i < col.length; i++) if (col[i].ty - col[i - 1].ty < 12) col[i].ty = col[i - 1].ty + 12;
		}
		return rs;
	}
	/** Keep a text of n characters inside the svg (mono font, about 6.2 px per character). */
	function clampX(x: number, anchor: 'start' | 'middle' | 'end', n: number): number {
		const w = n * 6.2 + 8;
		const left = anchor === 'start' ? x : anchor === 'end' ? x - w : x - w / 2;
		const shift = left < 2 ? 2 - left : left + w > W - 2 ? W - 2 - (left + w) : 0;
		return x + shift;
	}
	const markText = (d: Dim) => d.label + (d.alts.length ? '*' : '') + (d.badge ? ' ' + d.badge : '');
	const show = (d: Dim | undefined) => !compact || !d || d.row !== null || !!d.free;
	/** a mark stays while its measured span is on screen: its text must not pile up at the edge when zoomed elsewhere */
	const onScreen = (m: Mark) => {
		const [a, b] = m.dir === 'h' ? [X(m.a), X(m.b)] : [Y(m.b), Y(m.a)];
		const c = m.dir === 'h' ? Y(m.pos) : X(m.pos);
		const lim = m.dir === 'h' ? W : height;
		const limC = m.dir === 'h' ? height : W;
		return b > 0 && a < lim && c > -40 && c < limC + 40;
	};
	const mainMarks = $derived(W && !thumb ? declutter(scene.marks.filter((m) => !m.inset && show(m.dim) && onScreen(m)).map((m) => markRender(m, X, Y))) : []);
	const insetMarks = $derived(ins && !thumb && !compact ? declutter(scene.marks.filter((m) => m.inset && show(m.dim)).map((m) => markRender(m, ins.X, ins.Y))) : []);
	const labels = $derived(thumb ? [] : scene.labels.filter((l: Label) => show(l.dim) && X(l.at[0]) > 0 && X(l.at[0]) < W && Y(l.at[1]) > 0 && Y(l.at[1]) < height));

	function nice(v: number): number {
		const p = Math.pow(10, Math.floor(Math.log10(v)));
		const f = v / p;
		return (f >= 5 ? 5 : f >= 2 ? 2 : 1) * p;
	}
	function fmtLen(um: number): string {
		if (um >= 1000) return +(um / 1000).toPrecision(3) + ' mm';
		if (um < 1) return +(um * 1000).toPrecision(3) + ' nm';
		return +um.toPrecision(3) + ' µm';
	}
	const barX = $derived(W ? nice((pw * 0.2) / sx) : 1);
	const fmtK = (v: number) => (v >= 100 ? Math.round(v).toString() : v.toPrecision(2));
	const fmtXY = (v: number) => (Math.abs(sx) > 100 ? v.toFixed(3) : sx > 5 ? v.toFixed(2) : v.toFixed(1));
</script>

<div class="scene" class:compact>
	{#if !thumb}
	<div class="bar">
		<span class="title">{scene.title}</span>
		{#if scene.partial}
			<span class="badge warn" data-tip="Both axes at the same scale. Dashed shapes are not in the source: a drafting assumption, stated on hover.">TRUE SCALE, DASHED ASSUMED</span>
		{:else}
			<span class="badge" data-tip="Both axes at the same scale">TRUE SCALE</span>
		{/if}
		<span class="grow"></span>
		{#if hover && !compact}<span class="xy num" data-tip="Pointer position, um">{fmtXY(hover[0])}, {fmtXY(hover[1])}</span>{/if}
		{#if zoomed}<button class="fit" onclick={fit} data-tip="Fit (or double-click the drawing)">fit ×{fmtK(k)}</button>{/if}
	</div>
	{/if}
	<div class="svgwrap" class:live={!thumb} bind:this={wrap} bind:clientWidth={W} style:height="{height}px" onpointerdown={onDown} onpointermove={onMove} onpointerup={() => (drag = null)} onpointerleave={() => (hover = null)} ondblclick={fit} role="presentation">
		{#if W}
			<svg width={W} {height} viewBox="0 0 {W} {height}" role="img" aria-label={scene.title}>
				<defs>
					<pattern id="{uid}-hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
						<line x1="0" y1="0" x2="0" y2="5" stroke="var(--ink)" stroke-width="1.2" stroke-opacity="0.55" />
					</pattern>
					{#if ins}<clipPath id="{uid}-clip"><rect x={ins.bx} y={ins.by} width={ins.s} height={ins.s} /></clipPath>{/if}
				</defs>
				{#each drawn as { s, d }}
					<path
						{d}
						class="shape"
						class:sch={s.schematic}
						class:line={s.line}
						fill-rule="evenodd"
						fill={s.line ? 'none' : s.hatch ? `url(#${uid}-hatch)` : `var(--m-${s.mat})`}
						fill-opacity={s.line ? 0 : s.hatch ? 1 : (s.alpha ?? 0.85) * (s.schematic ? 0.55 : 1)}
						stroke={s.line ? 'var(--ink-2)' : s.hatch ? 'none' : `var(--m-${s.mat})`}
						data-tip={thumb ? undefined : s.tip}
					/>
				{/each}
				{#snippet marks(rs: MR[])}
					{#each rs as r}
						<g class="mark" class:nr={!r.m.dim.row && !r.m.dim.free} class:meas={r.m.dim.basis === 'measured'} data-tip={r.m.dim.tip}>
							{#each r.lines as [x1, y1, x2, y2]}<line {x1} {y1} {x2} {y2} />{/each}
							{#each r.ticks as [x, y]}<line class="tick" x1={x - 3} y1={y + 3} x2={x + 3} y2={y - 3} />{/each}
							<text x={clampX(r.tx, r.anchor, markText(r.m.dim).length)} y={Math.min(Math.max(r.ty, 10), height - 3)} text-anchor={r.anchor}>{r.m.dim.label}{r.m.dim.alts.length ? '*' : ''}{#if r.m.dim.badge}<tspan class="bd" dx="2" dy="-3">{r.m.dim.badge}</tspan>{/if}</text>
						</g>
					{/each}
				{/snippet}
				{@render marks(mainMarks)}
				{#each labels as l}
					<text class="lbl" class:muted={l.muted} class:nr={l.dim && !l.dim.row && !l.dim.free} class:meas={l.dim?.basis === 'measured'} x={clampX(X(l.at[0]) + (l.dx ?? 0), l.anchor, l.text.length + 3)} y={Math.min(Math.max(Y(l.at[1]) + (l.dy ?? 0), 10), height - 3)} text-anchor={l.anchor} data-tip={l.dim?.tip ?? l.tip ?? ''}>{l.text}{l.dim?.alts.length ? '*' : ''}{#if l.dim?.badge}<tspan class="bd" dx="2" dy="-3">{l.dim.badge}</tspan>{/if}</text>
				{/each}
				{#if ins && scene.inset}
					{@const [icx, icy] = scene.inset.c}
					{@const h = scene.inset.half}
					<rect class="inset-src" x={X(icx - h)} y={Y(icy + h)} width={Math.max(2, 2 * h * sx)} height={Math.max(2, 2 * h * sx)} />
					<rect class="inset-box" x={ins.bx} y={ins.by} width={ins.s} height={ins.s} />
					<g clip-path="url(#{uid}-clip)">
						{#each scene.shapes as s}
							<path d={path(s.rings, !!s.line, ins.X, ins.Y)} class="shape" class:sch={s.schematic} fill-rule="evenodd" fill={s.line ? 'none' : `var(--m-${s.mat})`} fill-opacity={(s.alpha ?? 0.85) * (s.schematic ? 0.55 : 1)} stroke={`var(--m-${s.mat})`} data-tip={s.tip} />
						{/each}
					</g>
					{@render marks(insetMarks)}
					<text class="lbl muted" x={ins.bx + 4} y={ins.by + 11} data-tip="Magnified view of the coupling region, both axes at the same scale">inset ×{fmtK(ins.zoom)}</text>
				{/if}
				{#if !scene.schematic}
					{@const bx = 8}
					{@const by = height - 8}
					<g class="ruler" data-tip="Scale bar (a ruler, not a data value)">
						<line x1={bx} y1={by} x2={bx + barX * sx} y2={by} />
						<line x1={bx} y1={by - 3} x2={bx} y2={by + 1} /><line x1={bx + barX * sx} y1={by - 3} x2={bx + barX * sx} y2={by + 1} />
						<text x={bx + barX * sx + 4} y={by + 3}>{fmtLen(barX)}</text>
					</g>
				{/if}
			</svg>
		{/if}
	</div>
	{#if !compact && !thumb && scene.notes.length}
		<ul class="notes">{#each scene.notes as n}<li>{n}</li>{/each}</ul>
	{/if}
</div>

<style>
	.scene { min-width: 0; }
	.bar { display: flex; align-items: center; gap: 6px; height: 22px; font-size: 11px; }
	.compact .bar { height: 18px; font-size: 10px; }
	.title { color: var(--ink-2); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.grow { flex: 1; }
	.badge { font: 600 9px/14px var(--mono); padding: 0 4px; border: 1px solid var(--line); color: var(--ink-3); letter-spacing: 0.04em; white-space: nowrap; }
	.badge.warn { color: var(--warn); border-color: var(--warn); }
	.xy { color: var(--ink-3); font: 10px var(--mono); white-space: nowrap; }
	.fit { height: 18px; padding: 0 6px; font-size: 10px; border-radius: 0; background: transparent; color: var(--ink-2); border: 1px solid var(--line); cursor: pointer; white-space: nowrap; }
	.svgwrap { position: relative; width: 100%; background: var(--bg); border: 1px solid var(--grid); overflow: hidden; }
	.svgwrap.live { cursor: grab; touch-action: none; }
	.svgwrap.live:active { cursor: grabbing; }
	svg { display: block; font: 10px var(--mono); user-select: none; }
	.compact svg { font-size: 9px; }
	.shape { stroke-width: 0.8; }
	.shape.sch { stroke-dasharray: 4 3; stroke-width: 1; }
	.shape.line { stroke-width: 1; }
	.shape.line.sch { stroke-dasharray: 2 3; }
	.mark line { stroke: var(--lv-dim); stroke-width: 0.7; }
	.mark .tick { stroke-width: 1.1; }
	.mark text, .lbl { fill: var(--ink); paint-order: stroke; stroke: var(--bg); stroke-width: 3px; stroke-linejoin: miter; }
	.mark.meas text, .lbl.meas { fill: var(--accent); }
	.mark.nr line { stroke: var(--warn); stroke-dasharray: 3 2; }
	.mark.nr text, .lbl.nr { fill: var(--warn); font-style: italic; }
	.lbl.muted { fill: var(--ink-3); }
	.bd { font-size: 7.5px; font-weight: 700; fill: var(--ink-3); }
	.meas .bd { fill: var(--accent); }
	.inset-box { fill: var(--bg); stroke: var(--line); }
	.inset-src { fill: none; stroke: var(--ink-3); stroke-dasharray: 2 2; }
	.ruler line { stroke: var(--ink-2); stroke-width: 1.2; }
	.ruler text { fill: var(--ink-2); font-size: 9px; }
	.notes { margin: 3px 0 0; padding: 0 0 0 14px; font-size: 10px; color: var(--ink-3); }
</style>
