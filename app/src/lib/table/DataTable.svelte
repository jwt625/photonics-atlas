<script lang="ts" generics="R">
	// The table of every table page (DevLog-013 D504): sort cycle per header, filter popover per column, windowed rows
	// (grown on scroll), sticky header and first column. Fixed layout: columns do not move when rows arrive or the window
	// grows. Filters and sort live with the page so its bar can list them and a tab switch keeps them.
	import { tick, untrack } from 'svelte';
	import FilterPop from './FilterPop.svelte';
	import { applyFilters, colWidth, enumVals, isActive, mayClip, nextSort, numVals, sortRows, textVal, type Col, type Filter, type Filters, type Sort } from './filters';

	let {
		columns,
		visible,
		rows,
		rowKey,
		selected = '',
		onselect,
		rowTip,
		defaultSort = null,
		tie,
		filters = $bindable({}),
		sort = $bindable(null),
		shown = $bindable(0),
		empty = 'No row matches.',
		page = 300,
		ownScroll = true,
		maxHeight,
		bg = 'var(--bg)',
		reveal = '',
		onrevealed
	}: {
		columns: Col<R>[];
		/** keys shown, in column order; default all */
		visible?: string[];
		rows: R[];
		rowKey: (r: R) => string;
		selected?: string;
		onselect?: (key: string, r: R) => void;
		rowTip?: (r: R) => string | undefined;
		/** order with no header sort active */
		defaultSort?: Sort | null;
		tie?: (a: R, b: R) => number;
		filters?: Filters;
		sort?: Sort | null;
		shown?: number;
		empty?: string;
		page?: number;
		/** false: the page's container scrolls (sticky header sticks to it); all rows render */
		ownScroll?: boolean;
		maxHeight?: string;
		bg?: string;
		/** key of a row to bring into view once, when it appears (deep link); a row click must not set this */
		reveal?: string;
		onrevealed?: () => void;
	} = $props();

	let limit = $state(untrack(() => page));
	let scroller: HTMLDivElement | undefined = $state();
	let tableEl: HTMLTableElement | undefined = $state();
	let openKey = $state('');
	let anchor: HTMLElement | null = $state(null);
	let winW = $state(0);
	const NARROW = 700;

	const shownCols = $derived(visible ? columns.filter((c) => visible.includes(c.key)) : columns);
	const openCol = $derived(columns.find((c) => c.key === openKey));
	const filtered = $derived(applyFilters(rows, columns, filters));
	const sorted = $derived.by(() => {
		const s = sort ?? defaultSort;
		return sortRows(filtered, s ? columns.find((c) => c.key === s.key) : undefined, s?.dir ?? 1, tie);
	});
	const facetRows = $derived(openCol ? applyFilters(rows, columns, filters, openCol.key) : []);
	const win = $derived(ownScroll ? sorted.slice(0, limit) : sorted);

	function cellText(c: Col<R>, r: R): string {
		if (c.text) return c.text(r);
		if (c.kind === 'num') {
			const v = numVals(c, r);
			return v.length ? v.map((x) => (Array.isArray(x) ? x.join('-') : String(x))).join(', ') : '';
		}
		if (c.kind === 'enum') return enumVals(c, r).map((v) => c.enumLabel?.(v) ?? v).join(', ');
		return textVal(c, r);
	}

	// widest text seen per column; a width never shrinks, so a search or filter does not move columns either
	const seen = new Map<string, number>();
	const SAMPLE = 1500;
	const widths = $derived.by(() => {
		const rs = rows;
		return untrack(() => {
			const out: Record<string, number> = {};
			for (const c of shownCols) {
				if (c.w) {
					out[c.key] = c.w;
					continue;
				}
				let n = seen.get(c.key) ?? 0;
				for (let i = 0; i < rs.length && i < SAMPLE; i++) {
					const l = cellText(c, rs[i]).length + (c.badge ? 1 : 0) + (c.more && c.more(rs[i]) ? 3 : 0);
					if (l > n) n = l;
				}
				seen.set(c.key, n);
				out[c.key] = colWidth(c, n);
			}
			// on a phone the first column leaves room for the others
			const first = shownCols[0];
			if (first && winW && winW <= NARROW) out[first.key] = Math.min(out[first.key], Math.round(winW * 0.42));
			return out;
		});
	});
	const total = $derived(shownCols.reduce((t, c) => t + (widths[c.key] ?? 80), 0));

	$effect(() => {
		shown = sorted.length;
	});
	let firstRun = true;
	$effect(() => {
		void filters, sort;
		limit = page;
		if (firstRun) {
			firstRun = false;
			return;
		}
		untrack(toTop);
	});
	/** Sort or filter changed: the reader wants the first rows, not the old offset. */
	function toTop() {
		if (scroller) {
			scroller.scrollTop = 0;
			return;
		}
		let p = tableEl?.parentElement;
		while (p && !/(auto|scroll)/.test(getComputedStyle(p).overflowY)) p = p.parentElement;
		if (!p || !tableEl) return;
		const top = tableEl.getBoundingClientRect().top - p.getBoundingClientRect().top + p.scrollTop;
		if (p.scrollTop > top) p.scrollTop = top;
	}
	$effect(() => {
		const k = reveal;
		if (!k) return;
		const i = sorted.findIndex((r) => rowKey(r) === k);
		if (i < 0) return;
		untrack(() => {
			if (i >= limit) limit = i + 50;
			onrevealed?.();
			tick().then(() => {
				const tr = tableEl?.querySelector(`[data-k="${CSS.escape(k)}"]`) as HTMLElement | null;
				if (tr && scroller) scroller.scrollTop = tr.offsetTop - scroller.clientHeight / 2;
			});
		});
	});

	function onScroll(e: Event) {
		const el = e.currentTarget as HTMLElement;
		if (limit < sorted.length && el.scrollTop + el.clientHeight > el.scrollHeight - 400) limit += page;
	}
	function setFilter(key: string, f: Filter | null) {
		const next = { ...filters };
		if (f) next[key] = f;
		else delete next[key];
		filters = next;
	}
	function openFilter(e: MouseEvent, key: string) {
		e.stopPropagation();
		if (openKey === key) {
			openKey = '';
			return;
		}
		anchor = e.currentTarget as HTMLElement;
		openKey = key;
	}
	const cycle = (c: Col<R>) => (sort = nextSort(sort, c));
	/** Enter or Space on the element itself, not on a control inside it. */
	const onKey = (e: KeyboardEvent, f: () => void) => {
		if ((e.key === 'Enter' || e.key === ' ') && e.target === e.currentTarget) {
			e.preventDefault();
			f();
		}
	};
	const caret = (c: Col<R>) => (sort?.key === c.key ? (sort.dir === 1 ? ' ^' : ' v') : '');
	const ariaSort = (c: Col<R>) => (sort?.key === c.key ? (sort.dir === 1 ? 'ascending' : 'descending') : undefined);
	function tipOf(c: Col<R>, r: R): string | undefined {
		const t = c.cellTip?.(r);
		if (t) return t;
		const x = cellText(c, r);
		return x && mayClip(x.length, widths[c.key] ?? 80) ? x : undefined;
	}
