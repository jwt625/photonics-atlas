import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		sveltekit({
			adapter: adapter({ pages: 'build', assets: 'build', fallback: undefined, precompress: false, strict: true }),
			paths: { base: (process.env.BASE_PATH ?? '') as '' | `/${string}`, relative: false },
			// handleMissingId: `#tab=standards` and the like are client-side state, not element ids
			prerender: { handleHttpError: 'fail', handleMissingId: 'ignore' },
			// CSS in the HTML: first paint needs no second request (DevLog-012)
			inlineStyleThreshold: 64 * 1024,
			// no worker on the dev server: it would hold a shared localhost port's scope and cache data under development
			...(process.argv.includes('dev') ? { serviceWorker: { register: false } } : {})
		})
	]
});
