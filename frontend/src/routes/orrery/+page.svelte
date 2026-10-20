<script lang="ts">
	import { onMount, tick } from 'svelte';
	import gsap from 'gsap';
	import { getBrands, getPublishedFieldNotes, type Brand, type FieldNote } from '../../lib/api';

	type Selection = { kind: 'brand'; item: Brand } | { kind: 'note'; item: FieldNote };
	type Point = { x: number; y: number };
	type Promotion = { id: string; path: string };

	const promotions: Promotion[] = [];
	const center = { x: 615, y: 455 };
	const placeholderStars: Point[] = [
		{ x: -58, y: 8 },
		{ x: -29, y: -19 },
		{ x: 0, y: -8 },
		{ x: 24, y: -43 },
		{ x: 47, y: -20 },
		{ x: 69, y: 12 }
	];
	let brands = $state<Brand[]>([]);
	let notes = $state<FieldNote[]>([]);
	let planetAngles = $state<number[]>([]);
	let selected = $state<Selection | null>(null);
	let loading = $state(true);
	let brandError = $state('');
	let notesUnavailable = $state(false);
	let mode = $state<'sky' | 'grid'>('sky');
	let notesHovered = $state(false);
	let reducedMotion = $state(false);
	let parallax = $state<Point>({ x: 0, y: 0 });
	let camera = $state({ x: 0, y: 0, scale: 1 });
	let skyElement: HTMLDivElement;
	let gridElement = $state<HTMLDivElement>();
	let readoutElement = $state<HTMLElement>();
	let wordmarkElement: HTMLSpanElement;
	let parallaxTweenTarget: Point | undefined;
	let planetDriftTarget: { progress: number } | undefined;
	let cameraFrame = 0;

	const planetPoints = $derived(
		brands.map((brand, index) => {
			const rx = 150 + index * 90;
			const ry = rx * 0.34;
			const angle = planetAngles[index] ?? 0;
			return {
				brand,
				index,
				rx,
				ry,
				radius: Math.max(5, 10 - index * 0.65),
				opacity: Math.max(0.58, 1 - index * 0.08),
				x: center.x + rx * Math.cos(angle),
				y: center.y + ry * Math.sin(angle)
			};
		})
	);

	const notePoints = $derived(
		notes.map((_, index) => {
			const angle = index * 2.4;
			const radius = 15 + 12 * Math.sqrt(index);
			return { x: Math.cos(angle) * radius, y: Math.sin(angle) * radius };
		})
	);

	const selectedBrandOrbit = $derived.by(() => {
		if (selected === null || selected.kind !== 'brand') return 0;
		const selectedId = selected.item.id;
		return brands.findIndex((brand) => brand.id === selectedId) + 1;
	});

	function planetColor(slug: string): string {
		switch (slug.toLowerCase()) {
			case 'suma':
				return 'var(--planet-suma)';
			case 'gida':
				return 'var(--planet-gida)';
			case 'tufa':
				return 'var(--planet-tufa)';
			case 'rocks':
				return 'var(--planet-rocks)';
			default:
				return 'var(--planet-fallback)';
		}
	}

	function selectBrand(brand: Brand, target?: SVGGElement): void {
		selected = { kind: 'brand', item: brand };
		if (target && !reducedMotion) {
			gsap.to('.planet-hit', {
				scale: 1,
				duration: 0.24,
				ease: 'power2.out',
				transformOrigin: 'center center',
				overwrite: true
			});
			gsap.to(target, {
				scale: 1.16,
				duration: 0.38,
				ease: 'power2.out',
				transformOrigin: 'center center',
				overwrite: true
			});
		}
		void animateReadout();
	}

	function selectNote(note: FieldNote): void {
		selected = { kind: 'note', item: note };
		void animateReadout();
	}

	async function toggleMode(): Promise<void> {
		const nextMode = mode === 'sky' ? 'grid' : 'sky';
		mode = nextMode;
		if (nextMode === 'grid') closeReadout();
		await tick();
		const target = nextMode === 'sky' ? skyElement : gridElement;
		if (target && !reducedMotion) {
			gsap.fromTo(
				target,
				{ opacity: 0.82, y: 8 },
				{ opacity: 1, y: 0, duration: 0.42, ease: 'power2.out', overwrite: true }
			);
		}
	}

	function closeReadout(): void {
		selected = null;
		if (!reducedMotion) {
			gsap.to('.planet-hit', {
				scale: 1,
				duration: 0.24,
				ease: 'power2.out',
				transformOrigin: 'center center',
				overwrite: true
			});
		}
	}

	function closeGrid(): void {
		mode = 'sky';
	}

	function selectBrandFromGrid(brand: Brand): void {
		mode = 'sky';
		selectBrand(brand);
	}

	function selectNoteFromGrid(note: FieldNote): void {
		mode = 'sky';
		selectNote(note);
	}

	function handleGlobalKeydown(event: KeyboardEvent): void {
		if (event.key !== 'Escape') return;
		if (mode === 'grid') {
			closeGrid();
			return;
		}
		closeReadout();
	}

	function handleSkyClick(event: PointerEvent): void {
		if (!(event.target instanceof Element)) return;
		if (!event.target.closest('.planet-hit, .note-hit')) closeReadout();
	}

	function handlePlanetKeydown(event: KeyboardEvent, brand: Brand): void {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			selectBrand(brand, event.currentTarget as SVGGElement);
		}
	}

	function handleNoteKeydown(event: KeyboardEvent, note: FieldNote): void {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			selectNote(note);
		}
	}

	async function animateReadout(): Promise<void> {
		await tick();
		if (readoutElement && !reducedMotion) {
			gsap.fromTo(
				readoutElement,
				{ opacity: 0, x: 18 },
				{ opacity: 1, x: 0, duration: 0.38, ease: 'power2.out', overwrite: true }
			);
		}
	}

	function animateWordmark(): void {
		if (wordmarkElement && !reducedMotion) {
			gsap.fromTo(
				wordmarkElement,
				{ scale: 0.96, opacity: 0.78 },
				{ scale: 1, opacity: 1, duration: 0.72, ease: 'power2.out', overwrite: true }
			);
		}
	}

	function handlePointerMove(event: PointerEvent): void {
		if (reducedMotion) return;
		const bounds =
			event.currentTarget instanceof HTMLElement
				? event.currentTarget.getBoundingClientRect()
				: null;
		if (!bounds) return;

		const x = ((event.clientX - bounds.left) / bounds.width - 0.5) * -12;
		const y = ((event.clientY - bounds.top) / bounds.height - 0.5) * -8;
		if (parallaxTweenTarget) gsap.killTweensOf(parallaxTweenTarget);
		parallaxTweenTarget = { x: parallax.x, y: parallax.y };
		const target = parallaxTweenTarget;
		gsap.to(target, {
			x,
			y,
			duration: 0.8,
			ease: 'power2.out',
			onUpdate: () => {
				parallax = { x: target.x, y: target.y };
				camera = { ...camera, x: target.x * 0.45, y: target.y * 0.45 };
			}
		});
	}

	function resetParallax(): void {
		if (reducedMotion) return;
		if (parallaxTweenTarget) gsap.killTweensOf(parallaxTweenTarget);
		parallaxTweenTarget = { x: parallax.x, y: parallax.y };
		const target = parallaxTweenTarget;
		gsap.to(target, {
			x: 0,
			y: 0,
			duration: 0.9,
			ease: 'power2.out',
			onUpdate: () => {
				parallax = { x: target.x, y: target.y };
				camera = { ...camera, x: target.x * 0.45, y: target.y * 0.45 };
			}
		});
	}

	onMount(() => {
		const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
		reducedMotion = motionPreference.matches;
		animateWordmark();
		window.addEventListener('keydown', handleGlobalKeydown);

		const cameraTween = { x: 0, y: 0, scale: 1 };
		if (!reducedMotion) {
			camera = { x: 0, y: 0, scale: 0.84 };
			cameraFrame = requestAnimationFrame(() => {
				if (reducedMotion) return;
				gsap.to(cameraTween, {
					x: -12,
					y: 8,
					scale: 1.06,
					duration: 1.4,
					ease: 'power2.out',
					onUpdate: () => {
						camera = { ...cameraTween };
					}
				});
			});
		}

		const handleMotionPreference = (event: MediaQueryListEvent) => {
			reducedMotion = event.matches;
			if (event.matches) {
				if (parallaxTweenTarget) gsap.killTweensOf(parallaxTweenTarget);
				if (planetDriftTarget) gsap.killTweensOf(planetDriftTarget);
				if (readoutElement) gsap.killTweensOf(readoutElement);
				gsap.killTweensOf(wordmarkElement);
				gsap.killTweensOf('.planet-hit');
				parallax = { x: 0, y: 0 };
				camera = { x: 0, y: 0, scale: 1 };
				planetAngles = brands.map(
					(_, index) => Math.PI * 0.2 + (index * Math.PI * 2) / Math.max(brands.length, 1)
				);
				gsap.killTweensOf(cameraTween);
				if (cameraFrame) cancelAnimationFrame(cameraFrame);
			} else {
				cameraTween.x = camera.x;
				cameraTween.y = camera.y;
				cameraTween.scale = camera.scale;
				gsap.to(cameraTween, {
					x: -12,
					y: 8,
					scale: 1.06,
					duration: 1.4,
					ease: 'power2.out',
					onUpdate: () => {
						camera = { ...cameraTween };
					}
				});
			}
		};
		motionPreference.addEventListener('change', handleMotionPreference);

		void (async () => {
			try {
				const [brandResult, noteResult] = await Promise.allSettled([
					getBrands(),
					getPublishedFieldNotes()
				]);
				if (brandResult.status === 'fulfilled') {
					brands = brandResult.value;
				} else {
					brandError =
						brandResult.reason instanceof Error ? brandResult.reason.message : 'Request failed.';
				}
				if (noteResult.status === 'fulfilled') {
					notes = noteResult.value;
				} else {
					notesUnavailable = true;
				}

				const restingAngles = brands.map(
					(_, index) => Math.PI * 0.2 + (index * Math.PI * 2) / Math.max(brands.length, 1)
				);
				planetAngles = restingAngles;
				await tick();

				if (!reducedMotion && restingAngles.length > 0) {
					planetDriftTarget = { progress: 0 };
					const startingAngles = restingAngles.map((angle, index) =>
						brands[index].status === 'active' ? angle - 0.14 : angle
					);
					planetAngles = startingAngles;
					gsap.to(planetDriftTarget, {
						progress: 1,
						duration: 1.25,
						ease: 'power2.out',
						onUpdate: () => {
							planetAngles = startingAngles.map(
								(angle, index) =>
									angle +
									(brands[index].status === 'active'
										? 0.14 * (planetDriftTarget?.progress ?? 1)
										: 0)
							);
						}
					});
				}
			} finally {
				loading = false;
			}
		})();

		return () => {
			window.removeEventListener('keydown', handleGlobalKeydown);
			motionPreference.removeEventListener('change', handleMotionPreference);
			if (cameraFrame) cancelAnimationFrame(cameraFrame);
			if (parallaxTweenTarget) gsap.killTweensOf(parallaxTweenTarget);
			if (planetDriftTarget) gsap.killTweensOf(planetDriftTarget);
			gsap.killTweensOf(cameraTween);
		};
	});
