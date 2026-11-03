import { getJson } from './paths';
import type { Org, OrgEvent, Registry } from './types';

// raw state: the registry is replaced as a whole, never mutated (no deep proxies over thousands of rows)
class RegistryState {
	reg = $state.raw<Registry | null>(null);
	byId = $state.raw<Map<string, Org>>(new Map());
	evById = $state.raw<Map<string, OrgEvent>>(new Map());
	loading = $state(true);
	error = $state('');
}
export const store = new RegistryState();
export const ui = $state<{ theme: 'dark' | 'light' }>({ theme: 'dark' });

let started = false;

export async function loadRegistry(): Promise<void> {
	if (started) return;
	started = true;
	try {
		const r = await getJson<Registry>('data/registry.json');
		store.byId = new Map(r.orgs.map((o) => [o.id, o]));
		store.evById = new Map(r.events.map((e) => [e.id, e]));
		store.reg = r;
	} catch (e) {
		store.error = e instanceof Error ? e.message : String(e);
	} finally {
		store.loading = false;
	}
}

export function setTheme(t: 'dark' | 'light'): void {
	ui.theme = t;
	document.documentElement.setAttribute('data-theme', t);
	try {
		localStorage.setItem('pa-atlas-theme', t);
	} catch {
		/* storage unavailable */
	}
}
