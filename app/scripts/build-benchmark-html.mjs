// @ts-nocheck plain node script
// Standalone foundry PDK benchmark (DevLog-014 D905): one self-contained HTML file, no network requests. Embeds
// static/data/benchmark.json, the shared renderer (src/lib/benchmark/render.js), its CSS and the app's colour tokens.
// Output: static/pdk-benchmark.html (also served by the site). Usage: node scripts/build-benchmark-html.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const data = readFileSync(join(APP, 'static/data/benchmark.json'), 'utf8');
const render = readFileSync(join(APP, 'src/lib/benchmark/render.js'), 'utf8').replace(/^export /gm, '');
const css = readFileSync(join(APP, 'src/lib/benchmark/benchmark.css'), 'utf8');
const appCss = readFileSync(join(APP, 'src/app.css'), 'utf8');
// the two token blocks of the app (dark default, light override)
const tokens = [...appCss.matchAll(/^:root(?:\[data-theme='light'\])? \{[\s\S]*?^\}/gm)].map((m) => m[0]).join('\n');
if (!tokens.includes("data-theme='light'")) throw new Error('app.css token blocks not found');
const view = JSON.parse(data);

const base = `*,*::before,*::after{box-sizing:border-box}
html,body{height:100%;margin:0;background:var(--bg);color:var(--ink);font:12px/1.35 var(--sans);overflow:hidden}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
button{font:inherit;color:inherit;background:var(--surface-2);border:1px solid var(--border);border-radius:0;padding:2px 8px;height:24px;cursor:pointer}
button:hover{background:var(--hover);border-color:var(--ink-3)}
button.on{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
button:focus-visible,a:focus-visible{outline:1px solid var(--accent);outline-offset:1px}
.muted{color:var(--ink-3)}
.page{height:100%;display:grid;grid-template-rows:minmax(0,1fr) auto}
footer{display:flex;gap:6px;height:20px;align-items:center;padding:0 10px;font-size:10px;color:var(--ink-3);background:var(--surface);border-top:1px solid var(--border)}
.tip-pop{position:fixed;z-index:100;max-width:380px;padding:4px 7px;font-size:11px;line-height:1.4;color:var(--ink);background:var(--surface);border:1px solid var(--line);box-shadow:0 3px 10px rgba(0,0,0,.3);white-space:pre-wrap;overflow-wrap:anywhere;pointer-events:none;border-radius:0}`;

// minimal data-tip tooltip, same behaviour as the app's Tooltip.svelte (hover delay, follows the pointer)
const tip = `(() => {
	const pop = document.createElement('div'); pop.className = 'tip-pop'; pop.hidden = true; document.body.append(pop);
	let cur = null, timer = 0;
	const place = (x, y) => { const w = pop.offsetWidth, h = pop.offsetHeight;
		pop.style.left = Math.max(4, Math.min(x + 12, innerWidth - w - 4)) + 'px';
		pop.style.top = (y + 18 + h > innerHeight - 4 ? Math.max(4, y - h - 8) : y + 18) + 'px'; };
	const hide = () => { clearTimeout(timer); pop.hidden = true; cur = null; };
	document.addEventListener('pointerover', (e) => {
		const t = e.target.closest?.('[data-tip]') ?? null; if (t === cur) return;
		hide(); cur = t; if (!t) return;
		timer = setTimeout(() => { pop.textContent = t.getAttribute('data-tip'); pop.hidden = false; place(e.clientX, e.clientY); }, 350);
	});
	document.addEventListener('pointermove', (e) => { if (!pop.hidden) place(e.clientX, e.clientY); }, { passive: true });
	document.addEventListener('pointerdown', hide, true);
	addEventListener('scroll', hide, true);
})();`;

const html = `<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Foundry PDK Benchmark</title>
<meta name="description" content="Best literature-measured values of foundry photonics building blocks by foundry and platform, from the Photonics Atlas (${view.generated_on})." />
<style>
${tokens}
${base}
${css}
</style>
</head>
<body>
<div class="page">
<div class="bm" id="bm"></div>
<footer>Photonics Atlas, generated ${view.generated_on}<span>|</span><a href="https://outside5sigma.com/photonics-atlas/benchmark" target="_blank" rel="noopener">live table</a></footer>
</div>
<script id="bm-data" type="application/json">${data.replace(/</g, '\\u003c')}</script>
<script>
${render}
${tip}
const root = document.documentElement;
try { const t = localStorage.getItem('pdk-benchmark-theme'); if (t === 'light' || t === 'dark') root.dataset.theme = t; } catch {}
mountBenchmark(document.getElementById('bm'), JSON.parse(document.getElementById('bm-data').textContent), {
	title: 'Foundry PDK benchmark',
	themeToggle: true,
	onTheme: () => { const t = root.dataset.theme === 'light' ? 'dark' : 'light'; root.dataset.theme = t; try { localStorage.setItem('pdk-benchmark-theme', t); } catch {} }
});
</script>
</body>
</html>
`;
writeFileSync(join(APP, 'static/pdk-benchmark.html'), html);
console.log(`wrote static/pdk-benchmark.html (${html.length} bytes)`);
