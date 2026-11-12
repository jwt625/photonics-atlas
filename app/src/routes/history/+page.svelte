<script lang="ts">
	import { onMount, tick } from 'svelte';
	import { getJson, link, staticUrl } from '../../lib/paths';
	import Expanded from '../../lib/history/Expanded.svelte';
	import HistoryFonts from '../../lib/history/HistoryFonts.svelte';
	import HistoryPanel from '../../lib/history/HistoryPanel.svelte';
	import { hasShowcase } from '../../lib/history/showcases';
	import { haystack, layoutTimeline, palette, shownMask, type HistoryView, type Milestone, type Mode } from '../../lib/history/layout';
	import { ui } from '../../lib/state.svelte';

	let view = $state<HistoryView | null>(null);
	let err = $state('');
	let width = $state(0);
	let mode = $state<Mode>('thread');
	let only = $state<Set<string>>(new Set());
	let q = $state('');
	let qLive = $state('');
	let selId = $state('');
	let vmode = $state<'expanded' | 'compact'>('expanded');
	/** "Stories" filter (?stories=1): only milestones with a showcase story, in both views */
	let storiesOnly = $state(false);
	/** compact-view story cards whose thumbnail failed to load (fall back to the plain node + marker) */
	let thumbFail = $state<Set<string>>(new Set());
	/** light-theme thumbnails missing: use the dark one */
	let lightFail = $state<Set<string>>(new Set());
	let failed = $state<Set<string>>(new Set());
	let timer: ReturnType<typeof setTimeout> | null = null;
	let lastNode: HTMLElement | null = null;

	const MODES: [Mode, string, string][] = [
		['thread', 'Topic', 'Research thread of the paper'],
		['inst', 'Institution', 'First listed institution (top 10 by count, rest as other)'],
		['material', 'Material', 'Main material the paper states (top 10); theory papers without one show theory / no device'],
		['era', 'Era', 'Decade-scale era of the timeline']
	];

	// ---------------------------------------------------------------- menu bar pin / unpin (expanded view, owner 2026-11-11)
	// Unpinned: the app nav row and the history toolbar + legend slide up out of view and the stories gain the height.
	// Pointer within EDGE px of the top (or on the revealed bar) shows them; leaving the bar hides them again. Touch: a
	// small handle at the top edge shows them; the next scroll down hides them. Choice kept per viewer (localStorage).
	// Default unpinned (owner 2026-11-11): pinned only after the viewer pins it.
	const PIN_KEY = 'history.barPinned';
	const EDGE = 12;
	let pinned = $state(false);
	let revealed = $state(false);
	let topEl: HTMLDivElement | undefined = $state();
	let pageEl: HTMLDivElement | undefined = $state();
	const unpinned = $derived(vmode === 'expanded' && !pinned);
	function setPinned(v: boolean) {
		pinned = v;
		revealed = false;
		try {
			localStorage.setItem(PIN_KEY, v ? '1' : '0');
		} catch {
			/* storage blocked: the choice lasts for this visit */
		}
	}
	function chromeBottom(): number {
		const hdr = document.querySelector('.app > header')?.getBoundingClientRect().bottom ?? 0;
		const tb = topEl && getComputedStyle(topEl).position === 'fixed' ? topEl.getBoundingClientRect().bottom : 0;
		return Math.max(hdr, tb);
	}
	function onPointerMove(e: PointerEvent) {
		if (!unpinned || e.pointerType === 'touch') return;
		if (!revealed && e.clientY <= EDGE) revealed = true;
		else if (revealed && e.clientY > chromeBottom() + 8) revealed = false;
	}
	let lastScroll = 0;
	let coarse = false;
	function onAnyScroll(e: Event) {
		const t = e.target as HTMLElement | Document;
		const top = t instanceof HTMLElement ? t.scrollTop : (document.scrollingElement?.scrollTop ?? 0);
		// touch: the next scroll down hides the revealed bar (pointer devices hide it when the pointer leaves it)
		if (unpinned && revealed && coarse && top > lastScroll + 4) revealed = false;
		lastScroll = top;
	}
	$effect(() => {
		const root = document.documentElement;
		root.classList.toggle('hist-unpinned', unpinned);
		root.classList.toggle('hist-reveal', unpinned && revealed);
		// the fixed toolbar sits under the (fixed) app header: publish the header height
		const hdr = document.querySelector<HTMLElement>('.app > header');
		if (hdr) root.style.setProperty('--hist-hdr', `${hdr.offsetHeight}px`);
	});

	onMount(() => {
		const root = document.documentElement;
		root.classList.add('hist-route');
		coarse = matchMedia('(pointer: coarse)').matches;
		try {
			pinned = localStorage.getItem(PIN_KEY) === '1';
		} catch {
			pinned = false;
		}
		addEventListener('pointermove', onPointerMove, { passive: true });
		addEventListener('scroll', onAnyScroll, { capture: true, passive: true });
		const hdr = document.querySelector<HTMLElement>('.app > header');
		const ro = new ResizeObserver(() => hdr && root.style.setProperty('--hist-hdr', `${hdr.offsetHeight}px`));
		if (hdr) ro.observe(hdr);
		const cleanup = () => {
			root.classList.remove('hist-route', 'hist-unpinned', 'hist-reveal', 'sc-thumb');
			root.style.removeProperty('--hist-hdr');
			removeEventListener('pointermove', onPointerMove);
			removeEventListener('scroll', onAnyScroll, { capture: true });
			ro.disconnect();
		};
		getJson<HistoryView>('data/history.json').then((v) => (view = v), (e: unknown) => (err = String(e)));
		const id = decodeURIComponent(location.hash.slice(1));
		if (id) selId = id;
		const qs = new URLSearchParams(location.search);
		if (qs.get('view') === 'compact') vmode = 'compact';
		if (qs.get('stories') === '1') storiesOnly = true;
		// thumbnail capture mode (app/scripts/showcase-thumbs.mjs): stories render the model only
		if (qs.get('thumb') === '1') root.classList.add('sc-thumb');
		return cleanup;
	});

	const ms = $derived(view?.milestones ?? []);
	const eras = $derived(view?.eras ?? []);
	// showcase milestones with a scene module (DevLog-017); a story that fails to load falls back to a card
	const stories = $derived(new Set(ms.filter((m) => m.showcase && hasShowcase(m.id) && !failed.has(m.id)).map((m) => m.id)));
	const cardIds = $derived(new Set([...stories].filter((id) => !thumbFail.has(id))));
	const lay = $derived(width ? layoutTimeline(ms, eras, width, cardIds) : null);
	const pal = $derived(palette(ms, eras, mode));
	const hay = $derived(ms.map(haystack));
	const terms = $derived(q.toLowerCase().split(/\s+/).filter(Boolean));
	const shown = $derived(shownMask(ms, { only, key: pal.key, terms, hay, storiesOnly, stories }));
	const nShown = $derived(shown.filter(Boolean).length);
	const sel = $derived(ms.find((m) => m.id === selId));

	/** Expanded (default) or compact view; compact is kept in the query (?view=compact), the milestone hash stays. */
	function setView(v: 'expanded' | 'compact') {
		if (v === vmode) return;
		vmode = v;
		const u = new URL(location.href);
		if (v === 'compact') u.searchParams.set('view', 'compact');
		else u.searchParams.delete('view');
		history.replaceState(history.state, '', u);
	}
	function setStoriesOnly(v: boolean) {
		storiesOnly = v;
		const u = new URL(location.href);
		if (v) u.searchParams.set('stories', '1');
		else u.searchParams.delete('stories');
		history.replaceState(history.state, '', u);
	}
	const thumbSrc = (id: string) => staticUrl(`data/showcases/thumbs/${id}${ui.theme === 'light' && !lightFail.has(id) ? '.light' : ''}.webp`);
	function onThumbError(id: string) {
		if (ui.theme === 'light' && !lightFail.has(id)) lightFail = new Set(lightFail).add(id);
		else thumbFail = new Set(thumbFail).add(id);
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

<div class="page" class:unpinned class:reveal={unpinned && revealed} bind:this={pageEl}>
	{#if unpinned}
		<!-- pointer: the top edge reveals the bar; touch: the handle does -->
		<div class="chrome-hot" aria-hidden="true" onpointerenter={(e) => e.pointerType !== 'touch' && (revealed = true)}></div>
		{#if !revealed}
			<button class="chrome-handle" aria-label="Show the menu bar" data-tip="Show the menu bar" onclick={() => (revealed = true)}>
				<svg viewBox="0 0 12 8" width="12" height="8" aria-hidden="true"><polyline points="1,1.5 6,6.5 11,1.5" /></svg>
			</button>
		{/if}
	{/if}
	<div class="top" bind:this={topEl} onfocusin={() => unpinned && (revealed = true)}>
	<div class="bar">
		<div class="modes vt" role="group" aria-label="View">
			<button class:on={vmode === 'expanded'} aria-pressed={vmode === 'expanded'} data-tip="Eras with showcase stories and milestone cards" onclick={() => setView('expanded')}>Expanded</button>
			<button class:on={vmode === 'compact'} aria-pressed={vmode === 'compact'} data-tip="Serpentine timeline of all milestones" onclick={() => setView('compact')}>Compact</button>
		</div>
		<button class="stbtn" class:on={storiesOnly} aria-pressed={storiesOnly} data-tip="Show only milestones with a story" onclick={() => setStoriesOnly(!storiesOnly)}>Stories <span class="num">{stories.size}</span></button>
		<div class="modes" role="group" aria-label="Color by">
			<span class="muted">Color</span>
			{#each MODES as [k, l, t]}
				<button class:on={mode === k} data-tip={t} onclick={() => setMode(k)}>{l}</button>
			{/each}
		</div>
		<input type="search" placeholder="Search title, topic, people, institution, DOI" value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
		<span class="muted num">{nShown} / {ms.length} milestones</span>
		{#if vmode === 'expanded'}
			<button class="pinbtn" class:on={pinned} aria-pressed={pinned} aria-label={pinned ? 'Unpin the menu bar' : 'Pin the menu bar'} data-tip={pinned ? 'Unpin the menu bar' : 'Pin the menu bar'} onclick={() => setPinned(!pinned)}>
				<svg viewBox="0 0 14 14" width="14" height="14" aria-hidden="true">
					{#if pinned}<path d="M5 1h4v1.5l-.8.8v3.4L10 8.5v1H7.6V13h-1.2V9.5H4v-1l1.8-1.8V3.3L5 2.5z" />{:else}<path class="ol" d="M5 1.5h4v1l-.8.8v3.6L10 8.7v.6H4v-.6l1.8-1.8V3.3L5 2.5z M7 9.3V13" />{/if}
				</svg>
			</button>
		{/if}
	</div>
	<div class="legend">
		{#each pal.items as it (it.key)}
			<button class="chip" class:off={only.size > 0 && !only.has(it.key)} data-tip="Click to show only this group; click again to undo" onclick={() => toggle(it.key)}>
				<span class="sw" style:background={it.color}></span>{it.key}<span class="muted num">{it.n}</span>
			</button>
		{/each}
		{#if only.size}<button class="chip clear" onclick={() => (only = new Set())}>show all</button>{/if}
	</div>
	</div>

	<div class="scroll" class:withpanel={!!sel}>
		<div class="intro muted">Milestones of guided-wave and integrated photonics in date order. Hover a point for the reference; click it for the event, the people and the key figure.</div>
		{#if err}
			<div class="err">Could not load the history view: {err}</div>
		{/if}
		{#if vmode === 'expanded'}
			{#if view}
				<Expanded {ms} {eras} {stories} {shown} color={(m) => pal.color.get(pal.key(m)) ?? ''} group={(m) => pal.key(m)} {selId} {tip} onopen={open} onfail={storyFailed} {storiesOnly} />
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
					{#if lay.thumb[i]}
						<!-- a showcase story: its thumbnail card is one large click target into the story -->
						<button
							class="tcard"
							class:mob={lay.mobile}
							class:dim={!shown[i]}
							style:left="{lay.mobile ? p.x - 7 : p.x - lay.thumbW / 2}px"
							style:top="{lay.mobile ? p.y - 7 : p.y - lay.thumbH / 2}px"
							style:width="{lay.thumbW}px"
							style:--c={pal.color.get(pal.key(m))}
							data-tip={tip(m)}
							aria-label="Open the story: {m.year ?? ''} {label(m)}"
							onclick={() => toStory(m.id)}
						>
							<span class="timg" style:height="{lay.thumbH}px">
								<img src={thumbSrc(m.id)} alt="" loading="lazy" decoding="async" onerror={() => onThumbError(m.id)} />
								<span class="stag"><svg viewBox="0 0 8 8" width="7" height="7" aria-hidden="true"><polygon points="1,0.5 7.5,4 1,7.5" /></svg>Story</span>
							</span>
							<span class="txt"><b class="num">{m.year ?? ''}</b> <span class="lab">{label(m)}</span></span>
						</button>
					{:else}
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
		position: relative; height: 100%; display: grid; grid-template-rows: auto minmax(0, 1fr); background: var(--bg);
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
	/* 1 px neutral outline: near-white swatches stay visible in the light theme, near-black ones in the dark theme */
	.sw { width: 9px; height: 9px; flex-shrink: 0; box-sizing: border-box; border: 1px solid color-mix(in srgb, var(--ink) 35%, transparent); }
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
	/* story thumbnail card (compact view): image + label, one click target; tag in the topic colour */
	.tcard { position: absolute; display: flex; flex-direction: column; align-items: center; gap: 4px; height: auto; padding: 0; border: 0; background: transparent; text-align: center; transition: opacity 0.2s; z-index: 1; }
	.tcard:hover { background: transparent; }
	.timg { position: relative; display: block; width: 100%; overflow: hidden; background: var(--surface-2); border: 1px solid var(--border); }
	.timg img { display: block; width: 100%; height: 100%; object-fit: cover; }
	.tcard:hover .timg, .tcard:focus-visible .timg { border-color: var(--ink-3); }
	.stag { position: absolute; left: 4px; top: 4px; display: inline-flex; align-items: center; gap: 3px; padding: 0 5px; height: 16px; font-size: 10px; color: var(--c, var(--accent)); background: color-mix(in srgb, var(--c, var(--accent)) 22%, var(--surface)); }
	.stag svg { position: static; inset: auto; fill: currentColor; }
	.tcard .txt { font-size: 11px; line-height: 14px; color: var(--ink-2); display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
	.tcard .txt b { color: var(--ink); font-weight: 600; }
	.tcard:hover .lab { color: var(--ink); }
	.tcard.dim { opacity: 0.12; }
	.tcard.mob { align-items: flex-start; text-align: left; }
	.stbtn { display: inline-flex; gap: 5px; align-items: center; }
	.stbtn .num { opacity: 0.8; }
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

	/* ---- menu bar pin / unpin (expanded view) ---- */
	.pinbtn { display: inline-flex; align-items: center; justify-content: center; width: 26px; padding: 0; margin-left: auto; }
	/* the page's own svg rule positions the timeline svg absolutely: icons opt out */
	.pinbtn svg, .chrome-handle svg { position: static; inset: auto; pointer-events: none; }
	.pinbtn svg { fill: currentColor; }
	.pinbtn svg .ol { fill: none; stroke: currentColor; stroke-width: 1.3; stroke-linejoin: miter; }
	/* the app shell follows the visible viewport on phones (address bar) while the history route is open */
	:global(html.hist-route .app) { height: 100vh; height: 100dvh; }
	/* unpinned: the app header and the toolbar leave the layout and slide up; the stories take the height */
	:global(html.hist-unpinned .app) { grid-template-rows: minmax(0, 1fr) auto; }
	:global(html.hist-unpinned .app > header) { position: fixed; top: 0; left: 0; right: 0; height: var(--hdr); z-index: 40; transform: translateY(-100%); transition: transform 0.2s ease; }
	:global(html.hist-unpinned.hist-reveal .app > header) { transform: none; }
	.page.unpinned { grid-template-rows: minmax(0, 1fr); }
	.page.unpinned .top { position: fixed; left: 0; right: 0; top: var(--hist-hdr, 36px); z-index: 39; transform: translateY(calc(-100% - var(--hist-hdr, 36px))); transition: transform 0.2s ease; }
	.page.unpinned.reveal .top { transform: none; }
	.chrome-hot { position: fixed; left: 0; right: 0; top: 0; height: 12px; z-index: 38; }
	.chrome-handle { display: none; position: fixed; top: 0; left: 50%; transform: translateX(-50%); z-index: 41; width: 56px; height: 18px; padding: 0; align-items: center; justify-content: center; background: var(--surface); border: 1px solid var(--border); border-top: 0; }
	.chrome-handle svg { fill: none; stroke: var(--ink-2); stroke-width: 1.5; }
	@media (pointer: coarse) {
		.chrome-handle { display: inline-flex; }
		.chrome-hot { display: none; }
	}
	@media (max-width: 700px) {
		/* phones: the toolbar scrolls with the page anyway; only the app header hides */
		.page.unpinned { display: block; }
		.page.unpinned .top { position: static; transform: none; transition: none; }
		:global(html.hist-unpinned .app > header) { height: auto; }
	}
	@media (prefers-reduced-motion: reduce) {
		:global(html.hist-unpinned .app > header), .page.unpinned .top { transition: none; }
	}
</style>
