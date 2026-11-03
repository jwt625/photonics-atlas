// Load / navigation timing of the atlas in a real browser (DevLog-012). Budget: every route starts showing within 100 ms.
//   node scripts/perf.mjs <base-url> [--cpu=4] [--runs=1] [--latency=0] [--out=file.json]
// Modes: cold (empty cache), warm (same context, second load), spa (click a nav link from the dashboard).
// Times are ms from navigation start (cold / warm) or from the click (spa), read inside the page.
import { chromium } from 'playwright-core';
import { readdirSync, writeFileSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const args = process.argv.slice(2);
const base = (args.find((a) => !a.startsWith('--')) ?? '').replace(/\/$/, '');
const opt = (k, d) => {
	const a = args.find((x) => x.startsWith(`--${k}=`));
	return a ? a.split('=')[1] : d;
};
if (!base) throw new Error('usage: perf.mjs <base-url> [--cpu=4] [--runs=1] [--latency=0] [--out=file.json]');
const CPU = Number(opt('cpu', 1));
const RUNS = Number(opt('runs', 1));
const LATENCY = Number(opt('latency', 0));
const OUT = opt('out', '');
const ONLY = opt('only', '');
const SETTLE_MS = 20000;

// route -> the selector that means real data is on screen
const ROUTES = [
	{ path: '/', tab: 'Dashboard', ready: '.tile' },
	{ path: '/orgs', tab: 'Organizations', ready: 'table tbody tr' },
	{ path: '/components', tab: 'Components', ready: 'table tbody tr' },
	{ path: '/supply', tab: 'Supply', ready: 'main table tbody tr, main .bar' },
	{ path: '/people', tab: 'People', ready: 'table tbody tr' },
	{ path: '/layout', tab: 'Layouts', ready: 'main svg' },
	{ path: '/explore', tab: 'Explore', ready: '.grid .main-svg' },
	{ path: '/about', tab: 'About', ready: 'main p' },
	{ path: '/orgs/hub?id=org_intel', ready: 'main .hd' },
	{ path: '/layout?id=__first__', ready: 'main svg' }
];

function browserPath() {
	const root = join(homedir(), 'Library/Caches/ms-playwright');
	const dirs = readdirSync(root).filter((d) => d.startsWith('chromium-')).sort((a, b) => Number(b.split('-')[1]) - Number(a.split('-')[1]));
	for (const d of dirs) {
		for (const p of ['chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium']) {
			if (existsSync(join(root, d, p))) return join(root, d, p);
		}
	}
	throw new Error('no chromium in ' + root);
}

// Runs before any page script. Everything is recorded on window.__perf, relative to navigation start (timeOrigin).
const probe = () => {
	const P = (window.__perf = { first: {}, longtasks: [], fcp: null, lcp: null, click: null });
	new PerformanceObserver((l) => {
		for (const e of l.getEntries()) if (e.name === 'first-contentful-paint') P.fcp = e.startTime;
	}).observe({ type: 'paint', buffered: true });
	new PerformanceObserver((l) => {
		for (const e of l.getEntries()) P.lcp = e.startTime;
	}).observe({ type: 'largest-contentful-paint', buffered: true });
	new PerformanceObserver((l) => {
		for (const e of l.getEntries()) P.longtasks.push([Math.round(e.startTime), Math.round(e.duration)]);
	}).observe({ type: 'longtask', buffered: true });
	// time of the first paint after the mark (a frame is produced after the double rAF)
	P.mark = (k) => {
		if (P.first[k] !== undefined) return;
		P.first[k] = -1;
		requestAnimationFrame(() => setTimeout(() => (P.first[k] = performance.now()), 0));
	};
	P.ready = null;
	const scan = () => {
		const main = document.querySelector('main');
		if (document.querySelector('header nav')) P.mark('shell');
		if (main && main.querySelector('.skel, svg, table, canvas, p, a, input')) P.mark('main');
		// not while the layout's placeholder covers the old page, whose rows may match
		if (P.ready && !document.querySelector('.changing') && document.querySelector(P.ready)) P.mark('ready');
		if (P.click) {
			const a = document.querySelector('nav a.active');
			if (a && a.textContent.trim() === P.click.tab) P.mark('active');
		}
	};
	P.scan = scan;
	new MutationObserver(scan).observe(document, { subtree: true, childList: true, attributes: true, attributeFilter: ['class'] });
};

const summarize = (P, from = 0) => {
	const lt = P.longtasks.filter(([s]) => s >= from);
	return {
		tasksOver50: lt.length,
		maxTask: lt.reduce((m, [, d]) => Math.max(m, d), 0),
		blocked: lt.reduce((t, [, d]) => t + Math.max(0, d - 50), 0)
	};
};
const rel = (v, from) => (v === undefined || v === null || v < 0 ? null : Math.round(v - from));

async function setup(ctx, page) {
	await page.addInitScript(probe);
	if (CPU > 1 || LATENCY > 0) {
		const c = await ctx.newCDPSession(page);
		if (CPU > 1) await c.send('Emulation.setCPUThrottlingRate', { rate: CPU });
		if (LATENCY > 0) {
			await c.send('Network.enable');
			await c.send('Network.emulateNetworkConditions', { offline: false, latency: LATENCY, downloadThroughput: -1, uploadThroughput: -1 });
		}
	}
}

async function resolvePath(r, first) {
	return r.path.replace('__first__', encodeURIComponent(first));
}

async function loadOnce(page, url, ready) {
	await page.addInitScript((s) => {
		const set = () => (window.__perf ? (window.__perf.ready = s) : setTimeout(set, 0));
		set();
	}, ready);
	await page.goto(url, { waitUntil: 'commit' });
	await page.waitForFunction(() => window.__perf && window.__perf.first.ready > 0, undefined, { timeout: SETTLE_MS }).catch(() => {});
	await page.waitForTimeout(600);
	return page.evaluate(() => {
		const P = window.__perf;
		return { first: P.first, fcp: P.fcp, lcp: P.lcp, longtasks: P.longtasks, status: document.title };
	});
}

const browser = await chromium.launch({ headless: true, executablePath: browserPath() });
const rows = [];
const firstId = 'showcase';
let layoutId = firstId;
{
	const ctx = await browser.newContext();
	const page = await ctx.newPage();
	const res = await page.request.get(`${base}/data/components.json`).catch(() => null);
	const j = res && res.ok() ? await res.json().catch(() => null) : null;
	layoutId = j?.showcase?.[0]?.component_id ?? firstId;
	await ctx.close();
}

const record = (mode, path, o) => {
	const row = { mode, path, ...o };
	rows.push(row);
	console.log(
		`${mode.padEnd(5)} ${path.slice(0, 26).padEnd(26)} paint=${String(o.paint).padStart(6)} main=${String(o.main).padStart(6)} ready=${String(o.ready).padStart(6)} maxTask=${String(o.maxTask).padStart(5)} blocked=${String(o.blocked).padStart(6)}`
	);
};

for (let run = 0; run < RUNS; run++) {
	for (const r of ONLY === 'spa' ? [] : ROUTES) {
		const path = await resolvePath(r, layoutId);
		const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
		const page = await ctx.newPage();
		await setup(ctx, page);
		const cold = await loadOnce(page, base + path, r.ready);
		record('cold', path, { paint: rel(cold.fcp, 0), shell: rel(cold.first.shell, 0), main: rel(cold.first.main, 0), ready: rel(cold.first.ready, 0), lcp: rel(cold.lcp, 0), ...summarize(cold) });
		// a service worker, if there is one, has to finish installing before the second load
		await page.evaluate(() => {
			if (!('serviceWorker' in navigator)) return;
			return Promise.race([
				navigator.serviceWorker.getRegistration().then((r) => (r ? navigator.serviceWorker.ready : null)),
				new Promise((res) => setTimeout(res, 15000))
			]);
		});
		await page.waitForTimeout(500);
		const warm = await loadOnce(page, base + path, r.ready);
		record('warm', path, { paint: rel(warm.fcp, 0), shell: rel(warm.first.shell, 0), main: rel(warm.first.main, 0), ready: rel(warm.first.ready, 0), lcp: rel(warm.lcp, 0), ...summarize(warm) });
		await ctx.close();
	}

	// SPA: one context, start at the dashboard, click each tab in turn; hover first as a real pointer does
	const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
	const page = await ctx.newPage();
	await setup(ctx, page);
	await loadOnce(page, base + '/', '.tile');
	// .tile is in the prerendered HTML: wait for the app itself (a click before hydration is a plain page load)
	await page.waitForLoadState('networkidle', { timeout: SETTLE_MS }).catch(() => {});
	for (const r of [...ROUTES.filter((x) => x.tab && x.path !== '/'), ROUTES[0]]) {
		const link = page.locator('nav a', { hasText: r.tab }).first();
		await link.hover();
		await page.waitForTimeout(120);
		const res = await page.evaluate(
			({ tab, ready }) =>
				new Promise((resolve) => {
					const P = window.__perf;
					P.first = {};
					P.ready = ready;
					const t0 = performance.now();
					P.click = { tab, t0 };
					const a = [...document.querySelectorAll('nav a')].find((x) => x.textContent.trim() === tab);
					a.click();
					const done = () => {
						if (P.first.ready > 0) resolve({ t0, first: P.first, longtasks: P.longtasks });
						else if (performance.now() - t0 > 20000) resolve({ t0, first: P.first, longtasks: P.longtasks });
						else setTimeout(done, 25);
					};
					done();
				}),
			{ tab: r.tab, ready: r.ready }
		);
		const { t0 } = res;
		await page.waitForTimeout(600);
		const lt = await page.evaluate(() => window.__perf.longtasks);
		record('spa', r.path, { paint: rel(res.first.active, t0), main: rel(res.first.main, t0), ready: rel(res.first.ready, t0), ...summarize({ longtasks: lt }, t0) });
	}
	await ctx.close();
}
await browser.close();
if (OUT) writeFileSync(OUT, JSON.stringify({ base, cpu: CPU, latency: LATENCY, at: new Date().toISOString(), rows }, null, 1));
