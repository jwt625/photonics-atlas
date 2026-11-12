<script lang="ts">
	// Supply-chain view (DevLog-010 D190, D194, D195): category tree A-K -> vendor -> usage rows -> papers; foundry
	// process observations; standards and reliability tests. Hash state: tab, cat, org, std.
	import { onMount } from 'svelte';
	import Preload from '../../lib/Preload.svelte';
	import Chips from '../../lib/table/Chips.svelte';
	import DataTable from '../../lib/table/DataTable.svelte';
	import type { Col, Filters, Sort } from '../../lib/table/filters';
	import type { Summary } from '../../lib/types';
	import { link } from '../../lib/paths';
	import { store, ui } from '../../lib/state.svelte';
	import { loadSupply, sup, type Row, type Usage } from '../../lib/supply.svelte';
	import { slotColor } from '../../lib/explore/colors';
	import StackBars from '../../lib/StackBars.svelte';
	import { descendants, OTHER, rollup, shareByYear, split, vendors, yearOf } from '../../lib/views';
	import { pubTip } from '../../lib/pub';

	let { data }: { data: { summary: Summary } } = $props();
	const head = $derived(data.summary.head.supply);

	type Tab = 'usage' | 'processes' | 'standards';
	let tab = $state<Tab>('usage');
	let cat = $state('');
	let org = $state('');
	let std = $state('');
	let q = $state('');
	let qLive = $state('');
	let open = $state<Set<string>>(new Set());
	let showEmpty = $state(false);
	let prod = $state('');
	let winW = $state(1400);
	const narrow = $derived(winW < 900);
	let timer: ReturnType<typeof setTimeout> | null = null;

	function readHash() {
		const p = new URLSearchParams(location.hash.slice(1));
		const t = p.get('tab');
		tab = t === 'processes' || t === 'standards' ? t : 'usage';
		cat = p.get('cat') ?? '';
		org = p.get('org') ?? '';
		std = p.get('std') ?? '';
		const hq = p.get('q');
		if (hq !== null) q = qLive = hq;
	}
	function writeHash() {
		const p = new URLSearchParams();
		if (tab !== 'usage') p.set('tab', tab);
		if (cat) p.set('cat', cat);
		if (org) p.set('org', org);
		if (std) p.set('std', std);
		const h = p.toString();
		history.replaceState(history.state, '', h ? '#' + h : location.pathname + location.search);
	}
	onMount(() => {
		loadSupply();
		readHash();
		addEventListener('hashchange', readHash);
		return () => removeEventListener('hashchange', readHash);
	});
	function onInput(v: string) {
		qLive = v;
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => (q = v), 300);
	}
	const set = (k: 'tab' | 'cat' | 'org' | 'std', v: string) => {
		prod = '';
		if (k === 'tab') tab = v as Tab;
		else if (k === 'cat') cat = v;
		else if (k === 'org') org = v;
		else std = v;
		writeHash();
	};

	const view = $derived(sup.view);
	type VRow = { org: string; name: string; type: string; country: string; rows: number; sources: number; roles: string[]; cats: string[]; y0: number | null; y1: number | null; years: number[] };
	const headName = $derived(new Map(head.rows.map((r) => [r.org, r.name])));
	const name = (id: string) => store.byId.get(id)?.name ?? headName.get(id) ?? id;
	// real tree and first vendor rows from the head inlined in the page until the view is in (D500)
	const cats = $derived<{ id: string; label: string; parent?: string }[]>(view?.categories ?? head.categories.map(([id, label, parent]) => ({ id, label, parent: parent || undefined })));
	const catById = $derived(new Map(cats.map((c) => [c.id, c])));
	const counts = $derived(view ? rollup(cats, view.usage) : new Map(head.categories.map((c) => [c[0], c[3]])));
	const kids = $derived.by(() => {
		const m = new Map<string, string[]>();
		for (const c of cats) if (c.parent) m.set(c.parent, [...(m.get(c.parent) ?? []), c.id]);
		return m;
	});
	let inited = false;
	$effect(() => {
		// default once: top levels with rows open, plus the ancestors of the selected category
		if (inited || !cats.length) return;
		inited = true;
		const s = new Set(cats.filter((c) => !c.parent && (counts.get(c.id) ?? 0) > 0).map((c) => c.id));
		if (cat && kids.has(cat)) s.add(cat);
		let p = catById.get(cat)?.parent;
		while (p) {
			s.add(p);
			p = catById.get(p)?.parent;
		}
		open = s;
	});
	type Node = { id: string; depth: number };
	const tree = $derived.by(() => {
		const out: Node[] = [];
		const walk = (id: string, depth: number) => {
			if (!showEmpty && !(counts.get(id) ?? 0) && depth > 0) return;
			out.push({ id, depth });
			if (open.has(id)) for (const k of kids.get(id) ?? []) walk(k, depth + 1);
		};
		for (const c of cats) if (!c.parent) walk(c.id, 0);
		return out;
	});
	function toggle(id: string) {
		const s = new Set(open);
		if (s.has(id)) s.delete(id);
		else s.add(id);
		open = s;
	}
	const ids = $derived(cat ? descendants(cats, cat) : null);
	const fold = (s: string) => s.toLowerCase();
	const usageIn = $derived((view?.usage ?? []).filter((u) => !ids || ids.has(u.category_id)));
	// years with a stated use per vendor, in the selected category: the Years filter matches these, not the first-last span
	const yearsBy = $derived.by(() => {
		const m = new Map<string, Set<number>>();
		for (const u of usageIn) {
			const y = yearOf(view?.sources ?? {}, u.source_id);
			if (y === null) continue;
			if (!m.has(u.org_id)) m.set(u.org_id, new Set());
			(m.get(u.org_id) as Set<number>).add(y);
		}
		return m;
	});
	const vend = $derived<VRow[]>(
		view
			? vendors(usageIn, view.sources, null)
					.filter((v) => !q || fold(name(v.org) + ' ' + v.org).includes(fold(q)))
					.map((v) => ({ ...v, name: name(v.org), type: store.byId.get(v.org)?.type ?? '', country: store.byId.get(v.org)?.country ?? '', years: [...(yearsBy.get(v.org) ?? [])] }))
			: head.rows.map((r) => ({ y0: null, y1: null, type: '', country: '', years: [r.y0, r.y1].filter((y): y is number => y !== undefined), ...r }))
	);
	const share = $derived(view ? shareByYear(view.usage, view.sources, ids) : null);
	const slotOf = (k: string, keys: string[]) => (k === OTHER ? -1 : keys.filter((x) => x !== OTHER).indexOf(k));
	const series = $derived(
		share ? share.keys.map((k) => ({ key: k, name: k === OTHER ? 'other vendors' : name(k), color: slotColor(slotOf(k, share.keys), ui.theme), y: share.counts.get(k) ?? [] })) : []
	);
	// chart colour of each vendor (D194 slots; grey = other vendors), repeated in the table so the legend can be hidden
	const swatch = (org: string) => (share && share.keys.includes(org) ? slotColor(slotOf(org, share.keys), ui.theme) : slotColor(-1, ui.theme));
	const orgRows = $derived(org ? usageIn.filter((u) => u.org_id === org).sort((a, b) => (yearOf(view?.sources ?? {}, b.source_id) ?? 0) - (yearOf(view?.sources ?? {}, a.source_id) ?? 0) || a.usage_id.localeCompare(b.usage_id)) : []);
	const orgAll = $derived(org && view ? view.usage.filter((u) => u.org_id === org).length : 0);
	const products = $derived(view ? view.products.filter((p) => (!ids || ids.has(p.category_id)) && (!org || p.org_id === org)) : []);
	const prodById = $derived(new Map((view?.products ?? []).map((p) => [p.product_id, p])));
	const prodRows = (pid: string) => orgRows.filter((u) => u.product_id === pid).length;
	const shownRows = $derived(prod ? orgRows.filter((u) => u.product_id === prod) : orgRows);
	const model = (pid: string | undefined) => {
		const p = pid ? prodById.get(pid) : undefined;
		return p ? p.model + (p.product_line ? ' (' + p.product_line + ')' : '') : '';
	};

	// processes
	const procs = $derived(
		(view?.processes ?? []).filter((p) => !q || fold([name(p.org_id), p.process_name, p.platform, p.pdk_name, src(p.source_id).title].join(' ')).includes(fold(q)))
	);
	// standards and tests
	const testsBy = $derived.by(() => {
		const m = new Map<string, Row[]>();
		for (const t of view?.tests ?? []) for (const s of split(t.standard_ids)) m.set(s, [...(m.get(s) ?? []), t]);
		return m;
	});
	const stds = $derived(
		(view?.standards ?? [])
			.filter((s) => !q || fold(s.designation + ' ' + name(s.body_org_id ?? '')).includes(fold(q)))
			.map((s) => ({ s, n: testsBy.get(s.standard_id)?.length ?? 0, papers: new Set((testsBy.get(s.standard_id) ?? []).map((t) => t.source_id)).size }))
			.sort((a, b) => b.n - a.n || a.s.designation.localeCompare(b.s.designation))
	);
	const unparsed = $derived((view?.tests ?? []).filter((t) => !t.standard_ids).length);
	const stdSel = $derived(view?.standards.find((s) => s.standard_id === std));
	const stdTests = $derived(std ? (testsBy.get(std) ?? []) : []);
	const typeCounts = $derived.by(() => {
		const m = new Map<string, number>();
		for (const t of view?.tests ?? []) m.set(t.test_type, (m.get(t.test_type) ?? 0) + 1);
		return [...m].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
	});

	const src = (sid: string) => view?.sources[sid] ?? {};
	// tables (D504)
	// fixed widths: the columns must not move when the view replaces the head rows
	const vCols: Col<VRow>[] = [
		{ key: 'name', label: 'Vendor', kind: 'text', w: 240, get: (v) => v.name, cell: vendorCell },
		{ key: 'type', label: 'Type', kind: 'enum', w: 110, get: (v) => v.type, enumLabel: (t) => t.replace(/_/g, ' ') },
		{ key: 'country', label: 'CC', kind: 'enum', w: 52, get: (v) => v.country },
		{ key: 'rows', label: 'Uses', kind: 'num', w: 62, right: true, tip: 'stated uses', get: (v) => v.rows },
		{ key: 'sources', label: 'Papers', kind: 'num', w: 70, right: true, tip: 'distinct publications', get: (v) => v.sources },
		{ key: 'roles', label: 'Roles', kind: 'enum', w: 240, get: (v) => v.roles, enumLabel: (r) => r.replace(/_/g, ' ') },
		{ key: 'cats', label: 'Categories', kind: 'enum', w: 190, get: (v) => v.cats, enumLabel: (c) => c + ' ' + (catById.get(c)?.label ?? ''), text: (v) => v.cats.join(', '), cellTip: (v) => v.cats.join(', ') + '\n' + v.cats.map((c) => c + ' ' + (catById.get(c)?.label ?? '')).join('\n') },
		{ key: 'years', label: 'Years', kind: 'num', w: 92, tip: 'Publication years of the stated uses; the filter matches a vendor with a use in that range', get: (v) => v.years, text: (v) => (v.y0 === null ? '' : v.y0 === v.y1 ? String(v.y0) : `${v.y0}-${v.y1}`), sort: (v) => v.y1 }
	];
	const vSort: Sort = { key: 'rows', dir: -1 };
	const vTie = (a: VRow, b: VRow) => a.org.localeCompare(b.org);
	const pCols: Col<Row>[] = [
		{ key: 'org', label: 'Org', kind: 'enum', cls: 'lbl', get: (p) => name(p.org_id), cell: procOrgCell },
		{ key: 'process', label: 'Process (as printed)', kind: 'text', cls: 'wrap', get: (p) => p.process_name },
		{ key: 'platform', label: 'Platform', kind: 'enum', get: (p) => p.platform },
		{ key: 'wafer', label: 'Wafer', unit: 'mm', kind: 'num', right: true, tip: 'nominal wafer diameter (mm)', get: (p) => p.wafer_mm, text: (p) => p.wafer_mm ?? '' },
		{ key: 'pdk', label: 'PDK', kind: 'enum', get: (p) => p.pdk_name },
		{ key: 'open', label: 'Open', kind: 'enum', tip: 'PDK stated open', get: (p) => p.pdk_open },
		{ key: 'route', label: 'Route', kind: 'enum', tip: 'how the foundry was accessed (MPW, dedicated run, ...)', get: (p) => p.access_route },
		{ key: 'broker', label: 'Broker', kind: 'enum', get: (p) => (p.broker_org_id ? name(p.broker_org_id) : '') },
		{ key: 'pub', label: 'Publication', kind: 'text', cls: 'pub', get: (p) => src(p.source_id).title },
		{ key: 'year', label: 'Year', kind: 'num', right: true, get: (p) => src(p.source_id).year, text: (p) => src(p.source_id).year ?? '' }
	];
	type SRow = { s: Row; n: number; papers: number };
	const sCols: Col<SRow>[] = [
		{ key: 'designation', label: 'Designation', kind: 'text', w: 170, cls: 'mono', get: (r) => r.s.designation },
		{ key: 'body', label: 'Body', kind: 'enum', get: (r) => (r.s.body_org_id ? name(r.s.body_org_id) : '') },
		{ key: 'n', label: 'Tests', kind: 'num', right: true, tip: 'reliability test rows citing the designation', get: (r) => r.n },
		{ key: 'papers', label: 'Papers', kind: 'num', right: true, get: (r) => r.papers }
	];
	const sSort: Sort = { key: 'n', dir: -1 };
	const sTie = (a: SRow, b: SRow) => a.s.designation.localeCompare(b.s.designation);
	type TRow = { t: string; n: number };
	const tCols: Col<TRow>[] = [
		{ key: 't', label: 'Test type', kind: 'enum', tip: 'stress applied; the measurement type where no stress is named', get: (r) => r.t },
		{ key: 'n', label: 'Tests', kind: 'num', right: true, get: (r) => r.n }
	];
	const tSort: Sort = { key: 'n', dir: -1 };
	const tTie = (a: TRow, b: TRow) => a.t.localeCompare(b.t);
	const typeRows = $derived(typeCounts.map(([t, n]) => ({ t, n })));
	const prodCols: Col<Row>[] = [
		{ key: 'model', label: 'model', kind: 'text', w: 210, get: (p) => p.model, cell: prodCell, cellTip: (p) => p.model + (p.product_line ? ' (' + p.product_line + ')' : '') },
		{ key: 'cat', label: 'cat', kind: 'enum', w: 56, cls: 'mono', get: (p) => p.category_id, enumLabel: (c) => c + ' ' + (catById.get(c)?.label ?? ''), text: (p) => p.category_id, cellTip: (p) => catById.get(p.category_id)?.label },
		{ key: 'uses', label: 'uses', kind: 'num', w: 56, right: true, tip: 'stated uses naming this product', get: (p) => prodRows(p.product_id), text: (p) => (prodRows(p.product_id) ? String(prodRows(p.product_id)) : '') }
	];
	const testCols: Col<Row>[] = [
		{ key: 'type', label: 'type', kind: 'enum', w: 130, cls: 'wrap', tip: 'stress type; measurand after the slash', get: (t) => t.test_type + (t.measurand && t.measurand !== t.test_type ? ' / ' + t.measurand : '') },
		{ key: 'cond', label: 'condition', kind: 'text', w: 130, cls: 'wrap', get: (t) => range(t) },
		{ key: 'value', label: 'value', kind: 'text', w: 110, cls: 'wrap', get: (t) => ((t.value ?? t.value_text ?? '') + ' ' + (t.unit ?? '')).trim() }
	];
	let vFilters = $state<Filters>({});
	let pFilters = $state<Filters>({});
	let sFilters = $state<Filters>({});
	let tFilters = $state<Filters>({});
	let vS = $state<Sort | null>(null);
	let pS = $state<Sort | null>(null);
	let sS = $state<Sort | null>(null);
	let tS = $state<Sort | null>(null);
	let prF = $state<Filters>({});
	let prS = $state<Sort | null>(null);
	let tcF = $state<Filters>({});
	let tcS = $state<Sort | null>(null);
	let vShown = $state(0);
	let pShown = $state(0);
	let sShown = $state(0);
	const drop = (f: Filters, k: string) => {
		const n = { ...f };
		delete n[k];
		return n;
	};
	const srcTip = (sid: string, loc = '') => pubTip(src(sid), loc);
	const BASIS: Record<string, string> = { stated: 'stated in the publication', inferred_from_model: 'vendor inferred from the stated model number', datasheet_spec: 'datasheet specification', datasheet_typical: 'datasheet typical value' };
	const uTip = (u: Usage) => [BASIS[u.basis] ?? u.basis, srcTip(u.source_id, u.locator)].filter(Boolean).join('\n');
	const range = (t: Row) => (t.t_min_c || t.t_max_c ? `${t.t_min_c ?? ''} to ${t.t_max_c ?? ''} C` : t.temp_c ? `${t.temp_c} C` : '') + (t.rh_pct ? ` / ${t.rh_pct} %RH` : '');
