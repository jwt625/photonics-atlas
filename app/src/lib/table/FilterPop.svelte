<script lang="ts" generics="R">
	// Filter popover of one column (DevLog-013 D504). Fixed position, so no scroll container clips it.
	import { onMount, tick, untrack } from 'svelte';
	import { facets, numStats, type Col, type Filter } from './filters';

	let {
		col,
		rows,
		filter,
		anchor,
		onchange,
		onclose
	}: { col: Col<R>; rows: R[]; filter: Filter | undefined; anchor: HTMLElement; onchange: (f: Filter | null) => void; onclose: () => void } = $props();

	let el: HTMLDivElement | undefined = $state();
	let left = $state(-9999);
	let top = $state(0);
	let search = $state('');
	const MAX_OPTS = 300;

	const sel = $derived(filter?.t === 'enum' ? filter.sel : []);
	const opts = $derived(col.kind === 'enum' ? facets(rows, col, sel) : []);
	const shownOpts = $derived.by(() => {
		const q = search.trim().toLowerCase();
		const f = q ? opts.filter((o) => o.label.toLowerCase().includes(q)) : opts;
		return f.slice(0, MAX_OPTS);
	});
	const stats = $derived(col.kind === 'num' ? numStats(rows, col) : null);
	const histMax = $derived(stats ? Math.max(...stats.hist, 1) : 1);

	function toggle(v: string) {
		const next = sel.includes(v) ? sel.filter((x) => x !== v) : [...sel, v];
		onchange(next.length ? { t: 'enum', sel: next } : null);
	}
	// inputs start from the filter when the popover opens, then own their text
	const initial = untrack(() => filter);
	let minS = $state(initial?.t === 'num' && initial.min !== null ? String(initial.min) : '');
	let maxS = $state(initial?.t === 'num' && initial.max !== null ? String(initial.max) : '');
	let textS = $state(initial?.t === 'text' ? initial.q : '');
	let timer: ReturnType<typeof setTimeout> | null = null;
	const later = (f: () => void) => {
		if (timer) clearTimeout(timer);
		timer = setTimeout(() => {
			timer = null;
			f();
		}, 300);
	};
	const parse = (s: string): number | null => {
		const t = s.trim();
		if (t === '') return null;
		const v = Number(t);
		return Number.isFinite(v) ? v : null;
	};
	const bad = (s: string) => s.trim() !== '' && parse(s) === null;
	const rangeMsg = $derived.by(() => {
		if (bad(minS) || bad(maxS)) return 'Not a number: ignored';
		const a = parse(minS),
			b = parse(maxS);
		return a !== null && b !== null && a > b ? 'Min is above max: no row can match' : '';
	});
	const pushRange = () => {
		const min = parse(minS),
			max = parse(maxS);
		onchange(min === null && max === null ? null : { t: 'num', min, max });
	};
	const pushText = () => onchange(textS.trim() ? { t: 'text', q: textS } : null);
	/** Typed text still waiting for its debounce goes in now. */
	const flush = () => {
		if (!timer) return;
		clearTimeout(timer);
		timer = null;
		if (col.kind === 'num') pushRange();
		else if (col.kind === 'text') pushText();
	};
	function clear() {
		if (timer) clearTimeout(timer);
		timer = null;
		minS = maxS = textS = '';
		onchange(null);
	}
	const fmt = (x: number) => String(+x.toPrecision(5));

	function place() {
		if (!el) return;
		const a = anchor.getBoundingClientRect();
		const w = el.offsetWidth,
			h = el.offsetHeight;
		left = Math.max(4, Math.min(a.left, innerWidth - w - 4));
		top = a.bottom + 2 + h > innerHeight - 4 ? Math.max(4, a.top - h - 2) : a.bottom + 2;
	}
	onMount(() => {
		tick().then(() => {
			place();
			el?.querySelector('input')?.focus();
		});
		const down = (e: PointerEvent) => {
			const t = e.target as Node;
			if (el?.contains(t) || anchor.contains(t)) return;
			onclose();
		};
		const key = (e: KeyboardEvent) => {
			// Enter on a button is the button's own click (clear)
			if (e.key === 'Escape' || (e.key === 'Enter' && !(e.target instanceof HTMLButtonElement))) {
				onclose();
				anchor.focus();
			}
		};
		// the anchor moved with the table: close instead of floating away from it
		const opened = performance.now();
		const scrolled = (e: Event) => {
			const t = e.target as Node;
			if (el?.contains(t) || !(t === document || t.contains?.(anchor))) return;
			// the scroll that brought the button into view before its click lands just after the popover opened
			if (performance.now() - opened < 200) place();
			else onclose();
		};
		const resized = () => onclose();
		document.addEventListener('pointerdown', down, true);
		document.addEventListener('keydown', key);
		document.addEventListener('scroll', scrolled, true);
		window.addEventListener('resize', resized);
		return () => {
			document.removeEventListener('pointerdown', down, true);
			document.removeEventListener('keydown', key);
			document.removeEventListener('scroll', scrolled, true);
			window.removeEventListener('resize', resized);
			flush(); // closing never loses typed text
		};
	});
