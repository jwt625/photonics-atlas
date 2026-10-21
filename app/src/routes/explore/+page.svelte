<script lang="ts">
	import { onMount } from 'svelte';
	import { comp, loadComponents, type Component } from '../../lib/components.svelte';
	import { ui } from '../../lib/state.svelte';
	import { exFilters, resetExFilters } from '../../lib/explore/state.svelte';
	import {
		applyExFilters,
		buildScatter,
		buildStrip,
		buildVsWavelength,
		classFamily,
		combineOmitted,
		countBy,
		familyOf,
		toMw,
		type AxisSpec,
		type GroupStat
	} from '../../lib/explore/logic';
	import { GROUP_ORDER, familyLabel, familyShort, groupColor, plotTheme } from '../../lib/explore/colors';
	import FilterPanel from '../../lib/explore/FilterPanel.svelte';
	import ScatterChart from '../../lib/explore/ScatterChart.svelte';
	import YearStack from '../../lib/explore/YearStack.svelte';
	import TopBars from '../../lib/explore/TopBars.svelte';
	import HeatChart from '../../lib/explore/HeatChart.svelte';

	onMount(() => {
		loadComponents();
	});

	const v = $derived(comp.view);
	const all = $derived(v?.components ?? []);
	const shown = $derived(applyExFilters(all, exFilters));
	const mo = $derived(exFilters.measuredOnly);

	const familyName = (f: string) => v?.classes[f]?.label ?? f;
	const classLabel = (cls: string) => {
		const [f, s] = cls.split('.');
		return `${familyName(f)} / ${s ?? ''}`;
	};

	/** components of the listed classes (class or class family), plus any component reporting one of the params */
	function domain(comps: Component[], classes: string[], params: string[] = []): Component[] {
		return comps.filter((c) => classes.includes(c.class) || classes.includes(classFamily(c)) || c.metrics.some((m) => params.includes(m.parameter)));
	}

	// axis specs -----------------------------------------------------------------------------------------------
	const COUPLER_SCOPES = ['per_coupler', 'per_facet', 'loopback_half'];
	const IL_COUPLER: AxisSpec = { label: 'Loss per coupler', params: ['insertion_loss_db'], scopes: COUPLER_SCOPES };
	const BW1: AxisSpec = { label: '1-dB bandwidth', params: ['bw_1db_nm'] };
	const IL_FACET: AxisSpec = { label: 'Loss per facet', params: ['insertion_loss_db'], scopes: ['per_facet', 'loopback_half'] };
	const PROP: AxisSpec = { label: 'Propagation loss', params: ['prop_loss_db_per_cm'] };
	const QI: AxisSpec = { label: 'Intrinsic Q', params: ['q_intrinsic'] };
	const RADIUS: AxisSpec = { label: 'Radius', params: ['radius_um'], geometry: true };
	const TRANS: AxisSpec = { label: 'Transition loss', params: ['transition_loss_db'] };
	const IL_WDM: AxisSpec = { label: 'Insertion loss', params: ['insertion_loss_db'] };
	const SP_NM: AxisSpec = { label: 'Channel spacing', params: ['channel_spacing_nm'] };
	const SP_GHZ: AxisSpec = { label: 'Channel spacing', params: ['channel_spacing_ghz'] };
	const PD_BW: AxisSpec = { label: '3-dB bandwidth', params: ['bw3db_ghz'] };
	const RESP: AxisSpec = { label: 'Responsivity', params: ['responsivity_a_per_w'] };
	const POUT: AxisSpec = { label: 'Output power', params: ['output_power_mw', 'output_power_dbm'], convert: toMw };
	const ITH: AxisSpec = { label: 'Threshold', params: ['threshold_ma'] };

	// axis scale state -----------------------------------------------------------------------------------------
	let aY = $state(false);
	let bX = $state(false), bY = $state(false);
	let cY = $state(false);
	let dY = $state(true);
	let eX = $state(true), eY = $state(true);
	let fY = $state(false);
	let gX = $state(true), gY = $state(false);
	let gUnit = $state<'ghz' | 'nm'>('ghz');
	let hX = $state(false), hY = $state(false);
	let iX = $state(true), iY = $state(true);

	const gc = $derived(shown.filter((c) => c.class === 'fiber_chip_coupler.grating'));
	const ec = $derived(shown.filter((c) => c.class === 'fiber_chip_coupler.edge'));

	const A0 = $derived(buildVsWavelength(gc, IL_COUPLER, { measuredOnly: mo, yLog: aY, panel: 0 }));
	const A1 = $derived(buildVsWavelength(ec, IL_COUPLER, { measuredOnly: mo, yLog: aY, panel: 1 }));
	const B = $derived(buildScatter(gc, BW1, IL_COUPLER, { measuredOnly: mo, xLog: bX, yLog: bY }));
	const C = $derived(buildStrip(ec, IL_FACET, { measuredOnly: mo, yLog: cY }));
	const D = $derived(
		buildStrip(domain(shown, ['waveguide_platform.straight', 'waveguide_platform.slow_light', 'waveguide_platform.other', 'resonator.ring', 'resonator.coupled_rings'], PROP.params), PROP, {
			measuredOnly: mo,
			yLog: dY
		})
	);
	const E = $derived(buildScatter(domain(shown, ['resonator.ring', 'resonator.coupled_rings'], QI.params), RADIUS, QI, { measuredOnly: mo, xLog: eX, yLog: eY }));
	const F = $derived(buildStrip(domain(shown, ['waveguide_platform.transition'], TRANS.params), TRANS, { measuredOnly: mo, yLog: fY }));
	const G = $derived(buildScatter(domain(shown, ['wdm']), gUnit === 'nm' ? SP_NM : SP_GHZ, IL_WDM, { measuredOnly: mo, xLog: gX, yLog: gY }));
	const H = $derived(buildScatter(domain(shown, ['photodetector']), RESP, PD_BW, { measuredOnly: mo, xLog: hX, yLog: hY }));
	const I = $derived(buildScatter(domain(shown, ['laser']), ITH, POUT, { measuredOnly: mo, xLog: iX, yLog: iY }));

	const th = $derived(plotTheme(ui.theme));
	/** a family median bar is drawn only over at least this many unqualified, measured values */
	const MIN_MEDIAN_N = 3;
	function medianTraces(stats: GroupStat[], unit: string): unknown[] {
		const s = stats.filter((x) => x.median !== null && x.n >= MIN_MEDIAN_N);
		if (!s.length) return [];
		return [
			{
				type: 'scatter',
				mode: 'markers',
				x: s.map((x) => x.index),
				y: s.map((x) => x.median),
				text: s.map((x) => `${familyLabel(x.group)}: median of ${x.n} unqualified, measured values`),
				marker: { symbol: 'line-ew', size: 26, color: th.ink, line: { width: 2, color: th.ink } },
				hovertemplate: `%{text}<br>%{y} ${unit}<extra></extra>`,
				showlegend: false
			}
		];
	}
	const stripTicks = (stats: GroupStat[]) => stats.map((s) => `${familyShort(s.group)} (${s.total})`);
	const stripRange = (stats: GroupStat[]): [number, number] | undefined => (stats.length ? [-0.6, stats.length - 0.4] : undefined);

	const fabCounts = $derived(countBy(shown, (c) => c.fab_orgs));
	const noFab = $derived(shown.filter((c) => !c.fab_orgs.length).length);
	const presentGroups = $derived(GROUP_ORDER.filter((g) => shown.some((c) => familyOf(c) === g)));
