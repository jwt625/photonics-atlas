<script lang="ts">
	import '../app.css';
	import { onMount, type Snippet } from 'svelte';
	import { link } from '../lib/paths';
	import { page } from '$app/state';
	import { loadRegistry, store, ui } from '../lib/state.svelte';
	import ThemeToggle from '../lib/ThemeToggle.svelte';
	import Tooltip from '../lib/Tooltip.svelte';

	let { children }: { children: Snippet } = $props();

	const nav = [
		{ href: '/', label: 'Dashboard' },
		{ href: '/orgs', label: 'Organizations' },
		{ href: '/components', label: 'Components' },
		{ href: '/supply', label: 'Supply' },
		{ href: '/people', label: 'People' },
		{ href: '/layout', label: 'Layouts' },
		{ href: '/explore', label: 'Explore' },
		{ href: '/about', label: 'About' }
	];

	onMount(() => {
		const t = document.documentElement.getAttribute('data-theme');
		ui.theme = t === 'light' ? 'light' : 'dark';
		loadRegistry();
	});

	const isActive = (href: string) => {
		const root = link('/').replace(/\/$/, '');
		const p = page.url.pathname.replace(root, '') || '/';
		return href === '/' ? p === '/' : p.startsWith(href);
	};
</script>

<div class="app">
	<header>
		<a class="brand" href={link('/')} data-tip="Shared registry for the PIC component, supply-chain and people atlases">Photonics Atlas</a>
		<nav>
			{#each nav as n}
				<a href={link(n.href)} class:active={isActive(n.href)}>{n.label}</a>
			{/each}
		</nav>
		<div class="grow"></div>
		{#if store.reg}
			<span class="muted num" data-tip="Organizations / sources in the loaded registry">
				{store.reg.counts.organizations} orgs, {store.reg.counts.sources} sources
			</span>
		{:else if store.loading}
			<span class="spinner"></span>
		{/if}
		<ThemeToggle />
	</header>
	<main>
		{#if store.error}
			<div class="err">Could not load the registry: {store.error}</div>
		{:else}
			{@render children()}
		{/if}
	</main>
	<Tooltip />
	<footer>
		Created by Wentao Jiang
		<span class="sep">|</span><a href="https://outside5sigma.com" target="_blank" rel="noopener">homepage</a>
		<span class="sep">|</span><a href="https://github.com/jwt625/photonics-atlas" target="_blank" rel="noopener">GitHub</a>
	</footer>
</div>

<style>
	.app { height: 100vh; display: grid; grid-template-columns: minmax(0, 1fr); grid-template-rows: var(--hdr) minmax(0, 1fr) auto; }
	header { min-width: 0; display: flex; align-items: center; gap: 14px; padding: 0 10px; background: var(--surface); border-bottom: 1px solid var(--border); }
	.brand { color: var(--ink); font-weight: 600; letter-spacing: 0.02em; white-space: nowrap; }
	.brand:hover { text-decoration: none; }
	nav { display: flex; gap: 2px; height: 100%; }
	nav a { display: flex; align-items: center; padding: 0 10px; color: var(--ink-2); border-bottom: 2px solid transparent; }
	nav a:hover { background: var(--hover); text-decoration: none; }
	nav a.active { color: var(--ink); border-bottom-color: var(--accent); }
	.grow { flex: 1; }
	footer { display: flex; align-items: center; gap: 6px; height: 20px; padding: 0 10px; font-size: 10px; color: var(--ink-3); background: var(--surface); border-top: 1px solid var(--border); white-space: nowrap; overflow: hidden; }
	footer .sep { color: var(--line); }
	main { min-height: 0; min-width: 0; overflow: hidden; }
	.err { padding: 12px; color: var(--crit); }
	@media (max-width: 1050px) {
		header > .muted { display: none; }
		nav a { padding: 0 7px; }
	}
	@media (max-width: 700px) {
		.app { grid-template-rows: auto minmax(0, 1fr) auto; }
		header { flex-wrap: wrap; gap: 6px 10px; padding: 6px 10px; }
		header > .muted { display: none; }
		nav { order: 3; width: 100%; height: 30px; overflow-x: auto; }
		nav a { flex-shrink: 0; padding: 0 8px; }
	}
</style>
