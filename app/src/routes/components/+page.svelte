<script lang="ts">
	// One row per component (DevLog-013 D502-D504): the family or subtype picked in the tree sets the columns. Rows show from
	// the head inlined in the page, then part by part. Hash: #<component_id> selects the row and moves to its family.
	import { onMount } from 'svelte';
	import { comp, fmtValue, fmtWavelength, loadComponents, type Component, type Metric } from '../../lib/components.svelte';
	import { link } from '../../lib/paths';
	import Preload from '../../lib/Preload.svelte';
	import type { Summary } from '../../lib/types';
	import LayoutViews from '../../lib/layout/LayoutViews.svelte';
	import { templateFor } from '../../lib/layout/resolve';
	import { pubTip, venueYear } from '../../lib/pub';
	import Chips from '../../lib/table/Chips.svelte';
	import ColumnChooser from '../../lib/table/ColumnChooser.svelte';
	import DataTable from '../../lib/table/DataTable.svelte';
	import FilterButton from '../../lib/table/FilterButton.svelte';
	import { applyFilters, safeDecode, type Choice, type Col, type Filter, type Filters, type Sort } from '../../lib/table/filters';
	import { BASIS_BADGE, cellNums, cellRep, cellText, cellTip, defaultParams, paramLabel, pivot, rankParams, rowNum, rowWavelength, scopeLabel, unitText, type PivotRow } from '../../lib/table/pivot';

	let { data }: { data: { summary: Summary } } = $props();
	const files = $derived(['data/parts/components/meta.json', ...Array.from({ length: data.summary.parts.components }, (_, i) => `data/parts/components/${i}.json`)]);
	const head = $derived(data.summary.head.components);

	let cls = $state('');
	let open = $state<Set<string>>(new Set());
	let q = $state('');
	let qLive = $state('');
	let selId = $state('');
	let reveal = $state('');
	let filters = $state<Filters>({});
	let rowFilters = $state<Filters>({});
	let sort = $state<Sort | null>(null);
	let shown = $state(0);
	let vFilters = $state<Filters>({});
	let vSort = $state<Sort | null>(null);
	// user choice of columns per selection; default until they touch it
	let chosen = $state<Record<string, string[]>>({});
	let timer: ReturnType<typeof setTimeout> | null = null;
	let pendingHash = '';

	const tryHash = () => {
		const id = pendingHash;
		if (!id) return;
		const c = (comp.view ?? comp.partial)?.components.find((x) => x.component_id === id);
		if (!c) return;
		pendingHash = '';
		const fam = c.class.split('.')[0];
		if (cls !== fam && cls !== c.class) setCls(fam);
		open = new Set(open).add(fam);
		filters = {};
		rowFilters = {};
		q = qLive = '';
		reveal = id;
	};
	onMount(() => {
		loadComponents();
		const fromHash = () => {
			const h = safeDecode(location.hash.slice(1));
			if (!h) return;
			selId = h;
			pendingHash = h;
			tryHash();
		};
		fromHash();
		addEventListener('hashchange', fromHash);
		return () => removeEventListener('hashchange', fromHash);
	});
	$effect(() => {
		void comp.partial;
		tryHash();
	});

	const view = $derived(comp.view ?? comp.partial);
	const reg = $derived(view ?? comp.early);
	const params = $derived(reg?.parameters ?? {});
	const inSel = (c: { class: string }, k: string) => !k || c.class === k || c.class.startsWith(k + '.');
	// real first rows until part 0 is in (same order, so nothing moves)
	const headComps = $derived(head.rows.map((r) => ({ metrics: [], source_id: '', row_kind: '', fab_orgs: [], source: {}, ...r }) as unknown as Component & { nv?: number }));
	const comps = $derived<Component[]>(view ? view.components : headComps);
	const selComps = $derived(comps.filter((c) => inSel(c, cls)));
	const match = (c: Component, s: string) => (c.label + ' ' + (c.source?.title ?? '') + ' ' + (c.source?.venue ?? '') + ' ' + c.class + ' ' + (c.platform ?? '')).toLowerCase().includes(s);
	const searched = $derived(q ? selComps.filter((c) => match(c, q.toLowerCase())) : selComps);
	const rows = $derived<PivotRow[]>(pivot(searched, rowFilters, params));
	const ranked = $derived(cls ? rankParams(selComps, params) : []);

	const subtypes = $derived(new Set(selComps.map((c) => c.class)).size);
	const subName = (c: Component) => c.class.split('.').slice(1).join('.').replace(/_/g, ' ');
	const yearOf = (c: Component) => {
		const y = Number(c.source?.year);
		return Number.isFinite(y) && y > 0 ? y : null;
	};
	// fixed widths: these columns show from the head rows on and must not move when the rest arrive (D500)
	const metaCols: Col<PivotRow>[] = [
		{ key: 'platform', label: 'Platform', kind: 'enum', w: 130, tip: 'Waveguide platform', get: (r) => r.c.platform },
		{ key: 'core', label: 'Core', kind: 'text', w: 170, tip: 'Core material as stated', get: (r) => r.c.core_material, cellTip: (r) => r.c.core_material },
		{ key: 'fab', label: 'Fab', kind: 'enum', w: 170, tip: 'Fabricating organization stated by the publication', get: (r) => r.c.fab_orgs, cellTip: (r) => r.c.fab_orgs.join(', ') },
		{ key: 'year', label: 'Year', kind: 'num', w: 64, right: true, tip: 'Publication year', get: (r) => yearOf(r.c) },
		{ key: 'pub', label: 'Publication', kind: 'text', w: 300, tip: 'Publication the values come from', get: (r) => r.c.source?.title, cellTip: (r) => pubTip(r.c.source) }
	];
	const extraCols: Col<PivotRow>[] = [
		{ key: 'values', label: 'Values', kind: 'num', w: 70, right: true, tip: 'Stored value rows of the component', get: (r) => (r.c as Component & { nv?: number }).nv ?? r.c.metrics.length },
		{ key: 'kind', label: 'Kind', kind: 'enum', tip: 'fabricated or design only', get: (r) => r.c.row_kind },
		{ key: 'cladding', label: 'Cladding', kind: 'text', cls: 'clip', tip: 'Cladding as stated', get: (r) => r.c.cladding, cellTip: (r) => r.c.cladding },
		{ key: 'process', label: 'Process', kind: 'text', cls: 'clip', tip: 'Process as stated', get: (r) => r.c.process_name, cellTip: (r) => r.c.process_name },
		{ key: 'venue', label: 'Venue', kind: 'enum', cls: 'clip', tip: 'Venue of the publication', get: (r) => r.c.source?.venue, cellTip: (r) => r.c.source?.venue },
		{ key: 'pubtype', label: 'Type', kind: 'enum', tip: 'Publication type', get: (r) => r.c.source?.type }
	];
	const nameCol: Col<PivotRow> = { key: 'label', label: 'Component', kind: 'text', w: 240, tip: 'Component label (source design)', get: (r) => r.c.label, cellTip: (r) => r.c.label };
	const classCol: Col<PivotRow> = { key: 'class', label: 'Class', kind: 'enum', w: 190, tip: 'class.subtype', get: (r) => r.c.class, cellTip: (r) => r.c.class, sort: (r) => r.c.class };
	const subCol: Col<PivotRow> = { key: 'sub', label: 'Subtype', kind: 'enum', tip: 'Subtype within the family', get: (r) => subName(r.c) };
	// one column per parameter and scope (D503): scopes never mix in a cell, a sort or a range
	const paramCols = $derived(
		ranked.map((rp): Col<PivotRow> => {
			const key = 'p:' + rp.key, def = params[rp.param];
			const cell = (r: PivotRow) => r.cells.get(rp.key);
			// with a range set, the cell and its sort follow the rows that matched it; the full list stays on hover
			const shownRow = (r: PivotRow) => {
				const c = cell(r);
				return c ? cellRep(c, filters[key]) : undefined;
			};
			return {
				key,
				label: paramLabel(rp.param) + (rp.split ? ', ' + scopeLabel(rp.scope) : ''),
				unit: unitText(def?.unit),
				kind: 'num',
				right: true,
				tip: [rp.param, rp.split ? 'scope: ' + scopeLabel(rp.scope) : rp.scope && 'scope: ' + scopeLabel(rp.scope), def?.def, 'One value per component: measured first; all stored rows on hover. The range filter matches any stored row; a stored bound matches where the range overlaps it.'].filter(Boolean).join('\n'),
				get: (r) => cellNums(cell(r)),
				sort: (r) => {
					const m = shownRow(r);
					return m ? Number(m.value) : null;
				},
				text: (r) => {
					const m = shownRow(r);
					return m ? cellText(m) : '';
				},
				badge: (r) => {
					const m = shownRow(r);
					return m ? (BASIS_BADGE[m.basis] ?? '?') : '';
				},
				badgeOn: (r) => shownRow(r)?.basis === 'measured',
				more: (r) => (cell(r)?.rows.length ?? 1) - 1,
				cellTip: (r) => cellTip(cell(r), shownRow(r))
			};
		})
	);
	const columns = $derived<Col<PivotRow>[]>(cls ? [nameCol, subCol, ...metaCols.slice(0, 1), ...paramCols, ...metaCols.slice(1), ...extraCols] : [nameCol, classCol, ...metaCols, ...extraCols]);
	const defaults = $derived.by(() => {
		if (!cls) return ['label', 'class', 'platform', 'core', 'fab', 'year', 'pub', 'values'];
		return ['label', ...(subtypes > 1 ? ['sub'] : []), 'platform', ...defaultParams(ranked, selComps.length).map((k) => 'p:' + k), 'core', 'fab', 'year', 'pub'];
	});
	const visible = $derived(chosen[cls] ?? defaults);
	const rankedBy = $derived(new Map(ranked.map((r) => ['p:' + r.key, r])));
	const choices = $derived<Choice[]>(
		columns
			.filter((c) => c.key !== 'label')
			.map((c) => {
				const rp = rankedBy.get(c.key);
				return {
					key: c.key,
					label: c.label,
					unit: c.unit,
					tip: rp ? [rp.param, params[rp.param]?.def].filter(Boolean).join('\n') : c.tip,
					n: rp?.n,
					group: rp ? (rp.kind === 'geometry' ? 'Geometry' : 'Performance') : 'Component'
				};
			})
			.sort((a, b) => (a.group === 'Component' ? 1 : 0) - (b.group === 'Component' ? 1 : 0))
	);
	const defaultSort: Sort = { key: 'class', dir: 1 };
	const sortCol = $derived(cls ? null : defaultSort);
	const tie = (a: PivotRow, b: PivotRow) => (cls ? (a.c.class < b.c.class ? -1 : a.c.class > b.c.class ? 1 : 0) : 0) || (a.c.component_id < b.c.component_id ? -1 : 1);

	// row-level filters: which stored rows feed the cells (D503)
	const basisCol: Col<Metric> = { key: 'basis', label: 'Basis', kind: 'enum', noEmpty: true, get: (m) => m.basis, enumLabel: (v) => (BASIS_BADGE[v] ? BASIS_BADGE[v] + ' ' : '') + v.replace(/_/g, ' ') };
	const wlCol: Col<Metric> = { key: 'wl', label: 'Wavelength', unit: 'nm', kind: 'num', get: (m) => rowWavelength(m) ?? null };
	const rowCols: Col<Metric>[] = [basisCol, wlCol];
	// counts of a row filter honour every other active filter, like a column's facets (read only while its popover is open)
	const facetMetrics = (except: string): Metric[] => {
		const rf = { ...rowFilters };
		delete rf[except];
		return applyFilters(pivot(searched, rf, params), columns, filters).flatMap((r) => [...r.cells.values()].flatMap((c) => c.rows));
	};
	const setRow = (k: string, f: Filter | null) => {
		const n = { ...rowFilters };
		if (f) n[k] = f;
		else delete n[k];
		rowFilters = n;
	};

	function setCls(k: string) {
		cls = k;
		if (sort && (sort.key.startsWith('p:') || sort.key === 'sub' || sort.key === 'class')) sort = null;
		// common columns keep their filters; parameter columns belong to the previous selection
		filters = Object.fromEntries(Object.entries(filters).filter(([f]) => !f.startsWith('p:') && f !== 'sub' && (k === '' || f !== 'class')));
	}
	function pickFamily(k: string) {
		setCls(k);
		open = new Set(open).add(k);
	}
	function toggle(k: string) {
		const s = new Set(open);
		if (s.has(k)) s.delete(k);
		else s.add(k);
		open = s;
	}
	function onInput(v: string) {
		qLive = v;
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => (q = v), 300);
	}
	function select(id: string) {
		if (id !== selId) {
			vFilters = {};
			vSort = null;
		}
		selId = id;
		history.replaceState(history.state, '', `#${encodeURIComponent(id)}`);
	}
	function closeDetail() {
		selId = '';
		history.replaceState(history.state, '', location.pathname + location.search);
	}
	function removeChip(set: number, key: string) {
		if (set === 0) {
			const n = { ...filters };
			delete n[key];
			filters = n;
		} else setRow(key, null);
	}
	const sel = $derived(view?.components.find((c) => c.component_id === selId));
	const valueCols: Col<Metric>[] = [
		{ key: 'parameter', label: 'parameter', kind: 'enum', w: 124, tip: 'Registry parameter', get: (m) => m.parameter },
		{ key: 'value', label: 'value', kind: 'num', w: 72, right: true, get: (m) => {
				const n = rowNum(m);
				return n === null ? [] : [n];
			}, text: (m) => fmtValue(m), sort: (m) => Number(m.value) },
		{ key: 'unit', label: 'unit', kind: 'enum', w: 56, get: (m) => m.unit },
		{ key: 'cond', label: 'conditions', kind: 'text', w: 200, cls: 'wrap', get: (m) => [fmtWavelength(m) && fmtWavelength(m) + (m.wavelength_nm ? ' nm' : ''), m.polarization, m.temperature_k && m.temperature_k + ' K', m.bias_v && m.bias_v + ' V', m.ref_plane, m.condition].filter(Boolean).join(', ') },
		{ key: 'scope', label: 'scope', kind: 'enum', w: 96, get: (m) => m.scope, enumLabel: (v) => v.replace(/_/g, ' ') },
		{ key: 'basis', label: 'basis', kind: 'enum', w: 96, get: (m) => m.basis, enumLabel: (v) => v.replace(/_/g, ' ') },
		{ key: 'loc', label: 'loc', kind: 'text', w: 76, cls: 'wrap', get: (m) => m.locator }
	];
	const valueTip = (m: Metric) => [m.includes && 'includes ' + m.includes, m.excludes && 'excludes ' + m.excludes, m.method && 'method ' + m.method, m.statistic && m.statistic + (m.n_samples ? ' n=' + m.n_samples : ''), m.notes].filter(Boolean).join('\n') || undefined;
	const famCount = (subs: [string, number][]) => subs.reduce((t, s) => t + s[1], 0);
	const loaded = $derived(view ? view.components.length : head.rows.length);
	const full = $derived(!!comp.view);
