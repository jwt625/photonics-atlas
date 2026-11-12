// Scene module: erbium-doped fibre amplifier, Mears, Reekie, Jauncey, Payne, Electron. Lett. 1987 (DevLog-017).
// Spec: data/history/showcases/mears1987.yaml. Contract: ../showcase/types.ts.
//
// Layout = the paper's Fig. 1 laid on the table: +x = Fig. 1 right (signal direction), +z = Fig. 1 down (toward the
// viewer), +y = up; units = Fig. 1 scan px / 4 (schematic, not to scale). Positions and sizes come from the spec
// (assembly, parts[].geometry); the coupler and the butt-splice are text-only parts (not in Fig. 1), drawn as plain
// stand-ins in the text's order. Bulk dichroic beam-splitter, backward CW dye pump, no WDM coupler, no isolator.
//
// Light (all pure in p): the signal front runs diode -> fibre end (signal), -> splice (launch), waits while the doped
// fibre is laid (fibre) and pumped (pump), then grows through the pumped fibre to the plate (gain) and reflects to the
// detector (detect). Signal colour is illustrative (1.54 um is infrared); growth along the fibre and pump fading are
// illustrative (not printed). Plot chapters: the model state is the point under the plot pen (D1006):
//   Fig. 2: pump power = the curve being drawn (newest pen), pump tone = pen wavelength, output = pen gain;
//   derived alternate: the last revealed point (power, gain); Fig. 3: last revealed circle (input, output power);
//   Fig. 4: last revealed measured point (gain). The pen holds at its last point; nothing sweeps past the data.
// Brightness is linear in dB (0.6 per 28 dB) for the signal and linear in absorbed pump power for the fibre glow.
import type * as T from 'three';
import { AXES_END, stagger, staggerK } from '../showcase/plot';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type Three = typeof T;
type V3 = [number, number, number];
type Rect = [number, number, number, number]; // pane fractions x0, y0, x1, y1
type Geo = Record<string, unknown>;

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);

// ------------------------------------------------------------------------------------------------ shots (camera)
interface Shot {
	t: V3;
	az: number;
	el: number;
	R: [number, number];
	drift: number;
	region: 'full' | 'plot';
}
const PLOT_SHOT = { t: [54, 0, 6] as V3, el: 50, R: [166, 42] as [number, number], drift: 3, region: 'plot' as const };
const SHOTS: Record<string, Shot> = {
	intro: { t: [50, 14, 4], az: -12, el: 30, R: [168, 56], drift: 18, region: 'full' },
	signal: { t: [-36, 0, -1], az: -6, el: 30, R: [62, 26], drift: 8, region: 'full' },
	launch: { t: [19, 0, 2], az: 8, el: 34, R: [30, 15], drift: 8, region: 'full' },
	fibre: { t: [52, 0, -12], az: 4, el: 54, R: [40, 28], drift: 8, region: 'full' },
	pump: { t: [115, 0, -2], az: -6, el: 40, R: [92, 34], drift: 6, region: 'full' },
	gain: { t: [84, 0, -4], az: 4, el: 46, R: [126, 40], drift: 6, region: 'full' },
	detect: { t: [138, 0, 14], az: -8, el: 50, R: [76, 38], drift: 6, region: 'full' },
	pump_curve: { ...PLOT_SHOT, az: 10 },
	transfer: { ...PLOT_SHOT, az: 8 },
	spectrum: { ...PLOT_SHOT, az: 10 }
};
const PHONE_AZ: Record<string, number> = { intro: 30, signal: 22, pump: 22, gain: 14, detect: 10 };
const CHAPTER_IDS = ['intro', 'signal', 'launch', 'fibre', 'pump', 'gain', 'detect', 'pump_curve', 'transfer', 'spectrum'];
const FALLBACK: Record<string, [number, number]> = {
	intro: [0, 0.08], signal: [0.08, 0.18], launch: [0.18, 0.28], fibre: [0.28, 0.38], pump: [0.38, 0.5],
	gain: [0.5, 0.62], detect: [0.62, 0.7], pump_curve: [0.7, 0.8], transfer: [0.8, 0.9], spectrum: [0.9, 1]
};

function regions(w: number, h: number): { full: Rect; plot: Rect; plotBox: Rect } {
	if (w < 700) return { full: [0.04, 0.2, 0.96, 0.98], plot: [0.04, 0.17, 0.96, 0.43], plotBox: [0, 0.44, 1, 1] };
	const top = Math.min(0.24, 150 / Math.max(1, h));
	return { full: [0.03, top, 0.97, 0.97], plot: [0.03, top, 0.49, 0.97], plotBox: [0.5, 0.16, 1, 1] };
}

// ------------------------------------------------------------------------------------------------ shaders
// One vertex shader for beams (along = uv.y of the unit cone) and fibre glow tubes (along = uv.x of TubeGeometry).
const VS = /* glsl */ `
uniform float uAlongX;
varying vec3 vN; varying vec3 vV; varying float vS;
void main() {
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	vN = normalize(normalMatrix * normal);
	vV = normalize(-mv.xyz);
	vS = uAlongX > 0.5 ? uv.x : uv.y;
	gl_Position = projectionMatrix * mv;
}`;
// free-space beam: intensity uI0 -> uI1 along the segment, drawn for s < uFront
const BEAM_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI0; uniform float uI1; uniform float uFront; uniform float uPow; uniform float uLight; uniform float uK;
varying vec3 vN; varying vec3 vV; varying float vS;
void main() {
	float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
	float f = pow(c, uPow);
	float m = 1.0 - smoothstep(uFront - 0.02, uFront, vS);
	float a = clamp(f * mix(uI0, uI1, vS) * m * uK, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a) : vec4(uColor * a, a);
}`;
// light inside a fibre: signal (linear ramp, front from s = 0) plus counter-running pump (enters at s = 1, decays
// toward s = 0, front from s = 1)
const FIBRE_FS = /* glsl */ `
uniform vec3 uSigC; uniform vec3 uPumpC;
uniform float uSig0; uniform float uSig1; uniform float uSigF;
uniform float uPump; uniform float uPumpAtt; uniform float uPumpF;
uniform float uPow; uniform float uLight; uniform float uK;
varying vec3 vN; varying vec3 vV; varying float vS;
void main() {
	float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
	float f = pow(c, uPow);
	float is = mix(uSig0, uSig1, vS) * (1.0 - smoothstep(uSigF - 0.012, uSigF, vS));
	float ip = uPump * exp(-uPumpAtt * (1.0 - vS)) * smoothstep(uPumpF, uPumpF + 0.012, vS);
	float tot = is + ip;
	// alpha follows the light (a transparent canvas: alpha 1 with black would paint the page black)
	vec3 col = (uSigC * is + uPumpC * ip) / max(tot, 1e-4);
	gl_FragColor = vec4(col, clamp(f * tot * uK, 0.0, 1.0));
}`;
// fresnel rim for glass (lenses, cell, plate): makes clear parts read on a dark page
const RIM_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uPow; uniform float uLight;
varying vec3 vN; varying vec3 vV; varying float vS;
void main() {
	float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
	float a = clamp(pow(1.0 - c, uPow) * uI, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a) : vec4(uColor * a, a);
}`;

