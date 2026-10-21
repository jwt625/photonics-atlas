<script lang="ts">
	// Component layout viewer (DevLog-005 D103-D108, D112). ?id=<component_id>: full-size top view, cross-section and
	// dimension table. No id: gallery of showcase components per template. Query parameters are read client-side only.
	import { onMount } from 'svelte';
	import { afterNavigate } from '$app/navigation';
	import { comp, fmtValue, loadComponents, type Metric } from '../../lib/components.svelte';
	import { link } from '../../lib/paths';
	import { gallery } from '../../lib/layout/gallery';
	import LayoutViews from '../../lib/layout/LayoutViews.svelte';
	import { buildScenes } from '../../lib/layout/scene';
	import Scene from '../../lib/layout/Scene.svelte';
	import { primaryMetric, resolve, rowLabel, unitLabel, type Dim } from '../../lib/layout/resolve';

	let id = $state('');
	const readId = () => (id = new URLSearchParams(location.search).get('id') ?? '');
	onMount(() => {
		loadComponents();
		readId();
	});
	afterNavigate(readId);

	const view = $derived(comp.view);
	const c = $derived(view && id ? view.components.find((x) => x.component_id === id) : undefined);
	const r = $derived(c && view ? resolve(c, view) : null);
	const prim = $derived(r && c ? primaryMetric(c, r.templateId, r.template) : null);
	const show = $derived(view && c ? (view.showcase ?? []).filter((s) => s.component_id === c.component_id) : []);
	const groups = $derived(view && !id ? gallery(view) : []);
	const dims = $derived(r ? Object.values(r.dims).sort((a, b) => Number(b.required) - Number(a.required) || (a.row ? 0 : 1) - (b.row ? 0 : 1)) : []);
	const href = (cid: string) => link('/layout') + '?id=' + encodeURIComponent(cid);
	const primText = (m: Metric | null, scopeMatch = true) => (m ? rowLabel(m) + (scopeMatch ? '' : ' (' + (m.scope ?? 'no scope') + ')') : 'not reported');
	const tipRow = (m: Metric) => [m.basis, m.scope, m.statistic, m.condition, 'locator ' + m.locator, m.notes].filter(Boolean).join('\n');
	const altTip = (d: Dim) => d.alts.map((a) => `${rowLabel(a)} [${a.basis}] ${a.condition ?? ''} (${a.locator})`).join('\n');
</script>

