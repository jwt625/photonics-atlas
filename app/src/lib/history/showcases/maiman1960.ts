// Scene module: first laser (ruby), Maiman 1960 (DevLog-017 pilot). Spec: data/history/showcases/maiman1960.yaml.
// Contract: ../showcase/types.ts. Units mm; x = rod axis, +x = output end (hole, beam); origin = rod centre.
// Geometry, looks and placements come from the spec (parts[].geometry / look, assembly); nothing the spec withholds is
// drawn (no rod mount, no cylinder end caps, no lamp bulb / base / terminals, no supply internals).
//
// Light timeline (audit W3): the flash rises and holds in "Negative temperature"; in "694.3 nm" the beam emerges while
// the flash is still bright, then flash and beam decay together to a held frame (FROZEN) that the last chapter keeps.
// The plot chapters frame the head in the left half; the supply and leads fade there and the beam ends before the plot.
import type * as THREE_NS from 'three';
import { clamp01, ease, easeOut, lerp, seg } from '../showcase/progress';
import type { ShowcaseContext, ShowcaseHandle, ShowcaseModule, Theme } from '../showcase/types';

type Three = typeof THREE_NS;
type V3 = [number, number, number];
type Rect = [number, number, number, number]; // pane fractions x0, y0, x1, y1
type Geo = Record<string, unknown>;

const DEG = Math.PI / 180;
const TAU = Math.PI * 2;
const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);

// ------------------------------------------------------------------------------------------------ shots (camera)
// One settled camera shot per chapter; the camera eases from the previous shot over the first part of a chapter and
// drifts in azimuth inside it. R = [half width, half height] (mm) around the target that must fit in the shot's region.
interface Shot {
	t: V3;
	az: number;
	el: number;
	R: [number, number];
	drift: number;
	region: 'full' | 'plot';
}
const SHOTS: Record<string, Shot> = {
	intro: { t: [-58, -22, 0], az: 20, el: 15, R: [102, 48], drift: 12, region: 'full' },
	rod: { t: [0, 0, 0], az: 30, el: 14, R: [17, 12], drift: 8, region: 'full' },
	mirrors: { t: [7, 0, 0], az: 64, el: 12, R: [12.5, 12.5], drift: 6, region: 'full' },
	lamp: { t: [0, 0, 0], az: 28, el: 18, R: [21, 19], drift: 8, region: 'full' },
	reflector: { t: [0, -22, 0], az: 26, el: 20, R: [34, 46], drift: 6, region: 'full' },
	levels: { t: [1, -1, 0], az: 24, el: 15, R: [30, 24], drift: 4, region: 'plot' },
	flash: { t: [0, 0, 0], az: 24, el: 13, R: [25, 22], drift: 6, region: 'full' },
	pulse: { t: [32, -4, 0], az: 32, el: 10, R: [52, 26], drift: 4, region: 'full' },
	spectrum: { t: [9, -1, 0], az: 30, el: 13, R: [30, 19], drift: 6, region: 'plot' }
};
const CHAPTER_IDS = ['intro', 'rod', 'mirrors', 'lamp', 'reflector', 'levels', 'flash', 'pulse', 'spectrum'];

function regions(w: number, h: number): { full: Rect; plot: Rect; plotBox: Rect } {
	if (w < 700)
		return { full: [0.04, 0.2, 0.96, 0.98], plot: [0.04, 0.17, 0.96, 0.43], plotBox: [0, 0.44, 1, 1] };
	const top = Math.min(0.24, 150 / Math.max(1, h));
	return { full: [0.03, top, 0.97, 0.97], plot: [0.03, top, 0.49, 0.97], plotBox: [0.5, 0.16, 1, 1] };
}

// ------------------------------------------------------------------------------------------------ glow shader
const GLOW_VS = /* glsl */ `
varying vec3 vN; varying vec3 vV; varying float vX;
void main() {
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	vN = normalize(normalMatrix * normal);
	vV = normalize(-mv.xyz);
	vX = position.x;
	gl_Position = projectionMatrix * mv;
}`;
const GLOW_FS = /* glsl */ `
uniform vec3 uColor; uniform float uI; uniform float uPow; uniform float uLight;
uniform float uBeam; uniform float uPk; uniform float uPkI; uniform float uRim; uniform float uK;
varying vec3 vN; varying vec3 vV; varying float vX;
void main() {
	float c = clamp(abs(dot(normalize(vN), normalize(vV))), 0.0, 1.0);
	float f = pow(uRim > 0.5 ? 1.0 - c : c, uPow);
	float a = f * uI;
	if (uBeam > 0.5) {
		a *= smoothstep(0.0, 0.03, vX) * (1.0 - smoothstep(0.93, 1.0, vX));
		a += f * uPkI * exp(-pow((vX - uPk) / 0.045, 2.0));
	}
	a = clamp(a * uK, 0.0, 1.0);
	gl_FragColor = uLight > 0.5 ? vec4(uColor, a) : vec4(uColor * a, a);
}`;

