<script lang="ts">
	import { onMount } from 'svelte';
	import {
		getBrands,
		getPublishedFieldNotes,
		getInitiatives,
		type Brand,
		type FieldNote,
		type Initiative
	} from '../../lib/api';
	// Type-only imports are erased at build time; the scene module (which pulls in three.js)
	// is loaded dynamically in onMount so it never runs during SSR.
	import type { OrreryController, ReadoutPayload, Promotion } from '../../lib/orrery/scene';

	let canvas: HTMLCanvasElement;
	let controller: OrreryController | null = null;

	// Promotions have no backend entity yet, so this stays empty and no shooting stars render
	// until a promotions/events endpoint exists. Nothing is fabricated.
	const promotions: Promotion[] = [];

	let selected = $state<ReadoutPayload | null>(null);
	let mode = $state<'sky' | 'grid'>('sky');
	let loading = $state(true);
	let brandError = $state('');
	let notesUnavailable = $state(false);
	let gridEntities = $state<ReadoutPayload[]>([]);

	function closeReadout(): void {
		controller?.focus(null); // the scene calls back onSelect(null), clearing `selected`
	}

	function selectFromGrid(id: string): void {
		controller?.focus(id);
		mode = 'sky';
	}

	function handleKeydown(event: KeyboardEvent): void {
		if (event.key !== 'Escape') return;
		if (mode === 'grid') mode = 'sky';
		else closeReadout();
	}

	onMount(() => {
		const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		window.addEventListener('keydown', handleKeydown);
		let disposed = false;

		void (async () => {
			// Load all three together, but keep the scene usable if any one collection fails.
			const [brandResult, noteResult, initiativeResult] = await Promise.allSettled([
				getBrands(),
				getPublishedFieldNotes(),
				getInitiatives()
			]);

			let brands: Brand[] = [];
			let notes: FieldNote[] = [];
			let initiatives: Initiative[] = [];

			if (brandResult.status === 'fulfilled') brands = brandResult.value;
			else brandError = brandResult.reason instanceof Error ? brandResult.reason.message : 'Request failed.';
			if (noteResult.status === 'fulfilled') notes = noteResult.value;
			else notesUnavailable = true;
			if (initiativeResult.status === 'fulfilled') initiatives = initiativeResult.value;

			loading = false;
			if (disposed) return;

			const { createOrrery } = await import('../../lib/orrery/scene');
			if (disposed) return;

			controller = createOrrery(canvas, {
				brands,
				notes,
				initiatives,
				promotions,
				reducedMotion,
				onSelect: (payload) => {
					selected = payload;
					if (payload) mode = 'sky';
				}
			});
			gridEntities = controller.entities();
		})();

		return () => {
			disposed = true;
			window.removeEventListener('keydown', handleKeydown);
			controller?.dispose();
			controller = null;
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

<svelte:window onresize={() => controller?.resize()} />

<main class="orrery">
	<canvas bind:this={canvas} class="scene"></canvas>

	<header class="topbar">
		<span class="wordmark">SHÉ</span>
		<div class="modebtn">
			<button class:on={mode === 'sky'} onclick={() => (mode = 'sky')}>SKY</button>
			<button class:on={mode === 'grid'} onclick={() => (mode = 'grid')}>GRID</button>
		</div>
	</header>

	{#if loading}
		<div class="toast">Charting the system…</div>
	{/if}
	{#if brandError}
		<div class="toast error">Couldn’t load brands — {brandError}</div>
	{/if}
	{#if notesUnavailable}
		<div class="toast muted">Field notes unavailable — the constellation is hidden.</div>
	{/if}

	{#if selected}
		<aside class="readout">
			<button class="pclose" onclick={closeReadout} aria-label="Close readout">×</button>
			<div class="pname">{selected.name}</div>
			<div class="pkind">{selected.subtitle}</div>
			{#if selected.status}<span class="pstatus">{selected.status}</span>{/if}
			<p class="pblurb">{selected.blurb}</p>
			<div class="pswatch" style="background:{selected.color}"></div>
		</aside>
	{/if}

	{#if mode === 'grid'}
		<div class="grid" role="dialog" aria-label="All worlds">
			<div class="gridinner">
				{#each gridEntities as entity (entity.id)}
					<button class="card" onclick={() => selectFromGrid(entity.id)}>
						<div class="cbar" style="background:{entity.color}"></div>
						<div class="cname">{entity.name}</div>
						<div class="ckind">{entity.subtitle}</div>
						{#if entity.status}<span class="cstat">{entity.status}</span>{/if}
					</button>
				{/each}
			</div>
		</div>
	{/if}
</main>

<style>
	.orrery {
		position: fixed;
		inset: 0;
		background: #000006;
		overflow: hidden;
		font-family: 'IBM Plex Mono', ui-monospace, monospace;
	}
	.scene {
		display: block;
		width: 100vw;
		height: 100vh;
	}

	.topbar {
		position: fixed;
		inset: 16px 0 auto 0;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 22px;
		z-index: 6;
		pointer-events: none;
	}
	.wordmark {
		font-size: 18px;
		letter-spacing: 0.28em;
		font-weight: 600;
		background: linear-gradient(120deg, #b7cef9, #a3a8c5, #c3e0c6, #f9e2b8);
		-webkit-background-clip: text;
		background-clip: text;
		color: transparent;
	}
	.modebtn {
		display: flex;
		border: 1px solid rgba(99, 102, 176, 0.4);
		border-radius: 20px;
		overflow: hidden;
		pointer-events: auto;
	}
	.modebtn button {
		background: transparent;
		color: #6366b0;
		border: 0;
		padding: 6px 18px;
		cursor: pointer;
		font: inherit;
		font-size: 10px;
		letter-spacing: 0.18em;
	}
	.modebtn button.on {
		background: rgba(99, 102, 176, 0.25);
		color: #f2e6cc;
	}

	.toast {
		position: fixed;
		left: 50%;
		bottom: 22px;
		transform: translateX(-50%);
		z-index: 6;
		font-size: 11px;
		letter-spacing: 0.1em;
		color: #d7cfbd;
		background: rgba(20, 18, 46, 0.72);
		border: 1px solid rgba(99, 102, 176, 0.3);
		border-radius: 6px;
		padding: 7px 14px;
	}
	.toast.error {
		color: #f2e6cc;
		border-color: rgba(185, 142, 94, 0.5);
	}
	.toast.muted {
		color: #6366b0;
	}

	.readout {
		position: fixed;
		right: 22px;
		top: 50%;
		transform: translateY(-50%);
		width: 272px;
		background: rgba(20, 18, 46, 0.82);
		backdrop-filter: blur(10px);
		-webkit-backdrop-filter: blur(10px);
		border: 1px solid rgba(99, 102, 176, 0.35);
		border-radius: 10px;
		padding: 18px 18px 20px;
		color: #d7cfbd;
		z-index: 4;
	}
	.readout .pclose {
		position: absolute;
		top: 10px;
		right: 14px;
		cursor: pointer;
		color: #6366b0;
		font-size: 18px;
		line-height: 1;
		background: none;
		border: 0;
	}
	.readout .pclose:hover {
		color: #f2e6cc;
	}
	.readout .pname {
		font-size: 18px;
		letter-spacing: 0.14em;
		color: #f2e6cc;
		margin-bottom: 3px;
	}
	.readout .pkind {
		font-size: 10px;
		letter-spacing: 0.16em;
		color: #6366b0;
		text-transform: uppercase;
		margin-bottom: 12px;
	}
	.readout .pstatus {
		display: inline-block;
		font-size: 10px;
		letter-spacing: 0.14em;
		color: #c4beb0;
		border: 1px solid rgba(196, 190, 176, 0.3);
		border-radius: 3px;
		padding: 2px 7px;
		margin-bottom: 13px;
	}
	.readout .pblurb {
		font-size: 12px;
		line-height: 1.62;
		margin: 0;
	}
	.readout .pswatch {
		height: 3px;
		border-radius: 2px;
		margin-top: 15px;
	}

	.grid {
		position: fixed;
		inset: 0;
		z-index: 5;
		background: rgba(6, 6, 15, 0.8);
		backdrop-filter: blur(7px);
		-webkit-backdrop-filter: blur(7px);
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding: 66px 24px 24px;
		overflow: auto;
	}
	.gridinner {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
		gap: 16px;
		width: 100%;
		max-width: 860px;
	}
	.card {
		text-align: left;
		background: rgba(20, 18, 46, 0.72);
		border: 1px solid rgba(99, 102, 176, 0.3);
		border-radius: 10px;
		padding: 16px;
		cursor: pointer;
		font: inherit;
		color: #d7cfbd;
		transition:
			border-color 0.15s,
			transform 0.15s;
	}
	.card:hover {
		border-color: rgba(242, 230, 204, 0.5);
		transform: translateY(-2px);
	}
	.card .cbar {
		height: 4px;
		border-radius: 2px;
		margin-bottom: 12px;
	}
	.card .cname {
		font-size: 15px;
		letter-spacing: 0.12em;
		color: #f2e6cc;
		margin-bottom: 3px;
	}
	.card .ckind {
		font-size: 9px;
		letter-spacing: 0.14em;
		color: #6366b0;
		text-transform: uppercase;
		margin-bottom: 10px;
	}
	.card .cstat {
		font-size: 9px;
		letter-spacing: 0.14em;
		color: #c4beb0;
		border: 1px solid rgba(196, 190, 176, 0.3);
		border-radius: 3px;
		padding: 2px 6px;
	}

	@media (prefers-reduced-motion: reduce) {
		.card {
			transition: none;
		}
	}
</style>
