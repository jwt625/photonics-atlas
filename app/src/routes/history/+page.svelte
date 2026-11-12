<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { getJson, link, staticUrl } from '../../lib/paths';
	import Expanded from '../../lib/history/Expanded.svelte';
	import HistoryFonts from '../../lib/history/HistoryFonts.svelte';
	import HistoryPanel from '../../lib/history/HistoryPanel.svelte';
	import { hasShowcase } from '../../lib/history/showcases';
	import { haystack, layoutTimeline, palette, type HistoryView, type Milestone, type Mode } from '../../lib/history/layout';

	let view = $state<HistoryView | null>(null);
	let err = $state('');
	let width = $state(0);
	let mode = $state<Mode>('thread');
	let only = $state<Set<string>>(new Set());
	let q = $state('');
	let qLive = $state('');
	let selId = $state('');
	let vmode = $state<'expanded' | 'compact'>('expanded');
	let failed = $state<Set<string>>(new Set());
	let timer: ReturnType<typeof setTimeout> | null = null;
	let lastNode: HTMLElement | null = null;

	const MODES: [Mode, string, string][] = [
		['thread', 'Topic', 'Research thread of the paper'],
		['inst', 'Institution', 'First listed institution (top 10 by count, rest as other)'],
		['material', 'Material', 'Main material the paper states (top 10); theory papers without one show theory / no device'],
		['era', 'Era', 'Decade-scale era of the timeline']
	];

	onMount(() => {
		getJson<HistoryView>('data/history.json').then((v) => (view = v), (e: unknown) => (err = String(e)));
		const id = decodeURIComponent(location.hash.slice(1));
		if (id) selId = id;
		if (new URLSearchParams(location.search).get('view') === 'compact') vmode = 'compact';
	});

	const ms = $derived(view?.milestones ?? []);
	const eras = $derived(view?.eras ?? []);
	const lay = $derived(width ? layoutTimeline(ms, eras, width) : null);
	const pal = $derived(palette(ms, eras, mode));
	const hay = $derived(ms.map(haystack));
	const terms = $derived(q.toLowerCase().split(/\s+/).filter(Boolean));
	const shown = $derived(ms.map((m, i) => (only.size === 0 || only.has(pal.key(m))) && terms.every((t) => hay[i].includes(t))));
	const nShown = $derived(shown.filter(Boolean).length);
	const sel = $derived(ms.find((m) => m.id === selId));
	// showcase milestones with a scene module (DevLog-017); a story that fails to load falls back to a card
	const stories = $derived(new Set(ms.filter((m) => m.showcase && hasShowcase(m.id) && !failed.has(m.id)).map((m) => m.id)));

	/** Expanded (default) or compact view; compact is kept in the query (?view=compact), the milestone hash stays. */
	function setView(v: 'expanded' | 'compact') {
		if (v === vmode) return;
		vmode = v;
		const u = new URL(location.href);
		if (v === 'compact') u.searchParams.set('view', 'compact');
		else u.searchParams.delete('view');
		history.replaceState(history.state, '', u);
	}
	async function toStory(id: string) {
		setView('expanded');
		await tick();
		requestAnimationFrame(() => document.getElementById(`story-${id}`)?.scrollIntoView({ block: 'start' }));
	}
	function storyFailed(id: string) {
		failed = new Set(failed).add(id);
	}

	function onInput(v: string) {
		qLive = v;
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => (q = v), 300);
	}
	function setMode(m: Mode) {
		mode = m;
		only = new Set();
	}
	function toggle(k: string) {
		const s = new Set(only);
		if (s.has(k)) s.delete(k);
		else s.add(k);
		only = s;
	}
	async function open(m: Milestone, el: HTMLElement) {
		lastNode = el;
		selId = m.id;
		history.replaceState(history.state, '', `#${encodeURIComponent(m.id)}`);
		// the timeline reflows into the space left of the panel; keep the clicked node in view
		await tick();
		setTimeout(() => document.querySelector('.hnode.sel, .hcard.sel')?.scrollIntoView({ block: 'nearest' }), 220);
	}
	async function close() {
		if (!selId) return;
		selId = '';
		history.replaceState(history.state, '', location.pathname + location.search);
		await tick();
		lastNode?.focus();
	}
	function onKey(e: KeyboardEvent) {
		if (e.key === 'Escape') close();
	}
	function onDown(e: PointerEvent) {
		const t = e.target as Element | null;
		if (selId && !t?.closest('.hpanel') && !t?.closest('.hnode, .hcard, .shead, .vt')) close();
	}
	const label = (m: Milestone) => m.topic || m.title;
	const tip = (m: Milestone) =>
		[m.venue, m.date || m.year, m.dri && `DRI: ${m.dri}`, (m.institutions.length ? m.institutions.join('; ') : m.orgs_printed) || '', m.doi && `doi:${m.doi}`]
			.filter(Boolean)
			.join(' | ');
