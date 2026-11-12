<script lang="ts">
	// Expanded history view (DevLog-017 section 1): one vertical scroll through the eras; per era its header, its
	// showcase stories, then the remaining milestones as a dense card strip.
	import { eraOf, type Era, type Milestone } from './layout';
	import ShowcaseStory from './showcase/ShowcaseStory.svelte';

	let {
		ms,
		eras,
		stories,
		shown,
		color,
		selId,
		tip,
		onopen,
		onfail
	}: {
		ms: Milestone[];
		eras: Era[];
		/** milestone ids that show a story */
		stories: ReadonlySet<string>;
		/** filter / search result, same index as ms */
		shown: boolean[];
		color: (m: Milestone) => string;
		selId: string;
		tip: (m: Milestone) => string;
		onopen: (m: Milestone, el: HTMLElement) => void;
		onfail: (id: string) => void;
	} = $props();

	const groups = $derived(
		eras.map((e) => {
			const idx = ms.map((m, i) => [m, i] as const).filter(([m]) => eraOf(m, eras) === e.id);
			return { era: e, n: idx.length, story: idx.filter(([m]) => stories.has(m.id)).map(([m]) => m), cards: idx.filter(([m]) => !stories.has(m.id)) };
		})
	);
</script>

<div class="exp">
	{#each groups as g (g.era.id)}
		<section class="era" id="era-{g.era.id}">
			<header class="eh">
				<div class="eid"><span class="yrs num">{g.era.years}</span></div>
				<p>{g.era.intro}</p>
				<span class="num cnt">{g.n} milestone{g.n === 1 ? '' : 's'}</span>
			</header>
			{#each g.story as m (m.id)}
				<ShowcaseStory id={m.id} year={m.year} dri={m.dri} onmilestone={(el) => onopen(m, el)} {onfail} />
			{/each}
			{#if g.cards.length}
				<div class="strip">
					{#each g.cards as [m, i] (m.id)}
						<button class="hcard" class:dim={!shown[i]} class:sel={m.id === selId} style:--c={color(m)} data-tip={tip(m)} onclick={(e) => onopen(m, e.currentTarget)}>
							<span class="yr num">{m.year ?? ''}</span>
							<span class="tp">{m.topic || m.title}</span>
							{#if m.dri}<span class="dri">{m.dri}</span>{/if}
						</button>
					{/each}
				</div>
			{/if}
		</section>
	{/each}
</div>

<style>
	/* plate language (DevLog-017 D997): scotch rule over each era, accent era number, display face for the years, serif
	   prose, small-caps kicker; cards carry their category as a top bar, never a left-edge bar */
	.exp { padding: 0 0 32px; }
	.era { padding: 0 0 18px; }
	.eh { position: relative; display: grid; grid-template-columns: auto minmax(0, 1fr) auto; align-items: baseline; gap: 4px 18px; margin: 28px 16px 0; padding: 14px 0 12px; border-top: 2px solid var(--rule); }
	.eh::before { content: ''; position: absolute; left: 0; right: 0; top: 2px; border-top: 1px solid var(--rule); }
	.eid { display: flex; align-items: baseline; gap: 12px; }
	.yrs { font: 500 30px/1.1 var(--display); font-variant-numeric: lining-nums; }
	.eh p { margin: 0; color: var(--ink-2); font: 14px/1.45 var(--text); max-width: 900px; }
	.cnt { font: 600 13px var(--text); font-variant-caps: all-small-caps; letter-spacing: 0.07em; color: var(--muted); white-space: nowrap; }
	.strip { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 6px; padding: 4px 16px 0; }
	.hcard { display: flex; flex-direction: column; align-items: stretch; gap: 3px; height: auto; min-height: 64px; padding: 7px 10px 8px; text-align: left; background: var(--surface); border: 1px solid var(--border); border-top: 3px solid var(--c, var(--ink-3)); transition: opacity 0.2s; }
	.hcard:hover { background: var(--surface-2); border-color: var(--ink-3); border-top-color: var(--c, var(--ink-3)); }
	.hcard.sel { background: color-mix(in srgb, var(--accent) 12%, var(--surface)); border-color: var(--accent); border-top-color: var(--c, var(--accent)); }
	.hcard.dim { opacity: 0.15; }
	.yr { font: 600 13px var(--text); font-variant-caps: all-small-caps; letter-spacing: 0.07em; color: var(--muted); }
	.tp { font: 500 14px/1.25 var(--text); color: var(--ink); display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
	.dri { font: italic 12px var(--text); color: var(--ink-3); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	@media (max-width: 700px) {
		.eh { grid-template-columns: minmax(0, 1fr) auto; margin: 20px 10px 0; padding: 12px 0 10px; }
		.eh p { grid-column: 1 / -1; grid-row: 2; font-size: 13px; }
		.yrs { font-size: 24px; }
		.strip { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); padding: 4px 10px 0; }
	}
	@media (prefers-reduced-motion: reduce) {
		.hcard { transition: none; }
	}
</style>
