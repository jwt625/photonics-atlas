// Foundry PDK benchmark table (DevLog-014 D904, D905). One renderer for the app tab (/benchmark) and the standalone
// file (app/static/pdk-benchmark.html, built by app/scripts/build-benchmark-html.mjs): plain JS, no framework, so both
// stay identical. Input: static/data/benchmark.json from scripts/build_benchmark.py. Ranking and emphasis are computed
// here, never stored: best in row (bold, tinted), second (underlined), leading column (most row bests, tinted band).

/**
 * @typedef {{ r: number, v: number, vmax?: number, q?: string, basis: string, source_id: string, n: number, n_src: number,
 *   date?: string, [k: string]: unknown }} Cell
 * @typedef {{ id: string, label: string, unit: string, better: 'lower' | 'higher', fmt: string, sub: string,
 *   note: string, cells: Record<string, Cell> }} Row
 * @typedef {{ id: string, label: string, rows: Row[] }} Category
 * @typedef {{ id: string, family: string, foundry: string, label: string, orgs: string[], processes: string[],
 *   n_rows: number, pinned?: boolean }} Column
 * @typedef {{ id: string, label: string, tip: string }} Family
 * @typedef {{ title?: string, venue?: string, year?: string, url?: string }} Pub
 * @typedef {{ generated_on: string, families: Family[], columns: Column[], categories: Category[],
 *   sources: Record<string, Pub>, rules: { basis: string[], min_rows_per_column: number, min_columns_per_row: number,
 *   telecom_window_nm: number[], min_temperature_k: number }, rows_not_shown: string[] }} BenchmarkView
 * @typedef {{ rank: 'all' | 'family', hidden: string[] }} BenchState
 */

const esc = (/** @type {unknown} */ s) =>
	String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c] ?? c);

const QUAL = /** @type {Record<string, string>} */ ({ lt: '<', le: '≤', gt: '>', ge: '≥', approx: '~' });
const BASIS = /** @type {Record<string, string>} */ ({
	measured: 'measured',
	extracted_from_figure: 'read from a figure',
	derived: 'derived from measured values',
	private_communication: 'private communication, unpublished'
});
const PC = 'private_communication';
const SCOPE = /** @type {Record<string, string>} */ ({
	per_facet: 'per facet',
	per_coupler: 'per coupler',
	loopback_half: 'half of a loopback pair',
	de_embedded: 'coupling de-embedded',
	per_component: 'per device'
});
const BAND = /** @type {Record<string, string>} */ ({
	o_band: 'O band', e_band: 'E band', s_band: 'S band', c_band: 'C band', l_band: 'L band', cl_band: 'C+L band'
});
const SUP = '⁰¹²³⁴⁵⁶⁷⁸⁹';

/** Number as shown: 3 significant digits below 100, integer above; `sci` = mantissa x 10^n from 1e4 (HTML). */
export function fmtNum(/** @type {number} */ v, fmt = 'auto') {
	if (fmt === 'sci' && Math.abs(v) >= 1e4) {
		const e = Math.floor(Math.log10(Math.abs(v)));
		const m = Number((v / 10 ** e).toPrecision(2));
		return `${m}×10<sup>${e}</sup>`;
	}
	if (Math.abs(v) >= 100) return String(Math.round(v));
	return String(Number(v.toPrecision(3)));
}

/** Same number as plain text (tooltips). */
export function fmtText(/** @type {number} */ v, fmt = 'auto') {
	if (fmt === 'sci' && Math.abs(v) >= 1e4) {
		const e = Math.floor(Math.log10(Math.abs(v)));
		const m = Number((v / 10 ** e).toPrecision(2));
		return `${m}×10${String(e).split('').map((d) => SUP[Number(d)]).join('')}`;
	}
	return String(v);
}

/**
 * Rank of each filled cell of a row among the given columns: 1 = best, 2 = second best value (ties share a rank).
 * mode 'family' ranks within each platform family.
 * @param {Row} row @param {Column[]} cols @param {'all' | 'family'} mode
 * @returns {Record<string, number>}
 */
