<script lang="ts">
	// People view (DevLog-010 D190, D192, D196, D197). Public persons and public observations only (people.json); dated
	// points, never intervals, no moves or flows. Hash state: m (persons / orgs / coverage), p (person id), org.
	import { onMount } from 'svelte';
	import { link } from '../../lib/paths';
	import { store, ui } from '../../lib/state.svelte';
	import { loadPeople, ppl, type Obs } from '../../lib/people.svelte';
	import { plotTheme, slotColor } from '../../lib/explore/colors';
	import Plot from '../../lib/explore/Plot.svelte';
	import StackBars from '../../lib/StackBars.svelte';
	import { coverage, dateNum, orgPeople, orgTable, personStats, typeOf } from '../../lib/views';
	import { provenance, pubTip } from '../../lib/pub';

	type Mode = 'persons' | 'orgs' | 'coverage';
	let mode = $state<Mode>('persons');
	let pid = $state('');
	let org = $state('');
	let q = $state('');
	let qLive = $state('');
	let sortKey = $state<'name' | 'n' | 'first' | 'last' | 'orgs'>('n');
	let sortDir = $state<1 | -1>(-1);
	let limit = $state(300);
	let timer: ReturnType<typeof setTimeout> | null = null;

	function readHash() {
		const p = new URLSearchParams(location.hash.slice(1));
		const m = p.get('m');
		mode = m === 'orgs' || m === 'coverage' ? m : 'persons';
		pid = p.get('p') ?? '';
		org = p.get('org') ?? '';
	}
	function writeHash() {
		const p = new URLSearchParams();
		if (mode !== 'persons') p.set('m', mode);
		if (pid) p.set('p', pid);
		if (org) p.set('org', org);
		const h = p.toString();
		history.replaceState(history.state, '', h ? '#' + h : location.pathname + location.search);
	}
	onMount(() => {
		loadPeople();
		readHash();
		addEventListener('hashchange', readHash);
		return () => removeEventListener('hashchange', readHash);
	});
	function onInput(v: string) {
		qLive = v;
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => ((q = v), (limit = 300)), 300);
	}
	function setMode(m: Mode) {
		mode = m;
		q = qLive = '';
		limit = 300;
		writeHash();
	}
	function pick(id: string) {
		pid = id;
		writeHash();
	}
	function pickOrg(id: string) {
		org = id;
		writeHash();
	}
	function sortBy(k: typeof sortKey) {
		if (sortKey === k) sortDir = sortDir === 1 ? -1 : 1;
		else {
			sortKey = k;
			sortDir = k === 'name' ? 1 : -1;
		}
		limit = 300;
	}
	function onScroll(e: Event) {
		const el = e.currentTarget as HTMLElement;
		if (el.scrollTop + el.clientHeight > el.scrollHeight - 400) limit += 300;
	}

	const view = $derived(ppl.view);
	const name = (id: string) => store.byId.get(id)?.name ?? id;
	const fold = (s: string) => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase();
	const stats = $derived(view ? personStats(view) : []);
	const plist = $derived.by(() => {
		if (!view) return [];
		const f = fold(q);
		const rows = view.persons.filter((p) => !f || fold(p.name).includes(f) || p.id.includes(f) || (p.orcid && p.orcid.includes(f)));
		const key = (i: number): string | number => {
			const s = stats[i];
			if (sortKey === 'name') return fold(view.persons[i].name);
			if (sortKey === 'first' || sortKey === 'last') return s[sortKey] ? dateNum(s[sortKey]) : 0;
			return s[sortKey];
		};
		return rows.sort((a, b) => {
			const x = key(a.i), y = key(b.i);
			return x === y ? a.name.localeCompare(b.name) : x < y ? -sortDir : sortDir;
		});
	});
	const person = $derived(view && pid ? view.persons.find((p) => p.id === pid) : undefined);
	const pobs = $derived(view && person ? [...view.byPerson[person.i]].sort((a, b) => dateNum(b.active_on) - dateNum(a.active_on) || a.obs_id.localeCompare(b.obs_id)) : []);

	// timeline (D196)
	const th = $derived(plotTheme(ui.theme));
	// D199k: colour = publication type (slots in the alphabetical order of all types present: identity, not rank)
	const allTypes = $derived(view ? [...new Set(view.obs.map((o) => typeOf(view.sources, o.source_id)))].sort() : []);
	const typeColor = (t: string) => slotColor(allTypes.indexOf(t), ui.theme);
	const trunc40 = (s: string) => trunc(s, 40);
	const orgFull = (o: Obs) => (o.org_id ? name(o.org_id) : o.printed_org + ' (as printed)');
	// y tick labels truncated so long unmapped printed strings do not squeeze the plot (full string in the hover)
	const orgLabel = (o: Obs) => trunc40(orgFull(o));
	// observations sharing one marker (same org and date, e.g. year-only rows of several papers)
	const stack = $derived.by(() => {
		const m = new Map<string, number>();
		for (const o of pobs) m.set(orgLabel(o) + '|' + o.active_on, (m.get(orgLabel(o) + '|' + o.active_on) ?? 0) + 1);
		return m;
	});
	const yCats = $derived.by(() => {
		// organizations ordered by first observation (top = earliest)
		const first = new Map<string, number>();
		for (const o of pobs) {
			const k = orgLabel(o), d = dateNum(o.active_on);
			if (!first.has(k) || d < (first.get(k) as number)) first.set(k, d);
		}
		return [...first].sort((a, b) => a[1] - b[1] || a[0].localeCompare(b[0])).map((x) => x[0]);
	});
	const tip = (o: Obs) => {
		const s = view?.sources[o.source_id] ?? {};
		return [
			`<b>${esc(orgFull(o))}</b>`,
			...((stack.get(orgLabel(o) + '|' + o.active_on) ?? 1) > 1 ? [`${stack.get(orgLabel(o) + '|' + o.active_on)} affiliations at this point`] : []),
			`${o.active_on}${o.active_on.length === 4 ? ' (year only)' : ''}; ${provenance(o.grade)}${o.aff_role !== 'primary' ? '; ' + o.aff_role.replace(/_/g, ' ') : ''}`,
			`printed: ${esc(o.printed_org)}${o.unit ? '; ' + esc(o.unit) : ''}`,
			`${esc(trunc(s.title ?? '', 70))}`,
			`${esc([s.venue, s.year].filter(Boolean).join(', '))}${o.locator ? '; ' + esc(o.locator) : ''}`
		].join('<br>');
	};
	const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
	const trunc = (s: string, n: number) => (s.length > n ? s.slice(0, n - 1) + '...' : s);
	const traces = $derived(
		[...new Set(pobs.map((o) => typeOf(view?.sources ?? {}, o.source_id)))].sort().map((t) => {
			const os = pobs.filter((o) => typeOf(view?.sources ?? {}, o.source_id) === t);
			return {
				type: 'scatter',
				mode: 'markers',
				name: t,
				x: os.map((o) => dateNum(o.active_on)),
				y: os.map(orgLabel),
				text: os.map(tip),
				hovertemplate: '%{text}<extra></extra>',
				marker: { color: typeColor(t), size: 10, symbol: 'circle', line: { color: th.surface, width: 1 } }
			};
		})
	);
	const xs = $derived(pobs.map((o) => dateNum(o.active_on)));
	const tlHeight = $derived(Math.max(150, Math.min(360, 70 + yCats.length * 26)));
	const tlLayout = $derived({
		paper_bgcolor: 'rgba(0,0,0,0)',
		plot_bgcolor: 'rgba(0,0,0,0)',
		margin: { l: 8, r: 10, t: 6, b: 6 },
		font: { family: 'system-ui, sans-serif', size: 11, color: th.ink2 },
		showlegend: true,
		legend: { orientation: 'h', x: 0, y: 1.02, yanchor: 'bottom', font: { size: 10, color: th.ink2 }, bgcolor: 'rgba(0,0,0,0)' },
		hovermode: 'closest',
		hoverlabel: { bgcolor: th.surface, bordercolor: th.line, font: { color: th.ink, size: 11 }, align: 'left' },
		xaxis: {
			title: { text: 'Date (year)', standoff: 4, font: { size: 11, color: th.ink2 } },
			range: xs.length ? [Math.floor(Math.min(...xs)) - 0.5, Math.ceil(Math.max(...xs)) + 0.5] : undefined,
			dtick: xs.length && Math.max(...xs) - Math.min(...xs) > 12 ? 2 : 1,
			tickformat: 'd',
			gridcolor: th.grid,
			linecolor: th.line,
			tickfont: { size: 10 },
			automargin: true,
			zeroline: false
		},
		yaxis: { type: 'category', categoryorder: 'array', categoryarray: [...yCats].reverse(), automargin: true, tickfont: { size: 10, color: th.ink }, gridcolor: th.grid, linecolor: th.line }
	});

	// orgs mode
	const otab = $derived(view ? orgTable(view) : new Map<string, { persons: number; obs: number }>());
	const olist = $derived.by(() => {
		const f = fold(q);
		return [...otab]
			.filter(([id]) => !f || fold(name(id)).includes(f) || id.includes(f))
			.sort((a, b) => b[1].persons - a[1].persons || name(a[0]).localeCompare(name(b[0])));
	});
	const opeople = $derived(view && org ? orgPeople(view, org) : []);
	const unmappedObs = $derived(view ? view.obs.filter((o) => !o.org_id).length : 0);

	// coverage (D197)
	const cov = $derived(view ? coverage(view.obs, view.sources) : null);
	const covSeries = $derived(cov ? cov.types.map((t) => ({ key: t, name: t, color: typeColor(t), y: cov.byYear.get(t) ?? [] })) : []);
	const pubsByType = $derived.by(() => {
		const m = new Map<string, Set<string>>();
		for (const o of view?.obs ?? []) {
			const t = typeOf(view?.sources ?? {}, o.source_id);
			if (!m.has(t)) m.set(t, new Set());
			(m.get(t) as Set<string>).add(o.source_id);
		}
		return new Map([...m].map(([k, v]) => [k, v.size]));
	});
	const withheld = $derived(view ? view.counts.obs_all - view.counts.obs_public : 0);