// ------------------------------------------------------------------------------------------------ module
const mod: ShowcaseModule = {
	renderer: '3d',
	build(ctx: ShowcaseContext): ShowcaseHandle {
		if (ctx.kind !== '3d') throw new Error('maiman1960 is a 3D scene');
		const { THREE, scene, camera, spec } = ctx;
		let w = Math.max(1, ctx.width);
		let h = Math.max(1, ctx.height);
		let k = 0;
		let theme: Theme = ctx.theme;
		let hi: string[] = [];

		const partOf = (id: string) => spec.parts.find((q) => q.id === id);
		const geo = (id: string): Geo => (partOf(id)?.geometry ?? {}) as Geo;
		const look = (id: string) => partOf(id)?.look ?? {};
		const at = (id: string): V3 => {
			const pos = spec.assembly?.find((a) => a.part === id)?.pos;
			return Array.isArray(pos) && pos.length === 3 ? [pos[0], pos[1], pos[2]] : [0, 0, 0];
		};
		const fallback: Record<string, [number, number]> = {
			intro: [0, 0.1], rod: [0.1, 0.22], mirrors: [0.22, 0.32], lamp: [0.32, 0.44], reflector: [0.44, 0.54],
			levels: [0.54, 0.66], flash: [0.66, 0.78], pulse: [0.78, 0.88], spectrum: [0.88, 1]
		};
		const C = Object.fromEntries(
			CHAPTER_IDS.map((id) => [id, (spec.chapters.find((c) => c.id === id)?.p ?? fallback[id]) as [number, number]])
		) as Record<string, [number, number]>;
		/** local progress inside chapter id */
		const cq = (id: string, p: number) => seg(p, C[id][0], C[id][1]);

		// ---------------------------------------------------------------------------- dimensions from the spec
		const rodG = geo('ruby_rod');
		const rodR = num(rodG.diameter, 10) / 2;
		const rodL = num(rodG.length, 20);
		const agT = num(geo('silver_back').thickness, 0.2);
		const holeR = num((geo('silver_output').hole as Geo | undefined)?.diameter, num(geo('output_hole').diameter, 1)) / 2;
		const lampG = geo('flash_lamp');
		const tubeR = num(lampG.tube_diameter, 3.5) / 2;
		const helixR = num(lampG.outer_diameter, 25.4) / 2 - tubeR;
		const helixSpan = num(lampG.length, 25.4) - 2 * tubeR;
		const turns = num(lampG.turns, 3);
		const refG = geo('reflector');
		const refRi = num(refG.inner_diameter, 34) / 2;
		const refRo = refRi + num(refG.wall, 1.5);
		const refL = num(refG.length, 40);
		const psuS = (Array.isArray(geo('power_supply').size) ? geo('power_supply').size : [40, 24, 24]) as number[];
		const beamG = geo('output_beam');
		const beamR = num(beamG.diameter, 1) / 2;
		const beamL = num(beamG.length, 120);

		const A: Record<string, V3> = {
			ruby_rod: at('ruby_rod'),
			silver_back: at('silver_back'),
			silver_output: at('silver_output'),
			flash_lamp: at('flash_lamp'),
			reflector: at('reflector'),
			power_supply: at('power_supply'),
			output_beam: at('output_beam')
		};
		// exploded line-up along the axis (intro and the explode slider at k = 1)
		const E: Record<string, V3> = {
			ruby_rod: [0, 0, 0],
			silver_back: [-27, 0, 0],
			silver_output: [27, 0, 0],
			flash_lamp: [-64, 0, 0],
			reflector: [-116, 0, 0],
			power_supply: [-52, -60, 0]
		};
		// where a part starts its fly-in in its own chapter
		const L: Record<string, V3> = {
			silver_back: [-36, 5, 0],
			silver_output: [36, 5, 0],
			flash_lamp: [-78, 0, 0],
			reflector: [-120, 0, 0],
			power_supply: [0, -100, 0]
		};

		// ---------------------------------------------------------------------------- materials
		const disposables: { dispose(): void }[] = [];
		const keep = <T extends { dispose(): void }>(x: T): T => (disposables.push(x), x);
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
		// studio environment (soft boxes on a dark room) for the module's own PBR materials: long, clean highlights on
		// the aluminum, silver, glass and ruby; converted to PMREM by the renderer on first use
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
		const std = (id: string, extra: Partial<THREE_NS.MeshPhysicalMaterialParameters> = {}) => {
			const lk = look(id);
			const op = num(lk.opacity, 1);
			return keep(
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
		};
		const glow = (color: string, pow: number, beam = false, rim = false) =>
			keep(
				new THREE.ShaderMaterial({
					uniforms: {
						uColor: { value: new THREE.Color(color) },
						uI: { value: 0 },
						uPow: { value: pow },
						uLight: { value: 0 },
						uBeam: { value: beam ? 1 : 0 },
						uPk: { value: -1 },
						uPkI: { value: 0 },
						uRim: { value: rim ? 1 : 0 },
						uK: { value: 1 }
					},
					vertexShader: GLOW_VS,
					fragmentShader: GLOW_FS,
					transparent: true,
					depthWrite: false,
					blending: THREE.AdditiveBlending,
					toneMapped: false
				})
			);
		// light theme: glows blend normally (additive light vanishes on a light page) and most are toned down (lightK)
		const glows: { m: THREE_NS.ShaderMaterial; dark: string; light: string; lightK: number }[] = [];
		const glowT = (dark: string, light: string, pow: number, beam = false, rim = false, lightK = 1) => {
			const m = glow(dark, pow, beam, rim);
			glows.push({ m, dark, light, lightK });
			return m;
		};
		const G = <T extends THREE_NS.BufferGeometry>(g: T): T => keep(g);
		const nopick = <T extends THREE_NS.Object3D>(o: T): T => ((o.userData.nopick = true), o);

		// ---------------------------------------------------------------------------- ruby rod
		const rodMat = std('ruby_rod', { clearcoat: 1, clearcoatRoughness: 0.12, ior: 1.77, specularIntensity: 1, envMapIntensity: 1.2 });
		rodMat.color.multiplyScalar(0.72); // the body carries most of the colour; the inner light and rim layers add depth
		rodMat.depthWrite = false; // inner light draws over the body; opaque parts still occlude it
		const rodGeo = G(new THREE.CylinderGeometry(rodR, rodR, rodL, 96, 1, false).rotateZ(Math.PI / 2));
		const rodMesh = new THREE.Mesh(rodGeo, rodMat);
		rodMesh.renderOrder = 2;
		const rodCoreMat = glowT('#ff4a6e', '#e0102a', 0.9);
		const rodCore = nopick(new THREE.Mesh(G(new THREE.CylinderGeometry(rodR * 0.86, rodR * 0.86, rodL * 0.99, 48, 1, true).rotateZ(Math.PI / 2)), rodCoreMat));
		rodCore.renderOrder = 3;
		const rodRimMat = glowT('#ffc4d2', '#ffffff', 2.2, false, true);
		rodRimMat.uniforms.uI.value = 1.0;
		const rodRim = nopick(new THREE.Mesh(G(new THREE.CylinderGeometry(rodR * 1.002, rodR * 1.002, rodL * 0.995, 96, 1, true).rotateZ(Math.PI / 2)), rodRimMat));
		rodRim.renderOrder = 3;
		const rodG3 = new THREE.Group();
		rodG3.add(rodMesh, rodCore, rodRim);
		const rod = body('ruby_rod', rodG3);

		// ---------------------------------------------------------------------------- silver ends (+ hole)
		const backGeo = G(new THREE.CylinderGeometry(rodR, rodR, agT, 96).rotateZ(Math.PI / 2));
		const back = body('silver_back', new THREE.Mesh(backGeo, std('silver_back', { envMapIntensity: 1.6, roughness: 0.16 })));
		const outShape = new THREE.Shape().absarc(0, 0, rodR, 0, TAU, false);
		outShape.holes.push(new THREE.Path().absarc(0, 0, holeR, 0, TAU, true));
		const outGeo = G(new THREE.ExtrudeGeometry(outShape, { depth: agT, bevelEnabled: false, curveSegments: 96 }).rotateY(Math.PI / 2).translate(-agT / 2, 0, 0));
		const outGroup = new THREE.Group();
		const outMesh = new THREE.Mesh(outGeo, std('silver_output', { envMapIntensity: 1.6, roughness: 0.16 }));
		outGroup.add(outMesh);
		const out = body('silver_output', outGroup);
		// hole: pick proxy only (the opening itself shows the ruby behind it)
		const holeProxy = new THREE.Mesh(G(new THREE.CircleGeometry(Math.max(holeR, 0.7), 24).rotateY(Math.PI / 2)), keep(new THREE.MeshBasicMaterial({ visible: false })));
		holeProxy.position.x = agT / 2 + 0.02;
		const holeGroup = new THREE.Group();
		// hover ring: the opening has no body of its own, so emphasis draws a thin ring at its edge
		const holeRingMat = keep(new THREE.MeshBasicMaterial({ color: '#3987e5', transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }));
		const holeRing = nopick(new THREE.Mesh(G(new THREE.RingGeometry(holeR, holeR + 0.3, 40).rotateY(Math.PI / 2)), holeRingMat));
		holeRing.position.x = agT / 2 + 0.03;
		holeRing.renderOrder = 11;
		holeGroup.add(holeProxy, holeRing);
		const hole = body('output_hole', holeGroup);

		// ---------------------------------------------------------------------------- helical flash lamp
		const a0 = -45 * DEG; // helix ends at the upper back (leads leave behind the beam line)
		const helixAt = (t: number) => {
			const a = a0 + t * turns * TAU;
			return new THREE.Vector3(-helixSpan / 2 + helixSpan * t, helixR * Math.cos(a), helixR * Math.sin(a));
		};
		const HN = Math.round(64 * turns);
		const helix = new THREE.CatmullRomCurve3(Array.from({ length: HN + 1 }, (_, i) => helixAt(i / HN)), false, 'centripetal');
		const glassMat = std('flash_lamp', { clearcoat: 1, clearcoatRoughness: 0.03, ior: 1.47, envMapIntensity: 2.6, depthWrite: false });
		glassMat.transparent = true;
		const glassBody = glassMat.opacity;
		glassMat.opacity = glassBody * 0.4; // look.opacity is carried by body + rim together
		const glassRimMat = glowT('#e8f0ff', '#7d8796', 2.2, false, true);
		glassRimMat.uniforms.uI.value = glassBody * 2;
		const lampGroup = new THREE.Group();
		const glass = new THREE.Mesh(G(new THREE.TubeGeometry(helix, Math.round(110 * turns), tubeR, 18, false)), glassMat);
		glass.renderOrder = 4;
		const capGeo = G(new THREE.SphereGeometry(tubeR, 18, 12));
		const endA = helixAt(0);
		const endB = helixAt(1);
		const capA = new THREE.Mesh(capGeo, glassMat);
		capA.position.copy(endA);
		const capB = new THREE.Mesh(capGeo, glassMat);
		capB.position.copy(endB);
		const xeMat = keep(new THREE.MeshBasicMaterial({ color: '#eef4ff', transparent: true, opacity: 0, depthWrite: false, toneMapped: false }));
		const xe = nopick(new THREE.Mesh(G(new THREE.TubeGeometry(helix, Math.round(110 * turns), tubeR * 0.45, 8, false)), xeMat));
		xe.renderOrder = 2;
		const lampHaloMat = glowT('#cfe0ff', '#8fb4ea', 1.6, false, false, 0.45);
		const lampHalo = nopick(new THREE.Mesh(G(new THREE.TubeGeometry(helix, Math.round(80 * turns), tubeR * 2.4, 12, false)), lampHaloMat));
		lampHalo.renderOrder = 6;
		const glassRim = nopick(new THREE.Mesh(glass.geometry, glassRimMat));
		glassRim.renderOrder = 5;
		const capRimA = nopick(new THREE.Mesh(capGeo, glassRimMat));
		capRimA.position.copy(endA);
		const capRimB = nopick(new THREE.Mesh(capGeo, glassRimMat));
		capRimB.position.copy(endB);
		lampGroup.add(glass, capA, capB, glassRim, capRimA, capRimB, xe, lampHalo);
		const lamp = body('flash_lamp', lampGroup);

		// ---------------------------------------------------------------------------- aluminum cylinder, cut away
		const cut = 150 * DEG;
		const cutC = -38 * DEG; // tube angle phi: world y = -r sin(phi), z = r cos(phi); centre of the opening up-front
		const ph0 = cutC + cut / 2;
		const phL = TAU - cut;
		const alMat = std('reflector', { side: THREE.DoubleSide, envMapIntensity: 1.25 });
		const cutMat = std('reflector', { side: THREE.DoubleSide, roughness: 0.42, envMapIntensity: 1 });
		const refGroup = new THREE.Group();
		const tubeParts: THREE_NS.Mesh[] = [
			new THREE.Mesh(G(new THREE.CylinderGeometry(refRo, refRo, refL, 128, 1, true, ph0, phL)), alMat),
			new THREE.Mesh(G(new THREE.CylinderGeometry(refRi, refRi, refL, 128, 1, true, ph0, phL)), alMat)
		];
		for (const y of [-refL / 2, refL / 2])
			tubeParts.push(new THREE.Mesh(G(new THREE.LatheGeometry([new THREE.Vector2(refRi, y), new THREE.Vector2(refRo, y)], 128, ph0, phL)), cutMat));
		for (const ph of [ph0, ph0 + phL]) {
			const m = new THREE.Mesh(G(new THREE.PlaneGeometry(refRo - refRi, refL)), cutMat);
			m.position.set(((refRi + refRo) / 2) * Math.sin(ph), 0, ((refRi + refRo) / 2) * Math.cos(ph));
			m.rotation.y = ph - Math.PI / 2;
			tubeParts.push(m);
		}
		const refInner = new THREE.Group();
		refInner.add(...tubeParts);
		refInner.rotation.z = -Math.PI / 2; // tube axis y -> x
		refGroup.add(refInner);
		const reflector = body('reflector', refGroup);

		// ---------------------------------------------------------------------------- power supply (schematic box)
		const psuGeo = G(new THREE.BoxGeometry(psuS[0] ?? 40, psuS[1] ?? 24, psuS[2] ?? 24));
		const psuMat = std('power_supply', { transparent: true, opacity: num(look('power_supply').opacity, 1) * 0.82, envMapIntensity: 0.6 });
		const psuGroup = new THREE.Group();
		const psuEdgeMat = keep(new THREE.LineBasicMaterial({ color: '#6c717b', transparent: true, opacity: 1 }));
		const psuEdges = nopick(new THREE.LineSegments(G(new THREE.EdgesGeometry(psuGeo)), psuEdgeMat));
		psuGroup.add(new THREE.Mesh(psuGeo, psuMat), psuEdges);
		const psu = body('power_supply', psuGroup);

		// ---------------------------------------------------------------------------- leads (FIG. 4: one per helix end)
		const xOut = refL / 2 + 7;
		const psuY = A.power_supply[1];
		const psuHalfX = (psuS[0] ?? 40) / 2;
		function leadPath(e: THREE_NS.Vector3, side: number): THREE_NS.CurvePath<THREE_NS.Vector3> {
			const pts = [e.clone(), new THREE.Vector3(side * xOut, e.y, e.z), new THREE.Vector3(side * xOut, psuY, e.z), new THREE.Vector3(side * psuHalfX, psuY, e.z)];
			const path = new THREE.CurvePath<THREE_NS.Vector3>();
			const r = 4;
			let cur = pts[0];
			for (let i = 1; i < pts.length; i++) {
				const p1 = pts[i];
				const next = pts[i + 1];
				if (!next) {
					path.add(new THREE.LineCurve3(cur, p1));
					break;
				}
				const inDir = p1.clone().sub(cur).normalize();
				const outDir = next.clone().sub(p1).normalize();
				const a = p1.clone().addScaledVector(inDir, -r);
				const b = p1.clone().addScaledVector(outDir, r);
				path.add(new THREE.LineCurve3(cur, a));
				path.add(new THREE.QuadraticBezierCurve3(a, p1, b));
				cur = b;
			}
			return path;
		}
		const leadMat = std('lamp_leads');
		const LEAD_SEG = 160;
		const LEAD_RAD = 8;
		const leadGeos = [leadPath(endA, -1), leadPath(endB, 1)].map((pth) => G(new THREE.TubeGeometry(pth, LEAD_SEG, 0.45, LEAD_RAD, false)));
		const leadsGroup = new THREE.Group();
		for (const g of leadGeos) leadsGroup.add(new THREE.Mesh(g, leadMat));
		const leads = body('lamp_leads', leadsGroup);

		// ---------------------------------------------------------------------------- pump light (effect)
		const pumpMat = glowT('#cfe6ff', '#a9c8f0', 0.55, false, false, 0.2);
		const pumpMesh = nopick(new THREE.Mesh(G(new THREE.CylinderGeometry(refRi - 0.6, refRi - 0.6, refL - 2, 64, 1, true).rotateZ(Math.PI / 2)), pumpMat));
		pumpMesh.renderOrder = 7;
		const pumpGroup = new THREE.Group();
		pumpGroup.add(pumpMesh);
		root.add(pumpGroup);
		const pumpLights = [-7, 0, 7].map((x) => {
			const l = new THREE.PointLight('#dfeaff', 0, 90, 2);
			l.position.set(x, 0, 0);
			root.add(l);
			return l;
		});

		// ---------------------------------------------------------------------------- output beam
		const unitBeam = (r: number, seg = 32) => G(new THREE.CylinderGeometry(r, r, 1, seg, 1, true).rotateZ(-Math.PI / 2).translate(0.5, 0, 0));
		const beamCoreMat = keep(new THREE.MeshBasicMaterial({ color: look('output_beam').color || '#ff1a1a', transparent: true, opacity: 0, depthWrite: false, toneMapped: false }));
		const beamCore = new THREE.Mesh(unitBeam(beamR), beamCoreMat);
		beamCore.renderOrder = 7;
		const beamHaloMat = glowT('#ff2a1a', '#e01a10', 1.4, true, false, 0.6);
		const beamHalo = nopick(new THREE.Mesh(unitBeam(beamR * 4.5), beamHaloMat));
		beamHalo.renderOrder = 8;
		const beamSoftMat = glowT('#ff1a10', '#ff5a50', 3, true, false, 0.22);
		const beamSoft = nopick(new THREE.Mesh(unitBeam(beamR * 12), beamSoftMat));
		beamSoft.renderOrder = 9;
		const beamPick = new THREE.Mesh(unitBeam(beamR * 4, 8), keep(new THREE.MeshBasicMaterial({ visible: false })));
		const beamScaled = new THREE.Group();
		beamScaled.add(beamCore, beamHalo, beamSoft, beamPick);
		const flareTex = (() => {
			const cv = document.createElement('canvas');
			cv.width = cv.height = 128;
			const g = cv.getContext('2d')!;
			const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64);
			gr.addColorStop(0, 'rgba(255,255,255,1)');
			gr.addColorStop(0.12, 'rgba(255,210,200,0.9)');
			gr.addColorStop(0.35, 'rgba(255,60,40,0.35)');
			gr.addColorStop(1, 'rgba(255,0,0,0)');
			g.fillStyle = gr;
			g.fillRect(0, 0, 128, 128);
			const t = new THREE.CanvasTexture(cv);
			t.colorSpace = THREE.SRGBColorSpace;
			return keep(t);
		})();
		const flareMat = keep(new THREE.SpriteMaterial({ map: flareTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, opacity: 0 }));
		const flare = nopick(new THREE.Sprite(flareMat));
		flare.renderOrder = 10;
		const beamGroup = new THREE.Group();
		beamGroup.add(beamScaled, flare);
		const beam = body('output_beam', beamGroup);
		const redLight = new THREE.PointLight('#ff3020', 0, 60, 2);
		root.add(redLight);

		// ---------------------------------------------------------------------------- lights
		const hemi = new THREE.HemisphereLight('#ffffff', '#3a3c44', 0.7);
		const key = new THREE.DirectionalLight('#fff3e6', 2.4);
		key.position.set(60, 120, 95);
		const rim = new THREE.DirectionalLight('#bcd2ff', 1.5);
		rim.position.set(-130, 50, -90);
		const fill = new THREE.DirectionalLight('#ffffff', 0.5);
		fill.position.set(-40, -60, 120);
		root.add(hemi, key, rim, fill);


		// ---------------------------------------------------------------------------- state helpers
		const raycaster = new THREE.Raycaster();
		const v2 = new THREE.Vector2();
		const tmp = new THREE.Vector3();
		const tmp2 = new THREE.Vector3();
		const accent = new THREE.Color();
		const tmpCol = new THREE.Color();
		const black = new THREE.Color(0, 0, 0);
		let shot: Shot & { rect: Rect } = { ...SHOTS.intro, rect: regions(w, h).full };

		function setOpacity(b: Body, o: number) {
			const lit = hi.includes(b.id);
			const eff = lit && o < 0.3 ? 0.3 : o;
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
		function tint(b: Body, glowCol: THREE_NS.Color | null, gi = 0) {
			const lit = hi.includes(b.id);
			for (const x of b.mats) {
				x.m.emissive.copy(glowCol ?? black);
				x.m.emissiveIntensity = glowCol ? gi : 1;
				if (lit) {
					x.m.emissive.lerp(accent, glowCol ? 0.25 : 1);
					if (!glowCol) x.m.emissiveIntensity = 0.2;
				}
			}
		}
		const place = (o: THREE_NS.Object3D, v: V3) => o.position.set(v[0], v[1], v[2]);
		const mix3 = (a: V3, b: V3, t: number): V3 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2], b[2], t)];
		const add3 = (a: V3, b: V3): V3 => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];

		/** smooth bump up then down across [a, b] */
		const bump = (q: number, a: number, b: number) => Math.sin(Math.PI * seg(q, a, b));

		function shotAt(p: number): Shot & { rect: Rect } {
			const R = regions(w, h);
			const kx = ease(clamp01(k));
			let i = 0;
			for (let j = 0; j < CHAPTER_IDS.length; j++) if (p >= C[CHAPTER_IDS[j]][0]) i = j;
			const id = CHAPTER_IDS[i];
			const q = cq(id, p);
			const cur = SHOTS[id];
			const prevId = CHAPTER_IDS[i - 1];
			const prev = prevId ? SHOTS[prevId] : null;
			const t = prev ? ease(seg(q, 0, cur.region === 'plot' ? 0.2 : 0.5)) : 1;
			const curAz = cur.az + cur.drift * (q - 0.5);
			const prevAz = prev ? prev.az + prev.drift * 0.5 : curAz;
			const rc = R[cur.region];
			const rp = prev ? R[prev.region] : rc;
			return {
				t: mix3(mix3(prev?.t ?? cur.t, cur.t, t), SHOTS.intro.t, kx),
				az: lerp(prevAz, curAz, t),
				el: lerp(prev?.el ?? cur.el, cur.el, t),
				R: [lerp(lerp(prev?.R[0] ?? cur.R[0], cur.R[0], t), SHOTS.intro.R[0], kx), lerp(lerp(prev?.R[1] ?? cur.R[1], cur.R[1], t), SHOTS.intro.R[1], kx)],
				drift: 0,
				region: cur.region,
				rect: [lerp(rp[0], rc[0], t), lerp(rp[1], rc[1], t), lerp(rp[2], rc[2], t), lerp(rp[3], rc[3], t)]
			};
		}
		let camDist = 100;
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
			accent.set(theme === 'light' ? '#2a78d6' : '#3987e5');
			for (const g of glows) {
				const light = theme === 'light';
				g.m.uniforms.uColor.value.set(light ? g.light : g.dark);
				g.m.uniforms.uLight.value = light ? 1 : 0;
				g.m.uniforms.uK.value = light ? g.lightK : 1;
				g.m.blending = light ? THREE.NormalBlending : THREE.AdditiveBlending;
			}
			flareMat.blending = theme === 'light' ? THREE.NormalBlending : THREE.AdditiveBlending;
			psuEdgeMat.color.set(theme === 'light' ? '#8d9098' : '#6c717b');
			hemi.intensity = theme === 'light' ? 0.9 : 0.7;
		}
		applyTheme();

		// ---------------------------------------------------------------------------- frame
		/** the held frame of the last chapter: flash at a visible glow, beam on (fractions of their peak) */
		const FROZEN = { flash: 0.42, beam: 0.8 };
		const beamCol = new THREE.Color(look('output_beam').color || '#ff1a1a');
		const bv = new THREE.Vector3();
		/** longest beam (mm) whose end stays left of screen x `xmax` (pane px), for the current camera */
		function beamClip(xmax: number): number {
			const sx = (L: number) => {
				bv.set(A.output_beam[0] + L, A.output_beam[1], A.output_beam[2]).project(camera);
				return ((bv.x + 1) / 2) * w;
			};
			if (sx(beamL) <= xmax) return beamL;
			let lo = 0;
			let hi2 = beamL;
			for (let i = 0; i < 14; i++) {
				const m = (lo + hi2) / 2;
				if (sx(m) <= xmax) lo = m;
				else hi2 = m;
			}
			return lo;
		}
		const red = new THREE.Color('#ff2a2a');
		const rodGlowCol = new THREE.Color(look('ruby_rod').emissive || '#ff2a2a');
		const flashCol = new THREE.Color(look('flash_lamp').emissive || '#cfe0ff');

		function frame(p: number) {
			const kk = clamp01(k);
			// camera first: the beam length depends on where the plot panel falls on screen
			shot = shotAt(p);
			applyCamera(shot);
			const rodQ = cq('rod', p);
			const introQ = cq('intro', p);
			// presence: everything floats in the intro, the others leave as the rod takes the stage, then return in
			// their own chapter
			const leave = ease(seg(rodQ, 0, 0.3));
			const settle = ease(seg(introQ, 0, 0.85));
			const float = (ph: number, amp: number) => amp * Math.sin(TAU * (p * 2.2 + ph)) * (1 - seg(p, C.rod[0], C.rod[0] + 0.04));

			function staged(id: string, chap: string, spin: (a: number) => V3, tilt: V3, phase: number) {
				const b = bodies.get(id)!;
				const q = cq(chap, p);
				const arrive = ease(seg(q, 0.04, 0.8));
				const fadeIn = easeOut(seg(q, 0.02, 0.28));
				let pos: V3;
				let rot: V3;
				let o: number;
				if (p < C[chap][0]) {
					// intro line-up, then leaving outward
					const spread = add3(E[id], [E[id][0] * 0.12 * (1 - settle), 0, (1 - settle) * 26 * Math.sin(phase * 7)]);
					pos = add3(add3(spread, [0, float(phase, 1.6), 0]), [E[id][0] * 0.3 * leave, 0, 0]);
					rot = [tilt[0] * (1 - settle), tilt[1] * (1 - settle), tilt[2] * (1 - settle)];
					o = 1 - leave;
				} else {
					pos = mix3(L[id], A[id], arrive);
					rot = spin(1 - arrive);
					o = fadeIn;
				}
				// user explode after assembly: towards the line-up
				if (kk > 0 && E[id]) pos = mix3(pos, E[id], kk);
				place(b.obj, pos);
				b.obj.rotation.set(rot[0], rot[1], rot[2]);
				setOpacity(b, o);
			}

			// ---- rod: centre stage, tumbles once in its chapter
			{
				const tum = ease(seg(rodQ, 0.05, 0.9));
				const tilt0: V3 = [0.5, 0.9, 0.35];
				const pos: V3 = [0, float(0.1, 1.2) + 2.5 * bump(rodQ, 0.05, 0.9), 0];
				place(rod.obj, kk > 0 ? mix3(pos, E.ruby_rod, kk) : pos);
				rod.obj.rotation.set(tilt0[0] * (1 - settle), tilt0[1] * (1 - settle) + TAU * tum, tilt0[2] * (1 - settle) + 0.35 * bump(rodQ, 0.05, 0.9));
				setOpacity(rod, 1);
			}
			staged('silver_back', 'mirrors', (u) => [0, Math.PI * u, 0], [0.2, 1.1, 0], 0.3);
			staged('silver_output', 'mirrors', (u) => [0, -Math.PI * u, 0], [-0.3, -1.2, 0.2], 0.55);
			staged('flash_lamp', 'lamp', (u) => [-TAU * 1.25 * u, 0, 0], [0.6, 0.5, 0.25], 0.75);
			staged('reflector', 'reflector', (u) => [0.9 * u, 0, 0], [0.25, -0.55, 0.15], 0.15);
			staged('power_supply', 'reflector', (u) => [0, 0.9 * u, 0], [0.2, 0.7, 0], 0.9);
			// the supply arrives after the cylinder: re-time it inside the chapter
			{
				const q = cq('reflector', p);
				if (p >= C.reflector[0]) {
					const a = ease(seg(q, 0.3, 0.8));
					const pos = mix3(L.power_supply, A.power_supply, a);
					place(psu.obj, kk > 0 ? mix3(pos, E.power_supply, kk) : pos);
					psu.obj.rotation.set(0, 0.9 * (1 - a), 0);
					setOpacity(psu, easeOut(seg(q, 0.3, 0.55)));
				}
			}
			// hole rides with the output silver
			hole.obj.position.copy(out.obj.position);
			hole.obj.rotation.copy(out.obj.rotation);
			setOpacity(hole, out.o);

			// ---- leads draw from the helix ends to the supply
			{
				const q = cq('reflector', p);
				const d = p >= C.reflector[0] ? ease(seg(q, 0.55, 0.95)) : 0;
				const n = Math.floor(d * LEAD_SEG) * LEAD_RAD * 6;
				for (const g of leadGeos) g.setDrawRange(0, n);
				const o = d > 0 ? 1 - seg(kk, 0, 0.12) : 0;
				setOpacity(leads, o);
			}
			// plot chapters: the head alone, calm in the left half (phone: the strip above the plot); the supply and leads
			// fade out (the explode slider brings the supply back)
			const inPlot = Math.max(
				seg(p, C.levels[0], C.levels[0] + 0.015) * (1 - seg(p, C.flash[0], C.flash[0] + 0.015)),
				seg(p, C.spectrum[0], C.spectrum[0] + 0.015) * (1 - kk)
			);
			{
				if (inPlot > 0) {
					setOpacity(psu, psu.o * (1 - inPlot));
					setOpacity(leads, leads.o * (1 - inPlot));
				}
			}

			// ---- flash, pump light, rod glow, beam
			const fq = cq('flash', p);
			const pq = cq('pulse', p);
			// flicker phase runs on across both chapters (pure in p)
			const flick = (u: number) => 0.92 + 0.08 * Math.cos(TAU * 6 * u);
			const ratio = (C.pulse[1] - C.pulse[0]) / Math.max(1e-6, C.flash[1] - C.flash[0]);
			const decay = ease(seg(pq, 0.42, 0.9)); // flash and beam fall together to the held frame
			let flashOn = 0;
			if (p >= C.pulse[0]) flashOn = lerp(flick(0.82 + pq * ratio), FROZEN.flash, decay);
			else if (p >= C.flash[0]) flashOn = fq < 0.1 ? 0 : fq < 0.18 ? easeOut((fq - 0.1) / 0.08) : flick(fq - 0.18);
			const fl = flashOn * (1 - kk);
			const pump = p >= C.flash[0] ? seg(fq, 0.16, 0.5) : 0; // inversion builds
			// laser output: emerges while the flash is bright (pulse q 0.08-0.3), then decays with it
			const lasing = p >= C.pulse[0] ? easeOut(seg(pq, 0.08, 0.3)) * lerp(1, FROZEN.beam, decay) : 0;
			const rodGlow = Math.max(0.9 * ease(pump), lasing) * (1 - kk);

			xeMat.opacity = Math.min(1, fl * 1.2);
			xeMat.color.copy(flashCol).lerp(new THREE.Color('#ffffff'), 0.6);
			lampHaloMat.uniforms.uI.value = fl * 0.45;
			tint(lamp, fl > 0.001 ? flashCol : null, fl * 0.7);
			for (const l of pumpLights) l.intensity = fl * 3200;
			const hiPump = hi.includes('pump_light') ? 0.25 : 0;
			pumpMat.uniforms.uI.value = Math.max(fl * 0.12, hiPump);
			pumpGroup.visible = pumpMat.uniforms.uI.value > 0.002 && reflector.o > 0.5;

			rodCoreMat.uniforms.uI.value = 0.3 + rodGlow * (0.75 + 0.35 * lasing) + fl * 0.25;
			glassRimMat.uniforms.uI.value = glassBody * (2 + 1.2 * fl) * lamp.o * lamp.o;
			lampHaloMat.uniforms.uI.value *= lamp.o;
			xeMat.opacity *= lamp.o;
			tint(rod, rodGlow > 0.001 ? rodGlowCol : null, rodGlow * 0.55);
			tint(back, null);
			tint(out, null);
			tint(reflector, null);
			tint(psu, null);
			tint(leads, null);
			// translucent parts: emphasis on their rim light (emissive barely shows through low opacity)
			const rimCol = (on: boolean, dark: string, light: string) => (on ? accent : tmpCol.set(theme === 'light' ? light : dark));
			glassRimMat.uniforms.uColor.value.copy(rimCol(hi.includes('flash_lamp'), '#e8f0ff', '#7d8796'));
			rodRimMat.uniforms.uColor.value.copy(rimCol(hi.includes('ruby_rod'), '#ffc4d2', '#ffffff'));
			if (hi.includes('flash_lamp')) glassRimMat.uniforms.uI.value *= 1.7;
			if (hi.includes('ruby_rod')) rodRimMat.uniforms.uI.value = 1.5;
			else rodRimMat.uniforms.uI.value = 1.0;
			holeRing.visible = hi.includes('output_hole');
			holeRingMat.color.copy(accent);

			// beam: the front runs out from the hole along +x while the flash is bright; a bright packet leads it
			const grow = p >= C.pulse[0] ? easeOut(seg(pq, 0.08, 0.4)) : 0;
			// plot chapters: the beam ends before the plot panel (its tip fades in the shader)
			// the beam ends before the pane edge (desktop: the side column starts there) and, in the plot chapters on
			// desktop, before the plot panel; its tip fades in the shader
			const paneClip = beamClip(w - 28);
			const clip = w >= 700 && inPlot > 0 ? lerp(paneClip, beamClip(regions(w, h).plotBox[0] * w - 28), inPlot) : paneClip;
			const len = Math.max(0.001, grow * Math.min(beamL, clip));
			const bOn = grow > 0 ? 1 - seg(kk, 0, 0.12) : 0;
			const bI = bOn * (lasing > 0 ? 0.35 + 0.65 * lasing : 0);
			place(beam.obj, A.output_beam);
			beamScaled.scale.set(len, 1, 1);
			beamCoreMat.opacity = 0.95 * bI;
			beamHaloMat.uniforms.uI.value = 0.95 * bI;
			beamSoftMat.uniforms.uI.value = 0.32 * bI;
			const pk = seg(pq, 0.08, 0.4);
			beamHaloMat.uniforms.uPk.value = pk < 1 ? 1 : -1;
			beamHaloMat.uniforms.uPkI.value = pk < 1 ? 0.9 * bOn : 0;
			flareMat.opacity = bI * (0.75 + 0.25 * (1 - pk));
			flare.scale.setScalar(5 + 3 * (1 - pk) * grow);
			flare.position.set(0.2, 0, 0);
			beam.obj.visible = bOn > 0.002;
			beam.o = bOn;
			redLight.position.set(A.output_beam[0] + 2, 0, 0);
			redLight.intensity = bI * 380;
			if (hi.includes('output_beam')) beamCoreMat.color.set(theme === 'light' ? '#c0281c' : '#ff8a7a');
			else beamCoreMat.color.copy(beamCol);

		}

		// ---------------------------------------------------------------------------- handle
		const handle: ShowcaseHandle = {
			assembledAt: C.spectrum[0],
			frame,
			highlight(ids) {
				hi = [...ids];
			},
			pick(x, y) {
				v2.set((x / w) * 2 - 1, 1 - (y / h) * 2);
				raycaster.setFromCamera(v2, camera);
				const cands: THREE_NS.Mesh[] = [];
				for (const b of bodies.values()) if (b.obj.visible && b.o > 0.2) cands.push(...b.picks);
				const hit = raycaster.intersectObjects(cands, false)[0];
				return (hit?.object.userData.part as string | undefined) ?? null;
			},
			anchor(id) {
				const b = bodies.get(id);
				if (!b || !b.obj.visible || b.o < 0.5) return null;
				b.obj.updateWorldMatrix(true, false);
				if (id === 'ruby_rod') tmp.set(-rodL * 0.4, rodR * 1.05, 0);
				else if (id === 'flash_lamp') tmp.set(helixSpan * 0.32, helixR + tubeR, 0);
				else if (id === 'output_beam') tmp.set(Math.min(beamL * 0.3, beamScaled.scale.x * (shot.region === 'plot' ? 0.18 : 0.5)), beamR * 3, 0);
				else return null;
				b.obj.localToWorld(tmp);
				camera.updateMatrixWorld();
				tmp2.copy(tmp).applyMatrix4(camera.matrixWorldInverse);
				if (tmp2.z > -camera.near) return null;
				tmp.project(camera);
				const sx = ((tmp.x + 1) / 2) * w;
				const sy = ((1 - tmp.y) / 2) * h;
				if (sx < 0 || sx > w || sy < 0 || sy > h) return null; // the runtime keeps labels inside the pane
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
