// Scene module: Kerr frequency comb from a silica toroid on a silicon chip (Del'Haye et al., Nature 2007; values and
// locators from the arXiv preprint). Spec: data/history/showcases/delhaye2007.yaml. Contract: ../showcase/types.ts.
// Units µm; y up, origin on the pillar axis at the etched silicon floor; taper axis along +x (light runs +x) on the -z
// side of the toroid, in the rim's equatorial plane.
//
// Process chapters (oxide, undercut, reflow) follow the toroid process the paper cites (Armani et al., Nature 2003);
// their values are that paper's (its Fig. 2 example toroid: 120 µm; process HUD and part hovers say so). The drawn disk and resist
// pad (100 µm), the taper waist (3 µm) and gap (0.3 µm) are assumed values from the spec, labelled in hover.
// Intermediate pillar shapes during the undercut are a morph toward the profile read from the Fig. 1C SEM.
//
// Light (colours illustrative, 1.55 µm is infrared): the pump runs +x along the taper, couples in at the taper and
// circulates in the same sense (+x at the coupling point); the rim light and the output taper carry one stripe per
// lit line, ordered by wavelength, brightness from each line's digitized power (dB). Before the pump reaches the rim no
// line exists; the first signal / idler pair appears in the four-wave-mixing chapter; in the comb chapter each further
// line lights once the plot has drawn its stem (the runtime's revealAt; whole stems only), pump outward as listed in the
// spec. The output light ends before the plot panel in the plot chapters.
import type * as THREE_NS from 'three';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import { revealAt } from '../showcase/plot';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type V3 = [number, number, number];
type Rect = [number, number, number, number];
type Geo = Record<string, unknown>;
type P2 = [number, number];

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);