export function rankRow(row, cols, mode) {
	/** @type {Record<string, number>} */
	const out = {};
	/** @type {Map<string, Column[]>} */
	const groups = new Map();
	for (const c of cols) {
		if (!row.cells[c.id]) continue;
		const k = mode === 'family' ? c.family : '';
		groups.set(k, [...(groups.get(k) ?? []), c]);
	}
	for (const g of groups.values()) {
		const vals = [...new Set(g.map((c) => row.cells[c.id].r))].sort((a, b) => (row.better === 'lower' ? a - b : b - a));
		for (const c of g) {
			const i = vals.indexOf(row.cells[c.id].r);
			if (i < 2) out[c.id] = i + 1;
		}
	}
	return out;
}

/**
 * Row bests per column, and the leading column(s): most row bests (within each family in 'family' mode).
 * @param {BenchmarkView} view @param {Column[]} cols @param {'all' | 'family'} mode
 */
export function leaders(view, cols, mode) {
	/** @type {Record<string, number>} */
	const wins = Object.fromEntries(cols.map((c) => [c.id, 0]));
	for (const cat of view.categories)
		for (const row of cat.rows) {
			const rk = rankRow(row, cols, mode);
			for (const [c, r] of Object.entries(rk)) if (r === 1) wins[c]++;
		}
	const lead = new Set();
	const fams = mode === 'family' ? [...new Set(cols.map((c) => c.family))] : [''];
	for (const f of fams) {
		const g = cols.filter((c) => !f || c.family === f);
		const max = Math.max(0, ...g.map((c) => wins[c.id]));
		if (max > 0) for (const c of g) if (wins[c.id] === max) lead.add(c.id);
	}
	return { wins, lead };
}

const words = (/** @type {unknown} */ s) => String(s ?? '').replace(/_/g, ' ');

/** Tooltip of a value cell (plain text, one fact per line). */
export function cellTip(/** @type {Row} */ row, /** @type {Column} */ col, /** @type {Cell} */ c, /** @type {Pub | undefined} */ pub) {
	const val = (c.q ? QUAL[c.q] ?? '' : '') + (c.vmax != null ? `${fmtText(c.v, row.fmt)} to ${fmtText(c.vmax, row.fmt)}` : fmtText(c.v, row.fmt));
	const range = c.vmax != null ? `range, ranked at its midpoint ${fmtText(Number(c.r.toPrecision(3)), row.fmt)} ${row.unit}` : '';
	const wl = c.wavelength_nm ? `${c.wavelength_nm} nm` : BAND[String(c.band)] ?? '';
	const cond = [
		wl,
		c.polarization && c.polarization !== 'unspecified' ? String(c.polarization).toUpperCase() : '',
		c.scope ? SCOPE[String(c.scope)] ?? words(c.scope) : '',
		c.temperature_k ? `${c.temperature_k} K` : '',
		c.bias_v ? `bias ${c.bias_v} V` : '',
		c.length_mm ? `length ${c.length_mm} mm` : '',
		c.convention ? String(c.convention) : '',
		c.bw_reference ? `bandwidth reference ${words(c.bw_reference)}` : '',
		c.statistic ? words(c.statistic) : '',
		c.method && c.method !== 'unspecified' ? words(c.method) : ''
	].filter(Boolean);
	const lines = [
		`${val} ${row.unit}`.trim() + `   ${row.label}, ${col.label} ${familyLabel(col)}`,
		range,
		c.basis === PC
			? `${BASIS[PC]} (${c.date}); not a literature value`
			: `best of ${c.n} value${c.n === 1 ? '' : 's'} from ${c.n_src} publication${c.n_src === 1 ? '' : 's'} in this cell; ${BASIS[c.basis] ?? words(c.basis)}`,
		'',
		`${c.org}: ${c.component}`,
		c.platform || c.core ? [c.platform ? words(c.platform) : '', c.core].filter(Boolean).join('; ') : '',
		c.effect ? `effect: ${c.effect}` : '',
		c.process ? `process: ${c.process}` : '',
		c.condition ? `conditions: ${c.condition}` : '',
		cond.join(', '),
		'',
		c.basis === PC ? '' : pub?.title ?? '',
		c.basis === PC ? '' : [pub?.venue, pub?.year].filter(Boolean).join(', '),
		c.locator ? `location: ${c.locator}` : '',
		pub?.url ? 'click to open the publication' : ''
	];
	return lines.filter((l, i) => l !== '' || (i > 0 && lines[i - 1] !== '')).join('\n').trim();
}

