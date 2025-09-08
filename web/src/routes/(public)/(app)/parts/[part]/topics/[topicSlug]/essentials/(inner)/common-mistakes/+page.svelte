<script lang="ts">
	import EssentialCard from '../essentialCard.svelte';

	let { data } = $props();

	const content = data.topic.essentials;
	const mistakes = content.usage_tips.common_mistakes;
</script>

<ul class="">
	{#each mistakes as mistake}
		<EssentialCard content={mistake} />
	{/each}
</ul>
