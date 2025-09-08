<script lang="ts">
	import type { Snippet } from 'svelte';
	import Portal from './portal.svelte';
	import { slide } from 'svelte/transition';
	import { mrg } from '$lib/helpers/mrg';

	interface Props {
		heading: string;
		children: Snippet;
		opened: boolean;
		className?: string;
	}

	let { heading, children, opened = $bindable(), className }: Props = $props();
</script>

{#if opened}
	<Portal bind:opened>
		<div
			transition:slide
			class={mrg(
				'rounded-t-4xl relative mx-auto h-[75%] max-w-3xl space-y-2 bg-white transition-transform',
				className
			)}
		>
			<h1 class="text-whisper-950 px-6 py-2 text-2xl font-bold">{heading}</h1>
			{@render children()}
		</div>
	</Portal>
{/if}
