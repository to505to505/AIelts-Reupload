<script lang="ts">
	import EssentialCard from '../essentialCard.svelte';

	let { data } = $props();

	const content = data.topic.essentials;
	const words = content.key_words_and_phrases.phrasal_verbs;
</script>

<ul class="">
	{#each words as word}
		<EssentialCard content={word} />
	{/each}
</ul>
