<script lang="ts">
	import { mrg } from '$lib/helpers/mrg';
	import type { Snippet } from 'svelte';
	import { onMount } from 'svelte';

	interface Props {
		children: Snippet;
		modifiers?: string;
	}

	let { children, modifiers }: Props = $props();

	let root: null | HTMLDivElement = $state(null);
	let dragged = $state(false);
	let currentTouch: { x: number; y: number } | null = $state({ x: 0, y: 0 });
	let velX = $state(0);
	let accX = $state(0);
	let decelerationCoefficient = $state(0.92);

	const startDrag = (x: number, y: number) => {
		const clickedElement = document.elementFromPoint(x, y);
		if (clickedElement?.closest('[data-drag-slider-ignore]')) return;
		dragged = true;
	};

	let updateDrag = (movX: number) => {
		if (dragged && root) {
			accX = -movX;
		}
	};

	const stopDrag = () => {
		dragged = false;
		currentTouch = null;
	};

	const handleTouchMove = (event: any) => {
		const touch = event.touches[0];
		if (currentTouch) {
			const movX = touch.pageX - currentTouch.x;
			updateDrag(movX);
		}
		currentTouch = {
			x: touch.pageX,
			y: touch.pageY
		};
	};

	let currentFrame = 0;
	const update = () => {
		if (root) {
			velX += accX;
			if (dragged && Math.abs(velX) > Math.abs(accX)) velX = accX;
			root.scrollLeft += velX;
			accX = 0;
			velX *= decelerationCoefficient;
		}
		currentFrame = requestAnimationFrame(update);
	};

	onMount(() => {
		currentFrame = requestAnimationFrame(update);

		return () => cancelAnimationFrame(currentFrame);
	});
</script>

<div
	bind:this={root}
	class={mrg(
		'relative z-10 flex w-full max-w-full cursor-pointer select-none items-center gap-8 overflow-x-hidden px-5 *:select-none md:px-8',
		modifiers,
		dragged ? 'cursor-grab' : ''
	)}
	onmousedown={(e) => {
		startDrag(e.clientX, e.clientY);
	}}
	onmouseup={stopDrag}
	onmouseleave={stopDrag}
	onmousemove={(e) => updateDrag(e.movementX)}
	ontouchstart={(e) => startDrag(e.touches[0].clientX, e.touches[0].clientY)}
	ontouchend={stopDrag}
	ontouchmove={handleTouchMove}
	role={'swiper'}
>
	{@render children()}
</div>