// ------------------------------------------------------------------------------------------------ light levels
/** signal brightness: linear in dB, 0.6 per 28 dB (the stated maximum gain) above the input level */
const B_IN = 0.35;
const DB = 0.6 / 28;
const bGain = (g: number) => B_IN + DB * Math.max(0, g);
/** Fig. 3 powers (dBm) on the same dB slope, anchored so the largest printed output (+8.64 dBm) reads 0.95 */
const bDbm = (pdbm: number) => Math.max(0.05, 0.95 + DB * (pdbm - 8.64));
/** fibre glow from absorbed pump power (mW), relative to 100 mW; pump on with the power not stated: P_ON */
const gPump = (mw: number) => 0.25 + 0.75 * clamp01(mw / 100);
const P_ON = 0.85;
const LAM_ON = 670; // drawn pump tone where the run's wavelength is not stated (the beam-splitter spec wavelength)
const PUMP_ATT = 3; // illustrative decay of the pump glow along the fibre (no absorption profile printed)

interface LightState {
	bIn: number;
	bOut: number;
	pump: number;
	lam: number;
}
const mixState = (a: LightState, b: LightState, t: number): LightState => ({
	bIn: lerp(a.bIn, b.bIn, t),
	bOut: lerp(a.bOut, b.bOut, t),
	pump: lerp(a.pump, b.pump, t),
	lam: lerp(a.lam, b.lam, t)
});

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('mears1987 is a 3D scene');
		const { THREE, scene, camera, spec } = ctx;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let k = 0;
		let theme: Theme = ctx.theme;
		let hi: string[] = [];
		let lastP = 0;
		/** plot on screen, from handle.plot (null = none; main Fig. 2 until told otherwise) */
		let shownPlot: string | null = null;

		const partOf = (id: string) => spec.parts.find((q) => q.id === id);
		const geo = (id: string): Geo => (partOf(id)?.geometry ?? {}) as Geo;
		const look = (id: string) => partOf(id)?.look ?? {};
		const at = (id: string, d: V3): V3 => {
			const pos = spec.assembly?.find((a) => a.part === id)?.pos;
			return Array.isArray(pos) && pos.length === 3 && pos.every((v) => Number.isFinite(v)) ? [pos[0], pos[1], pos[2]] : d;
		};
		const C = Object.fromEntries(
			CHAPTER_IDS.map((id) => [id, (spec.chapters.find((c) => c.id === id)?.p ?? FALLBACK[id]) as [number, number]])
		) as Record<string, [number, number]>;
		const cq = (id: string, p: number) => seg(p, C[id][0], C[id][1]);
		const inCh = (id: string, p: number) => p >= C[id][0] && (p < C[id][1] || (id === 'spectrum' && p <= C[id][1]));

		// ---------------------------------------------------------------------------- layout (spec, schematic units)
		const sizeOf = (id: string, d: V3): V3 => {
			const s = geo(id).size;
			return Array.isArray(s) && s.length === 3 ? [num(s[0], d[0]), num(s[1], d[1]), num(s[2], d[2])] : d;
		};
		const P = {
			diode: at('laser_diode', [-92.5, 0, 0]),
			lens1: at('lens_launch_1', [-67, 0, 0]),
			filter: at('density_filter', [-35.5, 0, -1.9]),
			lens2: at('lens_launch_2', [-26.25, 0, 0]),
			cell: at('index_cell', [9.4, 0, 0]),
			coupler: at('fibre_coupler', [25, 0, 0]),
			splice: at('butt_splice', [36, 0, 0]),
			loop: at('doped_fibre', [45, 0, -16.25]),
			lensOut: at('lens_output', [94.5, 0, 0]),
			plate: at('beam_splitter', [130, 0, 0]),
			lensDet: at('lens_detector', [98.75, 0, 27.5]),
			det: at('detector', [85, 0, 42.5]),
			dye: at('dye_laser', [182.5, 0, -1.25])
		};
		const diodeS = sizeOf('laser_diode', [8, 8, 8]);
		const cellS = sizeOf('index_cell', [16, 6, 6]);
		const coupS = sizeOf('fibre_coupler', [8, 3, 4]);
		const dyeS = sizeOf('dye_laser', [42.5, 14, 30]);
		const plateS = sizeOf('beam_splitter', [26, 14, 1]);
		const lensD = num(geo('lens_launch_1').diameter, 10);
		const lensT = num(geo('lens_launch_1').thickness, 2);
		const fG = geo('density_filter');
		const spG = geo('butt_splice');
		const dfG = geo('doped_fibre');
		const loopR = num(dfG.loop_radius, 16.25);
		const fibR = num(dfG.fibre_diameter, 0.8) / 2;
		const DF0 = num(dfG.from_x, 37); // butt joint (inside the splice sleeve)
		const DF1 = num(dfG.to_x, 75); // doped fibre output end
		const FX0 = P.cell[0] - cellS[0] / 2; // input fibre end, left end of the index-matching cell (Fig. 1)
		const FOCUS_X = -45.75; // intermediate focus drawn in Fig. 1 (spec assembly locator of lens_launch_1)
		const tilt = num(geo('beam_splitter').tilt_deg_from_x, 67) * DEG;
		const det = geo('detector');
		const detR = num(det.diameter, 6) / 2;
		const detL = num(det.length, 5);
		const stub = (geo('fibre_coupler').monitor_stub ?? {}) as Geo;
		const BEAM_R = 3.75; // collimated beam in Fig. 1: px 330-360 = 7.5 units wide (schematic)
		const dirDet = new THREE.Vector3(P.det[0] - P.lensDet[0], 0, P.det[2] - P.lensDet[2]).normalize();
		const dirRefl = new THREE.Vector3(P.lensDet[0] - P.plate[0], 0, P.lensDet[2] - P.plate[2]).normalize();
		const detFront: V3 = [P.det[0] - (dirDet.x * detL) / 2, 0, P.det[2] - (dirDet.z * detL) / 2];
		const dyeFace: V3 = [P.dye[0] - dyeS[0] / 2, 0, 0];
		const diodeFace: V3 = [P.diode[0] + diodeS[0] / 2, 0, 0];

		// explode / intro float heights per body
		const YE: Record<string, number> = {
			laser_diode: 22, lens_launch_1: 30, density_filter: 38, lens_launch_2: 30, index_cell: 24, input_fibre: 14,
			fibre_coupler: 32, butt_splice: 26, doped_fibre: 10, lens_output: 30, beam_splitter: 38, lens_detector: 28,
			detector: 22, dye_laser: 18
		};
		const ARRIVE: Record<string, string> = {
			laser_diode: 'signal', lens_launch_1: 'signal', density_filter: 'signal', lens_launch_2: 'signal',
			index_cell: 'launch', input_fibre: 'launch', fibre_coupler: 'launch', butt_splice: 'launch',
			doped_fibre: 'fibre', dye_laser: 'pump', beam_splitter: 'pump', lens_output: 'pump',
			lens_detector: 'detect', detector: 'detect'
		};

		// ---------------------------------------------------------------------------- materials
		const disposables: { dispose(): void }[] = [];
		const keep = <X extends { dispose(): void }>(x: X): X => (disposables.push(x), x);
		const G = <X extends T.BufferGeometry>(g: X): X => keep(g);
		const nopick = <X extends T.Object3D>(o: X): X => ((o.userData.nopick = true), o);
		const root = new THREE.Group();
		scene.add(root);

		interface Body {
			id: string;
			obj: T.Object3D;
			mats: { m: T.MeshStandardMaterial; base: number; trans: boolean }[];
			picks: T.Mesh[];
			o: number;
		}
		const bodies = new Map<string, Body>();
		function body(id: string, obj: T.Object3D): Body {
			const b: Body = { id, obj, mats: [], picks: [], o: 1 };
			obj.traverse((n) => {
				const mesh = n as T.Mesh;
				const m = mesh.material as T.MeshStandardMaterial | undefined;
				if (mesh.isMesh && m && 'emissive' in m && !b.mats.some((x) => x.m === m)) b.mats.push({ m, base: m.opacity, trans: m.transparent });
				if (mesh.isMesh && !n.userData.nopick) {
					n.userData.part = id;
					b.picks.push(mesh);
				}
			});
			root.add(obj);
			bodies.set(id, b);
			return b;
		}
		const std = (id: string, extra: Partial<T.MeshPhysicalMaterialParameters> = {}) => {
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
		const glows: { m: T.ShaderMaterial; dark: string; light: string; lightK: number }[] = [];
		const shader = (fs: string, uniforms: Record<string, { value: unknown }>, along: boolean) =>
			keep(
				new THREE.ShaderMaterial({
					uniforms: { ...uniforms, uAlongX: { value: along ? 1 : 0 }, uLight: { value: 0 } },
					vertexShader: VS,
					fragmentShader: fs,
					transparent: true,
					depthWrite: false,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
		const rimMat = (dark: string, light: string, pow: number, I: number) => {
			const m = shader(RIM_FS, { uColor: { value: new THREE.Color(dark) }, uI: { value: I }, uPow: { value: pow } }, false);
			glows.push({ m, dark, light, lightK: 1 });
			return m;
		};
		const edgeMats: T.LineBasicMaterial[] = [];
		const edges = (g: T.BufferGeometry) => {
			const m = keep(new THREE.LineBasicMaterial({ color: '#7a7f88', transparent: true, opacity: 0.9 }));
			edgeMats.push(m);
			return nopick(new THREE.LineSegments(G(new THREE.EdgesGeometry(g)), m));
		};
		const place = (o: T.Object3D, v: V3) => o.position.set(v[0], v[1], v[2]);
		const xAxis = new THREE.Vector3(1, 0, 0);
		const orientX = (o: T.Object3D, dir: T.Vector3) => o.quaternion.setFromUnitVectors(xAxis, dir.clone().normalize());

		// ---------------------------------------------------------------------------- stand-ins (spec geometry)
		function boxBody(id: string, s: V3, extra: Partial<T.MeshPhysicalMaterialParameters> = {}) {
			const g = G(new THREE.BoxGeometry(s[0], s[1], s[2]));
			const grp = new THREE.Group();
			grp.add(new THREE.Mesh(g, std(id, extra)), edges(g));
			return body(id, grp);
		}
		const diode = boxBody('laser_diode', diodeS, { envMapIntensity: 0.8 });
		const dye = boxBody('dye_laser', dyeS, { envMapIntensity: 0.6 });
		const coupler = (() => {
			const g = G(new THREE.BoxGeometry(coupS[0], coupS[1], coupS[2]));
			const grp = new THREE.Group();
			grp.add(new THREE.Mesh(g, std('fibre_coupler')), edges(g));
			// monitor port: a short open stub (destination not stated)
			const len = num(stub.length, 8);
			const sg = G(new THREE.CylinderGeometry(fibR, fibR, len, 12).translate(0, len / 2, 0).rotateX(Math.PI / 2));
			const s = new THREE.Mesh(sg, std('fibre_coupler', { color: '#d9dee3', metalness: 0, roughness: 0.35 }));
			s.position.set(0, 0, coupS[2] / 2);
			grp.add(s);
			return body('fibre_coupler', grp);
		})();
		const splice = (() => {
			const L = num(spG.length, 3);
			const r = num(spG.diameter, 2.5) / 2;
			const g = G(new THREE.CylinderGeometry(r, r, L, 32).rotateZ(Math.PI / 2));
			const grp = new THREE.Group();
			grp.add(new THREE.Mesh(g, std('butt_splice', { depthWrite: false })));
			const rim = nopick(new THREE.Mesh(g, rimMat('#f0dc96', '#8a7426', 2.0, 0.8)));
			rim.renderOrder = 4;
			grp.add(rim);
			return body('butt_splice', grp);
		})();
		const cell = (() => {
			const g = G(new THREE.BoxGeometry(cellS[0], cellS[1], cellS[2]));
			const grp = new THREE.Group();
			const m = new THREE.Mesh(g, std('index_cell', { depthWrite: false }));
			m.renderOrder = 3;
			grp.add(m, edges(g));
			return body('index_cell', grp);
		})();
		const filter = (() => {
			const g = G(new THREE.BoxGeometry(num(fG.thickness, 0.6), num(fG.width, 14), num(fG.height, 41)));
			const grp = new THREE.Group();
			const m = new THREE.Mesh(g, std('density_filter', { depthWrite: false, side: THREE.DoubleSide }));
			m.renderOrder = 3;
			grp.add(m, edges(g));
			return body('density_filter', grp);
		})();
		const plate = (() => {
			const g = G(new THREE.BoxGeometry(plateS[0], plateS[1], plateS[2]));
			const grp = new THREE.Group();
			const m = new THREE.Mesh(g, std('beam_splitter', { depthWrite: false, envMapIntensity: 1.4 }));
			m.renderOrder = 3;
			const rim = nopick(new THREE.Mesh(g, rimMat('#cfe2ff', '#5d7a9c', 1.6, 0.7)));
			rim.renderOrder = 4;
			grp.add(m, rim, edges(g));
			grp.rotation.y = -tilt; // long side at the drawn tilt in the table plane, toward +z (Fig. 1 down)
			return body('beam_splitter', grp);
		})();
		const lensGeo = G(new THREE.SphereGeometry(lensD / 2, 48, 24).scale(lensT / lensD, 1, 1));
		const lensBody = (id: string, dir?: T.Vector3) => {
			const grp = new THREE.Group();
			const m = new THREE.Mesh(lensGeo, std(id, { clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 1.8, depthWrite: false }));
			m.renderOrder = 3;
			const rim = nopick(new THREE.Mesh(lensGeo, rimMat('#dcefff', '#6d8299', 1.8, 0.95)));
			rim.renderOrder = 4;
			const inner = new THREE.Group();
			inner.add(m, rim);
			if (dir) orientX(inner, dir);
			grp.add(inner);
			return body(id, grp);
		};
		const lens1 = lensBody('lens_launch_1');
		const lens2 = lensBody('lens_launch_2');
		const lensOut = lensBody('lens_output');
		const lensDet = lensBody('lens_detector', dirRefl);
		const detector = (() => {
			const g = G(new THREE.CylinderGeometry(detR, detR, detL, 40).rotateZ(-Math.PI / 2));
			const grp = new THREE.Group();
			const inner = new THREE.Group();
			inner.add(new THREE.Mesh(g, std('detector', { envMapIntensity: 0.9 })));
			// active face toward the lens (the same material; the light spot is drawn separately)
			orientX(inner, dirDet);
			grp.add(inner);
			return body('detector', grp);
		})();

		// ---------------------------------------------------------------------------- fibres (jacket + light tubes)
		const fibreLook = look('doped_fibre');
		const inPath = new THREE.LineCurve3(new THREE.Vector3(FX0, 0, 0), new THREE.Vector3(DF0, 0, 0));
		// doped fibre: straight to the tangent point, the single loop of Fig. 1 (rising 1 unit so it crosses over
		// itself), then on to the output end; Fig. 1 plane = table plane, loop toward -z (Fig. 1 up)
		const LOOP_RISE = 1.0;
		const dfPts: T.Vector3[] = [];
		for (let x = DF0; x < P.loop[0] - 1e-6; x += 1) dfPts.push(new THREE.Vector3(x, 0, 0));
		for (let i = 0; i <= 96; i++) {
			const th = (i / 96) * TAU;
			const t = i / 96;
			dfPts.push(new THREE.Vector3(P.loop[0] + loopR * Math.sin(th), LOOP_RISE * (t * t * (3 - 2 * t)), P.loop[2] + loopR * Math.cos(th)));
		}
		for (let x = P.loop[0] + 1; x <= DF1 + 1e-6; x += 1) {
			const t = clamp01((x - P.loop[0]) / 11);
			dfPts.push(new THREE.Vector3(x, LOOP_RISE * (1 - t * t * (3 - 2 * t)), 0));
		}
		const dfPath = new THREE.CatmullRomCurve3(dfPts, false, 'centripetal');
		const DF_SEG = 640;
		const IN_SEG = 80;
		const RAD = 12;
		const fibreMat = (id: string) =>
			std(id, { color: fibreLook.color || '#a9b4ba', opacity: 1, transparent: false, roughness: 0.3, clearcoat: 0.6, envMapIntensity: 1.2 });
		const inJacketGeo = G(new THREE.TubeGeometry(inPath, IN_SEG, fibR, RAD, false));
		const dfJacketGeo = G(new THREE.TubeGeometry(dfPath, DF_SEG, fibR, RAD, false));
		const fibreLight = (along = true) => {
			const mk = (pow: number, kk: number) =>
				shader(
					FIBRE_FS,
					{
						uSigC: { value: new THREE.Color('#b07cff') }, uPumpC: { value: new THREE.Color('#ff3b1f') },
						uSig0: { value: 0 }, uSig1: { value: 0 }, uSigF: { value: 0 },
						uPump: { value: 0 }, uPumpAtt: { value: PUMP_ATT }, uPumpF: { value: 1 },
						uPow: { value: pow }, uK: { value: kk }
					},
					along
				);
			return { core: mk(0.6, 0.8), halo: mk(2.4, 0.6) };
		};
		const inLight = fibreLight();
		const dfLight = fibreLight();
		const fibreGroup = (jacketGeo: T.TubeGeometry, path: T.Curve<T.Vector3>, segs: number, id: string, lt: { core: T.ShaderMaterial; halo: T.ShaderMaterial }) => {
			const grp = new THREE.Group();
			const jacket = new THREE.Mesh(jacketGeo, fibreMat(id));
			const coreGeo = G(new THREE.TubeGeometry(path, segs, fibR * 1.45, RAD, false));
			const haloGeo = G(new THREE.TubeGeometry(path, segs, fibR * 5, RAD, false));
			const core = nopick(new THREE.Mesh(coreGeo, lt.core));
			const halo = nopick(new THREE.Mesh(haloGeo, lt.halo));
			core.renderOrder = 6;
			halo.renderOrder = 7;
			const pickGeo = G(new THREE.TubeGeometry(path, Math.max(24, segs / 4), 2.2, 8, false));
			const proxy = new THREE.Mesh(pickGeo, keep(new THREE.MeshBasicMaterial({ visible: false })));
			grp.add(jacket, core, halo, proxy);
			return { grp, geos: [jacketGeo, coreGeo, haloGeo] };
		};
		const inF = fibreGroup(inJacketGeo, inPath, IN_SEG, 'doped_fibre', inLight);
		const dfF = fibreGroup(dfJacketGeo, dfPath, DF_SEG, 'doped_fibre', dfLight);
		const inFibre = body('input_fibre', inF.grp);
		const doped = body('doped_fibre', dfF.grp);
		// a neutral jacket for the undoped input fibre (the doped one keeps its spec look)
		for (const x of inFibre.mats) x.m.color.set('#959ca2');
		const setDraw = (geos: T.BufferGeometry[], segs: number, d: number) => {
			for (const g of geos) g.setDrawRange(0, Math.floor(clamp01(d) * segs) * RAD * 6);
		};

		// ---------------------------------------------------------------------------- free-space beams
		interface Seg {
			mat: T.ShaderMaterial;
			mesh: T.Mesh;
			len: number;
		}
		const beamSeg = (a: V3, b: V3, r0: number, r1: number, dark: string, light: string, pow: number) => {
			const va = new THREE.Vector3(...a);
			const vb = new THREE.Vector3(...b);
			const d = vb.clone().sub(va);
			const len = d.length();
			const g = G(new THREE.CylinderGeometry(r1, r0, 1, 40, 1, true).rotateZ(-Math.PI / 2).translate(0.5, 0, 0));
			const mat = shader(BEAM_FS, { uColor: { value: new THREE.Color(dark) }, uI0: { value: 0 }, uI1: { value: 0 }, uFront: { value: 0 }, uPow: { value: pow }, uK: { value: 1 } }, false);
			glows.push({ m: mat, dark, light, lightK: 0.85 });
			const mesh = new THREE.Mesh(g, mat);
			mesh.renderOrder = 8;
			mesh.position.copy(va);
			orientX(mesh, d);
			mesh.scale.set(len, 1, 1);
			return { mat, mesh, len } as Seg;
		};
		// signal colour illustrative (1.54 um is infrared): violet, well apart from the red pump in both themes
		const SIG = { dark: look('signal_beam').color || '#b07cff', light: '#6a2fd0' };
		const PUMP = { dark: look('pump_beam').color || '#ff3b1f', light: '#c42a12' };
		const r = BEAM_R * 0.88; // signal drawn a little inside the pump where they share the path
		const lensR = lensD / 2 - 1;
		const sigFree = [
			beamSeg(diodeFace, [P.lens1[0], 0, 0], 0.3, lensR, SIG.dark, SIG.light, 1.1),
			beamSeg([P.lens1[0], 0, 0], [FOCUS_X, 0, 0], lensR, 0.25, SIG.dark, SIG.light, 1.1),
			beamSeg([FOCUS_X, 0, 0], [P.lens2[0], 0, 0], 0.25, lensR, SIG.dark, SIG.light, 1.1),
			beamSeg([P.lens2[0], 0, 0], [FX0, 0, 0], lensR, 0.25, SIG.dark, SIG.light, 1.1)
		];
		const sigOut = [
			beamSeg([DF1, 0, 0], [P.lensOut[0], 0, 0], 0.3, r, SIG.dark, SIG.light, 1.1),
			beamSeg([P.lensOut[0], 0, 0], [P.plate[0], 0, 0], r, r, SIG.dark, SIG.light, 1.1),
			beamSeg([P.plate[0], 0, 0], [P.lensDet[0], 0, P.lensDet[2]], r, r, SIG.dark, SIG.light, 1.1),
			beamSeg([P.lensDet[0], 0, P.lensDet[2]], detFront, r, 0.4, SIG.dark, SIG.light, 1.1)
		];
		const pumpFree = [
			beamSeg(dyeFace, [P.plate[0], 0, 0], BEAM_R, BEAM_R, PUMP.dark, PUMP.light, 1.3),
			beamSeg([P.plate[0], 0, 0], [P.lensOut[0], 0, 0], BEAM_R, BEAM_R, PUMP.dark, PUMP.light, 1.3),
			beamSeg([P.lensOut[0], 0, 0], [DF1, 0, 0], BEAM_R, 0.3, PUMP.dark, PUMP.light, 1.3)
		];
		const sigGrp = new THREE.Group();
		for (const s of [...sigFree, ...sigOut]) sigGrp.add(s.mesh);
		const pumpGrp = new THREE.Group();
		for (const s of pumpFree) pumpGrp.add(s.mesh);
		const sigBody = body('signal_beam', sigGrp);
		const pumpBody = body('pump_beam', pumpGrp);

		// light spots (physical light): diode exit, dye-laser exit, detector face
		const spotTex = (() => {
			const cv = document.createElement('canvas');
			cv.width = cv.height = 64;
			const g = cv.getContext('2d')!;
			const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
			gr.addColorStop(0, 'rgba(255,255,255,1)');
			gr.addColorStop(0.25, 'rgba(255,255,255,0.55)');
			gr.addColorStop(1, 'rgba(255,255,255,0)');
			g.fillStyle = gr;
			g.fillRect(0, 0, 64, 64);
			const t = new THREE.CanvasTexture(cv);
			t.colorSpace = THREE.SRGBColorSpace;
			return keep(t);
		})();
		const spot = (pos: V3) => {
			const m = keep(new THREE.SpriteMaterial({ map: spotTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, opacity: 0 }));
			const s = nopick(new THREE.Sprite(m));
			place(s, pos);
			s.renderOrder = 9;
			root.add(s);
			return { s, m };
		};
		const spotDiode = spot([diodeFace[0] + 0.3, 0, 0]);
		const spotDye = spot([dyeFace[0] - 0.3, 0, 0]);
		const spotDet = spot([detFront[0] - dirDet.x * 0.3, 0, detFront[2] - dirDet.z * 0.3]);

		// ---------------------------------------------------------------------------- lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.8);
		const key = new THREE.DirectionalLight('#fff3e6', 2.2);
		key.position.set(60, 140, 120);
		const rimL = new THREE.DirectionalLight('#bcd2ff', 1.2);
		rimL.position.set(-160, 60, -120);
		const fill = new THREE.DirectionalLight('#ffffff', 0.45);
		fill.position.set(40, -40, 160);
		root.add(hemi, key, rimL, fill);

		// ---------------------------------------------------------------------------- signal / pump chains
		// signal: 4 launch segments, input fibre, doped fibre, 4 output segments; distances in units along the path
		const inLen = DF0 - FX0;
		const dfLen = dfPath.getLength();
		const sigLens = [...sigFree.map((s) => s.len), inLen, dfLen, ...sigOut.map((s) => s.len)];
		const sigStart: number[] = [];
		sigLens.reduce((acc, l, i) => ((sigStart[i] = acc), acc + l), 0);
		const SIG_TOTAL = sigStart[sigStart.length - 1] + sigLens[sigLens.length - 1];
		const D_FIBRE_END = sigStart[4]; // input fibre end
		const D_SPLICE = sigStart[5]; // butt joint
		const D_PLATE = sigStart[8];
		const pumpLens = [...pumpFree.map((s) => s.len), dfLen];
		const PUMP_TOTAL = pumpLens.reduce((a, b) => a + b, 0);
		const localF = (d: number, start: number, len: number) => clamp01((d - start) / Math.max(1e-6, len));

		// ---------------------------------------------------------------------------- plot pens (D1006)
		const plotOf = (id: string) => spec.plots?.find((x) => x.id === id);
		const ptsOf = (id: string, si: number) => (plotOf(id)?.series?.[si]?.points ?? []) as [number, number][];
		const nSer = (id: string) => Math.max(1, plotOf(id)?.series?.length ?? 1);
		/** plot progress: the runtime assembles a plot over the first 90 % of its chapter (axes, then series staggered) */
		const rrOf = (q: number) => seg(q, 0, 0.9);
		const kOf = (id: string, si: number, rr: number) => staggerK(rr, AXES_END, 1, si, nSer(id));
		/** point under the pen of a line series (first point before it starts, last after it ends) */
		function linePen(id: string, si: number, rr: number): [number, number] | null {
			const pts = ptsOf(id, si);
			const N = pts.length;
			if (!N) return null;
			const t = Math.max(0, Math.min(N - 1, kOf(id, si, rr) * N - 1));
			const i = Math.floor(t);
			const j = Math.min(N - 1, i + 1);
			return [lerp(pts[i][0], pts[j][0], t - i), lerp(pts[i][1], pts[j][1], t - i)];
		}
		/** index of the last revealed point of a points series, held at 0 before the first appears */
		const shownIdx = (id: string, si: number, rr: number) => {
			const N = ptsOf(id, si).length;
			return Math.max(0, Math.min(N, Math.floor(kOf(id, si, rr) * N + 1e-9)) - 1);
		};
		const mwOf = (name: string | undefined) => {
			const m = /(\d+(?:\.\d+)?)\s*mW/.exec(name ?? '');
			return m ? Number(m[1]) : 0;
		};
		/** Fig. 2: the curve whose pen started last; pump power from its label, tone from the pen wavelength */
		function fig2(rr: number): LightState & { mw: number; gain: number } {
			let si = 0;
			for (let i = 0; i < nSer('gain_pump'); i++) if (kOf('gain_pump', i, rr) > 0) si = i;
			const pen = linePen('gain_pump', si, rr) ?? [LAM_ON, 0];
			const mw = mwOf(plotOf('gain_pump')?.series?.[si]?.name);
			return { bIn: B_IN, bOut: bGain(pen[1]), pump: gPump(mw), lam: pen[0], mw, gain: pen[1] };
		}
		/** derived alternate: the last revealed point over both series (power, gain); tone not stated -> default */
		function fig2alt(rr: number): LightState & { mw: number; gain: number } {
			const id = 'gain_power';
			const n = nSer(id);
			let best: [number, number] | null = null;
			let bt = -1;
			for (let i = 0; i < n; i++) {
				const pts = ptsOf(id, i);
				const [a, b] = stagger(AXES_END, 1, i, n);
				pts.forEach((pt, j) => {
					const t = a + ((j + 1) / pts.length) * (b - a);
					if (t <= rr + 1e-9 && t > bt) {
						bt = t;
						best = pt;
					}
				});
			}
			const pt: [number, number] = best ?? ptsOf(id, 0)[0] ?? [100, 0];
			return { bIn: B_IN, bOut: bGain(pt[1]), pump: gPump(pt[0]), lam: LAM_ON, mw: pt[0], gain: pt[1] };
		}
		const pumpPlot = (rr: number) => (shownPlot === 'gain_power' && plotOf('gain_power') ? fig2alt(rr) : fig2(rr));
		/** Fig. 3 at 60 mW absorbed (text): the last revealed circle */
		function fig3(rr: number): LightState & { pin: number; pout: number } {
			const pt = ptsOf('transfer', 0)[shownIdx('transfer', 0, rr)] ?? [-40, -14];
			return { bIn: bDbm(pt[0]), bOut: bDbm(pt[1]), pump: gPump(60), lam: LAM_ON, pin: pt[0], pout: pt[1] };
		}
		/** Fig. 4: the last revealed measured point (the fluorescence curve never drives the model) */
		function fig4(rr: number): LightState & { lam_s: number; gain: number } {
			const pt = ptsOf('spectrum', 0)[shownIdx('spectrum', 0, rr)] ?? [1536, 0];
			return { bIn: B_IN, bOut: bGain(pt[1]), pump: P_ON, lam: LAM_ON, lam_s: pt[0], gain: pt[1] };
		}
		const S_ON: LightState = { bIn: B_IN, bOut: bGain(28), pump: P_ON, lam: LAM_ON };

		interface Light extends LightState {
			sigD: number; // signal front, distance along the signal chain
			pumpD: number; // pump front, distance along the pump chain
		}
		function lightAt(p: number): Light {
			const L: Light = { ...S_ON, bOut: B_IN, pump: 0, sigD: 0, pumpD: 0 };
			if (p < C.signal[0]) return L;
			if (inCh('signal', p)) {
				L.sigD = D_FIBRE_END * ease(seg(cq('signal', p), 0.35, 0.95));
				return L;
			}
			if (inCh('launch', p)) {
				L.sigD = lerp(D_FIBRE_END, D_SPLICE, ease(seg(cq('launch', p), 0.45, 0.95)));
				return L;
			}
			L.sigD = D_SPLICE;
			if (inCh('fibre', p)) return L;
			L.pump = P_ON;
			if (inCh('pump', p)) {
				L.pumpD = PUMP_TOTAL * ease(seg(cq('pump', p), 0.42, 0.97));
				return L;
			}
			L.pumpD = PUMP_TOTAL;
			L.bOut = S_ON.bOut;
			if (inCh('gain', p)) {
				L.sigD = lerp(D_SPLICE, D_PLATE, ease(seg(cq('gain', p), 0.08, 0.85)));
				return L;
			}
			if (inCh('detect', p)) {
				L.sigD = lerp(D_PLATE, SIG_TOTAL, ease(seg(cq('detect', p), 0.4, 0.85)));
				return L;
			}
			L.sigD = SIG_TOTAL;
			// plot chapters: the state under the pen; a short blend from the previous chapter's end state
			let cur: LightState;
			let prev: LightState;
			let q: number;
			if (inCh('pump_curve', p)) {
				q = cq('pump_curve', p);
				cur = pumpPlot(rrOf(q));
				prev = S_ON;
			} else if (inCh('transfer', p)) {
				q = cq('transfer', p);
				cur = fig3(rrOf(q));
				prev = pumpPlot(1);
			} else {
				q = cq('spectrum', p);
				cur = fig4(rrOf(q));
				prev = fig3(1);
			}
			const s = mixState(prev, cur, ease(seg(q, 0, 0.1)));
			return { ...L, ...s };
		}

		// ---------------------------------------------------------------------------- state helpers
		const raycaster = new THREE.Raycaster();
		const v2 = new THREE.Vector2();
		const tmp = new THREE.Vector3();
		const tmp2 = new THREE.Vector3();
		const accent = new THREE.Color();
		const black = new THREE.Color(0, 0, 0);
		const pumpCol = new THREE.Color();
		const sigCol = new THREE.Color();
		let shot: Shot & { rect: Rect } = { ...SHOTS.intro, rect: regions(w, h).full };

		function setOpacity(b: Body, o: number) {
			const lit = hi.includes(b.id);
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
		function tint(b: Body, glowCol: T.Color | null, gi = 0) {
			const lit = hi.includes(b.id);
			for (const x of b.mats) {
				x.m.emissive.copy(glowCol ?? black);
				x.m.emissiveIntensity = glowCol ? gi : 1;
				if (lit) {
					x.m.emissive.lerp(accent, glowCol ? 0.35 : 1);
					if (!glowCol) x.m.emissiveIntensity = 0.25;
				}
			}
		}
		const mix3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];

		function shotAt(p: number): Shot & { rect: Rect } {
			const R = regions(w, h);
			let i = 0;
			for (let j = 0; j < CHAPTER_IDS.length; j++) if (p >= C[CHAPTER_IDS[j]][0]) i = j;
			const id = CHAPTER_IDS[i];
			const q = cq(id, p);
			const cur = SHOTS[id];
			const prev = i > 0 ? SHOTS[CHAPTER_IDS[i - 1]] : null;
			const t = prev ? ease(seg(q, 0, cur.region === 'plot' && prev.region !== 'plot' ? 0.2 : 0.45)) : 1;
			// phones (portrait pane): long shots turn toward the bench axis so the 300-unit bench is not a thin line
			const paz = (sid: string | undefined) => (w < 700 && sid ? (PHONE_AZ[sid] ?? 0) : 0);
			const curAz = cur.az + paz(id) + cur.drift * (q - 0.5);
			const prevAz = prev ? prev.az + paz(CHAPTER_IDS[i - 1]) + prev.drift * 0.5 : curAz;
			const rc = R[cur.region];
			const rp = prev ? R[prev.region] : rc;
			// user explode: pull back a little so the raised parts stay in the shot
			const kx = ease(clamp01(k));
			const tt = mix3(prev?.t ?? cur.t, cur.t, t);
			return {
				t: [tt[0], tt[1] + 12 * kx, tt[2]],
				az: lerp(prevAz, curAz, t),
				el: lerp(prev?.el ?? cur.el, cur.el, t) - 14 * kx,
				R: [lerp(prev?.R[0] ?? cur.R[0], cur.R[0], t), lerp(prev?.R[1] ?? cur.R[1], cur.R[1], t) + 22 * kx],
				drift: 0,
				region: cur.region,
				rect: [lerp(rp[0], rc[0], t), lerp(rp[1], rc[1], t), lerp(rp[2], rc[2], t), lerp(rp[3], rc[3], t)]
			};
		}
		function applyCamera(s: Shot & { rect: Rect }) {
			const [x0, y0, x1, y1] = s.rect;
			const tf = Math.tan((camera.fov * DEG) / 2);
			const dist = Math.max(s.R[0] / (tf * (w / h) * (x1 - x0)), s.R[1] / (tf * (y1 - y0)));
			const az = s.az * DEG;
			const el = s.el * DEG;
			camera.position.set(s.t[0] + dist * Math.cos(el) * Math.sin(az), s.t[1] + dist * Math.sin(el), s.t[2] + dist * Math.cos(el) * Math.cos(az));
			camera.lookAt(s.t[0], s.t[1], s.t[2]);
			camera.setViewOffset(w, h, (0.5 - (x0 + x1) / 2) * w, (0.5 - (y0 + y1) / 2) * h, w, h);
			camera.updateMatrixWorld();
		}

		/** pump tone for a pump wavelength (nm): illustrative red ramp, 640 nm orange-red to 690 nm deep red */
		const toneA = new THREE.Color();
		const toneB = new THREE.Color();
		function pumpTone(lam: number, out: T.Color) {
			const light = theme === 'light';
			const t = clamp01((lam - 640) / 50);
			const c0 = light ? '#d0400c' : '#ff6418';
			const c1 = light ? PUMP.light : PUMP.dark;
			const c2 = light ? '#a00c26' : '#d8102e';
			if (t < 0.6) out.copy(toneA.set(c0)).lerp(toneB.set(c1), t / 0.6);
			else out.copy(toneA.set(c1)).lerp(toneB.set(c2), (t - 0.6) / 0.4);
			return out;
		}

		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			for (const g of glows) {
				g.m.uniforms.uColor.value.set(light ? g.light : g.dark);
				g.m.uniforms.uLight.value = light ? 1 : 0;
				if (g.m.uniforms.uK) g.m.uniforms.uK.value = light ? g.lightK : 1;
				g.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			for (const lt of [inLight, dfLight])
				for (const m of [lt.core, lt.halo]) {
					m.uniforms.uLight.value = light ? 1 : 0;
					m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
				}
			for (const s of [spotDiode, spotDye, spotDet]) s.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			for (const m of edgeMats) m.color.set(light ? '#8d9098' : '#6c717b');
			hemi.intensity = light ? 1.0 : 0.8;
		}
		applyTheme();

		// ---------------------------------------------------------------------------- frame
		const bob = (ph: number, p: number) => 1.6 * Math.sin(TAU * (p * 3 + ph)) * (1 - seg(p, C.signal[0], C.signal[0] + 0.03));
		const POS: Record<string, V3> = {
			laser_diode: P.diode, lens_launch_1: P.lens1, density_filter: P.filter, lens_launch_2: P.lens2, index_cell: P.cell,
			input_fibre: [0, 0, 0], fibre_coupler: P.coupler, butt_splice: P.splice, doped_fibre: [0, 0, 0],
			lens_output: P.lensOut, beam_splitter: P.plate, lens_detector: P.lensDet, detector: P.det, dye_laser: P.dye
		};

		function frame(p: number) {
			lastP = p;
			const kk = clamp01(k);
			shot = shotAt(p);
			applyCamera(shot);
			const introQ = cq('intro', p);

			// ---- bodies: float in the intro (beams off), then arrive in their own chapter; explode raises them
			let ph = 0;
			for (const [id, ch] of Object.entries(ARRIVE)) {
				const b = bodies.get(id)!;
				const ye = YE[id] ?? 20;
				ph += 0.137;
				let y: number;
				let o: number;
				if (p < C.signal[0]) {
					y = ye * (0.85 + 0.15 * Math.sin(ph * 9)) + bob(ph, p);
					o = ch === 'signal' ? 1 : 1 - easeOut(seg(introQ, 0.62, 0.98));
				} else if (p < C[ch][0]) {
					y = ye;
					o = 0;
				} else {
					const q = cq(ch, p);
					const arrive = ease(seg(q, 0.0, 0.5));
					y = ye * (1 - arrive);
					o = ch === 'signal' ? 1 : easeOut(seg(q, 0, 0.22));
				}
				y += kk * ye;
				const base = POS[id];
				place(b.obj, [base[0], base[1] + y, base[2]]);
				setOpacity(b, o);
			}
			// fibres are laid along the table in their chapter (drawn progressively)
			{
				const dIn = p < C.signal[0] ? 1 : p < C.launch[0] ? 0 : ease(seg(cq('launch', p), 0.05, 0.55));
				const dDf = p < C.signal[0] ? 1 : p < C.fibre[0] ? 0 : ease(seg(cq('fibre', p), 0.05, 0.8));
				setDraw(inF.geos, IN_SEG, dIn);
				setDraw(dfF.geos, DF_SEG, dDf);
				// laid fibres need no drop: keep them on the table outside the intro / explode
				if (p >= C.signal[0]) {
					inFibre.obj.position.y = kk * YE.input_fibre;
					doped.obj.position.y = kk * YE.doped_fibre;
					setOpacity(inFibre, p >= C.launch[0] ? 1 : 0);
					setOpacity(doped, p >= C.fibre[0] ? 1 : 0);
				}
			}

			// ---- light
			const L = lightAt(p);
			const beamOn = 1 - seg(kk, 0, 0.15); // explode: light off while parts are apart
			const light = theme === 'light';
			pumpTone(L.lam, pumpCol);
			sigCol.set(light ? SIG.light : SIG.dark);
			const hiSig = (hi.includes('signal_beam') ? 1.35 : 1) * (light ? 1 : 1.4); // violet reads darker than red: one factor on every signal level
			const hiPump = hi.includes('pump_beam') ? 1.35 : 1;
			// signal chain
			const segI = (i: number) => localF(L.sigD, sigStart[i], sigLens[i]);
			sigFree.forEach((s, i) => {
				const f = segI(i);
				s.mat.uniforms.uFront.value = f >= 1 ? 2 : f;
				s.mat.uniforms.uI0.value = s.mat.uniforms.uI1.value = L.bIn * beamOn * hiSig;
				s.mesh.visible = f > 0 && beamOn > 0.01;
			});
			sigOut.forEach((s, i) => {
				const f = segI(6 + i);
				s.mat.uniforms.uFront.value = f >= 1 ? 2 : f;
				const b = (i >= 2 ? 0.9 : 1) * L.bOut * beamOn * hiSig; // 90 % reflected at 1.54 um
				s.mat.uniforms.uI0.value = s.mat.uniforms.uI1.value = b;
				s.mesh.visible = f > 0 && beamOn > 0.01;
			});
			const fIn = segI(4);
			const fDf = segI(5);
			for (const m of [inLight.core, inLight.halo]) {
				m.uniforms.uSigC.value.copy(sigCol);
				m.uniforms.uSig0.value = m.uniforms.uSig1.value = L.bIn * beamOn * hiSig * inFibre.o;
				m.uniforms.uSigF.value = fIn >= 1 ? 2 : fIn;
				m.uniforms.uPump.value = 0; // residual pump beyond the doped fibre is not described: not drawn
			}
			// pump chain: free space from the dye laser, then backward along the doped fibre
			const pumpI = L.pump * beamOn * hiPump;
			let acc = 0;
			pumpFree.forEach((s, i) => {
				const f = localF(L.pumpD, acc, pumpLens[i]);
				acc += pumpLens[i];
				s.mat.uniforms.uFront.value = f >= 1 ? 2 : f;
				s.mat.uniforms.uI0.value = s.mat.uniforms.uI1.value = pumpI * (i >= 1 ? 0.85 : 1); // 85 % T at 670 nm
				s.mat.uniforms.uColor.value.copy(pumpCol);
				s.mesh.visible = f > 0 && pumpI > 0.01;
			});
			const fPumpDf = localF(L.pumpD, acc, dfLen);
			for (const m of [dfLight.core, dfLight.halo]) {
				m.uniforms.uSigC.value.copy(sigCol);
				m.uniforms.uPumpC.value.copy(pumpCol);
				m.uniforms.uSig0.value = L.bIn * beamOn * hiSig * doped.o;
				m.uniforms.uSig1.value = L.bOut * beamOn * hiSig * doped.o;
				m.uniforms.uSigF.value = fDf >= 1 ? 2 : fDf;
				m.uniforms.uPump.value = 0.85 * pumpI * doped.o;
				m.uniforms.uPumpF.value = 1 - fPumpDf;
			}
			// spots
			const dOn = L.sigD > 0 ? 1 : 0;
			spotDiode.m.color.copy(sigCol);
			spotDiode.m.opacity = 0.9 * dOn * L.bIn * beamOn * diode.o;
			spotDiode.s.scale.setScalar(3.2);
			spotDye.m.color.copy(pumpCol);
			spotDye.m.opacity = 0.9 * (L.pumpD > 0 ? 1 : 0) * pumpI * dye.o;
			spotDye.s.scale.setScalar(4 + 3 * L.pump);
			const fDet = segI(9);
			spotDet.m.color.copy(sigCol);
			spotDet.m.opacity = 0.95 * seg(fDet, 0.9, 1) * L.bOut * beamOn * detector.o;
			spotDet.s.scale.setScalar(3 + 4 * L.bOut);
			for (const s of [spotDiode, spotDye, spotDet]) s.s.visible = s.m.opacity > 0.005;

			// bodies' emphasis (the light inside the fibre is drawn by its glow tubes, not by the jacket)
			for (const b of bodies.values()) if (b !== sigBody && b !== pumpBody) tint(b, null);
			sigBody.o = L.sigD > 0 ? beamOn : 0;
			pumpBody.o = L.pumpD > 0 ? pumpI : 0;
			sigBody.obj.visible = pumpBody.obj.visible = true;
		}

		// ---------------------------------------------------------------------------- pick, anchors
		const vq = new THREE.Vector3();
		function screen(v: V3): [number, number] | null {
			vq.set(v[0], v[1], v[2]);
			tmp2.copy(vq).applyMatrix4(camera.matrixWorldInverse);
			if (tmp2.z > -camera.near) return null;
			vq.project(camera);
			return [((vq.x + 1) / 2) * w, ((1 - vq.y) / 2) * h];
		}
		const SCHEMATIC = 'Position after Fig. 1: schematic, not to scale';
		const LEVELS = 'Brightness illustrative: signal on a dB scale, pump glow by absorbed pump power';
		const ALONG = 'Growth of the signal and fading of the pump along the fibre drawn, not measured';
		/** the plotted state the model shows in a plot chapter (one line), else null */
		function stateLine(p: number): string | null {
			const f = (v: number, d = 1) => v.toFixed(d);
			if (inCh('pump_curve', p)) {
				const q = rrOf(cq('pump_curve', p));
				if (shownPlot === 'gain_power') {
					const s2 = fig2alt(q);
					return `Shown: ${f(s2.mw, 0)} mW absorbed, gain ${f(s2.gain)} dB (point under the plot pen)`;
				}
				const s2 = fig2(q);
				return `Shown: ${f(s2.mw, 0)} mW absorbed at ${f(s2.lam)} nm, gain ${f(s2.gain)} dB (Fig. 2 under the pen)`;
			}
			if (inCh('transfer', p)) {
				const s3 = fig3(rrOf(cq('transfer', p)));
				return `Shown: input ${f(s3.pin)} dBm, output ${f(s3.pout)} dBm at 60 mW pump (Fig. 3 point)`;
			}
			if (inCh('spectrum', p)) {
				const s4 = fig4(rrOf(cq('spectrum', p)));
				return `Shown: ${f(s4.lam_s, 2)} nm, gain ${f(s4.gain)} dB (Fig. 4 point); pump power not stated`;
			}
			return null;
		}
		const CAVEATS: Record<string, (p: number) => string[]> = {
			doped_fibre: (p) => [LEVELS, ALONG, stateLine(p) ?? ''],
			signal_beam: (p) => [LEVELS, ALONG, stateLine(p) ?? ''],
			pump_beam: (p) => [
				LEVELS,
				inCh('pump_curve', p) && shownPlot !== 'gain_power'
					? 'Colour follows the plotted pump wavelength (illustrative red ramp, 640 to 690 nm)'
					: 'Colour illustrative (red, about 670 nm); run wavelength not stated outside Fig. 2',
				ALONG,
				stateLine(p) ?? ''
			]
		};
		const partInfo = (id: string): PickInfo => {
			const q = partOf(id);
			const where = id === 'signal_beam' || id === 'pump_beam' ? 'Path after Fig. 1: schematic, not to scale' : SCHEMATIC;
			return { id, label: q?.name ?? id, detail: [...(CAVEATS[id]?.(lastP) ?? []), where].filter(Boolean) };
		};
		const INPUT_INFO: PickInfo = {
			id: 'input_fibre',
			label: 'Signal input fibre',
			detail: [
				'Single-mode fibre from the index-matched input end to the butt-splice',
				'Coupler and splice placed in the order the text gives (not drawn in Fig. 1)',
				SCHEMATIC
			]
		};
		function pick(x: number, y: number): string | PickInfo | null {
			v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
			raycaster.setFromCamera(v2, camera);
			const cands: T.Object3D[] = [];
			for (const b of bodies.values()) {
				if (!b.obj.visible || b.o < 0.2) continue;
				if (b === sigBody || b === pumpBody) cands.push(...b.picks.filter((m) => m.visible));
				else cands.push(...b.picks);
			}
			const hit = raycaster.intersectObjects(cands, false)[0];
			const id = hit?.object.userData.part as string | undefined;
			if (!id) return null;
			if (id === 'input_fibre') return INPUT_INFO;
			return partInfo(id);
		}
		function anchor(id: string): [number, number] | null {
			const b = bodies.get(id);
			if (!b || !b.obj.visible || b.o < 0.5) return null;
			let s: [number, number] | null = null;
			const p = lastP;
			if (id === 'doped_fibre') s = screen([P.loop[0], LOOP_RISE + doped.obj.position.y, P.loop[2] - loopR]);
			else if (id === 'signal_beam') {
				if (inCh('detect', p)) s = screen([lerp(P.plate[0], P.lensDet[0], 0.45), 0, lerp(P.plate[2], P.lensDet[2], 0.45) + 1]);
				// between lens 2 and the cell, clear of the filter plate
				else if (L_front(p) > 0.5) s = screen([lerp(P.lens2[0], FX0, 0.55), 2.5, 0]);
			}
			if (!s) return null;
			if (s[0] < 4 || s[0] > w - 4 || s[1] < 8 || s[1] > h - 12) return null;
			if (shot.region === 'plot') {
				const pb = regions(w, h).plotBox;
				if (s[0] > pb[0] * w - 170 && s[1] > pb[1] * h) return null;
			}
			return s;
		}
		/** signal front reached the launch section (0..1) */
		const L_front = (p: number) => clamp01(lightAt(p).sigD / Math.max(1, sigStart[3]));

		// ---------------------------------------------------------------------------- handle
		const handle: ShowcaseHandle = {
			assembledAt: C.spectrum[0],
			orbit: { polar: [6, 82] },
			frame,
			highlight(ids) {
				hi = [...ids];
			},
			pick,
			anchor,
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
			/** plot on screen (runtime hook): the model follows the pen of the derived alternate when it is shown */
			plot(id) {
				shownPlot = id;
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
