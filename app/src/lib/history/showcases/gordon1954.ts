// Scene module: ammonia beam maser, Gordon, Zeiger, Townes, Phys. Rev. 1954 (DevLog-017). Spec:
// data/history/showcases/gordon1954.yaml; contract ../showcase/types.ts.
// Units mm. x = beam axis, +x downstream (source -> focuser -> cavity), y up; origin = centre of the source's perforated
// end face. Focuser cross-section as seen looking downstream: V electrodes upper-left and lower-right, O electrodes
// upper-right and lower-left (letter Fig. 1, patent FIG. 6). Looking along +x with y up, "right" is +z.
//
// Sources fix the arrangement (letter Fig. 1, US 2,879,439 FIG. 4); sizes are the letter's (cavity 12 cm) or the patent's
// example values; stand-ins (source tube, chamber, pump stub, guides) are plain shapes that add no detail. Not drawn
// (withheld): the beam after the cavity (molecules fade inside it), coupling holes, voltage source, klystron, detector.
//
// Physics on screen: molecules leave the source as a half-and-half mix of the two inversion states (illustrative; the
// letter gives no populations). With the focuser voltage off they fly straight. With it on, upper-state molecules feel
// a radial inward force and are brought onto the cavity entrance hole; lower-state molecules are pushed outward and
// are lost before the focuser end. Inside the cavity, and only there, upper-state molecules emit and become lower-state
// molecules; how many follows the emission level (spectrum chapter: the digitized Fig. 3b value under the plot pen).
// Particles are seeded and every position is a pure function of p (stream time tau = p * NT).
import type * as THREE_NS from 'three';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import { AXES_END, staggerK } from '../showcase/plot';
import type { ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type V3 = [number, number, number];
type Rect = [number, number, number, number]; // pane fractions x0, y0, x1, y1
type Geo = Record<string, unknown>;

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);

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

// ------------------------------------------------------------------------------------------------ shots (camera)
// az: degrees from +z toward +x (0 = side view, beam left to right); el: degrees above the horizon. R = [half width,
// half height] (mm) around the target that must fit the shot's region. `then`: a second shot eased to inside the chapter.
interface Shot {
	t: V3;
	az: number;
	el: number;
	R: [number, number];
	drift: number;
	region: 'full' | 'plot';
	then?: { q: [number, number]; t: V3; az: number; el: number; R: [number, number] };
}
const SHOTS: Record<string, Shot> = {
	intro: { t: [180, 5, 0], az: 26, el: 20, R: [300, 105], drift: 10, region: 'full' },
	source: { t: [-12, 0, 0], az: 60, el: 14, R: [34, 22], drift: 8, region: 'full' },
	focuser: {
		t: [228, 0, 0], az: 76, el: 12, R: [32, 30], drift: 4, region: 'full',
		then: { q: [0.55, 0.85], t: [125, 2, 0], az: 30, el: 16, R: [135, 78] }
	},
	select: { t: [118, 0, 0], az: 20, el: 14, R: [140, 26], drift: 4, region: 'plot' },
	cavity: { t: [300, 20, 0], az: 32, el: 20, R: [105, 72], drift: 6, region: 'full' },
	emission: { t: [262, 18, 0], az: 22, el: 15, R: [150, 66], drift: 6, region: 'full' },
	spectrum: { t: [296, 22, 0], az: 24, el: 15, R: [92, 72], drift: 4, region: 'plot' },
	oscillation: { t: [185, 16, 0], az: 26, el: 18, R: [245, 90], drift: 8, region: 'full' }
};
/** camera for the explode slider at k = 1 (the line-up spans x -130 ... 460 mm) */
const EXPLODED = { t: [168, 12, 0] as V3, az: 24, el: 18, R: [315, 112] as [number, number] };
const CHAPTER_IDS = ['intro', 'source', 'focuser', 'select', 'cavity', 'emission', 'spectrum', 'oscillation'];

function regions(w: number, h: number): { full: Rect; plot: Rect; plotBox: Rect } {
	if (w < 700) return { full: [0.04, 0.2, 0.96, 0.98], plot: [0.04, 0.17, 0.96, 0.43], plotBox: [0, 0.44, 1, 1] };
	const top = Math.min(0.24, 150 / Math.max(1, h));
	return { full: [0.03, top, 0.97, 0.97], plot: [0.03, top, 0.49, 0.97], plotBox: [0.5, 0.16, 1, 1] };
}

