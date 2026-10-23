<script lang="ts">
	// Org events (acquisition, rename, spin-off, merger) with participants and the publications that report them.
	import type { OrgEvent } from './types';
	import type { Pub } from './pub';
	import { pubTip } from './pub';

	let {
		events,
		self = '',
		name,
		href,
		onpick,
		sources
	}: { events: OrgEvent[]; self?: string; name: (id: string) => string; href: (id: string) => string; onpick?: (id: string) => void; sources: Record<string, Pub> } = $props();
</script>

{#each events as ev (ev.id)}
	<div class="ev">
		<div><span class="num">{ev.effective || ev.announced || 'undated'}</span> {ev.type.replace(/_/g, ' ')}{#if ev.announced && ev.effective && ev.announced !== ev.effective}<span class="muted ann">(announced {ev.announced})</span>{/if}</div>
		<div>{#each ev.participants as p, i}{i ? '; ' : ''}{#if p.org === self}<b>{name(p.org)}</b>{:else}<a href={href(p.org)} onclick={() => onpick?.(p.org)}>{name(p.org)}</a>{/if} <span class="muted">{p.role.replace(/_/g, ' ')}</span>{/each}</div>
		{#if ev.sources.some((s) => sources[s])}
			<div class="src">{#each ev.sources.filter((s) => sources[s]) as s, i}{i ? '; ' : ''}{@const p = sources[s]}{#if p.url}<a href={p.url} target="_blank" rel="noopener" data-tip={pubTip(p)}>{p.title}</a>{:else}<span data-tip={pubTip(p)}>{p.title}</span>{/if}{/each}</div>
		{/if}
	</div>
{/each}

<style>
	.ev { padding: 3px 0; border-bottom: 1px solid var(--grid); }
	.src { font-size: 10px; color: var(--ink-3); }
	.ann { margin-left: 4px; }
</style>