/** @type {Record<string, string>} */
let FAMILY_LABEL = {};
const familyLabel = (/** @type {Column} */ c) => FAMILY_LABEL[c.family] ?? c.family;

/** Visible columns in table order. */
export function visibleColumns(/** @type {BenchmarkView} */ view, /** @type {BenchState} */ st) {
	return view.columns.filter((c) => !st.hidden.includes(c.family));
}

const SUN = `<svg class="bm-sun" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><circle cx="8" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="1.4"/><g stroke="currentColor" stroke-width="1.4"><line x1="8" y1="1" x2="8" y2="3"/><line x1="8" y1="13" x2="8" y2="15"/><line x1="1" y1="8" x2="3" y2="8"/><line x1="13" y1="8" x2="15" y2="8"/><line x1="3" y1="3" x2="4.4" y2="4.4"/><line x1="11.6" y1="11.6" x2="13" y2="13"/><line x1="3" y1="13" x2="4.4" y2="11.6"/><line x1="11.6" y1="4.4" x2="13" y2="3"/></g></svg>`;
const MOON = `<svg class="bm-moon" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M13 9.6A5.6 5.6 0 0 1 6.4 3a5.6 5.6 0 1 0 6.6 6.6z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="miter"/></svg>`;

/**
 * Whole widget as an HTML string: toolbar, table, notes.
 * @param {BenchmarkView} view @param {BenchState} st @param {{ title?: string, themeToggle?: boolean }} [opt]
 */