{#if comp.error}
	<div class="err">{comp.error}</div>
{:else if !view}
	<div class="pad muted">loading</div>
{:else if id}
	<div class="page">
		{#if !c}
			<p class="muted">No component <span class="mono">{id}</span>. <a href={link('/layout')}>Gallery</a></p>
		{:else if !r}
			<p class="muted">Class <span class="mono">{c.class}</span> has no layout template. <a href={link('/components') + '#' + encodeURIComponent(c.component_id)}>Component</a></p>
		{:else}
			<header class="hd">
				<div class="crumbs"><a href={link('/layout')}>Layout gallery</a> / <span class="mono">{r.templateId}</span></div>
				<h1>{c.label}</h1>
				<div class="meta">
					<span class="mono">{c.component_id}</span>
					<span>{c.class}</span>
					{#if c.platform}<span data-tip={[c.core_material, c.cladding && 'cladding: ' + c.cladding].filter(Boolean).join('\n')}>{c.platform}</span>{/if}
					<span data-tip={r.template.applies_to.join('\n')}>{r.template.label}</span>
					{#each show as s}<span class="role {s.role}" data-tip={[s.criterion, s.rationale, s.selected_on].filter(Boolean).join('\n')}>{s.role}</span>{/each}
					<a href={link('/components') + '#' + encodeURIComponent(c.component_id)}>all values</a>
					{#if c.source.url}<a href={c.source.url} target="_blank" rel="noopener" data-tip={c.source.title}>source ({c.source.year})</a>{:else}<span data-tip={c.source.title}>{c.source.id}</span>{/if}
				</div>
				{#if prim}
					<div class="prim">
						<span class="k" data-tip={view.parameters[prim.param]?.def ?? ''}>{prim.param}{r.template.primary.scope ? ' (' + r.template.primary.scope + ')' : ''}</span>
						<span class="v" class:nr={!prim.row} data-tip={prim.row ? tipRow(prim.row) + (prim.scopeMatch ? '' : '\nno row with the template scope: best row of another scope shown') : 'no row with this parameter'}>{primText(prim.row, prim.scopeMatch)}</span>
						{#if prim.row}<span class="muted">{prim.row.basis}{prim.n > 1 ? ', best of ' + prim.n + ' rows' : ''}</span>{/if}
						{#each prim.companions as cp}<span class="k">{cp.param}</span><span class="v" data-tip={tipRow(cp.row)}>{rowLabel(cp.row)}</span>{/each}
					</div>
				{/if}
			</header>
			<LayoutViews comp={c} {view} height={380} />
			<div class="lower">
				<section>
					<h3>Dimensions <span class="muted num">{r.reported} / {r.total} reported</span></h3>
					<table class="t num">
						<thead><tr><th>parameter</th><th>view</th><th>req</th><th class="r">value</th><th>basis</th><th>stat</th><th>condition</th><th>locator</th><th class="r">rows</th></tr></thead>
						<tbody>
							{#each dims as d}
								<tr class:miss={!d.row} data-tip={d.tip}>
									<td data-tip={view.parameters[d.param]?.def ?? ''}>{d.param}</td>
									<td>{d.views.join(', ')}</td>
									<td>{d.required ? 'yes' : ''}</td>
									<td class="r">{d.row ? fmtValue(d.row) + ' ' + unitLabel(d.row.unit) : 'not reported'}</td>
									<td>{d.row?.basis ?? ''}</td>
									<td>{d.row?.statistic ?? ''}</td>
									<td class="cond">{d.row?.condition ?? ''}</td>
									<td>{d.row?.locator ?? ''}</td>
									<td class="r" data-tip={altTip(d)}>{d.row ? 1 + d.alts.length : d.alts.length || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</section>
				<section>
					<h3>Not reported</h3>
					{#if r.missingRequired.length}<p><span class="warn">required:</span> <span class="mono">{r.missingRequired.join(', ')}</span></p>{/if}
					{#if r.missingOptional.length}<p><span class="muted">optional:</span> <span class="mono">{r.missingOptional.join(', ')}</span></p>{/if}
					{#if !r.missingRequired.length && !r.missingOptional.length}<p class="muted">none</p>{/if}
					<p class="muted small">Not-reported dimensions are drawn dashed at a fixed proportion of a reported neighbour and never labelled with a number. Labels marked * have further rows (hover).</p>
				</section>
			</div>
		{/if}
	</div>
{:else}
	<div class="page">
		<header class="hd">
			<h1>Component layouts</h1>
			<p class="muted small">
				{#if groups.some((g) => g.fallback)}<span class="warn">Fallback: no showcase rows yet. Cards are the components with the most reported template dimensions per template.</span>{:else}Showcase components per template (hero: best measured primary metric with a drawable geometry; typical: foundry / PDK or median performer).{/if}
			</p>
		</header>
		{#each groups as g}
			<section class="grp">
				<h2>
					<span>{g.t.label}</span>
					<span class="mono muted">{g.id}</span>
					<span class="muted num" data-tip="components whose class the template serves / with at least one template dimension">{g.served} components, {g.withGeometry} with geometry</span>
					<span class="muted" data-tip="primary metric (D107)">{g.t.primary.parameter}{g.t.primary.scope ? ' ' + g.t.primary.scope : ''}</span>
				</h2>
				<div class="cards">
					{#each g.cards as cd (cd.c.component_id + cd.role)}
						{@const sc = buildScenes(cd.r)}
						<a class="card" href={href(cd.c.component_id)} data-tip={[cd.c.label, cd.show?.criterion, cd.show?.rationale].filter(Boolean).join('\n')}>
							<div class="ch">
								<span class="role {cd.role}">{cd.role}</span>
								<span class="lbl">{cd.c.label}</span>
							</div>
							<Scene scene={cd.r.templateId === 'waveguide_xsec' ? sc.xsec : sc.top} height={96} thumb />
							<div class="cf">
								<span class="muted">{cd.c.platform ?? ''}</span>
								<span class="pv" class:nr={!cd.primary.row}>{primText(cd.primary.row, cd.primary.scopeMatch)}{#if cd.primary.row}<span class="bs">{cd.primary.row.basis}</span>{/if}</span>
								<span class="muted num" data-tip="template dimensions reported / total">{cd.r.reported}/{cd.r.total}</span>
							</div>
						</a>
					{/each}
					{#each g.gaps as gap}
						<div class="card gap" data-tip="D112: no source in the atlas reports the required dimensions together with a measured primary metric for this role">
							<div class="ch"><span class="role {gap}">{gap}</span><span class="lbl">no {gap} component</span></div>
							<div class="gapbody">not selected: no qualifying source</div>
						</div>
					{/each}
				</div>
			</section>
		{/each}
	</div>
{/if}

<style>
	.page { height: 100%; overflow: auto; padding: 10px 14px 24px; }
	.pad { padding: 12px; }
	.err { padding: 12px; color: var(--crit); }
	.hd { margin-bottom: 8px; }
	h1 { margin: 2px 0 4px; font-size: 15px; font-weight: 600; }
	h2 { display: flex; align-items: baseline; gap: 10px; margin: 0 0 6px; font-size: 12px; font-weight: 600; }
	h3 { margin: 10px 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	.crumbs { font-size: 11px; color: var(--ink-3); }
	.meta { display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 11px; color: var(--ink-2); }
	.prim { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 8px; margin-top: 6px; font-size: 12px; }
	.prim .k { color: var(--ink-3); font-family: var(--mono); font-size: 11px; }
	.prim .v { font-weight: 600; }
	.nr { color: var(--warn); font-style: italic; }
	.warn { color: var(--warn); }
	.small { font-size: 11px; }
	.mono { font-family: var(--mono); }
	.role { font: 600 9px/14px var(--mono); padding: 0 4px; border: 1px solid var(--line); color: var(--ink-3); text-transform: uppercase; }
	.role.hero { color: var(--accent); border-color: var(--accent); }
	.role.typical { color: var(--good); border-color: var(--good); }
	.role.fallback { color: var(--warn); border-color: var(--warn); }
	.lower { display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 1fr); gap: 16px; }
	@media (max-width: 1000px) { .lower { grid-template-columns: minmax(0, 1fr); } }
	table.t { border-collapse: collapse; width: 100%; }
	.t th, .t td { padding: 2px 6px; border-bottom: 1px solid var(--grid); text-align: left; white-space: nowrap; }
	.t th { color: var(--ink-3); font-weight: 500; }
	.t .r { text-align: right; }
	.t td.cond { white-space: normal; max-width: 260px; color: var(--ink-2); }
	.t tr.miss td { color: var(--ink-3); }
	.t tr.miss td:nth-child(4) { color: var(--warn); font-style: italic; }
	.t tbody tr:hover { background: var(--hover); }
	p { margin: 4px 0; }
	.grp { margin: 12px 0 16px; }
	.cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 8px; }
	.card { display: flex; flex-direction: column; gap: 3px; padding: 6px; background: var(--surface); border: 1px solid var(--border); color: var(--ink); min-width: 0; }
	.card:hover { text-decoration: none; border-color: var(--accent); }
	.ch { display: flex; align-items: center; gap: 6px; min-width: 0; }
	.ch .lbl { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 11px; }
	.cf { display: flex; gap: 8px; align-items: baseline; font-size: 11px; }
	.cf .pv { flex: 1; text-align: right; font-weight: 600; }
	.bs { margin-left: 4px; font-weight: 400; color: var(--ink-3); font-size: 10px; }
	.card.gap { border-style: dashed; background: transparent; }
	.gapbody { height: 96px; display: flex; align-items: center; justify-content: center; color: var(--ink-3); font-size: 11px; border: 1px dashed var(--grid); }
</style>
