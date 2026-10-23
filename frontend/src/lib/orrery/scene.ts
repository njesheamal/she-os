// SHÉ OS Orrery — data-driven Three.js scene.
// Brands become planets (mapped by slug), the SHÉRocks initiative becomes the asteroid
// belt, published field notes become the Editions constellation, and promotions become
// brass shooting stars. The host component owns data loading and the readout / grid / UI;
// this module owns the 3D scene and emits a ReadoutPayload when a world is selected.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import type { Brand, FieldNote, Initiative } from '../api';

// ── shared GLSL ─────────────────────────────────────────────────────
const NOISE = `
float hash(vec3 p){ p = fract(p*0.3183099 + 0.1); p *= 17.0;
  return fract(p.x*p.y*p.z*(p.x+p.y+p.z)); }
float noise(vec3 x){ vec3 i = floor(x); vec3 f = fract(x); f = f*f*(3.0-2.0*f);
  return mix(mix(mix(hash(i+vec3(0,0,0)),hash(i+vec3(1,0,0)),f.x),
                 mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),
                 mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z); }
float fbm(vec3 p){ float v=0.0, a=0.5; for(int i=0;i<6;i++){ v+=a*noise(p); p*=2.0; a*=0.5; } return v; }
`;
const VERT = `
varying vec3 vLocal; varying vec3 vNormalW; varying vec3 vWorldPos;
void main(){
  vLocal = position;
  vNormalW = normalize(mat3(modelMatrix)*normal);
  vec4 wp = modelMatrix*vec4(position,1.0);
  vWorldPos = wp.xyz;
  gl_Position = projectionMatrix*viewMatrix*wp;
}`;

const SUMA_FRAG = NOISE + `
uniform float uTime; uniform vec3 uSunPos; uniform vec3 uCamPos;
varying vec3 vLocal; varying vec3 vNormalW; varying vec3 vWorldPos;
void main(){
  vec3 p = normalize(vLocal); float t = uTime*0.02; vec3 wp = p*2.0; float lat = p.y;
  float wa = fbm(wp*1.2 + vec3(t,0.0,0.0));
  float wb = fbm(wp*2.6 + wa*1.6 + vec3(0.0,t*0.6,0.0));
  float latf = lat + (wa-0.5)*0.22 + (wb-0.5)*0.10;
  float macro = fbm(vec3(latf*5.0, 1.7, 0.0));
  float meso  = fbm(vec3(latf*11.0, 4.0, 0.0));
  float micro = fbm(vec3(latf*52.0, p.x*4.0, p.z*4.0)) - 0.5;
  vec3 butter = vec3(0.976,0.886,0.722); vec3 blue = vec3(0.718,0.808,0.976);
  vec3 brown = vec3(0.647,0.518,0.302); vec3 celad = vec3(0.765,0.878,0.776);
  vec3 gold = vec3(0.90,0.74,0.34); vec3 lightB = vec3(0.99,0.93,0.74);
  vec3 butterShaded = mix(gold, butter, smoothstep(0.30,0.60,macro));
  butterShaded = mix(butterShaded, lightB, smoothstep(0.66,0.92,meso)*0.5);
  vec3 blueShaded = mix(vec3(0.58,0.64,0.74), blue, smoothstep(0.30,0.70,meso));
  float sel = smoothstep(0.26,0.74, mix(macro, meso, 0.35));
  sel += smoothstep(0.40,0.95, abs(lat))*0.12;
  sel += smoothstep(0.14,0.38,lat)*(1.0-smoothstep(0.46,0.70,lat))*0.03;
  sel = clamp(sel + micro*0.05, 0.0, 1.0);
  vec3 col = butterShaded;
  col = mix(col, blueShaded, smoothstep(0.580,0.645, sel));
  col = mix(col, brown,      smoothstep(0.785,0.835, sel));
  col = mix(col, celad,      smoothstep(0.935,0.965, sel));
  col *= 1.0 + micro*0.10;
  float cap = smoothstep(0.74,0.96, abs(lat));
  col = mix(col, vec3(0.58,0.61,0.63), cap*0.38);
  vec3 N = normalize(vNormalW); vec3 V = normalize(uCamPos - vWorldPos);
  float ndv = clamp(dot(V,N),0.0,1.0); float edge = 1.0 - ndv;
  float ph = fract(ndv*1.1 + macro*0.5 + micro*0.6);
  vec3 pcyan=vec3(0.80,0.92,0.90); vec3 silver=vec3(0.88,0.89,0.92);
  vec3 skyI=vec3(0.718,0.808,0.976); vec3 cream=vec3(0.98,0.95,0.86);
  vec3 pearl = mix(pcyan, silver, smoothstep(0.0,0.34,ph));
  pearl = mix(pearl, skyI, smoothstep(0.34,0.67,ph));
  pearl = mix(pearl, cream, smoothstep(0.67,1.0,ph));
  col = mix(col, pearl, pow(edge,1.3)*0.16);
  vec3 L = normalize(uSunPos - vWorldPos); float nl = dot(N,L);
  col *= 0.12 + 1.00*smoothstep(-0.30, 0.55, nl);
  col *= mix(1.0, 0.70, smoothstep(0.0,1.0,edge));
  col = mix(col, vec3(0.40,0.45,0.55), smoothstep(0.55,1.0,edge)*0.45);
  col += vec3(0.718,0.808,0.976) * pow(edge,4.0) * 0.32;
  float lum = dot(col, vec3(0.299,0.587,0.114)); col = mix(vec3(lum), col, 1.10);
  gl_FragColor = vec4(col,1.0);
}`;

const RING_VERT = `
varying float vR; varying vec3 vWorldPos;
void main(){ vR = length(position.xy);
  vec4 wp = modelMatrix*vec4(position,1.0); vWorldPos = wp.xyz;
  gl_Position = projectionMatrix*viewMatrix*wp; }`;
