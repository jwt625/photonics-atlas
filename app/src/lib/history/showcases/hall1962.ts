// Scene module: GaAs junction laser, Hall et al. 1962 (Phys. Rev. Lett. 9, 366) with the recipe of R. N. Hall's patent
// of the same work (US 3,245,002). Spec: data/history/showcases/hall1962.yaml. Contract: ../showcase/types.ts.
// Units mm; x = cavity axis (+x = front face, beam direction), y = up (normal to the junction), z = across.
// Origin = centre of the metal disc's top face; the cube stands on it from y = 0 to 0.4, junction plane at y = 0.2.
//
// Story: finished diode (intro) -> n-type wafer -> zinc diffusion in a sealed ampoule (cut-away front face shows the
// p skin growing in from every surface) -> cut piece of the patent example (one junction about 0.1 mm below the top,
// bottom skin ground away) replaced by the letter's 0.4 mm cube with the junction through the centre (hover on the cut
// piece says so) -> front and back faces polished -> top contact, metal disc, lead -> liquid nitrogen and the pulse
// source -> three plot chapters in which the light follows the plot:
//  - threshold (patent FIG. 3): drive = current density under the plot pen; spontaneous glow from the part of the
//    digitized curve on the extended low-current line (dashed), beam from the excess above it (display gamma 0.5);
//  - spectrum (letter Fig. 2, currents not printed): broad curve = weak glow, no beam; narrow curve = beam on;
//  - modes (letter Fig. 3): drive steps with the curve being drawn; glow and beam from that curve's peak (one vertical
//    scale), beam only above the letter's 8500 A/cm^2 threshold.
// Drive is pulsed (letter: 5 to 20 µs pulses): the emission blinks with slowed pulses and holds within one pulse at
// each chapter end. The beam leaves both polished faces (patent col. 6:26-28); drawn red, spread illustrative.
// Not drawn (withheld in the spec): Dewar, windows, converter tube, spectrometer, lead shapes, tapered side faces.
import type * as THREE_NS from 'three';
import { penAt, revealAt } from '../showcase/plot';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { PickInfo, ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type V3 = [number, number, number];
type Rect = [number, number, number, number]; // pane fractions x0, y0, x1, y1
type Geo = Record<string, unknown>;

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);

// ------------------------------------------------------------------------------------------------ camera shots
// One settled shot per chapter. R = [half width, half height] (mm) around t that must fit in the region; drift = degrees
// of azimuth turned across the chapter; win = part of the chapter over which the camera moves from the previous shot.
interface Shot {
	t: V3;
	az: number;
	el: number;
	R: [number, number];
	drift: number;
	region: 'full' | 'plot';
	win?: [number, number];
}
const SHOTS: Record<string, Shot> = {
	intro: { t: [0, 0.2, 0], az: 30, el: 20, R: [1.5, 0.95], drift: 50, region: 'full' },
	wafer: { t: [0, 0.3, 0], az: 28, el: 26, R: [2.1, 1.3], drift: 8, region: 'full' },
	diffuse: { t: [0, 0.3, 0], az: 24, el: 18, R: [5.0, 2.5], drift: 6, region: 'full' },
	cut: { t: [0, 0.3, 0], az: 32, el: 20, R: [0.9, 0.7], drift: 6, region: 'full', win: [0.15, 0.95] },
	polish: { t: [0, 0.2, 0], az: 0, el: 16, R: [0.8, 0.55], drift: -130, region: 'full', win: [0, 0.25] },
	contacts: { t: [0, 0.38, 0], az: 34, el: 22, R: [1.45, 1.0], drift: 8, region: 'full' },
	cold: { t: [-2.2, 1.2, 0], az: 20, el: 14, R: [5.6, 2.1], drift: 4, region: 'full' },
	threshold: { t: [0.4, 0.25, 0], az: 30, el: 24, R: [1.3, 0.8], drift: 4, region: 'plot', win: [0, 0.2] },
	spectrum: { t: [0.4, 0.25, 0], az: 36, el: 22, R: [1.3, 0.8], drift: 4, region: 'plot', win: [0, 0.2] },
	modes: { t: [0.4, 0.25, 0], az: 26, el: 24, R: [1.3, 0.8], drift: 4, region: 'plot', win: [0, 0.2] }
};
const CHAPTER_IDS = ['intro', 'wafer', 'diffuse', 'cut', 'polish', 'contacts', 'cold', 'threshold', 'spectrum', 'modes'];

function regions(w: number, h: number): { full: Rect; plot: Rect; plotBox: Rect } {
	if (w < 700) return { full: [0.04, 0.2, 0.96, 0.98], plot: [0.04, 0.2, 0.96, 0.43], plotBox: [0, 0.44, 1, 1] };
	const top = Math.min(0.24, 150 / Math.max(1, h));
	return { full: [0.03, top, 0.97, 0.97], plot: [0.03, top, 0.49, 0.97], plotBox: [0.5, 0.16, 1, 1] };
}

