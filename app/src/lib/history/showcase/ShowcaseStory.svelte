<script lang="ts">
	// Showcase story runtime (DevLog-017 section 2). A tall track holds a sticky stage; the scroll position of the track
	// inside the page's scroll container gives p in [0, 1], which drives the scene module's pure frame(p), the chapter
	// keywords, the plot assembler and part introduction. Contract for scene modules: ./types.ts.
	import { onMount, tick } from 'svelte';
	import type * as THREE_NS from 'three';
	import { getJson, staticUrl } from '../../paths';
	import { ui } from '../../state.svelte';
	import { SHOWCASES } from '../showcases';
	import PartPanel from './PartPanel.svelte';
	import PlotAssembler from './PlotAssembler.svelte';
	import {
		chapterIndexAt,
		chapterIndexBefore,
		chapterTarget,
		clamp01,
		defaultAssembledAt,
		keywordStates,
		partIntro,
		plotRange,
		scrollDeltaFor,
		scrollProgress,
		seg
	} from './progress';
	import Rich from './Rich.svelte';
	import { plotProgressIn, logOf, plainMarkup, plotLabel, toggleLog, withAlternates, type LogState } from './plot';
	import { claim, loadOrbit, shared, unclaim, type Claimant } from './three';
	import type { Trace } from './trace';
	import TraceView from './TraceView.svelte';
	import type { Part, PickInfo, ShowcaseHandle, ShowcaseSpec } from './types';
	import { thumbP, partTipLines, pickDetail, essentialDimText, labelLeft, orbitLimits, plainKeyword, stepTipLines, playAt, playDuration, playPlan, type PlayLeg } from './progress';

	let {
		id,
		year,
		dri,
		onmilestone,
		onfail
	}: {
		id: string;
		year: number | null;
		dri: string;
		/** open the milestone's detail panel */
		onmilestone: (el: HTMLElement) => void;
		/** the story cannot show (no spec, no module, build error) */
		onfail: (id: string) => void;
	} = $props();

	let spec = $state.raw<ShowcaseSpec | null>(null);
	let trace = $state.raw<Trace | null>(null);
	let track: HTMLElement | undefined = $state();
	let pane: HTMLDivElement | undefined = $state();
	let svgEl: SVGSVGElement | undefined = $state();
	let scroller: HTMLElement | null = null;
	let viewH = $state(700);
	let paneW = $state(0);
	let paneH = $state(0);
	let p = $state(0);
	let k = $state(0);
	let free = $state(false);
	let hoverId = $state<string | null>(null);
	let pinId = $state<string | null>(null);
	let panel = $state<'part' | 'story' | null>(null);
	let tipBox = $state<{ x: number; y: number; lines: string[] } | null>(null);
	let labels = $state<{ id: string; x: number; y: number; name: string; dim: string }[]>([]);
	let poster = $state('');
	let ready = $state(false);
	let holding = $state(false);
	let reduced = $state(false);
	let coarse = $state(false);
	let modAssembledAt = $state<number | undefined>(undefined);
	let hasExplode = $state(false);

	let handle: ShowcaseHandle | null = null;
	let three: { THREE: typeof THREE_NS; scene: THREE_NS.Scene; camera: THREE_NS.PerspectiveCamera } | null = null;
	let renderer: THREE_NS.WebGLRenderer | null = null;
	let controls: InstanceType<Awaited<ReturnType<typeof loadOrbit>>> | null = null;
	let pose: { pos: THREE_NS.Vector3; target: THREE_NS.Vector3 } | null = null;
	let started = false;
	let disposed = false;

	const chapters = $derived(spec?.chapters ?? []);
	const parts = $derived(spec?.parts ?? []);
	const partById = $derived(new Map(parts.map((q) => [q.id, q])));
	const ci = $derived(chapterIndexAt(chapters, p));
	const cb = $derived(chapterIndexBefore(chapters, p));
	const kws = $derived(keywordStates(chapters, p, 26));
	const assembledAt = $derived(modAssembledAt ?? defaultAssembledAt(chapters));
	const assembled = $derived(ready && p >= assembledAt);
	const canOrbit = $derived(assembled && spec?.renderer === '3d');
	const kEff = $derived(assembled ? k : 0);
	const on = $derived([...new Set([hoverId, pinId].filter((x): x is string => !!x))]);
	const pending = $derived(new Set(parts.filter((q) => p < partIntro(chapters, q.id)).map((q) => q.id)));
	const heightVh = $derived(reduced ? 1 : Math.max(2, spec?.height ?? 5));
	const drawing = $derived(spec?.drawings?.find((d) => d.trace || d.image) ?? null);
	const plots = $derived(
		(spec?.plots ?? []).flatMap((pl) => {
			if (!pl || typeof pl.id !== 'string' || pl.alt_of || (pl.kind !== 'levels' && !Array.isArray(pl.series))) return [];
			const r = spec ? plotRange(spec, pl.id) : null;
			if (!r) return [];
			const idx = chapters.findIndex((c) => c.p[0] === r[0] && c.p[1] === r[1]);
			return [{ pl, r, idx }];
		})
	);
	const plotNow = $derived(
		plots
			.map((it) => ({ ...it, o: it.idx >= 0 ? kws[it.idx].o : seg(p, it.r[0], it.r[0] + 0.05), dy: it.idx >= 0 ? kws[it.idx].dy : 0, rr: plotProgressIn(it.r, p) }))
			.find((it) => it.o > 0.01) ?? null
	);
	// alternates of the plot on screen (main first) and the one chosen per main plot id; log choices per plot id
	let altSel = $state<Record<string, string>>({});
	let logState = $state<LogState>({});
	const alts = $derived(plotNow && spec?.plots ? withAlternates(spec.plots, plotNow.pl.id).filter((q) => q.kind === 'levels' || Array.isArray(q.series)) : []);
	const plotShown = $derived(plotNow ? (alts.find((q) => q.id === altSel[plotNow.pl.id]) ?? plotNow.pl) : null);
	// handle.plot(id): tell the module which plot is on screen (null = none) when it changes, and once when ready
	let lastPlotId: string | null | undefined = undefined;
	$effect(() => {
		const id = plotShown?.id ?? null;
		if (!ready || !handle?.plot || id === lastPlotId) return;
		lastPlotId = id;
		handle.plot(id);
		requestDraw();
	});
	const step = $derived.by(() => {
		const c = chapters[cb];
		if (!c || !spec?.process) return null;
		return spec.process.find((s) => s.id === (c.process ?? c.id)) ?? null;
	});
	const selPart = $derived(pinId ? (partById.get(pinId) ?? null) : null);

	// ------------------------------------------------------------------------------------------- scroll -> p
	function findScroller(el: HTMLElement): HTMLElement | null {
		for (let n = el.parentElement; n; n = n.parentElement) {
			const oy = getComputedStyle(n).overflowY;
			if ((oy === 'auto' || oy === 'scroll') && n.scrollHeight > n.clientHeight + 1) return n;
		}
		return null;
	}
	function measure(): { secTop: number; secH: number; viewTop: number; viewH: number } | null {
		if (!track) return null;
		const r = track.getBoundingClientRect();
		const v = scroller ? scroller.getBoundingClientRect() : { top: 0, height: innerHeight };
		const vh = scroller ? scroller.clientHeight : innerHeight;
		return { secTop: r.top, secH: r.height, viewTop: v.top + (scroller?.clientTop ?? 0), viewH: vh };
	}
	let raf = 0;
	function onScroll() {
		if (raf) return;
		raf = requestAnimationFrame(() => {
			raf = 0;
			// Play sets p itself in the same frame as its scroll; the scroll it causes is not a new input
			if (reduced || playing) return;
			const m = measure();
			if (m) setP(scrollProgress(m.secTop, m.secH, m.viewTop, m.viewH));
		});
	}
	function setP(v: number) {
		const n = clamp01(v);
		if (n === p) return;
		p = n;
	}
	/** Jump to progress v: scroll the container (smooth) or, in reduced motion, set p directly. */
	function goTo(v: number, smooth = true) {
		if (reduced) {
			setP(v);
			return stageIntoView();
		}
		if (!scroller) return setP(v);
		const m = measure();
		if (!m) return;
		scroller.scrollBy({ top: scrollDeltaFor(v, m.secTop, m.secH, m.viewTop, m.viewH), behavior: smooth ? 'smooth' : 'auto' });
	}
	/** Reduced motion (stage not sticky, one view tall): bring the whole stage into the scroll container's view, below
	 *  the app header and the history toolbar (both sit outside the container), instantly and only when it is cut off. */
	function stageIntoView() {
		const m = measure();
		if (!m) return;
		const top = m.secTop - m.viewTop;
		const bottom = top + Math.min(m.secH, m.viewH);
		if (top >= -1 && bottom <= m.viewH + 1) return;
		if (scroller) scroller.scrollBy({ top, behavior: 'auto' });
		else window.scrollBy({ top, behavior: 'auto' });
	}
	let sro: ResizeObserver | null = null;
	/** The scroll container changed height (menu bar hidden / shown, address bar, rotation): the stage and the track
	 *  follow it; the story in view keeps its p (its scroll position is re-derived), Play re-reads its geometry. */
	function onScrollerResize() {
		if (!scroller) return;
		const h = scroller.clientHeight;
		if (h === viewH) return;
		const keep = p;
		const inView = !reduced && share > 0.5;
		viewH = h;
		tick().then(() => {
			if (!scroller || disposed) return;
			if (inView && !playing) {
				const m = measure();
				if (m) scroller.scrollTop += scrollDeltaFor(keep, m.secTop, m.secH, m.viewTop, m.viewH);
			}
			if (playing) playGeom();
		});
	}
	let near: IntersectionObserver | null = null;
	let vis: IntersectionObserver | null = null;
	let share = 0;
	let share0 = $state(false);
	/** (Re)attach to the scroll container: `.scroll` on desktop, the whole page on phones (it changes at the breakpoint). */
	function refreshScroller() {
		if (!track) return;
		const s = findScroller(track);
		if (s !== scroller || !near) {
			scroller?.removeEventListener('scroll', onScroll);
			if (!scroller) window.removeEventListener('scroll', onScroll);
			scroller = s;
			(scroller ?? window).addEventListener('scroll', onScroll, { passive: true });
			near?.disconnect();
			vis?.disconnect();
			near = new IntersectionObserver((es) => es.some((e) => e.isIntersecting) && start(), { root: scroller, rootMargin: '150% 0px' });
			vis = new IntersectionObserver(
				(es) => {
					for (const e of es) share = e.isIntersecting ? e.intersectionRect.height / Math.max(1, e.rootBounds?.height ?? innerHeight) : 0;
					share0 = share <= 0;
					if (three) claim(claimant, share);
				},
				{ root: scroller, threshold: [0, 0.05, 0.15, 0.3, 0.5, 0.7, 0.9, 1] }
			);
			near.observe(track);
			vis.observe(track);
			sro?.disconnect();
			if (scroller) {
				sro = new ResizeObserver(onScrollerResize);
				sro.observe(scroller);
			}
		}
		viewH = scroller ? scroller.clientHeight : innerHeight;
		onScroll();
	}

	// ------------------------------------------------------------------------------------------- model
	function draw() {
		if (!handle) return;
		drawnKey = drawKey();
		handle.explode?.(kEff);
		handle.frame(p);
		if (three && free && pose) {
			three.camera.position.copy(pose.pos);
			three.camera.lookAt(pose.target);
		}
		if (three && renderer && holding) {
			// optional per-story strength of the shared room environment (three r186: material.envMapIntensity does not
			// scale scene.environment); scene-owned, so it never leaks into another story's renders
			if (typeof handle.environmentIntensity === 'number') three.scene.environmentIntensity = handle.environmentIntensity;
			renderer.render(three.scene, three.camera);
		}
		placeLabels();
	}
	function placeLabels() {
		if (!handle?.anchor || !spec) {
			if (labels.length) labels = [];
			return;
		}
		const c = chapters[cb];
		const ids = (Array.isArray(c?.labels) ? c.labels : (c?.parts ?? [])).filter((q) => partById.get(q)?.essential);
		const out: typeof labels = [];
		for (const q of ids) {
			const a = handle.anchor(q);
			const part = partById.get(q);
			if (!a || !part) continue;
			out.push({ id: q, x: Math.round(a[0] * 2) / 2, y: Math.round(a[1] * 2) / 2, name: part.name, dim: dimText(part) });
		}
		// unchanged labels keep the same array: no DOM work on frames where nothing moved
		if (out.length === labels.length && out.every((l, i) => l.id === labels[i].id && l.x === labels[i].x && l.y === labels[i].y)) return;
		labels = out;
	}
	/** all essential dims of a part: "10 mm x 20 mm" when the units agree, else comma separated */
	const dimText = (part: Part): string => essentialDimText(part.dims);
	/** measured label widths (canvas labels flip left or clamp to stay inside the pane) */
	let labW = $state<Record<string, number>>({});
	let drawQueued = false;
	let drawForce = false;
	let drawnKey = '';
	const drawKey = () => `${p}|${kEff}|${free}`;
	/** Draw on the next frame; unforced requests (p, explode, orbit changes) are dropped when that state was already
	 *  drawn this frame (Play draws synchronously with its scroll). */
	function requestDraw(force = true) {
		drawForce ||= force;
		if (drawQueued) return;
		drawQueued = true;
		requestAnimationFrame(() => {
			drawQueued = false;
			const f = drawForce;
			drawForce = false;
			if (disposed || (!f && drawnKey === drawKey())) return;
			draw();
		});
	}
	$effect(() => {
		void p;
		void kEff;
		void free;
		if (ready) requestDraw(false);
	});
	$effect(() => {
		const ids = on;
		if (!ready || !handle) return;
		handle.highlight(ids);
		requestDraw();
	});
	$effect(() => {
		const t = ui.theme;
		if (!ready || !handle) return;
		handle.theme?.(t);
		requestDraw();
	});
	$effect(() => {
		if (!canOrbit && free) free = false;
		if (controls) {
			controls.enabled = canOrbit && (free || !coarse);
			controls.enableZoom = free;
		}
		if (renderer && holding) renderer.domElement.style.touchAction = free ? 'none' : 'pan-y';
	});

	function resize() {
		if (!pane) return;
		paneW = pane.clientWidth;
		paneH = pane.clientHeight;
		if (!handle || !paneW || !paneH) return;
		if (three) {
			three.camera.aspect = paneW / paneH;
			three.camera.updateProjectionMatrix();
			if (renderer && holding) renderer.setSize(paneW, paneH);
		}
		if (svgEl && !svgEl.dataset.fixedViewBox) svgEl.setAttribute('viewBox', `0 0 ${paneW} ${paneH}`);
		handle.resize(paneW, paneH);
		draw();
	}

	// ------------------------------------------------------------------------------------------- shared renderer
	const claimant: Claimant = {
		grant(r) {
			renderer = r;
			holding = true;
			if (!pane) return;
			pane.prepend(r.domElement);
			r.setSize(paneW || 1, paneH || 1);
			void attachOrbit(r);
			draw();
			poster = '';
		},
		revoke(moving) {
			if (moving && renderer && three && pane?.contains(renderer.domElement)) {
				if (typeof handle?.environmentIntensity === 'number') three.scene.environmentIntensity = handle.environmentIntensity;
				renderer.render(three.scene, three.camera);
				try {
					poster = renderer.domElement.toDataURL('image/png');
				} catch {
					poster = '';
				}
			}
			controls?.dispose();
			controls = null;
			holding = false;
			renderer = null;
		}
	};
	async function attachOrbit(r: THREE_NS.WebGLRenderer) {
		const Orbit = await loadOrbit();
		if (!three || renderer !== r || disposed) return;
		controls?.dispose();
		const c = new Orbit(three.camera, r.domElement);
		c.enableDamping = false;
		c.screenSpacePanning = true;
		c.enabled = canOrbit && (free || !coarse);
		c.enableZoom = free;
		const lim = orbitLimits(handle?.orbit ?? spec?.orbit);
		c.minPolarAngle = lim.polar[0];
		c.maxPolarAngle = lim.polar[1];
		if (lim.azimuth) [c.minAzimuthAngle, c.maxAzimuthAngle] = lim.azimuth;
		if (lim.distance) [c.minDistance, c.maxDistance] = lim.distance;
		r.domElement.style.touchAction = free ? 'none' : 'pan-y';
		c.addEventListener('start', () => {
			if (!three || free) return;
			const t = handle?.target?.();
			if (t) c.target.set(t[0], t[1], t[2]);
			else {
				const box = new three.THREE.Box3().setFromObject(three.scene);
				if (!box.isEmpty()) box.getCenter(c.target);
			}
		});
		c.addEventListener('change', () => {
			if (!three) return;
			free = true;
			pose = { pos: three.camera.position.clone(), target: c.target.clone() };
			requestDraw();
		});
		controls = c;
	}
	/** Phones during Play: render at most `cap` device pixels per CSS pixel (the shared renderer), restore on pause. */
	function setRenderCap(cap: number) {
		if (!renderer || !holding) return;
		const pr = Math.min(window.devicePixelRatio || 1, cap);
		if (renderer.getPixelRatio() === pr) return;
		renderer.setPixelRatio(pr);
		renderer.setSize(paneW || 1, paneH || 1);
		requestDraw();
	}
	function resetView() {
		free = false;
		pose = null;
		requestDraw();
	}

	// ------------------------------------------------------------------------------------------- loading
	async function start() {
		if (started) return;
		started = true;
		try {
			const load = SHOWCASES[id];
			if (!load) throw new Error(`no scene module for ${id}`);
			const [s, mod] = await Promise.all([getJson<ShowcaseSpec>(`data/showcases/${id}.json`), load()]);
			if (disposed) return;
			spec = s;
			const d = s.drawings?.find((x) => x.trace);
			if (d?.trace) getJson<Trace>(`data/showcases/traces/${d.trace}`).then((t) => (trace = t), () => (trace = null));
			await tick();
			resize();
			const base = { spec: s, width: paneW || 1, height: paneH || 1, theme: ui.theme, reduced };
			if (mod.renderer === '3d') {
				const sh = await shared();
				if (disposed) return;
				const scene = new sh.THREE.Scene();
				scene.environment = sh.env;
				const camera = new sh.THREE.PerspectiveCamera(30, (paneW || 1) / (paneH || 1), 0.1, 10000);
				three = { THREE: sh.THREE, scene, camera };
				handle = await mod.build({ ...base, kind: '3d', THREE: sh.THREE, scene, camera });
			} else {
				if (!svgEl) throw new Error('no svg root');
				handle = await mod.build({ ...base, kind: '2.5d', svg: svgEl });
			}
			if (disposed) return handle?.dispose();
			modAssembledAt = handle.assembledAt;
			hasExplode = typeof handle.explode === 'function';
			ready = true;
			if (reduced) p = chapters.length ? chapterTarget(chapters[0]) : 1;
			resize();
			handle.highlight(on);
			if (three) claim(claimant, share);
		} catch (e) {
			console.warn(`showcase ${id}:`, e);
			if (!disposed) onfail(id);
		}
	}

	onMount(() => {
		const mq = matchMedia('(prefers-reduced-motion: reduce)');
		reduced = mq.matches;
		const onMq = () => {
			reduced = mq.matches;
			if (reduced && chapters.length) p = chapterTarget(chapters[Math.max(0, chapterIndexBefore(chapters, p))]);
			tick().then(refreshScroller);
		};
		mq.addEventListener('change', onMq);
		coarse = matchMedia('(pointer: coarse)').matches;
		refreshScroller();
		const ro = new ResizeObserver(() => {
			resize();
			refreshScroller();
		});
		if (pane) ro.observe(pane);
		const onWin = () => refreshScroller();
		addEventListener('resize', onWin);
		window.visualViewport?.addEventListener('resize', onWin);
		return () => {
			disposed = true;
			pause();
			mq.removeEventListener('change', onMq);
			near?.disconnect();
			vis?.disconnect();
			ro.disconnect();
			removeEventListener('resize', onWin);
			window.visualViewport?.removeEventListener('resize', onWin);
			sro?.disconnect();
			(scroller ?? window).removeEventListener('scroll', onScroll);
			if (raf) cancelAnimationFrame(raf);
			unclaim(claimant);
			if (holding) claimant.revoke(false);
			handle?.dispose();
			handle = null;
			three = null;
		};
	});

	// ------------------------------------------------------------------------------------------- parts linking
	const partTip = (q: Part, extra: string[] = []): string[] => partTipLines(q, extra);
	function hover(idv: string | null, e?: { clientX: number; clientY: number }) {
		hoverId = idv;
		const q = idv ? partById.get(idv) : null;
		tipBox = q && e ? { x: e.clientX, y: e.clientY, lines: partTip(q) } : null;
	}
	/** hover from the model: a part id, or a PickInfo (non-part elements get their own tooltip and are highlighted) */
	function hoverPick(hit: string | PickInfo | null, e: { clientX: number; clientY: number }) {
		if (!hit) return hover(null);
		const id = typeof hit === 'string' ? hit : hit.id;
		const det = pickDetail(hit);
		const part = partById.get(id);
		if (part) {
			// a spec part: the usual part tooltip, plus the module's detail lines (per-part caveats) under the role
			hover(id, e);
			if (det.length) tipBox = { x: e.clientX, y: e.clientY, lines: partTip(part, det) };
			return;
		}
		if (typeof hit === 'string') return hover(null);
		hoverId = id;
		tipBox = { x: e.clientX, y: e.clientY, lines: [hit.label, ...det].filter(Boolean) };
	}
	const pickId = (hit: string | PickInfo | null): string | null => (hit == null ? null : typeof hit === 'string' ? hit : hit.id);
	function pin(idv: string | null) {
		pinId = idv;
		panel = idv ? 'part' : null;
	}
	function togglePin(idv: string) {
		pin(pinId === idv && panel === 'part' ? null : idv);
	}
	function tour(d: number) {
		if (!parts.length) return;
		const i = pinId ? parts.findIndex((q) => q.id === pinId) : -1;
		const n = i < 0 ? (d > 0 ? 0 : parts.length - 1) : (i + d + parts.length) % parts.length;
		pin(parts[n].id);
	}
	function plotTip(lines: string[] | null, x = 0, y = 0) {
		tipBox = lines ? { x, y, lines } : null;
	}

	let down: { x: number; y: number } | null = null;
	let pickQueued = false;
	function paneXY(e: PointerEvent): [number, number] {
		const r = pane!.getBoundingClientRect();
		return [e.clientX - r.left, e.clientY - r.top];
	}
	// overlays with their own pointer handling (plot) are not part of the model
	const overlay = (e: Event) => !!(e.target as Element | null)?.closest?.('.plotbox, .ctrl, .lab, .step');
	function onPaneMove(e: PointerEvent) {
		if (!handle || !ready || e.buttons) return;
		if (overlay(e)) {
			// over the plot: the plot owns the tooltip (point / bar values); only the model hover is dropped
			if ((e.target as Element | null)?.closest?.('.plotbox')) {
				if (hoverId) hoverId = null;
				return;
			}
			// over a control or chip: drop the model hover and its tooltip
			if (hoverId || tipBox) hover(null);
			return;
		}
		if (pickQueued) return;
		pickQueued = true;
		const ev = { clientX: e.clientX, clientY: e.clientY };
		const [x, y] = paneXY(e);
		requestAnimationFrame(() => {
			pickQueued = false;
			if (!handle) return;
			hoverPick(handle.pick(x, y), ev);
		});
	}
	function onPaneDown(e: PointerEvent) {
		down = overlay(e) ? null : { x: e.clientX, y: e.clientY };
	}
	function onPaneUp(e: PointerEvent) {
		if (!down || !handle) return;
		const moved = Math.hypot(e.clientX - down.x, e.clientY - down.y);
		down = null;
		if (moved > 5) return;
		const [x, y] = paneXY(e);
		const hit = pickId(handle.pick(x, y));
		if (hit && partById.has(hit)) togglePin(hit);
	}

	function stageVisible(): boolean {
		if (!track) return false;
		const m = measure();
		if (!m) return false;
		const top = Math.max(m.secTop, m.viewTop);
		const bot = Math.min(m.secTop + m.secH, m.viewTop + m.viewH);
		return bot - top > 0.6 * m.viewH;
	}
	// ------------------------------------------------------------------------------------------- autoplay
	// Play drives the story by scrolling the page's scroll container (reduced motion: sets p chapter by chapter), so
	// scroll, p, scrub bar and chapter buttons stay in sync and frame(p) stays a pure function of p. Any user input on
	// the page pauses. Pacing constants: PLAY in progress.ts.
	let playing = $state(false);
	let playRaf = 0;
	let playStart = 0;
	let plan: PlayLeg[] = [];
	let lastPlayP = -1;
	let article: HTMLElement | undefined = $state();
	const plotIdx = $derived(new Set(plots.map((it) => it.idx).filter((i) => i >= 0)));
	// Play geometry: scrollTop of p = 0 and the scroll run of the track, cached so frames write scrollTop without reading
	// layout; recomputed when the scroll container resizes (menu bar hidden / shown, rotation)
	let playOffset = 0;
	let playRun = 0;
	let expectTop = -1;
	function playGeom(): boolean {
		const m = measure();
		if (!m || !scroller) return false;
		playOffset = scroller.scrollTop + (m.secTop - m.viewTop);
		playRun = Math.max(0, m.secH - m.viewH);
		return true;
	}
	/** One Play frame: write scrollTop, set p and draw in the same frame (no scroll-event round trip). */
	function playTo(v: number) {
		if (reduced || !scroller) return goTo(v, false);
		scroller.scrollTop = playOffset + v * playRun;
		expectTop = scroller.scrollTop;
		setP(v);
		if (ready) draw();
	}
	function play() {
		if (!ready || !chapters.length) return;
		const p0 = p >= 0.999 ? 0 : p;
		plan = playPlan(chapters, p0, (i) => plotIdx.has(i), reduced);
		if (!reduced) playGeom();
		expectTop = -1;
		playTo(p0);
		lastPlayP = p0;
		playing = true;
		if (coarse) setRenderCap(1.5);
		playStart = performance.now();
		addEventListener('wheel', interrupt, { capture: true, passive: true });
		addEventListener('touchstart', interrupt, { capture: true, passive: true });
		addEventListener('pointerdown', interrupt, { capture: true });
		addEventListener('keydown', interruptKey, { capture: true });
		document.addEventListener('visibilitychange', onHidden);
		stepPlay();
	}
	function stepPlay() {
		playRaf = requestAnimationFrame((now) => {
			if (!playing || disposed) return;
			const t = now - playStart;
			// the user (or leftover touch momentum) moved the page since our last write: they take over
			if (!reduced && scroller && expectTop >= 0 && Math.abs(scroller.scrollTop - expectTop) > 3) return pause();
			const v = playAt(plan, t);
			if (Math.abs(v - lastPlayP) > 1e-5) {
				lastPlayP = v;
				playTo(v);
			}
			if (t >= playDuration(plan)) return pause();
			stepPlay();
		});
	}
	function pause() {
		if (!playing) return;
		playing = false;
		expectTop = -1;
		if (coarse) setRenderCap(2);
		cancelAnimationFrame(playRaf);
		removeEventListener('wheel', interrupt, { capture: true });
		removeEventListener('touchstart', interrupt, { capture: true });
		removeEventListener('pointerdown', interrupt, { capture: true });
		removeEventListener('keydown', interruptKey, { capture: true });
		document.removeEventListener('visibilitychange', onHidden);
	}
	function togglePlay() {
		if (playing) pause();
		else play();
	}
	function interrupt(e: Event) {
		if ((e.target as Element | null)?.closest?.('.playbtn, .pinbtn, .chrome-handle, .chrome-hot')) return;
		pause();
	}
	function interruptKey(e: KeyboardEvent) {
		if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'PageUp', 'PageDown', 'Home', 'End'].includes(e.key)) pause();
	}
	function onHidden() {
		if (document.hidden) pause();
	}
	$effect(() => {
		// the story left the viewport
		if (playing && share0) pause();
	});
	/** Space toggles Play while the story has focus (or nothing has focus and its stage fills the view). */
	function spaceToggles(e: KeyboardEvent): boolean {
		if (e.key !== ' ' || e.metaKey || e.ctrlKey || e.altKey) return false;
		const a = document.activeElement;
		if (a && a !== document.body && (a.closest('button, a, input, textarea, select, [contenteditable]') || !article?.contains(a))) return false;
		return !!article && (article.contains(a) || stageVisible());
	}

	function onKey(e: KeyboardEvent) {
		if (!ready) return;
		const t = e.target as HTMLElement | null;
		if (t?.closest('input, textarea, select, [contenteditable]')) return;
		if (spaceToggles(e)) {
			e.preventDefault();
			togglePlay();
			return;
		}
		if (e.key === 'Escape' && (panel || pinId)) {
			pin(null);
			panel = null;
			return;
		}
		if ((e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') || e.metaKey || e.ctrlKey || e.altKey) return;
		if (!stageVisible()) return;
		e.preventDefault();
		tour(e.key === 'ArrowRight' ? 1 : -1);
	}

	/** keyword runs; one phrase wrapped in *asterisks* in the spec is the amber italic emphasis (D997) */
	function emphasis(t: string): { t: string; em: boolean }[] {
		const m = /^(.*?)\*([^*]+)\*(.*)$/s.exec(t);
		return m ? [{ t: m[1], em: false }, { t: m[2], em: true }, { t: m[3].replace(/\*/g, ''), em: false }].filter((r) => r.t) : [{ t, em: false }];
	}
	const kwSize = $derived(paneW < 520 ? 34 : paneW < 900 ? 52 : 68);
</script>

<svelte:window onkeydown={onKey} />

<article class="story" id="story-{id}" class:reduced bind:this={article} data-thumb-p={spec ? thumbP(spec) : null}>
	<header class="shead">
		<div class="tl">
			<h3><Rich text={spec?.title ?? ''} /></h3>
			{#if spec?.tagline}<p><Rich text={spec.tagline} /></p>{/if}
		</div>
		<div class="meta">
			<span class="num">{year ?? ''}</span>
			{#if dri}<span class="muted">{dri}</span>{/if}
			<button onclick={(e) => onmilestone(e.currentTarget)} data-tip="Milestone details">Milestone</button>
			{#if spec}<button onclick={() => (panel = panel === 'story' ? null : 'story', pinId = null)} data-tip="Process, references and withheld items">Sources</button>{/if}
		</div>
	</header>
	<section class="track" bind:this={track} style:height="{heightVh * viewH}px">
		<div class="stage" style:height="{viewH}px">
			<div class="model" bind:this={pane} onpointermove={onPaneMove} onpointerleave={() => hover(null)} onpointerdown={onPaneDown} onpointerup={onPaneUp} role="presentation">
				{#if spec?.renderer === '2.5d'}<svg class="sc-svg" bind:this={svgEl}></svg>{/if}
				{#if poster && !holding}<img class="poster" src={poster} alt="" />{/if}
				<div class="kw" style:--kw="{kwSize}px">
					{#each chapters as c, i (c.id)}
						<div class="kwi" style:opacity={kws[i]?.o ?? 0} style:transform="translateY({kws[i]?.dy ?? 0}px)" aria-hidden={i !== cb}>
							<div class="big">{#each emphasis(c.keyword) as run, j (j)}{#if run.em}<em><Rich text={run.t} /></em>{:else}<Rich text={run.t} />{/if}{/each}</div>
							{#if c.line}<div class="line"><Rich text={c.line} /></div>{/if}
						</div>
					{/each}
				</div>
				{#each labels as l (l.id)}
					<div class="lab" class:on={on.includes(l.id)} bind:offsetWidth={labW[l.id]} style:left="{labelLeft(l.x, labW[l.id] ?? 0, paneW)}px" style:top="{l.y}px">
						<span><Rich text={l.name} /></span>{#if l.dim}<b class="num"><Rich text={l.dim} /></b>{/if}
					</div>
				{/each}
				{#if plotNow}
					<div class="plotbox" style:opacity={plotNow.o} style:transform="translateY({plotNow.dy}px)" class:live={plotNow.o > 0.5}>
						{#if plotShown}
							{#key plotShown.id}
								<PlotAssembler plot={plotShown} r={plotNow.rr} tip={plotTip} log={logOf(logState, plotShown)} onlog={(ax) => plotShown && (logState = toggleLog(logState, plotShown, ax))} />
							{/key}
						{/if}
						{#if alts.length > 1}
							<div class="alts" role="group" aria-label="Plot source">
								{#each alts as q (q.id)}
									<button class:on={q.id === plotShown?.id} onclick={() => plotNow && (altSel = { ...altSel, [plotNow.pl.id]: q.id })} data-tip={plainMarkup(q.title || q.id)}><Rich text={plotLabel(q)} /></button>
								{/each}
							</div>
						{/if}
					</div>
				{/if}
				{#if step}
					<div class="step" class:above={!!plotNow && plotNow.o > 0.01} data-tip={stepTipLines(step).map(plainMarkup).join('\n')}><Rich text={step.name} /></div>
				{/if}
			</div>
			<div class="side">
				{#if drawing}
					<div class="draw">
						<TraceView
							{drawing}
							{trace}
							image={drawing.image ? staticUrl(`data/showcases/drawings/${drawing.image}`) : null}
							{on}
							{pending}
							hover={(q, e) => hover(q, e)}
							pick={togglePin}
						/>
					</div>
				{/if}
				<ul class="parts" aria-label="Parts">
					{#each parts as q (q.id)}
						<li>
							<button
								class:on={on.includes(q.id)}
								class:fut={pending.has(q.id)}
								onpointerenter={(e) => hover(q.id, e)}
								onpointermove={(e) => hover(q.id, e)}
								onpointerleave={() => hover(null)}
								onfocus={(e) => {
									const r = e.currentTarget.getBoundingClientRect();
									hover(q.id, { clientX: r.left, clientY: r.bottom });
								}}
								onblur={() => hover(null)}
								onclick={() => togglePin(q.id)}
							>
								<span class="sw" style:background={q.look?.color ?? 'var(--ink-3)'}></span><span><Rich text={q.name} /></span>
							</button>
						</li>
					{/each}
				</ul>
			</div>
			<div class="ctrl">
				<button class="playbtn" class:on={playing} onclick={togglePlay} aria-label={playing ? 'Pause' : 'Play'} aria-pressed={playing} data-tip={playing ? 'Pause (Space)' : 'Play (Space)'} disabled={!ready}>
					<svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true">
						{#if playing}<rect x="2" y="1.5" width="2.8" height="9" /><rect x="7.2" y="1.5" width="2.8" height="9" />{:else}<polygon points="2.5,1.2 10.5,6 2.5,10.8" />{/if}
					</svg>
				</button>
				<div class="chap" role="group" aria-label="Chapters">
					{#each chapters as c, i (c.id)}
						<button class:on={i === cb} data-tip={plainMarkup(plainKeyword(c.keyword))} aria-label={plainMarkup(plainKeyword(c.keyword))} onclick={() => (pause(), goTo(chapterTarget(c)))}><span class="cn num">{i + 1}</span><span class="ck"><Rich text={plainKeyword(c.keyword)} /></span></button>
					{/each}
				</div>
				<input class="scrub" type="range" min="0" max="1000" value={Math.round(p * 1000)} aria-label="Story progress" data-tip="Story progress" oninput={(e) => (pause(), goTo(+e.currentTarget.value / 1000, false))} />
				<div class="grp" role="group" aria-label="Parts tour">
					<button onclick={() => tour(-1)} aria-label="Previous part" data-tip="Previous part (Left)">&lt;</button>
					<span class="muted">Parts</span>
					<button onclick={() => tour(1)} aria-label="Next part" data-tip="Next part (Right)">&gt;</button>
				</div>
				{#if assembled && hasExplode}
					<label class="grp ex" data-tip="Explode the assembly">
						<span class="muted">Explode</span>
						<input type="range" min="0" max="100" value={Math.round(k * 100)} oninput={(e) => (k = +e.currentTarget.value / 100)} />
					</label>
				{/if}
				{#if canOrbit}
					{#if free}
						<button onclick={resetView} data-tip="Back to the story camera">Reset view</button>
					{:else if coarse}
						<button onclick={() => (free = true, pose = three ? { pos: three.camera.position.clone(), target: controls?.target.clone() ?? new three.THREE.Vector3() } : null)} data-tip="Drag to orbit, pinch to zoom">Orbit</button>
					{/if}
				{/if}
			</div>
			{#if panel && spec}
				<div class="pwrap">
					<PartPanel {spec} part={panel === 'part' ? selPart : null} onclose={() => (pin(null), (panel = null))} />
				</div>
			{/if}
		</div>
	</section>
	{#if tipBox}
		<div class="sctip" role="tooltip" style:left="{Math.min(tipBox.x + 14, innerWidth - 270)}px" style:top="{tipBox.y + 16}px">
			{#each tipBox.lines as l, i (i)}<div class:b={i === 0}><Rich text={l} /></div>{/each}
		</div>
	{/if}
</article>

<style>
	/* thumbnail capture mode (?thumb=1, app/scripts/showcase-thumbs.mjs): the model only, no text or overlays */
	:global(html.sc-thumb) .kw, :global(html.sc-thumb) .lab, :global(html.sc-thumb) .plotbox, :global(html.sc-thumb) .step, :global(html.sc-thumb) .sctip { display: none !important; }
	.story { position: relative; margin: 0 0 8px; }
	/* plate language (D997): scotch rule over the story, display title, italic serif tagline; no edge bars, glows or
	   shadows in the chrome */
	.shead { position: relative; display: flex; flex-wrap: wrap; align-items: flex-end; gap: 6px 16px; margin: 28px 16px 0; padding: 16px 0 12px; border-top: 2px solid var(--rule, var(--ink-3)); }
	.shead::before { content: ''; position: absolute; left: 0; right: 0; top: 2px; border-top: 1px solid var(--rule, var(--ink-3)); }
	.tl { flex: 1; min-width: 240px; }
	.shead h3 { margin: 0; font: 500 42px/1.08 var(--display, inherit); font-variant-numeric: lining-nums; color: var(--ink); }
	.shead p { margin: 6px 0 0; font: italic 17px/1.35 var(--text, inherit); color: var(--ink-2); max-width: 720px; }
	.meta { display: flex; align-items: center; gap: 8px; font-size: 12px; }
	.meta .num { font-size: 13px; color: var(--ink); }

	.track { position: relative; }
	.stage {
		position: sticky;
		top: 0;
		display: grid;
		grid-template-columns: minmax(0, 1fr) 300px;
		grid-template-rows: minmax(0, 1fr) auto;
		grid-template-areas: 'model side' 'ctrl ctrl';
		overflow: hidden;
		background: var(--bg);
	}
	.reduced .stage { position: relative; }
	.model { grid-area: model; position: relative; min-width: 0; min-height: 0; overflow: hidden; touch-action: pan-y; }
	.model :global(canvas.sc-gl), .sc-svg, .poster { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
	.poster { object-fit: fill; pointer-events: none; }
	.kw { position: absolute; left: 0; top: 0; right: 0; pointer-events: none; }
	.kwi { position: absolute; left: 28px; top: 24px; right: 28px; will-change: opacity, transform; }
	/* a soft halo in the page background keeps the text legible over any model, in both themes */
	.big { font: 500 var(--kw) / 1.04 var(--display, inherit); font-variant-numeric: lining-nums; color: var(--ink); }
	.big em { font-style: italic; color: var(--amber, var(--warn)); letter-spacing: 0.012em; }
	.line { margin-top: 10px; max-width: 540px; font: 17px/1.4 var(--text, inherit); color: var(--ink-2); }
	/* canvas label: a flat plate with a top rule */
	.lab { position: absolute; transform: translateY(-50%); max-width: calc(100% - 8px); flex-wrap: wrap; display: flex; gap: 6px; align-items: baseline; padding: 2px 7px 3px; font: 13px var(--text, inherit); color: var(--ink-2); background: color-mix(in srgb, var(--ink-3) 18%, color-mix(in srgb, var(--bg) 85%, transparent)); pointer-events: none; font-variant-numeric: lining-nums; }
	.lab b { font-weight: 600; color: var(--ink); }
	.lab span, .lab b { white-space: nowrap; }
	.lab.on { background: color-mix(in srgb, var(--accent) 20%, color-mix(in srgb, var(--bg) 85%, transparent)); color: color-mix(in srgb, var(--accent) 70%, var(--ink)); }
	.plotbox { position: absolute; top: 16%; right: 16px; bottom: 16px; width: 50%; padding: 8px 8px 4px; background: color-mix(in srgb, var(--bg) 78%, transparent); pointer-events: none; }
	.plotbox.live { pointer-events: auto; }
	/* process step: a filled chip with a top rule */
	.step { position: absolute; left: 28px; bottom: 16px; padding: 3px 9px 4px; font: 14px var(--text, inherit); color: color-mix(in srgb, var(--accent) 75%, var(--ink)); background: color-mix(in srgb, var(--accent) 16%, var(--bg)); }
	.alts { position: absolute; left: 8px; top: 4px; display: flex; gap: 2px; z-index: 1; }
	.alts button { height: 20px; font-size: 10px; padding: 0 6px; }

	.side { grid-area: side; display: flex; flex-direction: column; gap: 10px; min-height: 0; padding: 16px 12px 8px 0; overflow: hidden; }
	.draw { flex: 1 1 50%; min-height: 140px; }
	.parts { flex: 0 1 auto; margin: 0; padding: 0; list-style: none; overflow-y: auto; min-height: 0; }
	.parts button { display: flex; align-items: center; gap: 8px; width: 100%; height: auto; min-height: 24px; padding: 3px 6px; text-align: left; background: transparent; border: 0; color: var(--ink-2); font: 14px var(--text, inherit); transition: opacity 0.15s; }
	.parts button:hover { color: var(--ink); background: var(--hover); }
	.parts button.on { color: var(--ink); background: color-mix(in srgb, var(--accent) 18%, transparent); }
	.parts button.fut { opacity: 0.35; }
	/* 1 px neutral outline: near-white swatches stay visible in the light theme, near-black ones in the dark theme */
	.sw { width: 9px; height: 9px; flex-shrink: 0; box-sizing: border-box; border: 1px solid color-mix(in srgb, var(--ink) 35%, transparent); }

	.ctrl { grid-area: ctrl; display: flex; flex-wrap: wrap; align-items: center; gap: 6px 14px; padding: 6px 12px 8px; border-top: 1px solid var(--border); background: var(--surface); }
	.chap { display: flex; gap: 2px; flex-wrap: wrap; }
	.playbtn { display: inline-flex; align-items: center; justify-content: center; width: 28px; padding: 0; }
	.playbtn svg { fill: currentColor; display: block; }
	.playbtn:disabled { opacity: 0.4; cursor: default; }
	.chap button { display: inline-flex; gap: 5px; align-items: center; font-size: 11px; }
	.chap .cn { color: var(--ink-3); }
	.chap button.on .cn { color: inherit; }
	.scrub { flex: 1; min-width: 120px; accent-color: var(--accent); }
	.grp { display: inline-flex; align-items: center; gap: 4px; }
	.ex input { width: 90px; accent-color: var(--accent); }

	.pwrap { grid-row: 1; grid-column: 1 / -1; position: relative; pointer-events: none; }
	.pwrap > :global(*) { pointer-events: auto; }
	.sctip { position: fixed; z-index: 100; max-width: 260px; padding: 4px 7px; font-size: 11px; line-height: 1.4; color: var(--ink-2); background: var(--surface); border: 1px solid var(--line); pointer-events: none; }
	.sctip .b { color: var(--ink); font-weight: 600; }

	@media (max-width: 1100px) {
		.chap .ck { display: none; }
	}
	@media (max-width: 700px) {
		.shead { margin: 20px 10px 0; padding: 12px 0 8px; }
		.shead h3 { font-size: 30px; }
		.shead p { font-size: 15px; }
		.stage { grid-template-columns: minmax(0, 1fr); grid-template-rows: minmax(0, 1fr) 26% auto; grid-template-areas: 'model' 'side' 'ctrl'; }
		.side { flex-direction: row; padding: 6px 8px 4px; gap: 8px; }
		.draw { flex: 0 0 38%; min-height: 0; }
		.parts { display: flex; flex-wrap: wrap; align-content: flex-start; gap: 2px; flex: 1; }
		.parts button { width: auto; font-size: 13px; padding: 2px 6px; }
		.kwi { left: 14px; top: 12px; right: 14px; }
		.line { font-size: 15px; margin-top: 6px; }
		.plotbox { top: auto; left: 8px; right: 8px; bottom: 8px; width: auto; height: 56%; }
		.step { left: 14px; bottom: 8px; }
		/* plot chapters: the plot fills the bottom of the pane, the step line sits just above it */
		.step.above { bottom: calc(56% + 14px); }
		.ctrl { padding: 4px 8px 6px; gap: 4px 10px; }
		.pwrap { grid-row: 1 / 3; }
		.scrub { order: -1; flex-basis: 100%; }
		.playbtn { width: 40px; height: 32px; }
		.chap button { height: 32px; min-width: 30px; justify-content: center; }
	}
	@media (prefers-reduced-motion: reduce) {
		.parts button { transition: none; }
	}
</style>