const RING_FRAG = NOISE + `
uniform float uInner; uniform float uOuter; uniform float uPlanetR;
uniform vec3 uSunPos; uniform vec3 uPlanetPos;
varying float vR; varying vec3 vWorldPos;
void main(){
  float f = (vR - uInner)/(uOuter - uInner); if(f<0.0||f>1.0) discard;
  float bands = fbm(vec3(vR*7.5,0.0,0.0))*0.6 + fbm(vec3(vR*19.0,2.0,0.0))*0.4;
  float a = smoothstep(0.0,0.14,f)*smoothstep(1.0,0.80,f);
  a *= 0.30 + 0.70*bands; a *= smoothstep(0.015,0.07,abs(f-0.46));
  vec3 toSun = normalize(uSunPos - vWorldPos); vec3 oc = vWorldPos - uPlanetPos;
  float b = dot(oc,toSun); float c = dot(oc,oc) - uPlanetR*uPlanetR; float h = b*b-c;
  float shadow = 1.0; if(h>0.0){ float tHit=-b-sqrt(h); if(tHit>0.0) shadow=0.34; }
  vec3 cDark=vec3(0.50,0.40,0.18); vec3 cLite=vec3(1.00,0.90,0.52);
  vec3 col = mix(cDark,cLite,bands)*shadow;
  col += vec3(1.00,0.92,0.60)*pow(bands,2.0)*shadow*0.7;
  gl_FragColor = vec4(col, a*0.96);
}`;

const GIDA_FRAG = NOISE + `
uniform float uTime; uniform vec3 uSunPos; uniform vec3 uCamPos;
varying vec3 vLocal; varying vec3 vNormalW; varying vec3 vWorldPos;
void main(){
  vec3 p = normalize(vLocal); float t = uTime*0.02; vec3 wp = p*2.4; float lat = p.y;
  vec3 dp = wp;
  dp += 0.55*vec3(fbm(dp+vec3(t,0.0,0.0)), fbm(dp+vec3(2.7,t*0.7,5.0)), fbm(dp+vec3(9.1,1.0,t)));
  dp += 0.38*vec3(fbm(dp*2.0+1.0), fbm(dp*2.0+3.3), fbm(dp*2.0+7.7));
  dp += 0.22*vec3(fbm(dp*4.0+2.0), fbm(dp*4.0+5.0), fbm(dp*4.0+8.0));
  float swirls = fbm(dp*2.4);
  float f1 = fbm(wp*1.3 + vec3(t,0.0,0.0));
  float shear = sin(lat*11.0 + (f1-0.5)*3.2);
  float latf = lat + (f1-0.5)*0.10 + (swirls-0.5)*0.30*shear;
  float belt = fbm(vec3(latf*9.0, 3.0, 0.0));
  float ridged = 1.0 - abs(2.0*fbm(vec3(latf*18.0,1.0,swirls*2.0))-1.0); ridged = pow(ridged,2.2);
  float ridgeB = 1.0 - abs(2.0*fbm(dp*6.0)-1.0); ridgeB = pow(ridgeB,2.6);
  float micro = fbm(dp*10.0);
  float v = belt*0.40 + swirls*0.28 + ridged*0.18 + (ridgeB-0.30)*0.14 + (micro-0.5)*0.10;
  v = smoothstep(0.10,0.88, clamp(v,0.0,1.0));
  vec3 cDeep=vec3(0.07,0.20,0.15); vec3 cEmer=vec3(0.184,0.439,0.341);
  vec3 cSage=vec3(0.639,0.761,0.655); vec3 cCel=vec3(0.765,0.878,0.776);
  vec3 cMint=vec3(0.95,0.99,0.94); vec3 peri=vec3(0.639,0.659,0.773);
  vec3 col = mix(cDeep,cEmer,smoothstep(0.05,0.26,v));
  col = mix(col,cSage,smoothstep(0.26,0.54,v));
  col = mix(col,cCel,smoothstep(0.54,0.80,v));
  col = mix(col,cMint,smoothstep(0.82,0.96,v));
  col = mix(col,cEmer, ridged*smoothstep(0.18,0.48,v)*0.40);
  col = mix(col,cMint, pow(ridgeB,3.0)*smoothstep(0.50,0.85,v)*0.45);
  col = mix(col,peri, smoothstep(0.55,0.95,swirls)*smoothstep(0.45,0.80,v)*0.14);
  vec3 N = normalize(vNormalW); vec3 V = normalize(uCamPos-vWorldPos);
  float ndv = clamp(dot(V,N),0.0,1.0); float edge = 1.0-ndv;
  vec3 L = normalize(uSunPos-vWorldPos); float diff = dot(N,L)*0.5+0.5;
  col *= 0.12 + 1.00*smoothstep(0.35,0.78,diff);
  col *= mix(1.0,0.70,smoothstep(0.0,1.0,edge));
  col = mix(col, vec3(0.30,0.36,0.46), smoothstep(0.58,1.0,edge)*0.40);
  col += peri*pow(edge,4.0)*0.55;
  col += peri*pow(edge,1.8)*0.10*diff;
  col = mix(vec3(dot(col,vec3(0.299,0.587,0.114))), col, 1.14);
  col = pow(col, vec3(0.95));
  gl_FragColor = vec4(col,1.0);
}`;

const TUFA_FRAG = NOISE + `
uniform float uTime; uniform vec3 uSunPos; uniform vec3 uCamPos;
varying vec3 vLocal; varying vec3 vNormalW; varying vec3 vWorldPos;
void main(){
  vec3 p = normalize(vLocal); float t = uTime*0.025; vec3 wp = p*1.8;
  vec3 q = vec3(fbm(wp+vec3(0.0,t,0.0)), fbm(wp+vec3(3.2,t*0.7,1.0)), fbm(wp+vec3(1.4,t*1.1,5.0)));
  float flow = fbm(wp*1.1 + q*2.3 + vec3(t*0.5,0.0,0.0));
  float streak = fbm(wp*3.1 + q*2.0);
  float deepv = fbm(wp*0.85 + q*1.5);
  vec3 indigo=vec3(0.17,0.18,0.39); vec3 blue=vec3(0.494,0.596,0.741);
  vec3 bark=vec3(0.647,0.518,0.302); vec3 lite=vec3(0.88,0.82,0.70);
  vec3 col = mix(blue,bark,smoothstep(0.39,0.63,flow));
  col = mix(col,indigo,smoothstep(0.44,0.08,deepv)*0.62);
  col = mix(col,lite,smoothstep(0.83,0.98,streak)*0.33);
  vec3 N = normalize(vNormalW); vec3 L = normalize(uSunPos-vWorldPos);
  float diff = dot(N,L)*0.5+0.5;
  col *= 0.12 + 1.00*smoothstep(0.35,0.78,diff);
  vec3 V = normalize(uCamPos-vWorldPos); float ndv = clamp(dot(V,N),0.0,1.0);
  col *= mix(0.70,1.0,pow(ndv,0.6));
  float fres = pow(1.0-ndv,3.0);
  col += vec3(0.55,0.62,0.85)*fres*0.5*(0.30+0.70*diff);
  gl_FragColor = vec4(col,1.0);
}`;

