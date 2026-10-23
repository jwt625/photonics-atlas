<script lang="ts">
	import type { Metric } from '../components.svelte';
	import { unitLabel } from '../layout/resolve';
	import { familyLabel } from './colors';
	import { isInferred, type Pt, type Val } from './logic';

	let { pt, classLabel, pinned = false }: { pt: Pt; classLabel: (cls: string) => string; pinned?: boolean } = $props();

	const QSYM: Record<string, string> = { lt: '<', gt: '>', le: '<=', ge: '>=', approx: '~' };

	function g3(v: number): string {
		return Math.abs(v) >= 1000 || Math.abs(v) < 0.01 ? v.toPrecision(3) : String(Number(v.toPrecision(3)));
	}
	function valText(v: Val): string {
		const q = v.m.qualifier ? QSYM[v.m.qualifier] + ' ' : '';
		if (v.note) return q + g3(v.v) + (v.vmax !== null ? '-' + g3(v.vmax) : '');
		return q + v.m.value + (v.m.value_max ? '-' + v.m.value_max : '');
	}
	function conds(m: Metric): string {
		const out: string[] = [];
		if (m.wavelength_nm) out.push(`${m.wavelength_nm}${m.wavelength_max_nm ? '-' + m.wavelength_max_nm : ''} nm${isInferred(m) ? ' (inferred)' : ''}`);
		if (m.band) out.push(m.band);
		if (m.polarization) out.push(m.polarization.toUpperCase());
		if (m.mode) out.push(m.mode);
		if (m.temperature_k) out.push(`${m.temperature_k} K`);
		if (m.bias_v) out.push(`${m.bias_v} V`);
		if (m.scope) out.push(`scope ${m.scope}`);
		if (m.ref_plane) out.push(`ref ${m.ref_plane}`);
		if (m.method) out.push(m.method);
		if (m.condition) out.push(m.condition);
		return out.join('; ');
	}
	const rows = $derived([pt.xv ? { lbl: pt.xLabel, v: pt.xv } : null, { lbl: pt.yLabel, v: pt.yv }].filter((r): r is { lbl: string; v: Val } => r !== null));
	const c = $derived(pt.c);
</script>

<div class="tip">
	<div class="tt">{c.label}</div>
	<div class="sub">{classLabel(c.class)}</div>
	<div class="sub">{c.platform || 'platform not stated'} ({familyLabel(pt.group)}){c.fab_orgs.length ? '; fab ' + c.fab_orgs.join(', ') : ''}</div>
	{#if !pt.xv}
		<div class="kv"><span class="l">{pt.xLabel}</span> <span class="v">{pt.xText}</span></div>
	{/if}
	{#each rows as r (r.lbl)}
		<div class="mv">
			<div class="kv">
				<span class="l">{r.lbl}</span>
				<span class="v num">{valText(r.v)}{unitLabel(r.v.unit) ? ' ' + unitLabel(r.v.unit) : ''}</span>
				<span class="b" class:mod={r.v.m.basis !== 'measured'}>{r.v.m.basis}{r.v.m.statistic ? ', ' + r.v.m.statistic : ''}</span>
			</div>
			{#if r.v.note}<div class="d">{r.v.note}</div>{/if}
			{#if conds(r.v.m)}<div class="d">{conds(r.v.m)}</div>{/if}
			<div class="d">{r.v.m.parameter}; {r.v.m.locator}</div>
		</div>
	{/each}
	<div class="src">{c.source.title} ({c.source.year}{c.source.venue ? ', ' + c.source.venue : ''})</div>
	{#if !pinned}<div class="hint">click a point to pin its card; click empty space to unpin</div>{/if}
</div>

<style>
	.tip {
		background: var(--surface);
		border: 1px solid var(--line);
		padding: 6px 8px;
		width: 320px;
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
		font-size: 11px;
		pointer-events: none;
	}
	.tt {
		font-weight: 600;
		line-height: 1.25;
		margin-bottom: 2px;
	}
	.sub {
		color: var(--ink-2);
	}
	.mv {
		margin-top: 4px;
		padding-top: 3px;
		border-top: 1px solid var(--border);
	}
	.kv {
		display: flex;
		gap: 6px;
		align-items: baseline;
	}
	.l {
		color: var(--ink-3);
		flex: none;
	}
	.v {
		color: var(--ink);
		font-weight: 600;
	}
	.b {
		margin-left: auto;
		color: var(--ink-3);
		font-size: 10px;
		white-space: nowrap;
	}
	.b.mod {
		color: var(--warn);
	}
	.d {
		color: var(--ink-3);
		font-size: 10px;
		line-height: 1.3;
	}
	.src {
		margin-top: 4px;
		padding-top: 3px;
		border-top: 1px solid var(--border);
		color: var(--ink-2);
		line-height: 1.3;
	}
	.hint {
		color: var(--ink-3);
		font-size: 10px;
		margin-top: 2px;
	}
</style>
