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
	import { corpusOf, coverage, dateNum, orgPeople, orgTable, personStats, siblingPaper } from '../../lib/views';

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
	const CORPORA = ['eo', 'pk', 'ofc2026'];
	// D199b: the grade belongs to the row (OFC header rows A, OFC program rows B), so corpus labels carry no grade
	const CORPUS_LABEL: Record<string, string> = { eo: 'EO atlas paper', pk: 'Packaging paper', ofc2026: 'OFC 2026' };
	const trunc40 = (s: string) => trunc(s, 40);
	const orgFull = (o: Obs) => (o.org_id ? name(o.org_id) : o.printed_org + ' (unmapped)');
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
	const GRADE_SYM: Record<string, string> = { A: 'circle', B: 'square' };
	const tip = (o: Obs) => {
		const s = view?.sources[o.source_id] ?? {};
		return [
			`<b>${esc(orgFull(o))}</b>`,
			...((stack.get(orgLabel(o) + '|' + o.active_on) ?? 1) > 1 ? [`${stack.get(orgLabel(o) + '|' + o.active_on)} observations at this point`] : []),
			`${o.active_on}${o.active_on.length === 4 ? ' (year only)' : ''}; grade ${o.grade}; ${o.aff_role}`,
			`printed: ${esc(o.printed_org)}${o.unit ? '; ' + esc(o.unit) : ''}`,
			`${esc(trunc(s.title ?? o.source_id, 70))}`,
			`${o.source_id}; ${esc(o.locator)}`
		].join('<br>');
	};
	const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
	const trunc = (s: string, n: number) => (s.length > n ? s.slice(0, n - 1) + '...' : s);
	const traces = $derived(
		CORPORA.map((c, i) => {
			const os = pobs.filter((o) => corpusOf(o.source_id) === c);
			return {
				type: 'scatter',
				mode: 'markers',
				name: CORPUS_LABEL[c],
				x: os.map((o) => dateNum(o.active_on)),
				y: os.map(orgLabel),
				text: os.map(tip),
				hovertemplate: '%{text}<extra></extra>',
				marker: { color: slotColor(i, ui.theme), size: 10, symbol: os.map((o) => GRADE_SYM[o.grade] ?? 'diamond'), line: { color: th.surface, width: 1 } }
			};
		})
			.filter((t) => t.x.length)
			// legend-only entries for the symbol = grade encoding (D196)
			.concat(
				[...new Set(pobs.map((o) => o.grade))].sort().map((g) => ({
					type: 'scatter',
					mode: 'markers',
					name: 'grade ' + g,
					x: [null],
					y: [null],
					text: [],
					hovertemplate: '',
					marker: { color: th.muted, size: 9, symbol: [GRADE_SYM[g] ?? 'diamond'], line: { color: th.surface, width: 1 } }
				})) as any[]
			)
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
	const cov = $derived(view ? coverage(view.obs) : null);
	const covSeries = $derived(cov ? CORPORA.filter((c) => cov.byYear.has(c)).map((c) => ({ key: c, name: CORPUS_LABEL[c], color: slotColor(CORPORA.indexOf(c), ui.theme), y: cov.byYear.get(c) ?? [] })) : []);
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
					<input type="search" placeholder={mode === 'persons' ? 'Search name, id, ORCID' : 'Search organization'} value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
				{:else}
					<div class="grow"></div>
				{/if}
				<span class="muted num" data-tip="Public persons and observations only (DevLog-004 D70, D94): observations of persons in the identity review queue, and queued observations, are not published. Grade A: affiliation printed in the paper (EO, packaging, OFC paper header); B: OFC program metadata.">
					{#if mode === 'persons'}{plist.length} / {view.counts.persons_public} persons{:else if mode === 'orgs'}{olist.length} orgs{:else}{view.counts.obs_public} / {view.counts.obs_all} obs public{/if}
				</span>
			</div>
			{#if mode === 'persons'}
				<div class="scroll" onscroll={onScroll}>
					<table class="t num">
						<thead>
							<tr>
								{#each [['name', 'Person', 'Display name'], ['n', 'Obs', 'Public observations'], ['first', 'First', 'Earliest observation date'], ['last', 'Last', 'Latest observation date'], ['orgs', 'Orgs', 'Distinct organizations observed']] as [k, l, t]}
									<th class:r={k !== 'name'} data-tip={t} onclick={() => sortBy(k as typeof sortKey)}>{l}{sortKey === k ? (sortDir === 1 ? ' ^' : ' v') : ''}</th>
								{/each}
							</tr>
						</thead>
						<tbody>
							{#each plist.slice(0, limit) as p (p.id)}
								{@const s = stats[p.i]}
								<tr class:sel={p.id === pid} onclick={() => pick(p.id)}>
									<td class="name" data-tip={p.id}>{p.name}</td><td class="r">{#if s.n}{s.n}{:else if p.lin_grade}<span class="muted" data-tip="public through a lineage (LIN) record; no affiliation observation published">LIN</span>{/if}</td><td class="r">{s.first}</td><td class="r">{s.last}</td><td class="r">{s.orgs || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
					{#if !plist.length}<p class="muted pad">No person matches.</p>{/if}
				</div>
			{:else if mode === 'orgs'}
				<div class="scroll" onscroll={onScroll}>
					<table class="t num">
						<thead><tr><th>Organization</th><th>Type</th><th>CC</th><th class="r" data-tip="distinct public persons with a public observation at the org">Persons</th><th class="r" data-tip="public observations">Obs</th></tr></thead>
						<tbody>
							{#each olist.slice(0, limit) as [id, n] (id)}
								{@const o = store.byId.get(id)}
								<tr class:sel={id === org} onclick={() => pickOrg(id)}>
									<td class="name" data-tip={id}>{name(id)}</td><td>{o?.type ?? ''}</td><td>{o?.country ?? ''}</td><td class="r">{n.persons}</td><td class="r">{n.obs}</td>
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
						desc="Public affiliation observations per year of the observation date, stacked by corpus; grades per corpus in the table below"
						badge={`${view.counts.obs_public}/${view.counts.obs_all}`}
						badgeTip={`${view.counts.obs_public} of ${view.counts.obs_all} observations are public; the rest are observations of persons in the identity review queue, or queued observations (not published)`}
						years={cov.years}
						series={covSeries}
						xTitle="Observation year"
						yTitle="Observations (count)"
						unit="observations"
						height={320}
					/>
					<table class="t num grid">
						<thead><tr><th>corpus</th>{#each cov.grades as g}<th class="r">grade {g}</th>{/each}<th class="r" data-tip="public observations">public</th><th class="r" data-tip="all observations in data/people (public + not published)">all</th><th class="r">public %</th></tr></thead>
						<tbody>
							{#each Object.entries(view.totals_by_corpus) as [c, t]}
								<tr><td>{c}</td>{#each cov.grades as g}<td class="r">{cov.byGrade.get(`${c}|${g}`) ?? ''}</td>{/each}<td class="r">{t.public}</td><td class="r">{t.all}</td><td class="r">{((100 * t.public) / t.all).toFixed(1)}</td></tr>
							{/each}
							<tr class="tot"><td>persons</td>{#each cov.grades as _}<td></td>{/each}<td class="r">{view.counts.persons_public}</td><td class="r">{view.counts.persons_all}</td><td class="r">{((100 * view.counts.persons_public) / view.counts.persons_all).toFixed(1)}</td></tr>
						</tbody>
					</table>
					<p class="muted small">{unmappedObs} public observations have a printed organization that maps to no registry org.</p>
				</div>
			{/if}
		</div>
		<aside class="detail">
			{#if mode === 'persons' && person}
				<h2>{person.name}</h2>
				<div class="meta">
					<span class="mono muted">{person.id}</span>
					{#if person.orcid}<a href="https://orcid.org/{person.orcid}" target="_blank" rel="noopener">ORCID {person.orcid}</a>{/if}
					{#if person.disambiguator}<span class="muted">{person.disambiguator}</span>{/if}
				</div>
				{#if pobs.length}
					<div class="tl" style:height="{tlHeight}px"><Plot data={traces} layout={tlLayout} /></div>
					<h3>Observations ({pobs.length})</h3>
					<table class="t num">
						<thead><tr><th>date</th><th>organization</th><th data-tip="evidence grade">gr</th><th>source</th></tr></thead>
						<tbody>
							{#each pobs as o (o.obs_id)}
								{@const s = view.sources[o.source_id] ?? {}}
								{@const sib = siblingPaper(o.source_id)}
								<tr data-tip={[o.obs_id, 'printed name: ' + o.printed_name, 'printed org: ' + o.printed_org, o.unit && 'unit: ' + o.unit, o.country && 'country: ' + o.country, o.kind + ', ' + o.aff_role, 'locator: ' + o.locator].filter(Boolean).join('\n')}>
									<td class="nw">{o.active_on}</td>
									<td>{#if o.org_id}<a href={link('/orgs/hub') + '?id=' + encodeURIComponent(o.org_id)}>{name(o.org_id)}</a>{:else}<span class="muted">{o.printed_org}</span>{/if}{#if o.aff_role !== 'primary'}<span class="muted role">({o.aff_role})</span>{/if}</td>
									<td>{o.grade}</td>
									<td>{#if s.url}<a href={s.url} target="_blank" rel="noopener" data-tip={s.title}>{o.source_id}</a>{:else}<span data-tip={s.title}>{o.source_id}</span>{/if}{#if sib} <a class="sib" href={sib.href} target="_blank" rel="noopener" data-tip="Open in the {sib.site}">atlas</a>{/if}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{:else}
					<p class="muted">No public affiliation observation.</p>
				{/if}
				{#if person.lin_grade}
					<h3>Lineage record</h3>
					<p class="small">Public through the lineage (LIN) record, grade {person.lin_grade}.</p>
					<ul class="small">
						{#each person.lin_sources.split(';').filter(Boolean) as sid}
							{@const s = view.sources[sid] ?? {}}
							<li>{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title || sid}</a>{:else}{s.title || sid}{/if} <span class="muted">{sid}</span></li>
						{/each}
					</ul>
				{/if}
			{:else if mode === 'orgs' && org}
				<h2>{name(org)} <a class="hub" href={link('/orgs/hub') + '?id=' + encodeURIComponent(org)}>hub</a></h2>
				<div class="meta muted">{opeople.length} persons, {otab.get(org)?.obs ?? 0} public observations</div>
				<table class="t num">
					<thead><tr><th>person</th><th class="r">obs</th><th class="r">first</th><th class="r">last</th></tr></thead>
					<tbody>
						{#each opeople as op (op.person.id)}
							<tr class="click" onclick={() => ((mode = 'persons'), pick(op.person.id))}><td>{op.person.name}</td><td class="r">{op.n}</td><td class="r">{op.first}</td><td class="r">{op.last}</td></tr>
						{/each}
					</tbody>
				</table>
			{:else if mode === 'coverage'}
				<h3>Rules</h3>
				<ul class="small">
					<li>Grade A: affiliation printed in the paper (EO, packaging, OFC paper header); grade B: OFC 2026 program metadata.</li>
					<li>An observation is a dated point (publication or session date), not an employment interval.</li>
					<li>Observations of persons in the identity review queue, and queued observations, are not published.</li>
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
	.t tr.tot td { border-top: 1px solid var(--line); }
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