</script>

{#if ppl.error}
	<div class="err">{ppl.error}</div>
{:else if view}
	<div class="page">
		<div class="main">
			<div class="bar">
				<span class="seg tabs">
					<button class:on={mode === 'persons'} onclick={() => setMode('persons')}>Persons</button><button class:on={mode === 'orgs'} onclick={() => setMode('orgs')}>Organizations</button><button class:on={mode === 'coverage'} onclick={() => setMode('coverage')}>Coverage</button>
				</span>
				{#if mode !== 'coverage'}
					<input type="search" placeholder={mode === 'persons' ? 'Search name or ORCID' : 'Search organization'} value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
				{:else}
					<div class="grow"></div>
				{/if}
				<span class="muted num" data-tip="Authors and their published affiliations from public professional sources. Affiliations of authors whose identity is under review are not shown.">
					{#if mode === 'persons'}{plist.length} / {view.counts.persons_public} people{:else if mode === 'orgs'}{olist.length} orgs{:else}{view.counts.obs_public} affiliations{/if}
				</span>
			</div>
			{#if mode === 'persons'}
				<div class="scroll" onscroll={onScroll}>
					<table class="t num">
						<thead>
							<tr>
								{#each [['name', 'Person', 'Display name'], ['n', 'Affiliations', 'Published affiliations of the person'], ['first', 'First', 'Earliest publication date'], ['last', 'Last', 'Latest publication date'], ['orgs', 'Orgs', 'Distinct organizations']] as [k, l, t]}
									<th class:r={k !== 'name'} data-tip={t} onclick={() => sortBy(k as typeof sortKey)}>{l}{sortKey === k ? (sortDir === 1 ? ' ^' : ' v') : ''}</th>
								{/each}
							</tr>
						</thead>
						<tbody>
							{#each plist.slice(0, limit) as p (p.id)}
								{@const s = stats[p.i]}
								<tr class:sel={p.id === pid} onclick={() => pick(p.id)}>
									<td class="name">{p.name}</td><td class="r">{#if s.n}{s.n}{:else if p.lin_grade}<span class="muted" data-tip="listed in a curated career-lineage record; no published affiliation in the atlas">lineage</span>{/if}</td><td class="r">{s.first}</td><td class="r">{s.last}</td><td class="r">{s.orgs || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
					{#if !plist.length}<p class="muted pad">No person matches.</p>{/if}
				</div>
			{:else if mode === 'orgs'}
				<div class="scroll" onscroll={onScroll}>
					<table class="t num">
						<thead><tr><th>Organization</th><th>Type</th><th>CC</th><th class="r" data-tip="people with a published affiliation at the organization">People</th><th class="r" data-tip="published affiliations">Affiliations</th></tr></thead>
						<tbody>
							{#each olist.slice(0, limit) as [id, n] (id)}
								{@const o = store.byId.get(id)}
								<tr class:sel={id === org} onclick={() => pickOrg(id)}>
									<td class="name">{name(id)}</td><td>{(o?.type ?? '').replace(/_/g, ' ')}</td><td>{o?.country ?? ''}</td><td class="r">{n.persons}</td><td class="r">{n.obs}</td>
								</tr>
							{/each}
						</tbody>
					</table>
					{#if !olist.length}<p class="muted pad">No organization matches.</p>{/if}
				</div>
			{:else if cov}
				<div class="scroll cov">
					<StackBars
						letter="a"
						desc="Published author affiliations per publication year, stacked by publication type"
						badge={`${view.counts.obs_public}`}
						badgeTip={`${view.counts.obs_public} affiliations shown; ${withheld} more are not shown while the author's identity is under review`}
						years={cov.years}
						series={covSeries}
						xTitle="Publication year"
						yTitle="Affiliations (count)"
						unit="affiliations"
						height={320}
					/>
					<table class="t num grid">
						<thead><tr><th>publication type</th><th class="r" data-tip="affiliation printed in the publication">printed</th><th class="r" data-tip="affiliation taken from the conference program listing">program listing</th><th class="r">affiliations</th><th class="r" data-tip="distinct publications">publications</th></tr></thead>
						<tbody>
							{#each cov.types as t}
								<tr><td>{t}</td><td class="r">{cov.byGrade.get(`${t}|A`) ?? ''}</td><td class="r">{cov.byGrade.get(`${t}|B`) ?? ''}</td><td class="r">{(cov.byYear.get(t) ?? []).reduce((x, y) => x + y, 0)}</td><td class="r">{pubsByType.get(t) ?? ''}</td></tr>
							{/each}
						</tbody>
					</table>
					<p class="muted small">{view.counts.persons_public} people. {unmappedObs} affiliations name an organization not yet in the organization list (shown as printed). {withheld} affiliations are not shown while the author's identity is under review.</p>
				</div>
			{/if}
		</div>
		<aside class="detail">
			{#if mode === 'persons' && person}
				<h2>{person.name}</h2>
				<div class="meta">
					{#if person.orcid}<a href="https://orcid.org/{person.orcid}" target="_blank" rel="noopener">ORCID {person.orcid}</a>{/if}
					{#if person.disambiguator}<span class="muted">{person.disambiguator}</span>{/if}
				</div>
				{#if pobs.length}
					<div class="tl" style:height="{tlHeight}px"><Plot data={traces} layout={tlLayout} /></div>
					<h3>Affiliations ({pobs.length})</h3>
					<table class="t num">
						<thead><tr><th>date</th><th>organization</th><th>publication</th></tr></thead>
						<tbody>
							{#each pobs as o (o.obs_id)}
								{@const s = view.sources[o.source_id] ?? {}}
								<tr data-tip={['name as printed: ' + o.printed_name, 'organization as printed: ' + o.printed_org, o.unit && 'unit: ' + o.unit, o.country && 'country: ' + o.country, provenance(o.grade)].filter(Boolean).join('\n')}>
									<td class="nw">{o.active_on}</td>
									<td>{#if o.org_id}<a href={link('/orgs/hub') + '?id=' + encodeURIComponent(o.org_id)}>{name(o.org_id)}</a>{:else}<span class="muted">{o.printed_org}</span>{/if}{#if o.aff_role !== 'primary'}<span class="muted role">({o.aff_role.replace(/_/g, ' ')})</span>{/if}</td>
									<td class="pubc" data-tip={pubTip(s, o.locator)}>{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title ?? ''}</a>{:else}{s.title ?? ''}{/if}{#if s.atlas} <a class="sib" href={s.atlas[1]} target="_blank" rel="noopener" data-tip="Open in the {s.atlas[0]}">atlas</a>{/if}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{:else}
					<p class="muted">No published affiliation in the atlas.</p>
				{/if}
				{#if person.lin_grade}
					<h3>Career lineage record</h3>
					<p class="small">Listed in a curated career-lineage record, from these public sources:</p>
					<ul class="small">
						{#each person.lin_sources.split(';').filter(Boolean) as sid}
							{@const s = view.sources[sid] ?? {}}
							<li>{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title}</a>{:else}{s.title}{/if} <span class="muted">{[s.type, s.year].filter(Boolean).join(', ')}</span></li>
						{/each}
					</ul>
				{/if}
			{:else if mode === 'orgs' && org}
				<h2>{name(org)} <a class="hub" href={link('/orgs/hub') + '?id=' + encodeURIComponent(org)}>hub</a></h2>
				<div class="meta muted">{opeople.length} people, {otab.get(org)?.obs ?? 0} published affiliations</div>
				<table class="t num">
					<thead><tr><th>person</th><th class="r">affiliations</th><th class="r">first</th><th class="r">last</th></tr></thead>
					<tbody>
						{#each opeople as op (op.person.id)}
							<tr class="click" onclick={() => ((mode = 'persons'), pick(op.person.id))}><td>{op.person.name}</td><td class="r">{op.n}</td><td class="r">{op.first}</td><td class="r">{op.last}</td></tr>
						{/each}
					</tbody>
				</table>
			{:else if mode === 'coverage'}
				<h3>What is shown</h3>
				<ul class="small">
					<li>An affiliation is what a publication prints for an author (or, for some conference papers, what the conference program lists), dated by the publication or session date. It is a dated point, not an employment period.</li>
					<li>Only public professional sources are used. Affiliations of authors whose identity is still under review are not shown.</li>
				</ul>
			{:else}
				<p class="muted">{mode === 'persons' ? 'Select a person.' : 'Select an organization.'}</p>
			{/if}
		</aside>
	</div>
{:else}
	<div class="pad muted">loading</div>
{/if}

<style>
	.page { height: 100%; display: grid; grid-template-columns: minmax(0, 1fr) 520px; grid-template-rows: minmax(0, 1fr); }
	.main { min-width: 0; min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr); border-right: 1px solid var(--border); }
	.bar { display: flex; gap: 6px; align-items: center; padding: 6px 8px; background: var(--surface); border-bottom: 1px solid var(--border); min-width: 0; }
	.bar input { flex: 1; min-width: 80px; }
	.bar > .muted { white-space: nowrap; }
	.grow { flex: 1; }
	.tabs button { height: 24px; font-size: 12px; padding: 0 10px; }
	.scroll { overflow: auto; min-height: 0; }
	.cov { padding: 8px; display: flex; flex-direction: column; gap: 8px; }
	.cov > :global(*) { flex: none; }
	.pad { padding: 12px; }
	table.t { border-collapse: collapse; width: 100%; }
	.t th, .t td { padding: 2px 6px; border-bottom: 1px solid var(--grid); text-align: left; white-space: nowrap; }
	.t th { position: sticky; top: 0; background: var(--surface); color: var(--ink-3); font-weight: 500; cursor: pointer; user-select: none; }
	.t .r { text-align: right; }
	.t td.name { max-width: 360px; overflow: hidden; text-overflow: ellipsis; }
	.main .t tbody tr, .t tr.click { cursor: pointer; }
	.t tbody tr:hover { background: var(--hover); }
	.t tbody tr.sel { background: var(--sel); }
	.t.grid { width: auto; background: var(--surface); border: 1px solid var(--border); }
	.t.grid th { position: static; cursor: default; }
	.detail { min-height: 0; overflow: auto; padding: 8px 10px; background: var(--surface); }
	.detail .t th { position: static; cursor: default; }
	.detail .t td { white-space: normal; }
	.detail .t td.nw { white-space: nowrap; }
	.tl { margin: 6px 0 4px; }
	h2 { margin: 0 0 4px; font-size: 14px; }
	h2 .hub { font-size: 11px; font-weight: 400; margin-left: 6px; }
	h3 { margin: 10px 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	.meta { display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 11px; }
	.small { font-size: 11px; }
	.sib { font-size: 10px; margin-left: 4px; }
	.detail .t td.pubc { min-width: 180px; }
	.role { margin-left: 4px; }
	ul { margin: 0; padding-left: 16px; }
	.err { padding: 12px; color: var(--crit); }
	@media (max-width: 1100px) { .page { grid-template-columns: minmax(0, 1fr) 400px; } }
	@media (max-width: 900px) {
		.page { grid-template-columns: minmax(0, 1fr); grid-template-rows: minmax(0, 1fr) 50%; }
		.main { border-right: none; }
		.detail { border-top: 1px solid var(--border); }
		.bar > .muted { display: none; }
	}
</style>
