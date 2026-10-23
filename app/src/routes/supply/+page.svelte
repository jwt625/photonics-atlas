<script lang="ts">
	// Supply-chain view (DevLog-010 D190, D194, D195): category tree A-K -> vendor -> usage rows -> papers; foundry
	// process observations; standards and reliability tests. Hash state: tab, cat, org, std.
	import { onMount } from 'svelte';
	import { link } from '../../lib/paths';
	import { store, ui } from '../../lib/state.svelte';
	import { loadSupply, sup, type Row, type Usage } from '../../lib/supply.svelte';
	import { slotColor } from '../../lib/explore/colors';
	import StackBars from '../../lib/StackBars.svelte';
	import { descendants, OTHER, rollup, shareByYear, siblingPaper, split, vendors, yearOf } from '../../lib/views';

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
	const name = (id: string) => store.byId.get(id)?.name ?? id;
	const cats = $derived(view?.categories ?? []);
	const catById = $derived(new Map(cats.map((c) => [c.id, c])));
	const counts = $derived(view ? rollup(cats, view.usage) : new Map<string, number>());
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
	const vend = $derived(view ? vendors(usageIn, view.sources, null).filter((v) => !q || fold(name(v.org) + ' ' + v.org).includes(fold(q))) : []);
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
		(view?.processes ?? []).filter((p) => !q || fold([name(p.org_id), p.process_name, p.platform, p.pdk_name, p.source_id].join(' ')).includes(fold(q)))
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
	const srcTip = (sid: string) => {
		const s = src(sid);
		return [sid, s.title, [s.venue, s.year].filter(Boolean).join(', '), s.access && 'access ' + s.access].filter(Boolean).join('\n');
	};
	const uTip = (u: Usage) => [u.usage_id, 'basis ' + u.basis + ', extraction ' + u.extraction, 'verified ' + u.verified_on, u.notes].filter(Boolean).join('\n');
	const range = (t: Row) => (t.t_min_c || t.t_max_c ? `${t.t_min_c ?? ''} to ${t.t_max_c ?? ''} C` : t.temp_c ? `${t.temp_c} C` : '') + (t.rh_pct ? ` / ${t.rh_pct} %RH` : '');
</script>

<svelte:window bind:innerWidth={winW} />

