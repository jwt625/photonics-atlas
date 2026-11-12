// @ts-nocheck plain node script
// History stories video capture (DevLog-018): for every story in static/data/showcases/*.json, render one complete
// playthrough as a fixed-fps JPEG frame sequence. Pacing = the runtime's Play plan (playPlan) scaled to the loop length,
// with hover pauses inserted; per frame: set the scroll position for p(t), draw the cursor arrow, put the real pointer on
// the target during holds (parked on the footer otherwise), wait for the story to draw, screenshot the 1920 x 1080 stage. Hover targets are found by scanning the pane with
// pointer events and reading the tooltip, never guessed. Resumable: a story with a matching done.json is skipped.
//
// Usage (a dev or preview server must be running; history menu bar is unpinned in the capture context):
//   node scripts/showcase-video.mjs <server url> [--out=../cache/showcase_video] [--workers=4] [--T=15] [--fps=30]
//        [--hero=macchesney1974] [--small-scale=0.5] [--dsf=2] [--reuse-hovers] [--range=a:b (test frames, no done.json)]
//        [--force] [id ...]
// Frames render at --dsf device px per CSS px and are box-filtered down by scripts/showcase_video_downsample.py (uv).
// Browser: the installed Google Chrome (override with CHROME=/path/to/chrome).
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync, appendFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import { chromium } from 'playwright-core';
import { playPlan, playAt, chapterTarget } from '../src/lib/history/showcase/progress.ts';

