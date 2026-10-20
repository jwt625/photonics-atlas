<div class="about">
	<h2>Photonics Atlas: shared registry</h2>
	<p>
		One registry of organizations (with aliases, parents and dated org events) and source documents, built to feed a PIC
		component atlas (WDM as its own category), a supply-chain / vendor atlas and a people / affiliation atlas. The EO
		modulator atlas and the advanced packaging atlas stay canonical for their own tables; this registry reads them.
	</p>
	<h3>Conventions</h3>
	<ul>
		<li>Empty cell = not stated by any source. Country, type, dates and names come from a record that states them (atlas row, ROR record, cited source).</li>
		<li>Renames, spin-offs, acquisitions and mergers are org events between separate organizations, not aliases.</li>
		<li>Printed affiliation strings map to organizations by normalized name, curated alias or exact ROR name match; no fuzzy matching.</li>
		<li>Evidence grades A-D, X; events carry sources and a locator. Dates are ISO (YYYY, YYYY-MM or YYYY-MM-DD).</li>
		<li>Non-open-access corpora (OFC 2026, packaging-atlas papers) contribute facts and locators only.</li>
	</ul>
	<h3>Data</h3>
	<p>CSV tables in <span class="mono">data/registry/</span>, generated crosswalk in <span class="mono">data/crosswalk/</span>; this page reads a generated view. ROR data (CC0) is used for organization identifiers.</p>
</div>

<style>
	.about { height: 100%; overflow: auto; padding: 12px 16px; max-width: 900px; }
	h2 { font-size: 15px; margin: 0 0 8px; }
	h3 { font-size: 12px; color: var(--ink-2); margin: 14px 0 4px; }
	ul { padding-left: 18px; margin: 0; }
	li { margin: 2px 0; }
	p { color: var(--ink-2); }
</style>
