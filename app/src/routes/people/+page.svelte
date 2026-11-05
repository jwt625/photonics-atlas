<script lang="ts">
	// People view (DevLog-010 D190, D192, D196, D197). Public persons and public observations only (people.json); dated
	// points, never intervals, no moves or flows. Hash state: m (persons / orgs / coverage), p (person id), org.
	import { onMount } from 'svelte';
	import { link } from '../../lib/paths';
	import { store, ui } from '../../lib/state.svelte';
	import { loadPeople, ppl, type Obs } from '../../lib/people.svelte';
	import { plotTheme, slotColor } from '../../lib/explore/colors';
	import Plot from '../../lib/explore/Plot.svelte';
	import Preload from '../../lib/Preload.svelte';
	import Chips from '../../lib/table/Chips.svelte';
	import DataTable from '../../lib/table/DataTable.svelte';
	import { dateYear, type Col, type Filters, type Sort } from '../../lib/table/filters';
	import type { Summary } from '../../lib/types';
	import StackBars from '../../lib/StackBars.svelte';
	import { coverage, dateNum, orgPeople, orgTable, personStats, typeOf } from '../../lib/views';
	import { provenance, pubTip } from '../../lib/pub';

	let { data }: { data: { summary: Summary } } = $props();
	const files = $derived(['data/parts/people/meta.json', ...Array.from({ length: data.summary.parts.people }, (_, i) => `data/parts/people/${i}.json`)]);

	type Mode = 'persons' | 'orgs' | 'coverage';
	let mode = $state<Mode>('persons');
	let pid = $state('');
	let org = $state('');
	let q = $state('');
	let qLive = $state('');
	let pFilters = $state<Filters>({});
	let oFilters = $state<Filters>({});
	let pS = $state<Sort | null>(null);
	let oS = $state<Sort | null>(null);
	let aF = $state<Filters>({});
	let aS = $state<Sort | null>(null);
	let dF = $state<Filters>({});
	let dS = $state<Sort | null>(null);
	let cF = $state<Filters>({});
	let cS = $state<Sort | null>(null);
	let pShown = $state(0);
	let oShown = $state(0);
	// a deep link brings its row into view once; a row click never scrolls
	let revealP = $state('');
	let revealO = $state('');
	let timer: ReturnType<typeof setTimeout> | null = null;

	function readHash() {
		const p = new URLSearchParams(location.hash.slice(1));
		const m = p.get('m');
		mode = m === 'orgs' || m === 'coverage' ? m : 'persons';
		pid = p.get('p') ?? '';
		org = p.get('org') ?? '';
		revealP = pid;
		revealO = org;
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
		timer = setTimeout(() => (q = v), 300);
	}
	function setMode(m: Mode) {
		mode = m;
		q = qLive = '';
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
	// grows part by part (D500); what must be complete (coverage, totals) reads ppl.view
	const view = $derived(ppl.view ?? ppl.partial);
	const complete = $derived(!!ppl.view);
	const name = (id: string) => store.byId.get(id)?.name ?? id;
	const fold = (s: string) => s.normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase();
	const stats = $derived(view ? personStats(view) : []);
	// flat rows of the persons table: the head inlined in the page until the view is in (same order, so nothing moves)
	interface PRow {
		id: string;
		name: string;
		orcid?: string;
		lin?: string;
		n: number;
		first: string;
		last: string;
		orgs: number;
	}
	const head = $derived(data.summary.head.people);
	const headRows = $derived(head.rows.map((r) => ({ n: 0, first: '', last: '', orgs: 0, ...r }) as PRow));
	// the head rows keep their true numbers and places on top; others join as their rows arrive, with their count so far (a
	// count so far cannot pass a head row, so the head never moves); all persons once complete
	const headIds = $derived(new Set(head.rows.map((r) => r.id)));
	const prows = $derived.by<PRow[]>(() => {
		if (!view) return headRows;
		const all = view.persons.map((p, i) => ({ id: p.id, name: p.name, orcid: p.orcid, lin: p.lin_grade, n: stats[i].n, first: stats[i].first, last: stats[i].last, orgs: stats[i].orgs }));
		return complete ? all : [...headRows, ...all.filter((p) => p.n > 0 && !headIds.has(p.id))];
	});
	const plist = $derived.by(() => {
		const f = fold(q);
		return f ? prows.filter((p) => fold(p.name).includes(f) || p.id.includes(f) || (p.orcid && p.orcid.includes(f))) : prows;
	});
	const dateCol = (k: 'first' | 'last', label: string, tip: string): Col<PRow> => ({
		key: k,
		label,
		w: 96,
		tip: tip + ' (range filter in years)',
		kind: 'num',
		right: true,
		firstDir: -1,
		get: (p) => dateYear(p[k]),
		sort: (p) => (p[k] ? dateNum(p[k]) : null),
		text: (p) => p[k]
	});
	const pCols: Col<PRow>[] = [
		{ key: 'name', label: 'Person', kind: 'text', w: 300, tip: 'Display name', get: (p) => p.name },
		{ key: 'n', label: 'Affiliations', kind: 'num', w: 96, right: true, tip: 'Published affiliations of the person', get: (p) => p.n, cell: affCell },
		dateCol('first', 'First', 'Earliest publication date'),
		dateCol('last', 'Last', 'Latest publication date'),
		{ key: 'orgs', label: 'Orgs', kind: 'num', w: 64, right: true, tip: 'Distinct organizations', get: (p) => p.orgs, text: (p) => (p.orgs ? String(p.orgs) : '') }
	];
	const pSort: Sort = { key: 'n', dir: -1 };
	const pTie = (a: PRow, b: PRow) => a.name.localeCompare(b.name);
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
	interface ORow {
		id: string;
		name: string;
		type: string;
		country: string;
		persons: number;
		obs: number;
	}
	const olist = $derived.by<ORow[]>(() => {
		const f = fold(q);
		return [...otab]
			.filter(([id]) => !f || fold(name(id)).includes(f) || id.includes(f))
			.map(([id, n]) => {
				const o = store.byId.get(id);
				return { id, name: name(id), type: o?.type ?? '', country: o?.country ?? '', persons: n.persons, obs: n.obs };
			});
	});
	const oCols: Col<ORow>[] = [
		{ key: 'name', label: 'Organization', kind: 'text', cls: 'wide', get: (o) => o.name },
		{ key: 'type', label: 'Type', kind: 'enum', get: (o) => o.type, enumLabel: (v) => v.replace(/_/g, ' ') },
		{ key: 'country', label: 'CC', kind: 'enum', get: (o) => o.country },
		{ key: 'persons', label: 'People', kind: 'num', right: true, tip: 'people with a published affiliation at the organization', get: (o) => o.persons },
		{ key: 'obs', label: 'Affiliations', kind: 'num', right: true, tip: 'published affiliations', get: (o) => o.obs }
	];
	const oSort: Sort = { key: 'persons', dir: -1 };
	const oTie = (a: ORow, b: ORow) => a.name.localeCompare(b.name);
	const opeople = $derived(view && org ? orgPeople(view, org) : []);
	const unmappedObs = $derived(view ? view.obs.filter((o) => !o.org_id).length : 0);

	// coverage (D197)
	const cov = $derived(ppl.view ? coverage(ppl.view.obs, ppl.view.sources) : null);
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

	// secondary tables (D504)
	const aCols: Col<Obs>[] = [
		{ key: 'date', label: 'date', kind: 'num', w: 88, tip: 'Publication or session date (range filter in years)', get: (o) => dateYear(o.active_on), sort: (o) => dateNum(o.active_on), text: (o) => o.active_on },
		{ key: 'org', label: 'organization', kind: 'enum', w: 170, cls: 'wrap', get: orgFull, cell: obsOrgCell },
		{ key: 'pub', label: 'publication', kind: 'text', w: 230, cls: 'wrap', get: (o) => view?.sources[o.source_id]?.title, cellTip: (o) => pubTip(view?.sources[o.source_id] ?? {}, o.locator), cell: obsPubCell }
	];
	const aTip = (o: Obs) => ['name as printed: ' + o.printed_name, 'organization as printed: ' + o.printed_org, o.unit && 'unit: ' + o.unit, o.country && 'country: ' + o.country, provenance(o.grade)].filter(Boolean).join('\n');
	type OP = (typeof opeople)[number];
	const dCols: Col<OP>[] = [
		{ key: 'name', label: 'person', kind: 'text', w: 230, get: (p) => p.person.name },
		{ key: 'n', label: 'affiliations', kind: 'num', w: 92, right: true, get: (p) => p.n },
		{ key: 'first', label: 'first', kind: 'num', w: 88, right: true, tip: 'Range filter in years', get: (p) => dateYear(p.first), sort: (p) => dateNum(p.first), text: (p) => p.first },
		{ key: 'last', label: 'last', kind: 'num', w: 88, right: true, tip: 'Range filter in years', get: (p) => dateYear(p.last), sort: (p) => dateNum(p.last), text: (p) => p.last }
	];
	const dSort: Sort = { key: 'n', dir: -1 };
	const dTie = (a: OP, b: OP) => a.person.name.localeCompare(b.person.name);
	type CR = { t: string; a: number; b: number; n: number; pubs: number };
	const covRows = $derived<CR[]>(cov ? cov.types.map((t) => ({ t, a: cov.byGrade.get(`${t}|A`) ?? 0, b: cov.byGrade.get(`${t}|B`) ?? 0, n: (cov.byYear.get(t) ?? []).reduce((x, y) => x + y, 0), pubs: pubsByType.get(t) ?? 0 })) : []);
	const blank0 = (n: number) => (n ? String(n) : '');
	const cCols: Col<CR>[] = [
		{ key: 't', label: 'publication type', kind: 'enum', w: 180, get: (r) => r.t },
		{ key: 'a', label: 'printed', kind: 'num', w: 80, right: true, tip: 'affiliation printed in the publication', get: (r) => r.a, text: (r) => blank0(r.a) },
		{ key: 'b', label: 'program listing', kind: 'num', w: 120, right: true, tip: 'affiliation taken from the conference program listing', get: (r) => r.b, text: (r) => blank0(r.b) },
		{ key: 'n', label: 'affiliations', kind: 'num', w: 96, right: true, get: (r) => r.n },
		{ key: 'pubs', label: 'publications', kind: 'num', w: 96, right: true, tip: 'distinct publications', get: (r) => r.pubs, text: (r) => blank0(r.pubs) }
	];
</script>

<Preload {files} />

{#snippet obsOrgCell(o: Obs)}{#if o.org_id}<a href={link('/orgs/hub') + '?id=' + encodeURIComponent(o.org_id)}>{name(o.org_id)}</a>{:else}<span class="muted">{o.printed_org}</span>{/if}{#if o.aff_role !== 'primary'}<span class="muted role">({o.aff_role.replace(/_/g, ' ')})</span>{/if}{/snippet}
{#snippet obsPubCell(o: Obs)}{@const s = view?.sources[o.source_id] ?? {}}{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title ?? ''}</a>{:else}{s.title ?? ''}{/if}{#if s.atlas} <a class="sib" href={s.atlas[1]} target="_blank" rel="noopener" data-tip="Open in the {s.atlas[0]}">atlas</a>{/if}{/snippet}
{#snippet affCell(p: PRow)}{#if p.n}<span class:muted={!complete && !headIds.has(p.id)} data-tip={!complete && !headIds.has(p.id) ? 'so far; more rows are arriving' : undefined}>{p.n}</span>{:else if p.lin}<span class="muted" data-tip="listed in a curated career-lineage record; no published affiliation in the atlas">lineage</span>{/if}{/snippet}

{#if ppl.error}
	<div class="err">{ppl.error}</div>
{:else}
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
				{#if complete && view}
					<span class="muted num" data-tip="Authors and their published affiliations from public professional sources. Affiliations of authors whose identity is under review are not shown.">
						{#if mode === 'persons'}{pShown} / {view.counts.persons_public} people{:else if mode === 'orgs'}{oShown} orgs{:else}{view.counts.obs_public} affiliations{/if}
					</span>
				{:else}
					<span class="muted num" data-tip="Affiliation rows received; the table grows as they arrive and counts are final when all are in">{ppl.loaded} / {ppl.total || data.summary.overview.people.affiliations} affiliations loaded</span>
				{/if}
			</div>
			{#if mode === 'persons'}
				<Chips sets={[{ columns: pCols, filters: pFilters }]} onremove={(_, k) => { const n = { ...pFilters }; delete n[k]; pFilters = n; }} onclear={() => (pFilters = {})} />
				<DataTable columns={pCols} rows={plist} rowKey={(p) => p.id} selected={pid} onselect={pick} defaultSort={pSort} tie={pTie} bind:filters={pFilters} bind:sort={pS} bind:shown={pShown} reveal={revealP} onrevealed={() => (revealP = '')} empty={complete ? 'No person matches.' : ''} />
			{:else if mode === 'orgs'}
				<Chips sets={[{ columns: oCols, filters: oFilters }]} onremove={(_, k) => { const n = { ...oFilters }; delete n[k]; oFilters = n; }} onclear={() => (oFilters = {})} />
				<DataTable columns={oCols} rows={olist} rowKey={(o) => o.id} selected={org} onselect={pickOrg} defaultSort={oSort} tie={oTie} bind:filters={oFilters} bind:sort={oS} bind:shown={oShown} reveal={revealO} onrevealed={() => (revealO = '')} empty={complete ? 'No organization matches.' : ''} />
			{:else if !complete}
				<p class="muted num pad">{ppl.loaded} / {ppl.total || data.summary.overview.people.affiliations} affiliations loaded</p>
			{:else if cov && view}
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
					<Chips sets={[{ columns: cCols, filters: cF }]} onremove={(_, k) => { const n = { ...cF }; delete n[k]; cF = n; }} onclear={() => (cF = {})} />
					<div class="covt"><DataTable columns={cCols} rows={covRows} rowKey={(r) => r.t} bind:filters={cF} bind:sort={cS} ownScroll={false} bg="var(--surface)" /></div>
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
					<h3>Affiliations ({pobs.length}{complete ? '' : ' so far'})</h3>
					<Chips sets={[{ columns: aCols, filters: aF }]} onremove={(_, k) => { const n = { ...aF }; delete n[k]; aF = n; }} onclear={() => (aF = {})} />
					<div class="dt"><DataTable columns={aCols} rows={pobs} rowKey={(o) => o.obs_id} rowTip={aTip} bind:filters={aF} bind:sort={aS} ownScroll={false} bg="var(--surface)" /></div>
				{:else if complete}
					<p class="muted">No published affiliation in the atlas.</p>
				{/if}
				{#if person.lin_grade}
					<h3>Career lineage record</h3>
					<p class="small">Listed in a curated career-lineage record, from these public sources:</p>
					<ul class="small">
						{#each person.lin_sources.split(';').filter(Boolean) as sid}
							{@const s = view?.sources[sid] ?? {}}
							<li>{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title}</a>{:else}{s.title}{/if} <span class="muted">{[s.type, s.year].filter(Boolean).join(', ')}</span></li>
						{/each}
					</ul>
				{/if}
			{:else if mode === 'orgs' && org}
				<h2>{name(org)} <a class="hub" href={link('/orgs/hub') + '?id=' + encodeURIComponent(org)}>hub</a></h2>
				<div class="meta muted">{opeople.length} people, {otab.get(org)?.obs ?? 0} published affiliations{complete ? '' : ' so far'}</div>
				<Chips sets={[{ columns: dCols, filters: dF }]} onremove={(_, k) => { const n = { ...dF }; delete n[k]; dF = n; }} onclear={() => (dF = {})} />
				<div class="dt"><DataTable columns={dCols} rows={opeople} rowKey={(p) => p.person.id} onselect={(k) => ((mode = 'persons'), pick(k))} defaultSort={dSort} tie={dTie} bind:filters={dF} bind:sort={dS} ownScroll={false} bg="var(--surface)" empty="" /></div>
			{:else if mode === 'coverage'}
				<h3>What is shown</h3>
				<ul class="small">
					<li>An affiliation is what a publication prints for an author (or, for some conference papers, what the conference program lists), dated by the publication or session date. It is a dated point, not an employment period.</li>
					<li>Only public professional sources are used. Affiliations of authors whose identity is still under review are not shown.</li>
				</ul>
			{:else if complete}
				<p class="muted">{mode === 'persons' ? 'Select a person.' : 'Select an organization.'}</p>
			{/if}
		</aside>
	</div>
{/if}

<style>
	.page { height: 100%; display: grid; grid-template-columns: minmax(0, 1fr) 520px; grid-template-rows: minmax(0, 1fr); }
	.main { min-width: 0; min-height: 0; display: flex; flex-direction: column; border-right: 1px solid var(--border); }
	.main > :global(.scroll) { flex: 1; height: auto; }
	.bar { display: flex; gap: 6px; align-items: center; padding: 6px 8px; background: var(--surface); border-bottom: 1px solid var(--border); min-width: 0; }
	.bar input { flex: 1; min-width: 80px; }
	.bar > .muted { white-space: nowrap; }
	.grow { flex: 1; }
	.tabs button { height: 24px; font-size: 12px; padding: 0 10px; }
	.scroll { overflow: auto; min-height: 0; flex: 1; }
	.cov { padding: 8px; display: flex; flex-direction: column; gap: 8px; }
	.cov > :global(*) { flex: none; }
	.dt { overflow-x: auto; }
	.covt { max-width: 720px; }
	.pad { padding: 12px; }
	.detail { min-height: 0; overflow: auto; padding: 8px 10px; background: var(--surface); }
	.tl { margin: 6px 0 4px; }
	h2 { margin: 0 0 4px; font-size: 14px; }
	h2 .hub { font-size: 11px; font-weight: 400; margin-left: 6px; }
	h3 { margin: 10px 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	.meta { display: flex; flex-wrap: wrap; gap: 4px 12px; font-size: 11px; }
	.small { font-size: 11px; }
	.sib { font-size: 10px; margin-left: 4px; }
	.role { margin-left: 4px; }
	ul { margin: 0; padding-left: 16px; }
	.err { padding: 12px; color: var(--crit); }
	@media (max-width: 1100px) { .page { grid-template-columns: minmax(0, 1fr) 400px; } }
	@media (max-width: 900px) {
		.page { grid-template-columns: minmax(0, 1fr); grid-template-rows: minmax(0, 1fr) 50%; }
		.main { border-right: none; }
		.detail { border-top: 1px solid var(--border); }
		.bar { flex-wrap: wrap; }
	}
</style>
