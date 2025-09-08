<script lang="ts">
	import { goto } from '$app/navigation';

	import ChevronRight from '$lib/assets/icons/chevronRight.svelte';
	import Button from '$lib/components/ui/button.svelte';

	import Part1 from '$lib/assets/icons/Part 1.svelte';
	import Part2 from '$lib/assets/icons/Part 2.svelte';
	import Part3 from '$lib/assets/icons/Part 3.svelte';
	import { statProvider } from '$lib/providers/stat';

	let history = $derived(statProvider.history);

	let clientWidth = $state(0);
</script>

<section class="pb-2 pl-6 pr-4 pt-2">
	<a
		class="bg-whilte border-whisper-500 hover:border-whisper-950 flex h-full w-full justify-between rounded border px-3 py-2 transition"
		href="/progress"
	>
		<h3 class="text-h3 font-semibold">Progress & Review</h3>
		<div><ChevronRight stroke="var(--color-whisper-950)" strokeWidth="2" /></div>
	</a>
</section>

{#if !history?.length}
	<section class="p-4">
		<div class="flex flex-col items-center space-y-6 rounded-lg bg-white px-4 pb-4 pt-6">
			<p class="max-w-[450px] text-center">
				Before you can see the statistics, please complete a few tasks so we can assess your
				speaking level
			</p>
			<Button onclick={() => goto('/full-section/prepare')} className="text-white w-full">
				Take a test
			</Button>
		</div>
	</section>
{/if}

<header class="text-h3 pb-2 pl-6 pr-4 pt-4 font-semibold">Speaking</header>
<section bind:clientWidth class="grid grid-cols-2 grid-rows-2 gap-2 px-4 py-2 text-lg">
	<a
		class="bg-chimera-200 relative block aspect-square size-full overflow-hidden rounded-lg p-4 transition hover:font-semibold"
		href="/parts/1/topics"
	>
		<p>Practice Part 1</p>
		<div class="absolute -bottom-16 -right-16">
			<Part1 size={clientWidth / 2} fill={'var(--color-chimera-600)'} />
		</div>
	</a>
	<a
		class="bg-mindaro-200 relative block aspect-square size-full overflow-hidden rounded-lg p-4 transition hover:font-semibold"
		href="/parts/2/topics"
	>
		<p>Practice Part 2</p>
		<div class="absolute -bottom-16 -right-16">
			<Part2 size={clientWidth / 2} fill={'var(--color-mindaro-600)'} />
		</div>
	</a>
	<a
		class="bg-rapture-200 relative block aspect-square size-full overflow-hidden rounded-lg p-4 transition hover:font-semibold"
		href="/parts/3/topics"
	>
		<p>Practice Part 3</p>
		<div class="absolute -bottom-16 -right-16">
			<Part3 size={clientWidth / 2} fill={'var(--color-rapture-600)'} />
		</div>
	</a>
	<a
		class="bg-whisper-950 relative block aspect-square size-full overflow-hidden rounded-lg p-4 text-white transition hover:font-semibold"
		href="/full-section/prepare"
	>
		<div class="relative z-10">
			<p>Take a Random Full</p>
			<p>Speaking Test</p>
		</div>
		<div class="absolute -bottom-10 -right-10 z-0">
			<Part1 size={clientWidth / 4} fill={'var(--color-chimera-600)'} />
		</div>
		<div class="absolute -right-10 top-[15%] z-0">
			<Part3 size={clientWidth / 4} fill={'var(--color-rapture-600)'} />
		</div>
		<div class="absolute -bottom-10 left-[20%] z-0">
			<Part2 size={clientWidth / 4} fill={'var(--color-mindaro-600)'} />
		</div>
	</a>
</section>
