<script lang="ts">
	import Shuffle from '$lib/assets/icons/shuffle.svelte';
	import AttemptCard from '$lib/components/widgets/AttemptCard.svelte';
	import { statProvider } from '$lib/providers/stat';

	const userHistory = $derived(statProvider.history?.filter((a) => !a.singlePart) || []);
</script>

<aside class="px-4 pb-2 pt-4">
	<h3 class="text-h3 px-2 pb-2 font-semibold">Full Section</h3>
	<a
		href="/full-section/prepare"
		class="border-whisper-500 flex w-full flex-col gap-y-2 rounded border px-4 py-4 pb-2"
	>
		<Shuffle fill={'var(--color-whisper-950)'} />
		<p class="text-left">Random test</p>
	</a>
</aside>

<main class="">
	<h4 class="px-7 pt-4 text-lg font-semibold">Completed</h4>
	<div class="bg-bg-gray mx-6 h-[1px]"></div>
	<div class="mb-2 ml-4 mt-4 w-fit rounded-lg border px-4 py-1">Recent tries</div>
	{#if !userHistory.length}
		<div class="space-y-2 p-4 text-center">
			<p class="font-semibold">No test completed yet :(</p>
			<p>Here you will be able to see the results of previous attempts</p>
		</div>
	{:else}
		<ul class="space-y-2 px-4">
			{#each userHistory as attempt (attempt.id)}
				<li>
					<AttemptCard {attempt} />
				</li>
			{/each}
		</ul>
	{/if}
</main>