</script>

<Preload {files} />

{#if comp.error}
	<div class="err">{comp.error}</div>
{:else}
	<div class="page" class:open={!!sel && !!view}>
		<aside class="tree">
			<button class="node" class:on={!cls} onclick={() => setCls('')}><span class="cl">All classes</span> <span class="num">{head.total}</span></button>
			{#each head.tree as [k, label, subs] (k)}
				<div class="fam">
					<button class="tw" onclick={() => toggle(k)} aria-label="expand {label}">{open.has(k) ? '-' : '+'}</button>
					<button class="node" class:on={cls === k} disabled={!famCount(subs)} onclick={() => pickFamily(k)} data-tip={reg ? [reg.classes[k]?.label, ...Object.values(reg.classes[k]?.subtypes ?? {})].filter(Boolean).join('\n') : label}>
						<span class="cl">{label}</span> <span class="num">{famCount(subs) || ''}</span>
					</button>
				</div>
				{#if open.has(k)}
					{#each subs.filter((s) => s[1]) as [s, n] (s)}
						<button class="node sub" class:on={cls === k + '.' + s} onclick={() => setCls(k + '.' + s)} data-tip={reg?.classes[k]?.subtypes[s]}><span class="cl">{s.replace(/_/g, ' ')}</span> <span class="num">{n}</span></button>
					{/each}
				{/if}
			{/each}
		</aside>
		<div class="main">
			<div class="bar">
				<input type="search" placeholder="Search component, publication, platform" value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
				<FilterButton col={basisCol} rows={facetMetrics('basis')} filter={rowFilters.basis} onchange={(f) => setRow('basis', f)} tip="Which stored rows feed the cells: measured, simulated, design target, ..." />
				<FilterButton col={wlCol} rows={facetMetrics('wl')} filter={rowFilters.wl} onchange={(f) => setRow('wl', f)} tip="Wavelength of the performance rows (a center wavelength by its own value; otherwise the stated value, else ITU band edges). Geometry rows stay." />
				<ColumnChooser {choices} {visible} total={selComps.length} onchange={(k) => (chosen = { ...chosen, [cls]: k })} onreset={() => { const n = { ...chosen }; delete n[cls]; chosen = n; }} />
				{#if full}<span class="muted num" data-tip="components shown / in this selection">{shown} / {selComps.length} components</span>{:else}<span class="muted num" data-tip="components received; the table grows as they arrive">{loaded} / {comp.total || head.total} loaded</span>{/if}
			</div>
			<Chips sets={[{ columns, filters }, { columns: rowCols, filters: rowFilters }]} onremove={removeChip} onclear={() => ((filters = {}), (rowFilters = {}))} />
			{#key cls}
				<DataTable {columns} {visible} {rows} rowKey={(r) => r.c.component_id} selected={selId} onselect={select} defaultSort={sortCol} {tie} bind:filters bind:sort bind:shown {reveal} onrevealed={() => (reveal = '')} empty={full ? 'No component matches.' : ''} />
			{/key}
		</div>
		{#if sel && view}<aside class="detail">
				<div class="dh"><h2>{sel.label}</h2><button class="x" onclick={closeDetail} aria-label="Close" data-tip="Close this panel">x</button></div>
				<dl>
					<dt>class</dt><dd>{sel.class}</dd>
					<dt>kind</dt><dd>{sel.row_kind}</dd>
					{#if sel.platform}<dt>platform</dt><dd>{sel.platform}</dd>{/if}
					{#if sel.core_material}<dt>core</dt><dd>{sel.core_material}</dd>{/if}
					{#if sel.cladding}<dt>cladding</dt><dd>{sel.cladding}</dd>{/if}
					{#if sel.fab_orgs.length}<dt>fab</dt><dd>{sel.fab_orgs.join(', ')}</dd>{/if}
					{#if sel.process_name}<dt>process</dt><dd>{sel.process_name}</dd>{/if}
					<dt>publication</dt><dd data-tip={pubTip(sel.source)}>{#if sel.source.url}<a href={sel.source.url} target="_blank" rel="noopener">{sel.source.title}</a>{:else}{sel.source.title}{/if} <span class="muted">{[venueYear(sel.source), sel.source.type].filter(Boolean).join('; ')}</span>{#if sel.source.atlas} <a href={sel.source.atlas[1]} target="_blank" rel="noopener">{sel.source.atlas[0]}</a>{/if}</dd>
				</dl>
				{#if sel.notes}<p class="muted">{sel.notes}</p>{/if}
				{#if templateFor(sel.class, view.layouts)}
					<h3 class="lay">Layout <a href={link('/layout') + '?id=' + encodeURIComponent(sel.component_id)} data-tip="Full-size top view, cross-section and dimension table">full view</a></h3>
					<LayoutViews comp={sel} {view} compact />
				{/if}
				<h3>Values</h3>
				<Chips sets={[{ columns: valueCols, filters: vFilters }]} onremove={(_, k) => { const n = { ...vFilters }; delete n[k]; vFilters = n; }} onclear={() => (vFilters = {})} />
				<div class="vt"><DataTable columns={valueCols} rows={sel.metrics} rowKey={(m) => m.metric_id} rowTip={valueTip} bind:filters={vFilters} bind:sort={vSort} ownScroll={false} bg="var(--surface)" /></div>
		</aside>{/if}
	</div>
{/if}

<style>
	.page { height: 100%; display: grid; grid-template-columns: 200px minmax(0, 1fr); grid-template-rows: minmax(0, 1fr); }
	.page.open { grid-template-columns: 200px minmax(0, 1fr) 400px; }
	.tree { min-height: 0; overflow: auto; border-right: 1px solid var(--border); background: var(--surface); padding: 4px; display: flex; flex-direction: column; gap: 1px; }
	.fam { display: flex; align-items: center; min-width: 0; flex: none; }
	.tw { width: 14px; height: 22px; padding: 0; border: none; background: transparent; color: var(--ink-3); flex: none; }
	.node { flex: 1; text-align: left; display: flex; justify-content: space-between; border: none; background: transparent; height: 22px; gap: 6px; min-width: 0; }
	.tree > .node { flex: none; padding-left: 22px; }
	.node.on { background: var(--sel); color: var(--ink); }
	.node:disabled { color: var(--ink-3); cursor: default; }
	.node.sub { flex: none; padding-left: 26px; height: 20px; color: var(--ink-2); }
	.node.sub.on { color: var(--ink); }
	.cl { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.main { min-width: 0; min-height: 0; display: flex; flex-direction: column; border-right: 1px solid var(--border); }
	.main > :global(.scroll) { flex: 1; height: auto; }
	.bar { display: flex; gap: 6px; align-items: center; padding: 6px 8px; background: var(--surface); border-bottom: 1px solid var(--border); min-width: 0; }
	.bar input { flex: 1; min-width: 60px; }
	.bar > .muted { white-space: nowrap; }
	.detail { min-height: 0; overflow: auto; padding: 8px 10px; background: var(--surface); }
	.dh { display: flex; align-items: flex-start; gap: 8px; }
	.dh h2 { flex: 1; min-width: 0; }
	.x { flex: none; width: 20px; height: 20px; padding: 0; }
	.vt { overflow-x: auto; }
	h2 { margin: 0 0 6px; font-size: 14px; overflow-wrap: anywhere; }
	h3.lay { display: flex; justify-content: space-between; }
	h3.lay a { text-transform: none; letter-spacing: 0; font-weight: 400; }
	h3 { margin: 10px 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	dl { display: grid; grid-template-columns: 80px 1fr; gap: 2px 8px; margin: 0; }
	dt { color: var(--ink-3); }
	dd { margin: 0; overflow-wrap: anywhere; }
	.err { padding: 12px; color: var(--crit); }
	.page { position: relative; }
	@media (max-width: 1100px) {
		.page, .page.open { grid-template-columns: 160px minmax(0, 1fr); }
		/* over the table, not instead of it */
		.detail { position: absolute; top: 0; right: 0; bottom: 0; width: min(400px, 100%); z-index: 6; border-left: 1px solid var(--line); box-shadow: -3px 0 10px rgba(0, 0, 0, 0.3); }
	}
	@media (max-width: 700px) {
		.page, .page.open { grid-template-columns: minmax(0, 1fr); grid-template-rows: 120px minmax(0, 1fr); }
		.tree { border-right: none; border-bottom: 1px solid var(--border); }
		.main { border-right: none; }
		.bar { flex-wrap: wrap; }
		.bar input { flex-basis: 100%; }
	}
</style>
