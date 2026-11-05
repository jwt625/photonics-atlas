<script lang="ts">
	// Which columns a table shows (DevLog-013 D502): every parameter of the selection with its coverage.
	import { onMount, tick } from 'svelte';
	import type { Choice } from './filters';

	let { choices, visible, total, onchange, onreset }: { choices: Choice[]; visible: string[]; total: number; onchange: (keys: string[]) => void; onreset: () => void } = $props();

	let btn: HTMLButtonElement | undefined = $state();
	let el: HTMLDivElement | undefined = $state();
	let open = $state(false);
	let search = $state('');
	let left = $state(-9999);
	let top = $state(0);

	const groups = $derived.by(() => {
		const q = search.trim().toLowerCase();
		const m = new Map<string, Choice[]>();
		for (const c of choices) {
			if (q && !(c.label + ' ' + c.key).toLowerCase().includes(q)) continue;
			m.set(c.group, [...(m.get(c.group) ?? []), c]);
		}
		return [...m];
	});
	const nOn = $derived(choices.filter((c) => visible.includes(c.key)).length);
	const toggle = (k: string) => onchange(visible.includes(k) ? visible.filter((x) => x !== k) : [...visible, k]);

	async function show() {
		open = !open;
		if (!open) return;
		await tick();
		if (!el || !btn) return;
		const a = btn.getBoundingClientRect();
		left = Math.max(4, Math.min(a.right - el.offsetWidth, innerWidth - el.offsetWidth - 4));
		top = a.bottom + 2;
		el.querySelector('input')?.focus();
	}
	onMount(() => {
		const down = (e: PointerEvent) => {
			const t = e.target as Node;
			if (open && !el?.contains(t) && !btn?.contains(t)) open = false;
		};
		const key = (e: KeyboardEvent) => {
			if (e.key === 'Escape' && open) {
				open = false;
				btn?.focus();
			}
		};
		document.addEventListener('pointerdown', down, true);
		document.addEventListener('keydown', key);
		return () => {
			document.removeEventListener('pointerdown', down, true);
			document.removeEventListener('keydown', key);
		};
	});
</script>

<button class="cc" bind:this={btn} onclick={show} data-tip="Choose columns">Columns <span class="muted num">{nOn}/{choices.length}</span></button>
{#if open}
	<div class="pop" bind:this={el} style:left="{left}px" style:top="{top}px" role="dialog" aria-label="Columns">
		<div class="ph">
			<input type="search" placeholder="Search columns" bind:value={search} />
			<button class="rs" onclick={onreset} data-tip="Back to the columns reported by at least 10 % of this selection">default</button>
		</div>
		<div class="list">
			{#each groups as [g, cs]}
				<div class="g">{g}</div>
				{#each cs as c (c.key)}
					<label class="opt" data-tip={c.tip}><input type="checkbox" checked={visible.includes(c.key)} onchange={() => toggle(c.key)} /><span class="ol">{c.label}{#if c.unit} <span class="muted">{c.unit}</span>{/if}</span>{#if c.n !== undefined}<span class="muted num">{c.n}/{total}</span>{/if}</label>
				{/each}
			{/each}
		</div>
	</div>
{/if}

<style>
	.cc { flex: none; }
	.pop { position: fixed; z-index: 50; width: min(300px, calc(100vw - 8px)); padding: 6px; display: flex; flex-direction: column; gap: 4px; background: var(--surface); border: 1px solid var(--line); box-shadow: 0 3px 10px rgba(0, 0, 0, 0.35); }
	.ph { display: flex; gap: 4px; }
	.ph input { flex: 1; }
	.rs { height: 24px; font-size: 11px; }
	.list { max-height: min(440px, 70vh); overflow: auto; }
	.g { margin-top: 4px; font-size: 10px; color: var(--ink-3); text-transform: uppercase; letter-spacing: 0.04em; }
	.opt { display: flex; align-items: center; gap: 6px; height: 20px; padding: 0 2px; cursor: pointer; }
	.opt:hover { background: var(--hover); }
	.ol .muted { margin-left: 3px; }
	.ol { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