const AMSA_FRAG = NOISE + `
uniform float uTime; uniform vec3 uSunPos; uniform vec3 uCamPos;
varying vec3 vLocal; varying vec3 vNormalW; varying vec3 vWorldPos;
void main(){
  vec3 p = normalize(vLocal); float t = uTime*0.03; vec3 wp = p*2.2;
  vec3 q = vec3(fbm(wp+vec3(0.0,t,0.0)), fbm(wp+vec3(2.7,t*0.8,1.3)), fbm(wp+vec3(5.1,t*1.1,4.2)));
  float storm = fbm(wp*2.0 + q*2.2);
  vec3 dark=vec3(0.16,0.18,0.18); vec3 grey=vec3(0.667,0.702,0.667); vec3 shell=vec3(0.725,0.741,0.788);
  vec3 col = mix(dark,grey,smoothstep(0.28,0.58,storm));
  col = mix(col,shell,smoothstep(0.70,0.95,storm)*0.6);
  float lf = fbm(wp*3.0 + q*3.0 + vec3(0.0, uTime*0.25, 0.0));
  float bolt = pow(1.0 - abs(2.0*lf-1.0), 14.0);
  float flick = pow(max(0.0, sin(uTime*0.90 + storm*6.2832)), 22.0);
  float strike = bolt*flick;
  vec3 electric = vec3(0.68,0.80,1.0);
  col += electric*strike*3.2;
  col += electric*flick*storm*0.10;
  vec3 N = normalize(vNormalW); vec3 L = normalize(uSunPos-vWorldPos);
  float diff = dot(N,L)*0.5+0.5;
  col *= 0.12 + 1.00*smoothstep(0.35,0.78,diff);
  vec3 V = normalize(uCamPos-vWorldPos); float ndv = clamp(dot(V,N),0.0,1.0);
  col *= mix(0.70,1.0,pow(ndv,0.6));
  float fres = pow(1.0-ndv,3.0);
  col += vec3(0.55,0.66,0.92)*fres*0.45*(0.30+0.70*diff);
  gl_FragColor = vec4(col,1.0);
}`;

const NEB_VERT = `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`;
const NEB_FRAG = NOISE + `
uniform float uTime; uniform float uSeed; uniform float uGap; uniform float uBright;
varying vec2 vUv;
void main(){
  vec2 uv = vUv*2.0-1.0; float r = length(uv); float ang = atan(uv.y,uv.x);
  float t = uTime*0.05 + uSeed;
  float fil = fbm(vec3(ang*7.0, r*3.0 - t*1.6, uSeed));
  float filFine = pow(fbm(vec3(ang*22.0, r*2.0 - t*1.0, uSeed+3.0)), 1.6);
  float neb = fbm(vec3(uv*3.2 + fil*1.2 + uSeed, t));
  float knots = fbm(vec3(uv*9.0 + neb*2.0, t*0.5 + uSeed));
  float shell = smoothstep(uGap, uGap+0.26, r)*(1.0 - smoothstep(0.52,0.99,r));
  float dens = ((neb*0.55 + filFine*0.45) + knots*0.25)*shell; dens = clamp(dens*1.5,0.0,1.0);
  vec3 deepsea=vec3(0.02,0.08,0.22); vec3 indigo=vec3(0.14,0.15,0.40);
  vec3 eblue=vec3(0.24,0.50,1.00); vec3 peri=vec3(0.64,0.66,0.80); vec3 silver=vec3(0.88,0.92,1.00);
  vec3 col = mix(deepsea,indigo,smoothstep(0.05,0.45,dens));
  col = mix(col,eblue,smoothstep(0.40,0.72,dens));
  col = mix(col,peri,smoothstep(0.60,0.86,dens)*0.6);
  col = mix(col,silver,smoothstep(0.82,0.99,dens));
  col = mix(col, vec3(0.72,0.64,0.52), smoothstep(0.72,1.0,knots)*smoothstep(0.42,0.72,r)*0.10);
  gl_FragColor = vec4(col*uBright, dens);
}`;

const DUST_VERT = `
varying float vR; varying float vAng; varying vec3 vWorldPos;
void main(){ vR=length(position.xy); vAng=atan(position.y,position.x);
  vec4 wp=modelMatrix*vec4(position,1.0); vWorldPos=wp.xyz;
  gl_Position=projectionMatrix*viewMatrix*wp; }`;
const DUST_FRAG = NOISE + `
uniform float uTime; uniform float uInner; uniform float uOuter; uniform float uOp;
varying float vR; varying float vAng; varying vec3 vWorldPos;
void main(){
  float f = (vR - uInner)/(uOuter - uInner); if(f<0.0||f>1.0) discard;
  float prof = smoothstep(0.0,0.28,f)*smoothstep(1.0,0.55,f);
  vec3 sp = vec3(cos(vAng)*vR, sin(vAng)*vR, 0.0);
  float cloud  = fbm(sp*0.6 + vec3(uTime*0.015,0.0,0.0));
  float cloud2 = fbm(sp*1.9 + cloud*1.6);
  float lit = mix(1.0, 0.45, f);
  float dens = prof * (0.30 + 0.70*cloud) * (0.45 + 0.55*cloud2) * lit;
  vec3 cDust = mix(vec3(0.74,0.72,0.64), vec3(0.62,0.65,0.78), cloud2);
  gl_FragColor = vec4(cDust, dens*0.45*uOp);
}`;