</script>

<svelte:head>
	<title>SHÉ OS · Orrery</title>
	<meta
		name="description"
		content="A live spatial view of SHÉ ESTATE brands and published field notes."
	/>
</svelte:head>

<main class="orrery-app" data-promotions={promotions.length}>
	<header class="topbar">
		<div class="identity">
			<button
				class="wordmark"
				type="button"
				bind:this={wordmarkElement}
				onmouseenter={animateWordmark}
				onclick={animateWordmark}
				aria-label="SHÉ ESTATE">SHÉ</button
			>
			<span class="topbar-caption">ESTATE <span aria-hidden="true">/</span> OPERATING SYSTEM</span>
		</div>
		<div class="topbar-actions">
			<span class="topbar-coordinate">FIELD INSTRUMENT · 01</span>
			<button class="mode-toggle" type="button" aria-pressed={mode === 'grid'} onclick={toggleMode}>
				<span class="toggle-mark" aria-hidden="true">{mode === 'sky' ? '▦' : '◉'}</span>
				{mode === 'sky' ? 'Grid view' : 'Sky view'}
			</button>
		</div>
	</header>

	<section class="instrument" aria-label="SHÉ estate instrument">
		<div
			class="sky"
			bind:this={skyElement}
			role="region"
			aria-label="Spatial sky"
			onpointerdown={handleSkyClick}
			onpointermove={handlePointerMove}
			onpointerleave={resetParallax}
		>
			<div class="scene-title">
				<p class="micro-label">A SYSTEM IN MOTION</p>
				<h1>One estate.<br />Many worlds.</h1>
			</div>

			<svg
				class="sky-map"
				viewBox="0 0 1380 900"
				preserveAspectRatio="xMidYMid meet"
				role="group"
				aria-label="Elliptical brand orbits and published field note constellation"
			>
				<defs>
					<radialGradient id="sun-glow">
						<stop offset="0%" stop-color="#F2E6CC" stop-opacity="0.2" />
						<stop offset="42%" stop-color="#F2E6CC" stop-opacity="0.07" />
						<stop offset="100%" stop-color="#F2E6CC" stop-opacity="0" />
					</radialGradient>
					{#each planetPoints as point (point.brand.id)}
						<radialGradient id={`planet-gradient-${point.index}`} cx="32%" cy="28%" r="78%">
							<stop offset="0%" stop-color={planetColor(point.brand.slug)} />
							<stop offset="54%" stop-color={planetColor(point.brand.slug)} />
							<stop offset="100%" stop-color="#0A0A18" stop-opacity="0.78" />
						</radialGradient>
					{/each}
				</defs>

				<g
					transform={`translate(${center.x + camera.x} ${center.y + camera.y}) scale(${camera.scale}) translate(${-center.x} ${-center.y})`}
				>
					<g transform={`translate(${parallax.x * 0.8} ${parallax.y * 0.8})`}>
						{#each planetPoints as point (point.brand.id)}
							<ellipse
								cx={center.x}
								cy={center.y}
								rx={point.rx}
								ry={point.ry}
								class="orbit"
								class:orbit-active={point.brand.status === 'active'}
							/>
							<path
								d={`M ${center.x - point.rx} ${center.y} A ${point.rx} ${point.ry} 0 0 0 ${center.x + point.rx} ${center.y}`}
								class="orbit-front"
							/>
						{/each}

						<circle cx={center.x} cy={center.y} r="116" fill="url(#sun-glow)" />
						<circle cx={center.x} cy={center.y} r="47" class="sun-halo" />
						<circle cx={center.x} cy={center.y} r="33" class="sun-core" />
						<text x={center.x} y={center.y + 2} class="sun-label" text-anchor="middle">SHÉ</text>
						<text x={center.x} y={center.y + 56} class="sun-subtitle" text-anchor="middle">
							ESTATE
						</text>

						{#each planetPoints as point (point.brand.id)}
							<g
								role="button"
								tabindex="0"
								data-brand-id={point.brand.id}
								aria-label={`Select ${point.brand.name}, ${point.brand.status}`}
								aria-pressed={selected?.kind === 'brand' && selected.item.id === point.brand.id}
								class="planet-hit"
								class:inactive={point.brand.status !== 'active'}
								class:selected={selected?.kind === 'brand' && selected.item.id === point.brand.id}
								onclick={(event) => selectBrand(point.brand, event.currentTarget)}
								onkeydown={(event) => handlePlanetKeydown(event, point.brand)}
							>
								<circle cx={point.x} cy={point.y} r="19" class="planet-selection" />
								<circle
									cx={point.x}
									cy={point.y}
									r={point.radius}
									fill={`url(#planet-gradient-${point.index})`}
									opacity={point.opacity}
									class="planet"
								/>
								<text x={point.x + 16} y={point.y - 12} class="planet-label" text-anchor="start"
									>{point.brand.name}</text
								>
							</g>
						{/each}
					</g>

					<g
						class="editions-cluster"
						class:cluster-hovered={notesHovered}
						transform={`translate(${1050 + parallax.x * 1.3} ${690 + parallax.y * 1.3})`}
						role="group"
						aria-label="Published field notes constellation"
						onmouseenter={() => (notesHovered = true)}
						onmouseleave={() => (notesHovered = false)}
					>
						<text x="0" y="-94" class="cluster-label">EDITIONS</text>
						{#if notes.length === 0}
							{#each placeholderStars as star, index (index)}
								{#if notesHovered && index < placeholderStars.length - 1}
									<line
										x1={star.x}
										y1={star.y}
										x2={placeholderStars[index + 1].x}
										y2={placeholderStars[index + 1].y}
										class="constellation-line"
									/>
								{/if}
								<circle
									cx={star.x}
									cy={star.y}
									r={index === 2 ? 2.5 : 1.8}
									class="note-star placeholder-star"
								/>
							{/each}
							<text x="0" y="45" class="cluster-empty">
								{notesUnavailable ? 'FIELD NOTES UNAVAILABLE' : 'NO PUBLISHED NOTES'}
							</text>
						{:else}
							{#each notePoints as point, index (notes[index].id)}
								{#if notesHovered && index < notePoints.length - 1}
									<line
										x1={point.x}
										y1={point.y}
										x2={notePoints[index + 1].x}
										y2={notePoints[index + 1].y}
										class="constellation-line"
									/>
								{/if}
							{/each}
							{#each notes as note, index (note.id)}
								<g
									role="button"
									tabindex="0"
									aria-label={`Read field note: ${note.title}`}
									aria-pressed={selected?.kind === 'note' && selected.item.id === note.id}
									class="note-hit"
									class:note-selected={selected?.kind === 'note' && selected.item.id === note.id}
									onclick={() => selectNote(note)}
									onkeydown={(event) => handleNoteKeydown(event, note)}
								>
									<circle
										cx={notePoints[index].x}
										cy={notePoints[index].y}
										r="11"
										class="note-target"
									/>
									<circle
										cx={notePoints[index].x}
										cy={notePoints[index].y}
										r={index % 4 === 0 ? 2.8 : 2}
										class="note-star"
									/>
								</g>
							{/each}
						{/if}
					</g>

					{#each promotions as promotion (promotion.id)}
						<path d={promotion.path} class="promotion-trail" aria-hidden="true" />
					{/each}

					{#if brandError}
						<text x="70" y="180" class="api-message">BRANDS UNAVAILABLE · {brandError}</text>
					{:else if !loading && brands.length === 0}
						<text x="70" y="180" class="api-message">NO BRANDS RETURNED FROM THE API</text>
					{/if}
				</g>
			</svg>

			<div class="scene-footer">
				<span>BRANDS · {brands.length.toString().padStart(2, '0')}</span>
				<span class="footer-separator">/</span>
				<span>EDITIONS · {notes.length.toString().padStart(2, '0')}</span>
				<span class="footer-hint">SELECT A BODY TO READ ITS SIGNAL</span>
			</div>
		</div>

		{#if mode === 'grid'}
			<div
				class="grid-overlay"
				bind:this={gridElement}
				role="dialog"
				aria-modal="true"
				aria-labelledby="grid-title"
			>
				<div class="grid-overlay-header">
					<div class="grid-heading">
						<p class="micro-label">INSTRUMENT VOICE · INDEX</p>
						<h1 id="grid-title">Field index</h1>
						<p class="grid-description">A flat reading of every brand and published edition.</p>
					</div>
					<button
						class="close-control grid-close"
						type="button"
						aria-label="Close field index"
						onclick={closeGrid}
					>
						<span aria-hidden="true">×</span>
					</button>
				</div>

				{#if loading}
					<p class="grid-empty" role="status">Reading live API…</p>
				{:else}
					{#if brandError}
						<p class="grid-empty" role="status">Brands unavailable: {brandError}</p>
					{/if}
					{#if notesUnavailable}
						<p class="quiet-notice" role="status">
							Published editions are temporarily unavailable.
						</p>
					{/if}
					<div class="card-grid">
						{#each brands as brand (brand.id)}
							<button class="index-card" type="button" onclick={() => selectBrandFromGrid(brand)}>
								<span class="card-kind">
									BRAND · <span class="card-status">{brand.status}</span>
								</span>
								<span class="card-title brand-card-title">{brand.name}</span>
								<span class="card-detail">/{brand.slug}</span>
							</button>
						{/each}
						{#each notes as note (note.id)}
							<button class="index-card" type="button" onclick={() => selectNoteFromGrid(note)}>
								<span class="card-kind">EDITION · {note.theme || 'FIELD NOTE'}</span>
								<span class="card-title">{note.title}</span>
								<span class="card-detail">{note.excerpt || 'Published field note'}</span>
							</button>
						{/each}
					</div>
					{#if brands.length === 0 && notes.length === 0}
						<p class="grid-empty">No brands or published notes are available yet.</p>
					{/if}
				{/if}
			</div>
		{/if}

		{#if selected && mode === 'sky'}
			<aside class="readout" class:has-selection={selected !== null} bind:this={readoutElement}>
				<div class="readout-topline">
					<p class="micro-label">INSTRUMENT VOICE · DATA</p>
					<button
						class="close-control readout-close"
						type="button"
						aria-label="Close readout"
						onclick={closeReadout}
					>
						<span aria-hidden="true">×</span>
					</button>
				</div>
				{#if selected.kind === 'brand'}
					<div class="readout-content">
						<p class="readout-type">
							BRAND BODY · ORBIT {selectedBrandOrbit.toString().padStart(2, '0')}
						</p>
						<h2
							class="brand-readout-title"
							class:suma-title={selected.item.slug.toLowerCase() === 'suma'}
						>
							{selected.item.name}
						</h2>
						<p class="status-readout">{selected.item.status}</p>
						<dl class="data-list">
							<div>
								<dt>SLUG</dt>
								<dd>/{selected.item.slug}</dd>
							</div>
							<div>
								<dt>ABOUT</dt>
								<dd>{selected.item.description || 'No description recorded.'}</dd>
							</div>
						</dl>
						<!-- TODO: add the authenticated zoom-into-world transition here. -->
						<p class="readout-footnote">
							ORBIT STABLE <span aria-hidden="true">·</span> WORLD ACCESS LATER
						</p>
					</div>
				{:else}
					<div class="readout-content">
						<p class="readout-type">PUBLISHED EDITION</p>
						<h2 class="note-readout-title">{selected.item.title}</h2>
						<p class="note-theme">{selected.item.theme || 'FIELD NOTE'}</p>
						<p class="note-excerpt">
							{selected.item.excerpt || selected.item.description || 'No excerpt available.'}
						</p>
						{#if selected.item.tags?.length}
							<ul class="tag-list" aria-label="Tags">
								{#each selected.item.tags as tag (tag)}
									<li>{tag}</li>
								{/each}
							</ul>
						{/if}
						<p class="readout-footnote">EDITION · {selected.item.slug || selected.item.id}</p>
					</div>
				{/if}
			</aside>
		{/if}
	</section>
</main>

<style>
	.orrery-app {
		--rail-width: 330px;
		position: relative;
		min-height: 100vh;
		overflow: hidden;
		background: var(--ground);
		color: var(--starlight);
		font-family: 'Manrope', sans-serif;
	}

	.topbar {
		position: relative;
		z-index: 5;
		display: flex;
		height: 86px;
		align-items: center;
		justify-content: space-between;
		padding: 0 4.2vw;
		border-bottom: 1px solid rgb(196 190 176 / 10%);
	}

	.identity,
	.topbar-actions {
		display: flex;
		align-items: center;
	}

	.identity {
		gap: 1rem;
		color: inherit;
		text-decoration: none;
	}

	.wordmark {
		display: inline-block;
		padding: 0;
		border: 0;
		background-color: transparent;
		background: linear-gradient(112deg, #f2e6cc 8%, #bdc1eb 35%, #d7cfbd 61%, #9ea9db 82%);
		background-clip: text;
		color: transparent;
		font-family: 'Archivo Black', sans-serif;
		font-size: 1.65rem;
		letter-spacing: -0.09em;
		cursor: pointer;
		-webkit-background-clip: text;
	}

	.topbar-caption,
	.topbar-coordinate,
	.mode-toggle,
	.micro-label,
	.scene-footer,
	.readout-type,
	.data-list,
	.readout-footnote,
	.cluster-label,
	.cluster-empty,
	.api-message,
	.card-kind,
	.card-detail,
	.status-readout,
	.note-theme {
		font-family: 'Space Mono', monospace;
	}

	.topbar-caption {
		color: var(--metal-shadow);
		font-size: 0.59rem;
		letter-spacing: 0.12em;
	}

	.topbar-caption span {
		padding: 0 0.45rem;
		color: var(--label);
	}

	.topbar-actions {
		gap: 1.65rem;
	}

	.topbar-coordinate {
		color: var(--label);
		font-size: 0.58rem;
		letter-spacing: 0.07em;
	}

	.mode-toggle {
		display: inline-flex;
		min-height: 38px;
		align-items: center;
		gap: 0.6rem;
		padding: 0 0.9rem;
		border: 1px solid rgb(196 190 176 / 25%);
		border-radius: 999px;
		background: transparent;
		color: var(--body-cream);
		cursor: pointer;
		font-size: 0.68rem;
		transition:
			border-color 180ms ease,
			background 180ms ease,
			color 180ms ease;
	}

	.mode-toggle:hover,
	.mode-toggle[aria-pressed='true'] {
		border-color: var(--metal);
		background: rgb(44 46 99 / 45%);
		color: var(--starlight);
	}

	.toggle-mark {
		color: var(--metal);
		font-size: 0.85rem;
	}

	.instrument {
		position: relative;
		min-height: calc(100vh - 87px);
	}

	.sky {
		position: relative;
		min-height: calc(100vh - 87px);
		overflow: hidden;
	}

	.sky-map {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		min-height: 650px;
		overflow: visible;
	}

	.scene-title,
	.scene-footer {
		position: absolute;
		z-index: 1;
		pointer-events: none;
	}

	.scene-title {
		top: 8.2%;
		left: 5.1%;
	}

	.micro-label {
		margin: 0;
		color: var(--label);
		font-size: 0.57rem;
		letter-spacing: 0.16em;
	}

	.scene-title h1,
	.grid-heading h1 {
		margin: 0.8rem 0 0;
		font-family: 'Archivo Black', sans-serif;
		font-size: clamp(2rem, 4vw, 3.6rem);
		font-weight: 400;
		letter-spacing: -0.065em;
		line-height: 0.98;
	}

	.orbit {
		fill: none;
		stroke: var(--metal);
		stroke-opacity: 0.22;
		stroke-width: 1;
	}

	.orbit-active {
		stroke-opacity: 0.3;
	}

	.orbit-front {
		fill: none;
		stroke: var(--metal);
		stroke-opacity: 0.34;
		stroke-width: 1;
	}

	.sun-halo {
		fill: var(--indigo-lit);
		fill-opacity: 0.12;
		stroke: var(--metal);
		stroke-opacity: 0.42;
		stroke-width: 1;
	}

	.sun-core {
		fill: var(--indigo-deep);
		stroke: var(--metal);
		stroke-opacity: 0.7;
		stroke-width: 1;
	}

	.sun-label {
		fill: var(--starlight);
		font-family: 'Archivo Black', sans-serif;
		font-size: 14px;
		letter-spacing: -0.06em;
	}

	.sun-subtitle {
		fill: var(--metal);
		font-family: 'Space Mono', monospace;
		font-size: 6px;
		letter-spacing: 0.18em;
	}

	.planet-hit,
	.note-hit {
		cursor: pointer;
		outline: none;
	}

	.planet-selection,
	.note-target {
		fill: transparent;
		stroke: var(--starlight);
		stroke-opacity: 0;
		stroke-width: 1;
		transition:
			stroke-opacity 180ms ease,
			r 180ms ease;
	}

	.planet-hit:hover .planet-selection,
	.planet-hit:focus-visible .planet-selection,
	.planet-hit.selected .planet-selection {
		stroke-opacity: 0.72;
	}

	.planet {
		filter: drop-shadow(1px 1px 2px rgb(10 10 24 / 70%));
	}

	.planet-hit.inactive {
		opacity: 0.36;
	}

	.planet-hit.inactive .planet {
		filter: none;
	}

	.planet-label {
		fill: var(--body-cream);
		font-family: 'Manrope', sans-serif;
		font-size: 10px;
		font-weight: 500;
		opacity: 0.74;
	}

	.editions-cluster {
		cursor: default;
	}

	.cluster-label {
		fill: var(--label);
		font-size: 8px;
		letter-spacing: 0.18em;
		text-anchor: middle;
	}

	.cluster-empty {
		fill: var(--label);
		font-size: 6px;
		letter-spacing: 0.1em;
		text-anchor: middle;
	}

	.note-star {
		fill: var(--starlight);
		opacity: 0.47;
		transition:
			opacity 220ms ease,
			r 220ms ease;
	}

	.cluster-hovered .note-star,
	.note-hit:hover .note-star,
	.note-hit:focus-visible .note-star,
	.note-hit.note-selected .note-star {
		opacity: 1;
	}

	.placeholder-star {
		opacity: 0.22;
	}

	.cluster-hovered .placeholder-star {
		opacity: 0.72;
	}

	.note-target {
		stroke: var(--starlight);
		stroke-opacity: 0;
	}

	.note-hit:hover .note-target,
	.note-hit:focus-visible .note-target,
	.note-hit.note-selected .note-target {
		stroke-opacity: 0.55;
	}

	.constellation-line {
		stroke: var(--starlight);
		stroke-opacity: 0.42;
		stroke-width: 0.8;
	}

	.api-message {
		fill: var(--body-cream);
		font-size: 8px;
		letter-spacing: 0.1em;
	}

	.scene-footer {
		bottom: 4.2%;
		left: 5.1%;
		display: flex;
		align-items: center;
		gap: 0.75rem;
		color: var(--metal-shadow);
		font-size: 0.56rem;
		letter-spacing: 0.09em;
	}

	.footer-separator {
		color: var(--label);
	}

	.footer-hint {
		margin-left: 1.15rem;
		color: var(--label);
	}

	.readout {
		position: absolute;
		z-index: 3;
		top: 9%;
		right: 3.2%;
		width: min(var(--rail-width), 29vw);
		min-height: 350px;
		padding: 1.45rem 1.35rem;
		border: 1px solid rgb(196 190 176 / 19%);
		border-radius: 3px;
		background: rgb(44 46 99 / 32%);
		box-shadow: 0 18px 70px rgb(10 10 24 / 18%);
		backdrop-filter: blur(14px);
		-webkit-backdrop-filter: blur(14px);
	}

	.close-control {
		display: grid;
		width: 34px;
		height: 34px;
		flex: 0 0 auto;
		place-items: center;
		border: 1px solid rgb(196 190 176 / 26%);
		border-radius: 50%;
		background: rgb(10 10 24 / 32%);
		color: var(--body-cream);
		cursor: pointer;
		font-family: 'Manrope', sans-serif;
		font-size: 1.45rem;
		font-weight: 300;
		line-height: 1;
		transition:
			border-color 180ms ease,
			color 180ms ease,
			background 180ms ease;
	}

	.close-control:hover,
	.close-control:focus-visible {
		border-color: var(--metal);
		background: rgb(44 46 99 / 62%);
		color: var(--starlight);
	}

	.readout-topline {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.6rem;
		padding-bottom: 1rem;
		border-bottom: 1px solid rgb(196 190 176 / 13%);
	}

	.readout-content {
		padding-top: 1.5rem;
	}

	.readout-type {
		margin: 0 0 0.65rem;
		color: var(--label);
		font-size: 0.55rem;
		letter-spacing: 0.13em;
	}

	.brand-readout-title,
	.note-readout-title {
		margin: 0;
		color: var(--starlight);
	}

	.brand-readout-title {
		font-family: 'Manrope', sans-serif;
		font-size: clamp(1.9rem, 3vw, 2.7rem);
		font-weight: 300;
		letter-spacing: -0.07em;
		line-height: 1.05;
	}

	.brand-readout-title.suma-title {
		font-family: 'Fraunces', serif;
		font-weight: 500;
	}

	.status-readout {
		margin: 0.75rem 0 1.5rem;
		color: var(--metal);
		font-size: 0.62rem;
		letter-spacing: 0.15em;
		text-transform: uppercase;
	}

	.data-list {
		display: grid;
		gap: 1.05rem;
		margin: 0;
		font-size: 0.62rem;
		line-height: 1.6;
	}

	.data-list div {
		display: grid;
		grid-template-columns: 4.1rem minmax(0, 1fr);
		gap: 0.7rem;
	}

	.data-list dt {
		color: var(--label);
		font-weight: 700;
	}

	.data-list dd {
		margin: 0;
		color: var(--body-cream);
		overflow-wrap: anywhere;
	}

	.readout-footnote {
		margin: 2rem 0 0;
		color: var(--metal-shadow);
		font-size: 0.5rem;
		letter-spacing: 0.08em;
	}

	.readout-footnote span {
		color: var(--metal);
	}

	.note-readout-title {
		font-family: 'Archivo Black', sans-serif;
		font-size: clamp(1.6rem, 2.4vw, 2.25rem);
		font-weight: 400;
		letter-spacing: -0.055em;
		line-height: 1.02;
		text-transform: uppercase;
	}

	.note-theme {
		margin: 1rem 0;
		color: var(--label);
		font-size: 0.61rem;
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}

	.note-excerpt {
		margin: 0;
		color: var(--body-cream);
		font-size: 0.85rem;
		font-weight: 300;
		line-height: 1.75;
	}

	.tag-list {
		display: flex;
		flex-wrap: wrap;
		gap: 0.45rem;
		margin: 1.2rem 0 0;
		padding: 0;
		list-style: none;
	}

	.tag-list li {
		padding: 0.28rem 0.48rem;
		border: 1px solid rgb(196 190 176 / 22%);
		border-radius: 999px;
		color: var(--body-cream);
		font-size: 0.62rem;
	}

	.grid-overlay {
		position: fixed;
		z-index: 8;
		inset: 0;
		overflow: auto;
		padding: 7vh 4.8vw 6rem;
		background: rgb(44 46 99 / 74%);
		backdrop-filter: blur(24px);
		-webkit-backdrop-filter: blur(24px);
	}

	.grid-overlay-header {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: 1.5rem;
		margin-bottom: 2.5rem;
	}

	.grid-heading {
		max-width: 620px;
	}

	.grid-heading h1 {
		font-size: clamp(2.2rem, 5vw, 4.4rem);
	}

	.grid-description {
		margin: 1rem 0 0;
		color: var(--body-cream);
		font-size: 0.9rem;
		font-weight: 300;
	}

	.card-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
		gap: 0.85rem;
	}

	.quiet-notice {
		margin: 0 0 1rem;
		color: var(--metal-shadow);
		font-size: 0.72rem;
	}

	.index-card {
		display: flex;
		min-height: 170px;
		flex-direction: column;
		align-items: flex-start;
		padding: 1.15rem;
		border: 1px solid rgb(196 190 176 / 18%);
		border-radius: 3px;
		background: rgb(28 26 74 / 32%);
		text-align: left;
		cursor: pointer;
		transition:
			border-color 180ms ease,
			background 180ms ease;
	}

	.index-card:hover,
	.index-card:focus-visible {
		border-color: rgb(196 190 176 / 52%);
		background: rgb(44 46 99 / 36%);
	}

	.card-kind {
		color: var(--label);
		font-size: 0.52rem;
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}

	.card-status {
		color: var(--metal);
	}

	.card-title {
		margin-top: 1rem;
		color: var(--starlight);
		font-family: 'Archivo Black', sans-serif;
		font-size: 1.1rem;
		letter-spacing: -0.04em;
		text-transform: uppercase;
	}

	.brand-card-title {
		color: var(--starlight);
		font-family: 'Manrope', sans-serif;
		font-size: 1.3rem;
		font-weight: 400;
		text-transform: none;
	}

	.card-detail {
		display: -webkit-box;
		margin-top: 0.55rem;
		overflow: hidden;
		color: var(--metal-shadow);
		font-size: 0.56rem;
		line-height: 1.55;
		-webkit-box-orient: vertical;
		line-clamp: 2;
		-webkit-line-clamp: 2;
	}

	.grid-empty {
		color: var(--body-cream);
		font-size: 0.8rem;
	}

	@media (max-width: 980px) {
		.orrery-app {
			--rail-width: 285px;
		}

		.topbar {
			padding: 0 3vw;
		}

		.topbar-coordinate {
			display: none;
		}

		.readout {
			right: 2.5%;
			width: 275px;
		}
	}

	@media (max-width: 700px) {
		.orrery-app {
			overflow: hidden;
		}

		.topbar {
			height: 72px;
			padding: 0 1.1rem;
		}

		.topbar-caption {
			display: none;
		}

		.topbar-actions {
			gap: 0;
		}

		.instrument,
		.sky {
			min-height: calc(100dvh - 73px);
		}

		.sky-map {
			top: 0;
			left: -45%;
			width: 145%;
			height: 72%;
			min-height: 480px;
		}

		.scene-title {
			top: 5%;
			left: 6%;
		}

		.scene-title h1 {
			font-size: 2.25rem;
		}

		.readout {
			position: fixed;
			top: auto;
			right: 0.7rem;
			bottom: 0.7rem;
			left: 0.7rem;
			width: auto;
			min-height: 0;
			max-height: 43dvh;
			overflow: auto;
			padding: 1rem 1.1rem;
			background: rgb(44 46 99 / 68%);
		}

		.readout-content {
			padding-top: 1rem;
		}

		.readout-footnote {
			margin-top: 1.1rem;
		}

		.scene-footer {
			bottom: 47%;
			left: 6%;
			flex-wrap: wrap;
			font-size: 0.48rem;
		}

		.footer-hint {
			display: none;
		}

		.grid-overlay {
			padding: 5vh 1.1rem 3rem;
		}

		.grid-overlay-header {
			gap: 0.75rem;
			margin-bottom: 1.7rem;
		}

		.card-grid {
			grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
		}

		.index-card {
			min-height: 145px;
			padding: 0.9rem;
		}

		.cluster-label {
			font-size: 10px;
		}
	}

	@media (prefers-reduced-motion: reduce) {
		*,
		*::before,
		*::after {
			scroll-behavior: auto !important;
			animation-duration: 0.01ms !important;
			animation-iteration-count: 1 !important;
			transition-duration: 0.01ms !important;
		}
	}
</style>