</script>

<div class="pop" bind:this={el} style:left="{left}px" style:top="{top}px" role="dialog" aria-label="Filter {col.label}">
	<div class="ph">
		<span class="tt">{col.label}{#if col.unit} <span class="muted">{col.unit}</span>{/if}</span>
		<button class="cl" onclick={clear} disabled={!filter}>clear</button>
	</div>
	{#if col.kind === 'enum'}
		<input type="search" placeholder="Search {opts.length} values" bind:value={search} />
		<div class="opts">
			{#each shownOpts as o (o.value)}
				<label class="opt" data-tip={o.label.length > 40 ? o.label : undefined}><input type="checkbox" checked={sel.includes(o.value)} onchange={() => toggle(o.value)} /><span class="ol">{o.label}</span><span class="muted num">{o.n}</span></label>
			{/each}
			{#if !shownOpts.length}<div class="muted none">No value</div>{/if}
		</div>
		{#if opts.length > MAX_OPTS && !search}<div class="muted hint">First {MAX_OPTS} of {opts.length}; search for the rest</div>{/if}
	{:else if col.kind === 'num'}
		{#if stats}
			<div class="hist" data-tip={`${stats.cells} rows with a value${stats.log ? '; log bins' : ''}`}>
				{#each stats.hist as n}<i style:height="{(100 * n) / histMax}%"></i>{/each}
			</div>
		{/if}
		<div class="range">
			<input class:bad={bad(minS)} type="text" inputmode="decimal" placeholder={stats ? fmt(stats.min) : 'min'} bind:value={minS} oninput={() => later(pushRange)} aria-label="Minimum" />
			<span class="muted">to</span>
			<input class:bad={bad(maxS)} type="text" inputmode="decimal" placeholder={stats ? fmt(stats.max) : 'max'} bind:value={maxS} oninput={() => later(pushRange)} aria-label="Maximum" />
		</div>
		{#if rangeMsg}<div class="msg">{rangeMsg}</div>{/if}
	{:else}
		<input type="search" placeholder="Contains" bind:value={textS} oninput={() => later(pushText)} />
	{/if}
</div>

<style>
	.pop { position: fixed; z-index: 50; width: min(260px, calc(100vw - 8px)); padding: 6px; display: flex; flex-direction: column; gap: 4px; background: var(--surface); border: 1px solid var(--line); box-shadow: 0 3px 10px rgba(0, 0, 0, 0.35); }
	.ph { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
	.tt .muted { margin-left: 3px; }
	.tt { color: var(--ink-2); font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.cl { height: 18px; padding: 0 6px; font-size: 11px; }
	.cl:disabled { color: var(--ink-3); cursor: default; }
	input[type='search'], input[type='text'] { width: 100%; }
	.opts { max-height: 280px; overflow: auto; display: flex; flex-direction: column; }
	.opt { display: flex; align-items: center; gap: 6px; height: 20px; padding: 0 2px; cursor: pointer; }
	.opt:hover { background: var(--hover); }
	.ol { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
	.none, .hint { padding: 2px; font-size: 11px; }
	.hist { display: flex; align-items: flex-end; gap: 1px; height: 36px; border-bottom: 1px solid var(--line); }
	.hist i { flex: 1; min-width: 0; background: var(--accent); }
	.range { display: flex; align-items: center; gap: 6px; }
	.bad { border-color: var(--crit); }
	.msg { font-size: 11px; color: var(--crit); }
</style>