// ------------------------------------------------------------------------------------------------ shaders
// Beam: a flat fan in the junction plane (plus a thin crossed ribbon so it reads from any elevation). Positions are
// built from uv in the vertex shader: x along the beam (0..uLen), across = (v - 0.5) * width(x).
const BEAM_VS = /* glsl */ `
uniform float uLen; uniform float uW0; uniform float uTan; uniform float uVert;
varying vec2 vUv;
void main() {
	vUv = uv;
	float x = uv.x * uLen;
	float half_w = 0.5 * uW0 + x * uTan;
	float a = (uv.y - 0.5) * 2.0 * half_w;
	vec3 p = uVert > 0.5 ? vec3(x, a, 0.0) : vec3(x, 0.0, a);
	gl_Position = projectionMatrix * modelViewMatrix * vec4(p, 1.0);
}`;
const BEAM_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uLight; uniform float uTail;
varying vec2 vUv;
void main() {
	float v = (vUv.y - 0.5) * 2.0;
	float a = uI * exp(-v * v * 3.2) * smoothstep(0.0, 0.015, vUv.x) * (1.0 - smoothstep(uTail, 1.0, vUv.x)) * (1.0 - 0.45 * vUv.x);
	a = clamp(a, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a) : vec4(uColor * a, a);
}`;
// Glint: a bright diagonal band sweeping across a polished face (specular reflection of the room light).
const GLINT_FS = /* glsl */ `
uniform float uS; uniform float uI; uniform vec3 uColor; uniform float uLight;
varying vec2 vUv;
void main() {
	float d = (vUv.x + vUv.y - 1.0) - uS;
	float a = clamp(uI * exp(-d * d / 0.018), 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a * 0.8) : vec4(uColor * a, a);
}`;
const UV_VS = /* glsl */ `
varying vec2 vUv;
void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('hall1962 is a 3D scene');
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
			intro: [0, 0.07], wafer: [0.07, 0.15], diffuse: [0.15, 0.26], cut: [0.26, 0.36], polish: [0.36, 0.45],
			contacts: [0.45, 0.54], cold: [0.54, 0.62], threshold: [0.62, 0.75], spectrum: [0.75, 0.88], modes: [0.88, 1]
		};
		const C = Object.fromEntries(
			CHAPTER_IDS.map((id) => [id, (spec.chapters.find((c) => c.id === id)?.p ?? fallback[id]) as [number, number]])
		) as Record<string, [number, number]>;
		const cq = (id: string, p: number) => seg(p, C[id][0], C[id][1]);
		const chapterOf = (p: number): string => {
			let id = CHAPTER_IDS[0];
			for (const c of CHAPTER_IDS) if (p >= C[c][0]) id = c;
			return id;
		};

		// ---------------------------------------------------------------------------- dimensions from the spec
		const cubeS = (geo('crystal').size as number[] | undefined) ?? [0.4, 0.4, 0.4];
		const E = num(cubeS[0], 0.4); // cube edge
		const HE = E / 2;
		const jT = num((geo('junction').size as number[] | undefined)?.[1], 0.012);
		const jY = at('junction', [0, 0.2, 0])[1];
		const ctT = num((geo('top_contact').size as number[] | undefined)?.[1], 0.03);
		const discR = num(geo('mount_disc').diameter, 2) / 2;
		const discH = num(geo('mount_disc').height, 0.2);
		const wS = (geo('wafer').size as number[] | undefined) ?? [2.4, 0.6, 2.4];
		const [WX, WY, WZ] = [num(wS[0], 2.4), num(wS[1], 0.6), num(wS[2], 2.4)];
		const skinD = num(geo('zn_skin').depth, 0.1);
		const ampR = num(geo('quartz_ampoule').diameter, 4) / 2;
		const ampL = num(geo('quartz_ampoule').length, 9);
		const lnR = num(geo('ln2_bath').diameter, 6) / 2;
		const lnH = num(geo('ln2_bath').height, 3);
		const lnY = at('ln2_bath', [0, 1.2, 0])[1];
		const psuS = (geo('pulse_source').size as number[] | undefined) ?? [3, 1.6, 1.6];
		const psuP = at('pulse_source', [-5.5, 1, 0]);
		const leadR = num(geo('top_lead').diameter, 0.05) / 2;
		const beamL = num(geo('beam').length, 8);
		const waferY = at('wafer', [0, 0.3, 0])[1] - WY / 2; // wafer bottom

		// ---------------------------------------------------------------------------- plot data (light follows the plot)
		const plotOf = (id: string) => spec.plots?.find((x) => x.id === id);
		const ptsOf = (id: string, i: number) => ((plotOf(id)?.series?.[i]?.points ?? []) as [number, number][]).filter((q) => q.every(Number.isFinite));
		const thrSolid = ptsOf('threshold', 0);
		const thrDash = ptsOf('threshold', 1);
		const thrMark = ptsOf('threshold', 2);
		/** threshold current density from the letter text (marker series), A/cm^2 */
		const JTH = thrMark[0]?.[0] ?? 8500;
		// extended low-current line of FIG. 3: least-squares power law through the dashed points (log-log straight line)
		const dashFit = (() => {
			const xs = thrDash.map((q) => Math.log10(q[0]));
			const ys = thrDash.map((q) => Math.log10(q[1]));
			const n = xs.length;
			if (n < 2) return { a: 0, b: 1 };
			const mx = xs.reduce((s, v) => s + v, 0) / n;
			const my = ys.reduce((s, v) => s + v, 0) / n;
			let sxy = 0;
			let sxx = 0;
			for (let i = 0; i < n; i++) {
				sxy += (xs[i] - mx) * (ys[i] - my);
				sxx += (xs[i] - mx) ** 2;
			}
			const b = sxx > 0 ? sxy / sxx : 1;
			return { a: my - b * mx, b };
		})();
		const dashAt = (x: number) => 10 ** (dashFit.a + dashFit.b * Math.log10(Math.max(1, x)));
		// Display split of the FIG. 3 curve: spontaneous glow follows the low-current line and holds at its threshold
		// level (carrier density pins above threshold); the beam is the excess over that line, counted only beyond the
		// 5 % fit residual of region A (no beam below threshold).
		const dashTh = Math.max(1e-6, dashAt(JTH));
		const excess = (x: number, y: number) => Math.max(0, y - 1.05 * dashAt(x));
		const exMax = Math.max(1e-6, ...thrSolid.map((q) => excess(q[0], q[1])));
		/** glow level held from threshold on (all plot chapters) */
		const GTH = 0.8;
		const glowAt = (x: number, y: number) => GTH * Math.sqrt(Math.min(y, dashAt(Math.min(x, JTH))) / dashTh);
		const modeSeries = plotOf('modes')?.series ?? [];
		const modeCur = modeSeries.map((s) => {
			const m = /([\d][\d\s,]*)\s*A\/cm/.exec(s.name ?? '');
			return m ? Number(m[1].replace(/[\s,]/g, '')) : NaN;
		});
		const modePeak = modeSeries.map((_, i) => Math.max(0, ...ptsOf('modes', i).map((q) => q[1])));
		const peakMax = Math.max(1e-6, ...modePeak);

		// ---------------------------------------------------------------------------- materials and registry
		const disposables: { dispose(): void }[] = [];
		const keep = <T extends { dispose(): void }>(x: T): T => (disposables.push(x), x);
		const G = <T extends THREE_NS.BufferGeometry>(g: T): T => keep(g);
		const root = new THREE.Group();
		scene.add(root);

		// studio environment (soft boxes on a dark room) for metal and polished faces
		const studio = (() => {
			const S = 256;
			const face = (base: [string, string, string], boxes: [number, number, number, number, number][]) => {
				const cv = document.createElement('canvas');
				cv.width = cv.height = S;
				const g = cv.getContext('2d')!;
				const gr = g.createLinearGradient(0, 0, 0, S);
				gr.addColorStop(0, base[0]);
				gr.addColorStop(0.5, base[1]);
				gr.addColorStop(1, base[2]);
				g.fillStyle = gr;
				g.fillRect(0, 0, S, S);
				for (const [x, y, bw, bh, a] of boxes) {
					const cx = (x + bw / 2) * S;
					const cy = (y + bh / 2) * S;
					const rg = g.createRadialGradient(cx, cy, 0, cx, cy, (Math.max(bw, bh) * S) / 2);
					rg.addColorStop(0, `rgba(255,255,255,${a})`);
					rg.addColorStop(0.55, `rgba(255,255,255,${a * 0.75})`);
					rg.addColorStop(1, 'rgba(255,255,255,0)');
					g.fillStyle = rg;
					g.fillRect(x * S, y * S, bw * S, bh * S);
				}
				return cv;
			};
			const side: [string, string, string] = ['#9a9da2', '#3e4044', '#0e0f10'];
			const t = new THREE.CubeTexture([
				face(side, [[0.12, 0.1, 0.76, 0.6, 1]]),
				face(side, [[0.12, 0.1, 0.76, 0.6, 1]]),
				face(['#55585d', '#55585d', '#55585d'], [[0.18, 0.18, 0.64, 0.64, 1]]),
				face(['#0b0b0c', '#0b0b0c', '#0b0b0c'], []),
				face(side, [[0.06, 0.08, 0.88, 0.16, 0.95]]),
				face(side, [[0.14, 0.14, 0.18, 0.6, 0.55], [0.68, 0.14, 0.18, 0.6, 0.55]])
			]);
			t.colorSpace = THREE.SRGBColorSpace;
			t.needsUpdate = true;
			return keep(t);
		})();

		/** a material with its highlight id (part id or info id) and base opacity */
		interface M {
			m: THREE_NS.MeshPhysicalMaterial;
			id: string;
			base: number;
			trans: boolean;
			/** emissive set by the scene this frame (thermal or junction light), before highlight */
			glow: THREE_NS.Color | null;
			gi: number;
		}
		const mats: M[] = [];
		const mk = (id: string, lookId = id, extra: Partial<THREE_NS.MeshPhysicalMaterialParameters> = {}): M => {
			const lk = look(lookId);
			const op = num(lk.opacity, 1);
			const m = keep(
				new THREE.MeshPhysicalMaterial({
					color: lk.color ?? '#888888',
					metalness: num(lk.metal, 0),
					roughness: num(lk.rough, 0.5),
					transparent: op < 1,
					opacity: op,
					envMap: studio,
					...extra
				})
			);
			const r: M = { m, id, base: m.opacity, trans: m.transparent, glow: null, gi: 0 };
			mats.push(r);
			return r;
		};
		/** set the opacity of a material (fraction of its base) and the visibility of the meshes that use it */
		const setO = (x: M, o: number) => {
			const op = x.base * o;
			const trans = x.trans || op < 0.999;
			if (x.m.transparent !== trans) {
				x.m.transparent = trans;
				x.m.needsUpdate = true;
			}
			x.m.opacity = op;
			x.m.visible = op > 0.004;
		};

		/** pickable meshes: userData.part (spec part id) or userData.info (PickInfo); soft = only when nothing solid is hit */
		const picks: { mesh: THREE_NS.Mesh; soft: boolean; on: () => boolean }[] = [];
		const pickable = (mesh: THREE_NS.Mesh, on: () => boolean, soft = false) => picks.push({ mesh, soft, on });
		const mesh = (g: THREE_NS.BufferGeometry, x: M, part?: string) => {
			const o = new THREE.Mesh(g, x.m);
			if (part) o.userData.part = part;
			return o;
		};
		const unitBox = G(new THREE.BoxGeometry(1, 1, 1));
		const place = (o: THREE_NS.Object3D, c: V3, s: V3) => {
			o.position.set(c[0], c[1], c[2]);
			o.scale.set(Math.max(1e-5, s[0]), Math.max(1e-5, s[1]), Math.max(1e-5, s[2]));
		};

		// ---------------------------------------------------------------------------- wafer (cut-away front face)
		// Section view: the front (+z) face of the slab is drawn as a cut, so the p skin shows as a frame around the n core.
		const waferG = new THREE.Group();
		root.add(waferG);
		const mWafer = mk('wafer');
		const mSkin = mk('zn_skin');
		const coreBox = mesh(unitBox, mWafer, 'wafer');
		const skinTop = mesh(unitBox, mSkin, 'zn_skin');
		const skinBot = mesh(unitBox, mSkin, 'zn_skin');
		const skinL = mesh(unitBox, mSkin, 'zn_skin');
		const skinR = mesh(unitBox, mSkin, 'zn_skin');
		const skinB = mesh(unitBox, mSkin, 'zn_skin');
		// cut variant (skin depth fixed): top / bottom skin and core with the square hole the piece leaves
		const holed = (x0: number, x1: number, z0: number, z1: number, y0: number, y1: number) => {
			const sh = new THREE.Shape();
			// shape (x, s) -> world (x, z = -s) after rotateX(-90 deg); extrusion -> world y
			sh.moveTo(x0, -z1);
			sh.lineTo(x1, -z1);
			sh.lineTo(x1, -z0);
			sh.lineTo(x0, -z0);
			sh.lineTo(x0, -z1);
			const hp = new THREE.Path();
			hp.moveTo(-HE, -HE);
			hp.lineTo(-HE, HE);
			hp.lineTo(HE, HE);
			hp.lineTo(HE, -HE);
			hp.lineTo(-HE, -HE);
			sh.holes.push(hp);
			return G(new THREE.ExtrudeGeometry(sh, { depth: y1 - y0, bevelEnabled: false }).rotateX(-Math.PI / 2).translate(0, y0, 0));
		};
		const hTop = mesh(holed(-WX / 2, WX / 2, -WZ / 2, WZ / 2, WY - skinD, WY), mSkin, 'zn_skin');
		const hBot = mesh(holed(-WX / 2, WX / 2, -WZ / 2, WZ / 2, 0, skinD), mSkin, 'zn_skin');
		const hCore = mesh(holed(-WX / 2 + skinD, WX / 2 - skinD, -WZ / 2 + skinD, WZ / 2, skinD, WY - skinD), mWafer, 'wafer');
		waferG.add(coreBox, skinTop, skinBot, skinL, skinR, skinB, hTop, hBot, hCore);
		for (const o of [coreBox, skinTop, skinBot, skinL, skinR, skinB, hTop, hBot, hCore]) pickable(o, () => o.visible && mWafer.m.opacity > 0.3);
		// kerf outline of the piece on the top face
		const kerfMat = keep(new THREE.LineBasicMaterial({ color: '#cfd5dc', transparent: true, opacity: 0 }));
		const kerf = new THREE.LineSegments(G(new THREE.EdgesGeometry(new THREE.BoxGeometry(E, WY, E))), kerfMat);
		kerf.position.y = WY / 2;
		kerf.scale.set(1.004, 1.004, 1.004);
		waferG.add(kerf);

		// ---------------------------------------------------------------------------- sealed quartz ampoule
		const mAmp = mk('quartz_ampoule', 'quartz_ampoule', { depthWrite: false, side: THREE.DoubleSide, clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 2 });
		const capLen = Math.max(0.01, ampL - 2 * ampR);
		const amp = mesh(G(new THREE.CapsuleGeometry(ampR, capLen, 12, 48).rotateZ(Math.PI / 2)), mAmp, 'quartz_ampoule');
		amp.renderOrder = 5;
		const ampG = new THREE.Group();
		ampG.add(amp);
		root.add(ampG);
		pickable(amp, () => amp.visible && mAmp.m.opacity > 0.05, true);
		const heatLight = new THREE.PointLight('#ff8a3a', 0, 12, 2);
		root.add(heatLight);

		// ---------------------------------------------------------------------------- cut piece of the patent example
		const pieceInfo: PickInfo = {
			id: 'patent_piece',
			label: 'Cut piece, patent example',
			detail: [
				'One junction kept, about 0.1 mm below the top; bottom skin ground away (US 3,245,002 col. 3:45-50).',
				"The letter's diodes: about 0.4 mm cubes, junction through the centre (p.366). The model continues with that cube.",
				'Junction band drawn about 100x thicker than scale.'
			]
		};
		const pieceG = new THREE.Group();
		root.add(pieceG);
		const mPSkin = mk('patent_piece', 'zn_skin');
		const mPCore = mk('patent_piece', 'wafer');
		const mPJ = mk('patent_piece', 'junction', { roughness: 0.6, metalness: 0 });
		const pTop = mesh(unitBox, mPSkin);
		const pCore = mesh(unitBox, mPCore);
		const pBot = mesh(unitBox, mPSkin);
		const pJ = mesh(unitBox, mPJ);
		pieceG.add(pTop, pCore, pBot, pJ);
		for (const o of [pTop, pCore, pBot, pJ]) {
			o.userData.info = pieceInfo;
			pickable(o, () => pieceG.visible && mPCore.m.opacity > 0.3);
		}

		// ---------------------------------------------------------------------------- the letter's cube
		const cubeG = new THREE.Group(); // base of the cube at its local y = 0
		root.add(cubeG);
		const mP = mk('p_region');
		const mN = mk('n_region');
		const mJ = mk('junction', 'junction', { metalness: 0, roughness: 0.6 });
		const pReg = mesh(unitBox, mP, 'p_region');
		const nReg = mesh(unitBox, mN, 'n_region');
		const jun = mesh(unitBox, mJ, 'junction');
		const jPick = new THREE.Mesh(unitBox, keep(new THREE.MeshBasicMaterial({ visible: false })));
		jPick.userData.part = 'junction';
		cubeG.add(pReg, nReg, jun, jPick);
		pickable(pReg, () => cubeG.visible && mP.m.opacity > 0.3);
		pickable(nReg, () => cubeG.visible && mN.m.opacity > 0.3);
		pickable(jPick, () => cubeG.visible && mJ.m.opacity > 0.3);
		// polished faces (front +x, back -x) and the plain side faces (shown only when emphasized)
		const mFront = mk('front_face', 'front_face', { envMapIntensity: 1.8, depthWrite: false });
		const mRear = mk('rear_face', 'rear_face', { envMapIntensity: 1.8, depthWrite: false });
		const faceGeo = G(new THREE.PlaneGeometry(E, E));
		const front = mesh(faceGeo, mFront, 'front_face');
		front.rotation.y = Math.PI / 2;
		const rear = mesh(faceGeo, mRear, 'rear_face');
		rear.rotation.y = -Math.PI / 2;
		front.renderOrder = rear.renderOrder = 3;
		const sideMat = keep(new THREE.MeshBasicMaterial({ color: '#3987e5', transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide }));
		const sideA = new THREE.Mesh(faceGeo, sideMat);
		const sideB = new THREE.Mesh(faceGeo, sideMat);
		sideA.userData.part = sideB.userData.part = 'side_faces';
		sideB.rotation.y = Math.PI;
		cubeG.add(front, rear, sideA, sideB);
		pickable(front, () => cubeG.visible && mFront.m.opacity > 0.15);
		pickable(rear, () => cubeG.visible && mRear.m.opacity > 0.15);
		let sidesPick = false;
		pickable(sideA, () => sidesPick && cubeG.visible);
		pickable(sideB, () => sidesPick && cubeG.visible);
		// glints on the polished faces
		const glintMat = (): THREE_NS.ShaderMaterial =>
			keep(
				new THREE.ShaderMaterial({
					uniforms: { uS: { value: -2 }, uI: { value: 0 }, uColor: { value: new THREE.Color('#ffffff') }, uLight: { value: 0 } },
					vertexShader: UV_VS,
					fragmentShader: GLINT_FS,
					transparent: true,
					depthWrite: false,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
		const glF = glintMat();
		const glR = glintMat();
		const glintF = new THREE.Mesh(faceGeo, glF);
		glintF.rotation.y = Math.PI / 2;
		const glintR = new THREE.Mesh(faceGeo, glR);
		glintR.rotation.y = -Math.PI / 2;
		glintF.renderOrder = glintR.renderOrder = 4;
		cubeG.add(glintF, glintR);
		// cavity axis: a faint arrow pair normal to the polished faces
		const axisInfo: PickInfo = { id: 'cavity_axis', label: 'Cavity axis', detail: 'Normal to the polished front and back faces, in the plane of the junction (letter p.366).' };
		const arrowMat = keep(new THREE.MeshBasicMaterial({ color: '#9aa3ad', transparent: true, opacity: 0, depthWrite: false }));
		const arrowsG = new THREE.Group();
		for (const s of [1, -1]) {
			const shaft = new THREE.Mesh(G(new THREE.CylinderGeometry(0.006, 0.006, 0.26, 10).rotateZ(Math.PI / 2)), arrowMat);
			shaft.position.set(s * (HE + 0.17), jY, 0);
			const head = new THREE.Mesh(G(new THREE.ConeGeometry(0.026, 0.07, 18).rotateZ(-s * (Math.PI / 2))), arrowMat);
			head.position.set(s * (HE + 0.335), jY, 0);
			const prox = new THREE.Mesh(G(new THREE.BoxGeometry(0.36, 0.08, 0.08)), keep(new THREE.MeshBasicMaterial({ visible: false })));
			prox.position.set(s * (HE + 0.19), jY, 0);
			prox.userData.info = axisInfo;
			arrowsG.add(shaft, head, prox);
			pickable(prox, () => arrowsG.visible && arrowMat.opacity > 0.2);
		}
		cubeG.add(arrowsG);

		// ---------------------------------------------------------------------------- emission (drawn red; 842 nm is IR)
		const glowTex = (stops: [number, string][]) => {
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
		const haloTex = glowTex([[0, 'rgba(255,120,90,1)'], [0.25, 'rgba(255,60,40,0.55)'], [0.6, 'rgba(255,20,10,0.16)'], [1, 'rgba(255,0,0,0)']]);
		const spotTex = glowTex([[0, 'rgba(255,255,255,1)'], [0.15, 'rgba(255,200,190,0.95)'], [0.4, 'rgba(255,50,30,0.45)'], [1, 'rgba(255,0,0,0)']]);
		const spriteMat = (t: THREE_NS.Texture) => keep(new THREE.SpriteMaterial({ map: t, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, opacity: 0 }));
		const haloMat = spriteMat(haloTex);
		const halo = new THREE.Sprite(haloMat);
		halo.position.set(0, jY, 0);
		halo.renderOrder = 8;
		const spotMatF = spriteMat(spotTex);
		const spotMatR = spriteMat(spotTex);
		const spotF = new THREE.Sprite(spotMatF);
		spotF.position.set(HE + 0.004, jY, 0);
		const spotR = new THREE.Sprite(spotMatR);
		spotR.position.set(-HE - 0.004, jY, 0);
		spotF.renderOrder = spotR.renderOrder = 9;
		cubeG.add(halo, spotF, spotR);

		const beamCol = look('beam').color || '#ff1a1a';
		const beamMats: THREE_NS.ShaderMaterial[] = [];
		const beamGeo = G(new THREE.PlaneGeometry(1, 1, 48, 6));
		const BEAM_TAN = Math.tan(6 * DEG); // illustrative horizontal spread (half angle); not stated for L-69 / L-70
		const BEAM_TAN_V = Math.tan(0.6 * DEG); // illustrative, thin in the vertical plane
		function beamSide(dir: 1 | -1) {
			const g = new THREE.Group();
			const mkB = (vert: boolean, w0: number, tn: number, tail: number) => {
				const m = keep(
					new THREE.ShaderMaterial({
						uniforms: {
							uLen: { value: 1 }, uW0: { value: w0 }, uTan: { value: tn }, uVert: { value: vert ? 1 : 0 },
							uColor: { value: new THREE.Color(beamCol) }, uI: { value: 0 }, uLight: { value: 0 }, uTail: { value: tail }
						},
						vertexShader: BEAM_VS,
						fragmentShader: BEAM_FS,
						transparent: true,
						depthWrite: false,
						side: THREE.DoubleSide,
						blending: THREE.AdditiveBlending,
						toneMapped: false
					})
				);
				beamMats.push(m);
				const o = new THREE.Mesh(beamGeo, m);
				o.frustumCulled = false;
				o.renderOrder = 7;
				g.add(o);
				return m;
			};
			const fan = mkB(false, E * 0.9, BEAM_TAN, 0.55);
			const rib = mkB(true, 0.03, BEAM_TAN_V, 0.6);
			const core = mkB(false, 0.05, 0.002, 0.7);
			const prox = new THREE.Mesh(G(new THREE.BoxGeometry(1, 0.06, 0.3).translate(0.5, 0, 0)), keep(new THREE.MeshBasicMaterial({ visible: false })));
			prox.userData.part = 'beam';
			g.add(prox);
			g.position.set(dir * (HE + 0.002), jY, 0);
			if (dir < 0) g.rotation.y = Math.PI;
			cubeG.add(g);
			return { g, fan, rib, core, prox };
		}
		const beamF = beamSide(1);
		const beamR = beamSide(-1);
		pickable(beamF.prox, () => beamF.g.visible && beamF.fan.uniforms.uI.value > 0.12);
		pickable(beamR.prox, () => beamR.g.visible && beamR.fan.uniforms.uI.value > 0.12);
		const redLight = new THREE.PointLight('#ff3020', 0, 6, 2);
		redLight.position.set(HE + 0.5, jY + 0.1, 0.3);
		cubeG.add(redLight);

		// ---------------------------------------------------------------------------- top contact, disc, lead
		const mContact = mk('top_contact', 'top_contact', { envMapIntensity: 1.4 });
		const contact = mesh(unitBox, mContact, 'top_contact');
		root.add(contact);
		pickable(contact, () => contact.visible && mContact.m.opacity > 0.3);
		const mDisc = mk('mount_disc', 'mount_disc', { envMapIntensity: 1.4 });
		const disc = mesh(G(new THREE.CylinderGeometry(discR, discR, discH, 96)), mDisc, 'mount_disc');
		root.add(disc);
		pickable(disc, () => disc.visible && mDisc.m.opacity > 0.3);
		// lead: up from the top contact, then off to the pulse source (plain wire stand-in)
		const leadTop = ctT + E;
		const leadRise = 1.0;
		const psuRight = psuP[0] + num(psuS[0], 3) / 2;
		const leadPath = (() => {
			const pts = [new THREE.Vector3(0, leadTop, 0), new THREE.Vector3(0, leadRise, 0), new THREE.Vector3(psuRight, leadRise, 0)];
			const r = 0.15;
			const path = new THREE.CurvePath<THREE_NS.Vector3>();
			const a = pts[1].clone().add(new THREE.Vector3(0, -r, 0));
			const b = pts[1].clone().add(new THREE.Vector3(-r, 0, 0));
			path.add(new THREE.LineCurve3(pts[0], a));
			path.add(new THREE.QuadraticBezierCurve3(a, pts[1], b));
			path.add(new THREE.LineCurve3(b, pts[2]));
			return path;
		})();
		const LEAD_SEG = 240;
		const LEAD_RAD = 8;
		const leadGeo = G(new THREE.TubeGeometry(leadPath, LEAD_SEG, leadR, LEAD_RAD, false));
		const mLead = mk('top_lead');
		const lead = mesh(leadGeo, mLead, 'top_lead');
		root.add(lead);
		// fat invisible proxy for picking the thin wire
		const leadProx = new THREE.Mesh(G(new THREE.TubeGeometry(leadPath, 60, 0.07, 6, false)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		leadProx.userData.part = 'top_lead';
		root.add(leadProx);
		pickable(leadProx, () => lead.visible && mLead.m.opacity > 0.3);
		const leadLen = leadPath.getLength();
		const leadFirst = Math.min(1, (leadRise - leadTop + 0.15 + 2.6) / leadLen); // contacts chapter: up to x = -2.6

		// ---------------------------------------------------------------------------- liquid nitrogen, pulse source
		const mLN = mk('ln2_bath', 'ln2_bath', { depthWrite: false, side: THREE.FrontSide, envMapIntensity: 0.5, clearcoat: 0.3, clearcoatRoughness: 0.2 });
		const lnBody = mesh(G(new THREE.CylinderGeometry(lnR, lnR, 1, 96, 1, true).translate(0, 0.5, 0)), mLN, 'ln2_bath');
		lnBody.renderOrder = 6;
		const mLNs = mk('ln2_bath', 'ln2_bath', { depthWrite: false, side: THREE.DoubleSide, envMapIntensity: 0.8, clearcoat: 0.5, clearcoatRoughness: 0.1 });
		const lnTop = mesh(G(new THREE.CircleGeometry(lnR, 96).rotateX(-Math.PI / 2)), mLNs, 'ln2_bath');
		lnTop.renderOrder = 6;
		const lnRingMat = keep(new THREE.LineBasicMaterial({ color: '#a9cfee', transparent: true, opacity: 0 }));
		const ringPts = Array.from({ length: 129 }, (_, i) => new THREE.Vector3(lnR * Math.cos((i / 128) * TAU), 0, lnR * Math.sin((i / 128) * TAU)));
		const lnRing = new THREE.Line(G(new THREE.BufferGeometry().setFromPoints(ringPts)), lnRingMat);
		const lnRingB = new THREE.Line(lnRing.geometry, lnRingMat);
		const lnG = new THREE.Group();
		lnG.add(lnBody, lnTop, lnRing, lnRingB);
		root.add(lnG);
		pickable(lnBody, () => lnG.visible && mLN.m.opacity > 0.02, true);
		pickable(lnTop, () => lnG.visible && mLN.m.opacity > 0.02, true);
		const lnBottom = lnY - lnH / 2;

		const mPsu = mk('pulse_source', 'pulse_source', { envMapIntensity: 0.6 });
		const psuGeo = G(new THREE.BoxGeometry(num(psuS[0], 3), num(psuS[1], 1.6), num(psuS[2], 1.6)));
		const psuBox = mesh(psuGeo, mPsu, 'pulse_source');
		const psuEdgeMat = keep(new THREE.LineBasicMaterial({ color: '#6c717b', transparent: true, opacity: 1 }));
		const psuEdges = new THREE.LineSegments(G(new THREE.EdgesGeometry(psuGeo)), psuEdgeMat);
		const psuG = new THREE.Group();
		psuG.add(psuBox, psuEdges);
		root.add(psuG);
		pickable(psuBox, () => psuG.visible && mPsu.m.opacity > 0.3);

		// ---------------------------------------------------------------------------- lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.75);
		const key = new THREE.DirectionalLight('#fff3e6', 2.3);
		key.position.set(6, 12, 9);
		const rim = new THREE.DirectionalLight('#bcd2ff', 1.3);
		rim.position.set(-13, 5, -9);
		const fill = new THREE.DirectionalLight('#ffffff', 0.5);
		fill.position.set(-4, -6, 12);
		root.add(hemi, key, rim, fill);

		// ---------------------------------------------------------------------------- camera
		const raycaster = new THREE.Raycaster();
		const v2 = new THREE.Vector2();
		const tmp = new THREE.Vector3();
		const tmp2 = new THREE.Vector3();
		const accent = new THREE.Color();
		const black = new THREE.Color(0, 0, 0);
		const heatCol = new THREE.Color('#ff6a1a');
		const junCol = new THREE.Color(look('junction').emissive || '#ff3020');
		const mix3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
		let shot: Shot & { rect: Rect } = { ...SHOTS.intro, rect: regions(w, h).full };

		function shotAt(p: number): Shot & { rect: Rect } {
			const R = regions(w, h);
			const id = chapterOf(p);
			const i = CHAPTER_IDS.indexOf(id);
			const q = cq(id, p);
			const cur = SHOTS[id];
			const prevId = CHAPTER_IDS[i - 1];
			const prev = prevId ? SHOTS[prevId] : null;
			const win = cur.win ?? [0, 0.5];
			const t = prev ? ease(seg(q, win[0], win[1])) : 1;
			const curAz = cur.az + cur.drift * (q - 0.5);
			const prevAz = prev ? prev.az + prev.drift * 0.5 : curAz;
			const rc = R[cur.region];
			const rp = prev ? R[prev.region] : rc;
			// phone plot chapters: aim a little higher so the lead clears the chapter line
			const lift = w < 700 && cur.region === 'plot' ? 0.2 * t : 0;
			const tt = mix3(prev?.t ?? cur.t, cur.t, t);
			return {
				t: [tt[0], tt[1] + lift, tt[2]],
				az: lerp(prevAz, curAz, t),
				el: lerp(prev?.el ?? cur.el, cur.el, t),
				R: [lerp(prev?.R[0] ?? cur.R[0], cur.R[0], t), lerp(prev?.R[1] ?? cur.R[1], cur.R[1], t)],
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
		/** longest beam (mm) from world point o along world direction dx (+1 / -1 in x) whose end stays inside [xmin, xmax]
		 *  in pane px and, for the rear beam, right of world x = wxMin */
		function beamClip(o: THREE_NS.Vector3, dx: number, xmin: number, xmax: number, wxMin: number): number {
			const ok = (L: number) => {
				if (o.x + dx * L < wxMin) return false;
				tmp2.set(o.x + dx * L, o.y, o.z).project(camera);
				const sx = ((tmp2.x + 1) / 2) * w;
				return sx >= xmin && sx <= xmax;
			};
			if (ok(beamL)) return beamL;
			let lo = 0;
			let hi2 = beamL;
			for (let i = 0; i < 16; i++) {
				const m = (lo + hi2) / 2;
				if (ok(m)) lo = m;
				else hi2 = m;
			}
			return lo;
		}

		function applyTheme() {
			const light = theme === 'light';
			accent.set(light ? '#2a78d6' : '#3987e5');
			for (const m of beamMats) {
				m.uniforms.uLight.value = light ? 1 : 0;
				m.uniforms.uColor.value.set(light ? '#d0180e' : beamCol);
				m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			for (const m of [glF, glR]) {
				m.uniforms.uLight.value = light ? 1 : 0;
				m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			for (const m of [haloMat, spotMatF, spotMatR]) m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			psuEdgeMat.color.set(light ? '#8d9098' : '#6c717b');
			kerfMat.color.set(light ? '#3d434b' : '#cfd5dc');
			arrowMat.color.set(light ? '#5b6470' : '#9aa3ad');
			lnRingMat.color.set(light ? '#5d8fbf' : '#a9cfee');
			hemi.intensity = light ? 0.95 : 0.75;
		}
		applyTheme();

		// ---------------------------------------------------------------------------- emission state
		/** slowed pulse train inside a chapter: 9 pulses over q in [0, 0.9], then held on (frozen inside one pulse); the
		 *  plot chapters also hold on once their curve is drawn, so a finished curve never sits beside a dark diode */
		const pulse = (q: number): number => {
			if (q >= 0.9) return 1;
			const s = (q / 0.9) * 9;
			const f = s - Math.floor(s);
			return seg(f, 0, 0.03) * (1 - seg(f, 0.82, 0.86));
		};
		interface Em {
			G: number; // spontaneous glow 0..1
			B: number; // beam 0..1
			on: number; // pulse 0..1
		}
		function emission(p: number): Em {
			const id = chapterOf(p);
			const q = cq(id, p);
			if (id === 'cold') {
				// first pulses at the lowest plotted current density of FIG. 3
				const g = thrSolid.length ? glowAt(thrSolid[0][0], thrSolid[0][1]) * seg(q, 0.7, 0.78) : 0;
				return { G: g, B: 0, on: q >= 0.7 ? pulse(seg(q, 0.7, 1) * 0.9) : 0 };
			}
			if (id === 'threshold') {
				// drive = the plot pen on the measured curve (first point while the axes draw); held on once it is drawn
				const pn = penAt(spec, 'threshold', p)[0];
				const x = pn?.x ?? thrSolid[0]?.[0] ?? 1500;
				const y = pn?.y ?? thrSolid[0]?.[1] ?? 0.2;
				const done = (revealAt(spec, 'threshold', p)[0] ?? 0) >= 1;
				return { G: glowAt(x, y), B: Math.sqrt(excess(x, y) / exMax), on: done ? 1 : pulse(q) };
			}
			if (id === 'spectrum') {
				const rv = revealAt(spec, 'spectrum', p);
				const above = seg(rv[1] ?? 0, 0, 0.06);
				// currents not printed: a below-threshold glow, then the threshold-level glow with the beam
				return { G: lerp(0.5, GTH, above), B: 0.85 * above, on: (rv[1] ?? 0) >= 1 ? 1 : pulse(q) };
			}
			if (id === 'modes') {
				const rv = revealAt(spec, 'modes', p);
				let i = 0;
				for (let j = 0; j < rv.length; j++) if (rv[j] > 0) i = j;
				const pk = modePeak[i] ?? 0;
				const above = Number.isFinite(modeCur[i]) ? modeCur[i] > JTH : i > 0;
				// glow below threshold scales with the curve's peak against the first above-threshold curve; held above
				const firstAbove = modeCur.findIndex((c) => c > JTH);
				const pkTh = Math.max(1e-6, modePeak[firstAbove >= 0 ? firstAbove : 0] ?? 1);
				const G = above ? GTH : GTH * Math.sqrt(Math.min(1, pk / pkTh));
				return { G, B: above ? Math.sqrt(pk / peakMax) : 0, on: (rv[rv.length - 1] ?? 0) >= 1 ? 1 : pulse(q) };
			}
			return { G: 0, B: 0, on: 0 };
		}

		// ---------------------------------------------------------------------------- frame
		let lastP = 0;
		function frame(p: number) {
			lastP = p;
			const kk = p >= C.cold[1] ? clamp01(k) : 0;
			shot = shotAt(p);
			applyCamera(shot);
			const chap = chapterOf(p);
			const qi = cq('intro', p);
			const qw = cq('wafer', p);
			const qd = cq('diffuse', p);
			const qc = cq('cut', p);
			const qp = cq('polish', p);
			const qk = cq('contacts', p);
			const qo = cq('cold', p);
			// the finished diode holds through the end of the intro and leaves early in the wafer chapter
			const inIntro = p < C.wafer[0] || (p < C.wafer[1] && qw < 0.3);
			for (const x of mats) {
				x.glow = null;
				x.gi = 0;
			}

			// ---- intro: the finished diode floats in on its disc, then leaves for the process
			const introO = easeOut(seg(qi, 0, 0.35)) * (1 - ease(seg(qw, 0, 0.25)));
			const introLift = 0.9 * (1 - ease(seg(qi, 0, 0.6)));
			const introSpin = 1.1 * (1 - ease(seg(qi, 0, 0.7)));

			// ---- wafer and skin
			const waferIn = easeOut(seg(qw, 0.2, 0.45));
			const waferDrop = 1.4 * (1 - ease(seg(qw, 0.2, 0.8)));
			const d = skinD * ease(seg(qd, 0.35, 0.85));
			const cutOn = p >= C.cut[0] && qc >= 0.2; // the piece is separate from here on
			const waferO = p < C.wafer[0] ? 0 : waferIn * (1 - seg(qc, 0.38, 0.58));
			waferG.visible = waferO > 0.004;
			// the slab drops away from the cut piece
			waferG.position.y = waferY + waferDrop - 1.2 * ease(seg(qc, 0.25, 0.55));
			setO(mWafer, waferO);
			setO(mSkin, waferO);
			const dd = cutOn ? skinD : d;
			const hasSkin = dd > 1e-4;
			coreBox.visible = !cutOn;
			skinTop.visible = skinBot.visible = !cutOn && hasSkin;
			skinL.visible = skinR.visible = skinB.visible = hasSkin;
			hTop.visible = hBot.visible = hCore.visible = cutOn;
			place(coreBox, [0, WY / 2, dd / 2], [WX - 2 * dd, WY - 2 * dd, WZ - dd]);
			place(skinTop, [0, WY - dd / 2, 0], [WX, dd, WZ]);
			place(skinBot, [0, dd / 2, 0], [WX, dd, WZ]);
			place(skinL, [-WX / 2 + dd / 2, WY / 2, 0], [dd, WY - 2 * dd, WZ]);
			place(skinR, [WX / 2 - dd / 2, WY / 2, 0], [dd, WY - 2 * dd, WZ]);
			place(skinB, [0, WY / 2, -WZ / 2 + dd / 2], [WX - 2 * dd, WY - 2 * dd, dd]);
			// thermal glow of the hot ampoule contents (about 1000 °C)
			const heat = seg(qd, 0.25, 0.42) * (1 - seg(qd, 0.8, 0.94));
			if (heat > 0) {
				mWafer.glow = mSkin.glow = heatCol;
				mWafer.gi = mSkin.gi = 0.55 * heat;
			}
			heatLight.intensity = heat * 6;
			heatLight.position.set(0, waferY + WY + 0.8, 0);
			// kerf outline
			kerfMat.opacity = seg(qc, 0.02, 0.12) * (1 - seg(qc, 0.18, 0.26));
			kerf.visible = kerfMat.opacity > 0.004;

			// ---- ampoule closes around the wafer, holds through the heat, then leaves
			const ampO = easeOut(seg(qd, 0, 0.25)) * (1 - seg(qd, 0.86, 1));
			setO(mAmp, ampO);
			ampG.visible = ampO > 0.004;
			ampG.position.set(6 * (1 - ease(seg(qd, 0, 0.32))), waferY + WY / 2, 0);

			// ---- cut piece (patent example): the slab drops away, the bottom skin is ground off, then the letter's cube
			const grind = ease(seg(qc, 0.45, 0.6));
			const pieceO = cutOn ? 1 - seg(qc, 0.64, 0.74) : 0;
			pieceG.visible = pieceO > 0.004;
			pieceG.position.y = waferY;
			for (const x of [mPSkin, mPCore]) setO(x, pieceO);
			// the piece's junction band leaves before the cube's band arrives (never two junctions at once)
			setO(mPJ, pieceO * (1 - seg(qc, 0.58, 0.64)));
			for (const x of [mPSkin, mPCore, mPJ]) x.m.depthWrite = pieceO > 0.99;
			const botH = skinD * (1 - grind);
			place(pTop, [0, WY - skinD / 2, 0], [E, skinD, E]);
			place(pJ, [0, WY - skinD, 0], [E * 1.002, jT, E * 1.002]);
			place(pCore, [0, (skinD + WY - skinD) / 2, 0], [E, WY - 2 * skinD, E]);
			place(pBot, [0, skinD - botH / 2, 0], [E, botH, E]);
			pBot.visible = botH > 1e-4;

			// ---- the letter's cube
			let cubeO: number;
			let cubeY: number;
			let polF: number;
			let polR: number;
			if (inIntro) {
				cubeO = introO;
				cubeY = introLift;
				polF = polR = 1;
			} else {
				cubeO = p >= C.cut[0] ? seg(qc, 0.62, 0.72) : 0;
				const pieceMid = waferY + (skinD + WY) / 2 - jY; // cube centred on the ground piece
				cubeY = lerp(pieceMid, 0, ease(seg(qc, 0.8, 1)));
				polF = ease(seg(qp, 0.05, 0.3));
				polR = ease(seg(qp, 0.5, 0.72));
			}
			cubeG.visible = cubeO > 0.004;
			cubeG.position.set(0, cubeY, 0);
			cubeG.rotation.y = inIntro ? introSpin : 0;
			for (const x of [mP, mN, mJ]) {
				setO(x, cubeO);
				x.m.depthWrite = cubeO > 0.99;
			}
			if (!inIntro && p < C.cut[1]) setO(mJ, cubeO * seg(qc, 0.66, 0.72));
			const jHalf = jT / 2;
			const pH = E - jY - jHalf;
			const nH = jY - jHalf;
			const ex = kk; // explode: p up, n down, faces out
			place(pReg, [0, jY + jHalf + pH / 2 + 0.28 * ex, 0], [E, pH, E]);
			place(nReg, [0, nH / 2 - 0.28 * ex, 0], [E, nH, E]);
			place(jun, [0, jY, 0], [E * 1.002, jT, E * 1.002]);
			place(jPick, [0, jY, 0], [E * 1.03, 0.04, E * 1.03]);
			front.position.set(HE + 0.001 + 0.3 * ex, E / 2, 0);
			rear.position.set(-HE - 0.001 - 0.3 * ex, E / 2, 0);
			setO(mFront, cubeO * polF);
			setO(mRear, cubeO * polR);
			sideA.position.set(0, E / 2, HE + 0.002);
			sideB.position.set(0, E / 2, -HE - 0.002);
			sidesPick = chap === 'polish' || hi.includes('side_faces');
			sideMat.opacity = hi.includes('side_faces') && cubeO > 0.3 ? 0.35 : 0;
			sideMat.color.copy(accent);
			sideA.visible = sideB.visible = cubeO > 0.004;
			// glints: front in the first half of the polish chapter, back in the second
			const gf = seg(qp, 0.1, 0.42);
			const gr = seg(qp, 0.58, 0.9);
			glF.uniforms.uS.value = lerp(-1.4, 1.4, gf);
			glF.uniforms.uI.value = p >= C.polish[0] && p < C.polish[1] ? Math.sin(Math.PI * gf) * 0.9 : 0;
			glR.uniforms.uS.value = lerp(-1.4, 1.4, gr);
			glR.uniforms.uI.value = p >= C.polish[0] && p < C.polish[1] ? Math.sin(Math.PI * gr) * 0.9 : 0;
			glintF.position.set(HE + 0.003 + 0.3 * ex, E / 2, 0);
			glintR.position.set(-HE - 0.003 - 0.3 * ex, E / 2, 0);
			glintF.visible = glF.uniforms.uI.value > 0.004;
			glintR.visible = glR.uniforms.uI.value > 0.004;
			// cavity axis arrows
			arrowMat.opacity = 0.75 * seg(qp, 0.2, 0.42) * (1 - seg(qk, 0, 0.2));
			arrowsG.visible = arrowMat.opacity > 0.004;

			// ---- top contact, disc, lead
			let contactO: number;
			let contactY: number;
			let discO: number;
			let discY: number;
			if (inIntro) {
				contactO = discO = introO;
				contactY = introLift + E + ctT / 2;
				discY = introLift - discH / 2;
			} else {
				contactO = p >= C.contacts[0] ? easeOut(seg(qk, 0.02, 0.2)) : 0;
				contactY = E + ctT / 2 + 0.8 * (1 - ease(seg(qk, 0.02, 0.35))) + 0.55 * ex;
				discO = p >= C.contacts[0] ? easeOut(seg(qk, 0.25, 0.42)) : 0;
				discY = -discH / 2 - 1.5 * (1 - ease(seg(qk, 0.25, 0.62))) - 0.5 * ex;
			}
			setO(mContact, contactO);
			contact.visible = contactO > 0.004;
			place(contact, [0, contactY, 0], [E, ctT, E]);
			contact.rotation.y = inIntro ? introSpin : 0;
			setO(mDisc, discO);
			disc.visible = discO > 0.004;
			disc.position.set(0, discY, 0);
			const leadF = p < C.contacts[0] ? 0 : lerp(leadFirst * ease(seg(qk, 0.55, 0.95)), 1, ease(seg(qo, 0.45, 0.85)));
			// phone plot chapters: the lead ends where it would run into the chapter line above the model strip
			let leadU = leadF;
			if (w < 700 && shot.region === 'plot' && leadU > 0) {
				const yMin = regions(w, h).plot[1] * h;
				const below = (u: number) => {
					leadPath.getPointAt(u, tmp2);
					tmp2.project(camera);
					return ((1 - tmp2.y) / 2) * h >= yMin;
				};
				if (!below(leadU)) {
					let lo = 0;
					let hi2 = leadU;
					for (let i = 0; i < 14; i++) {
						const m = (lo + hi2) / 2;
						if (below(m)) lo = m;
						else hi2 = m;
					}
					leadU = lo;
				}
			}
			const leadN = Math.floor(leadU * LEAD_SEG) * LEAD_RAD * 6;
			leadGeo.setDrawRange(0, leadN);
			const leadO = leadF > 0 ? 1 - seg(kk, 0, 0.12) : 0;
			setO(mLead, leadO);
			lead.visible = leadO > 0.004 && leadN > 0;
			leadProx.scale.setScalar(1);

			// ---- liquid nitrogen rises; pulse source arrives
			const lvl = p < C.cold[0] ? 0 : ease(seg(qo, 0.05, 0.55));
			const lnO = (lvl > 0 ? Math.min(1, lvl * 6) : 0) * (1 - kk);
			// plot chapters: the liquid stays but recedes (the near wall would otherwise veil the diode)
			const lnPlot = 1 - 0.6 * seg(p, C.threshold[0], C.threshold[0] + 0.015);
			setO(mLN, lnO * lnPlot);
			setO(mLNs, lnO * lnPlot);
			// rim outlines would cross the keyword and run behind the plot: gone in the plot chapters
			lnRingMat.opacity = 0.55 * lnO * (1 - seg(p, C.threshold[0], C.threshold[0] + 0.015));
			lnG.visible = lnO > 0.004;
			lnBody.position.y = lnBottom;
			lnBody.scale.set(1, Math.max(1e-4, lnH * lvl), 1);
			lnTop.position.y = lnBottom + lnH * lvl;
			lnRing.position.y = lnTop.position.y;
			lnRingB.position.y = lnBottom;
			const inPlot = seg(p, C.threshold[0], C.threshold[0] + 0.015);
			const psuO = (p < C.cold[0] ? 0 : easeOut(seg(qo, 0.3, 0.55))) * (1 - inPlot);
			setO(mPsu, psuO);
			psuEdgeMat.opacity = psuO;
			psuG.visible = psuO > 0.004;
			psuG.position.set(psuP[0] - 2 * (1 - ease(seg(qo, 0.3, 0.6))), psuP[1], psuP[2]);

			// ---- emission: pulses, spontaneous glow, beam out of both polished faces
			const em = emission(p);
			const live = (1 - kk) * (cubeO > 0.5 ? 1 : 0);
			const Gv = em.G * em.on * live;
			const Bv = em.B * em.on * live;
			const light = theme === 'light';
			haloMat.opacity = Math.min(1, (light ? 0.35 : 0.55) * Gv + 0.25 * Bv);
			halo.scale.setScalar(0.9 + 0.7 * Gv);
			halo.visible = haloMat.opacity > 0.004;
			if (Gv > 0.001 || Bv > 0.001) {
				mJ.glow = junCol;
				mJ.gi = 0.9 * Gv + 1.6 * Bv;
			}
			for (const [sm, sp] of [
				[spotMatF, spotF],
				[spotMatR, spotR]
			] as const) {
				sm.opacity = Math.min(1, Bv * 1.1);
				sp.scale.set(0.42 + 0.45 * Bv, 0.07 + 0.08 * Bv, 1);
				sp.visible = sm.opacity > 0.004;
			}
			const paneMin = 22;
			const plotting = w >= 700 && shot.region === 'plot';
			const xmaxF = plotting ? regions(w, h).plotBox[0] * w - 28 : w - 22;
			cubeG.updateMatrixWorld(true);
			tmp.set(HE, jY, 0);
			cubeG.localToWorld(tmp);
			const lenF = beamClip(tmp.clone(), 1, paneMin, xmaxF, -1e9);
			tmp.set(-HE, jY, 0);
			cubeG.localToWorld(tmp);
			const lenR = beamClip(tmp.clone(), -1, paneMin, w - 22, psuRight + 0.25);
			const hiBeam = hi.includes('beam');
			for (const [side, len] of [
				[beamF, lenF],
				[beamR, lenR]
			] as const) {
				const L = Math.max(0.001, len);
				for (const m of [side.fan, side.rib, side.core]) m.uniforms.uLen.value = L;
				side.fan.uniforms.uI.value = 0.75 * Bv;
				side.rib.uniforms.uI.value = 0.55 * Bv;
				side.core.uniforms.uI.value = Math.min(1, 1.3 * Bv);
				if (hiBeam && Bv > 0.05) {
					side.fan.uniforms.uColor.value.copy(accent);
				} else side.fan.uniforms.uColor.value.set(light ? '#d0180e' : beamCol);
				side.prox.scale.set(L, 1, 1);
				side.g.visible = Bv > 0.004;
			}
			redLight.intensity = Bv * 1.2;

			// ---- emphasis (hover / pinned) on top of the scene's own emissive
			const lit = (id: string) =>
				hi.includes(id) || (hi.includes('crystal') && (id === 'p_region' || id === 'n_region' || id === 'junction'));
			for (const x of mats) {
				const on = lit(x.id);
				x.m.emissive.copy(x.glow ?? black);
				x.m.emissiveIntensity = x.glow ? x.gi : 1;
				if (on) {
					x.m.emissive.lerp(accent, x.glow ? 0.35 : 1);
					if (!x.glow) x.m.emissiveIntensity = 0.28;
				}
			}
			if (hi.includes('ln2_bath') && lnG.visible) {
				mLN.m.opacity = Math.max(mLN.m.opacity, 0.32 * lnO);
				lnRingMat.opacity = Math.max(lnRingMat.opacity, 0.9 * lnO);
				lnRingMat.color.copy(accent);
			} else lnRingMat.color.set(light ? '#5d8fbf' : '#a9cfee');
			if (hi.includes('cavity_axis')) arrowMat.color.copy(accent);
			else arrowMat.color.set(light ? '#5b6470' : '#9aa3ad');
		}

		// ---------------------------------------------------------------------------- hover caveats (pick detail lines)
		const PULSES = 'Pulses drawn slowed and blinking; the letter used pulses of 5 to 20 µs.';
		const DETAIL: Record<string, (plotCh: boolean, ch: string) => string[]> = {
			junction: (pc, ch) => [
				'Drawn about 100x thicker than scale (patent example about 1000 Å).',
				...(ch === 'threshold' ? ['Glow follows the low-current line and holds at threshold; the beam is the excess above it (illustrative split).'] : []),
				...(pc ? [PULSES] : [])
			],
			beam: (pc) => [
				'Drawn red: 8420 Å is near-infrared. Spread illustrative.',
				'Leaves both polished faces (US 3,245,002 col. 6:26-28); the letter measured the front beam only.',
				...(pc ? [PULSES] : [])
			],
			ln2_bath: () => ['Patent: liquid air at about 77 K (US 3,245,002 col. 4:17-18); the letter prints no temperature.'],
			pulse_source: () => [PULSES],
			front_face: () => ['Light leaves both polished faces (US 3,245,002 col. 6:26-28); the letter measured on the front beam axis.']
		};

		// ---------------------------------------------------------------------------- handle
		const handle: ShowcaseHandle = {
			assembledAt: C.modes[0],
			orbit: { distance: [1.2, 40] },
			frame,
			highlight(ids) {
				hi = [...ids];
			},
			pick(x, y) {
				v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
				raycaster.setFromCamera(v2, camera);
				const cands = picks.filter((c) => c.on());
				const hits = raycaster.intersectObjects(
					cands.map((c) => c.mesh),
					false
				);
				const soft = new Set(cands.filter((c) => c.soft).map((c) => c.mesh));
				const hit = hits.find((q) => !soft.has(q.object as THREE_NS.Mesh)) ?? hits[0];
				if (!hit) return null;
				const info = hit.object.userData.info as PickInfo | undefined;
				if (info) return info;
				const id = hit.object.userData.part as string | undefined;
				if (!id) return null;
				const ch = chapterOf(lastP);
				if ((id === 'p_region' || id === 'n_region') && (ch === 'intro' || ch === 'cut')) return 'crystal';
				const plotCh = ch === 'threshold' || ch === 'spectrum' || ch === 'modes';
				const det = DETAIL[id]?.(plotCh, ch);
				return det && det.length ? { id, label: partOf(id)?.name ?? id, detail: det } : id;
			},
			anchor(id) {
				let ok = false;
				if (id === 'crystal' && cubeG.visible && mP.m.opacity > 0.5) {
					tmp.set(HE, E, HE);
					cubeG.localToWorld(tmp);
					ok = true;
				} else if (id === 'ln2_bath' && lnG.visible && mLN.m.opacity > 0.05) {
					tmp.set(lnR * 0.92, lnTop.position.y, 0);
					ok = true;
				} else if (id === 'beam' && beamF.g.visible && beamF.fan.uniforms.uI.value > 0.15) {
					const L = beamF.fan.uniforms.uLen.value as number;
					// phone: just right of the diode, above the beam, so the label fits to its right
					if (w < 700) tmp.set(HE + Math.min(0.3, L * 0.3), jY + 0.38, 0);
					else tmp.set(HE + Math.min(1.4, L * 0.7), jY + 0.05, 0);
					cubeG.localToWorld(tmp);
					ok = true;
				}
				if (!ok) return null;
				camera.updateMatrixWorld();
				tmp2.copy(tmp).applyMatrix4(camera.matrixWorldInverse);
				if (tmp2.z > -camera.near) return null;
				tmp.project(camera);
				const sx = ((tmp.x + 1) / 2) * w;
				const sy = ((1 - tmp.y) / 2) * h;
				if (sx < 0 || sx > w || sy < 0 || sy > h) return null;
				if (shot.region === 'plot') {
					const pb = regions(w, h).plotBox;
					if (sx > pb[0] * w - 170 && sy > pb[1] * h) return null;
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
