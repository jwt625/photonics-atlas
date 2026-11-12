// @ts-nocheck plain node script
// Story thumbnails for the compact history view (DevLog-017): for every story in static/data/showcases/*.json, scroll
// the expanded history view to the story's thumbnail frame (spec thumb_p, else the end of the last chapter before the
// first plot chapter: the runtime publishes it as data-thumb-p) in capture mode (?thumb=1: no keyword, labels, plot or
// step chip), screenshot the model pane, cover-crop it to 16:10 and write static/data/showcases/thumbs/<id>.webp (dark)
// and <id>.light.webp (light theme) at 480 x 300 px (2x the largest card).
//
// Usage (a dev or preview server must be running):
//   node scripts/showcase-thumbs.mjs http://127.0.0.1:<port> [id ...]
// Browser: the installed Google Chrome (override with CHROME=/path/to/chrome).
import { mkdirSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(APP, 'static/data/showcases');
const OUT = join(SRC, 'thumbs');
const W = 480;
const H = 300;
const base = (process.argv[2] || '').replace(/\/$/, '');
if (!/^https?:\/\//.test(base)) {
	console.error('usage: node scripts/showcase-thumbs.mjs <server url> [id ...]');
	process.exit(2);
}
const only = process.argv.slice(3);
const ids = readdirSync(SRC)
	.filter((f) => f.endsWith('.json'))
	.map((f) => f.slice(0, -5))
	.filter((id) => !only.length || only.includes(id))
	.sort();
mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({
	headless: true,
	executablePath: process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	args: ['--use-angle=metal']
});
const results = [];
for (const id of ids) {
	for (const theme of ['dark', 'light']) {
		const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
		await ctx.addInitScript((t) => {
			try {
				localStorage.setItem('pa-atlas-theme', t); // read by app.html and the layout (ui.theme reaches the scene modules)
			} catch {}
		}, theme);
		const pg = await ctx.newPage();
		try {
			await pg.goto(`${base}/history?thumb=1`);
			await pg.waitForSelector(`#story-${id}`, { timeout: 30000 });
			await pg.evaluate((id) => document.getElementById(`story-${id}`).scrollIntoView(), id);
			await pg.waitForSelector(`#story-${id}[data-thumb-p]`, { timeout: 30000 });
			const p = Number(await pg.getAttribute(`#story-${id}`, 'data-thumb-p'));
			await pg.evaluate(
				([id, p]) => {
					const track = document.querySelector(`#story-${id} .track`);
					let sc = track.parentElement;
					while (sc && !(/(auto|scroll)/.test(getComputedStyle(sc).overflowY) && sc.scrollHeight > sc.clientHeight + 1)) sc = sc.parentElement;
					const tr = track.getBoundingClientRect();
					const vr = sc.getBoundingClientRect();
					sc.scrollTop += tr.top - vr.top + p * (tr.height - sc.clientHeight);
				},
				[id, p]
			);
			await pg.mouse.move(2, 600); // no hover highlight
			await pg.waitForTimeout(2500);
			const png = await pg.locator(`#story-${id} .model`).screenshot();
			const webp = await pg.evaluate(
				async ([b64, W, H]) => {
					const img = new Image();
					img.src = `data:image/png;base64,${b64}`;
					await img.decode();
					// cover-crop the pane to 16:10, centred
					const k = Math.max(W / img.width, H / img.height);
					const sw = W / k;
					const sh = H / k;
					const c = document.createElement('canvas');
					c.width = W;
					c.height = H;
					const g = c.getContext('2d');
					g.imageSmoothingQuality = 'high';
					g.drawImage(img, (img.width - sw) / 2, (img.height - sh) / 2, sw, sh, 0, 0, W, H);
					return c.toDataURL('image/webp', 0.8).split(',')[1];
				},
				[png.toString('base64'), W, H]
			);
			const file = join(OUT, `${id}${theme === 'light' ? '.light' : ''}.webp`);
			writeFileSync(file, Buffer.from(webp, 'base64'));
			results.push(`${id} ${theme} p=${p.toFixed(3)} ${statSync(file).size} B`);
		} catch (e) {
			results.push(`${id} ${theme} FAILED ${e.message.split('\n')[0]}`);
		}
		await ctx.close();
	}
}
await browser.close();
console.log(results.join('\n'));
