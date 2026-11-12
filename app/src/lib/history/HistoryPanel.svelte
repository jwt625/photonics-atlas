<script lang="ts">
	import { onMount } from 'svelte';
	import type { Milestone } from './layout';

	let { m, color, figUrl, componentsHref, onclose }: { m: Milestone; color: string; figUrl: string; componentsHref: string; onclose: () => void } = $props();
	let closeBtn: HTMLButtonElement | undefined = $state();
	let imgFailed = $state(false);
	$effect(() => {
		void m.id;
		imgFailed = false;
	});
	onMount(() => closeBtn?.focus());
	const printed = $derived(m.orgs_printed || m.institutions.join('; '));
</script>

<aside class="hpanel" aria-label="Milestone details" style:--c={color}>
	<div class="head">
		<span class="tag num">{m.date || m.year}</span>
		<span class="tag thread">{m.thread}</span>
		<div class="grow"></div>
		<button bind:this={closeBtn} onclick={onclose} aria-label="Close" data-tip="Close (Esc)">Close</button>
	</div>
	<div class="body">
		<h2>{m.title || m.topic}</h2>
		{#if m.topic && m.title}<div class="topic">{m.topic}</div>{/if}
		{#if m.event}
			<h3>What the paper reports</h3>
			<p>{m.event}</p>
		{/if}
		{#if m.significance}
			<h3>Significance</h3>
			<p>{m.significance}</p>
		{/if}
		<dl>
			{#if m.dri}<dt data-tip="Directly responsible individual(s) for the work">DRI</dt><dd>{m.dri}</dd>{/if}
			{#if printed}<dt>Institutions</dt><dd>{printed}</dd>{/if}
			{#if m.venue}<dt>Venue</dt><dd>{m.venue}{m.year ? `, ${m.year}` : ''}</dd>{/if}
			{#if m.doi}<dt>DOI</dt><dd><a href="https://doi.org/{m.doi}" target="_blank" rel="noopener">{m.doi}</a></dd>{/if}
			{#if m.kind}<dt>Type</dt><dd>{m.kind}</dd>{/if}
			<dt>Material</dt><dd>{m.material}</dd>
			{#if m.materials.length && m.materials.join(', ') !== m.material}<dt data-tip="Platform of the paper's component rows">Platform</dt><dd>{m.materials.join(', ')}</dd>{/if}
		</dl>
		{#if m.fig}
			<h3>Key figure</h3>
			{#if m.has_local_figure && !imgFailed}
				<img src={figUrl} alt="{m.fig.label} of the paper" onerror={() => (imgFailed = true)} />
			{/if}
			<p class="cap"><b>{m.fig.label}</b>{m.fig.page ? ` (p. ${m.fig.page})` : ''}: {m.fig.caption}</p>
			{#if m.fig.reason}<p class="muted small">Why this figure: {m.fig.reason}</p>{/if}
			{#if !m.has_local_figure || imgFailed}<p class="muted small">Figure in the source paper.</p>{/if}
		{/if}
		{#if m.components.length}
			<h3>Component rows <span class="muted num">{m.components.length}, {m.n_metrics} values</span></h3>
			<ul class="comps">
				{#each m.components as c (c.id)}
					<li>
						<a href="{componentsHref}#{encodeURIComponent(c.id)}" data-tip="Open in the component atlas">{c.label}</a>
						<span class="muted">{c.class}, {c.n} value{c.n === 1 ? '' : 's'}</span>
					</li>
				{/each}
			</ul>
		{/if}
	</div>
</aside>

<style>
	.hpanel { position: absolute; top: 0; right: 0; bottom: 0; width: min(440px, 100%); display: grid; grid-template-rows: auto minmax(0, 1fr); background: var(--surface); border-left: 1px solid var(--border); z-index: 5; }
	.head { display: flex; flex-wrap: wrap; align-items: center; gap: 4px; padding: 6px 10px; border-bottom: 1px solid var(--border); }
	.tag { padding: 1px 6px; font-size: 11px; background: var(--surface-2); border: 1px solid var(--border); }
	/* the thread colour as a filled chip, not an edge bar */
	.tag.thread { background: color-mix(in srgb, var(--c, var(--accent)) 16%, transparent); border-color: transparent; color: color-mix(in srgb, var(--c, var(--accent)) 82%, var(--ink)); }
	.grow { flex: 1; }
	.body { overflow-y: auto; padding: 10px 14px 20px; }
	/* plate type (D997): display title, serif prose, small-caps kickers */
	.body { font: 14px/1.45 var(--text, inherit); }
	h2 { margin: 2px 0 6px; font: 500 22px/1.2 var(--display, inherit); }
	.topic { color: var(--ink-2); margin-bottom: 6px; font-style: italic; }
	h3 { margin: 16px 0 4px; font: 600 13px var(--text, inherit); font-variant-caps: all-small-caps; letter-spacing: 0.07em; color: var(--muted, var(--ink-3)); }
	p { margin: 0 0 4px; line-height: 1.45; }
	dl { display: grid; grid-template-columns: 96px minmax(0, 1fr); gap: 4px 8px; margin: 14px 0 0; padding-top: 6px; border-top: 1px solid var(--line); }
	dt { color: var(--muted, var(--ink-3)); font-variant-caps: all-small-caps; letter-spacing: 0.07em; font-weight: 600; }
	dd { margin: 0; overflow-wrap: anywhere; }
	img { display: block; max-width: 100%; height: auto; margin: 4px 0 6px; background: #fff; border: 1px solid var(--border); }
	.cap { color: var(--ink-2); }
	.small { font-size: 12px; }
	.comps { margin: 0; padding: 0; list-style: none; }
	.comps li { padding: 4px 0; border-bottom: 1px solid var(--grid); display: flex; flex-direction: column; gap: 1px; }
	@media (max-width: 700px) {
		.hpanel { position: fixed; top: auto; bottom: 0; height: 78vh; width: 100%; }
	}
</style>