</script>

<svelte:window onkeydown={onKey} onpointerdown={onDown} />

<HistoryFonts />

<div class="page">
	<div class="bar">
		<div class="modes vt" role="group" aria-label="View">
			<button class:on={vmode === 'expanded'} aria-pressed={vmode === 'expanded'} data-tip="Eras with showcase stories and milestone cards" onclick={() => setView('expanded')}>Expanded</button>
			<button class:on={vmode === 'compact'} aria-pressed={vmode === 'compact'} data-tip="Serpentine timeline of all milestones" onclick={() => setView('compact')}>Compact</button>
		</div>
		<div class="modes" role="group" aria-label="Color by">
			<span class="muted">Color</span>
			{#each MODES as [k, l, t]}
				<button class:on={mode === k} data-tip={t} onclick={() => setMode(k)}>{l}</button>
			{/each}
		</div>
		<input type="search" placeholder="Search title, topic, people, institution, DOI" value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
		<span class="muted num">{nShown} / {ms.length} milestones</span>
	</div>
	<div class="legend">
		{#each pal.items as it (it.key)}
			<button class="chip" class:off={only.size > 0 && !only.has(it.key)} data-tip="Click to show only this group; click again to undo" onclick={() => toggle(it.key)}>
				<span class="sw" style:background={it.color}></span>{it.key}<span class="muted num">{it.n}</span>
			</button>
		{/each}
		{#if only.size}<button class="chip clear" onclick={() => (only = new Set())}>show all</button>{/if}
	</div>

	<div class="scroll" class:withpanel={!!sel}>
		<div class="intro muted">Milestones of guided-wave and integrated photonics in date order. Hover a point for the reference; click it for the event, the people and the key figure.</div>
		{#if err}
			<div class="err">Could not load the history view: {err}</div>
		{/if}
		{#if vmode === 'expanded'}
			{#if view}
				<Expanded {ms} {eras} {stories} {shown} color={(m) => pal.color.get(pal.key(m)) ?? ''} group={(m) => pal.key(m)} {selId} {tip} onopen={open} onfail={storyFailed} />
			{/if}
		{:else}
		<div class="canvas" bind:clientWidth={width} style:height={lay ? `${lay.height}px` : '60vh'}>
			{#if lay}
				<svg width={width} height={lay.height} aria-hidden="true">
					<path d={lay.path} class="trail" />
				</svg>
				{#each lay.bands as b (b.era.id)}
					<section class="band" style:left="{b.x}px" style:top="{b.y}px" style:width="{b.w}px" style:min-height="{b.h}px">
						<h2>{b.era.years}<span class="muted num cnt">{b.n} milestone{b.n === 1 ? '' : 's'}</span></h2>
						<p>{b.era.intro}</p>
					</section>
				{/each}
				{#each ms as m, i (m.id)}
					{@const p = lay.nodes[i]}
					<button
						class="hnode"
						class:mob={lay.mobile}
						class:dim={!shown[i]}
						class:sel={m.id === selId}
						style:left="{lay.mobile ? p.x - 7 : p.x - lay.slot / 2}px"
						style:top="{p.y - 7}px"
						style:width="{lay.slot}px"
						style:--c={pal.color.get(pal.key(m))}
						data-tip={tip(m)}
						aria-label="{m.year ?? ''} {label(m)}"
						onclick={(e) => open(m, e.currentTarget)}
					>
						<span class="dot"></span>
						<span class="txt"><b class="num">{m.year ?? ''}</b> <span class="lab">{label(m)}</span></span>
					</button>
					{#if stories.has(m.id)}
						<button class="smark" style:left="{p.x + 6}px" style:top="{p.y - 15}px" data-tip="Showcase story" aria-label="Open the {label(m)} story" onclick={() => toStory(m.id)}></button>
					{/if}
				{/each}
			{/if}
		</div>
		{/if}
	</div>

	{#if sel}
		<HistoryPanel m={sel} color={pal.color.get(pal.key(sel)) ?? ''} figUrl={staticUrl(`data/history_figs/${sel.id}.png`)} componentsHref={link('/components')} onclose={close} />
	{/if}
</div>

<style>
	/* Plate type and palette for the history tab (DevLog-017 D997): display and prose faces switch, data UI stays sans. */
	.page {
		position: relative; height: 100%; display: grid; grid-template-rows: auto auto minmax(0, 1fr); background: var(--bg);
		--display: 'Playfair Display', 'Source Serif 4', Georgia, serif; --text: 'Source Serif 4', Georgia, serif;
		--muted: #a8a69d; --amber: #f7962c; --rule: var(--muted);
	}
	:global(:root[data-theme='light']) .page { --muted: #5f5e59; --amber: #b85f08; }
	.bar { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 14px; padding: 6px 10px; background: var(--surface); border-bottom: 1px solid var(--border); }
	.modes { display: flex; align-items: center; gap: 2px; }
	.modes .muted { margin-right: 6px; }
	.bar input { width: 300px; max-width: 100%; }
	.legend { display: flex; flex-wrap: wrap; gap: 4px; padding: 6px 10px; border-bottom: 1px solid var(--border); background: var(--surface); }
	.chip { display: inline-flex; align-items: center; gap: 6px; height: 22px; font-size: 11px; background: transparent; }
	.chip.off { opacity: 0.4; }
	.chip.clear { color: var(--accent); }
	.sw { width: 9px; height: 9px; flex-shrink: 0; }
	.scroll { overflow-y: auto; overflow-x: hidden; min-height: 0; transition: padding-right 0.15s; }
	.scroll.withpanel { padding-right: min(440px, 100%); }
	.intro { max-width: 900px; padding: 10px 16px 0; font-size: 12px; }
	.err { padding: 12px 16px; color: var(--crit); }
	.canvas { position: relative; margin: 0 8px 24px; }
	svg { position: absolute; inset: 0; pointer-events: none; }
	.trail { fill: none; stroke: var(--line); stroke-width: 2; }
	/* scotch rule (2px over 1px) above the era band; accent era number; display face for the years */
	.band { position: absolute; padding: 8px 12px; border-top: 2px solid var(--rule); background: var(--surface); }
	.band::before { content: ''; position: absolute; left: 0; right: 0; top: 2px; border-top: 1px solid var(--rule); }
	.band h2 { margin: 0 0 4px; font: 500 15px/18px var(--display); font-variant-numeric: lining-nums; }
	.band .cnt { margin-left: 8px; font: 600 12px var(--text); font-variant-caps: all-small-caps; letter-spacing: 0.07em; color: var(--muted); }
	.band p { margin: 0; color: var(--ink-2); font: 12px/17px var(--text); }

	.hnode { position: absolute; display: flex; flex-direction: column; align-items: center; gap: 4px; height: auto; padding: 0 4px 2px; border: 0; background: transparent; text-align: center; transition: opacity 0.2s; }
	.hnode:hover { background: transparent; }
	.hnode .dot { width: 14px; height: 14px; flex-shrink: 0; background: var(--c, var(--ink-3)); border: 2px solid var(--bg); box-shadow: 0 0 0 1px var(--c, var(--ink-3)); transition: transform 0.15s; }
	.hnode:hover .dot,
	.hnode:focus-visible .dot,
	.hnode.sel .dot { transform: scale(1.35); }
	.hnode .txt { font-size: 11px; line-height: 14px; color: var(--ink-2); display: -webkit-box; -webkit-line-clamp: 3; line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
	.hnode .txt b { color: var(--ink); font-weight: 600; }
	.hnode:hover .lab,
	.hnode.sel .lab { color: var(--ink); }
	.hnode.dim { opacity: 0.12; }
	.smark { position: absolute; width: 10px; height: 10px; padding: 0; border: 0; background: var(--accent); clip-path: polygon(50% 0, 100% 50%, 50% 100%, 0 50%); z-index: 1; }
	.smark:hover { background: var(--ink); }
	.hnode.mob { flex-direction: row; align-items: flex-start; gap: 10px; text-align: left; padding: 0; }
	.hnode.mob .txt { -webkit-line-clamp: 2; line-clamp: 2; margin-top: -1px; }

	@media (max-width: 700px) {
		.scroll.withpanel { padding-right: 0; }
		/* one scroll for controls and timeline: the legend must not eat the screen */
		.page { display: block; overflow-y: auto; }
		.scroll { overflow: visible; }
		.bar input { width: 100%; }
		.intro { padding: 8px 10px 0; }
		.canvas { margin: 0 4px 16px; }
	}
	@media (prefers-reduced-motion: reduce) {
		.hnode, .hnode .dot { transition: none; }
	}
</style>