export function renderBenchmark(view, st, opt = {}) {
	FAMILY_LABEL = Object.fromEntries(view.families.map((f) => [f.id, f.label]));
	const cols = visibleColumns(view, st);
	const { wins, lead } = leaders(view, cols, st.rank);
	const famSpans = view.families
		.map((f) => ({ f, n: cols.filter((c) => c.family === f.id).length }))
		.filter((x) => x.n > 0);
	const nRows = view.categories.reduce((n, c) => n + c.rows.length, 0);
	const ncol = cols.length + 1;
	const anyPc = view.categories.some((cat) => cat.rows.some((row) => cols.some((c) => row.cells[c.id]?.basis === PC)));

	const toolbar = `<div class="bm-bar">
	${opt.title ? `<span class="bm-title">${esc(opt.title)}</span>` : ''}
	<span class="bm-grp" role="group" aria-label="Ranking">
		<span class="bm-lbl" data-tip="Which columns compete for best and second best in a row">rank</span>
		<button data-bm-rank="all" class="${st.rank === 'all' ? 'on' : ''}" data-tip="Best and second best among all shown columns">all columns</button>
		<button data-bm-rank="family" class="${st.rank === 'family' ? 'on' : ''}" data-tip="Best and second best within each platform family">within family</button>
	</span>
	<span class="bm-grp" role="group" aria-label="Platform families">
		<span class="bm-lbl">families</span>
		${view.families.map((f) => `<button data-bm-fam="${esc(f.id)}" class="${st.hidden.includes(f.id) ? '' : 'on'}" data-tip="${esc(f.tip)}">${esc(f.label)}</button>`).join('')}
	</span>
	<span class="bm-legend">
		<span class="bm-key r1" data-tip="Best value in the row">best</span>
		<span class="bm-key r2" data-tip="Second-best value in the row">second</span>
		<span class="bm-key lead" data-tip="Column with the most row bests">most bests</span>
		${anyPc ? `<span class="bm-key" data-tip="Unpublished value from private communication; ranked like any value"><span class="bm-pc">†</span> private comm.</span>` : ''}
	</span>
	<span class="bm-grow"></span>
	<span class="bm-meta muted" data-tip="Date the table was generated from the atlas tables">${cols.length} columns, ${nRows} rows, ${esc(view.generated_on)}</span>
	${opt.themeToggle ? `<button class="bm-theme" data-bm-theme aria-label="Toggle theme" data-tip="Light / dark theme">${SUN}${MOON}</button>` : ''}
</div>`;

	let note = 0;
	/** @type {string[]} */
	const notes = [];
	const head = `<thead>
	<tr class="bm-famrow">
		<th class="bm-stub" rowspan="2"><span class="bm-stubh">Building block</span><span class="bm-sub">conditions · unit · better</span></th>
		${famSpans.map(({ f, n }) => `<th class="bm-famh" colspan="${n}" data-tip="${esc(f.tip)}">${esc(f.label)}</th>`).join('')}
	</tr>
	<tr class="bm-colrow">
		${cols
			.map((c) => {
				const tip = [
					`${c.label}, ${familyLabel(c)}`,
					`organizations: ${c.orgs.join(', ')}`,
					c.processes.length ? `processes (most cited first):\n  ${c.processes.join('\n  ')}` : '',
					`rows filled: ${c.n_rows}; row bests: ${wins[c.id]}`,
					c.pinned ? 'pinned: shown whatever its fill; a dash is a coverage gap of the atlas' : ''
				]
					.filter(Boolean)
					.join('\n');
				return `<th class="bm-colh${lead.has(c.id) ? ' lead' : ''}" data-tip="${esc(tip)}"><span class="bm-name">${esc(c.label)}</span></th>`;
			})
			.join('')}
	</tr>
</thead>`;

	const body = view.categories
		.map((cat) => {
			const rows = cat.rows
				.map((row) => {
					const k = ++note;
					notes.push(`<li value="${k}"><b>${esc(row.label)}.</b> ${esc(row.note)}</li>`);
					const rk = rankRow(row, cols, st.rank);
					const dir = row.better === 'lower' ? '↓' : '↑';
					const tds = cols
						.map((c) => {
							const cell = row.cells[c.id];
							const cls = ['bm-v', lead.has(c.id) ? 'lead' : '', rk[c.id] ? 'r' + rk[c.id] : ''].filter(Boolean).join(' ');
							if (!cell) return `<td class="${cls} na" data-tip="${esc(`${c.label} ${familyLabel(c)}: no value in the atlas that passes this row's rules`)}">—</td>`;
							const pub = view.sources[cell.source_id];
							const num = cell.vmax != null ? `${fmtNum(Math.min(cell.v, cell.vmax), row.fmt)}–${fmtNum(Math.max(cell.v, cell.vmax), row.fmt)}` : fmtNum(cell.v, row.fmt);
							const txt = `${cell.q ? esc(QUAL[cell.q] ?? '') : ''}${num}${cell.basis === PC ? '<sup class="bm-pc">†</sup>' : ''}`;
							const inner = pub?.url ? `<a href="${esc(pub.url)}" target="_blank" rel="noopener">${txt}</a>` : `<span>${txt}</span>`;
							return `<td class="${cls}" data-tip="${esc(cellTip(row, c, cell, pub))}">${inner}</td>`;
						})
						.join('');
					return `<tr class="bm-row"><th class="bm-stub" scope="row"><span class="bm-label">${esc(row.label)}<sup class="bm-fn">${k}</sup></span><span class="bm-sub">${esc(row.sub)} · <span class="bm-unit">${esc(row.unit || 'no unit')}</span> <span class="bm-dir" data-tip="${row.better === 'lower' ? 'lower is better' : 'higher is better'}">${dir}</span></span></th>${tds}</tr>`;
				})
				.join('');
			return `<tr class="bm-cat"><th colspan="${ncol}"><span>${esc(cat.label)}</span></th></tr>${rows}`;
		})
		.join('');

	const foot = `<tfoot>
	<tr class="bm-sum"><th class="bm-stub" scope="row" data-tip="Rows in which the column holds the best value (${st.rank === 'all' ? 'among all shown columns' : 'within its family'})">Row bests</th>${cols.map((c) => `<td class="bm-v${lead.has(c.id) ? ' lead' : ''}">${wins[c.id]}</td>`).join('')}</tr>
	<tr class="bm-sum"><th class="bm-stub" scope="row" data-tip="Rows with a value in this column, out of ${nRows}">Rows reported</th>${cols.map((c) => `<td class="bm-v${lead.has(c.id) ? ' lead' : ''}">${c.n_rows}</td>`).join('')}</tr>
</tfoot>`;

	const r = view.rules;
	const basisWords = r.basis.map((b) => BASIS[b] ?? words(b)).join(', ');
	const famNotes = view.families.map((f) => `<b>${esc(f.label)}</b>: ${esc(f.tip)}.`).join(' ');
	const general = `<div class="bm-notes">
	<ol>${notes.join('')}</ol>
	<p>Each cell is the best value the atlas holds for a component fabricated in that foundry's process, from the publications it cites (${esc(basisWords)}); it is a literature result, not a PDK specification. A reported range (spread over dies, channels or a band) is shown as a range and ranked at its midpoint; bounds pointing the wrong way, standard deviations, design and simulated values, author estimates and rows below ${r.min_temperature_k} K are not entered. Telecom rows: ${r.telecom_window_nm[0]}-${r.telecom_window_nm[1]} nm. Columns with fewer than ${r.min_rows_per_column} filled rows and rows with fewer than ${r.min_columns_per_row} filled columns are not shown, except pinned columns (${esc(cols.filter((c) => c.pinned).map((c) => `${c.label} ${familyLabel(c)}`).join(', ') || 'none')}), which are always shown. ${anyPc ? 'Values marked † are unpublished values from private communication, dated in the tooltip; they are ranked like any value. ' : ''} Hover a value for its device, conditions and publication; click to open the publication.</p>
	<p>${famNotes} AMF / IME: Advanced Micro Foundry and A*STAR Institute of Microelectronics in one column; the tooltip names the organization of each value. Modulator rows (EO modulator atlas) take the platform's native effect only.</p>
</div>`;

	return `${toolbar}<div class="bm-scroll"><table class="bm-t">${head}<tbody>${body}</tbody>${foot}</table>${general}</div>`;
}

