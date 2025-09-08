<script lang="ts">
	import type { Component, Snippet } from 'svelte';

	interface Props {
		icon?: Snippet;
		progress: number;
		title?: string;
		points?: number;
	}

	let { icon, progress, title, points }: Props = $props();
</script>

<div class="flex w-full flex-row items-center gap-3">
	{#if icon}
		{@render icon()}
	{/if}
	<div class="flex w-full flex-col gap-2">
		<div class="flex items-start justify-between">
			<h3 class="text-sm capitalize">{title}</h3>
			{#if points}
				<p class="text-md">{String(points.toFixed(1))}</p>
			{/if}
		</div>
		<div class="bg-whisper-100 relative h-2 w-full rounded-xl">
			<div class="bg-whisper-950 h-full rounded-xl" style:width={`${progress}%`}></div>
		</div>
	</div>
</div>
