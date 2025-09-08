<script lang="ts">
	let { data } = $props();

	import EssentialCard from '../essentialCard.svelte';

	const content = data.topic.essentials;
	const words = content.key_words_and_phrases.collocations;
</script>

<ul class="">
	{#each words as word}
		<EssentialCard content={word} />
	{/each}
</ul>