// ------------------------------------------------------------------------------------------------ shaders
// mode 0: cavity field, alpha follows sin(pi u) along the cavity axis (u = 0 .. 1), flat across.
// mode 1 / 2: microwave power in a guide, stripes travelling down (1, into the cavity) or up (2, out of it).
const FX_VS = /* glsl */ `
varying vec3 vN; varying vec3 vV; varying vec3 vP;
void main() {
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	vN = normalize(normalMatrix * normal);
	vV = normalize(-mv.xyz);
	vP = position;
	gl_Position = projectionMatrix * mv;
}`;
const FX_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uLight; uniform float uK; uniform float uMode;
uniform float uLen; uniform float uPhase; uniform float uLam;
varying vec3 vN; varying vec3 vV; varying vec3 vP;
void main() {
	float a;
	if (uMode < 0.5) {
		float u = clamp(vP.x / uLen + 0.5, 0.0, 1.0);
		float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
		a = uI * sin(3.14159265 * u) * (0.35 + 0.65 * c);
	} else {
		float y = vP.y;
		float dir = uMode < 1.5 ? 1.0 : -1.0;
		float s = 0.5 + 0.5 * cos(6.2831853 * (y / uLam + dir * uPhase));
		float ends = smoothstep(0.0, 6.0, y) * (1.0 - smoothstep(uLen - 6.0, uLen, y));
		a = uI * (0.22 + 0.78 * s * s) * ends;
	}
	a = clamp(a * uK, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a) : vec4(uColor * a, a);
}`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('gordon1954 is a 3D scene');
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
			intro: [0, 0.08], source: [0.08, 0.2], focuser: [0.2, 0.34], select: [0.34, 0.48], cavity: [0.48, 0.58],
			emission: [0.58, 0.7], spectrum: [0.7, 0.86], oscillation: [0.86, 1]
		};
		const C = Object.fromEntries(
			CHAPTER_IDS.map((id) => [id, (spec.chapters.find((c) => c.id === id)?.p ?? fallback[id]) as [number, number]])
		) as Record<string, [number, number]>;
		const cq = (id: string, p: number) => seg(p, C[id][0], C[id][1]);

		// ---------------------------------------------------------------------------- dimensions from the spec
		const srcG = geo('nh3_source');
		const srcR = num(srcG.outer_diameter, 16) / 2;
		const srcWall = num(srcG.wall, 1.5);
		const srcL = num(srcG.length, 60);
		const apG = geo('apertures');
		const holes = (Array.isArray(apG.holes_norm) ? apG.holes_norm : []) as [number, number][];
		const holeRn = num(apG.hole_radius_norm, 0.079);
		const focG = geo('focuser_hv');
		const focL = num(focG.length, 200);
		const profile = (Array.isArray(focG.profile_mm_upper_left) ? focG.profile_mm_upper_left : []) as [number, number][];
		const focX = at('focuser_hv', [130, 0, 0])[0];
		const XF0 = focX - focL / 2;
		const XF1 = focX + focL / 2;
		const cavG = geo('cavity');
		const cavRi = num(cavG.inner_diameter, 15.24) / 2;
		const cavRo = cavRi + num(cavG.wall, 1.5);
		const cavL = num(cavG.length, 120);
		const cavX = at('cavity', [310, 0, 0])[0];
		const XC0 = cavX - cavL / 2;
		const XC1 = cavX + cavL / 2;
		const apR = num(geo('entry_aperture').diameter, 10.16) / 2;
		const outG = geo('output_guide');
		const outA = at('output_guide', [280, 9.1, 0]);
		const outIn = (Array.isArray(outG.inner) ? outG.inner : [10, 5]) as number[];
		const outLen = num(outG.length, 90);
		const inG = geo('input_guide');
		const inA = at('input_guide', [373.5, -9.1, 0]);
		const inIn = (Array.isArray(inG.inner) ? inG.inner : [10, 5]) as number[];
		const inLen = num(inG.length, 110);
		const gWall = num(outG.wall, 1);
		const chG = geo('vacuum_chamber');
		const chX = (Array.isArray(chG.x) ? chG.x : [-20, 400]) as number[];
		const chHH = num(chG.half_height, 60);
		const chHD = num(chG.half_depth, 60);
		const pumpG = geo('pump_port');
		const pumpA = at('pump_port', [330, -60, 0]);
		const pumpR = num(pumpG.outer_diameter, 30) / 2;
		const pumpL = num(pumpG.length, 40);

		// ---------------------------------------------------------------------------- bodies
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
			picks: THREE_NS.Object3D[];
			o: number;
		}
		const bodies = new Map<string, Body>();
		function body(id: string, obj: THREE_NS.Object3D, parent: THREE_NS.Object3D = root): Body {
			const b: Body = { id, obj, mats: [], picks: [], o: 1 };
			obj.traverse((n) => {
				const m = (n as THREE_NS.Mesh).material as THREE_NS.MeshStandardMaterial | undefined;
				if ((n as THREE_NS.Mesh).isMesh && m && 'emissive' in m && !b.mats.some((x) => x.m === m))
					b.mats.push({ m, base: m.opacity, trans: m.transparent });
				if (((n as THREE_NS.Mesh).isMesh || (n as THREE_NS.LineSegments).isLineSegments) && !n.userData.nopick) {
					n.userData.part = id;
					b.picks.push(n);
				}
			});
			parent.add(obj);
			bodies.set(id, b);
			return b;
		}
		// studio environment (soft boxes on a dark room) for the module's own PBR materials: long, clean highlights on
		// the electrodes, tubes and copper; converted to PMREM by the renderer on first use
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
				// soft boxes: bright core fading to the edge (gives metals a gradient instead of a flat fill)
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
		const std = (id: string, extra: Partial<THREE_NS.MeshStandardMaterialParameters> = {}) => {
			const lk = look(id);
			const op = num(lk.opacity, 1);
			return keep(
				new THREE.MeshStandardMaterial({
					color: lk.color || '#888888',
					metalness: num(lk.metal, 0),
					roughness: num(lk.rough, 0.5),
					transparent: op < 1,
					opacity: op,
					envMap: studio,
					...extra
				})
			);
		};
		const glows: { m: THREE_NS.ShaderMaterial; dark: string; light: string; lightK: number }[] = [];
		const fx = (mode: number, dark: string, light: string, len: number, lightK = 1) => {
			const m = keep(
				new THREE.ShaderMaterial({
					uniforms: {
						uColor: { value: new THREE.Color(dark) },
						uI: { value: 0 },
						uLight: { value: 0 },
						uK: { value: 1 },
						uMode: { value: mode },
						uLen: { value: len },
						uPhase: { value: 0 },
						uLam: { value: 14 }
					},
					vertexShader: FX_VS,
					fragmentShader: FX_FS,
					transparent: true,
					depthWrite: false,
					side: THREE.DoubleSide,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
			glows.push({ m, dark, light, lightK });
			return m;
		};
		/** annular sector in the y-z plane (angle phi from +z toward +y), extruded along +x from 0 to len */
		function sectorGeo(r0: number, r1: number, a0: number, a1: number, len: number, segs = 96) {
			const s = new THREE.Shape();
			const P = (r: number, a: number): [number, number] => [-r * Math.cos(a), r * Math.sin(a)];
			const n = Math.max(4, Math.round((segs * (a1 - a0)) / TAU));
			s.moveTo(...P(r1, a0));
			for (let i = 1; i <= n; i++) s.lineTo(...P(r1, a0 + ((a1 - a0) * i) / n));
			for (let i = n; i >= 0; i--) s.lineTo(...P(r0, a0 + ((a1 - a0) * i) / n));
			s.closePath();
			// shape (u, v) -> world (z = -u, y = v) after rotateY(90 deg); extrusion -> world +x
			return G(new THREE.ExtrudeGeometry(s, { depth: len, bevelEnabled: false, curveSegments: 4 }).rotateY(Math.PI / 2));
		}
		const unitCylX = (r: number, len: number, segs = 48, open = true) =>
			G(new THREE.CylinderGeometry(r, r, len, segs, 1, open).rotateZ(-Math.PI / 2));

		// ---------------------------------------------------------------------------- source tube + perforated face
		const srcMat = std('nh3_source', { side: THREE.DoubleSide });
		const srcGroup = new THREE.Group();
		{
			const outer = new THREE.Mesh(unitCylX(srcR, srcL, 64), srcMat);
			outer.position.x = -srcL / 2;
			const inner = new THREE.Mesh(unitCylX(srcR - srcWall, srcL, 64), srcMat);
			inner.position.x = -srcL / 2;
			const back = new THREE.Mesh(G(new THREE.RingGeometry(srcR - srcWall, srcR, 64).rotateY(-Math.PI / 2)), srcMat);
			back.position.x = -srcL;
			srcGroup.add(outer, inner, back);
		}
		const source = body('nh3_source', srcGroup);
		const apGroup = new THREE.Group();
		{
			const face = new THREE.Shape().absarc(0, 0, srcR, 0, TAU, false);
			// FIG. 5 is a view looking upstream (section 5-5): drawing x right -> world -z, drawing y up -> world y
			for (const [xn, yn] of holes) face.holes.push(new THREE.Path().absarc(xn * srcR, yn * srcR, holeRn * srcR, 0, TAU, true));
			const faceGeo = G(new THREE.ShapeGeometry(face, 24).rotateY(Math.PI / 2)); // shape x -> world -z, normal -> +x
			const faceMesh = new THREE.Mesh(faceGeo, std('nh3_source', { side: THREE.DoubleSide }));
			const darkMat = std('apertures');
			const dark = nopick(new THREE.Mesh(G(new THREE.CircleGeometry(srcR - srcWall, 48).rotateY(Math.PI / 2)), darkMat));
			dark.position.x = -0.8;
			apGroup.add(faceMesh, dark);
		}
		const apertures = body('apertures', apGroup);

		// ---------------------------------------------------------------------------- focuser electrodes
		// four extruded profiles (letter Fig. 1 cross-section scaled to the patent's 2 cm); each electrode moves radially
		// on its own (slide in, explode)
		interface Electrode {
			mesh: THREE_NS.Mesh;
			mat: THREE_NS.MeshStandardMaterial;
			id: string;
			near: boolean; // on the camera side (+z): ghosted in the state-selection chapter so the beam inside shows
			dir: [number, number]; // radial unit direction (y, z)
			order: number;
		}
		const electrodes: Electrode[] = [];
		function electrodeGeo(sz: number, sy: number) {
			const s = new THREE.Shape();
			profile.forEach(([a, b], i) => {
				const z = sz * a;
				const y = sy * b;
				if (i === 0) s.moveTo(-z, y);
				else s.lineTo(-z, y);
			});
			s.closePath();
			return G(new THREE.ExtrudeGeometry(s, { depth: focL, bevelEnabled: false, curveSegments: 4 }).rotateY(Math.PI / 2));
		}
		const hvGroup = new THREE.Group();
		const gndGroup = new THREE.Group();
		// (sz, sy, group): upper-left V, lower-right V, upper-right O, lower-left O
		const EL: [number, number, 'hv' | 'gnd', number][] = [
			[1, 1, 'hv', 0],
			[-1, -1, 'hv', 2],
			[-1, 1, 'gnd', 1],
			[1, -1, 'gnd', 3]
		];
		if (profile.length > 2)
			for (const [sz, sy, g, order] of EL) {
				const mat = std(g === 'hv' ? 'focuser_hv' : 'focuser_ground', { side: THREE.DoubleSide });
				const mesh = new THREE.Mesh(electrodeGeo(sz, sy), mat);
				(g === 'hv' ? hvGroup : gndGroup).add(mesh);
				// profile upper-left: a < 0 (z), b > 0 (y): radial direction (y, z) = (sy, -sz) / sqrt 2
				electrodes.push({ mesh, mat, id: g === 'hv' ? 'focuser_hv' : 'focuser_ground', near: sz < 0, dir: [sy / Math.SQRT2, -sz / Math.SQRT2], order });
			}
		hvGroup.position.x = XF0;
		gndGroup.position.x = XF0;
		const focHV = body('focuser_hv', hvGroup);
		const focGnd = body('focuser_ground', gndGroup);
		// top of the upper-right O electrode / bottom of the lower-right V electrode (profile point with the largest |y|)
		const pTop = profile.reduce((m, q) => (q[1] > m[1] ? q : m), profile[0] ?? [-11.7, 21.5]);

		// ---------------------------------------------------------------------------- leads (FIG. 4: up to ground, down to the source)
		const leadMat = std('leads');
		const leadLen = chHH + 12 - pTop[1];
		const leadGeo = G(new THREE.CylinderGeometry(0.6, 0.6, 1, 10, 1, false).translate(0, 0.5, 0));
		const leadUp = new THREE.Mesh(leadGeo, leadMat);
		leadUp.position.set(focX, pTop[1], -pTop[0]); // O, upper-right (z > 0)
		const leadDn = new THREE.Mesh(leadGeo, leadMat);
		leadDn.position.set(focX, -pTop[1], -pTop[0]); // V, lower-right (z > 0)
		leadDn.rotation.x = Math.PI;
		const leadGroup = new THREE.Group();
		leadGroup.add(leadUp, leadDn);
		const leads = body('leads', leadGroup);

		// ---------------------------------------------------------------------------- chamber (stand-in) + pump stub
		const chMat = std('vacuum_chamber', { side: THREE.BackSide, depthWrite: false });
		const chGeo = G(new THREE.BoxGeometry(chX[1] - chX[0], 2 * chHH, 2 * chHD));
		const chEdgeMat = keep(new THREE.LineBasicMaterial({ color: '#6b7078', transparent: true, opacity: 0.5 }));
		const chGroup = new THREE.Group();
		const chFaces = nopick(new THREE.Mesh(chGeo, chMat));
		chFaces.renderOrder = -1;
		chGroup.add(chFaces, new THREE.LineSegments(G(new THREE.EdgesGeometry(chGeo)), chEdgeMat));
		chGroup.position.x = (chX[0] + chX[1]) / 2;
		const chamber = body('vacuum_chamber', chGroup);
		const pumpMat = std('pump_port', { depthWrite: false });
		const pumpGroup = new THREE.Group();
		{
			const tube = new THREE.Mesh(G(new THREE.CylinderGeometry(pumpR, pumpR, pumpL, 48, 1, true).translate(0, -pumpL / 2, 0)), pumpMat);
			const rimGeo = G(new THREE.EdgesGeometry(new THREE.CylinderGeometry(pumpR, pumpR, pumpL, 48, 1, true).translate(0, -pumpL / 2, 0), 30));
			pumpGroup.add(tube, nopick(new THREE.LineSegments(rimGeo, chEdgeMat)));
		}
		pumpGroup.position.set(pumpA[0], pumpA[1], pumpA[2]);
		const pump = body('pump_port', pumpGroup);

		// ---------------------------------------------------------------------------- cavity (cut away) + entry aperture
		const cut = 120 * DEG;
		const cutC = 28 * DEG; // centre of the opening: toward the camera side (+z), a little up
		const cuMat = std('cavity', { side: THREE.DoubleSide, envMapIntensity: 1.1 });
		const cuInMat = std('cavity', { side: THREE.DoubleSide, roughness: 0.4, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
		const lidMat = std('cavity', { side: THREE.DoubleSide, transparent: true, depthWrite: true });
		const cavGroup = new THREE.Group();
		const wallMesh = new THREE.Mesh(sectorGeo(cavRi, cavRo, cutC + cut / 2, cutC + TAU - cut / 2, cavL), cuMat);
		wallMesh.position.x = -cavL / 2;
		const lid = new THREE.Mesh(sectorGeo(cavRi, cavRo, cutC - cut / 2, cutC + cut / 2, cavL, 64), lidMat);
		lid.position.x = -cavL / 2;
		const capUp = new THREE.Mesh(G(new THREE.RingGeometry(apR, cavRo, 64).rotateY(-Math.PI / 2)), cuInMat);
		capUp.position.x = -cavL / 2;
		const capDn = new THREE.Mesh(G(new THREE.CircleGeometry(cavRo, 64).rotateY(Math.PI / 2)), cuInMat);
		capDn.position.x = cavL / 2;
		cavGroup.add(wallMesh, lid, capUp, capDn);
		cavGroup.position.x = cavX;
		const cavity = body('cavity', cavGroup);
		const lidBody = { m: lidMat, base: lidMat.opacity };
		cavity.mats = cavity.mats.filter((x) => x.m !== lidMat); // the lid fades on its own (cut-away)

		const accent = new THREE.Color();
		const apRingMat = keep(new THREE.MeshBasicMaterial({ color: '#3987e5', transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }));
		const apRing = nopick(new THREE.Mesh(G(new THREE.RingGeometry(apR - 0.1, apR + 0.6, 48).rotateY(-Math.PI / 2)), apRingMat));
		apRing.position.x = -0.15;
		const apProxy = new THREE.Mesh(G(new THREE.CircleGeometry(apR, 32).rotateY(-Math.PI / 2)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		apProxy.position.x = -0.1;
		const apHole = new THREE.Group();
		apHole.add(apProxy, apRing);
		apHole.position.x = XC0 - cavX;
		const entry = body('entry_aperture', apHole, cavGroup);

		// ---------------------------------------------------------------------------- guides (rectangular stand-ins)
		// output guide: from inside the cavity's top wall up (10 along x, 5 along z); input guide: against the downstream end
		// wall, from the cavity's bottom up (5 along x, 10 along z). Both run up out of the chamber (FIG. 4). Drawn cut away
		// on the camera side, like the cavity.
		function guide(id: string, ix: number, iz: number, len: number) {
			const g = new THREE.Group();
			const m = std(id);
			const ox = ix / 2 + gWall;
			const oz = iz / 2 + gWall;
			const wallX = G(new THREE.BoxGeometry(gWall, len, 2 * oz).translate(0, len / 2, 0));
			const wallZ = G(new THREE.BoxGeometry(ix, len, gWall).translate(0, len / 2, 0));
			const a = new THREE.Mesh(wallX, m);
			a.position.x = -ox + gWall / 2;
			const b = new THREE.Mesh(wallX, m);
			b.position.x = ox - gWall / 2;
			const c = new THREE.Mesh(wallZ, m);
			c.position.z = -oz + gWall / 2;
			// the near (+z) wall is left out: a cut-away, so the power inside shows
			g.add(a, b, c);
			return g;
		}
		const outBase = cavRi + 0.15; // starts in the top wall (its curved outer surface hides the joint)
		const outGroup = guide('output_guide', outIn[0] ?? 10, outIn[1] ?? 5, outLen + (outA[1] - outBase));
		outGroup.position.set(outA[0] - cavX, outBase, outA[2]);
		const outGuide = body('output_guide', outGroup, cavGroup);
		const inBase = inA[1]; // shares the cavity's downstream end wall, from the cavity bottom up (letter Fig. 1, FIG. 4)
		const inGroup = guide('input_guide', inIn[1] ?? 5, inIn[0] ?? 10, inLen);
		inGroup.position.set(inA[0] - cavX, inBase, inA[2]);
		const inGuide = body('input_guide', inGroup, cavGroup);

		// ---------------------------------------------------------------------------- effects: field, waves
		const fieldMat = fx(0, look('cavity_field').color || '#46dca5', '#14a874', cavL - 1, 0.55);
		const field = new THREE.Mesh(unitCylX(cavRi - 0.4, cavL - 1, 48, true), fieldMat);
		field.renderOrder = 5;
		const fieldGroup = new THREE.Group();
		fieldGroup.add(field);
		const fieldBody = body('cavity_field', fieldGroup, cavGroup);
		const inLenW = inLen - 2;
		const inWaveMat = fx(1, look('input_wave').color || '#c6a6fa', '#7b4fd0', inLenW, 0.7);
		const inWave = new THREE.Mesh(G(new THREE.BoxGeometry((inIn[1] ?? 5) - 0.6, inLenW, (inIn[0] ?? 10) - 0.6).translate(0, inLenW / 2, 0)), inWaveMat);
		inWave.renderOrder = 6;
		const inWaveGroup = new THREE.Group();
		inWaveGroup.add(inWave);
		inWaveGroup.position.y = 1;
		const inWaveBody = body('input_wave', inWaveGroup, inGroup);
		const outLenW = outLen - 2;
		const outWaveMat = fx(2, look('output_wave').color || '#46dca5', '#14a874', outLenW, 0.7);
		const outWave = new THREE.Mesh(G(new THREE.BoxGeometry((outIn[0] ?? 10) - 0.6, outLenW, (outIn[1] ?? 5) - 0.6).translate(0, outLenW / 2, 0)), outWaveMat);
		outWave.renderOrder = 6;
		const outWaveGroup = new THREE.Group();
		outWaveGroup.add(outWave);
		outWaveGroup.position.y = outA[1] - outBase + 1;
		const outWaveBody = body('output_wave', outWaveGroup, outGroup);

		// ---------------------------------------------------------------------------- molecules (seeded)
		const N = 440;
		const R = rng(1954);
		interface Mol {
			y0: number;
			z0: number;
			vy: number;
			vz: number;
			s: number; // speed factor (velocity spread)
			ph: number; // phase in the stream
			up: boolean; // upper inversion state at the source
			u: number; // emission threshold
			xc: number; // where it emits in the cavity
			// focuser exit (x = XF1) position and slope: straight flight and full voltage
			ey: [number, number];
			ez: [number, number];
			ey1: [number, number];
			ez1: [number, number];
			rIn: number; // radius at the focuser entrance
		}
		const KU = 1.4 / focL; // upper states: harmonic focusing, kappa L = 1.4 brings them onto the entrance hole
		const KL = 3.5 / focL; // lower states: pushed outward (drawn stronger so all leave before the focuser end)
		// clear radius of the model (the profile mirrored four times): nearest profile point to the axis, 5.85 mm
		const RCLEAR = profile.length ? Math.min(...profile.map(([a, b]) => Math.hypot(a, b))) : 5.85;
		const LPATH = XC1 + 20;
		const NT = 16; // stream traversals over the whole story (motion slowed, not to scale)
		const mols: Mol[] = [];
		const hp = holes.length ? holes : [[0, 0]];
		const solve = (r0: number, v: number, up: boolean, V: number, s: number): number => {
			if (V <= 0) return r0 + v * s;
			if (up) return r0 * Math.cos(KU * s) + (v / KU) * Math.sin(KU * s);
			return r0 * Math.cosh(KL * s) + (v / KL) * Math.sinh(KL * s);
		};
		const slope = (r0: number, v: number, up: boolean, s: number): number =>
			up ? -r0 * KU * Math.sin(KU * s) + v * Math.cos(KU * s) : r0 * KL * Math.sinh(KL * s) + v * Math.cosh(KL * s);
		for (let i = 0; i < N; i++) {
			const [xn, yn] = hp[Math.floor(R() * hp.length) % hp.length];
			const y0 = yn * srcR + (R() - 0.5) * 0.6;
			const z0 = -xn * srcR + (R() - 0.5) * 0.6;
			const th = 0.012 * Math.sqrt(R());
			const ps = R() * TAU;
			const vy = th * Math.sin(ps);
			const vz = th * Math.cos(ps);
			const up = i % 2 === 0; // half and half (illustrative)
			const ya = y0 + vy * XF0;
			const za = z0 + vz * XF0;
			mols.push({
				y0, z0, vy, vz,
				s: 0.85 + 0.3 * R(),
				ph: R(),
				up,
				u: R(),
				xc: XC0 + cavL * (0.25 + 0.5 * R()),
				ey: [ya + vy * focL, vy],
				ez: [za + vz * focL, vz],
				ey1: [solve(ya, vy, up, 1, focL), slope(ya, vy, up, focL)],
				ez1: [solve(za, vz, up, 1, focL), slope(za, vz, up, focL)],
				rIn: Math.hypot(ya, za)
			});
		}
		const molGeo = G(new THREE.IcosahedronGeometry(1, 1));
		const upMat = keep(new THREE.MeshBasicMaterial({ color: look('upper_state').color || '#f7962c', toneMapped: false }));
		const loMat = keep(new THREE.MeshBasicMaterial({ color: look('lower_state').color || '#4c9bf0', toneMapped: false }));
		const upI = new THREE.InstancedMesh(molGeo, upMat, N);
		const loI = new THREE.InstancedMesh(molGeo, loMat, N);
		upI.frustumCulled = false;
		loI.frustumCulled = false;
		upI.count = 0;
		loI.count = 0;
		const upBody = body('upper_state', upI);
		const loBody = body('lower_state', loI);
		const mtx = new THREE.Matrix4();

		// ---------------------------------------------------------------------------- lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.8);
		const key = new THREE.DirectionalLight('#fff3e6', 2.2);
		key.position.set(120, 220, 180);
		const rim = new THREE.DirectionalLight('#bcd2ff', 1.2);
		rim.position.set(-200, 80, -160);
		const fill = new THREE.DirectionalLight('#ffffff', 0.5);
		fill.position.set(-60, -100, 200);
		root.add(hemi, key, rim, fill);

		// ---------------------------------------------------------------------------- helpers
		const raycaster = new THREE.Raycaster();
		const v2 = new THREE.Vector2();
		const tmp = new THREE.Vector3();
		const tmp2 = new THREE.Vector3();
		const black = new THREE.Color(0, 0, 0);

		function setOpacity(b: Body, o: number) {
			const lit = hi.includes(b.id);
			const eff = lit && o < 0.3 && o > 0 ? 0.3 : o;
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
		function tint(b: Body) {
			const lit = hi.includes(b.id);
			for (const x of b.mats) {
				x.m.emissive.copy(lit ? accent : black);
				x.m.emissiveIntensity = lit ? 0.35 : 1;
			}
		}
		const mix3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
		const add3 = (a: V3, b: V3): V3 => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];

		// ---------------------------------------------------------------------------- camera
		let shot: Shot & { rect: Rect } = { ...SHOTS.intro, rect: regions(w, h).full };
		function settled(id: string, q: number): { t: V3; az: number; el: number; R: [number, number] } {
			const s = SHOTS[id];
			let r = { t: s.t, az: s.az + s.drift * (q - 0.5), el: s.el, R: s.R };
			if (s.then) {
				const u = ease(seg(q, s.then.q[0], s.then.q[1]));
				r = { t: mix3(r.t, s.then.t, u), az: lerp(r.az, s.then.az, u), el: lerp(r.el, s.then.el, u), R: [lerp(r.R[0], s.then.R[0], u), lerp(r.R[1], s.then.R[1], u)] };
			}
			return r;
		}
		function shotAt(p: number): Shot & { rect: Rect } {
			const RG = regions(w, h);
			const kx = ease(clamp01(k));
			let i = 0;
			for (let j = 0; j < CHAPTER_IDS.length; j++) if (p >= C[CHAPTER_IDS[j]][0]) i = j;
			const id = CHAPTER_IDS[i];
			const q = cq(id, p);
			const cur = SHOTS[id];
			const prevId = CHAPTER_IDS[i - 1];
			const t = prevId ? ease(seg(q, 0, cur.region === 'plot' ? 0.2 : 0.45)) : 1;
			const a = settled(id, q);
			const b = prevId ? settled(prevId, 1) : a;
			const rc = RG[cur.region];
			const rp = prevId ? RG[SHOTS[prevId].region] : rc;
			const ex = EXPLODED;
			return {
				t: mix3(mix3(b.t, a.t, t), ex.t, kx),
				az: lerp(lerp(b.az, a.az, t), ex.az, kx),
				el: lerp(lerp(b.el, a.el, t), ex.el, kx),
				R: [lerp(lerp(b.R[0], a.R[0], t), ex.R[0], kx), lerp(lerp(b.R[1], a.R[1], t), ex.R[1], kx)],
				drift: 0,
				region: cur.region,
				rect: [lerp(rp[0], rc[0], t), lerp(rp[1], rc[1], t), lerp(rp[2], rc[2], t), lerp(rp[3], rc[3], t)]
			};
		}
		let camDist = 300;
		function applyCamera(s: Shot & { rect: Rect }) {
			const [x0, y0, x1, y1] = s.rect;
			const tf = Math.tan((camera.fov * DEG) / 2);
			camDist = Math.max(s.R[0] / (tf * (w / h) * (x1 - x0)), s.R[1] / (tf * (y1 - y0)));
			const az = s.az * DEG;
			const el = s.el * DEG;
			camera.position.set(s.t[0] + camDist * Math.cos(el) * Math.sin(az), s.t[1] + camDist * Math.sin(el), s.t[2] + camDist * Math.cos(el) * Math.cos(az));
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
				g.m.uniforms.uK.value = light ? g.lightK : 1;
				g.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			chEdgeMat.color.set(light ? '#9a9ea6' : '#5d626b');
			chEdgeMat.opacity = light ? 0.7 : 0.55;
			hemi.intensity = light ? 1.0 : 0.8;
			upMat.color.set(light ? '#e07a10' : look('upper_state').color || '#f7962c');
			loMat.color.set(light ? '#2a78d6' : look('lower_state').color || '#4c9bf0');
		}
		applyTheme();

		// ---------------------------------------------------------------------------- plot pen (spectrum chapter)
		/** point of series 0 of a plot under the plot pen at chapter progress q: the runtime assembles a plot over the first
		 *  90 % of its chapter, draws the axes first, then reveals the series (plot.ts); the pen holds at the last point */
		function pen(plotId: string, q: number): [number, number] | null {
			const pl = spec.plots?.find((x) => x.id === plotId);
			const pts = (pl?.series?.[0]?.points ?? []) as [number, number][];
			const n = pts.length;
			if (!n) return null;
			const kk = staggerK(seg(q, 0, 0.9), AXES_END, 1, 0, pl?.series?.length ?? 1);
			const t = Math.max(0, Math.min(n - 1, kk * n - 1));
			const i = Math.floor(t);
			const j = Math.min(n - 1, i + 1);
			return [lerp(pts[i][0], pts[j][0], t - i), lerp(pts[i][1], pts[j][1], t - i)];
		}

		// ---------------------------------------------------------------------------- staging
		const A: Record<string, V3> = {
			nh3_source: [0, 0, 0],
			focuser: [XF0, 0, 0],
			cavity: [cavX, 0, 0],
			out: [outA[0] - cavX, outBase, outA[2]],
			inp: [inA[0] - cavX, inBase, inA[2]]
		};
		// exploded offsets (intro line-up and the explode slider at k = 1)
		const E: Record<string, V3> = { nh3_source: [-70, 0, 0], cavity: [66, 0, 0], out: [0, 45, 0], inp: [6, 30, 0] };
		const EL_EX = 22; // electrodes: radial offset when exploded

		// ---------------------------------------------------------------------------- frame
		let lastP = 0;
		function frame(p: number) {
			lastP = p;
			const kk = clamp01(k);
			const kx = ease(kk);
			shot = shotAt(p);
			applyCamera(shot);
			const introQ = cq('intro', p);
			const srcQ = cq('source', p);
			const focQ = cq('focuser', p);
			const selQ = cq('select', p);
			const cavQ = cq('cavity', p);
			const emQ = cq('emission', p);
			const spQ = cq('spectrum', p);
			const osQ = cq('oscillation', p);
			const settle = ease(seg(introQ, 0, 0.85));
			const float = (ph: number, amp: number) => amp * Math.sin(TAU * (p * 3 + ph)) * (1 - seg(p, C.source[0], C.source[0] + 0.03));
			const leave = ease(seg(srcQ, 0, 0.25)); // intro line-up leaves as the source chapter starts

			// ---- source tube: from the intro line-up straight to its place
			{
				const a = ease(seg(srcQ, 0.02, 0.45));
				const ex: V3 = add3(E.nh3_source, [0, float(0.1, 3), (1 - settle) * 14]);
				let pos = p < C.source[0] ? ex : mix3(ex, A.nh3_source, a);
				pos = mix3(pos, add3(A.nh3_source, E.nh3_source), kx);
				for (const b of [source, apertures]) {
					b.obj.position.set(pos[0], pos[1], pos[2]);
					b.obj.rotation.set(0, 0.6 * (1 - settle) * (1 - a), 0);
					setOpacity(b, 1);
				}
			}
			// ---- chamber and pump stub: faint in the intro, settle in with the source; out of the way in the plot chapters
			const inPlot = Math.max(
				seg(p, C.select[0], C.select[0] + 0.015) * (1 - seg(p, C.cavity[0], C.cavity[0] + 0.015)),
				seg(p, C.spectrum[0], C.spectrum[0] + 0.015) * (1 - seg(p, C.oscillation[0], C.oscillation[0] + 0.015))
			);
			{
				const o = (p < C.source[0] ? 0.55 * settle : lerp(0.55, 1, easeOut(seg(srcQ, 0.1, 0.4)))) * (1 - inPlot);
				setOpacity(chamber, o * (1 - 0.7 * kx));
				setOpacity(pump, o * (1 - 0.7 * kx));
				// the faces are drawn from inside (far walls only); with the camera inside the box they would wrap the view
				const cp = camera.position;
				const din = Math.min(cp.x - chX[0], chX[1] - cp.x, chHH - Math.abs(cp.y), chHD - Math.abs(cp.z));
				chFaces.visible = din < -8;
			}
			// ---- electrodes: float in the intro, leave, slide in radially in the focuser chapter
			for (const e of electrodes) {
				let r: number;
				let o: number;
				if (p < C.focuser[0]) {
					r = EL_EX + 6 * (1 - settle) + float(0.2 + e.order * 0.2, 1.5) + 40 * leave;
					o = 1 - leave;
				} else {
					const a = ease(seg(focQ, 0.05 + 0.08 * e.order, 0.4 + 0.08 * e.order));
					r = 60 * (1 - a);
					o = easeOut(seg(focQ, 0.02 + 0.08 * e.order, 0.2 + 0.08 * e.order));
				}
				r = lerp(r, EL_EX, kx);
				e.mesh.position.set(0, e.dir[0] * r, e.dir[1] * r);
				e.mesh.userData.o = o;
			}
			for (const b of [focHV, focGnd]) {
				setOpacity(b, 1);
				b.obj.position.x = p < C.focuser[0] ? lerp(XF0, XF0 + 20, 1 - settle) : XF0;
			}
			{
				// per electrode opacity (staggered arrival); the near pair is ghosted while the states separate
				const ghost = p >= C.select[0] && p < C.cavity[0] ? ease(seg(selQ, 0, 0.15)) * (1 - seg(p, C.cavity[0] - 0.015, C.cavity[0])) : 0;
				for (const e of electrodes) {
					let o = num(e.mesh.userData.o, 1);
					if (e.near) o *= 1 - 0.78 * ghost;
					const base = num(look(e.id).opacity, 1);
					const op = base * o;
					const trans = op < 0.999;
					if (e.mat.transparent !== trans) {
						e.mat.transparent = trans;
						e.mat.needsUpdate = true;
					}
					e.mat.opacity = op;
					e.mat.depthWrite = op > 0.6;
					e.mesh.visible = op > 0.004;
				}
			}
			const fPres = p >= C.focuser[0] ? ease(seg(focQ, 0.4, 0.66)) : 0; // electrodes in place (particle clipping)
			// ---- leads grow from the electrodes through the chamber wall
			{
				const d = p >= C.focuser[0] ? ease(seg(focQ, 0.6, 0.85)) : 0;
				leadUp.scale.set(1, Math.max(1e-3, d * leadLen), 1);
				leadDn.scale.set(1, Math.max(1e-3, d * leadLen), 1);
				setOpacity(leads, d > 0 ? 1 - seg(kk, 0, 0.15) : 0);
			}
			// ---- cavity: in the line-up in the intro, slides onto the axis from downstream in its chapter
			let cPres = 0;
			{
				let pos: V3;
				let o: number;
				if (p < C.cavity[0]) {
					pos = add3(add3(A.cavity, E.cavity), [0, float(0.6, 2.5), (1 - settle) * -16]);
					o = 1 - leave;
				} else {
					const a = ease(seg(cavQ, 0.0, 0.42));
					pos = add3(A.cavity, [130 * (1 - a), 0, 0]);
					o = easeOut(seg(cavQ, 0.0, 0.18));
					cPres = seg(cavQ, 0.3, 0.45);
				}
				pos = mix3(pos, add3(A.cavity, E.cavity), kx);
				cavity.obj.position.set(pos[0], pos[1], pos[2]);
				cavity.obj.rotation.set(p < C.cavity[0] ? 0.5 * (1 - settle) : 0, 0, 0);
				setOpacity(cavity, o);
				setOpacity(entry, o);
				// guides: in the line-up in the intro, drop in after the cavity
				const ga = p < C.cavity[0] ? 0 : ease(seg(cavQ, 0.35, 0.75));
				const go = p < C.cavity[0] ? 1 - leave : easeOut(seg(cavQ, 0.33, 0.5));
				const gp = (base: V3, ex: V3): V3 => {
					const q = p < C.cavity[0] ? add3(base, add3(ex, [0, 30 * (1 - settle), 0])) : add3(base, [0, 90 * (1 - ga), 0]);
					return mix3(q, add3(base, ex), kx);
				};
				const po = gp(A.out, E.out);
				const pi = gp(A.inp, E.inp);
				outGroup.position.set(po[0], po[1], po[2]);
				inGroup.position.set(pi[0], pi[1], pi[2]);
				setOpacity(outGuide, go);
				setOpacity(inGuide, go);
				// cut-away: the near sector of the wall fades once the cavity is in place
				const lidO = p < C.cavity[0] ? 1 : 1 - ease(seg(cavQ, 0.55, 0.85));
				const lo = lidBody.base * lidO * o;
				lidMat.opacity = lo;
				lidMat.transparent = lo < 0.999;
				lidMat.depthWrite = lo > 0.5;
				lid.visible = lo > 0.01;
			}

			// ---- voltage, klystron power, emission (all pure in p)
			const V = p < C.select[0] ? 0 : ease(seg(selQ, 0.06, 0.36));
			let kp = 0; // klystron power in the input guide (fraction)
			let e = 0; // emission from the beam (fraction of the on-line level)
			let osc = 0; // self-sustained share
			if (p >= C.oscillation[0]) {
				const e0 = pen('spectrum', 1)?.[1] ?? 0;
				osc = ease(seg(osQ, 0.0, 0.4));
				kp = 1 - ease(seg(osQ, 0.05, 0.45));
				e = lerp(e0, 1, osc);
			} else if (p >= C.spectrum[0]) {
				kp = 1;
				// drive = klystron offset under the plot pen; response = the digitized Fig. 3b signal there
				const pn = pen('spectrum', spQ);
				e = lerp(1, clamp01(pn?.[1] ?? 0), ease(seg(spQ, 0, 0.12)));
			} else if (p >= C.emission[0]) {
				kp = ease(seg(emQ, 0.04, 0.3));
				e = ease(seg(emQ, 0.25, 0.6));
			}
			const fieldI = clamp01(0.35 * kp * (1 - osc) + 0.65 * e + 0.35 * osc);
			const outI = clamp01(0.2 * kp + 0.8 * e);
			const F = 0.45 * e; // share of arriving upper-state molecules that emit in the cavity (illustrative)
			const fxOn = 1 - seg(kk, 0, 0.15);
			const tau = p * NT;
			const cavOn = p >= C.cavity[0] ? cPres : 0;
			{
				const hiF = hi.includes('cavity_field') ? 0.25 : 0;
				fieldMat.uniforms.uI.value = Math.max(fieldI * 0.8, hiF) * fxOn * cavOn;
				setOpacity(fieldBody, (fieldI > 0.02 || hiF > 0) && cavOn > 0.5 ? fxOn : 0);
				const hiIn = hi.includes('input_wave') ? 0.3 : 0;
				inWaveMat.uniforms.uI.value = Math.max(kp * 0.8, hiIn) * fxOn * inGuide.o;
				inWaveMat.uniforms.uPhase.value = tau * 3;
				setOpacity(inWaveBody, (kp > 0.01 || hiIn > 0) && inGuide.o > 0.5 ? fxOn : 0);
				const hiOut = hi.includes('output_wave') ? 0.3 : 0;
				outWaveMat.uniforms.uI.value = Math.max(outI * 0.85, hiOut) * fxOn * outGuide.o;
				outWaveMat.uniforms.uPhase.value = tau * 3;
				setOpacity(outWaveBody, (outI > 0.01 || hiOut > 0) && outGuide.o > 0.5 ? fxOn : 0);
			}

			// ---- molecules
			{
				const tauOn = NT * lerp(C.source[0], C.source[1], 0.42); // the stream starts once the tube is in place
				const molOn = fxOn * (p >= C.source[0] ? 1 : 0);
				const size = Math.min(2.0, Math.max(0.2, camDist * 0.0034)) * molOn;
				const xEnd = lerp(lerp(205, XF1 + 10, fPres), XC1 - 4, cavOn);
				const xEnd0 = xEnd - lerp(lerp(55, 22, fPres), 14, cavOn);
				const big = (id: string) => (hi.includes(id) ? 1.6 : 1);
				let nu = 0;
				let nl = 0;
				if (size > 0)
					for (const m of mols) {
						const c = tau * m.s + m.ph;
						const born = (Math.floor(c) - m.ph) / m.s;
						if (born < tauOn) continue;
						const x = (c - Math.floor(c)) * LPATH;
						let y: number;
						let z: number;
						let a = seg(x, 0, 5);
						if (x <= XF0 || fPres <= 0) {
							y = m.y0 + m.vy * x;
							z = m.z0 + m.vz * x;
						} else if (x <= XF1) {
							const s = x - XF0;
							const ya = m.y0 + m.vy * XF0;
							const za = m.z0 + m.vz * XF0;
							y = lerp(ya + m.vy * s, solve(ya, m.vy, m.up, 1, s), V);
							z = lerp(za + m.vz * s, solve(za, m.vz, m.up, 1, s), V);
						} else {
							const d = x - XF1;
							y = lerp(m.ey[0] + m.ey[1] * d, m.ey1[0] + m.ey1[1] * d, V);
							z = lerp(m.ez[0] + m.ez[1] * d, m.ez1[0] + m.ez1[1] * d, V);
						}
						// electrodes in place: molecules outside the clear radius at the entrance hit the electrode ends; lower
						// states pushed outward leave between the electrodes and are gone before the focuser end
						if (fPres > 0 && x > XF0 - 2) {
							if (m.rIn > RCLEAR) a *= 1 - fPres;
							if (!m.up && x <= XF1 + 30) a *= 1 - fPres * V * seg(Math.hypot(y, z), RCLEAR, RCLEAR + 3);
							if (!m.up) a *= 1 - fPres * V * seg(x, XF0 + 0.6 * focL, XF1 - 6);
						}
						// end of the drawn stream: fades in the empty chamber, after the focuser, or inside the cavity
						a *= 1 - seg(x, xEnd0, xEnd);
						if (a <= 0.02) continue;
						// emission happens only inside the cavity, from upper-state molecules
						const emitted = m.up && cavOn > 0.5 && x > m.xc && m.u < F;
						const upper = m.up && !emitted;
						const sz = size * a * big(upper ? 'upper_state' : 'lower_state');
						mtx.makeScale(sz, sz, sz).setPosition(x, y, z);
						if (upper) upI.setMatrixAt(nu++, mtx);
						else loI.setMatrixAt(nl++, mtx);
					}
				upI.count = nu;
				loI.count = nl;
				upI.instanceMatrix.needsUpdate = true;
				loI.instanceMatrix.needsUpdate = true;
				upBody.o = nu > 0 ? 1 : 0;
				loBody.o = nl > 0 ? 1 : 0;
				upI.visible = nu > 0;
				loI.visible = nl > 0;
			}

			for (const b of [source, apertures, focHV, focGnd, leads, chamber, pump, cavity, outGuide, inGuide]) tint(b);
			apRing.visible = hi.includes('entry_aperture') && entry.o > 0.3;
			apRingMat.color.copy(accent);
			chEdgeMat.color.set(hi.includes('vacuum_chamber') ? (theme === 'light' ? '#2a78d6' : '#3987e5') : theme === 'light' ? '#9a9ea6' : '#5d626b');
		}

		// ---------------------------------------------------------------------------- handle
		// anchor points in the local frame of the part's group
		const ANCH: Record<string, () => V3> = {
			cavity: () => [cavL * 0.15, cavRo + 0.5, 0],
			output_wave: () => [(outIn[0] ?? 10) / 2 + 2, outLen * 0.42, 0]
		};
		// electrode pairs: end face (downstream) of one electrode of each pair (V upper-left, O lower-left), mesh frame
		const pc: [number, number] = profile.length
			? [profile.reduce((t, q) => t + q[0], 0) / profile.length, profile.reduce((t, q) => t + q[1], 0) / profile.length]
			: [-11.7, 11.7];
		const EANCH: Record<string, { e: Electrode | undefined; pt: V3 }> = {
			focuser_hv: { e: electrodes.find((e) => e.id === 'focuser_hv' && e.order === 0), pt: [focL, pc[1], pc[0]] }, // V, upper-left
			focuser_ground: { e: electrodes.find((e) => e.id === 'focuser_ground' && e.order === 3), pt: [focL, -pc[1], pc[0]] } // O, lower-left (labels on different rows)
		};
		// caveats on illustrative choices, shown in the part tooltip (pick detail)
		const CUT = "Drawn cut open on the near side to show the inside (the patent's FIG. 4 is likewise partly in section).";
		const STRIPES = 'Stripes show the direction of the power flow; their spacing is illustrative, not the guide wavelength.';
		const SHARE = 'The share of molecules drawn turning blue in the cavity (up to about half) is illustrative; the letter gives no transition probability.';
		function detailFor(id: string, p: number): string[] {
			switch (id) {
				case 'lower_state':
					return ['Drawn: the outward push is about 6 times the inward one, and the few lower-state molecules near the axis are faded out, so that none reach the cavity ("virtually all in the upper states"); neither source gives the size of the forces.'];
				case 'upper_state':
					return ['Focusing strength chosen to bring the beam onto the entrance hole (illustrative).', SHARE];
				case 'cavity':
				case 'output_guide':
				case 'input_guide':
					return [CUT];
				case 'input_wave':
					return [STRIPES];
				case 'output_wave':
					return [STRIPES, SHARE];
				case 'focuser_hv':
				case 'focuser_ground':
					return p >= C.select[0] && p < C.cavity[0] ? ['The near pair is drawn see-through in this chapter so the beam inside shows.'] : [];
				default:
					return [];
			}
		}
		const OSC_ID = 'oscillator_output';
		/** screen point (pane px) of the world point in tmp, or null when behind the camera, off the pane or under the plot */
		function project(): [number, number] | null {
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
		}
		const handle: ShowcaseHandle = {
			assembledAt: C.oscillation[0],
			frame,
			highlight(ids) {
				hi = ids.map((x) => (x === OSC_ID ? 'output_wave' : x));
			},
			pick(x, y) {
				v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
				raycaster.setFromCamera(v2, camera);
				raycaster.params.Line = { threshold: Math.max(1, camDist * 0.006) };
				const cands: THREE_NS.Object3D[] = [];
				for (const b of bodies.values()) {
					if (!b.obj.visible || b.o < 0.2) continue;
					let vis = true;
					b.obj.traverseAncestors((a) => (vis = vis && a.visible));
					if (vis) cands.push(...b.picks);
				}
				if (!lid.visible || lidMat.opacity < 0.5) {
					const i = cands.indexOf(lid);
					if (i >= 0) cands.splice(i, 1);
				}
				const hits = raycaster.intersectObjects(cands, false);
				// prefer a solid part over the chamber edge lines behind it
				const hit = hits.find((q) => q.object.userData.part !== 'vacuum_chamber') ?? hits[0];
				const id = hit?.object.userData.part as string | undefined;
				if (!id) return null;
				// the oscillator's output: no line frequency (the letter does not name the line it ran on)
				if (id === 'output_wave' && lastP >= C.oscillation[0])
					return {
						id: OSC_ID,
						label: 'Emission',
						detail: [
							'Microwave power leaving the cavity through the output guide.',
							'Oscillator: the letter does not say on which line it ran.',
							'Power estimated at about 10^{-8} watt, not measured (letter p.283).',
							STRIPES
						]
					};
				const d = detailFor(id, lastP);
				return d.length ? { id, label: partOf(id)?.name ?? id, detail: d } : id;
			},
			anchor(id) {
				const ea = EANCH[id];
				if (ea?.e) {
					if (!ea.e.mesh.visible || ea.e.mat.opacity < 0.5) return null;
					ea.e.mesh.updateWorldMatrix(true, false);
					tmp.set(ea.pt[0], ea.pt[1], ea.pt[2]);
					ea.e.mesh.localToWorld(tmp);
					return project();
				}
				const b = bodies.get(id);
				const f = ANCH[id];
				if (!b || !f || !b.obj.visible || b.o < 0.5) return null;
				let vis = true;
				b.obj.traverseAncestors((a) => (vis = vis && a.visible));
				if (!vis) return null;
				const pt = f();
				b.obj.updateWorldMatrix(true, false);
				tmp.set(pt[0], pt[1], pt[2]);
				b.obj.localToWorld(tmp);
				return project();
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
				upI.dispose();
				loI.dispose();
				for (const d of disposables) d.dispose();
			}
		};
		return handle;
	}
};
export default mod;