// ── public types ────────────────────────────────────────────────────
export type ReadoutKind = 'core' | 'brand' | 'initiative' | 'editions';
export interface ReadoutPayload {
	id: string;
	kind: ReadoutKind;
	name: string;
	subtitle: string;
	status: string;
	blurb: string;
	color: string;
}
export interface Promotion {
	id: string;
	brandSlug: string;
}
export interface OrreryOptions {
	brands: Brand[];
	notes: FieldNote[];
	initiatives: Initiative[];
	promotions: Promotion[];
	reducedMotion: boolean;
	onSelect: (payload: ReadoutPayload | null) => void;
}
export interface OrreryController {
	focus: (id: string | null) => void;
	entities: () => ReadoutPayload[];
	resize: () => void;
	dispose: () => void;
}

// slug → shader, orbit, spin, rings
const BRAND_CONFIG: Record<string, { frag: string; orbitR: number; orbitSpeed: number; spin: number; rings: boolean; color: string; subtitle: string }> = {
	amsa: { frag: AMSA_FRAG, orbitR: 5.5, orbitSpeed: 0.055, spin: 0.05, rings: false, color: '#AAB3AA', subtitle: 'Technology · infrastructure' },
	tufa: { frag: TUFA_FRAG, orbitR: 7.6, orbitSpeed: 0.040, spin: 0.04, rings: false, color: '#7E98BD', subtitle: 'Core brand' },
	suma: { frag: SUMA_FRAG, orbitR: 9.4, orbitSpeed: 0.032, spin: 0.03, rings: true, color: '#F9E2B8', subtitle: 'Core brand' },
	gida: { frag: GIDA_FRAG, orbitR: 10.3, orbitSpeed: 0.025, spin: 0.035, rings: false, color: '#A3C2A7', subtitle: 'Core brand' }
};
const FALLBACK = { frag: TUFA_FRAG, orbitSpeed: 0.02, spin: 0.03, rings: false, color: '#B9BDC9', subtitle: 'Brand' };
const PLANET_R = 0.45;

function radial(stops: [number, string][], size = 512): THREE.CanvasTexture {
	const cv = document.createElement('canvas');
	cv.width = cv.height = size;
	const ctx = cv.getContext('2d')!;
	const g = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
	for (const [o, c] of stops) g.addColorStop(o, c);
	ctx.fillStyle = g;
	ctx.fillRect(0, 0, size, size);
	return new THREE.CanvasTexture(cv);
}

