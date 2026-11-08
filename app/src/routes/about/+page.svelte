<script lang="ts">
	import { link, staticUrl } from '../../lib/paths';
	import type { Summary } from '../../lib/types';

	let { data }: { data: { summary: Summary } } = $props();
	let ov = $derived(data.summary.overview);
</script>

<div class="about">
	<h2>Photonics Atlas</h2>
	<p>
		An atlas of integrated photonics built from published work: PIC components and their reported performance and
		geometry, the supply chain behind them (wafers, foundries, instruments, materials, packaging, reliability
		standards), and the people and organizations that publish them.
		{#if ov}It currently holds {ov.components.n} components with {ov.values.n} values ({ov.values.measured} measured) from {ov.components.publications} publications, {ov.orgs.n} organizations and {ov.people.persons} people.{/if}
		Sources are journal and conference papers (a curated literature corpus of about a thousand papers, OFC 2026, and
		the papers of the EO modulator and advanced packaging atlases); each paper is distilled into component and value
		rows and checked by an independent audit before it is merged.
	</p>
	<h3>Pages</h3>
	<ul>
		<li><a href={link('/')}>Dashboard</a>: counts, publications by year and type, leading fabricating organizations and vendors.</li>
		<li><a href={link('/components')}>Components</a>: every reported value with its conditions, basis and location in the publication; tables per class with column filters.</li>
		<li><a href={link('/explore')}>Explore</a>: performance plots across components and platforms.</li>
		<li><a href={link('/layout')}>Layouts</a>: true-scale top views and cross-sections drawn from the reported dimensions and the source figures.</li>
		<li><a href={link('/benchmark')}>Benchmark</a>: foundry PDK building blocks side by side, the best published value per foundry and platform (also as a <a href={staticUrl('pdk-benchmark.html')} target="_blank" rel="noopener">standalone page</a>).</li>
		<li><a href={link('/supply')}>Supply</a>: vendors, foundries, products and standards named in the papers.</li>
		<li><a href={link('/people')}>People</a>: authors and their published affiliations.</li>
		<li><a href={link('/orgs')}>Organizations</a>: each organization with its components, supply facts, people and publications.</li>
	</ul>
	<h3>How to read the data</h3>
	<ul>
		<li>Every value comes from a publication and carries its location (page, figure, table or section).</li>
		<li>Basis: measured, read from a figure, derived (arithmetic on the publication's own numbers), author estimate (rests on an assumed or unstated input), simulated, design target or specification. Values are as reported; unit conversions and sign conventions (losses stored as positive dB) are noted with the value.</li>
		<li>An empty field means the publication does not state it. A layout the source does not fix is not drawn, with the reason on the page; assumed parts inside a drawn layout are dashed. Dimensions read off a source figure are marked as figure readings and never enter the value tables.</li>
		<li>Benchmark cells are literature results on devices made in a foundry's process, not PDK specifications. Ranges are ranked at their midpoint. Italic: the publication names no fab and the foundry follows from the authors' affiliation. Marked values come from a foundry customer's public product specification or from private communication; each is labelled in its tooltip.</li>
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
