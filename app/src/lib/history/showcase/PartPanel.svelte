<script lang="ts">
	// Side panel of a story: one part (detail, quote, locator, full dimension table with basis) or, with no part, the
	// story (process steps with their parameters); both end with the story's references and withheld items.
	import type { Part, ShowcaseSpec } from './types';

	let { spec, part, onclose }: { spec: ShowcaseSpec; part: Part | null; onclose: () => void } = $props();

	const BASIS: Record<string, string> = {
		stated: 'Stated in the source text',
		figure: 'Measured from a figure with a printed scale',
		ref: 'Other primary or museum source',
		assumed: 'Assumed (secondary dimension, not in the sources)',
		derived: 'Derived from stated values',
		digitized: 'Digitized from a figure'
	};
	const val = (v: number | string, u?: string) => `${v}${u ? ' ' + u : ''}`;
</script>

<aside class="pp" aria-label={part ? `${part.name} details` : `${spec.title} sources`}>
	<div class="head">
		<span class="kind">{part ? 'Part' : 'Story'}</span>
		<div class="grow"></div>
		<button onclick={onclose} aria-label="Close" data-tip="Close (Esc)">Close</button>
	</div>
	<div class="body">
		{#if part}
			<h2>{part.name}</h2>
			{#if part.role}<p class="role">{part.role}</p>{/if}
			{#if part.material}<p class="muted">{part.material}</p>{/if}
			{#if part.detail}<p>{part.detail}</p>{/if}
			{#if part.quote}
				<blockquote>{part.quote}</blockquote>
			{/if}
			{#if part.locator}<p class="loc">{part.locator}</p>{/if}
			{#if part.dims?.length}
				<h3>Dimensions</h3>
				<table>
					<tbody>
						{#each part.dims as d, i (i)}
							<tr class:assumed={d.basis === 'assumed'}>
								<td>{d.label}</td>
								<td class="num v">{val(d.value, d.unit)}</td>
								<td><span class="b" data-tip={[BASIS[d.basis ?? ''] ?? d.basis, d.locator].filter(Boolean).join('\n')}>{d.basis ?? ''}</span></td>
							</tr>
						{/each}
					</tbody>
				</table>
			{/if}
		{:else}
			<h2>{spec.title}</h2>
			{#if spec.tagline}<p class="role">{spec.tagline}</p>{/if}
			{#if spec.title_note}<p class="note">{spec.title_note}</p>{/if}
			{#each spec.process ?? [] as st (st.id)}
				<h3>{st.name}</h3>
				{#if st.params?.length}
					<table>
						<tbody>
							{#each st.params as q, i (i)}
								<tr class:assumed={q.basis === 'assumed'}>
									<td>{q.label}</td>
									<td class="num v">{val(q.value, q.unit)}</td>
									<td><span class="b" data-tip={[BASIS[q.basis ?? ''] ?? q.basis, q.source ?? st.source, q.locator].filter(Boolean).join('\n')}>{q.basis ?? ''}</span></td>
								</tr>
							{/each}
						</tbody>
					</table>
				{/if}
			{/each}
		{/if}
		{#if spec.references?.length}
			<h3>References</h3>
			<ul class="refs">
				{#each spec.references as r (r.id)}
					<li>
						{#if r.url}<a href={r.url} target="_blank" rel="noopener">{r.cite}</a>{:else}{r.cite}{/if}
						{#if r.used_for}<span class="muted">{r.used_for}</span>{/if}
					</li>
				{/each}
			</ul>
		{/if}
		{#if spec.withheld?.length}
			<h3>Withheld</h3>
			<ul class="refs">
				{#each spec.withheld as w, i (i)}
					<li><span>{w.what}</span><span class="muted">{w.reason}</span></li>
				{/each}
			</ul>
		{/if}
	</div>
</aside>

<style>
	/* plate language (D997): no edge bars or shadows; a top rule, display title, serif prose, small-caps kickers,
	   booktabs tables (2px top, 1px bottom, hairline rows, no vertical rules) */
	.pp { position: absolute; top: 0; right: 0; bottom: 0; width: min(380px, 100%); display: grid; grid-template-rows: auto minmax(0, 1fr); background: var(--surface); border-left: 1px solid var(--border); z-index: 6; }
	.head { display: flex; align-items: center; gap: 6px; padding: 6px 12px; border-bottom: 1px solid var(--line); }
	.kind { font: 600 13px var(--text, inherit); font-variant-caps: all-small-caps; letter-spacing: 0.07em; color: var(--muted, var(--ink-3)); }
	.grow { flex: 1; }
	.body { overflow-y: auto; padding: 12px 14px 20px; font: 14px/1.45 var(--text, inherit); }
	h2 { margin: 0 0 4px; font: 500 24px/1.15 var(--display, inherit); }
	h3 { margin: 16px 0 4px; font: 600 13px var(--text, inherit); font-variant-caps: all-small-caps; letter-spacing: 0.07em; color: var(--muted, var(--ink-3)); }
	p { margin: 0 0 6px; }
	.role { color: var(--ink-2); font-style: italic; }
	.note { font-size: 12.5px; color: var(--ink-3); line-height: 1.45; }
	blockquote { margin: 10px 0 4px; padding: 6px 10px; background: color-mix(in srgb, var(--accent) 8%, transparent); color: var(--ink-2); font-style: italic; }
	.loc { font: 12px var(--text, inherit); color: var(--ink-3); }
	table { width: 100%; border-collapse: collapse; border-top: 2px solid var(--muted, var(--ink-3)); border-bottom: 1px solid var(--muted, var(--ink-3)); font-variant-numeric: lining-nums tabular-nums; }
	td { padding: 4px 6px 4px 0; border-bottom: 1px solid var(--grid); vertical-align: top; }
	tr:last-child td { border-bottom: 0; }
	td.v { white-space: nowrap; }
	.b { font: 600 12px var(--text, inherit); font-variant-caps: all-small-caps; letter-spacing: 0.06em; color: var(--ink-3); background: var(--surface-2); padding: 0 5px; }
	tr.assumed .b { color: var(--amber, var(--warn)); background: color-mix(in srgb, var(--amber, var(--warn)) 14%, transparent); }
	.refs { margin: 0; padding: 0; list-style: none; }
	.refs li { display: flex; flex-direction: column; gap: 1px; padding: 5px 0; border-bottom: 1px solid var(--grid); overflow-wrap: anywhere; }
	@media (max-width: 700px) {
		.pp { top: auto; height: 70%; width: 100%; }
	}
</style>
