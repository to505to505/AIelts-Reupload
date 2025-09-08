<script lang="ts">
	import EssentialCard from '../essentialCard.svelte';

	let { data } = $props();

	const content = data.topic.essentials;
	const samples = content.usage_tips.sample_answers;
</script>

<ul>
	{#each samples as sample}
		<EssentialCard content={sample} />
	{/each}
</ul>