/** Hash state: #rank=family&hide=sin */
export function readState(/** @type {string} */ hash) {
	const p = new URLSearchParams(hash.replace(/^#/, ''));
	return /** @type {BenchState} */ ({
		rank: p.get('rank') === 'family' ? 'family' : 'all',
		hidden: (p.get('hide') ?? '').split(',').filter(Boolean)
	});
}
export function writeState(/** @type {BenchState} */ st) {
	const p = new URLSearchParams();
	if (st.rank !== 'all') p.set('rank', st.rank);
	if (st.hidden.length) p.set('hide', st.hidden.join(','));
	const s = p.toString();
	return s ? '#' + s : '';
}

/**
 * Render into `el` and handle the toolbar. Returns a function that detaches the handler.
 * @param {HTMLElement} el @param {BenchmarkView} view
 * @param {{ title?: string, themeToggle?: boolean, onTheme?: () => void }} [opt]
 */
export function mountBenchmark(el, view, opt = {}) {
	let st = readState(location.hash);
	const draw = () => {
		const sx = el.querySelector('.bm-scroll')?.scrollLeft ?? 0;
		const sy = el.querySelector('.bm-scroll')?.scrollTop ?? 0;
		el.innerHTML = renderBenchmark(view, st, opt);
		const sc = el.querySelector('.bm-scroll');
		if (sc) (sc.scrollLeft = sx), (sc.scrollTop = sy);
	};
	const click = (/** @type {MouseEvent} */ e) => {
		const b = /** @type {HTMLElement | null} */ (e.target instanceof Element ? e.target.closest('button') : null);
		if (!b || !el.contains(b)) return;
		if (b.dataset.bmRank) st = { ...st, rank: b.dataset.bmRank === 'family' ? 'family' : 'all' };
		else if (b.dataset.bmFam) {
			const f = b.dataset.bmFam;
			const hidden = st.hidden.includes(f) ? st.hidden.filter((x) => x !== f) : [...st.hidden, f];
			if (hidden.length >= view.families.length) return; // keep one family
			st = { ...st, hidden };
		} else if ('bmTheme' in b.dataset) {
			opt.onTheme?.();
			return;
		} else return;
		history.replaceState(history.state, '', location.pathname + location.search + writeState(st));
		draw();
	};
	el.addEventListener('click', click);
	draw();
	return () => el.removeEventListener('click', click);
}