/** deterministic PRNG (mulberry32) */
function prng(seed: number) {
	let a = seed >>> 0;
	return () => {
		a = (a + 0x6d2b79f5) >>> 0;
		let t = a;
		t = Math.imul(t ^ (t >>> 15), t | 1);
		t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
}

// ------------------------------------------------------------------------------------------------ shots (camera)
// Keyframed shots per chapter (q = local progress). R = [half width, half height] (µm) around t that must fit the
// region (full pane, or the left half / top strip during plot chapters). az from +z toward +x, el above the horizon.
interface Shot {
	t: V3;
	az: number;
	el: number;
	R: [number, number];
}
interface Key extends Shot {
	q: number;
}
const CHAPTER_IDS = ['intro', 'oxide', 'undercut', 'reflow', 'toroid', 'taper', 'pump', 'fwm', 'comb', 'spacing'];
const PLOT_CHAPTERS = new Set(['comb', 'spacing']);
const SHOTS: Record<string, Key[]> = {
	intro: [
		{ q: 0, t: [0, 24, -12], az: -18, el: 24, R: [80, 44] },
		{ q: 1, t: [0, 18, 0], az: 16, el: 28, R: [120, 62] }
	],
	oxide: [
		{ q: 0, t: [0, 24, 0], az: 18, el: 42, R: [112, 56] },
		{ q: 1, t: [0, 26, 0], az: 30, el: 36, R: [92, 46] }
	],
	undercut: [
		{ q: 0, t: [0, 20, 0], az: 30, el: 16, R: [78, 40] },
		{ q: 1, t: [0, 16, 0], az: 42, el: 12, R: [70, 38] }
	],
	reflow: [
		{ q: 0, t: [0, 95, 0], az: 40, el: 16, R: [150, 110] },
		{ q: 0.22, t: [0, 80, 0], az: 37, el: 18, R: [135, 95] },
		{ q: 0.6, t: [0, 30, 0], az: 33, el: 22, R: [66, 40] },
		{ q: 1, t: [0, 26, 0], az: 30, el: 22, R: [60, 36] }
	],
	toroid: [
		{ q: 0, t: [0, 22, 0], az: 30, el: 20, R: [50, 32] },
		{ q: 1, t: [0, 22, 0], az: 110, el: 24, R: [50, 32] }
	],
	taper: [
		{ q: 0, t: [0, 28, -50], az: 24, el: 9, R: [96, 46] },
		{ q: 0.85, t: [0, 28.5, -20], az: 20, el: 4, R: [80, 30] },
		{ q: 1, t: [0, 28.5, -20], az: 20, el: 4, R: [80, 30] }
	],
	pump: [
		{ q: 0, t: [-210, 30, -40], az: 12, el: 18, R: [265, 80] },
		{ q: 0.42, t: [-170, 30, -40], az: 14, el: 18, R: [225, 70] },
		{ q: 0.74, t: [0, 27, -18], az: 22, el: 24, R: [60, 37] },
		{ q: 1, t: [0, 27, -18], az: 28, el: 24, R: [58, 36] }
	],
	fwm: [
		{ q: 0, t: [0, 27, -18], az: 28, el: 24, R: [58, 36] },
		{ q: 1, t: [0, 27, -18], az: 36, el: 24, R: [56, 35] }
	],
	comb: [
		{ q: 0, t: [4, 27, -18], az: 26, el: 24, R: [50, 32] },
		{ q: 1, t: [4, 27, -18], az: 34, el: 24, R: [50, 32] }
	],
	spacing: [
		{ q: 0, t: [196, 34, -90], az: 10, el: 26, R: [268, 92] },
		{ q: 1, t: [196, 34, -90], az: 16, el: 26, R: [268, 92] }
	]
};

function regions(w: number, h: number): { full: Rect; plot: Rect; plotBox: Rect } {
	if (w < 700) return { full: [0.04, 0.2, 0.96, 0.98], plot: [0.04, 0.17, 0.96, 0.43], plotBox: [0, 0.44, 1, 1] };
	const top = Math.min(0.24, 150 / Math.max(1, h));
	return { full: [0.03, top, 0.97, 0.97], plot: [0.03, top, 0.49, 0.97], plotBox: [0.5, 0.16, 1, 1] };
}

// ------------------------------------------------------------------------------------------------ shaders
// glow: view-dependent soft light (rim = bright at the silhouette), for the CO2 beam, the molten edge, the rim halo and
// the glass edge of the silica
const GLOW_VS = /* glsl */ `
varying vec3 vN; varying vec3 vV; varying float vX; varying float vR;
void main() {
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	vN = normalize(normalMatrix * normal);
	vV = normalize(-mv.xyz);
	vX = position.x;
	vR = length(position.xz);
	gl_Position = projectionMatrix * mv;
}`;
const GLOW_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uPow; uniform float uLight; uniform float uRim; uniform float uK;
uniform float uXMax; uniform float uR0;
varying vec3 vN; varying vec3 vV; varying float vX; varying float vR;
void main() {
	if (vX > uXMax) discard;
	float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
	float f = pow(uRim > 0.5 ? 1.0 - c : c, uPow);
	float a = clamp(f * uI * uK * (uR0 > 0.0 ? smoothstep(uR0 - 4.0, uR0 + 1.0, vR) : 1.0), 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a) : vec4(uColor * a, a);
}`;
// comb light: one stripe per lit line across the ribbon (aV), ordered by wavelength; stripe widths follow the line
// weights (a new line grows from zero width); a travelling pattern along aS shows the flow direction
const LIGHT_VS = /* glsl */ `
attribute float aS; attribute float aV;
varying float vS; varying float vV; varying float vX;
void main() {
	vS = aS; vV = aV; vX = position.x;
	gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`;
const lightFS = (n: number) => /* glsl */ `
#define NL ${n}
uniform float uW[NL]; uniform float uB[NL]; uniform vec3 uC[NL];
uniform float uS0; uniform float uS1; uniform float uFeather; uniform float uPhase; uniform float uLobes;
uniform float uK; uniform float uLight; uniform float uXMax; uniform float uStripe;
varying float vS; varying float vV; varying float vX;
void main() {
	if (vX > uXMax) discard;
	float win = smoothstep(uS0, uS0 + uFeather, vS) * (1.0 - smoothstep(uS1 - uFeather, uS1, vS));
	if (win <= 0.0) discard;
	float tot = 0.0;
	for (int i = 0; i < NL; i++) tot += uW[i];
	if (tot < 1e-4) discard;
	float t = clamp(vV, 0.0, 1.0) * tot;
	float acc = 0.0; vec3 col = vec3(0.0); float b = 0.0; float fr = 0.5;
	for (int i = 0; i < NL; i++) {
		float wi = uW[i];
		if (wi <= 0.0) continue;
		if (t <= acc + wi) { col = uC[i]; b = uB[i]; fr = (t - acc) / wi; break; }
		acc += wi;
	}
	float stripe = mix(1.0, 0.62 + 0.38 * sin(3.14159265 * fr), uStripe);
	float flow = 0.7 + 0.3 * cos(6.2831853 * (uLobes * vS - uPhase));
	float edge = smoothstep(0.0, 0.14, vV) * smoothstep(1.0, 0.86, vV);
	float xf = 1.0 - smoothstep(uXMax - 6.0, uXMax, vX);
	float a = clamp(b * stripe * flow * edge * win * xf * uK, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(col, a) : vec4(col * a, a);
}`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('delhaye2007 is a 3D scene');
		const { THREE, scene, camera, spec } = ctx;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let k = 0;
		let theme: Theme = ctx.theme;
		let hi: string[] = [];

		const partOf = (id: string) => spec.parts.find((q) => q.id === id);
		const geo = (id: string): Geo => (partOf(id)?.geometry ?? {}) as Geo;
		const look = (id: string) => partOf(id)?.look ?? {};
		const at = (id: string, d: V3): V3 => {
			const pos = spec.assembly?.find((a) => a.part === id)?.pos;
			return Array.isArray(pos) && pos.length === 3 ? [pos[0], pos[1], pos[2]] : d;
		};
		const fallback: Record<string, [number, number]> = {
			intro: [0, 0.07], oxide: [0.07, 0.17], undercut: [0.17, 0.27], reflow: [0.27, 0.38], toroid: [0.38, 0.45],
			taper: [0.45, 0.54], pump: [0.54, 0.63], fwm: [0.63, 0.72], comb: [0.72, 0.87], spacing: [0.87, 1]
		};
		const C = Object.fromEntries(
			CHAPTER_IDS.map((id) => [id, (spec.chapters.find((c) => c.id === id)?.p ?? fallback[id]) as [number, number]])
		) as Record<string, [number, number]>;
		const cq = (id: string, p: number) => seg(p, C[id][0], C[id][1]);
		const after = (id: string, p: number) => p >= C[id][0];

		// ---------------------------------------------------------------------------- dimensions from the spec
		const chipG = geo('si_chip');
		const chipXZ = (Array.isArray(chipG.size_xz) ? chipG.size_xz : [400, 400]) as number[];
		const Y_OX0 = num(chipG.y_top_before_etch, 27.5); // silicon top before the undercut = disk underside
		const DEPTH = num(chipG.drawn_depth, 40);
		const oxG = geo('oxide_film');
		const OX_T = Array.isArray(oxG.y) ? num((oxG.y as number[])[1], 29.5) - num((oxG.y as number[])[0], 27.5) : 2;
		const padG = geo('resist_pad');
		const PAD_R = num(padG.diameter, 100) / 2;
		const PAD_T = num(padG.thickness, 1.5);
		const DISK_R = num(geo('silica_disk').diameter, 100) / 2;
		const torG = geo('toroid');
		const RO = num(torG.outer_diameter, 75) / 2; // drawn as the outer diameter (spec)
		const AMIN = num(torG.minor_diameter, 5) / 2;
		const YC = num(torG.rim_center_y, 28.5);
		const MEM_H = OX_T / 2; // membrane half thickness
		const pillarProf = ((geo('si_pillar').profile_h_r as P2[] | undefined) ?? [[0, 27], [27.5, 15.3]]).slice().sort((a, b) => a[0] - b[0]);
		const beamR = num(geo('co2_beam').diameter, 200) / 2;
		const tapG = geo('taper');
		const WAIST_R = num(tapG.waist_diameter, 3) / 2;
		const WAIST_HL = num(tapG.waist_length_drawn, 300) / 2;
		const TAPER: V3 = at('taper', (Array.isArray(tapG.center) ? tapG.center : [0, 28.5, -39.3]) as V3);
		const LASER = at('pump_laser', [-400, 28.5, -39.3]);
		const OSA = at('osa', [400, 28.5, -39.3]);
		// boxes are schematic stand-ins (spec: not to scale); the reference comb sits beside the output box (spec)
		const BOX: V3 = [90, 52, 72];
		const REF: V3 = [OSA[0] - 30, OSA[1], OSA[2] - 170];
		const X_IN = LASER[0] + BOX[0] / 2; // fiber leaves the laser box
		const X_OUT = OSA[0] - BOX[0] / 2; // and enters the output box
		const pillarR = (y: number) => {
			const P = pillarProf;
			if (y <= P[0][0]) return P[0][1];
			for (let i = 1; i < P.length; i++)
				if (y <= P[i][0]) return lerp(P[i - 1][1], P[i][1], (y - P[i - 1][0]) / Math.max(1e-6, P[i][0] - P[i - 1][0]));
			return P[P.length - 1][1];
		};
		const taperR = (x: number) => {
			const ax = Math.abs(x);
			if (ax <= WAIST_HL) return WAIST_R;
			const u = clamp01((ax - WAIST_HL) / Math.max(1, X_OUT - WAIST_HL));
			return WAIST_R + 7.5 * u * u; // neutral flare toward the boxes, not to scale
		};

		// ---------------------------------------------------------------------------- comb lines (plot Fig. 1A)
		const combPlot = spec.plots?.find((q) => q.id === 'comb');
		const combSeries = combPlot?.series ?? [];
		const stemIdx = Math.max(0, combSeries.findIndex((s) => s.style === 'stems'));
		const linePts = ((combSeries[stemIdx]?.points ?? []) as P2[]).filter((q) => Number.isFinite(q[0]) && Number.isFinite(q[1]));
		const NL = Math.max(1, linePts.length);
		const pumpLam = linePts[0]?.[0] ?? 1551.9;
		/** lines drawn by the plot pen at p (continuous: whole lines plus the fraction of the next), with the runtime's own
		 *  reveal (revealAt, the code the plot assembler uses) */
		const penAt = (p: number): number => (revealAt(spec, 'comb', p)[stemIdx] ?? 0) * linePts.length;
		// slots ordered by wavelength (short at the top of a ribbon); spec index -> slot
		const order = linePts.map((q, i) => ({ i, lam: q[0], dbm: q[1] })).sort((a, b) => a.lam - b.lam);
		const slotOf = new Int32Array(NL);
		order.forEach((o, s) => (slotOf[o.i] = s));
		const dbN = (d: number) => clamp01((d + 30) / (17.7 + 30)); // -30 dBm .. pump peak
		const COL = {
			dark: { pump: '#ff4d4d', blue: '#4c9bf0', pink: '#ea70a3' },
			light: { pump: '#d42a2a', blue: '#1f6fd0', pink: '#c23d7c' }
		};
		const uW = new Float32Array(NL);
		const uB = new Float32Array(NL);
		const uC = new Float32Array(NL * 3);
		const uWin = new Float32Array(NL); // input taper: pump only
		const uBin = new Float32Array(NL);
		const baseW = new Float32Array(NL);
		const baseB = new Float32Array(NL);
		order.forEach((o, s) => {
			baseW[s] = 0.45 + 0.55 * dbN(o.dbm);
			baseB[s] = 0.3 + 0.7 * dbN(o.dbm);
		});
		const tmpC = new THREE.Color();
		function fillColours() {
			const pal = COL[theme];
			order.forEach((o, s) => {
				const side = o.i === 0 ? pal.pump : o.lam < pumpLam ? pal.blue : pal.pink;
				tmpC.set(side);
				if (o.i !== 0) tmpC.multiplyScalar(s % 2 ? 0.86 : 1.06); // neighbouring stripes stay distinguishable
				uC[s * 3] = tmpC.r;
				uC[s * 3 + 1] = tmpC.g;
				uC[s * 3 + 2] = tmpC.b;
			});
		}

		// ---------------------------------------------------------------------------- materials, bodies
		const disposables: { dispose(): void }[] = [];
		const keep = <T extends { dispose(): void }>(x: T): T => (disposables.push(x), x);
		const G = <T extends THREE_NS.BufferGeometry>(g: T): T => keep(g);
		const nopick = <T extends THREE_NS.Object3D>(o: T): T => ((o.userData.nopick = true), o);
		const root = new THREE.Group();
		scene.add(root);

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
				if ((n as THREE_NS.Mesh).isMesh && m && 'emissive' in m && !b.mats.some((x) => x.m === m))
					b.mats.push({ m, base: m.opacity, trans: m.transparent });
				if ((n as THREE_NS.Mesh).isMesh && !n.userData.nopick) {
					n.userData.part = id;
					b.picks.push(n as THREE_NS.Mesh);
				}
			});
			root.add(obj);
			bodies.set(id, b);
			return b;
		}
		const std = (id: string, extra: Partial<THREE_NS.MeshPhysicalMaterialParameters> = {}) => {
			const lk = look(id);
			const op = num(lk.opacity, 1);
			return keep(
				new THREE.MeshPhysicalMaterial({
					color: lk.color || '#888888',
					metalness: num(lk.metal, 0),
					roughness: num(lk.rough, 0.5),
					transparent: op < 1,
					opacity: op,
					...extra
				})
			);
		};
		interface GlowRec {
			m: THREE_NS.ShaderMaterial;
			dark: string;
			light: string;
			lightK: number;
		}
		const glows: GlowRec[] = [];
		const glowT = (dark: string, light: string, pow: number, rim = false, lightK = 1) => {
			const m = keep(
				new THREE.ShaderMaterial({
					uniforms: {
						uColor: { value: new THREE.Color(dark) },
						uI: { value: 0 },
						uPow: { value: pow },
						uLight: { value: 0 },
						uRim: { value: rim ? 1 : 0 },
						uK: { value: 1 },
						uXMax: { value: 1e9 },
						uR0: { value: -1 }
					},
					vertexShader: GLOW_VS,
					fragmentShader: GLOW_FS,
					transparent: true,
					depthWrite: false,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
			glows.push({ m, dark, light, lightK });
			return m;
		};
		const lights: THREE_NS.ShaderMaterial[] = [];
		const lightMat = (w: Float32Array, b: Float32Array, side: THREE_NS.Side = THREE.DoubleSide) => {
			const m = keep(
				new THREE.ShaderMaterial({
					uniforms: {
						uW: { value: w },
						uB: { value: b },
						uC: { value: uC },
						uS0: { value: 0 },
						uS1: { value: 1 },
						uFeather: { value: 0.02 },
						uPhase: { value: 0 },
						uLobes: { value: 6 },
						uK: { value: 1 },
						uLight: { value: 0 },
						uXMax: { value: 1e9 },
						uStripe: { value: 1 }
					},
					vertexShader: LIGHT_VS,
					fragmentShader: lightFS(NL),
					transparent: true,
					depthWrite: false,
					side,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
			lights.push(m);
			return m;
		};

		// ---------------------------------------------------------------------------- dynamic lathe (profile morphs)
		// contour in (r, y) traversed outward along the top, then down / around; normals from neighbour tangents
		function lathe(nProf: number, segs: number) {
			const g = G(new THREE.BufferGeometry());
			const pos = new Float32Array(nProf * (segs + 1) * 3);
			const nor = new Float32Array(nProf * (segs + 1) * 3);
			const idx: number[] = [];
			for (let i = 0; i < nProf - 1; i++)
				for (let j = 0; j < segs; j++) {
					const a = i * (segs + 1) + j;
					const b = (i + 1) * (segs + 1) + j;
					idx.push(a, a + 1, b, b, a + 1, b + 1);
				}
			g.setIndex(idx);
			g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
			g.setAttribute('normal', new THREE.BufferAttribute(nor, 3));
			const cs = Float32Array.from({ length: segs + 1 }, (_, j) => Math.cos((j / segs) * TAU));
			const sn = Float32Array.from({ length: segs + 1 }, (_, j) => Math.sin((j / segs) * TAU));
			let last = '';
			return {
				g,
				set(prof: P2[], key: string) {
					if (key === last) return;
					last = key;
					for (let i = 0; i < nProf; i++) {
						const [r, y] = prof[i];
						const pa = prof[Math.max(0, i - 1)];
						const pb = prof[Math.min(nProf - 1, i + 1)];
						let tx = pb[0] - pa[0];
						let ty = pb[1] - pa[1];
						const L = Math.hypot(tx, ty) || 1;
						tx /= L;
						ty /= L;
						const nr = -ty;
						const ny = tx;
						for (let j = 0; j <= segs; j++) {
							const o = (i * (segs + 1) + j) * 3;
							pos[o] = r * cs[j];
							pos[o + 1] = y;
							pos[o + 2] = r * sn[j];
							nor[o] = nr * cs[j];
							nor[o + 1] = ny;
							nor[o + 2] = nr * sn[j];
						}
					}
					g.attributes.position.needsUpdate = true;
					g.attributes.normal.needsUpdate = true;
					g.computeBoundingSphere();
					g.computeBoundingBox();
				}
			};
		}

		// ---------------------------------------------------------------------------- silicon chip (patch) + pillar
		const chipGeo = G(new THREE.BoxGeometry(chipXZ[0] ?? 400, 1, chipXZ[1] ?? 400).translate(0, 0.5, 0));
		// a finite chip patch with hard straight edges (patch size assumed in the spec); matte, low specular
		const chipMat = std('si_chip', { envMapIntensity: 0, specularIntensity: 0.25 });
		// silicon grey, toned per theme so the upward-facing patch does not read as a lit backdrop (look colour = hue)
		const chipBase = chipMat.color.clone();
		const chipMesh = new THREE.Mesh(chipGeo, chipMat);
		chipMesh.renderOrder = 1;
		const chipGroup = new THREE.Group();
		chipGroup.add(chipMesh);
		const chip = body('si_chip', chipGroup);

		const NPS = 26;
		const pillarL = lathe(NPS + 2, 96);
		const pillarMat = std('si_pillar', { envMapIntensity: 0 });
		const pillarGroup = new THREE.Group();
		const pillarMesh = new THREE.Mesh(pillarL.g, pillarMat);
		pillarMesh.renderOrder = 2; // after the (edge-faded, transparent) chip, so a fading pillar shows the chip behind it
		pillarGroup.add(pillarMesh);
		const pillar = body('si_pillar', pillarGroup);
		const pillarPts: P2[] = Array.from({ length: NPS + 2 }, () => [0, 0] as P2);
		function setPillar(e: number) {
			const yf = Y_OX0 * (1 - e);
			const tw = 0.82 * e + 0.18 * e * e; // lateral front lags slightly behind the vertical one at first
			pillarPts[0] = [0, Y_OX0];
			for (let i = 0; i <= NPS; i++) {
				const y = Y_OX0 - ((Y_OX0 - yf) * i) / NPS;
				pillarPts[i + 1] = [lerp(DISK_R, pillarR(y), tw), y];
			}
			pillarL.set(pillarPts, e.toFixed(4));
			return yf;
		}

		// ---------------------------------------------------------------------------- oxide film, resist pad
		const oxGeo = G(new THREE.BoxGeometry(chipXZ[0] ?? 400, 1, chipXZ[1] ?? 400).translate(0, 0.5, 0));
		const oxMat = std('oxide_film', { depthWrite: false, envMapIntensity: 0 });
		const oxGroup = new THREE.Group();
		const oxBase = oxMat.color.clone();
		const oxMesh = new THREE.Mesh(oxGeo, oxMat);
		oxMesh.renderOrder = 2;
		oxGroup.add(oxMesh);
		const oxide = body('oxide_film', oxGroup);
		const padGeo = G(new THREE.CylinderGeometry(PAD_R, PAD_R, PAD_T, 96).translate(0, PAD_T / 2, 0));
		const padGroup = new THREE.Group();
		padGroup.add(new THREE.Mesh(padGeo, std('resist_pad', { envMapIntensity: 0 })));
		const pad = body('resist_pad', padGroup);

		// ---------------------------------------------------------------------------- silica: disk -> toroid
		const NTOP = 8;
		const NARC = 44;
		const NSIL = NTOP * 2 + NARC;
		const silL = lathe(NSIL, 160);
		const silMat = std('toroid', { clearcoat: 1, clearcoatRoughness: 0.05, ior: 1.45, depthWrite: false, envMapIntensity: 0.7 });
		silMat.transparent = true;
		const silMesh = new THREE.Mesh(silL.g, silMat);
		silMesh.renderOrder = 4;
		const silEdgeMat = glowT('#dfeaf6', '#7d8796', 2.4, true);
		const silEdge = nopick(new THREE.Mesh(silL.g, silEdgeMat));
		silEdge.renderOrder = 5;
		const silGroup = new THREE.Group();
		silGroup.add(silMesh, silEdge);
		const sil = body('toroid', silGroup); // pick id switches to silica_disk before the reflow ends (frame)
		const silPts: P2[] = Array.from({ length: NSIL }, () => [0, 0] as P2);
		let rimRc = RO - AMIN;
		let rimA = AMIN;
		/** reflow progress s: outer radius 50 -> 37.5, rim radius 1 (half the membrane) -> 2.5; membrane unchanged */
		function setSilica(s: number) {
			const Ro = lerp(DISK_R, RO, s);
			const a = lerp(MEM_H, AMIN, s);
			const Rc = Ro - a;
			const th = Math.asin(Math.min(1, MEM_H / a)); // where the rim circle meets the membrane faces
			const rj = Rc - a * Math.cos(th);
			let n = 0;
			for (let i = 0; i < NTOP; i++) silPts[n++] = [(rj * i) / (NTOP - 1) * 0.999, YC + MEM_H];
			for (let i = 0; i < NARC; i++) {
				const ang = Math.PI - th - ((2 * Math.PI - 2 * th) * i) / (NARC - 1); // top, outer, bottom (clockwise)
				silPts[n++] = [Rc + a * Math.cos(ang), YC + a * Math.sin(ang)];
			}
			for (let i = 0; i < NTOP; i++) silPts[n++] = [rj * (1 - i / (NTOP - 1)) * 0.999, YC - MEM_H];
			silL.set(silPts, s.toFixed(4));
			rimRc = Rc;
			rimA = a;
		}

		// molten edge (reflow): soft orange light along the rim, illustrative
		const meltMat = glowT('#ff9a4a', '#d0601a', 0.8, false, 0.7);
		const melt = nopick(new THREE.Mesh(silL.g, meltMat));
		melt.renderOrder = 7;
		root.add(melt);

		// ---------------------------------------------------------------------------- XeF2 haze (seeded particles)
		const NH = 520;
		const hazeSeed = prng(2007);
		const hazeBase = Float32Array.from({ length: NH * 4 }, () => hazeSeed());
		const hazePos = new Float32Array(NH * 3);
		const hazeGeo = G(new THREE.BufferGeometry());
		hazeGeo.setAttribute('position', new THREE.BufferAttribute(hazePos, 3));
		const dotTex = (() => {
			const cv = document.createElement('canvas');
			cv.width = cv.height = 64;
			const g = cv.getContext('2d')!;
			const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
			gr.addColorStop(0, 'rgba(255,255,255,1)');
			gr.addColorStop(0.45, 'rgba(255,255,255,0.55)');
			gr.addColorStop(1, 'rgba(255,255,255,0)');
			g.fillStyle = gr;
			g.fillRect(0, 0, 64, 64);
			const t = new THREE.CanvasTexture(cv);
			t.colorSpace = THREE.SRGBColorSpace;
			return keep(t);
		})();
		const hazeMat = keep(new THREE.PointsMaterial({ color: look('xef2_gas').color || '#d8d8e6', map: dotTex, size: 2.2, sizeAttenuation: true, transparent: true, opacity: 0, depthWrite: false }));
		const haze = nopick(new THREE.Points(hazeGeo, hazeMat));
		haze.renderOrder = 6;
		const hazeProxy = new THREE.Mesh(G(new THREE.BoxGeometry(300, 70, 300).translate(0, 38, 0)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		const hazeGroup = new THREE.Group();
		hazeGroup.add(haze, hazeProxy);
		const gas = body('xef2_gas', hazeGroup);
		const HZ = { x: 130, y0: 4, y1: 70 };
		function setHaze(p: number) {
			for (let i = 0; i < NH; i++) {
				const r0 = hazeBase[i * 4];
				const r1 = hazeBase[i * 4 + 1];
				const r2 = hazeBase[i * 4 + 2];
				const r3 = hazeBase[i * 4 + 3];
				const span = HZ.y1 - HZ.y0;
				const y = HZ.y1 - ((((r1 * span + p * 2600 * (0.6 + 0.8 * r3)) % span) + span) % span);
				hazePos[i * 3] = (r0 * 2 - 1) * HZ.x + 6 * Math.sin(TAU * (r2 + p * 9));
				hazePos[i * 3 + 1] = y;
				hazePos[i * 3 + 2] = (r2 * 2 - 1) * HZ.x;
			}
			hazeGeo.attributes.position.needsUpdate = true;
		}

		// ---------------------------------------------------------------------------- CO2 beam (illustrative colour)
		const BEAM_Y0 = YC + MEM_H + 1.5;
		const BEAM_L = 230;
		const beamMat = glowT(look('co2_beam').emissive || '#ff8a3a', '#d06a20', 1.6, false, 0.55);
		const beamMesh = new THREE.Mesh(G(new THREE.CylinderGeometry(beamR, beamR, BEAM_L, 96, 1, true).translate(0, BEAM_Y0 + BEAM_L / 2, 0)), beamMat);
		beamMesh.renderOrder = 8;
		const beamGroup = new THREE.Group();
		beamGroup.add(beamMesh);
		const beam = body('co2_beam', beamGroup);

		// ---------------------------------------------------------------------------- tapered fiber
		const NTX = 260;
		const NTR = 28;
		const tapGeo = G(new THREE.BufferGeometry());
		{
			const pos: number[] = [];
			const nor: number[] = [];
			const idx: number[] = [];
			for (let i = 0; i <= NTX; i++) {
				const x = lerp(X_IN, X_OUT, i / NTX);
				const r = taperR(x);
				const dr = (taperR(x + 0.5) - taperR(x - 0.5)) / 1;
				for (let j = 0; j <= NTR; j++) {
					const a = (j / NTR) * TAU;
					pos.push(x, r * Math.cos(a), r * Math.sin(a));
					const L = Math.hypot(1, dr);
					nor.push(-dr / L, Math.cos(a) / L, Math.sin(a) / L);
				}
			}
			for (let i = 0; i < NTX; i++)
				for (let j = 0; j < NTR; j++) {
					const a = i * (NTR + 1) + j;
					const b = (i + 1) * (NTR + 1) + j;
					idx.push(a, a + 1, b, b, a + 1, b + 1);
				}
			tapGeo.setIndex(idx);
			tapGeo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
			tapGeo.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
		}
		const tapMat = std('taper', { clearcoat: 1, clearcoatRoughness: 0.05, depthWrite: false, envMapIntensity: 0.7 });
		tapMat.transparent = true;
		const tapClip = { value: 1e9 };
		tapMat.customProgramCacheKey = () => 'delhaye2007-taper-clip';
		tapMat.onBeforeCompile = (sh) => {
			sh.uniforms.uXMax = tapClip;
			sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying float vTX;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvTX = position.x;');
			sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying float vTX;\nuniform float uXMax;').replace('void main() {', 'void main() {\n\tif (vTX > uXMax) discard;');
		};
		const tapMesh = new THREE.Mesh(tapGeo, tapMat);
		tapMesh.renderOrder = 4;
		const tapEdgeMat = glowT('#e6eef5', '#7d8796', 2.2, true, 1);
		const tapEdge = nopick(new THREE.Mesh(tapGeo, tapEdgeMat));
		tapEdge.renderOrder = 5;
		// pick proxy: the waist is a few µm thick, so hovering uses a wider invisible sleeve
		const tapProxy = new THREE.Mesh(G(new THREE.CylinderGeometry(7, 7, X_OUT - X_IN, 12, 1, true).rotateZ(Math.PI / 2).translate((X_IN + X_OUT) / 2, 0, 0)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		const tapGroup = new THREE.Group();
		tapGroup.add(tapMesh, tapEdge, tapProxy);
		const taper = body('taper', tapGroup);

		// ---------------------------------------------------------------------------- light ribbons
		// ring: a vertical band at the rim's outer equator plus a flat band in the equatorial plane (seen from above);
		// aS = 0 at the coupling point, increasing in the circulation sense (+x at the coupling point)
		const RB = RO - AMIN * 0.55;
		const HB = AMIN * 0.68;
		function ringRibbon(vertical: boolean) {
			const S = 320;
			const pos: number[] = [];
			const aS: number[] = [];
			const aV: number[] = [];
			const idx: number[] = [];
			for (let j = 0; j <= S; j++) {
				const s = j / S;
				const ph = -Math.PI / 2 + s * TAU;
				for (let v = 0; v <= 1; v++) {
					const r = vertical ? RB : RB + (v - 0.5) * 2 * HB;
					const y = vertical ? YC + (0.5 - v) * 2 * HB : YC;
					pos.push(r * Math.cos(ph), y, r * Math.sin(ph));
					aS.push(s);
					aV.push(vertical ? v : 1 - v);
				}
			}
			for (let j = 0; j < S; j++) idx.push(j * 2, j * 2 + 1, j * 2 + 2, j * 2 + 1, j * 2 + 3, j * 2 + 2);
			const g = G(new THREE.BufferGeometry());
			g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
			g.setAttribute('aS', new THREE.Float32BufferAttribute(aS, 1));
			g.setAttribute('aV', new THREE.Float32BufferAttribute(aV, 1));
			g.setIndex(idx);
			return g;
		}
		const ringMat = lightMat(uW, uB);
		const ringV = nopick(new THREE.Mesh(ringRibbon(true), ringMat));
		const ringH = nopick(new THREE.Mesh(ringRibbon(false), ringMat));
		ringV.renderOrder = ringH.renderOrder = 9;
		const haloMat = glowT('#ff7a7a', '#c03030', 1.2, false, 0.45);
		const halo = nopick(new THREE.Mesh(G(new THREE.TorusGeometry(RB, AMIN * 1.15, 18, 200).rotateX(Math.PI / 2).translate(0, YC, 0)), haloMat));
		halo.renderOrder = 8;
		// ring pick proxy (a sleeve around the rim; the membrane inside it still picks the toroid)
		const ringProxy = new THREE.Mesh(G(new THREE.TorusGeometry(RO - AMIN, AMIN * 1.6, 10, 96).rotateX(Math.PI / 2).translate(0, YC, 0)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		const ringGroup = new THREE.Group();
		ringGroup.add(ringV, ringH, halo, ringProxy);
		root.add(ringGroup);
		ringProxy.userData.light = 'ring';

		// taper ribbons (vertical + horizontal), across = 0.8 of the local fiber radius; aS along x from x0 to x1
		function taperRibbon(x0: number, x1: number) {
			const S = 240;
			const pos: number[] = [];
			const aS: number[] = [];
			const aV: number[] = [];
			const idx: number[] = [];
			for (const vertical of [true, false]) {
				const base = pos.length / 3;
				for (let j = 0; j <= S; j++) {
					const s = j / S;
					const x = lerp(x0, x1, s);
					const r = taperR(x) * 0.8;
					for (let v = 0; v <= 1; v++) {
						const off = (0.5 - v) * 2 * r;
						pos.push(x, vertical ? off : 0, vertical ? 0 : -off);
						aS.push(s);
						aV.push(v);
					}
				}
				for (let j = 0; j < S; j++) {
					const a = base + j * 2;
					idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
				}
			}
			const g = G(new THREE.BufferGeometry());
			g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
			g.setAttribute('aS', new THREE.Float32BufferAttribute(aS, 1));
			g.setAttribute('aV', new THREE.Float32BufferAttribute(aV, 1));
			g.setIndex(idx);
			return g;
		}
		const inMat = lightMat(uWin, uBin);
		const outMat = lightMat(uW, uB);
		const inRib = nopick(new THREE.Mesh(taperRibbon(X_IN, 0), inMat));
		const outRib = nopick(new THREE.Mesh(taperRibbon(0, X_OUT), outMat));
		inRib.renderOrder = outRib.renderOrder = 9;
		inMat.uniforms.uLobes.value = Math.abs(X_IN) / 34;
		outMat.uniforms.uLobes.value = Math.abs(X_OUT) / 34;
		ringMat.uniforms.uLobes.value = 7;
		const inProxy = new THREE.Mesh(G(new THREE.CylinderGeometry(7.5, 7.5, -X_IN, 10, 1, true).rotateZ(Math.PI / 2).translate(X_IN / 2, 0, 0)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		inProxy.userData.light = 'in';
		const outProxy = new THREE.Mesh(G(new THREE.CylinderGeometry(7.5, 7.5, X_OUT, 10, 1, true).rotateZ(Math.PI / 2).translate(X_OUT / 2, 0, 0)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		outProxy.userData.light = 'out';
		const fiberLight = new THREE.Group();
		fiberLight.add(inRib, outRib, inProxy, outProxy);
		root.add(fiberLight);

		// ---------------------------------------------------------------------------- schematic boxes
		const boxGeo = G(new THREE.BoxGeometry(BOX[0], BOX[1], BOX[2]));
		const boxEdgeGeo = G(new THREE.EdgesGeometry(boxGeo));
		const edgeMats: THREE_NS.LineBasicMaterial[] = [];
		function box(id: string, at3: V3) {
			const g = new THREE.Group();
			const m = std(id, { transparent: true, opacity: num(look(id).opacity, 1) * 0.85, envMapIntensity: 0 });
			const em = keep(new THREE.LineBasicMaterial({ color: '#6c717b', transparent: true, opacity: 1 }));
			edgeMats.push(em);
			g.add(new THREE.Mesh(boxGeo, m), nopick(new THREE.LineSegments(boxEdgeGeo, em)));
			g.position.set(at3[0], at3[1], at3[2]);
			const b = body(id, g);
			return { b, em };
		}
		const laser = box('pump_laser', LASER);
		const osa = box('osa', OSA);
		const refc = box('reference_comb', REF);

		// ---------------------------------------------------------------------------- lights (scene)
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.6);
		const key = new THREE.DirectionalLight('#fff3e6', 1.7);
		key.position.set(120, 260, 200);
		const rimL = new THREE.DirectionalLight('#bcd2ff', 1.3);
		rimL.position.set(-260, 120, -220);
		const fill = new THREE.DirectionalLight('#ffffff', 0.5);
		fill.position.set(-100, -60, 240);
		root.add(hemi, key, rimL, fill);

		// ---------------------------------------------------------------------------- state helpers
		const raycaster = new THREE.Raycaster();
		const v2 = new THREE.Vector2();
		const tmp = new THREE.Vector3();
		const tmp2 = new THREE.Vector3();
		const accent = new THREE.Color();
		const black = new THREE.Color(0, 0, 0);

		function setOpacity(b: Body, o: number) {
			const lit = hi.includes(b.id) || (b.id === 'toroid' && hi.includes('silica_disk'));
			const eff = lit && o < 0.3 && o > 0.004 ? 0.3 : o;
			b.o = o;
			b.obj.visible = eff > 0.004;
			for (const x of b.mats) {
				const op = x.base * eff;
				const trans = x.trans || op < 0.999;
				if (x.m.transparent !== trans) {
					x.m.transparent = trans;
					x.m.needsUpdate = true;
				}
				x.m.opacity = op;
			}
		}
		function tint(b: Body, ids: string[]) {
			const lit = ids.some((id) => hi.includes(id));
			for (const x of b.mats) {
				x.m.emissive.copy(lit ? accent : black);
				x.m.emissiveIntensity = lit ? 0.35 : 1;
			}
		}
		const mix3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];

		// ---------------------------------------------------------------------------- camera
		function keyAt(keys: Key[], q: number): Shot {
			if (q <= keys[0].q) return keys[0];
			for (let i = 1; i < keys.length; i++)
				if (q <= keys[i].q) {
					const a = keys[i - 1];
					const b = keys[i];
					const t = ease(seg(q, a.q, b.q));
					return { t: mix3(a.t, b.t, t), az: lerp(a.az, b.az, t), el: lerp(a.el, b.el, t), R: [lerp(a.R[0], b.R[0], t), lerp(a.R[1], b.R[1], t)] };
				}
			return keys[keys.length - 1];
		}
		let shot: Shot & { rect: Rect; region: 'full' | 'plot' } = { ...SHOTS.intro[0], rect: regions(w, h).full, region: 'full' };
		function shotAt(p: number) {
			const R = regions(w, h);
			let i = 0;
			for (let j = 0; j < CHAPTER_IDS.length; j++) if (p >= C[CHAPTER_IDS[j]][0]) i = j;
			const id = CHAPTER_IDS[i];
			const q = cq(id, p);
			const cur = keyAt(SHOTS[id], q);
			const prevId = CHAPTER_IDS[i - 1];
			const plotNow = PLOT_CHAPTERS.has(id);
			const prev = prevId ? SHOTS[prevId][SHOTS[prevId].length - 1] : null;
			const t = prev ? ease(seg(q, 0, plotNow ? 0.22 : id === 'pump' ? 0.2 : 0.4)) : 1;
			const rc = R[plotNow ? 'plot' : 'full'];
			const rp = prevId && PLOT_CHAPTERS.has(prevId) ? R.plot : R.full;
			const s: Shot = prev
				? { t: mix3(prev.t, cur.t, t), az: lerp(prev.az, cur.az, t), el: lerp(prev.el, cur.el, t), R: [lerp(prev.R[0], cur.R[0], t), lerp(prev.R[1], cur.R[1], t)] }
				: { t: [cur.t[0], cur.t[1], cur.t[2]], az: cur.az, el: cur.el, R: [cur.R[0], cur.R[1]] };
			// phones: in the plot strip the taper runs level across the screen (no fiber through the keyword above)
			if (w < 700) {
				const ph = (c: string) => (PLOT_CHAPTERS.has(c) ? 1 : 0);
				const k2 = lerp(prevId ? ph(prevId) : ph(id), ph(id), t);
				s.az = lerp(s.az, 3, k2);
				s.el = lerp(s.el, 20, k2);
			}
			return { ...s, region: (plotNow ? 'plot' : 'full') as 'full' | 'plot', rect: [lerp(rp[0], rc[0], t), lerp(rp[1], rc[1], t), lerp(rp[2], rc[2], t), lerp(rp[3], rc[3], t)] as Rect };
		}
		function applyCamera(s: Shot & { rect: Rect }) {
			const [x0, y0, x1, y1] = s.rect;
			const tf = Math.tan((camera.fov * DEG) / 2);
			const d = Math.max(s.R[0] / (tf * (w / h) * (x1 - x0)), s.R[1] / (tf * (y1 - y0)));
			const az = s.az * DEG;
			const el = s.el * DEG;
			camera.position.set(s.t[0] + d * Math.cos(el) * Math.sin(az), s.t[1] + d * Math.sin(el), s.t[2] + d * Math.cos(el) * Math.cos(az));
			camera.near = Math.max(0.1, d / 200);
			camera.far = d * 20 + 4000;
			camera.updateProjectionMatrix();
			camera.lookAt(s.t[0], s.t[1], s.t[2]);
			camera.setViewOffset(w, h, (0.5 - (x0 + x1) / 2) * w, (0.5 - (y0 + y1) / 2) * h, w, h);
			camera.updateMatrixWorld();
		}
		const pv = new THREE.Vector3();
		/** largest x on the taper line whose screen point stays left of pane x `xmax` (bisection; the taper runs +x) */
		function clipX(xmax: number, z: number): number {
			const sx = (x: number) => {
				pv.set(x, TAPER[1], z).project(camera);
				return ((pv.x + 1) / 2) * w;
			};
			if (sx(X_OUT + BOX[0]) <= xmax) return 1e9;
			if (sx(0) > xmax) return 0;
			let lo = 0;
			let hi2 = X_OUT + BOX[0];
			for (let i = 0; i < 18; i++) {
				const m = (lo + hi2) / 2;
				if (sx(m) <= xmax) lo = m;
				else hi2 = m;
			}
			return lo;
		}

		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			for (const g of glows) {
				g.m.uniforms.uColor.value.set(light ? g.light : g.dark);
				g.m.uniforms.uLight.value = light ? 1 : 0;
				g.m.uniforms.uK.value = light ? g.lightK : 1;
				g.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			for (const m of lights) {
				m.uniforms.uLight.value = light ? 1 : 0;
				m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			for (const em of edgeMats) em.color.set(light ? '#8d9098' : '#6c717b');
			hazeMat.color.set(light ? '#8a8aa0' : look('xef2_gas').color || '#d8d8e6');
			hemi.intensity = light ? 0.9 : 0.6;
			// floor and oxide film: dim on the dark page (no lit backdrop), light on the light page (no dark blot)
			chipMat.color.copy(chipBase).multiplyScalar(light ? 1.1 : 0.45);
			oxMat.color.copy(oxBase).multiplyScalar(light ? 1 : 0.5);
			fillColours();
		}
		applyTheme();

		// ---------------------------------------------------------------------------- frame state (for pick / anchor)
		let lightState: 'none' | 'pump' | 'fwm' | 'comb' = 'none';
		let silId: 'toroid' | 'silica_disk' = 'toroid';
		let litOn = 0;
		let inFront = 0;

		function frame(p: number) {
			const kk = clamp01(k);
			shot = shotAt(p);
			applyCamera(shot);
			const inPlot = PLOT_CHAPTERS.has(CHAPTER_IDS.reduce((acc, id) => (p >= C[id][0] ? id : acc), 'intro'));

			// ---- intro: the finished device, then everything fades back to the bare chip
			const iq = cq('intro', p);
			const back = p < C.oxide[0] ? ease(seg(iq, 0.68, 0.97)) : 1; // 0 = finished device, 1 = bare chip
			const inIntro = p < C.oxide[0];

			// ---- etch (undercut) and reflow progress
			let e: number;
			if (inIntro) e = 1 - back;
			else if (!after('undercut', p)) e = 0;
			else e = ease(seg(cq('undercut', p), 0.12, 0.86));
			let s: number;
			if (inIntro) s = 1;
			else if (!after('reflow', p)) s = 0;
			else s = easeOut(seg(cq('reflow', p), 0.16, 0.84));

			// ---- chip and pillar
			const yf = setPillar(Math.max(1e-4, e));
			chip.obj.scale.set(1, yf + DEPTH, 1);
			chip.obj.position.set(0, -DEPTH, 0);
			setOpacity(chip, 1);
			setOpacity(pillar, inIntro ? 1 - back : e > 0.004 ? 1 : 0);

			// ---- oxide chapter: film grows, resist pad lands, HF etch removes the film outside the disk, pad lifts off
			const oq = cq('oxide', p);
			const inOx = after('oxide', p) && !after('undercut', p);
			const grow = ease(seg(oq, 0.02, 0.24));
			const etchHF = ease(seg(oq, 0.46, 0.74));
			const filmT = inOx ? OX_T * grow * (1 - etchHF) : 0;
			oxide.obj.scale.set(1, Math.max(0.001, filmT), 1);
			oxide.obj.position.set(0, Y_OX0, 0);
			setOpacity(oxide, inOx && filmT > 0.01 ? 1 : 0);
			{
				const land = ease(seg(oq, 0.22, 0.44));
				const lift = ease(seg(oq, 0.78, 0.96));
				const y = Y_OX0 + (inOx ? lerp(OX_T * grow, OX_T, 1) : OX_T) + 40 * (1 - land) + 30 * lift;
				pad.obj.position.set(0, y, 0);
				setOpacity(pad, inOx ? easeOut(seg(oq, 0.22, 0.34)) * (1 - seg(oq, 0.8, 0.96)) : 0);
			}

			// ---- silica (disk, then toroid)
			setSilica(s);
			const silVis = inIntro ? 1 - back : inOx ? (oq >= 0.46 ? 1 : 0) : after('undercut', p) ? 1 : 0;
			silId = !inIntro && !after('toroid', p) ? 'silica_disk' : 'toroid';
			for (const m of sil.picks) m.userData.part = silId;
			sil.obj.position.set(0, kk * 34, 0);
			setOpacity(sil, silVis);
			silEdgeMat.uniforms.uI.value = 0.55 * silVis * (hi.includes(silId) ? 2.2 : 1);
			silEdgeMat.uniforms.uColor.value.copy(hi.includes(silId) ? accent : tmpC.set(theme === 'light' ? '#7d8796' : '#dfeaf6'));

			// ---- XeF2 haze
			const uq = cq('undercut', p);
			const hz = after('undercut', p) && !after('reflow', p) ? easeOut(seg(uq, 0, 0.14)) * (1 - seg(uq, 0.86, 1)) : 0;
			setHaze(p);
			hazeMat.opacity = num(look('xef2_gas').opacity, 0.18) * 3.2 * hz;
			gas.o = hz;
			gas.obj.visible = hz > 0.004;

			// ---- CO2 beam and the molten edge
			const rq = cq('reflow', p);
			const inRe = after('reflow', p) && !after('toroid', p);
			const bOn = inRe ? easeOut(seg(rq, 0.02, 0.14)) * (1 - seg(rq, 0.86, 0.97)) : 0;
			beamMat.uniforms.uI.value = 0.42 * bOn * (hi.includes('co2_beam') ? 1.6 : 1);
			beam.o = bOn;
			beam.obj.visible = bOn > 0.004;
			const heat = inRe ? Math.sin(Math.PI * seg(rq, 0.12, 0.9)) : 0;
			melt.visible = heat > 0.004 && silVis > 0.5;
			meltMat.uniforms.uR0.value = rimRc - rimA * 1.2;
			meltMat.uniforms.uI.value = 0.9 * heat;

			// ---- taper: slides in beside the rim (in its plane) in its chapter
			const tq = cq('taper', p);
			let tapO: number;
			let tz: number;
			if (inIntro) {
				tapO = 1 - back;
				tz = TAPER[2];
			} else if (!after('taper', p)) {
				tapO = 0;
				tz = TAPER[2] - 220;
			} else {
				const slide = ease(seg(tq, 0.04, 0.82));
				tapO = easeOut(seg(tq, 0.02, 0.2));
				tz = lerp(TAPER[2] - 220, TAPER[2], slide);
			}
			tz -= kk * 40;
			taper.obj.position.set(0, TAPER[1], tz);
			setOpacity(taper, tapO);
			tapEdgeMat.uniforms.uI.value = 0.7 * tapO * (hi.includes('taper') ? 2 : 1);
			tapEdgeMat.uniforms.uColor.value.copy(hi.includes('taper') ? accent : tmpC.set(theme === 'light' ? '#7d8796' : '#e6eef5'));
			fiberLight.position.set(0, TAPER[1], tz);

			// ---- boxes (schematic)
			const pq = cq('pump', p);
			setOpacity(laser.b, after('pump', p) ? easeOut(seg(pq, 0, 0.14)) : 0);
			setOpacity(osa.b, after('comb', p) ? easeOut(seg(cq('comb', p), 0, 0.2)) : 0);
			setOpacity(refc.b, after('spacing', p) ? easeOut(seg(cq('spacing', p), 0.1, 0.4)) : 0);
			for (const x of [laser, osa, refc]) x.em.opacity = x.b.o;

			// ---- light: pump, then the first sideband pair, then the cascade (plot pen)
			const fq = cq('fwm', p);
			const pumpIn = after('pump', p) ? seg(pq, 0.08, 0.4) : 0; // front from the laser to the coupling point
			// the rim lights only once the front has reached the coupling point (pq 0.40)
			const ringFill = after('pump', p) ? ease(seg(pq, 0.4, 0.64)) : 0; // light builds round the rim from the taper
			const outFront = after('pump', p) ? seg(pq, 0.42, 0.8) : 0; // transmitted light runs on toward the output
			const pair = after('fwm', p) ? ease(seg(fq, 0.16, 0.6)) : 0;
			const pen = after('comb', p) ? penAt(p) : 0;
			const lightK = 1 - kk;
			uW.fill(0);
			uB.fill(0);
			uWin.fill(0);
			uBin.fill(0);
			const sP = slotOf[0];
			uW[sP] = baseW[sP] * (ringFill > 0 ? 1 : 0);
			uB[sP] = baseB[sP];
			uWin[sP] = 1;
			uBin[sP] = baseB[sP];
			for (let i = 1; i < NL; i++) {
				const sl = slotOf[i];
				// the plot draws whole stems only (stem i shows once the pen count reaches i + 1): a line lights no
				// earlier than its stem, then ramps in over a third of the next stem
				const lit = clamp01((pen - (i + 1)) * 3);
				const a = i <= 2 ? Math.max(pair, lit) : lit;
				uW[sl] = baseW[sl] * a;
				uB[sl] = baseB[sl] * (0.4 + 0.6 * a);
			}
			let nLit = 0;
			for (let i = 1; i < NL; i++) if (uW[slotOf[i]] > 1e-3) nLit++;
			lightState = !after('pump', p) || pumpIn <= 0 ? 'none' : after('comb', p) ? 'comb' : nLit > 0 ? 'fwm' : 'pump';
			litOn = lightK;
			inFront = pumpIn;
			const phase = p * 70;
			const stripes = clamp01(1 - (nLit - 8) / 30); // stripes blend into a band once many lines are on

			inMat.uniforms.uS0.value = 0;
			inMat.uniforms.uS1.value = pumpIn * 1.02;
			inMat.uniforms.uPhase.value = phase;
			inMat.uniforms.uK.value = 1.15 * lightK * (pumpIn > 0 ? 1 : 0);
			if (pumpIn <= 0) inMat.uniforms.uS1.value = -1;
			inRib.visible = true; // always submitted (shader compiled up front); the window / uK hide it

			ringMat.uniforms.uS0.value = 0;
			ringMat.uniforms.uS1.value = ringFill >= 1 ? 1.1 : ringFill > 0 ? ringFill : -1;
			ringMat.uniforms.uFeather.value = ringFill >= 1 ? 0.0001 : 0.05;
			ringMat.uniforms.uPhase.value = phase;
			ringMat.uniforms.uStripe.value = stripes;
			ringMat.uniforms.uK.value = 1.25 * lightK * (0.6 + 0.4 * ringFill);
			ringV.visible = ringH.visible = true;
			ringGroup.position.set(0, kk * 34, 0);
			const hk = ringFill * lightK;
			haloMat.uniforms.uI.value = 0.32 * hk * (nLit > 0 ? 1.15 : 1) * (hi.includes(lightState === 'none' ? '' : lightPart()) ? 1.8 : 1);
			halo.visible = hk > 0.004;
			{
				// halo colour: the pump red blended toward the sidebands as lines appear
				const pal = COL[theme];
				const mixT = clamp01(nLit / 12);
				tmpC.set(pal.pump).lerp(new THREE.Color(pal.blue).lerp(new THREE.Color(pal.pink), 0.5), 0.55 * mixT);
				haloMat.uniforms.uColor.value.copy(tmpC);
			}

			// output light ends before the plot panel (plot chapters) and inside the pane
			const R = regions(w, h);
			const paneClip = clipX(w - 24, tz);
			const plotClip = w >= 700 ? clipX(R.plotBox[0] * w - 24, tz) : paneClip;
			const xClip = inPlot ? Math.min(paneClip, plotClip) : paneClip;
			outMat.uniforms.uS0.value = 0;
			outMat.uniforms.uS1.value = outFront > 0 ? outFront * 1.02 : -1;
			outMat.uniforms.uPhase.value = phase;
			outMat.uniforms.uStripe.value = stripes;
			outMat.uniforms.uXMax.value = xClip;
			outMat.uniforms.uK.value = 1.15 * lightK;
			outRib.visible = true;
			tapClip.value = inPlot && w >= 700 ? Math.max(plotClip, 40) : 1e9;
			tapEdgeMat.uniforms.uXMax.value = tapClip.value;
			// output box hidden when it would sit under the plot panel
			if (inPlot && w >= 700 && tapClip.value < X_OUT) {
				setOpacity(osa.b, 0);
				setOpacity(refc.b, 0);
				osa.em.opacity = refc.em.opacity = 0;
			}

			// ---- emphasis
			tint(chip, ['si_chip']);
			tint(pillar, ['si_pillar']);
			tint(oxide, ['oxide_film']);
			tint(pad, ['resist_pad']);
			tint(sil, [silId]);
			tint(taper, ['taper']);
			tint(laser.b, ['pump_laser']);
			tint(osa.b, ['osa']);
			tint(refc.b, ['reference_comb']);
			hazeMat.size = hi.includes('xef2_gas') ? 3.2 : 2.2;
		}
		/** the part the light currently stands for */
		const lightPart = (): string => (lightState === 'fwm' ? 'sidebands' : lightState === 'comb' ? 'comb_light' : 'pump_light');

		// ---------------------------------------------------------------------------- hover texts (illustrative choices)
		const COLOUR = 'Colour illustrative: 1.55 µm light is infrared.';
		const STRIPES = 'Drawn as stripes ordered by wavelength so each line shows; the generated modes belong to the same mode family (US 7,982,944 col. 6:20-24). Brightness follows each line\'s digitized power (dB).';
		const info = (id: string, detail: string[]): PickInfo => ({ id, label: partOf(id)?.name ?? id, detail });
		function lightInfo(where: 'in' | 'ring' | 'out'): PickInfo {
			if (where === 'in' || lightState === 'pump') return info('pump_light', [COLOUR, 'Runs along the taper toward the output; in the rim it circulates the same way as the taper light at the coupling point.']);
			if (lightState === 'fwm') return info('sidebands', ['Signal and idler, symmetric about the pump (blue: higher frequency, pink: lower, after Fig. 1B).', COLOUR, STRIPES]);
			return info('comb_light', ['Lines light up as the plot draws them, pump outward: the four-wave-mixing cascade, not a measured time order.', STRIPES, COLOUR]);
		}
		const DETAIL: Record<string, string[]> = {
			silica_disk: ['Drawn 100 µm across (assumed: 75 µm x 160 / 120, the pad size of Armani et al., Nature 2003 over its example toroid; that paper does not link the two). The comb paper gives no disk size.'],
			toroid: ['75 µm drawn as the outer diameter; rim about 5 µm from the Fig. 1C SEM sample.'],
			si_pillar: ['Final profile read from the Fig. 1C SEM (not the comb device); intermediate shapes during the etch are illustrative.'],
			xef2_gas: ['Haze illustrative; values are those of Armani et al., Nature 2003.'],
			co2_beam: ['Colour illustrative: 10.6 µm is infrared. Spot centring assumed.'],
			taper: ['Waist 3 µm and gap 0.3 µm drawn (assumed, within the ranges of Armani et al., Nature 2003); the widening beyond the waist is not to scale.'],
			resist_pad: ['Drawn 100 µm (assumed); the cited process gives 160 µm pads, and its Fig. 2 example toroid is 120 µm.'],
			pump_laser: ['Schematic box, not to scale.'],
			osa: ['Schematic box, not to scale.'],
			reference_comb: ['Schematic box, not to scale; placed beside the output box.']
		};

		// ---------------------------------------------------------------------------- handle
		const handle: ShowcaseHandle = {
			assembledAt: C.spacing[0],
			// the shared room environment would wash the matte silicon floor into a grey haze (three r186 ignores
			// material.envMapIntensity for scene.environment): keep it faint for this story; glass keeps soft reflections
			environmentIntensity: 0.12,
			frame,
			highlight(ids) {
				hi = [...ids];
			},
			pick(x, y) {
				v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
				raycaster.setFromCamera(v2, camera);
				const cands: THREE_NS.Object3D[] = [];
				for (const b of bodies.values()) if (b.obj.visible && b.o > 0.2 && b.id !== 'xef2_gas') cands.push(...b.picks);
				const lightOn = lightState !== 'none' && litOn > 0.2;
				if (lightOn) {
					if (ringMat.uniforms.uS1.value > 0) cands.push(ringProxy);
					if (inFront > 0) cands.push(inProxy);
					if (outMat.uniforms.uS1.value > 0) cands.push(outProxy);
				}
				const hits = raycaster.intersectObjects(cands, false);
				// light first (it sits inside the glass), then the nearest body
				const lh = hits.find((q) => q.object.userData.light);
				if (lh) {
					const where = lh.object.userData.light as 'in' | 'ring' | 'out';
					if (where === 'out' && lh.point.x > outMat.uniforms.uXMax.value) return null;
					return lightInfo(where);
				}
				const hit = hits[0];
				let id = (hit?.object.userData.part as string | undefined) ?? null;
				if (hit && id === 'taper' && hit.point.x > tapClip.value) id = null;
				if (!id && gas.obj.visible && gas.o > 0.2 && raycaster.intersectObject(hazeProxy, false).length) id = 'xef2_gas';
				if (!id) return null;
				return DETAIL[id] ? info(id, DETAIL[id]) : id;
			},
			anchor(id) {
				if (id === 'toroid') {
					if (!sil.obj.visible || sil.o < 0.5 || silId !== 'toroid') return null;
					tmp.set(RO * Math.cos(20 * DEG), YC + AMIN + sil.obj.position.y, RO * Math.sin(20 * DEG));
				} else if (id === 'pump_light') {
					if (lightState === 'none' || inFront <= 0 || litOn < 0.5) return null;
					tmp.set(lerp(X_IN, 0, Math.max(0.15, Math.min(0.85, inFront * 0.55))), TAPER[1] + WAIST_R, taper.obj.position.z);
				} else return null;
				camera.updateMatrixWorld();
				tmp2.copy(tmp).applyMatrix4(camera.matrixWorldInverse);
				if (tmp2.z > -camera.near) return null;
				tmp.project(camera);
				const sx = ((tmp.x + 1) / 2) * w;
				const sy = ((1 - tmp.y) / 2) * h;
				if (sx < 4 || sx > w - 4 || sy < 4 || sy > h - 4) {
					if (id !== 'pump_light') return null;
					// pump label: pick the first on-screen point along the lit input fiber
					for (let f = 0.9; f >= 0.1; f -= 0.1) {
						tmp.set(lerp(X_IN, 0, f * Math.max(0.2, inFront)), TAPER[1] + WAIST_R, taper.obj.position.z).project(camera);
						const ax = ((tmp.x + 1) / 2) * w;
						const ay = ((1 - tmp.y) / 2) * h;
						if (ax > 8 && ax < w - 8 && ay > 8 && ay < h - 8) return [ax, ay];
					}
					return null;
				}
				return [sx, sy];
			},
			target() {
				return [shot.t[0], shot.t[1], shot.t[2]];
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
				for (const d of disposables) d.dispose();
			}
		};
		return handle;
	}
};
export default mod;
