<script lang="ts">
	import { page } from '$app/state';
	import ArrowRefresh from '$lib/assets/icons/arrowRefresh.svelte';
	import Questions from '$lib/assets/icons/questions.svelte';
	import { mrg } from '$lib/helpers/mrg';
	import BottomModal from '$lib/components/ui/bottomModal.svelte';
	import { getPartColor } from '$lib/helpers/get-part-color.js';
	import { onMount } from 'svelte';
	import { parseQuestionsFromTask } from '$lib/helpers/parse-questions-from-task.js';
	import AttemptCard from '$lib/components/widgets/AttemptCard.svelte';
	import { statProvider } from '$lib/providers/stat/stat.svelte.js';

	const part = $derived(page.params.part);

	let { data } = $props();

	const { task, topic } = data;

	let showQuestions = $state(false);

	let questions: string[] = $state([]);

	onMount(() => {
		questions = parseQuestionsFromTask(task);
	});

	const taskMap = $derived(statProvider.tasksMap);
	const attempts = $derived(
		taskMap[task.id]?.subhistory.filter((attempt) => attempt.answered) || []
	);
</script>

<BottomModal className="max-w-3xl mx-auto" heading={task.title} bind:opened={showQuestions}>
	{#if task.part !== 2}
		<ul class="space-y-6 p-6">
			{#each questions as question, index}
				<li>{index + 1}. {question}</li>
			{/each}
		</ul>
	{:else}
		<div class="space-y-4 py-6">
			<h4 class="font-bold">{questions[0]}</h4>
			<p>{questions[1]}</p>
			<ul>
				{#each questions.slice(2, questions.length - 1) as question, index (question)}
					<li>{index + 1}{')'} {question}</li>
				{/each}
			</ul>
			<p class="font-bold">{questions[questions.length - 1]}</p>
		</div>
	{/if}
</BottomModal>

<aside class="pb-2 pt-4">
	<div class="space-y-2 px-6">
		<h3 class="text-h3 mb-2 font-semibold">{task.title}</h3>
		<p>Speaking part {part}</p>
		<p>{topic.title}</p>
	</div>
	<div class="flex space-x-2 px-4 py-2">
		<button
			onclick={() => (showQuestions = true)}
			class="border-whisper-500 block flex-1 space-y-2 rounded-lg border px-4 py-3 text-left hover:cursor-pointer"
		>
			<Questions size={24} />
			<p>Show questions</p>
		</button>
		<a
			href={`prepare`}
			class="border-whisper-500 block flex-1 space-y-2 rounded-lg border px-4 py-3 text-left"
		>
			<ArrowRefresh size={24} fill={`var(--color-${getPartColor(part)}-600)`} />
			<p>Retry</p>
		</a>
	</div>
</aside>

<main>
	<header class="px-4">
		<div class="border-whisper-100 flex space-x-4 border-b px-2 pb-3">
			<h3 class="border-whisper-500 text-lg font-semibold">Previous attempts</h3>
		</div>
	</header>

	<ul class="space-y-2 p-4">
		{#each attempts || [] as attempt (attempt.id)}
			<li>
				<AttemptCard {attempt} />
			</li>
		{/each}
	</ul>
</main>
