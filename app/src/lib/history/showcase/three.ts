// One shared WebGL renderer for all 3D stories (DevLog-017 section 2: browsers cap live contexts). three.js loads
// lazily, the first time a 3D story comes near the viewport. Stories ask for the renderer with their visible share;
// the most visible one holds it: its canvas moves into that story's model pane. Pixel ratio capped at 2.
import type * as THREE_NS from 'three';

type Three = typeof THREE_NS;

let threeP: Promise<Three> | null = null;
export function loadThree(): Promise<Three> {
	return (threeP ??= import('three'));
}

type OrbitCtor = typeof import('three/examples/jsm/controls/OrbitControls.js').OrbitControls;
let orbitP: Promise<OrbitCtor> | null = null;
export function loadOrbit(): Promise<OrbitCtor> {
	return (orbitP ??= import('three/examples/jsm/controls/OrbitControls.js').then((m) => m.OrbitControls));
}

let renderer: THREE_NS.WebGLRenderer | null = null;
let env: THREE_NS.Texture | null = null;

/** The shared renderer (created on first call) and a neutral room environment map for PBR metals. */
export async function shared(): Promise<{ THREE: Three; renderer: THREE_NS.WebGLRenderer; env: THREE_NS.Texture }> {
	const THREE = await loadThree();
	if (!renderer) {
		renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
		renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
		renderer.setClearColor(0x000000, 0);
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 1;
		renderer.domElement.className = 'sc-gl';
		const { RoomEnvironment } = await import('three/examples/jsm/environments/RoomEnvironment.js');
		const pm = new THREE.PMREMGenerator(renderer);
		env = pm.fromScene(new RoomEnvironment(), 0.04).texture;
		pm.dispose();
	}
	return { THREE, renderer, env: env! };
}

export interface Claimant {
	/** called when this story receives the renderer (its canvas must be placed by the story) */
	grant(r: THREE_NS.WebGLRenderer): void;
	/** called when the story loses the renderer; `moving`: another story takes the canvas (keep a still of the last frame) */
	revoke(moving: boolean): void;
}

const claims = new Map<Claimant, number>();
let holder: Claimant | null = null;

/** Report a story's visible share (0 = off screen); the largest positive share holds the renderer. */
export function claim(c: Claimant, share: number): void {
	if (share > 0) claims.set(c, share);
	else claims.delete(c);
	arbitrate();
}

export function unclaim(c: Claimant): void {
	claims.delete(c);
	if (holder === c) holder = null;
	arbitrate();
}

function arbitrate(): void {
	if (!renderer) return;
	let best: Claimant | null = null;
	let bs = 0;
	for (const [c, s] of claims) if (s > bs) [best, bs] = [c, s];
	// hysteresis: keep the holder while it is still visible and not clearly beaten
	if (holder && claims.has(holder) && best !== holder && bs < (claims.get(holder) ?? 0) + 0.15) return;
	if (best === holder) return;
	const old = holder;
	holder = best;
	old?.revoke(!!best);
	if (best) best.grant(renderer);
}
