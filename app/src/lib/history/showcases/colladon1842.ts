// Scene module: light guided in a water jet, Colladon, Comptes rendus 1842 (spec data/history/showcases/colladon1842.yaml).
// Contract: ../showcase/types.ts. Units mm; origin = orifice centre on the vessel's outer face; +x = jet direction,
// +y = up, z across. Story per the 1842 letter: sunlight sent by a mirror through a hole in the shutter of a darkened
// room, along a blackened tube, focused by a lens in the opposite wall into the orifice (no lamp in the model).
//
// Physics: the jet path is the ideal free jet (Torricelli efflux v = (2 g h)^1/2, horizontal launch, y = x^2 / 4h),
// derived from the spec's assumed head and basin height; the jet front advances in physical time along it and drops
// follow the same ballistic path. Light: parallel outside the vessel, a converging cone in the water (apex in the
// orifice), schematic total-internal-reflection rays inside the jet (zigzag at glancing angles inside the jet radius),
// escaping where the jet meets the basin. Clear water: jet barely visible. Thin jet: drops light up, each pinch-off
// flashes. Clouded water: the upper jet glows, fading downstream. Glow strengths are illustrative (spec withheld).
// Only the vessel height is stated; every other size is assumed (spec dims) and the hover roles say so.
import type * as THREE_NS from 'three';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type V3 = [number, number, number];
type Rect = [number, number, number, number];
type Geo = Record<string, unknown>;

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const G_MM = 9810; // g in mm / s^2
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
const nums = (v: unknown, d: number[]): number[] => (Array.isArray(v) && v.length >= d.length && v.every((x) => typeof x === 'number') ? (v as number[]) : d);
const fract = (x: number) => x - Math.floor(x);
/** deterministic PRNG (mulberry32) */
function rng(seed: number) {
	let a = seed >>> 0;
	return () => {
		a = (a + 0x6d2b79f5) >>> 0;
		let t = a;
		t = Math.imul(t ^ (t >>> 15), t | 1);
		t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}

// ------------------------------------------------------------------------------------------------ camera shots
// One settled shot per phase; the camera eases from the previous shot over the first half of a phase and drifts in
// azimuth inside it. R = [half width, half height] (mm) around the target that must fit the pane region.
interface Shot {
	t: V3;
	/** optional target at the end of the phase (tracking shot) */
	t1?: V3;
	az: number;
	el: number;
	R: [number, number];
	drift: number;
}
const PHASES = ['intro', 'vessel', 'diaphragm', 'jet', 'lens', 'room', 'sun', 'focus', 'tir', 'basin', 'drops', 'clouded'] as const;
type Phase = (typeof PHASES)[number];

function regions(w: number, h: number): Rect {
	if (w < 700) return [0.04, Math.min(0.24, 170 / Math.max(1, h)), 0.96, 0.97];
	return [0.03, Math.min(0.22, 150 / Math.max(1, h)), 0.97, 0.97];
}

// ------------------------------------------------------------------------------------------------ glow shader
// Light only (physical glow): fresnel-weighted soft volume, revealed between uBack and uFront along the beam
// coordinate s (object position along uAxis, or the tube's uv.x when uMode = 1), optional decay exp(-s / uDecay).
const GLOW_VS = /* glsl */ `
uniform vec3 uAxis; uniform vec3 uOrigin; uniform float uLen; uniform float uMode;
varying vec3 vN; varying vec3 vV; varying float vS;
void main() {
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	vN = normalize(normalMatrix * normal);
	vV = normalize(-mv.xyz);
	vS = uMode > 0.5 ? uv.x : dot(position - uOrigin, uAxis) / uLen;
	gl_Position = projectionMatrix * mv;
}`;
const GLOW_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uPow; uniform float uLight;
uniform float uFront; uniform float uBack; uniform float uDecay; uniform float uTail;
varying vec3 vN; varying vec3 vV; varying float vS;
void main() {
	float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
	float a = pow(c, uPow) * uI;
	a *= smoothstep(uBack - 0.004, uBack + 0.004, vS) * (1.0 - smoothstep(uFront - 0.02, uFront, vS));
	if (uDecay > 0.0) a *= exp(-max(vS, 0.0) / uDecay);
	if (uTail > 0.0) a *= 1.0 - smoothstep(1.0 - uTail, 1.0, vS);
	a = clamp(a, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a) : vec4(uColor * a, a);
}`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('colladon1842 is a 3D scene');
		const { THREE, scene, camera, spec } = ctx;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let k = 0;
		let theme: Theme = ctx.theme;
		let hi: string[] = [];

		const partOf = (id: string) => spec.parts.find((q) => q.id === id);
		const geo = (id: string): Geo => (partOf(id)?.geometry ?? {}) as Geo;
		const look = (id: string) => partOf(id)?.look ?? {};

		// ---------------------------------------------------------------------------- phases (chapter windows)
		const chap = (id: string) => spec.chapters.find((c) => c.id === id)?.p as [number, number] | undefined;
		const fallback: Record<Phase, [number, number]> = {
			intro: [0, 0.07], vessel: [0.07, 0.16], diaphragm: [0.16, 0.24], jet: [0.24, 0.35], lens: [0.35, 0.44],
			room: [0.44, 0.52], sun: [0.52, 0.61], focus: [0.61, 0.7], tir: [0.7, 0.8], basin: [0.8, 0.87],
			drops: [0.87, 0.935], clouded: [0.935, 1]
		};
		const PH = {} as Record<Phase, [number, number]>;
		for (const id of PHASES) PH[id] = chap(id) ?? fallback[id];
		// the closing chapter "observe" holds the two observations: drops first half, clouded water second half
		const obs = chap('observe');
		if (obs && !chap('drops') && !chap('clouded')) {
			const mid = (obs[0] + obs[1]) / 2;
			PH.drops = [obs[0], mid];
			PH.clouded = [mid, obs[1]];
		}
		const cq = (id: Phase, p: number) => seg(p, PH[id][0], PH[id][1]);
		/** progress from a point (phase a, local qa) to (phase b, local qb) */
		const span = (p: number, a: Phase, qa: number, b: Phase, qb: number) =>
			seg(p, lerp(PH[a][0], PH[a][1], qa), lerp(PH[b][0], PH[b][1], qb));

		// ---------------------------------------------------------------------------- dimensions from the spec
		const vG = geo('vessel');
		const vX = nums(vG.x, [-320, 0]);
		const vY = nums(vG.y, [-110, 890]);
		const vZ = nums(vG.z, [-160, 160]);
		const wall = num(vG.wall, 10);
		const wG = geo('water');
		const wX = nums(wG.x, [-310, -10]);
		const wZ = nums(wG.z, [-150, 150]);
		const wY0 = nums(wG.y, [-100, 800])[0];
		const level = num(wG.fill_level_y, 800); // water surface height (y); orifice centre at y = 0
		const head = level; // head above the orifice centre (assumed level - orifice height, both from the spec)
		const dG = geo('diaphragm');
		const dR = num(dG.outer_diameter, 60) / 2;
		const dT = num(dG.thickness, 4);
		const apR = num(dG.aperture, 10) / 2;
		const apRs = num(dG.aperture_small, 3) / 2;
		const jetR = num(geo('jet').diameter, 2 * apR) / 2;
		const thinR = apRs; // drops chapter: the small diaphragm sets the jet size
		const lG = geo('lens');
		const lensC = nums(lG.center, [-315, 0, 0]);
		const lensR = num(lG.diameter, 80) / 2;
		const tG = geo('tube');
		const tX = nums(tG.x, [-620, -320]);
		const tRi = num(tG.inner_diameter, 80) / 2;
		const tRo = tRi + num(tG.wall, 3);
		const sG = geo('shutter');
		const sXp = num(sG.plane_x, -630);
		const sTh = num(sG.thickness, 20);
		const sY = nums(sG.y, [-610, 600]);
		const sZ = nums(sG.z, [-450, 450]);
		const sHole = num(sG.hole_diameter, 86) / 2;
		const mG = geo('mirror');
		const mC = nums(mG.center, [-900, 0, 0]);
		const mS = nums(mG.size, [200, 200]);
		const mT = num(mG.thickness, 6);
		const mN = new THREE.Vector3(...(nums(mG.normal, [0.707, 0.354, 0.612]) as V3)).normalize();
		// incoming sun direction from the law of reflection: reflected ray = +x, so d = r - 2 (r . n) n
		const rOut = new THREE.Vector3(1, 0, 0);
		const sunDir = rOut.clone().addScaledVector(mN, -2 * rOut.dot(mN)).normalize(); // travel direction of sunlight
		const toSun = sunDir.clone().negate();
		const beamR = num(geo('beam').diameter, 2 * lensR) / 2;
		const bG = geo('basin');
		const bC = nums(bG.center, [1290, -610, 0]);
		const bR = num(bG.diameter, 500) / 2;
		const bH = num(bG.height, 120);
		const bWD = num(bG.water_depth, 90);
		const ySurf = bC[1] + bWD; // basin water surface
		const stG = geo('stand');
		const stX = nums(stG.x, [-320, 0]);
		const stY = nums(stG.y, [-610, -110]);
		const stZ = nums(stG.z, [-160, 160]);
		const floorY = stY[0];

		// ---------------------------------------------------------------------------- jet path (derived, ideal free jet)
		const v0 = Math.sqrt(2 * G_MM * head); // Torricelli efflux speed, mm / s
		const tauL = Math.sqrt((2 * Math.max(1, -ySurf)) / G_MM); // flight time to the basin water
		const xL = v0 * tauL; // landing x (= (4 h y)^1/2)
		const NJ = 240;
		const jetPts: THREE_NS.Vector3[] = [];
		const cum: number[] = [0];
		for (let i = 0; i <= NJ; i++) {
			const tau = (tauL * i) / NJ;
			jetPts.push(new THREE.Vector3(v0 * tau, -0.5 * G_MM * tau * tau, 0));
			if (i > 0) cum.push(cum[i - 1] + jetPts[i].distanceTo(jetPts[i - 1]));
		}
		const jetLen = cum[NJ];
		/** arc fraction reached at flight time tau */
		const uAtTau = (tau: number) => {
			const f = clamp01(tau / tauL) * NJ;
			const i = Math.min(NJ - 1, Math.floor(f));
			return lerp(cum[i], cum[i + 1], f - i) / jetLen;
		};
		/** flight time at arc fraction u */
		const tauAtU = (u: number) => {
			const s = clamp01(u) * jetLen;
			let i = 0;
			while (i < NJ - 1 && cum[i + 1] < s) i++;
			return (tauL * (i + (s - cum[i]) / Math.max(1e-9, cum[i + 1] - cum[i]))) / NJ;
		};
		const pathAt = (tau: number, out = new THREE.Vector3()) => out.set(v0 * tau, -0.5 * G_MM * tau * tau, 0);
		const jetAtU = (u: number) => pathAt(tauAtU(u));
		const breakU = clamp01(num(geo('drops').from_fraction, 0.5));
		const tauB = tauAtU(breakU);

		// ---------------------------------------------------------------------------- scene bookkeeping
		const disposables: { dispose(): void }[] = [];
		const keep = <T extends { dispose(): void }>(x: T): T => (disposables.push(x), x);
		const G = <T extends THREE_NS.BufferGeometry>(g: T): T => keep(g);
		const root = new THREE.Group();
		scene.add(root);
		const nopick = <T extends THREE_NS.Object3D>(o: T): T => ((o.userData.nopick = true), o);

		/** polyline curve (linear between points): sharp corners for the reflected rays, exact path for proxies */
		class Poly extends THREE.Curve<THREE_NS.Vector3> {
			pts: THREE_NS.Vector3[];
			constructor(pts: THREE_NS.Vector3[]) {
				super();
				this.pts = pts;
				this.arcLengthDivisions = Math.max(200, pts.length * 2);
			}
			getPoint(t: number, target = new THREE.Vector3()) {
				const f = clamp01(t) * (this.pts.length - 1);
				const i = Math.min(this.pts.length - 2, Math.floor(f));
				return target.copy(this.pts[i]).lerp(this.pts[i + 1], f - i);
			}
		}
		const jetCurve = new Poly(jetPts);

		interface Body {
			id: string;
			obj: THREE_NS.Object3D;
			mats: { m: THREE_NS.MeshStandardMaterial; base: number; trans: boolean }[];
			picks: THREE_NS.Mesh[];
			o: number;
		}
		const bodies = new Map<string, Body>();
		function body(id: string, obj: THREE_NS.Object3D): Body {
			const b: Body = { id, obj, mats: [], picks: [], o: 1 };
			obj.traverse((n) => {
				const m = (n as THREE_NS.Mesh).material as THREE_NS.MeshStandardMaterial | undefined;
				if ((n as THREE_NS.Mesh).isMesh && m && 'emissive' in m && !b.mats.some((x) => x.m === m)) b.mats.push({ m, base: m.opacity, trans: m.transparent });
				if ((n as THREE_NS.Mesh).isMesh && !n.userData.nopick) {
					n.userData.part = id;
					b.picks.push(n as THREE_NS.Mesh);
				}
			});
			root.add(obj);
			bodies.set(id, b);
			return b;
		}
		/** physical materials whose environment reflection follows the room light (all but the sunlit mirror) */
		const roomLit: { m: THREE_NS.MeshPhysicalMaterial; env: number }[] = [];
		const std = (id: string, extra: Partial<THREE_NS.MeshPhysicalMaterialParameters> = {}, lit = true) => {
			const lk = look(id);
			const op = num(lk.opacity, 1);
			const m = keep(
				new THREE.MeshPhysicalMaterial({
					color: lk.color || '#888888',
					metalness: num(lk.metal, 0),
					roughness: num(lk.rough, 0.5),
					transparent: op < 1,
					opacity: op,
					depthWrite: op >= 1,
					// explicit envMap (the shared scene environment, never disposed here): with scene.environment alone
					// three.js ignores envMapIntensity, which the dark room needs
					envMap: scene.environment ?? null,
					...extra
				})
			);
			if (lit) roomLit.push({ m, env: m.envMapIntensity });
			return m;
		};
		const glows: { m: THREE_NS.ShaderMaterial; dark: string; light: string }[] = [];
		const glow = (dark: string, light: string, pow: number, axis: V3 = [1, 0, 0], origin: V3 = [0, 0, 0], len = 1, mode = 0) => {
			const m = keep(
				new THREE.ShaderMaterial({
					uniforms: {
						uColor: { value: new THREE.Color(dark) },
						uI: { value: 0 },
						uPow: { value: pow },
						uLight: { value: 0 },
						uFront: { value: 1.1 },
						uBack: { value: -0.1 },
						uDecay: { value: 0 },
						uTail: { value: 0 },
						uAxis: { value: new THREE.Vector3(...axis) },
						uOrigin: { value: new THREE.Vector3(...origin) },
						uLen: { value: len },
						uMode: { value: mode }
					},
					vertexShader: GLOW_VS,
					fragmentShader: GLOW_FS,
					transparent: true,
					depthWrite: false,
					side: THREE.DoubleSide,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
			glows.push({ m, dark, light });
			return m;
		};
		const radialTex = (stops: [number, string][]) => {
			const cv = document.createElement('canvas');
			cv.width = cv.height = 128;
			const g = cv.getContext('2d')!;
			const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
			for (const [o, c] of stops) gr.addColorStop(o, c);
			g.fillStyle = gr;
			g.fillRect(0, 0, 128, 128);
			const t = new THREE.CanvasTexture(cv);
			t.colorSpace = THREE.SRGBColorSpace;
			return keep(t);
		};
		const softTex = radialTex([[0, 'rgba(255,255,255,1)'], [0.25, 'rgba(255,255,255,0.55)'], [0.6, 'rgba(255,255,255,0.12)'], [1, 'rgba(255,255,255,0)']]);
		const flareTex = radialTex([[0, 'rgba(255,255,255,1)'], [0.1, 'rgba(255,255,255,0.85)'], [0.3, 'rgba(255,255,255,0.25)'], [1, 'rgba(255,255,255,0)']]);
		const sprites: { m: THREE_NS.SpriteMaterial | THREE_NS.MeshBasicMaterial; dark: string; light: string }[] = [];
		const spriteMat = (dark: string, light: string, tex = flareTex) => {
			const m = keep(new THREE.SpriteMaterial({ map: tex, color: dark, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, opacity: 0 }));
			sprites.push({ m, dark, light });
			return m;
		};
		const WARM_D = '#fff1c8';
		const WARM_L = '#c98612';

		// ---------------------------------------------------------------------------- vessel (open box, translucent)
		const vW = vX[1] - vX[0];
		const vH = vY[1] - vY[0];
		const vD = vZ[1] - vZ[0];
		const vc: V3 = [(vX[0] + vX[1]) / 2, (vY[0] + vY[1]) / 2, (vZ[0] + vZ[1]) / 2];
		const glassMat = std('vessel', { side: THREE.FrontSide, envMapIntensity: 0.5 });
		const vesselGroup = new THREE.Group();
		const slab = (sx: number, sy: number, sz: number, x: number, y: number, z: number) => {
			const m = new THREE.Mesh(G(new THREE.BoxGeometry(sx, sy, sz)), glassMat);
			m.position.set(x, y, z);
			m.userData.nopick = true; // the walls are picked by their edges (the water inside is picked through them)
			m.renderOrder = 1;
			vesselGroup.add(m);
		};
		slab(vW, wall, vD, vc[0], vY[0] + wall / 2, vc[2]); // bottom
		slab(wall, vH, vD, vX[0] + wall / 2, vc[1], vc[2]); // lens wall (-x)
		slab(wall, vH, vD, vX[1] - wall / 2, vc[1], vc[2]); // orifice wall (+x)
		slab(vW - 2 * wall, vH, wall, vc[0], vc[1], vZ[0] + wall / 2);
		slab(vW - 2 * wall, vH, wall, vc[0], vc[1], vZ[1] - wall / 2);
		const edgeMat = keep(new THREE.LineBasicMaterial({ color: '#9aa3ad', transparent: true, opacity: 0.9 }));
		const outerBox = G(new THREE.BoxGeometry(vW, vH, vD));
		const vEdges = nopick(new THREE.LineSegments(G(new THREE.EdgesGeometry(outerBox)), edgeMat));
		vEdges.position.set(...vc);
		vesselGroup.add(vEdges);
		// pick proxies along the 12 edges
		const proxyMat = keep(new THREE.MeshBasicMaterial({ visible: false }));
		const ET = 26;
		for (const [sx, sy, sz, dx, dy, dz] of [
			[vW, ET, ET, 0, 1, 1], [vW, ET, ET, 0, 1, -1], [vW, ET, ET, 0, -1, 1], [vW, ET, ET, 0, -1, -1],
			[ET, vH, ET, 1, 0, 1], [ET, vH, ET, 1, 0, -1], [ET, vH, ET, -1, 0, 1], [ET, vH, ET, -1, 0, -1],
			[ET, ET, vD, 1, 1, 0], [ET, ET, vD, 1, -1, 0], [ET, ET, vD, -1, 1, 0], [ET, ET, vD, -1, -1, 0]
		] as number[][]) {
			const m = new THREE.Mesh(G(new THREE.BoxGeometry(sx, sy, sz)), proxyMat);
			m.position.set(vc[0] + (dx * vW) / 2, vc[1] + (dy * vH) / 2, vc[2] + (dz * vD) / 2);
			vesselGroup.add(m);
		}
		const vessel = body('vessel', vesselGroup);

		// ---------------------------------------------------------------------------- water (rises to the assumed level)
		const waterMat = std('water', { side: THREE.FrontSide });
		const waterBase = new THREE.Color(look('water').color || '#bcd9f0');
		const milky = new THREE.Color('#eef2f4');
		const waterLight = new THREE.Color('#8fb3d0');
		const waterGeo = G(new THREE.BoxGeometry(1, 1, 1).translate(0, 0.5, 0));
		const waterMesh = new THREE.Mesh(waterGeo, waterMat);
		waterMesh.renderOrder = 2;
		const waterGroup = new THREE.Group();
		waterGroup.add(waterMesh);
		const water = body('water', waterGroup);

		// ---------------------------------------------------------------------------- stand (plain block, stand-in)
		const standGeo = G(new THREE.BoxGeometry(stX[1] - stX[0], stY[1] - stY[0], stZ[1] - stZ[0]));
		const standGroup = new THREE.Group();
		const standMesh = new THREE.Mesh(standGeo, std('stand'));
		standMesh.position.set((stX[0] + stX[1]) / 2, (stY[0] + stY[1]) / 2, (stZ[0] + stZ[1]) / 2);
		const standEdgeMat = keep(new THREE.LineBasicMaterial({ color: '#55595f', transparent: true, opacity: 1 }));
		const standEdges = nopick(new THREE.LineSegments(G(new THREE.EdgesGeometry(standGeo)), standEdgeMat));
		standEdges.position.copy(standMesh.position);
		standGroup.add(standMesh, standEdges);
		const stand = body('stand', standGroup);

		// ---------------------------------------------------------------------------- diaphragm (two plates: 10 / 3 mm)
		const plateGeo = (r: number) => {
			const sh = new THREE.Shape().absarc(0, 0, dR, 0, TAU, false);
			sh.holes.push(new THREE.Path().absarc(0, 0, r, 0, TAU, true));
			return G(new THREE.ExtrudeGeometry(sh, { depth: dT, bevelEnabled: false, curveSegments: 64 }).rotateY(Math.PI / 2));
		};
		const diaMatA = std('diaphragm');
		const diaMatB = std('diaphragm');
		const diaBig = new THREE.Mesh(plateGeo(apR), diaMatA);
		const diaSmall = new THREE.Mesh(plateGeo(apRs), diaMatB);
		const diaGroup = new THREE.Group();
		diaGroup.add(diaBig, diaSmall);
		const dia = body('diaphragm', diaGroup);
		const diaBase = diaMatA.opacity;

		// ---------------------------------------------------------------------------- jet (thick + thin tubes)
		const JT = 320;
		const JRAD = 18;
		const jetGeo = G(new THREE.TubeGeometry(jetCurve, JT, jetR, JRAD, false));
		const thinGeo = G(new THREE.TubeGeometry(jetCurve, JT, thinR, 10, false));
		const jetMat = std('jet', { side: THREE.FrontSide, clearcoat: 1, clearcoatRoughness: 0.05 });
		const thinMat = std('jet', { side: THREE.FrontSide, clearcoat: 1, clearcoatRoughness: 0.05 });
		const jetBase = jetMat.opacity;
		const jetColor = look('jet').color || '#d6ecff';
		const jetMesh = nopick(new THREE.Mesh(jetGeo, jetMat));
		const thinMesh = nopick(new THREE.Mesh(thinGeo, thinMat));
		jetMesh.renderOrder = 4;
		thinMesh.renderOrder = 4;
		const jetProxy = new THREE.Mesh(G(new THREE.TubeGeometry(jetCurve, 120, 26, 8, false)), proxyMat);
		const jetGroup = new THREE.Group();
		jetGroup.add(jetMesh, thinMesh, jetProxy);
		const jet = body('jet', jetGroup);

		// ---------------------------------------------------------------------------- basin (plain dish) + its water
		const bWall = 6;
		const basinGeo = G(
			new THREE.LatheGeometry(
				[new THREE.Vector2(0.01, 0), new THREE.Vector2(bR, 0), new THREE.Vector2(bR, bH), new THREE.Vector2(bR - bWall, bH), new THREE.Vector2(bR - bWall, bWall), new THREE.Vector2(0.01, bWall)],
				96
			)
		);
		const basinGroup = new THREE.Group();
		const basinMesh = new THREE.Mesh(basinGeo, std('basin', { side: THREE.DoubleSide }));
		const bWaterMat = std('water', { side: THREE.DoubleSide, depthWrite: false });
		const bWater = nopick(new THREE.Mesh(G(new THREE.CircleGeometry(bR - bWall, 64).rotateX(-Math.PI / 2)), bWaterMat));
		bWater.position.y = bWD;
		bWater.renderOrder = 3;
		basinGroup.add(basinMesh, bWater);
		const basin = body('basin', basinGroup);
		const basinAt: V3 = [xL, bC[1], bC[2]]; // centred where the derived jet lands (spec: placed where the jet lands)

		// ---------------------------------------------------------------------------- lens (biconvex, assumed thickness)
		const lensT = 14; // centre thickness, illustrative (not stated)
		const prof: THREE_NS.Vector2[] = [];
		for (let i = 0; i <= 24; i++) {
			const r = (lensR * i) / 24;
			prof.push(new THREE.Vector2(Math.max(0.01, r), -(1.5 + (lensT / 2 - 1.5) * (1 - (r / lensR) ** 2))));
		}
		for (let i = 24; i >= 0; i--) {
			const r = (lensR * i) / 24;
			prof.push(new THREE.Vector2(Math.max(0.01, r), 1.5 + (lensT / 2 - 1.5) * (1 - (r / lensR) ** 2)));
		}
		const lensGeo = G(new THREE.LatheGeometry(prof, 72).rotateZ(Math.PI / 2));
		const lensMat = std('lens', { side: THREE.FrontSide, clearcoat: 1, clearcoatRoughness: 0.03, ior: 1.5, envMapIntensity: 0.7 });
		const lensGroup = new THREE.Group();
		const lensMesh = new THREE.Mesh(lensGeo, lensMat);
		lensMesh.renderOrder = 3;
		const lensEdgeMat = keep(new THREE.LineBasicMaterial({ color: '#cfe4f5', transparent: true, opacity: 0.8 }));
		const lensRim = nopick(new THREE.LineLoop(G(new THREE.BufferGeometry().setFromPoints(Array.from({ length: 73 }, (_, i) => new THREE.Vector3(0, lensR * Math.cos((i / 72) * TAU), lensR * Math.sin((i / 72) * TAU))))), lensEdgeMat));
		lensGroup.add(lensMesh, lensRim);
		const lens = body('lens', lensGroup);

		// ---------------------------------------------------------------------------- blackened tube
		const tLen = tX[1] - tX[0];
		const tubeMat = std('tube', { side: THREE.DoubleSide });
		const tubeGroup = new THREE.Group();
		const tOuter = new THREE.Mesh(G(new THREE.CylinderGeometry(tRo, tRo, tLen, 64, 1, true).rotateZ(Math.PI / 2)), tubeMat);
		const innerMat = keep(new THREE.MeshStandardMaterial({ color: '#050505', roughness: 1, metalness: 0, side: THREE.BackSide, transparent: true }));
		const tInner = new THREE.Mesh(G(new THREE.CylinderGeometry(tRi, tRi, tLen, 64, 1, true).rotateZ(Math.PI / 2)), innerMat);
		const ringGeo = G(new THREE.RingGeometry(tRi, tRo, 64).rotateY(Math.PI / 2));
		const ringA = new THREE.Mesh(ringGeo, tubeMat);
		ringA.position.x = -tLen / 2;
		const ringB = new THREE.Mesh(ringGeo, tubeMat);
		ringB.position.x = tLen / 2;
		tubeGroup.add(tOuter, tInner, ringA, ringB);
		const tube = body('tube', tubeGroup);
		const tubeC: V3 = [(tX[0] + tX[1]) / 2, 0, 0];

		// ---------------------------------------------------------------------------- shutter (plain panel with a hole)
		const shShape = new THREE.Shape();
		shShape.moveTo(sZ[0], sY[0]).lineTo(sZ[1], sY[0]).lineTo(sZ[1], sY[1]).lineTo(sZ[0], sY[1]).lineTo(sZ[0], sY[0]);
		shShape.holes.push(new THREE.Path().absarc(0, 0, sHole, 0, TAU, true));
		const shGeo = G(new THREE.ExtrudeGeometry(shShape, { depth: sTh, bevelEnabled: false, curveSegments: 48 }).rotateY(Math.PI / 2).translate(-sTh / 2, 0, 0));
		const shGroup = new THREE.Group();
		const shMesh = new THREE.Mesh(shGeo, std('shutter'));
		const shEdgeMat = keep(new THREE.LineBasicMaterial({ color: '#5d5853', transparent: true, opacity: 1 }));
		const shEdges = nopick(new THREE.LineSegments(G(new THREE.EdgesGeometry(shGeo, 30)), shEdgeMat));
		shGroup.add(shMesh, shEdges);
		const shutter = body('shutter', shGroup);
		const shutterAt: V3 = [sXp, 0, 0];

		// ---------------------------------------------------------------------------- mirror (plain plate, sunlit)
		const mirrorMat = std('mirror', { envMap: null }, false); // sunlit outside: shared environment at full strength
		const mirrorGroup = new THREE.Group();
		const mirrorMesh = new THREE.Mesh(G(new THREE.BoxGeometry(mS[0], mS[1], mT)), mirrorMat);
		mirrorGroup.add(mirrorMesh);
		const mirror = body('mirror', mirrorGroup);
		const mirrorAt: V3 = [mC[0], mC[1], mC[2]];

		// ---------------------------------------------------------------------------- beam: sunlight in, parallel beam, cone
		const SUN_L = 760; // drawn length of the incoming sunlight (illustrative)
		const sunGeo = G(new THREE.CylinderGeometry(beamR, beamR, 1, 40, 1, true).translate(0, 0.5, 0));
		const sunMat = glow('#fff4d6', WARM_L, 1.4, [0, 1, 0], [0, 0, 0], 1);
		sunMat.uniforms.uTail.value = 0.45; // sunlight arrives from far away: the drawn length fades out
		const sunMesh = nopick(new THREE.Mesh(sunGeo, sunMat));
		sunMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), toSun);
		sunMesh.renderOrder = 6;
		const parL = lensC[0] - mC[0];
		const parGeo = G(new THREE.CylinderGeometry(beamR, beamR, 1, 40, 1, true).rotateZ(-Math.PI / 2).translate(0.5, 0, 0));
		const parMat = glow('#fff4d6', WARM_L, 1.4, [1, 0, 0], [0, 0, 0], 1);
		const parMesh = nopick(new THREE.Mesh(parGeo, parMat));
		parMesh.renderOrder = 6;
		const coneL = -lensC[0];
		const coneGeo = G(new THREE.ConeGeometry(beamR, coneL, 64, 1, true).rotateZ(-Math.PI / 2).translate(lensC[0] + coneL / 2, 0, 0));
		const coneMat = glow('#fff4d6', WARM_L, 0.7, [1, 0, 0], [lensC[0], 0, 0], coneL);
		const coneMesh = nopick(new THREE.Mesh(coneGeo, coneMat));
		coneMesh.renderOrder = 6;
		// pick proxies for the light (only while lit)
		const sunProxy = new THREE.Mesh(sunGeo, proxyMat);
		sunProxy.quaternion.copy(sunMesh.quaternion);
		const parProxy = new THREE.Mesh(parGeo, proxyMat);
		const coneProxy = new THREE.Mesh(coneGeo, proxyMat);
		const spotMat = spriteMat(WARM_D, WARM_L); // focus in the orifice
		const spot = nopick(new THREE.Sprite(spotMat));
		spot.position.set(0.5, 0, 0);
		spot.renderOrder = 9;
		const mirrorFlashMat = spriteMat(WARM_D, WARM_L);
		const mirrorFlash = nopick(new THREE.Sprite(mirrorFlashMat));
		mirrorFlash.position.set(mC[0], mC[1], mC[2]);
		mirrorFlash.renderOrder = 9;
		const beamGroup = new THREE.Group();
		beamGroup.add(sunMesh, parMesh, coneMesh, sunProxy, parProxy, coneProxy, spot, mirrorFlash);
		const beam = body('beam', beamGroup);

		// ---------------------------------------------------------------------------- guided light: schematic TIR rays
		// Each ray leaves the focus on the axis and zigzags between the jet walls at a glancing angle theta (wall to wall
		// every 2 a / tan(theta)), in a plane through the jet axis at angle psi; angles below the lens cone half-angle.
		const coneHalf = Math.atan(beamR / coneL);
		const RAYS: { th: number; psi: number }[] = [
			{ th: coneHalf * 0.95, psi: 0 },
			{ th: coneHalf * 0.68, psi: 62 * DEG },
			{ th: coneHalf * 0.45, psi: 118 * DEG }
		];
		const rayA = jetR * 0.84;
		const rayMat = keep(new THREE.MeshBasicMaterial({ color: '#fff6dc', transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
		const RAY_SEG = 1400;
		const RAY_RAD = 5;
		const rayGeos: THREE_NS.TubeGeometry[] = [];
		const tg = new THREE.Vector3();
		const nrm = new THREE.Vector3();
		const zAx = new THREE.Vector3(0, 0, 1);
		for (const r of RAYS) {
			const period = (4 * rayA) / Math.tan(r.th);
			const pts: THREE_NS.Vector3[] = [];
			const N = 900;
			for (let i = 0; i <= N; i++) {
				const u = i / N;
				const tau = tauAtU(u);
				const c = pathAt(tau);
				tg.set(v0, -G_MM * tau, 0).normalize();
				nrm.set(-tg.y, tg.x, 0);
				const off = rayA * (2 / Math.PI) * Math.asin(Math.sin((TAU * u * jetLen) / period));
				c.addScaledVector(nrm, off * Math.cos(r.psi)).addScaledVector(zAx, off * Math.sin(r.psi));
				pts.push(c);
			}
			rayGeos.push(G(new THREE.TubeGeometry(new Poly(pts), RAY_SEG, 0.65, RAY_RAD, false)));
		}
		const rayGroup = new THREE.Group();
		for (const g of rayGeos) {
			const m = nopick(new THREE.Mesh(g, rayMat));
			m.renderOrder = 7;
			rayGroup.add(m);
		}
		const rayProxy = new THREE.Mesh(G(new THREE.TubeGeometry(jetCurve, 120, 12, 8, false)), proxyMat);
		rayGroup.add(rayProxy);
		const guided = body('guided_light', rayGroup);

		// ---------------------------------------------------------------------------- escaped light (basin floor glow)
		const floorGlowMat = keep(new THREE.MeshBasicMaterial({ map: softTex, color: WARM_D, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
		sprites.push({ m: floorGlowMat, dark: WARM_D, light: WARM_L });
		const floorGlow = new THREE.Mesh(G(new THREE.CircleGeometry(1, 64).rotateX(-Math.PI / 2)), floorGlowMat);
		floorGlow.position.set(0, bWall + 0.8, 0);
		floorGlow.renderOrder = 5;
		const contactMat = spriteMat(WARM_D, WARM_L);
		const contact = nopick(new THREE.Sprite(contactMat));
		contact.position.set(0, bWD + 2, 0);
		contact.renderOrder = 9;
		const escGroup = new THREE.Group();
		escGroup.add(floorGlow, contact);
		const escaped = body('escaped_light', escGroup);
		const basinLight = new THREE.PointLight('#ffe9c0', 0, 700, 1.8);
		root.add(basinLight);

		// ---------------------------------------------------------------------------- drops (seeded) + rupture flash
		const ND = 34;
		const rand = rng(1842);
		const dropSeeds = Array.from({ length: ND }, () => ({ j: rand(), s: 0.85 + 0.3 * rand(), dy: (rand() - 0.5) * 1.2, dz: (rand() - 0.5) * 1.6 }));
		const dropR = 1.89 * thinR; // Rayleigh break-up: drop diameter about 1.9 jet diameters (illustrative)
		const dropMat = keep(new THREE.MeshBasicMaterial({ color: '#ffffff', transparent: true, opacity: 1, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false }));
		const dropMesh = nopick(new THREE.InstancedMesh(G(new THREE.SphereGeometry(1, 14, 10)), dropMat, ND));
		dropMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
		dropMesh.frustumCulled = false;
		dropMesh.renderOrder = 8;
		const ruptMat = spriteMat(WARM_D, WARM_L);
		const rupt = nopick(new THREE.Sprite(ruptMat));
		rupt.renderOrder = 9;
		const lowerPts = jetPts.filter((_, i) => i / NJ >= tauB / tauL - 1e-9);
		const dropProxy = new THREE.Mesh(G(new THREE.TubeGeometry(new Poly(lowerPts.length > 1 ? lowerPts : jetPts), 80, 22, 8, false)), proxyMat);
		const dropGroup = new THREE.Group();
		dropGroup.add(dropMesh, rupt, dropProxy);
		const drops = body('drops', dropGroup);
		const dropCol = new THREE.Color();
		for (let i = 0; i < ND; i++) dropMesh.setColorAt(i, dropCol.set('#ffffff')); // instance colours exist before first use
		const dm = new THREE.Matrix4();
		const dq = new THREE.Quaternion();
		const dsv = new THREE.Vector3();
		const dpv = new THREE.Vector3();

		// ---------------------------------------------------------------------------- clouded water: scatter glow
		const scatGeo = G(new THREE.TubeGeometry(jetCurve, JT, jetR * 1.9, 16, false));
		const scatMat = glow('#fff1c8', WARM_L, 0.6, [1, 0, 0], [0, 0, 0], 1, 1);
		scatMat.uniforms.uDecay.value = 0.16;
		const scatMesh = nopick(new THREE.Mesh(scatGeo, scatMat));
		scatMesh.renderOrder = 7;
		const upperPts = jetPts.filter((_, i) => i <= NJ * 0.4);
		const scatProxy = new THREE.Mesh(G(new THREE.TubeGeometry(new Poly(upperPts), 60, 20, 8, false)), proxyMat);
		const scatGroup = new THREE.Group();
		scatGroup.add(scatMesh, scatProxy);
		const scatter = body('scatter', scatGroup);
		// clouded water inside the vessel: a soft glow along the cone (the scattered beam becomes visible)
		const vesselScatMat = glow('#fff1c8', WARM_L, 0.5, [1, 0, 0], [lensC[0], 0, 0], coneL);
		const vesselScat = nopick(new THREE.Mesh(G(new THREE.ConeGeometry(beamR * 1.25, coneL, 48, 1, true).rotateZ(-Math.PI / 2).translate(lensC[0] + coneL / 2, 0, 0)), vesselScatMat));
		vesselScat.renderOrder = 6;
		scatGroup.add(vesselScat);

		// ---------------------------------------------------------------------------- lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.9);
		const key = new THREE.DirectionalLight('#fff3e6', 2.2);
		key.position.set(900, 1600, 1500);
		const fill = new THREE.DirectionalLight('#dfe8ff', 0.8);
		fill.position.set(-1500, 500, 900);
		root.add(hemi, key, fill);

		// ---------------------------------------------------------------------------- state helpers
		const raycaster = new THREE.Raycaster();
		const v2 = new THREE.Vector2();
		const tmp = new THREE.Vector3();
		const tmp2 = new THREE.Vector3();
		const accent = new THREE.Color();
		const black = new THREE.Color(0, 0, 0);
		const mix3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
		const add3 = (a: V3, b: V3): V3 => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
		const sc3 = (a: V3, s: number): V3 => [a[0] * s, a[1] * s, a[2] * s];

		function setOpacity(b: Body, o: number) {
			const lit = hi.includes(b.id);
			const eff = lit && o > 0.004 && o < 0.3 ? 0.3 : o;
			b.o = o;
			b.obj.visible = eff > 0.004;
			for (const x of b.mats) {
				const op = x.base * eff;
				const trans = x.trans || op < 0.999;
				if (x.m.transparent !== trans) {
					x.m.transparent = trans;
					x.m.needsUpdate = true;
				}
				x.m.depthWrite = !trans;
				x.m.opacity = op;
			}
		}
		function tint(b: Body) {
			const lit = hi.includes(b.id);
			for (const x of b.mats) {
				x.m.emissive.copy(lit ? accent : black);
				x.m.emissiveIntensity = lit ? 0.35 : 1;
			}
		}

		// ---------------------------------------------------------------------------- camera
		const jp = (u: number): V3 => {
			const v = jetAtU(u);
			return [v.x, v.y, v.z];
		};
		const SHOTS: Record<Phase, Shot> = {
			intro: { t: [(mC[0] + xL + bR) / 2, (floorY + vY[1]) / 2, 0], az: 8, el: 12, R: [(xL + bR - mC[0]) / 2 + 60, (vY[1] - floorY) / 2 + 60], drift: 16 },
			vessel: { t: [vc[0], (floorY + vY[1]) / 2, 0], az: 30, el: 13, R: [430, (vY[1] - floorY) / 2 + 40], drift: 8 },
			diaphragm: { t: [0, 0, 0], az: 68, el: 9, R: [140, 100], drift: 10 },
			jet: { t: [(vX[0] + xL + bR) / 2, (floorY + vY[1]) / 2 - 80, 0], az: 12, el: 9, R: [(xL + bR - vX[0]) / 2 + 40, (vY[1] - floorY) / 2 - 20], drift: 6 },
			lens: { t: [(tX[0] + vX[1]) / 2, 0, 0], az: -40, el: 15, R: [440, 250], drift: 10 },
			room: { t: [(sXp + vX[1]) / 2 + 40, (sY[0] + sY[1]) / 2, 0], az: 36, el: 12, R: [520, (sY[1] - sY[0]) / 2 + 40], drift: 6 },
			sun: { t: [(mC[0] + sXp) / 2 - 40, 150, 0], az: -32, el: 16, R: [440, 420], drift: 6 },
			focus: { t: [lensC[0] / 2 + 10, 0, 0], az: 26, el: 11, R: [300, 170], drift: 6 },
			tir: { t: jp(0.06), t1: jp(0.5), az: 6, el: 6, R: [330, 190], drift: 4 },
			basin: { t: [xL - 180, ySurf + 60, 0], az: 12, el: 22, R: [560, 320], drift: 6 },
			drops: { t: jp(0.72), az: 8, el: 8, R: [420, 260], drift: 4 },
			clouded: { t: [200, -20, 0], az: 14, el: 10, R: [540, 310], drift: 6 }
		};
		// explode slider: a wide shot over the exploded line-up (mirror pulled furthest out)
		const xMin = mC[0] - 380 - mS[0] / 2;
		const xMax = xL + bR;
		const EXPL: Shot = { t: [(xMin + xMax) / 2, (floorY + vY[1]) / 2, 0], az: 10, el: 12, R: [(xMax - xMin) / 2 + 60, (vY[1] - floorY) / 2 + 60], drift: 0 };
		let curShot: Shot = SHOTS.intro;
		function shotAt(p: number): Shot {
			const kx = ease(clamp01(k));
			let i = 0;
			for (let j = 0; j < PHASES.length; j++) if (p >= PH[PHASES[j]][0]) i = j;
			const id = PHASES[i];
			const q = cq(id, p);
			const cur = SHOTS[id];
			const prev = i > 0 ? SHOTS[PHASES[i - 1]] : null;
			const t = prev ? ease(seg(q, 0, 0.5)) : 1;
			const curT = cur.t1 ? mix3(cur.t, cur.t1, ease(q)) : cur.t;
			const prevT = prev ? (prev.t1 ?? prev.t) : curT;
			const curAz = cur.az + cur.drift * (q - 0.5);
			const prevAz = prev ? prev.az + prev.drift * 0.5 : curAz;
			const s: Shot = {
				t: mix3(prev ? mix3(prevT, curT, t) : curT, EXPL.t, kx),
				az: lerp(lerp(prevAz, curAz, t), EXPL.az, kx),
				el: lerp(lerp(prev?.el ?? cur.el, cur.el, t), EXPL.el, kx),
				R: [lerp(lerp(prev?.R[0] ?? cur.R[0], cur.R[0], t), EXPL.R[0], kx), lerp(lerp(prev?.R[1] ?? cur.R[1], cur.R[1], t), EXPL.R[1], kx)],
				drift: 0
			};
			return s;
		}
		function applyCamera(s: Shot) {
			const [x0, y0, x1, y1] = regions(w, h);
			const tf = Math.tan((camera.fov * DEG) / 2);
			const d = Math.max(s.R[0] / (tf * (w / h) * (x1 - x0)), s.R[1] / (tf * (y1 - y0)));
			const az = s.az * DEG;
			const el = s.el * DEG;
			camera.near = Math.max(1, d / 50);
			camera.far = d * 6 + 6000;
			camera.updateProjectionMatrix();
			camera.position.set(s.t[0] + d * Math.cos(el) * Math.sin(az), s.t[1] + d * Math.sin(el), s.t[2] + d * Math.cos(el) * Math.cos(az));
			camera.lookAt(s.t[0], s.t[1], s.t[2]);
			camera.setViewOffset(w, h, (0.5 - (x0 + x1) / 2) * w, (0.5 - (y0 + y1) / 2) * h, w, h);
			camera.updateMatrixWorld();
		}

		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			for (const g of glows) {
				g.m.uniforms.uColor.value.set(light ? g.light : g.dark);
				g.m.uniforms.uLight.value = light ? 1 : 0;
				g.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			for (const s of sprites) {
				s.m.color.set(light ? s.light : s.dark);
				s.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			for (const m of [rayMat, dropMat]) m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			rayMat.color.set(light ? '#b8740a' : '#fff6dc');
			edgeMat.color.set(light ? '#5f6a76' : '#9aa3ad');
			standEdgeMat.color.set(light ? '#7d8288' : '#55595f');
			shEdgeMat.color.set(light ? '#8a847d' : '#5d5853');
			lensEdgeMat.color.set(light ? '#5d84a8' : '#cfe4f5');
			// light page: the pale water colour vanishes on it; a blue-grey body still reads as water (no glow)
			for (const m of [jetMat, thinMat]) m.color.set(light ? '#3f6d93' : jetColor);
		}
		applyTheme();

		// intro: every hardware part floats in as a ghost from a seeded offset and settles at its place (the vessel
		// hovers above the stand and lowers in its own chapter); E = explode slider offsets after assembly
		const ir = rng(7);
		const IOFF: Record<string, V3> = {};
		for (const id of ['vessel', 'stand', 'diaphragm', 'jet', 'basin', 'lens', 'tube', 'shutter', 'mirror']) IOFF[id] = [(ir() - 0.5) * 360, (ir() - 0.3) * 300, (ir() - 0.5) * 500];
		const E: Record<string, V3> = { mirror: [-380, 120, 0], shutter: [-240, 0, 0], tube: [-140, 0, 0], lens: [-60, 0, 0], diaphragm: [70, 0, 0] };
		const VESSEL_LIFT = 320;

		// ---------------------------------------------------------------------------- frame
		function frame(p: number) {
			const kk = clamp01(k);
			curShot = shotAt(p);
			applyCamera(curShot);
			const introQ = cq('intro', p);
			const settle = ease(seg(introQ, 0.05, 0.9));
			const leave = ease(seg(cq('vessel', p), 0, 0.3)); // ghosts other than vessel / stand leave
			const ghostIn = (d: number) => 0.32 * easeOut(seg(introQ, d, d + 0.45));

			/** hardware part: intro ghost, leaves, then arrives in its own phase from offset `from` */
			function staged(b: Body, own: Phase, a0: number, a1: number, home: V3, from: V3, spin: V3, delay: number, extra?: (q: number) => V3) {
				let pos: V3;
				let rot: V3 = [0, 0, 0];
				let o: number;
				if (p < PH[own][0]) {
					pos = add3(home, sc3(IOFF[b.id], 1 - settle));
					o = ghostIn(delay) * (1 - leave);
				} else {
					const q = cq(own, p);
					const arr = ease(seg(q, a0, a1));
					pos = add3(home, sc3(from, 1 - arr));
					if (extra) pos = add3(pos, extra(q));
					rot = sc3(spin, 1 - arr);
					o = easeOut(seg(q, a0, a0 + (a1 - a0) * 0.45));
				}
				if (kk > 0 && E[b.id]) pos = add3(pos, sc3(E[b.id], ease(kk)));
				b.obj.position.set(pos[0], pos[1], pos[2]);
				b.obj.rotation.set(rot[0], rot[1], rot[2]);
				setOpacity(b, o);
			}
			// relative groups: their geometry is in world coordinates (home = origin), or centred (home = placement)
			{
				// vessel + stand: ghosts settle, the stand solidifies and the vessel lowers onto it in the vessel phase
				const vq = cq('vessel', p);
				const lower = ease(seg(vq, 0.05, 0.4));
				const vPos: V3 = p < PH.vessel[0] ? add3([0, VESSEL_LIFT, 0], sc3(IOFF.vessel, 1 - settle)) : [0, VESSEL_LIFT * (1 - lower), 0];
				vessel.obj.position.set(...vPos);
				setOpacity(vessel, p < PH.vessel[0] ? ghostIn(0) : lerp(0.32, 1, easeOut(seg(vq, 0, 0.3))));
				const sPos: V3 = p < PH.vessel[0] ? sc3(IOFF.stand, 1 - settle) : [0, 0, 0];
				stand.obj.position.set(...sPos);
				setOpacity(stand, p < PH.vessel[0] ? ghostIn(0.05) : lerp(0.32, 1, easeOut(seg(vq, 0, 0.3))));
				// water rises once the vessel sits on the stand
				const fill = p < PH.vessel[0] ? 0 : ease(seg(vq, 0.42, 0.95));
				const hgt = Math.max(0.01, (level - wY0) * fill);
				waterMesh.scale.set(wX[1] - wX[0], hgt, wZ[1] - wZ[0]);
				waterMesh.position.set((wX[0] + wX[1]) / 2, wY0, (wZ[0] + wZ[1]) / 2);
				water.obj.position.copy(vessel.obj.position);
				setOpacity(water, fill > 0.002 ? 1 : 0);
			}
			staged(dia, 'diaphragm', 0.1, 0.75, [0, 0, 0], [80, 0, 0], [TAU, 0, 0], 0.1);
			staged(basin, 'jet', 0.0, 0.3, basinAt, [0, 260, 0], [0, 0.8, 0], 0.22);
			staged(lens, 'lens', 0.05, 0.45, [lensC[0], lensC[1], lensC[2]], [-260, 0, 0], [0, 0, 0], 0.15);
			staged(tube, 'lens', 0.4, 0.9, tubeC, [-340, 0, 0], [0, 0, 0], 0.18);
			staged(shutter, 'room', 0.0, 0.45, shutterAt, [0, -1300, 0], [0, 0, 0], 0.26);
			staged(mirror, 'sun', 0.0, 0.32, mirrorAt, [-160, 120, 0], [0, 0.6, 0], 0.3);
			// once the light is inside the vessel the close shots look past the shutter: it fades to a ghost (cutaway)
			// and returns with the explode slider
			{
				const cut = ease(seg(cq('focus', p), 0, 0.3)) * (1 - kk);
				if (cut > 0) setOpacity(shutter, shutter.o * (1 - cut));
			}
			// mirror orientation: law of reflection (normal from the spec), spin on arrival about the vertical
			{
				const spinY = mirror.obj.rotation.y;
				mirror.obj.lookAt(tmp.set(mirror.obj.position.x + mN.x, mirror.obj.position.y + mN.y, mirror.obj.position.z + mN.z));
				mirror.obj.rotateOnWorldAxis(tmp.set(0, 1, 0), spinY);
			}

			// ---- room light: falls to near dark in the room phase (sunlit mirror outside keeps its reflection)
			const dark = ease(seg(cq('room', p), 0.25, 0.85));
			// light page: the room darkens less (a black model on a light page would bury the chapter text)
			const amb = lerp(1, theme === 'light' ? 0.6 : 0.2, dark);
			hemi.intensity = (theme === 'light' ? 1.1 : 0.9) * amb;
			key.intensity = 2.2 * amb;
			fill.intensity = 0.8 * amb;
			for (const r of roomLit) r.m.envMapIntensity = r.env * lerp(1, theme === 'light' ? 0.6 : 0.2, dark);
			edgeMat.opacity = lerp(0.9, 0.6, dark) * vessel.o;

			// ---- phases of the closing chapter: drops (thin jet), then clouded water (thick jet back)
			const dq0 = cq('drops', p);
			const cl = cq('clouded', p);
			const toThin = p < PH.drops[0] ? 0 : p < PH.clouded[0] ? ease(seg(dq0, 0, 0.25)) : 1 - ease(seg(cl, 0, 0.2));
			const dropsOn = p < PH.drops[0] ? 0 : p < PH.clouded[0] ? easeOut(seg(dq0, 0.18, 0.4)) : 1 - ease(seg(cl, 0, 0.18));
			const cloud = ease(seg(cl, 0.15, 0.6));

			// ---- diaphragm plates: 10 mm, swapped for 3 mm in the drops phase
			diaMatA.opacity *= 1 - toThin;
			diaMatB.opacity = diaBase * dia.o * toThin;
			diaMatB.transparent = diaMatB.opacity < 0.999;
			diaMatB.depthWrite = !diaMatB.transparent;
			diaBig.visible = diaMatA.opacity > 0.004;
			diaSmall.visible = diaMatB.opacity > 0.004;
			if (toThin > 0 && toThin < 1) diaGroup.rotation.x = TAU * 0.5 * (toThin < 0.5 ? toThin : 1 - toThin);

			// ---- jet: intro ghost (whole path), grows in the jet phase along the ballistic path in physical time
			let front = 0;
			let jetO = 0;
			if (p < PH.jet[0]) {
				front = 1;
				jetO = ghostIn(0.2) * (1 - leave);
				jet.obj.position.set(...sc3(IOFF.jet, 1 - settle));
			} else {
				const jq = cq('jet', p);
				front = uAtTau(tauL * seg(jq, 0.3, 0.9));
				jetO = front > 0 ? 1 : 0;
				jet.obj.position.set(0, 0, 0);
			}
			setOpacity(jet, jetO);
			// in the dark room the clear jet is barely visible
			const faint = lerp(1, 0.4, dark) * (1 - 0.25 * cloud);
			const jetK = theme === 'light' ? 2.3 : 1;
			jetMat.opacity = Math.min(1, jetBase * jetK * jetO * faint * (1 - toThin));
			thinMat.opacity = Math.min(1, jetBase * jetK * jetO * faint * toThin);
			jetMesh.visible = jetMat.opacity > 0.003;
			thinMesh.visible = thinMat.opacity > 0.003;
			jetGeo.setDrawRange(0, Math.round(front * JT) * JRAD * 6);
			// thin jet: continuous to the break-up point while drops show
			const thinEnd = lerp(1, breakU, clamp01(dropsOn * 1.4));
			thinGeo.setDrawRange(0, Math.round(Math.min(front, thinEnd) * JT) * 10 * 6);

			// ---- light (fades with the explode slider)
			const lightK = 1 - seg(kk, 0, 0.15);
			const sq = cq('sun', p);
			const sunG = p < PH.sun[0] ? 0 : ease(seg(sq, 0.28, 0.55));
			const parG = p < PH.sun[0] ? 0 : seg(sq, 0.52, 0.95);
			const coneG = p < PH.focus[0] ? 0 : seg(cq('focus', p), 0.05, 0.7);
			const sunI = (sunG > 0 ? 1 : 0) * lightK;
			sunMesh.position.set(mC[0] + toSun.x * SUN_L * (1 - sunG), mC[1] + toSun.y * SUN_L * (1 - sunG), mC[2] + toSun.z * SUN_L * (1 - sunG));
			sunMesh.scale.set(1, Math.max(0.001, SUN_L * sunG), 1);
			sunProxy.position.copy(sunMesh.position);
			sunProxy.scale.copy(sunMesh.scale);
			sunMat.uniforms.uI.value = 0.8 * sunI;
			parMesh.position.set(mC[0], 0, 0);
			parMesh.scale.set(Math.max(0.001, parL * parG), 1, 1);
			parProxy.position.copy(parMesh.position);
			parProxy.scale.copy(parMesh.scale);
			parMat.uniforms.uI.value = (parG > 0 ? 0.55 : 0) * lightK;
			coneMat.uniforms.uI.value = (coneG > 0 ? 0.5 + 0.35 * cloud : 0) * lightK;
			coneMat.uniforms.uFront.value = coneG * 1.02;
			mirrorFlashMat.opacity = (sunG > 0.98 ? 0.55 : 0) * lightK;
			mirrorFlash.scale.setScalar(150);
			spotMat.opacity = seg(coneG, 0.85, 1) * 0.8 * lightK;
			spot.scale.setScalar(36);
			const beamOn = Math.max(sunI > 0 ? 1 : 0, coneG > 0 ? 1 : 0) * lightK;
			beam.o = beamOn;
			beam.obj.visible = beamOn > 0.002;

			// ---- guided rays: enter when the cone reaches the orifice, run along the jet to the basin
			const rayF = span(p, 'focus', 0.75, 'tir', 0.8);
			const rayI =
				p < PH.basin[0]
					? 1
					: p < PH.drops[0]
						? lerp(1, 0.1, ease(seg(cq('basin', p), 0.1, 0.6))) // clear water: the jet barely shows
						: p < PH.clouded[0]
							? 0.1 * (1 - toThin)
							: 0.1 * (1 - toThin) * (1 - 0.35 * cloud);
			const rayO = (rayF > 0 ? rayI : 0) * lightK;
			rayMat.opacity = (theme === 'light' ? 0.85 : 0.95) * rayO;
			const nR = Math.round(Math.min(rayF, front) * RAY_SEG) * RAY_RAD * 6;
			for (const g of rayGeos) g.setDrawRange(0, nR);
			guided.o = rayO;
			guided.obj.visible = rayO > 0.003;

			// ---- escaped light: the basin floor lights once the light reaches it (end of the reflection phase)
			const esc = span(p, 'tir', 0.8, 'basin', 0.55); // starts when the ray front reaches the basin
			const escK = p < PH.drops[0] ? 1 : p < PH.clouded[0] ? lerp(1, 0.25, dropsOn) : lerp(0.25, 0.6, ease(seg(cl, 0, 0.3)));
			const escI = esc * escK * lightK;
			escaped.obj.position.set(...basinAt);
			floorGlow.scale.setScalar(lerp(30, bR * 0.82, easeOut(esc)));
			floorGlowMat.opacity = 0.75 * escI;
			contactMat.opacity = 0.7 * escI * (1 - toThin);
			contact.scale.setScalar(70);
			escaped.o = escI;
			escaped.obj.visible = escI > 0.003;
			basinLight.position.set(basinAt[0], ySurf - 30, basinAt[2]);
			basinLight.intensity = escI * 2.2e4;

			// ---- drops: thin jet breaks up in its lower part; drops follow the ballistic path, each pinch-off flashes
			const dropI = dropsOn * lightK;
			if (dropI > 0.003) {
				// A in path cycles; one pinch-off every 1 / ND: 8 pinch-offs (8 rupture flashes) across the drops phase,
				// slow motion so each flash is seen in Play
				const A = dq0 * (8 / ND) + 0.37;
				let newest = 1;
				for (let i = 0; i < ND; i++) {
					const s0 = dropSeeds[i];
					const ph = fract(i / ND + A + (s0.j - 0.5) * (0.35 / ND));
					newest = Math.min(newest, ph * ND);
					const tau = tauB + ph * (tauL - tauB);
					pathAt(tau, dpv);
					dpv.y += s0.dy;
					dpv.z += s0.dz;
					const r = dropR * s0.s * (0.75 + 0.25 * clamp01(ph * ND));
					dsv.setScalar(r);
					dm.compose(dpv, dq, dsv);
					dropMesh.setMatrixAt(i, dm);
					const fl = Math.exp(-ph * ND * 2.2);
					const b = clamp01((0.5 + 0.9 * fl) * dropI);
					if (theme === 'light') dropCol.set(WARM_L).multiplyScalar(0.75 + 0.25 * b);
					else dropCol.setRGB(b, b * 0.95, b * 0.82);
					dropMesh.setColorAt(i, dropCol);
				}
				dropMesh.instanceMatrix.needsUpdate = true;
				if (dropMesh.instanceColor) dropMesh.instanceColor.needsUpdate = true;
				pathAt(tauB, dpv);
				rupt.position.copy(dpv);
				ruptMat.opacity = dropI * (0.35 + 0.65 * Math.exp(-newest * 2.6));
				rupt.scale.setScalar(26 + 22 * Math.exp(-newest * 2.6));
			}
			drops.o = dropI;
			drops.obj.visible = dropI > 0.003;

			// ---- clouded water: milky water, the upper jet and the cone in the vessel glow
			waterMat.color.copy(theme === 'light' ? waterLight : waterBase).lerp(milky, 0.7 * cloud); // light page: blue-grey
			waterMat.opacity = num(look('water').opacity, 0.22) * water.o * (1 + 0.6 * cloud);
			const scI = cloud * lightK;
			scatMat.uniforms.uI.value = 0.75 * scI;
			vesselScatMat.uniforms.uI.value = 0.22 * scI;
			scatter.o = scI;
			scatter.obj.visible = scI > 0.003;

			// ---- emphasis
			for (const b of [vessel, stand, dia, jet, basin, lens, tube, shutter, mirror, water]) tint(b);
			edgeMat.color.set(hi.includes('vessel') ? accent : theme === 'light' ? '#5f6a76' : '#9aa3ad');
			if (hi.includes('vessel')) edgeMat.opacity = Math.max(edgeMat.opacity, 0.9);
			lensEdgeMat.color.set(hi.includes('lens') ? accent : theme === 'light' ? '#5d84a8' : '#cfe4f5');
			lensEdgeMat.opacity = 0.8 * lens.o;
			standEdgeMat.opacity = stand.o;
			shEdgeMat.opacity = shutter.o;
			const emph = (on: boolean, m: THREE_NS.ShaderMaterial, dark: string, light: string) => m.uniforms.uColor.value.set(on ? accent : theme === 'light' ? light : dark);
			for (const m of [sunMat, parMat, coneMat]) emph(hi.includes('beam'), m, '#fff4d6', WARM_L);
			emph(hi.includes('scatter'), scatMat, '#fff1c8', WARM_L);
			rayMat.color.set(hi.includes('guided_light') ? accent : theme === 'light' ? '#b8740a' : '#fff6dc');
			floorGlowMat.color.set(hi.includes('escaped_light') ? accent : theme === 'light' ? WARM_L : WARM_D);
		}

		// ---------------------------------------------------------------------------- handle
		/** effects and small parts win over the large bodies they sit in */
		const PRIORITY = ['diaphragm', 'lens', 'drops', 'guided_light', 'scatter', 'escaped_light', 'beam', 'jet'];
		const handle: ShowcaseHandle = {
			assembledAt: spec.chapters[spec.chapters.length - 1]?.p[0] ?? PH.drops[0],
			frame,
			highlight(ids) {
				hi = [...ids];
			},
			pick(x, y): string | PickInfo | null {
				v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
				raycaster.setFromCamera(v2, camera);
				const cands: THREE_NS.Mesh[] = [];
				for (const b of bodies.values()) if (b.obj.visible && b.o > 0.2) cands.push(...b.picks);
				const hits = raycaster.intersectObjects(cands, false);
				if (!hits.length) return null;
				let best: string | null = null;
				let rank = PRIORITY.length;
				for (const hh of hits) {
					const id = hh.object.userData.part as string;
					const r = PRIORITY.indexOf(id);
					if (r >= 0 && r < rank) {
						rank = r;
						best = id;
					}
				}
				return best ?? (hits[0].object.userData.part as string) ?? null;
			},
			anchor(id) {
				if (id !== 'vessel' || vessel.o < 0.5) return null;
				tmp.set(vX[1], vY[0] + vH * 0.62, vZ[1]).add(vessel.obj.position);
				camera.updateMatrixWorld();
				tmp2.copy(tmp).applyMatrix4(camera.matrixWorldInverse);
				if (tmp2.z > -camera.near) return null;
				tmp.project(camera);
				const sx = ((tmp.x + 1) / 2) * w;
				const sy = ((1 - tmp.y) / 2) * h;
				if (sx < 0 || sx > w || sy < 0 || sy > h) return null;
				return [sx, sy];
			},
			target() {
				return [curShot.t[0], curShot.t[1], curShot.t[2]];
			},
			resize(nw, nh) {
				w = Math.max(1, nw);
				h = Math.max(1, nh);
			},
			explode(nk) {
				k = clamp01(nk);
			},
			theme(t) {
				theme = t;
				applyTheme();
			},
			dispose() {
				scene.remove(root);
				camera.clearViewOffset();
				dropMesh.dispose();
				for (const d of disposables) d.dispose();
			}
		};
		return handle;
	}
};
export default mod;
