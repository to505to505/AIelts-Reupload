<script lang="ts">
	import EssentialCard from '../essentialCard.svelte';

	let { data } = $props();

	const content = data.topic.essentials;
	const expressions = content.expressions_and_idioms.expressions;
	const idioms = content.expressions_and_idioms.idioms;
	const joinedIdiomsAndExpression = [...expressions, ...idioms];
</script>

<ul class="">
	{#each joinedIdiomsAndExpression as joinedEntry}
		<EssentialCard content={joinedEntry} />
	{/each}
</ul>
