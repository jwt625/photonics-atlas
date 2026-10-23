<script lang="ts">
	import { link } from '../../lib/paths';
	import { store } from '../../lib/state.svelte';

	let ov = $derived(store.reg?.overview);
</script>

<div class="about">
	<h2>Photonics Atlas</h2>
	<p>
		An atlas of integrated photonics built from published work: PIC components and their reported performance and
		geometry, the supply chain behind them (wafers, foundries, instruments, materials, packaging, reliability
		standards), and the people and organizations that publish them.
		{#if ov}It currently holds {ov.components.n} components with {ov.values.n} values from {ov.components.publications} publications, {ov.orgs.n} organizations and {ov.people.persons} people.{/if}
	</p>
	<h3>Pages</h3>
	<ul>
		<li><a href={link('/components')}>Components</a>: every reported value with its conditions, basis and location in the publication.</li>
		<li><a href={link('/explore')}>Explore</a>: performance plots across components and platforms.</li>
		<li><a href={link('/layout')}>Layouts</a>: top views and cross-sections drawn from the reported dimensions.</li>
		<li><a href={link('/supply')}>Supply</a>: vendors, foundries, products and standards named in the papers.</li>
		<li><a href={link('/people')}>People</a>: authors and their published affiliations.</li>
		<li><a href={link('/orgs')}>Organizations</a>: each organization with its components, supply facts, people and publications.</li>
	</ul>
	<h3>How to read the data</h3>
	<ul>
		<li>Every value comes from a publication and carries its location (page, figure, table or section).</li>
		<li>Basis: measured, simulated, design target or derived, as the publication states it. Values are as reported; unit conversions and sign conventions (losses stored as positive dB) are noted with the value.</li>
		<li>An empty field means the publication does not state it. Layout drawings show unreported dimensions dashed and without a number.</li>
		<li>An author affiliation is what the publication prints (or, for some conference papers, what the conference program lists), dated by the publication; it is not an employment period. Only public professional sources are used.</li>
		<li>Acquisitions, renames, spin-offs and mergers link separate organizations; names as printed in publications are matched to organizations by normalized name, a curated alias or the exact ROR name (no fuzzy matching).</li>
		<li>Dates are ISO (YYYY, YYYY-MM or YYYY-MM-DD).</li>
	</ul>
	<h3>Related atlases</h3>
	<ul>
		<li><a href="https://outside5sigma.com/eo-modulator-atlas/" target="_blank" rel="noopener">EO modulator atlas</a></li>
		<li><a href="https://outside5sigma.com/advanced-packaging-atlas/" target="_blank" rel="noopener">Advanced packaging atlas</a></li>
	</ul>
	<p class="muted">Organization identifiers from ROR (CC0).</p>
</div>

<style>
	.about { height: 100%; overflow: auto; padding: 12px 16px; max-width: 900px; }
	h2 { font-size: 15px; margin: 0 0 8px; }
	h3 { font-size: 12px; color: var(--ink-2); margin: 14px 0 4px; }
	ul { padding-left: 18px; margin: 0; }
	li { margin: 2px 0; }
	p { color: var(--ink-2); }
</style>
