// Serves app/build the way the deployed site does, for repeatable local timing (DevLog-012): under the base path, extension-
// less pages, gzip, max-age=600, and a fixed delay on every response standing in for the measured first-byte time.
//   node scripts/perf-serve.mjs [--port=47533] [--delay=190]
import { createServer } from 'node:http';
import { existsSync, readFileSync, statSync } from 'node:fs';
import { dirname, extname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzipSync } from 'node:zlib';

const opt = (k, d) => Number(process.argv.find((a) => a.startsWith(`--${k}=`))?.split('=')[1] ?? d);
const PORT = opt('port', 47533);
const DELAY = opt('delay', 190);
const BASE = '/photonics-atlas';
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', 'build');
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml' };
const gz = new Map();

createServer((req, res) => {
	const url = new URL(req.url, 'http://x');
	setTimeout(() => {
		if (url.pathname === BASE) {
			res.writeHead(301, { location: BASE + '/' });
			return res.end();
		}
		if (!url.pathname.startsWith(BASE + '/')) {
			res.writeHead(404);
			return res.end();
		}
		let f = join(ROOT, decodeURIComponent(url.pathname.slice(BASE.length)));
		if (url.pathname === BASE + '/') f = join(ROOT, 'index.html');
		else if (!extname(f)) f += '.html';
		if (!existsSync(f) || !statSync(f).isFile()) {
			res.writeHead(404);
			return res.end();
		}
		const key = f + statSync(f).mtimeMs;
		if (!gz.has(key)) gz.set(key, gzipSync(readFileSync(f)));
		const headers = { 'content-type': TYPES[extname(f)] ?? 'application/octet-stream', 'content-encoding': 'gzip', 'cache-control': 'max-age=600' };
		res.writeHead(200, headers);
		res.end(gz.get(key));
	}, DELAY);
}).listen(PORT, () => console.log(`http://localhost:${PORT}${BASE}/ delay ${DELAY} ms`));