</script>

<svelte:window bind:innerWidth={winW} />

{#snippet table()}
	<table class="t num" class:click={!!onselect} bind:this={tableEl} style:--tbg={bg} style:min-width="{total}px">
		<colgroup>{#each shownCols as c (c.key)}<col style:width="{widths[c.key] ?? 80}px" />{/each}</colgroup>
		<thead>
			<tr>
				{#each shownCols as c (c.key)}
					<th class:r={c.right} class:act={isActive(filters[c.key])} aria-sort={ariaSort(c)} data-tip={c.tip} tabindex="0" onclick={() => cycle(c)} onkeydown={(e) => onKey(e, () => cycle(c))}>
						<span class="th"><span class="tl">{c.label}{#if c.unit}<span class="u">{c.unit}</span>{/if}{caret(c)}</span>{#if c.kind !== 'none'}<button class="fn" class:on={isActive(filters[c.key])} onclick={(e) => openFilter(e, c.key)} aria-label="Filter {c.label}"><svg viewBox="0 0 8 8" width="8" height="8"><path d="M0 0.5h8L5 4v3.5L3 6.5V4z" fill="currentColor" /></svg></button>{/if}</span>
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each win as r (rowKey(r))}
				{@const k = rowKey(r)}
				<tr class:sel={!!selected && k === selected} data-k={k} data-tip={rowTip?.(r)} tabindex={onselect ? 0 : undefined} onclick={() => onselect?.(k, r)} onkeydown={onselect ? (e) => onKey(e, () => onselect?.(k, r)) : undefined}>
					{#each shownCols as c (c.key)}
						<td class={c.cls} class:r={c.right} data-tip={tipOf(c, r)}>
							{#if c.cell}{@render c.cell(r)}{:else}{cellText(c, r)}{#if c.badge?.(r)}<sup class="b" class:m={c.badgeOn?.(r)}>{c.badge(r)}</sup>{/if}{#if c.more?.(r)}<span class="more">+{c.more(r)}</span>{/if}{/if}
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
	{#if !sorted.length && empty}<p class="muted pad">{empty}</p>{/if}
{/snippet}

{#if ownScroll}
	<div class="scroll" bind:this={scroller} onscroll={onScroll} style:max-height={maxHeight}>{@render table()}</div>
{:else}
	{@render table()}
{/if}
{#if openCol && anchor}
	{#key openKey}
		{@const k = openKey}
		<FilterPop col={openCol} rows={facetRows} filter={filters[k]} {anchor} onchange={(f) => setFilter(k, f)} onclose={() => { if (openKey === k) openKey = ''; }} />
	{/key}
{/if}

<style>
	.scroll { overflow: auto; min-height: 0; height: 100%; }
	table.t { border-collapse: separate; border-spacing: 0; width: 100%; table-layout: fixed; }
	.t th, .t td { padding: 2px 6px; border-bottom: 1px solid var(--grid); text-align: left; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.t th { position: sticky; top: 0; z-index: 2; background: var(--surface); color: var(--ink-3); font-weight: 500; cursor: pointer; user-select: none; white-space: normal; vertical-align: bottom; }
	.t th.act { color: var(--accent); }
	.t th:first-child { left: 0; z-index: 3; }
	.t td:first-child { position: sticky; left: 0; z-index: 1; background-color: var(--tbg); }
	.t .r { text-align: right; }
	.th { display: inline-flex; align-items: center; gap: 3px; max-width: 100%; }
	.tl { min-width: 0; overflow-wrap: anywhere; }
	.u { margin-left: 3px; color: var(--ink-3); font-weight: 400; }
	.t th.act .u { color: inherit; }
	/* --ink-3 is at least 3:1 against the header in both themes */
	.fn { height: 14px; width: 14px; padding: 0; display: inline-flex; align-items: center; justify-content: center; border: none; background: transparent; color: var(--ink-3); flex: none; }
	.fn:hover { color: var(--ink); background: var(--hover); }
	.fn.on, .fn.on:hover { color: var(--accent-ink); background: var(--accent); }
	.t.click tbody tr { cursor: pointer; }
	.t tbody tr:hover td { background-image: linear-gradient(var(--hover), var(--hover)); }
	.t tbody tr.sel td { background-image: linear-gradient(var(--sel), var(--sel)); }
	.b { margin-left: 2px; font-size: 8px; line-height: 0; color: var(--ink-3); font-weight: 700; }
	.b.m { color: var(--accent); }
	.more { margin-left: 3px; font-size: 10px; color: var(--ink-3); }
	.pad { padding: 12px; }
	.t td:global(.wrap) { white-space: normal; overflow-wrap: anywhere; }
	.t td:global(.mono) { font-family: var(--mono); }
	@media (max-width: 700px) {
		.t th:first-child { left: auto; }
		.t td:first-child { position: static; }
	}
</style>