</script>

<svelte:window bind:innerWidth={winW} />

<Preload files={['data/supply.json']} />

{#snippet vendorCell(v: VRow)}<span class="sw" style:background={swatch(v.org)}></span>{v.name}{/snippet}
{#snippet prodCell(p: Row)}{p.model}{#if p.product_line}<span class="muted pl">{p.product_line}</span>{/if}{/snippet}
{#snippet procOrgCell(p: Row)}<a href={link('/orgs/hub') + '?id=' + encodeURIComponent(p.org_id)}>{name(p.org_id)}</a>{/snippet}

{#if sup.error}
	<div class="err">{sup.error}</div>
{:else}
	<div class="page">
		<aside class="tree" class:off={tab !== 'usage'} inert={tab !== 'usage'} data-tip={tab !== 'usage' ? 'Categories apply to the Usage tab' : undefined}>
			<div class="th">
				<span class="muted" data-tip="Supply categories A-K; counts are stated uses in the subtree">Categories</span>
				<label class="muted" data-tip="Show categories without stated uses"><input type="checkbox" bind:checked={showEmpty} /> empty</label>
			</div>
			<button class="node" class:on={!cat} onclick={() => set('cat', '')}><span class="lbl">All categories</span><span class="num">{head.usage}</span></button>
			{#each tree as n (n.id)}
				{@const c = catById.get(n.id)}
				{@const k = kids.get(n.id)?.length ?? 0}
				<div class="row" style:padding-left="{n.depth * 12}px">
					<button class="tw" class:hide={!k} onclick={() => toggle(n.id)} aria-label="expand">{open.has(n.id) ? '-' : '+'}</button>
					<button class="node" class:on={cat === n.id} class:empty={!counts.get(n.id)} onclick={() => set('cat', n.id)} data-tip={c?.label}>
						<span class="id mono">{n.id}</span><span class="lbl">{c?.label}</span><span class="num">{counts.get(n.id) || ''}</span>
					</button>
				</div>
			{/each}
		</aside>
		<div class="main">
			<div class="bar">
				<span class="seg tabs">
					<button class:on={tab === 'usage'} onclick={() => set('tab', 'usage')} data-tip="Vendors per category with the papers that state their use">Usage</button><button class:on={tab === 'processes'} onclick={() => set('tab', 'processes')} data-tip="Foundry processes as described in each publication">Processes</button><button class:on={tab === 'standards'} onclick={() => set('tab', 'standards')} data-tip="Standards cited by packaging reliability tests">Standards</button>
				</span>
				<input type="search" placeholder={tab === 'usage' ? 'Filter vendors' : tab === 'processes' ? 'Filter org, process, platform, PDK' : 'Filter designation, body'} value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
				{#if !view}
					<span class="muted num" data-tip="rows shown so far; the rest arrive with the supply view">{tab === 'usage' ? `${head.rows.length} / ${head.vendors} vendors loaded` : 'supply view loading'}</span>
				{:else if tab === 'usage'}
					<span class="muted num" data-tip="vendors, stated uses and named products in the selected category">{vShown} / {vend.length} vendors, {usageIn.length} uses, {products.length} products</span>
				{:else if tab === 'processes'}
					<span class="muted num">{pShown} / {view.processes.length}</span>
				{:else}
					<span class="muted num" data-tip="cited standards / reliability tests; tests whose printed standard is not one of the listed designations">{sShown} / {view.standards.length} standards, {view.tests.length} tests, {unparsed} without a listed standard</span>
				{/if}
			</div>
			<div class="scroll">
				{#if tab === 'usage'}
					{#if share}
						<div class="chart" style:min-height="{narrow ? 186 : 316}px">
							<StackBars
								letter="a"
								desc="Stated uses (one per publication, vendor and role) per publication year in the selected category, stacked by vendor; the six vendors with most uses keep their own colour, the rest are grey. Uses stated in the papers, not market share."
								badge={`${share.total - share.noYear}/${share.total}`}
								badgeTip={`${share.total - share.noYear} of ${share.total} stated uses plotted; ${share.noYear} without a publication year`}
								years={share.years}
								{series}
								yTitle="Stated uses (count)"
								unit="rows"
								height={narrow ? 170 : 300}
								legend={!narrow}
							/>
						</div>
					{:else}
						<div class="chart" style:min-height="{narrow ? 186 : 316}px"></div>
					{/if}
					<Chips sets={[{ columns: vCols, filters: vFilters }]} onremove={(_, k) => (vFilters = drop(vFilters, k))} onclear={() => (vFilters = {})} />
					<DataTable columns={vCols} rows={vend} rowKey={(v) => v.org} selected={org} onselect={(k) => set('org', k === org ? '' : k)} defaultSort={vSort} tie={vTie} bind:filters={vFilters} bind:sort={vS} bind:shown={vShown} ownScroll={false} empty={view ? 'No stated use matches.' : ''} />
				{:else if tab === 'processes'}
					<Chips sets={[{ columns: pCols, filters: pFilters }]} onremove={(_, k) => (pFilters = drop(pFilters, k))} onclear={() => (pFilters = {})} />
					<DataTable columns={pCols} rows={procs} rowKey={(p) => p.process_id} rowTip={(p) => srcTip(p.source_id, p.locator)} bind:filters={pFilters} bind:sort={pS} bind:shown={pShown} ownScroll={false} empty={view ? 'No process matches.' : ''} />
				{:else}
					<div class="split2">
						<div class="cell">
							<Chips sets={[{ columns: sCols, filters: sFilters }]} onremove={(_, k) => (sFilters = drop(sFilters, k))} onclear={() => (sFilters = {})} />
							<DataTable columns={sCols} rows={stds} rowKey={(r) => r.s.standard_id} selected={std} onselect={(k) => set('std', k === std ? '' : k)} rowTip={(r) => [r.s.title, r.s.edition, r.s.scope].filter(Boolean).join('\n') || undefined} defaultSort={sSort} tie={sTie} bind:filters={sFilters} bind:sort={sS} bind:shown={sShown} ownScroll={false} empty={view ? 'No standard matches.' : ''} />
						</div>
						<div class="cell types">
							<Chips sets={[{ columns: tCols, filters: tFilters }]} onremove={(_, k) => (tFilters = drop(tFilters, k))} onclear={() => (tFilters = {})} />
							<DataTable columns={tCols} rows={typeRows} rowKey={(r) => r.t} defaultSort={tSort} tie={tTie} bind:filters={tFilters} bind:sort={tS} ownScroll={false} empty="" />
						</div>
					</div>
				{/if}
			</div>
		</div>
		<aside class="detail">
			{#if !view}
				{#if tab === 'usage' && org}<h2>{name(org)}</h2>{/if}
			{:else if tab === 'usage' && org}
				{@const o = store.byId.get(org)}
				<h2>{name(org)} <a class="hub" href={link('/orgs/hub') + '?id=' + encodeURIComponent(org)} data-tip="All lenses for this organization">hub</a></h2>
				<div class="meta muted spaced">
					{#if [o?.type, o?.country].some((x) => x && x !== 'unknown')}<span>{[o?.type, o?.country].filter((x) => x && x !== 'unknown').join(', ')}</span>{/if}
					<span>{cat ? cat + ': ' : ''}{orgRows.length} of {orgAll} stated uses</span>
				</div>
				<h3>Products</h3>
				{#if products.length}
					<Chips sets={[{ columns: prodCols, filters: prF }]} onremove={(_, k) => (prF = drop(prF, k))} onclear={() => (prF = {})} />
					<div class="dt"><DataTable columns={prodCols} rows={products} rowKey={(p) => p.product_id} selected={prod} onselect={(k) => (prod = prod === k ? '' : k)} rowTip={(p) => (p.status ? 'status ' + p.status : undefined)} bind:filters={prF} bind:sort={prS} ownScroll={false} bg="var(--surface)" /></div>
				{:else}
					<p class="muted small" data-tip="no product rows for this vendor{cat ? ' in this category' : ''}">none recorded</p>
				{/if}
				<h3>Used in{#if prod} <span class="muted">{model(prod)}</span>{/if}</h3>
				{#each shownRows as u (u.usage_id)}
					{@const s = src(u.source_id)}
					<div class="use" data-tip={uTip(u)}>
						<div class="uh"><span class="num">{s.year ?? ''}</span> <span class="role">{u.role.replace(/_/g, ' ')}</span> <span class="mono" data-tip={catById.get(u.category_id)?.label}>{u.category_id}</span>{#if u.product_id}<span class="model">{model(u.product_id)}</span>{/if}</div>
						<div>{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title ?? ''}</a>{:else}{s.title ?? ''}{/if}</div>
						<div class="muted small">{[s.venue, s.type].filter(Boolean).join('; ')}</div>
						{#if u.stated_spec}<div class="small">stated: {u.stated_spec}</div>{/if}
						<div class="small muted">{#if s.atlas && u.locator.startsWith('paper record')}<a href={s.atlas[1]} target="_blank" rel="noopener">{u.locator}</a>{:else}{u.locator}{#if s.atlas}; <a href={s.atlas[1]} target="_blank" rel="noopener">{s.atlas[0]}</a>{/if}{/if}</div>
					</div>
				{/each}
			{:else if tab === 'standards' && stdSel}
				<h2 class="mono">{stdSel.designation}</h2>
				<div class="meta muted">{stdSel.body_org_id ? name(stdSel.body_org_id) : 'body not a registry org'}{stdSel.notes ? '; ' + stdSel.notes : ''}</div>
				<h3>Tests citing it ({stdTests.length}, {new Set(stdTests.map((t) => t.source_id)).size} papers)</h3>
				<Chips sets={[{ columns: testCols, filters: tcF }]} onremove={(_, k) => (tcF = drop(tcF, k))} onclear={() => (tcF = {})} />
				<div class="dt"><DataTable columns={testCols} rows={stdTests} rowKey={(t) => t.test_id} rowTip={(t) => [srcTip(t.source_id, t.locator), t.parameter, t.variant, 'printed: ' + t.standard_printed, t.pass_criterion && 'pass: ' + t.pass_criterion, t.result && 'result: ' + t.result].filter(Boolean).join('\n')} bind:filters={tcF} bind:sort={tcS} ownScroll={false} bg="var(--surface)" /></div>
			{:else if tab === 'usage' && cat}
				{@const c = catById.get(cat)}
				<h2><span class="mono">{cat}</span> {c?.label}</h2>
				<p class="muted small">{usageIn.length} stated uses, {vend.length} vendors, {products.length} products. Select a vendor.</p>
			{:else}
				<p class="muted">{tab === 'usage' ? 'Select a category or vendor.' : tab === 'standards' ? 'Select a standard.' : 'Each row is one foundry process as a publication describes it.'}</p>
			{/if}
		</aside>
	</div>
{/if}

<style>
	.page { height: 100%; display: grid; grid-template-columns: 260px minmax(0, 1fr) 400px; grid-template-rows: minmax(0, 1fr); }
	.tree { min-height: 0; overflow: auto; border-right: 1px solid var(--border); background: var(--surface); padding: 4px; }
	.th { display: flex; justify-content: space-between; align-items: center; padding: 2px 4px 4px; font-size: 11px; }
	.th label { display: flex; gap: 4px; align-items: center; }
	.row { display: flex; align-items: center; }
	.tw { width: 16px; height: 20px; padding: 0; border: none; background: transparent; color: var(--ink-3); flex: none; }
	.tw.hide { visibility: hidden; }
	.node { flex: 1; min-width: 0; display: flex; gap: 6px; align-items: center; text-align: left; border: none; background: transparent; height: 20px; padding: 0 4px; }
	.node.on { background: var(--sel); color: var(--ink); }
	.node.empty { color: var(--ink-3); }
	.node .id { flex: none; font-size: 10px; color: var(--ink-3); min-width: 26px; }
	.node .lbl { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.main { min-width: 0; min-height: 0; display: grid; grid-template-rows: auto minmax(0, 1fr); border-right: 1px solid var(--border); }
	.bar { display: flex; gap: 6px; align-items: center; padding: 6px 8px; background: var(--surface); border-bottom: 1px solid var(--border); min-width: 0; }
	.bar input { flex: 1; min-width: 80px; }
	.bar > .muted { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
	.tabs button { height: 24px; font-size: 12px; padding: 0 10px; }
	.scroll { overflow: auto; min-height: 0; }
	.chart { padding: 8px; }
	.tree.off { opacity: 0.45; }
	.model { color: var(--ink); }
	.pl { margin-left: 6px; }
	.sw { display: inline-block; width: 8px; height: 8px; margin-right: 6px; vertical-align: 0; }
	.spaced { display: flex; flex-wrap: wrap; gap: 0 12px; }
	.dt { overflow-x: auto; }
	.split2 { display: grid; grid-template-columns: minmax(0, 1fr) 220px; gap: 0; align-items: start; }
	.split2 .cell { min-width: 0; }
	.types { margin-left: 10px; border-top: 3px solid var(--line); }
	.detail { min-height: 0; overflow: auto; padding: 8px 10px; background: var(--surface); }
	h2 { margin: 0 0 4px; font-size: 14px; }
	h2 .hub { font-size: 11px; font-weight: 400; margin-left: 6px; }
	h3 { margin: 10px 0 4px; font-size: 11px; color: var(--ink-3); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
	.meta { font-size: 11px; }
	.small { font-size: 11px; }
	p { margin: 4px 0; }
	.use { padding: 4px 0; border-bottom: 1px solid var(--grid); }
	.uh { display: flex; gap: 8px; font-size: 11px; }
	.role { color: var(--ink-2); }
	.err { padding: 12px; color: var(--crit); }
	@media (max-width: 1200px) { .page { grid-template-columns: 220px minmax(0, 1fr) 320px; } }
	@media (max-width: 900px) {
		.page { grid-template-columns: minmax(0, 1fr); grid-template-rows: 150px minmax(0, 1fr) 35%; }
		.tree { border-right: none; border-bottom: 1px solid var(--border); }
		.main { border-right: none; }
		.detail { border-top: 1px solid var(--border); }
		.split2 { grid-template-columns: minmax(0, 1fr); }
		.types { margin-left: 0; }
		.bar { flex-wrap: wrap; }
	}
</style>