{#if sup.error}
	<div class="err">{sup.error}</div>
{:else if view}
	<div class="page">
		<aside class="tree" class:off={tab !== 'usage'} inert={tab !== 'usage'} data-tip={tab !== 'usage' ? 'Categories apply to the Usage tab' : undefined}>
			<div class="th">
				<span class="muted" data-tip="Category tree A-K (DevLog-003 D52); counts are product_usage rows in the subtree">Categories</span>
				<label class="muted" data-tip="Show categories without usage rows"><input type="checkbox" bind:checked={showEmpty} /> empty</label>
			</div>
			<button class="node" class:on={!cat} onclick={() => set('cat', '')}><span class="lbl">All categories</span><span class="num">{view.usage.length}</span></button>
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
					<button class:on={tab === 'usage'} onclick={() => set('tab', 'usage')} data-tip="Vendors per category with the papers that state their use">Usage</button><button class:on={tab === 'processes'} onclick={() => set('tab', 'processes')} data-tip="Per-source foundry process observations (DevLog-003 D58)">Processes</button><button class:on={tab === 'standards'} onclick={() => set('tab', 'standards')} data-tip="Standards cited by packaging reliability tests (D59, D60)">Standards</button>
				</span>
				<input type="search" placeholder={tab === 'usage' ? 'Filter vendors' : tab === 'processes' ? 'Filter org, process, platform, PDK' : 'Filter designation, body'} value={qLive} oninput={(e) => onInput(e.currentTarget.value)} onkeydown={(e) => e.key === 'Enter' && (q = qLive)} />
				{#if tab === 'usage'}
					<span class="muted num" data-tip="vendors / usage rows in the selected category subtree; products recorded (products.csv)">{vend.length} vendors, {usageIn.length} rows, {products.length} products</span>
				{:else if tab === 'processes'}
					<span class="muted num">{procs.length} / {view.processes.length}</span>
				{:else}
					<span class="muted num" data-tip="standards / reliability test rows; rows whose printed standard has no parsed designation">{view.standards.length} standards, {view.tests.length} tests, {unparsed} unparsed</span>
				{/if}
			</div>
			<div class="scroll">
				{#if tab === 'usage'}
					{#if share}
						<div class="chart">
							<StackBars
								letter="a"
								desc="Usage rows (one per source x org x role fact) per source year in the selected category subtree, stacked by vendor; the six vendors with most rows keep their own colour (ordered by id), the rest are grey. Counts of stated use in the papers, not market share."
								badge={`${share.total - share.noYear}/${share.total}`}
								badgeTip={`${share.total - share.noYear} of ${share.total} usage rows plotted; ${share.noYear} without a source year`}
								years={share.years}
								{series}
								yTitle="Usage rows (count)"
								unit="rows"
								height={narrow ? 170 : 300}
								legend={!narrow}
							/>
						</div>
					{/if}
					<table class="t num click">
						<thead><tr><th>Vendor</th><th>Type</th><th>CC</th><th class="r" data-tip="usage rows">Rows</th><th class="r" data-tip="distinct sources">Papers</th><th>Roles</th><th>Categories</th><th data-tip="source years">Years</th></tr></thead>
						<tbody>
							{#each vend as v (v.org)}
								{@const o = store.byId.get(v.org)}
								<tr class:sel={v.org === org} onclick={() => set('org', v.org === org ? '' : v.org)}>
									<td class="name" data-tip={v.org}><span class="sw" style:background={swatch(v.org)}></span>{name(v.org)}</td><td>{o?.type ?? ''}</td><td>{o?.country ?? ''}</td>
									<td class="r">{v.rows}</td><td class="r">{v.sources}</td><td>{v.roles.join(', ')}</td>
									<td data-tip={v.cats.map((c) => c + ' ' + (catById.get(c)?.label ?? '')).join('\n')}>{v.cats.join(', ')}</td>
									<td>{v.y0 === null ? '' : v.y0 === v.y1 ? v.y0 : `${v.y0}-${v.y1}`}</td>
								</tr>
							{/each}
						</tbody>
					</table>
					{#if !vend.length}<p class="muted pad">No usage rows in this category.</p>{/if}
				{:else if tab === 'processes'}
					<table class="t num">
						<thead><tr><th>Org</th><th>Process (as printed)</th><th>Platform</th><th class="r" data-tip="nominal wafer diameter (mm)">Wafer mm</th><th>PDK</th><th data-tip="PDK stated open">Open</th><th>Access</th><th>Broker</th><th>Source</th><th>Loc</th></tr></thead>
						<tbody>
							{#each procs as p (p.process_id)}
								<tr data-tip={[p.process_id, p.notes].filter(Boolean).join('\n')}>
									<td class="name"><a href={link('/orgs/hub') + '?id=' + encodeURIComponent(p.org_id)}>{name(p.org_id)}</a></td>
									<td class="wrap">{p.process_name}</td><td>{p.platform ?? ''}</td><td class="r">{p.wafer_mm ?? ''}</td><td>{p.pdk_name ?? ''}</td><td>{p.pdk_open ?? ''}</td><td>{p.access_route ?? ''}</td>
									<td>{p.broker_org_id ? name(p.broker_org_id) : ''}</td>
									<td data-tip={srcTip(p.source_id)}>{p.source_id} <span class="muted">{src(p.source_id).year ?? ''}</span></td><td class="loc" data-tip={p.locator}>{p.locator}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{:else}
					<div class="split2">
						<div class="cell">
							<table class="t num click">
								<thead><tr><th>Designation</th><th>Body</th><th class="r" data-tip="reliability test rows citing the designation">Tests</th><th class="r">Papers</th><th>Access</th></tr></thead>
								<tbody>
									{#each stds as { s, n, papers } (s.standard_id)}
										<tr class:sel={s.standard_id === std} onclick={() => set('std', s.standard_id === std ? '' : s.standard_id)} data-tip={[s.standard_id, s.title, s.notes].filter(Boolean).join('\n')}>
											<td class="mono">{s.designation}</td><td>{s.body_org_id ? name(s.body_org_id) : ''}</td><td class="r">{n}</td><td class="r">{papers}</td><td>{s.access ?? ''}</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
						<div class="cell types">
							<table class="t num">
								<thead><tr><th data-tip="stress type (D60); measurement types where no stress is named">Test type</th><th class="r">Tests</th></tr></thead>
								<tbody>{#each typeCounts as [t, n]}<tr><td>{t}</td><td class="r">{n}</td></tr>{/each}</tbody>
							</table>
						</div>
					</div>
				{/if}
			</div>
		</div>
		<aside class="detail">
			{#if tab === 'usage' && org}
				{@const o = store.byId.get(org)}
				<h2>{name(org)} <a class="hub" href={link('/orgs/hub') + '?id=' + encodeURIComponent(org)} data-tip="All lenses for this organization">hub</a></h2>
				<div class="meta muted spaced">
					{#if [o?.type, o?.country].some((x) => x && x !== 'unknown')}<span>{[o?.type, o?.country].filter((x) => x && x !== 'unknown').join(', ')}</span>{/if}
					<span>{cat ? cat + ': ' : ''}{orgRows.length} of {orgAll} usage rows</span>
				</div>
				<h3>Products</h3>
				{#if products.length}
					<table class="t num prods">
						<tbody>
							{#each products as p (p.product_id)}
								<tr class:sel={prod === p.product_id} class="click" onclick={() => (prod = prod === p.product_id ? '' : p.product_id)} data-tip={[p.product_id, p.status && 'status ' + p.status, p.notes].filter(Boolean).join('\n')}>
									<td>{p.model}{#if p.product_line}<span class="muted pl">{p.product_line}</span>{/if}</td><td class="mono" data-tip={catById.get(p.category_id)?.label}>{p.category_id}</td><td class="r" data-tip="usage rows naming this product">{prodRows(p.product_id) || ''}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				{:else}
					<p class="muted small" data-tip="no product rows for this vendor{cat ? ' in this category' : ''}">none recorded</p>
				{/if}
				<h3>Used in{#if prod} <span class="muted">{model(prod)}</span>{/if}</h3>
				{#each shownRows as u (u.usage_id)}
					{@const s = src(u.source_id)}
					{@const sib = siblingPaper(u.source_id)}
					<div class="use" data-tip={uTip(u)}>
						<div class="uh"><span class="num">{s.year ?? ''}</span> <span class="role">{u.role}</span> <span class="mono" data-tip={catById.get(u.category_id)?.label}>{u.category_id}</span>{#if u.product_id}<span class="model" data-tip={u.product_id}>{model(u.product_id)}</span>{/if}</div>
						<div>{#if s.url}<a href={s.url} target="_blank" rel="noopener">{s.title ?? u.source_id}</a>{:else}{s.title ?? u.source_id}{/if}</div>
						<div class="muted small">{s.venue ?? ''}</div>
						{#if u.stated_spec}<div class="small">stated: {u.stated_spec}</div>{/if}
						<div class="small muted">{u.source_id}; {u.locator}{#if sib}; <a href={sib.href} target="_blank" rel="noopener">{sib.site}</a>{/if}</div>
					</div>
				{/each}
			{:else if tab === 'standards' && stdSel}
				<h2 class="mono">{stdSel.designation}</h2>
				<div class="meta muted">{stdSel.body_org_id ? name(stdSel.body_org_id) : 'body not a registry org'}{stdSel.notes ? '; ' + stdSel.notes : ''}</div>
				<h3>Tests citing it ({stdTests.length}, {new Set(stdTests.map((t) => t.source_id)).size} papers)</h3>
				<table class="t num">
					<thead><tr><th data-tip="stress type; measurand after the slash">type</th><th>condition</th><th class="r">value</th></tr></thead>
					<tbody>
						{#each stdTests as t (t.test_id)}
							<tr data-tip={[srcTip(t.source_id), t.test_id, t.parameter, t.variant, 'printed: ' + t.standard_printed, t.pass_criterion && 'pass: ' + t.pass_criterion, t.result && 'result: ' + t.result, 'locator ' + t.locator, t.notes].filter(Boolean).join('\n')}>
								<td>{t.test_type}{t.measurand && t.measurand !== t.test_type ? ' / ' + t.measurand : ''}</td>
								<td>{range(t)}</td>
								<td class="r">{t.value ?? t.value_text ?? ''} {t.unit ?? ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{:else if tab === 'usage' && cat}
				{@const c = catById.get(cat)}
				<h2><span class="mono">{cat}</span> {c?.label}</h2>
				<p class="muted small">{usageIn.length} usage rows, {vend.length} vendors, {products.length} products. Select a vendor.</p>
			{:else}
				<p class="muted">{tab === 'usage' ? 'Select a category or vendor.' : tab === 'standards' ? 'Select a standard.' : 'Process observations are per source (D58): identity between rows is not asserted.'}</p>
			{/if}
		</aside>
	</div>
{:else}
	<div class="pad muted">loading</div>
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
	.pad { padding: 12px; }
	table.t { border-collapse: collapse; width: 100%; }
	.t th, .t td { padding: 2px 6px; border-bottom: 1px solid var(--grid); text-align: left; white-space: nowrap; }
	.t th { position: sticky; top: 0; background: var(--surface); color: var(--ink-3); font-weight: 500; }
	.t .r { text-align: right; }
	.t td.name { max-width: 260px; overflow: hidden; text-overflow: ellipsis; }
	.t td.wrap { white-space: normal; min-width: 220px; max-width: 420px; }
	.t td.loc { max-width: 200px; overflow: hidden; text-overflow: ellipsis; }
	.t.click tbody tr, .t tr.click { cursor: pointer; }
	.tree.off { opacity: 0.45; }
	.model { color: var(--ink); }
	.pl { margin-left: 6px; }
	.sw { display: inline-block; width: 8px; height: 8px; margin-right: 6px; vertical-align: 0; }
	.spaced { display: flex; flex-wrap: wrap; gap: 0 12px; }
	.prods td { white-space: normal; }
	.t tbody tr:hover { background: var(--hover); }
	.t tbody tr.sel { background: var(--sel); }
	.split2 { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 0; align-items: start; }
	.split2 .cell { min-width: 0; overflow-x: auto; }
	.types { border-left: 1px solid var(--border); }
	.detail { min-height: 0; overflow: auto; padding: 8px 10px; background: var(--surface); }
	.detail .t th { position: static; }
	.detail .t td { white-space: normal; }
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
		.bar > .muted { display: none; }
	}
</style>