export function createOrrery(canvas: HTMLCanvasElement, opts: OrreryOptions): OrreryController {
	const { brands, notes, initiatives, promotions, reducedMotion, onSelect } = opts;

	const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
	renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
	renderer.setSize(innerWidth, innerHeight);
	renderer.setClearColor(0x000006, 1);

	const scene = new THREE.Scene();
	const camera = new THREE.PerspectiveCamera(42, innerWidth / innerHeight, 0.1, 200);
	camera.position.set(9, 22, 50); // intro starts far

	const controls = new OrbitControls(camera, canvas);
	controls.enableDamping = true;
	controls.minDistance = 6;
	controls.maxDistance = 60;
	controls.target.set(0, 0, 0);

	const SUN = new THREE.Vector3(0, 0, 0);
	const disposables: { dispose(): void }[] = [];

	// starfield
	const starGeo = new THREE.BufferGeometry();
	const NST = 2600, spos = new Float32Array(NST * 3);
	for (let i = 0; i < NST; i++) {
		const r = 70 + Math.random() * 70, th = Math.random() * 6.283, ph = Math.acos(2 * Math.random() - 1);
		spos[i * 3] = r * Math.sin(ph) * Math.cos(th);
		spos[i * 3 + 1] = r * Math.cos(ph);
		spos[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th);
	}
	starGeo.setAttribute('position', new THREE.BufferAttribute(spos, 3));
	scene.add(new THREE.Points(starGeo, new THREE.PointsMaterial({ color: 0xcfd0ee, size: 0.09, sizeAttenuation: true, transparent: true, opacity: 0.8 })));

	scene.add(new THREE.AmbientLight(0x3b3d66, 0.9));
	const sunLight = new THREE.PointLight(0xcdd0ff, 2.4, 0, 0.0);
	sunLight.position.copy(SUN);
	scene.add(sunLight);

	// ── nebula sun ──
	const nebLayers: { m: THREE.Mesh; u: Record<string, { value: number }> }[] = [];
	function nebulaLayer(sc: number, seed: number, gap: number, bright: number) {
		const u = { uTime: { value: 0 }, uSeed: { value: seed }, uGap: { value: gap }, uBright: { value: bright } };
		const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1),
			new THREE.ShaderMaterial({ vertexShader: NEB_VERT, fragmentShader: NEB_FRAG, uniforms: u, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: true }));
		m.scale.set(sc, sc, 1); m.renderOrder = -2; scene.add(m); nebLayers.push({ m, u });
	}
	nebulaLayer(6.6, 0.0, 0.12, 1.25);
	nebulaLayer(9.6, 5.3, 0.20, 0.70);
	nebulaLayer(4.6, 9.1, 0.06, 1.10);

	function addSprite(tex: THREE.Texture, sc: number, order: number) {
		const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false, depthTest: true }));
		sp.scale.set(sc, sc, 1); sp.renderOrder = order; sp.position.copy(SUN); scene.add(sp); return sp;
	}
	addSprite(radial([[0, 'rgba(220,226,240,0.70)'], [0.4, 'rgba(150,160,195,0.26)'], [1, 'rgba(90,100,150,0)']]), 2.9, -1);

	function starburstTex(): THREE.CanvasTexture {
		const s = 1024, cv = document.createElement('canvas'); cv.width = cv.height = s;
		const ctx = cv.getContext('2d')!; ctx.translate(s / 2, s / 2);
		const g = ctx.createRadialGradient(0, 0, 0, 0, 0, s * 0.30);
		g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(0.18, 'rgba(248,250,255,0.95)');
		g.addColorStop(0.45, 'rgba(200,210,235,0.45)'); g.addColorStop(1, 'rgba(150,160,200,0)');
		ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, s * 0.30, 0, 6.2832); ctx.fill();
		ctx.globalCompositeOperation = 'lighter';
		for (let i = 0; i < 120; i++) {
			const a = Math.random() * 6.2832, len = s * (0.18 + Math.random() * 0.30), w = 0.6 + Math.random() * 1.6;
			const lg = ctx.createLinearGradient(0, 0, Math.cos(a) * len, Math.sin(a) * len);
			lg.addColorStop(0, 'rgba(240,244,255,0.55)'); lg.addColorStop(1, 'rgba(200,210,240,0)');
			ctx.strokeStyle = lg; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * len, Math.sin(a) * len); ctx.stroke();
		}
		for (const a of [0, Math.PI / 2, Math.PI, -Math.PI / 2]) {
			const len = s * 0.47; const lg = ctx.createLinearGradient(0, 0, Math.cos(a) * len, Math.sin(a) * len);
			lg.addColorStop(0, 'rgba(255,255,255,0.9)'); lg.addColorStop(1, 'rgba(220,228,255,0)');
			ctx.strokeStyle = lg; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * len, Math.sin(a) * len); ctx.stroke();
		}
		return new THREE.CanvasTexture(cv);
	}
	const coreSprite = addSprite(starburstTex(), 2.4, 1);

	// ── orbit paths ──
	function orbitPath(radius: number) {
		const pts: THREE.Vector3[] = [];
		for (let i = 0; i <= 128; i++) { const a = (i / 128) * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(a) * radius, 0, Math.sin(a) * radius)); }
		const g = new THREE.BufferGeometry().setFromPoints(pts);
		scene.add(new THREE.LineLoop(g, new THREE.LineBasicMaterial({ color: 0x3a3d70, transparent: true, opacity: 0.35 })));
	}

	// ── clickable registry ──
	interface Clickable { id: string; mesh: THREE.Object3D; payload: ReadoutPayload; pos: () => THREE.Vector3; focusDist: number }
	const clickables: Clickable[] = [];

	// SHÉ ESTATE core (the sun) — invisible hit sphere so it is selectable and appears in the grid
	const sunHit = new THREE.Mesh(new THREE.SphereGeometry(2.0, 16, 16), new THREE.MeshBasicMaterial({ visible: false }));
	scene.add(sunHit);
	clickables.push({
		id: 'core', mesh: sunHit, pos: () => SUN, focusDist: 10,
		payload: { id: 'core', kind: 'core', name: 'SHÉ ESTATE', subtitle: 'The core', status: '', blurb: 'The master brand at the center — the gravity every world orbits.', color: '#7E98BD' }
	});

	// ── planets from brands ──
	interface Planet { id: string; grp: THREE.Group; mesh: THREE.Mesh; u: Record<string, { value: unknown }>; orbitR: number; orbitSpeed: number; spin: number; angle: number }
	const planets: Planet[] = [];
	let fallbackOrbit = 12.2;
	let sumaPlanet: Planet | null = null;
	for (let i = 0; i < brands.length; i++) {
		const brand = brands[i];
		const cfg = BRAND_CONFIG[brand.slug.toLowerCase()];
		const frag = cfg?.frag ?? FALLBACK.frag;
		const orbitR = cfg?.orbitR ?? (fallbackOrbit += 1.8);
		const orbitSpeed = cfg?.orbitSpeed ?? FALLBACK.orbitSpeed;
		const spin = cfg?.spin ?? FALLBACK.spin;
		const color = cfg?.color ?? FALLBACK.color;
		const subtitle = cfg?.subtitle ?? FALLBACK.subtitle;
		const u = { uTime: { value: 0 }, uSunPos: { value: SUN.clone() }, uCamPos: { value: camera.position.clone() } };
		const grp = new THREE.Group();
		const mesh = new THREE.Mesh(new THREE.SphereGeometry(PLANET_R, 96, 96),
			new THREE.ShaderMaterial({ vertexShader: VERT, fragmentShader: frag, uniforms: u }));
		grp.add(mesh); scene.add(grp); orbitPath(orbitR);
		const angle = Math.PI * 0.3 + (i * Math.PI * 2) / Math.max(brands.length, 1);
		const planet: Planet = { id: brand.id, grp, mesh, u: u as never, orbitR, orbitSpeed, spin, angle };
		grp.position.set(Math.cos(angle) * orbitR, 0, Math.sin(angle) * orbitR);
		planets.push(planet);
		clickables.push({
			id: brand.id, mesh, pos: () => grp.position, focusDist: 3.8,
			payload: {
				id: brand.id, kind: 'brand', name: brand.name, subtitle,
				status: (brand.status ?? '').toUpperCase(),
				blurb: brand.description ?? 'A SHÉ ESTATE brand world.', color
			}
		});
		if (cfg?.rings) sumaPlanet = planet;
	}

	// ── SUMA rings ──
	let ringU: Record<string, { value: unknown }> | null = null;
	if (sumaPlanet) {
		ringU = { uInner: { value: 0.62 }, uOuter: { value: 1.12 }, uPlanetR: { value: PLANET_R }, uSunPos: { value: SUN.clone() }, uPlanetPos: { value: sumaPlanet.grp.position.clone() } };
		const rings = new THREE.Mesh(new THREE.RingGeometry(0.62, 1.12, 180, 6),
			new THREE.ShaderMaterial({ vertexShader: RING_VERT, fragmentShader: RING_FRAG, uniforms: ringU, transparent: true, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
		rings.rotation.set(-Math.PI * 0.5 + 0.40, 0, 0.16);
		sumaPlanet.grp.add(rings);
	}

	// ── SHÉRocks asteroid belt (from an initiative, if present) ──
	const rocksInit = initiatives.find((x) => /rock/i.test(x.slug) || /rock/i.test(x.name));
	const ROCK_COUNT = 700;
	const rockGeo = new THREE.IcosahedronGeometry(1, 0);
	const rockMat = new THREE.MeshStandardMaterial({ roughness: 0.82, metalness: 0.18, flatShading: true });
	const rocksMesh = new THREE.InstancedMesh(rockGeo, rockMat, ROCK_COUNT);
	rocksMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
	scene.add(rocksMesh);
	const BELT_IN = 12.4, BELT_OUT = 14.2, BELT_THICK = 0.5;
	const BMID = (BELT_IN + BELT_OUT) / 2, BHALF = (BELT_OUT - BELT_IN) / 2;
	const rpal = [new THREE.Color(0xb9bdc9), new THREE.Color(0xa3a8c5), new THREE.Color(0xc5c0a3)];
	interface Rock { a: number; rr: number; y: number; sx: number; sy: number; sz: number; ox: number; oy: number; oz: number; spin: number; orbit: number }
	const rparams: Rock[] = [];
	const rdummy = new THREE.Object3D();
	const rcol = new THREE.Color();
	for (let i = 0; i < ROCK_COUNT; i++) {
		const a = Math.random() * Math.PI * 2;
		const rr = BELT_IN + (BELT_OUT - BELT_IN) * (0.5 + 0.5 * (Math.random() - Math.random()));
		const fade = 1.0 - Math.abs(rr - BMID) / BHALF;
		const y = (Math.random() - 0.5) * BELT_THICK * Math.max(0.2, fade);
		const s = 0.05 + Math.pow(Math.random(), 2.3) * 0.22;
		rparams.push({ a, rr, y, sx: s * (0.7 + Math.random() * 0.6), sy: s * (0.7 + Math.random() * 0.6), sz: s * (0.7 + Math.random() * 0.6), ox: Math.random() * 6.28, oy: Math.random() * 6.28, oz: Math.random() * 6.28, spin: (Math.random() - 0.5) * 0.9, orbit: (0.10 / Math.sqrt(rr)) * (0.85 + Math.random() * 0.3) });
		rcol.copy(rpal[(Math.random() * rpal.length) | 0]).offsetHSL(0, 0, (Math.random() - 0.5) * 0.12);
		rocksMesh.setColorAt(i, rcol);
	}
	if (rocksMesh.instanceColor) rocksMesh.instanceColor.needsUpdate = true;
	function updateRocks(time: number) {
		for (let i = 0; i < ROCK_COUNT; i++) {
			const pm = rparams[i]; const ang = pm.a + time * pm.orbit;
			rdummy.position.set(Math.cos(ang) * pm.rr, pm.y, Math.sin(ang) * pm.rr);
			rdummy.rotation.set(pm.ox + time * pm.spin, pm.oy + time * pm.spin * 0.7, pm.oz + time * pm.spin * 0.4);
			rdummy.scale.set(pm.sx, pm.sy, pm.sz); rdummy.updateMatrix(); rocksMesh.setMatrixAt(i, rdummy.matrix);
		}
		rocksMesh.instanceMatrix.needsUpdate = true;
	}
	updateRocks(0);
	clickables.push({
		id: rocksInit?.id ?? 'shrocks', mesh: rocksMesh, pos: () => SUN, focusDist: 17,
		payload: {
			id: rocksInit?.id ?? 'shrocks', kind: 'initiative', name: rocksInit?.name ?? 'SHÉRocks',
			subtitle: 'Social impact · initiative', status: (rocksInit?.status ?? 'active').toUpperCase(),
			blurb: rocksInit?.description ?? 'The community and social-impact initiative, in collaboration with Shiny Gloves Club.', color: '#A3A8C5'
		}
	});

	// ── dust haze band + motes ──
	const dustRings: { value: number }[] = [];
	function dustRing(inner: number, outer: number, yOff: number, op: number) {
		const u = { uTime: { value: 0 }, uInner: { value: inner }, uOuter: { value: outer }, uOp: { value: op } };
		const m = new THREE.Mesh(new THREE.RingGeometry(inner, outer, 200, 10),
			new THREE.ShaderMaterial({ vertexShader: DUST_VERT, fragmentShader: DUST_FRAG, uniforms: u, transparent: true, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
		m.rotation.x = -Math.PI / 2; m.position.y = yOff; m.renderOrder = -1; scene.add(m);
		dustRings.push(u.uTime);
	}
	dustRing(BELT_IN - 0.8, BELT_OUT + 1.0, 0.0, 1.0);
	dustRing(BELT_IN - 0.3, BELT_OUT + 0.5, 0.2, 0.6);
	dustRing(BELT_IN - 0.3, BELT_OUT + 0.5, -0.2, 0.6);

	const MOTES = 3500, mpos = new Float32Array(MOTES * 3);
	for (let i = 0; i < MOTES; i++) {
		const a = Math.random() * 6.2832;
		const rr = (BELT_IN - 0.5) + ((BELT_OUT + 0.7) - (BELT_IN - 0.5)) * (0.5 + 0.5 * (Math.random() - Math.random()));
		const y = (Math.random() - 0.5) * BELT_THICK * 1.7;
		mpos[i * 3] = Math.cos(a) * rr; mpos[i * 3 + 1] = y; mpos[i * 3 + 2] = Math.sin(a) * rr;
	}
	const moteGeo = new THREE.BufferGeometry();
	moteGeo.setAttribute('position', new THREE.BufferAttribute(mpos, 3));
	const motes = new THREE.Points(moteGeo, new THREE.PointsMaterial({ color: 0xcdc9c0, size: 0.045, sizeAttenuation: true, transparent: true, opacity: 0.5, depthWrite: false }));
	scene.add(motes);

	// ── Editions constellation from published field notes ──
	let constLine: THREE.Line | null = null;
	let cstars: THREE.Sprite[] = [];
	let constHit: THREE.Mesh | null = null;
	if (notes.length > 0) {
		const constDir = new THREE.Vector3(0.45, 0.55, -0.70).normalize();
		const constCenter = constDir.clone().multiplyScalar(55);
		const ctX = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), constDir).normalize();
		const ctY = new THREE.Vector3().crossVectors(constDir, ctX).normalize();
		// one star per note, arranged on a gentle spiral in the constellation's plane
		const constPos = notes.map((_, i) => {
			const ang = i * 2.4, rad = 2.2 + 1.6 * Math.sqrt(i);
			return constCenter.clone().addScaledVector(ctX, Math.cos(ang) * rad).addScaledVector(ctY, Math.sin(ang) * rad);
		});
		const cstarTex = radial([[0, 'rgba(242,230,204,1)'], [0.5, 'rgba(242,230,204,0.4)'], [1, 'rgba(242,230,204,0)']]);
		cstars = constPos.map((p) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: cstarTex, blending: THREE.AdditiveBlending, transparent: true, depthWrite: false })); s.scale.set(1.6, 1.6, 1); s.position.copy(p); scene.add(s); return s; });
		if (constPos.length > 1) {
			constLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints(constPos),
				new THREE.LineBasicMaterial({ color: 0xf2e6cc, transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, depthWrite: false }));
			constLine.frustumCulled = false; scene.add(constLine);
		}
		constHit = new THREE.Mesh(new THREE.SphereGeometry(Math.max(10, 3 + constPos.length), 12, 12), new THREE.MeshBasicMaterial({ visible: false }));
		constHit.position.copy(constCenter); scene.add(constHit);
		clickables.push({
			id: 'editions', mesh: constHit, pos: () => constCenter, focusDist: 0,
			payload: { id: 'editions', kind: 'editions', name: 'SHÉ Editions', subtitle: 'Library · field notes', status: `${notes.length} PUBLISHED`, blurb: 'The celestial atlas — every published field note is a star. Observations, essays, and media from across the system.', color: '#F2E6CC' }
		});
	}

	// ── promotions → brass shooting stars (over matching brands) ──
	interface Promo { getPos: () => THREE.Vector3; head: THREE.Sprite; tail: THREE.Line; tp: Float32Array; TAILN: number; tgeo: THREE.BufferGeometry; timer: number; active: boolean; prog: number; from: THREE.Vector3; to: THREE.Vector3; trail: THREE.Vector3[] }
	const promos: Promo[] = [];
	function makePromo(getPos: () => THREE.Vector3): Promo {
		const head = new THREE.Sprite(new THREE.SpriteMaterial({ map: radial([[0, 'rgba(240,210,150,1)'], [0.35, 'rgba(185,142,94,0.6)'], [1, 'rgba(185,142,94,0)']]), blending: THREE.AdditiveBlending, transparent: true, depthWrite: false }));
		head.scale.set(0.2, 0.2, 1); head.visible = false; scene.add(head);
		const TAILN = 10, tp = new Float32Array(TAILN * 3);
		const tgeo = new THREE.BufferGeometry(); tgeo.setAttribute('position', new THREE.BufferAttribute(tp, 3)); tgeo.setDrawRange(0, 0);
		const tail = new THREE.Line(tgeo, new THREE.LineBasicMaterial({ color: 0xb98e5e, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, depthWrite: false }));
		tail.visible = false; tail.frustumCulled = false; scene.add(tail);
		return { getPos, head, tail, tp, TAILN, tgeo, timer: 2 + Math.random() * 4, active: false, prog: 0, from: new THREE.Vector3(), to: new THREE.Vector3(), trail: [] };
	}
	function updatePromo(pr: Promo, dt: number) {
		if (!pr.active) {
			pr.timer -= dt;
			if (pr.timer <= 0) {
				const c = pr.getPos();
				const dir = new THREE.Vector3(Math.random() - 0.5, 0.35 + Math.random() * 0.4, Math.random() - 0.5).normalize();
				const perp = new THREE.Vector3(-dir.z, 0, dir.x).normalize(), span = 1.3;
				pr.from.copy(c).addScaledVector(dir, span).addScaledVector(perp, (Math.random() - 0.5) * 0.8);
				pr.to.copy(c).addScaledVector(dir, -span).addScaledVector(perp, (Math.random() - 0.5) * 0.8);
				pr.prog = 0; pr.active = true; pr.trail.length = 0; pr.head.visible = true; pr.tail.visible = true;
			}
			return;
		}
		pr.prog += dt / 1.1;
		if (pr.prog >= 1) { pr.active = false; pr.head.visible = false; pr.tail.visible = false; pr.timer = 5 + Math.random() * 6; return; }
		const p = new THREE.Vector3().lerpVectors(pr.from, pr.to, pr.prog), fade = Math.sin(pr.prog * Math.PI);
		pr.head.position.copy(p); (pr.head.material as THREE.SpriteMaterial).opacity = fade; pr.head.scale.setScalar(0.12 + 0.10 * fade);
		pr.trail.unshift(p.clone()); if (pr.trail.length > pr.TAILN) pr.trail.pop();
		for (let i = 0; i < pr.TAILN; i++) { const q = pr.trail[Math.min(i, pr.trail.length - 1)]; pr.tp[i * 3] = q.x; pr.tp[i * 3 + 1] = q.y; pr.tp[i * 3 + 2] = q.z; }
		pr.tgeo.attributes.position.needsUpdate = true; pr.tgeo.setDrawRange(0, pr.trail.length);
		(pr.tail.material as THREE.LineBasicMaterial).opacity = 0.85 * fade;
	}
	for (const promo of promotions) {
		const pl = planets.find((p) => {
			const b = brands.find((br) => br.id === p.id);
			return b && b.slug.toLowerCase() === promo.brandSlug.toLowerCase();
		});
		if (pl) promos.push(makePromo(() => pl.grp.position));
	}

	// ── interaction ──
	const raycaster = new THREE.Raycaster();
	const ndc = new THREE.Vector2();
	const hitMeshes = clickables.map((c) => c.mesh);
	let hovered: Clickable | null = null;
	let selected: Clickable | null = null;
	let camAnim = false;
	let downX = 0, downY = 0;
	const focusTarget = new THREE.Vector3();

	// hover label element
	const label = document.createElement('div');
	label.style.cssText = 'position:fixed;transform:translate(-50%,-150%);pointer-events:none;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;letter-spacing:.18em;color:#F2E6CC;background:rgba(28,26,74,0.55);border:1px solid rgba(99,102,176,0.4);padding:3px 9px;border-radius:3px;opacity:0;transition:opacity .15s;white-space:nowrap;z-index:40';
	document.body.appendChild(label);

	function pick(ev: PointerEvent): Clickable | null {
		ndc.x = (ev.clientX / innerWidth) * 2 - 1;
		ndc.y = -(ev.clientY / innerHeight) * 2 + 1;
		raycaster.setFromCamera(ndc, camera);
		const hits = raycaster.intersectObjects(hitMeshes, false);
		if (hits.length) { const o = hits[0].object; return clickables.find((c) => c.mesh === o) ?? null; }
		return null;
	}
	function selectInternal(c: Clickable | null) {
		selected = c; camAnim = true;
		onSelect(c ? c.payload : null);
	}
	const onMove = (ev: PointerEvent) => { hovered = pick(ev); document.body.style.cursor = hovered ? 'pointer' : 'default'; };
	const onDown = (ev: PointerEvent) => { downX = ev.clientX; downY = ev.clientY; introDone = true; };
	const onUp = (ev: PointerEvent) => {
		if (Math.abs(ev.clientX - downX) > 4 || Math.abs(ev.clientY - downY) > 4) return;
		const c = pick(ev); selectInternal(c);
	};
	canvas.addEventListener('pointermove', onMove);
	canvas.addEventListener('pointerdown', onDown);
	canvas.addEventListener('pointerup', onUp);

	// intro state
	let introDone = false, introT = 0;
	const INTRO_DUR = 3.6;
	const introA = new THREE.Vector3(9, 22, 50), introB = new THREE.Vector3(0, 8.5, 21);

	// ── loop ──
	const clock = new THREE.Clock();
	let t = 0, raf = 0;
	function frame() {
		raf = requestAnimationFrame(frame);
		const dt = clock.getDelta();
		if (!reducedMotion) t += dt;

		for (const b of nebLayers) { b.m.quaternion.copy(camera.quaternion); b.u.uTime.value = t; }
		const pulse = 1.0 + 0.05 * Math.sin(t * 1.3); coreSprite.scale.set(2.4 * pulse, 2.4 * pulse, 1);

		for (const pl of planets) {
			if (!reducedMotion) { pl.angle += dt * pl.orbitSpeed; pl.grp.position.set(Math.cos(pl.angle) * pl.orbitR, 0, Math.sin(pl.angle) * pl.orbitR); pl.mesh.rotation.y += dt * pl.spin; }
			(pl.u.uTime as { value: number }).value = t;
			(pl.u.uCamPos as { value: THREE.Vector3 }).value.copy(camera.position);
		}
		if (ringU && sumaPlanet) (ringU.uPlanetPos as { value: THREE.Vector3 }).value.copy(sumaPlanet.grp.position);
		if (!reducedMotion) updateRocks(t);
		for (const u of dustRings) u.value = t;
		if (!reducedMotion) { motes.rotation.y += dt * 0.02; for (const pr of promos) updatePromo(pr, dt); }

		// intro zoom
		if (!introDone) {
			introT += dt; const k = Math.min(introT / INTRO_DUR, 1); const e = 1 - Math.pow(1 - k, 3);
			camera.position.lerpVectors(introA, introB, e); controls.target.set(0, 0, 0);
			if (k >= 1) introDone = true;
		}

		// constellation hover brighten
		const cl = !!(hovered && constHit && hovered.mesh === constHit);
		if (constLine) (constLine.material as THREE.LineBasicMaterial).opacity = THREE.MathUtils.lerp((constLine.material as THREE.LineBasicMaterial).opacity, cl ? 0.75 : 0.16, 0.14);
		for (const s of cstars) { const tgt = cl ? 2.4 : 1.6; s.scale.lerp(new THREE.Vector3(tgt, tgt, 1), 0.14); }

		// hover label
		if (hovered) {
			const v = hovered.pos().clone().project(camera);
			if (v.z < 1) { label.style.left = (v.x * 0.5 + 0.5) * innerWidth + 'px'; label.style.top = (-v.y * 0.5 + 0.5) * innerHeight + 'px'; label.textContent = hovered.payload.name; label.style.opacity = '1'; } else label.style.opacity = '0';
		} else label.style.opacity = '0';
		// hover scale planets
		for (const pl of planets) { const sc = hovered && hovered.mesh === pl.mesh ? 1.3 : 1.0; pl.mesh.scale.lerp(new THREE.Vector3(sc, sc, sc), 0.15); }

		// camera focus / follow
		if ((selected || camAnim) && introDone) {
			const isConst = !!(selected && constHit && selected.mesh === constHit);
			focusTarget.copy(selected && !isConst ? selected.pos() : SUN);
			controls.target.lerp(focusTarget, 0.06);
			const dir = camera.position.clone().sub(controls.target); let d = dir.length(); dir.normalize();
			const want = !selected ? 21 : isConst ? d : selected.focusDist;
			d = THREE.MathUtils.lerp(d, want, 0.045);
			camera.position.copy(controls.target).add(dir.multiplyScalar(d));
			if (!selected && controls.target.length() < 0.4 && Math.abs(d - 21) < 0.6) camAnim = false;
		}

		controls.update();
		renderer.render(scene, camera);
	}
	frame();

	// ── controller ──
	function resize() {
		camera.aspect = innerWidth / innerHeight;
		camera.updateProjectionMatrix();
		renderer.setSize(innerWidth, innerHeight);
	}
	function focus(id: string | null) {
		if (id === null) { selectInternal(null); return; }
		const c = clickables.find((x) => x.id === id);
		if (c) selectInternal(c);
	}
	function dispose() {
		cancelAnimationFrame(raf);
		canvas.removeEventListener('pointermove', onMove);
		canvas.removeEventListener('pointerdown', onDown);
		canvas.removeEventListener('pointerup', onUp);
		label.remove();
		controls.dispose();
		renderer.dispose();
		scene.traverse((o) => {
			const m = o as THREE.Mesh;
			if (m.geometry) m.geometry.dispose();
			const mat = (m as THREE.Mesh).material as THREE.Material | THREE.Material[] | undefined;
			if (Array.isArray(mat)) mat.forEach((x) => x.dispose());
			else mat?.dispose();
		});
		void disposables;
	}
	function entities(): ReadoutPayload[] {
		return clickables.map((c) => c.payload);
	}
	return { focus, entities, resize, dispose };
}