</script>

<div class="page">
	<div class="side"><FilterPanel {all} nShown={shown.length} {familyName} /></div>
	<div class="main">
		<div class="legend">
			{#each presentGroups as g (g)}
				<span class="it" data-tip="Platform family {familyLabel(g)}"><i class="sw" style="background:{groupColor(g, ui.theme)}"></i>{familyLabel(g)}</span>
			{/each}
			<span class="sep"></span>
			<span class="it" data-tip="Measured, derived, extracted from a figure or specification (circle)"><svg viewBox="0 0 10 10" width="10" height="10"><circle cx="5" cy="5" r="4" fill="currentColor" /></svg>measured</span>
			<span class="it" data-tip="A performance value of the point is simulated, a design target or an author estimate (diamond)"><svg viewBox="0 0 10 10" width="10" height="10"><path d="M5 0 L10 5 L5 10 L0 5 Z" fill="currentColor" /></svg>modelled</span>
			<span class="it" data-tip="Upper (lt, le) or lower (gt, ge) bound, drawn as a bar-arrow in the bound direction"><svg viewBox="0 0 10 10" width="10" height="10"><path d="M1 1 L1 9 M1 5 L9 5 M5 2 L1 5 L5 8" fill="none" stroke="currentColor" stroke-width="1.4" /></svg>bound</span>
			<span class="muted hint" data-tip="Hover a point for its card; click to pin, click empty space to unpin. One point per component. Values not reported are omitted, never drawn at 0; the badge tooltip gives the omitted breakdown.">1 point per component</span>
		</div>
		<div class="scroll">
			{#if comp.error}
				<div class="msg">Failed to load data: {comp.error}</div>
			{:else if !v}
				<div class="msg"><span class="spinner"></span></div>
			{:else if !shown.length}
				<div class="msg"><span>No component matches the filters.</span><button onclick={resetExFilters} data-tip="Clear all filters">Reset filters</button></div>
			{:else}
				<div class="grid">
					<ScatterChart
						letter="a"
						desc="Fiber-chip coupler loss per coupler against wavelength: grating couplers (top), edge couplers (bottom). Loss rows with scope per_coupler, per_facet or loopback_half; x is the wavelength stated with the loss row (range start for a range), else the component's center wavelength row. Band-only rows have no x."
						panels={[
							{ pts: A0.pts, yTitle: 'Loss per coupler (dB)', tag: 'grating' },
							{ pts: A1.pts, yTitle: 'Loss per facet (dB)', tag: 'edge' }
						]}
						xTitle="Wavelength (nm)"
						allowX={false}
						bind:yLog={aY}
						omitted={combineOmitted([A0.omitted, A1.omitted])}
						unit="grating and edge couplers"
						{classLabel}
						wide
					/>
					<ScatterChart
						letter="b"
						desc="Grating coupler loss per coupler (scope per_coupler or loopback_half) against 1-dB bandwidth"
						panels={[{ pts: B.pts, yTitle: 'Loss per coupler (dB)' }]}
						xTitle="1-dB bandwidth (nm)"
						bind:xLog={bX}
						bind:yLog={bY}
						omitted={B.omitted}
						unit="grating couplers"
						{classLabel}
					/>
					<ScatterChart
						letter="c"
						desc="Edge coupler insertion loss per facet by platform family (insertion_loss_db rows with scope per_facet or loopback_half; other scopes not accepted), jittered horizontally; the horizontal bar is the family median of unqualified, measured values (drawn when there are at least 3)"
						panels={[{ pts: C.pts, yTitle: 'Loss per facet (dB)' }]}
						xTitle="Platform family (components)"
						allowX={false}
						bind:yLog={cY}
						omitted={C.omitted}
						unit="edge couplers"
						{classLabel}
						xTickvals={C.stats.map((s) => s.index)}
						xTicktext={stripTicks(C.stats)}
						xRange={stripRange(C.stats)}
						extraTraces={medianTraces(C.stats, 'dB')}
						emptyText="no edge coupler in the filter reports a per-facet loss"
					/>
					<ScatterChart
						letter="d"
						desc="Propagation loss by platform family (straight / slow-light / other waveguides, rings and coupled rings, plus any component reporting it), jittered horizontally; the horizontal bar is the family median of unqualified, measured values (drawn when there are at least 3)"
						panels={[{ pts: D.pts, yTitle: 'Propagation loss (dB/cm)' }]}
						xTitle="Platform family (components)"
						allowX={false}
						bind:yLog={dY}
						omitted={D.omitted}
						unit="waveguides, rings and components reporting propagation loss"
						{classLabel}
						xTickvals={D.stats.map((s) => s.index)}
						xTicktext={stripTicks(D.stats)}
						xRange={stripRange(D.stats)}
						extraTraces={medianTraces(D.stats, 'dB/cm')}
						emptyText="no component in the filter reports a propagation loss"
					/>
					<ScatterChart
						letter="e"
						desc="Ring and coupled-ring intrinsic Q against ring radius (bend radius for racetracks). Radius is a geometry dimension: its design basis does not make the point a diamond."
						panels={[{ pts: E.pts, yTitle: 'Intrinsic Q' }]}
						xTitle="Radius (µm)"
						bind:xLog={eX}
						bind:yLog={eY}
						omitted={E.omitted}
						unit="rings, coupled rings and components reporting intrinsic Q"
						{classLabel}
					/>
					<ScatterChart
						letter="f"
						desc="Loss per layer / material transition by platform family (transition structures plus any component reporting it), jittered horizontally; the horizontal bar is the family median of unqualified, measured values (drawn when there are at least 3)"
						panels={[{ pts: F.pts, yTitle: 'Transition loss (dB)' }]}
						xTitle="Platform family (components)"
						allowX={false}
						bind:yLog={fY}
						omitted={F.omitted}
						unit="transitions and components reporting transition loss"
						{classLabel}
						xTickvals={F.stats.map((s) => s.index)}
						xTicktext={stripTicks(F.stats)}
						xRange={stripRange(F.stats)}
						extraTraces={medianTraces(F.stats, 'dB')}
						emptyText="no component in the filter reports a transition loss"
					/>
					<ScatterChart
						letter="g"
						desc="WDM filter insertion loss (any scope; scope in the card) against channel spacing as reported, in GHz (channel_spacing_ghz) or nm (channel_spacing_nm); no conversion between the two"
						panels={[{ pts: G.pts, yTitle: 'Insertion loss (dB)' }]}
						xTitle={gUnit === 'nm' ? 'Channel spacing (nm)' : 'Channel spacing (GHz)'}
						bind:xLog={gX}
						bind:yLog={gY}
						omitted={G.omitted}
						unit="WDM components"
						{classLabel}
					>
						{#snippet headerExtra()}
							<span class="seg" data-tip="Channel spacing as reported: GHz or nm rows">
								<button class:on={gUnit === 'ghz'} onclick={() => (gUnit = 'ghz')}>GHz</button><button class:on={gUnit === 'nm'} onclick={() => (gUnit = 'nm')}>nm</button>
							</span>
						{/snippet}
					</ScatterChart>
					<ScatterChart
						letter="h"
						desc="Photodetector 3-dB bandwidth against responsivity (reference plane and bias in the card)"
						panels={[{ pts: H.pts, yTitle: '3-dB bandwidth (GHz)' }]}
						xTitle="Responsivity (A/W)"
						bind:xLog={hX}
						bind:yLog={hY}
						omitted={H.omitted}
						unit="photodetectors"
						{classLabel}
					/>
					<ScatterChart
						letter="i"
						desc="Laser output power against threshold current; dBm rows converted to mW (10^(dBm/10)), noted in the card"
						panels={[{ pts: I.pts, yTitle: 'Output power (mW)' }]}
						xTitle="Threshold current (mA)"
						bind:xLog={iX}
						bind:yLog={iY}
						omitted={I.omitted}
						unit="lasers"
						{classLabel}
					/>
					<YearStack comps={shown} {familyName} />
					<TopBars
						letter="k"
						desc="Components per fabricating organization (fab_org_ids: the org the source states fabricated the component; a component counts once per org)"
						counts={fabCounts}
						badgeTip={`distinct fabricating organizations in the current filter; ${noFab} of ${shown.length} components name none`}
					/>
					<div class="full"><HeatChart comps={shown} rowName={(k) => (k.includes('.') ? k : familyName(k))} /></div>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.page {
		display: grid;
		grid-template-columns: 220px minmax(0, 1fr);
		grid-template-rows: minmax(0, 1fr);
		height: 100%;
	}
	.side {
		min-height: 0;
	}
	.main {
		display: flex;
		flex-direction: column;
		min-width: 0;
		min-height: 0;
	}
	.legend {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 4px 12px;
		padding: 7px 10px;
		flex: none;
		background: var(--surface);
		border-bottom: 1px solid var(--border);
		white-space: nowrap;
	}
	.it {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		color: var(--ink-2);
	}
	.sw {
		width: 10px;
		height: 10px;
		display: inline-block;
	}
	.sep {
		width: 1px;
		height: 14px;
		background: var(--line);
	}
	.hint {
		cursor: help;
	}
	.scroll {
		flex: 1;
		min-height: 0;
		overflow-y: auto;
		padding: 8px;
	}
	.grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 8px;
		align-items: start;
	}
	.full {
		grid-column: 1 / -1;
	}
	.msg {
		padding: 20px;
		color: var(--ink-3);
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 10px;
	}
	.seg {
		display: inline-flex;
	}
	.seg button {
		height: 20px;
		font-size: 10px;
		padding: 0 6px;
	}
	@media (max-width: 1100px) {
		.grid {
			grid-template-columns: minmax(0, 1fr);
		}
	}
	@media (max-width: 720px) {
		.page {
			grid-template-columns: minmax(0, 1fr);
			grid-template-rows: auto minmax(0, 1fr);
		}
		.legend {
			white-space: normal;
		}
	}
</style>
