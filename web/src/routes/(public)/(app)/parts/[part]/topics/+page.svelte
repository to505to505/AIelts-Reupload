<script lang="ts">
	import { page } from '$app/state';
	import { getPartColor } from '$lib/helpers/get-part-color.js';
	import TopicCard from './TopicCard.svelte';

	let { data } = $props();

	let part = $derived(page.params.part);
</script>

<aside class="px-6 pb-2 pt-4">
	<h3 class="text-h3 mb-2 font-semibold">Part {part}</h3>
	<p class="mb-4">
		{#if part === '1'}
			This section assess your ability to communicate about everyday subjects and familiar topics
		{:else if part === '2'}
			This section assesses your ability to speak at length on a given topic, using appropriate
			language and organizing your thoughts.
		{:else if part === '3'}
			This section assesses your ability to discuss abstract ideas, express opinions, and engage in
			a more detailed conversation on broader topics.
		{/if}
	</p>
	<p style:color={`var(--color-${getPartColor(part)}-600)`} class="font-semibold">
		{#if part === '1'}
			3 min • 4-9 questions
		{:else if part === '2'}
			2 min • 1 extended question
		{:else if part === '3'}
			3 min • 4-8 questions
		{/if}
	</p>
</aside>

<main class="space-y-2 p-4">
	{#each data.topics as topic (topic.id)}
		<TopicCard {topic} />
	{/each}
</main>