const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(APP, 'static/data/showcases');
const args = process.argv.slice(2);
const opt = (k, d) => args.find((a) => a.startsWith(`--${k}=`))?.split('=')[1] ?? d;
const flag = (k) => args.includes(`--${k}`);
const base = (args.find((a) => /^https?:\/\//.test(a)) || '').replace(/\/$/, '');
if (!base) {
	console.error('usage: node scripts/showcase-video.mjs <server url> [options] [id ...]');
	process.exit(2);
}
const OUT = resolve(APP, opt('out', '../cache/showcase_video'));
const WORKERS = Number(opt('workers', 4));
const T = Number(opt('T', 15)); // loop length, s (D1120)
const FPS = Number(opt('fps', 30));
const HERO = opt('hero', 'macchesney1974');
const SMALL = Number(opt('small-scale', 0.5)); // output scale of non-hero stories vs 1920 x 1080 (D1125)
const DSF = Number(opt('dsf', 2)); // render at this device pixel ratio, box-filter down to the output size (D1132)
const HELPER = resolve(APP, '../scripts/showcase_video_downsample.py');
const PAUSE = 0.8; // hover hold, s (D1124)
const GLIDE = 0.6; // cursor glide to a target, s
const RAMP = 0.3; // playback slows to the hold and speeds back up over this time, cosine rate ramps (D1133)
const VW = 1920;
const VH = 1100; // stage = scroll container = VH - 20 px footer = 1080 (D1123)
const only = args.filter((a) => !a.startsWith('--') && !/^https?:\/\//.test(a));
const ids = readdirSync(SRC)
	.filter((f) => f.endsWith('.json'))
	.map((f) => f.slice(0, -5))
	.filter((id) => !only.length || only.includes(id))
	.sort();
mkdirSync(join(OUT, 'frames'), { recursive: true });
mkdirSync(join(OUT, 'hovers'), { recursive: true });
mkdirSync(join(OUT, 'tmp'), { recursive: true });
const stamp = new Date().toISOString().replace(/[:T]/g, '-').slice(0, 19);
const LOG = join(OUT, `capture-${stamp}.log`);
const log = (s) => {
	const line = `${new Date().toISOString()} ${s}`;
	console.log(line);
	appendFileSync(LOG, line + '\n');
};

// ---------------------------------------------------------------------------------------------- page helpers
async function openStory(browser, id) {
	const ctx = await browser.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: DSF });
	await ctx.addInitScript(() => {
		try {
			localStorage.setItem('pa-atlas-theme', 'dark');
			localStorage.setItem('history.barPinned', 'false');
		} catch {}
	});
	const pg = await ctx.newPage();
	await pg.goto(`${base}/history`);
	await pg.waitForSelector(`#story-${id}`, { timeout: 60000 });
	await pg.evaluate((id) => document.getElementById(`story-${id}`).scrollIntoView(), id);
	await pg.waitForSelector(`#story-${id}[data-thumb-p]`, { timeout: 60000 });
	await pg.waitForSelector(`#story-${id} .playbtn:not([disabled])`, { timeout: 60000 });
	await pg.mouse.move(VW / 2, VH - 4); // footer: no hover
	// in-page helpers: geometry, set p, wait frames, cursor overlay, hover scans
	await pg.evaluate((id) => {
		const art = document.getElementById(`story-${id}`);
		const track = art.querySelector('.track');
		let sc = track.parentElement;
		while (sc && !(/(auto|scroll)/.test(getComputedStyle(sc).overflowY) && sc.scrollHeight > sc.clientHeight + 1)) sc = sc.parentElement;
		const raf = () => new Promise((r) => requestAnimationFrame(() => r()));
		const W = (window.__vid = {
			art,
			sc,
			geom() {
				const tr = track.getBoundingClientRect();
				const vr = sc.getBoundingClientRect();
				W.off = sc.scrollTop + tr.top - vr.top;
				W.run = Math.max(0, tr.height - sc.clientHeight);
			},
			setP(p) {
				sc.scrollTop = W.off + p * W.run;
			},
			async frames(n) {
				for (let i = 0; i < n; i++) await raf();
			},
			stage() {
				const r = art.querySelector('.stage').getBoundingClientRect();
				return { x: r.x, y: r.y, w: r.width, h: r.height };
			},
			cursor(x, y) {
				let c = document.getElementById('__vid_cursor');
				if (!c) {
					c = document.createElement('div');
					c.id = '__vid_cursor';
					c.style.cssText = 'position:fixed;left:0;top:0;width:24px;height:36px;pointer-events:none;z-index:2147483647;will-change:transform';
					c.innerHTML =
						'<svg width="24" height="36" viewBox="0 0 16 24"><path d="M1 1 L1 19 L5.5 14.8 L8.6 22 L11.4 20.8 L8.4 13.8 L14.5 13.8 Z" fill="#fff" stroke="#000" stroke-width="1.2" stroke-linejoin="round"/></svg>';
					document.body.appendChild(c);
				}
				c.style.transform = `translate(${x - 1.5}px, ${y - 1.5}px)`;
			},
			tipText() {
				const t = art.querySelector('.sctip');
				if (t) return t.innerText.trim();
				const g = document.querySelector('.tip-pop');
				return g ? g.innerText.trim() : '';
			},
			async move(x, y, n = 2) {
				const el = document.elementFromPoint(x, y);
				if (!el) return;
				el.dispatchEvent(new PointerEvent('pointermove', { clientX: x, clientY: y, bubbles: true, pointerType: 'mouse', buttons: 0 }));
				for (let i = 0; i < n; i++) await raf();
			},
			/** scan a rect with pointer moves; returns hits [{x, y, name}] (tooltip first line) */
			async scan(r, step, accept, n = 2) {
				const hits = [];
				for (let y = r.y + step / 2; y < r.y + r.h; y += step)
					for (let x = r.x + step / 2; x < r.x + r.w; x += step) {
						const el = document.elementFromPoint(x, y);
						if (!el || !accept(el)) continue;
						await W.move(x, y, n);
						const t = art.querySelector('.sctip');
						const fresh = t && Math.abs(parseFloat(t.style.left) - Math.min(x + 14, innerWidth - 270)) < 1 && Math.abs(parseFloat(t.style.top) - (y + 16)) < 1;
						if (fresh) hits.push({ x, y, name: t.innerText.trim().split('\n')[0], text: t.innerText.trim() });
					}
				await W.move(innerWidth / 2, innerHeight - 4);
				return hits;
			},
			plotLive() {
				const b = art.querySelector('.plotbox.live');
				return b ? b.getBoundingClientRect().toJSON() : null;
			},
			stepRect() {
				const s = art.querySelector('.step');
				return s && s.getAttribute('data-tip') ? s.getBoundingClientRect().toJSON() : null;
			},
			/** resting spot of the drawn cursor */
			rest() {
				// the real pointer is parked off-stage outside holds, so the drawn arrow may rest anywhere: low centre
				const c = art.querySelector('.ctrl').getBoundingClientRect();
				return { x: c.left + 0.6 * c.width, y: c.top - 48 };
			}
		});
		W.geom();
	}, id);
	return { ctx, pg };
}

async function setP(pg, p) {
	await pg.evaluate(async (p) => {
		window.__vid.setP(p);
		await window.__vid.frames(3);
	}, p);
}

// ---------------------------------------------------------------------------------------------- hover targets
/** Pick hover targets for a story (D1124): a 3D part near 35 % of the chapters, the first plot chapter after it (a
 *  revealed point), MCVD also the process step chip. Each target is a real tooltip found by scanning. */
async function findHovers(pg, spec, hero) {
	const ch = spec.chapters;
	const n = ch.length;
	await setP(pg, 0.5);
	const stage = await pg.evaluate(() => window.__vid.stage());
	const out = [];
	// part hover: chapters from 35 % onwards (then before), first one with a hit on a part of that chapter
	const order = [...Array(n).keys()].sort((a, b) => Math.abs(a - 0.35 * (n - 1)) - Math.abs(b - 0.35 * (n - 1)));
	const partHover = async (skip) => {
		for (const ci of order) {
			if (skip.has(ci)) continue;
			const p = chapterTarget(ch[ci]);
			await setP(pg, p);
			await pg.waitForTimeout(300);
			const plot = await pg.evaluate(() => window.__vid.plotLive());
			// model pane minus the side column, the control bar, and the plot when it is on screen
			const pane = await pg.evaluate(() => window.__vid.art.querySelector('.model').getBoundingClientRect().toJSON());
			const r = { x: pane.x + 10, y: pane.y + 150, w: (plot ? plot.x - pane.x : pane.width) - 20, h: pane.height - 200 };
			const hits = await pg.evaluate(
				async ([r]) => window.__vid.scan(r, 40, (el) => !el.closest('.plotbox, .ctrl, .lab, .step, .kw')),
				[r]
			);
			if (!hits.length) continue;
			const by = new Map();
			for (const h of hits) by.set(h.name, [...(by.get(h.name) || []), h]);
			const chParts = new Set((ch[ci].parts || []).map((id) => (spec.parts.find((q) => q.id === id) || {}).name).filter(Boolean));
			const cands = [...by.entries()].filter(([, hs]) => hs.length >= 3);
			if (!cands.length) continue;
			cands.sort((a, b) => (chParts.has(b[0]) - chParts.has(a[0])) || b[1].length - a[1].length);
			const [name, hs] = cands[0];
			const cx = hs.reduce((s, h) => s + h.x, 0) / hs.length;
			const cy = hs.reduce((s, h) => s + h.y, 0) / hs.length;
			const best = hs.reduce((a, h) => (Math.hypot(h.x - cx, h.y - cy) < Math.hypot(a.x - cx, a.y - cy) ? h : a));
			return { kind: 'part', chapter: ci, p, x: best.x, y: best.y, name, hits: hs.length };
		}
		return null;
	};
	const used = new Set();
	const h1 = await partHover(used);
	if (h1) {
		out.push(h1);
		used.add(h1.chapter);
	}
	// plot hover: first chapter after the part hover (else any) whose plot is live at its end
	let plotH = null;
	const after = [...Array(n).keys()].filter((i) => !used.has(i));
	after.sort((a, b) => ((a > (h1?.chapter ?? -1)) === (b > (h1?.chapter ?? -1)) ? a - b : a > (h1?.chapter ?? -1) ? -1 : 1));
	for (const ci of after) {
		const p = chapterTarget(ch[ci]);
		await setP(pg, p);
		const plot = await pg.evaluate(() => window.__vid.plotLive());
		if (!plot) continue;
		await pg.waitForTimeout(400);
		const svg = await pg.evaluate(() => {
			const s = window.__vid.art.querySelector('.plotbox.live svg');
			return s ? s.getBoundingClientRect().toJSON() : null;
		});
		if (!svg) continue;
		const hits = await pg.evaluate(async ([r]) => window.__vid.scan(r, 12, (el) => !!el.closest('.plotbox svg'), 1), [
			{ x: svg.x + 40, y: svg.y + 10, w: svg.width - 60, h: svg.height - 50 }
		]);
		if (!hits.length) continue;
		// prefer hits on drawn markers (measured points), not on guide or model lines; legend swatches excluded
		const dots = await pg.evaluate(() =>
			[...window.__vid.art.querySelectorAll('.plotbox.live svg circle:not(.swo)')].map((c) => {
				const r = c.getBoundingClientRect();
				return [r.x + r.width / 2, r.y + r.height / 2];
			})
		);
		const onDot = hits.filter((h) => dots.some(([x, y]) => Math.hypot(x - h.x, y - h.y) < 7));
		if (onDot.length) hits.splice(0, hits.length, ...onDot);
		else {
			// line-only plot: the series with the most hits (the main curve, not a short guide)
			const cnt = new Map();
			for (const h of hits) cnt.set(h.name, (cnt.get(h.name) || 0) + 1);
			const top = [...cnt.entries()].sort((a, b) => b[1] - a[1])[0][0];
			hits.splice(0, hits.length, ...hits.filter((h) => h.name === top));
		}
		// a point right of centre, near the middle of the plot height
		const gx = svg.x + 0.62 * svg.width;
		const gy = svg.y + 0.45 * svg.height;
		const best = hits.reduce((a, h) => (Math.hypot(h.x - gx, (h.y - gy) * 0.5) < Math.hypot(a.x - gx, (a.y - gy) * 0.5) ? h : a));
		plotH = { kind: 'plot', chapter: ci, p, x: best.x, y: best.y, name: best.name, hits: hits.length };
		break;
	}
	if (plotH) {
		out.push(plotH);
		used.add(plotH.chapter);
	} else {
		// no plot: a second part, late in the story
		order.sort((a, b) => Math.abs(a - 0.75 * (n - 1)) - Math.abs(b - 0.75 * (n - 1)));
		const h2 = await partHover(used);
		if (h2) {
			out.push(h2);
			used.add(h2.chapter);
		}
	}
	if (hero) {
		// process step chip: the chapter with a step nearest 60 %
		const sorder = [...Array(n).keys()].filter((i) => !used.has(i)).sort((a, b) => Math.abs(a - 0.6 * (n - 1)) - Math.abs(b - 0.6 * (n - 1)));
		for (const ci of sorder) {
			const p = chapterTarget(ch[ci]);
			await setP(pg, p);
			const r = await pg.evaluate(() => window.__vid.stepRect());
			if (!r) continue;
			out.push({ kind: 'step', chapter: ci, p, x: r.x + Math.min(40, r.width / 2), y: r.y + r.height / 2, name: 'process step', hits: 1 });
			break;
		}
	}
	out.sort((a, b) => a.p - b.p);
	return { stage, hovers: out };
}

// ---------------------------------------------------------------------------------------------- timeline
/** Output frames -> {p, cursor, pause}. Play plan (runtime pacing) scaled to T minus pauses; a pause holds at the
 *  hover chapter's end, entered and left through RAMP s cosine rate ramps (rate 1 -> 0 -> hold -> 0 -> 1, each ramp
 *  costs RAMP / 2 of play time); the cursor glides to each target, then back to rest unless the next glide starts soon. */
function timeline(spec, hovers, rest) {
	const plan = playPlan(spec.chapters, 0, () => false, false);
	const D = plan.length ? plan[plan.length - 1].t0 + plan[plan.length - 1].move + plan[plan.length - 1].dwell : 1;
	const N = Math.round(T * FPS);
	const LOST = PAUSE + RAMP; // output time per hover not spent on play: the hold plus two half ramps
	const k = (T - hovers.length * LOST) / (D / 1000); // output s per play s
	// play time (ms) at which each hover chapter is reached = end of the leg that targets it
	const ev = hovers.map((h) => {
		const L = plan.find((l) => Math.abs(l.to - h.p) < 1e-6);
		const tp = L ? L.t0 + L.move : 0;
		return { ...h, tp };
	});
	ev.forEach((e, i) => (e.u0 = (e.tp / 1000) * k + i * LOST + RAMP / 2)); // output time the hold starts
	const ease = (x) => (x < 0.5 ? 2 * x * x : 1 - (-2 * x + 2) ** 2 / 2);
	// cursor keyframes: rest -> target (arrive at u0) -> hold -> rest
	const keys = [{ u: 0, x: rest.x, y: rest.y }];
	ev.forEach((e, i) => {
		const prev = keys[keys.length - 1];
		keys.push({ u: Math.max(prev.u, e.u0 - GLIDE), x: prev.x, y: prev.y });
		keys.push({ u: e.u0, x: e.x, y: e.y, glide: true });
		keys.push({ u: e.u0 + PAUSE, x: e.x, y: e.y });
		const next = ev[i + 1];
		if (!next || next.u0 - GLIDE > e.u0 + PAUSE + GLIDE + 0.3) keys.push({ u: Math.min(e.u0 + PAUSE + GLIDE, T - 1 / FPS), x: rest.x, y: rest.y, glide: true });
	});
	const cursorAt = (u) => {
		let a = keys[0];
		for (let i = 1; i < keys.length; i++) {
			const b = keys[i];
			if (u <= b.u) {
				const t = b.u > a.u ? ease((u - a.u) / (b.u - a.u)) : 1;
				return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
			}
			a = b;
		}
		return { x: a.x, y: a.y };
	};
	const frames = [];
	for (let f = 0; f < N; f++) {
		const u = f / FPS;
		let extra = 0; // output time not spent on play before u (ramps and holds)
		let pause = -1;
		const W = RAMP / (2 * Math.PI);
		for (let i = 0; i < ev.length; i++) {
			const e = ev[i];
			const a = e.u0 - RAMP; // ramp down [a, u0], hold [u0, b], ramp up [b, b + RAMP]
			const b = e.u0 + PAUSE;
			if (u <= a) continue;
			if (u < e.u0) extra += 0.5 * (u - a) - W * Math.sin((Math.PI * (u - a)) / RAMP);
			else if (u < b) {
				extra += RAMP / 2 + (u - e.u0);
				pause = i;
			} else if (u < b + RAMP) extra += RAMP / 2 + PAUSE + 0.5 * (u - b) + W * Math.sin((Math.PI * (u - b)) / RAMP);
			else extra += LOST;
		}
		const tp = Math.min(D, ((u - extra) / k) * 1000);
		const p = f === N - 1 ? 1 : pause >= 0 ? ev[pause].p : playAt(plan, tp);
		const c = cursorAt(u);
		frames.push({ f, u, p, x: Math.round(c.x * 2) / 2, y: Math.round(c.y * 2) / 2, pause });
	}
	return { frames, plan: { D, k, N }, events: ev };
}

// ---------------------------------------------------------------------------------------------- capture
async function captureStory(browser, id) {
	const spec = JSON.parse(readFileSync(join(SRC, `${id}.json`), 'utf8'));
	const hero = id === HERO;
	const scale = hero ? 1 : SMALL;
	const dir = join(OUT, 'frames', id);
	const sig = JSON.stringify({ T, FPS, scale, DSF, PAUSE, GLIDE, RAMP, v: 4 });
	const factor = Math.round(DSF / scale);
	const done = join(dir, 'done.json');
	if (!flag('force') && existsSync(done) && JSON.parse(readFileSync(done, 'utf8')).sig === sig) return log(`${id} skip (done)`);
	if (existsSync(dir)) rmSync(dir, { recursive: true }); // our own frames only
	mkdirSync(dir, { recursive: true });
	const t0 = Date.now();
	const { ctx, pg } = await openStory(browser, id);
	try {
		// --reuse-hovers: targets from an earlier run (CSS px, independent of the device pixel ratio)
		const hfile = join(OUT, 'hovers', `${id}.json`);
		let stage, hovers;
		if (flag('reuse-hovers') && existsSync(hfile)) {
			const H = JSON.parse(readFileSync(hfile, 'utf8'));
			stage = H.stage;
			hovers = H.hovers.map(({ tp, u0, ...h }) => h);
			await setP(pg, 0.5);
		} else ({ stage, hovers } = await findHovers(pg, spec, hero));
		const rest = await pg.evaluate(() => window.__vid.rest());
		const tl = timeline(spec, hovers, rest);
		writeFileSync(join(OUT, 'hovers', `${id}.json`), JSON.stringify({ id, stage, rest, hovers: tl.events, plan: tl.plan }, null, 1));
		log(`${id} hovers ${hovers.map((h) => `${h.kind}@ch${h.chapter + 1}:${h.name}`).join(' | ')} (${((Date.now() - t0) / 1000).toFixed(1)} s)`);
		const cdp = await ctx.newCDPSession(pg);
		await pg.evaluate(() => window.__vid.geom());
		const PARK = { x: VW / 2, y: VH - 4 }; // site footer, below the stage: no hover
		const clip = { x: stage.x, y: stage.y, width: stage.w, height: stage.h, scale: DSF }; // CDP clip scale is per CSS px: DSF x 1920 x 1080 output
		const helper = spawn('uv', ['run', '-q', HELPER], { stdio: ['pipe', 'pipe', 'inherit'] });
		let helperOut = '';
		helper.stdout.on('data', (d) => (helperOut += d));
		const helperDone = new Promise((r) => helper.on('close', r));
		let lastDst = null;
		let last = null;
		let lastBuf = null;
		const tf = Date.now();
		const N = tl.frames.length;
		const [b0, b1] = (opt('range', '') || `0:${N}`).split(':').map(Number);
		for (let i = b0; i < Math.min(b1, N); i++) {
			const fr = tl.frames[i];
			const key = `${fr.p.toFixed(6)}|${fr.x}|${fr.y}`;
			if (key !== last || !lastBuf) {
				const first = fr.pause >= 0 && (i === 0 || tl.frames[i - 1].pause !== fr.pause);
				await pg.evaluate(
					async ([p, x, y]) => {
						window.__vid.setP(p);
						window.__vid.cursor(x, y);
						await window.__vid.frames(2); // the story draws this p before the pointer arrives
					},
					[fr.p, fr.x, fr.y]
				);
				if (fr.pause >= 0) await pg.mouse.move(fr.x, fr.y);
				else await pg.mouse.move(PARK.x, PARK.y);
				await pg.evaluate(() => window.__vid.frames(3));
				if (first) {
					// re-enter the target once the scene holds: data-tip tooltips hide on scroll and re-arm on pointerover
					await pg.mouse.move(PARK.x, PARK.y);
					await pg.mouse.move(fr.x, fr.y);
					await pg.waitForTimeout(700); // 350 ms data-tip delay, then settle
				}
				const r = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 95, clip, fromSurface: true });
				lastBuf = true;
				last = key;
				const tmp = join(OUT, 'tmp', `${id}_${i}.jpg`);
				writeFileSync(tmp, Buffer.from(r.data, 'base64'));
				lastDst = join(dir, `${String(i).padStart(4, '0')}.jpg`);
				helper.stdin.write(`${tmp}\t${lastDst}\t${factor}\n`);
			} else helper.stdin.write(`=\t${lastDst}\t${join(dir, `${String(i).padStart(4, '0')}.jpg`)}\n`);
		}
		helper.stdin.end();
		const code = await helperDone;
		if (code !== 0 || !helperOut.startsWith('done')) throw new Error(`downsample helper exit ${code}: ${helperOut}`);
		const sec = (Date.now() - tf) / 1000;
		log(`${id} ${Math.min(b1, N) - b0} frames in ${sec.toFixed(1)} s (${((sec / (Math.min(b1, N) - b0)) * 1000).toFixed(0)} ms/frame) scale ${scale} dsf ${DSF} box ${factor}`);
		if (!opt('range', '')) writeFileSync(done, JSON.stringify({ sig, frames: N, hovers: hovers.length, at: new Date().toISOString() }));
	} finally {
		await ctx.close();
	}
}

const browser = await chromium.launch({
	headless: true,
	executablePath: process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	args: ['--use-angle=metal']
});
log(`start ${ids.length} stories, T ${T} s, ${FPS} fps, hero ${HERO}, workers ${WORKERS}, out ${OUT}`);
const queue = [...ids].sort((a, b) => (b === HERO) - (a === HERO));
await Promise.all(
	Array.from({ length: Math.min(WORKERS, queue.length) }, async () => {
		while (queue.length) {
			const id = queue.shift();
			try {
				await captureStory(browser, id);
			} catch (e) {
				log(`${id} FAILED ${String(e.message).split('\n')[0]}`);
			}
		}
	})
);
await browser.close();
log('end');
