<script lang="ts">
	import { z } from 'zod';
	import { calculateBandScore } from '$lib/helpers/calculate-band-score';
	import { ieltsToCeft } from '$lib/helpers/ielts-to-cefr';
	import FlashOn from '$lib/assets/icons/flashOn.svelte';
	import StaticProgressBar from '$lib/components/ui/staticProgressBar.svelte';
	import CheckCircleContained from '$lib/assets/icons/checkCircleContained.svelte';
	import Loader from '$lib/assets/icons/loader.svelte';
	import Questions from '$lib/assets/icons/questions.svelte';
	import Download from '$lib/assets/icons/download.svelte';
	import { mrg } from '$lib/helpers/mrg';
	import CloseCircleContained from '$lib/assets/icons/CloseCircleContained.svelte';
	import Pencil from '$lib/assets/icons/pencil.svelte';
	import ArrowRight from '$lib/assets/icons/arrow-right.svelte';
	import AudioPlayer from '$lib/components/ui/audioPlayer.svelte';
	import Button from '$lib/components/ui/button.svelte';
	import BottomModal from '$lib/components/ui/bottomModal.svelte';
	import { onMount } from 'svelte';
	import { AttemptSchema } from '$lib/models/attempt';
	import type { AttemptStatSchema } from '$lib/models/stat';
	import { parseQuestionsFromTask } from '$lib/helpers/parse-questions-from-task';
	import { gradeRound } from '$lib/helpers/grade-round';
	import { AnswerSchema } from '$lib/models/answer';
	import type { RecordModel } from 'pocketbase';
	import { pb, pbInitPromise } from '$lib/config/pb';
	import html2canvas from 'html2canvas-pro';

	let { attemptStat }: { attemptStat: z.infer<typeof AttemptStatSchema> } = $props();

	let questions: string[] = $state([]);
	let questionsOpened = $state(false);

	let urls: string[] = $state([]);

	let answers: z.infer<typeof AnswerSchema>[] = $state([]);

	const grammarScore = $derived(attemptStat.result!.feedback!.grammar.criterion.score);
	const coherenceScore = $derived(attemptStat.result!.feedback!.coherence.criterion.score);
	const lexicalScore = $derived(attemptStat.result!.feedback!.lexical.criterion.score);
	const grammarMistakes = $derived(attemptStat.result!.feedback!.grammar.mistakes);
	const grammarText = $derived(attemptStat.result!.feedback!.grammar.criterion.text);
	const lexicalText = $derived(attemptStat.result!.feedback!.lexical.criterion.text);
	const coherenceText = $derived(attemptStat.result!.feedback!.coherence.criterion.text);
	const lexicalMistakes = $derived(attemptStat.result!.feedback!.lexical.mistakes);
	const coherenceSpeedSec = $derived(attemptStat.result!.feedback!.coherence.speed);

	let tabState: number = $state(1);

	let grammarHidden = $state(grammarMistakes!.length > 2 ? true : false);
	let lexicalHidden = $state(lexicalMistakes!.length > 2 ? true : false);

	const bandScore = $derived(calculateBandScore(grammarScore, coherenceScore, lexicalScore));
	const cefrScore = $derived(ieltsToCeft(gradeRound(bandScore)));

	onMount(async () => {
		// ANSWERS
		await pbInitPromise;
		const attemptRecord = await pb
			.collection('attempts')
			.getOne(attemptStat.id, { expand: 'answers,answers.task' });
		const attempt = AttemptSchema.parse(attemptRecord);

		answers.push(...attempt.expand!.answers!);

		// PARSE QUESTIONS
		const tasks = answers.map((answer) => answer.expand!.task!);
		for (const task of tasks) {
			questions.push(...parseQuestionsFromTask(task));
		}

		// GET AUDIO URLS
		urls.push(
			...attemptRecord.expand!.answers.map((answer: RecordModel) =>
				pb.files.getURL(answer, answer!.audio!)
			)
		);
	});
</script>

<BottomModal bind:opened={questionsOpened} heading="Questions">
	<ol class="max-h-full list-inside list-decimal space-y-4 overflow-y-scroll p-6">
		{#each questions as question}
			<li class=" list-item flex-row items-center gap-2">
				{@html question}
			</li>
		{/each}
	</ol>
</BottomModal>

<h1 class="text-h3 pb-2 pl-6 pr-6 pt-4 font-semibold">Attempt #{attemptStat.id}</h1>
{#if !attemptStat.singlePart}
	<section class="m-4 rounded-xl bg-white pb-5 pl-4 pr-4 pt-4">
		<div class="flex flex-row items-start justify-between">
			<div class="">
				<p class="text-h2 font-semibold">{bandScore}</p>
				<p class="text-md">Band score</p>
			</div>
			<p class="bg-whisper-950 rounded-xl px-4 py-2 text-sm font-semibold text-white">
				{cefrScore}
			</p>
		</div>
		<div class="w-full space-y-4 py-4 pr-2">
			<StaticProgressBar title="Grammar" progress={grammarScore * 10} points={grammarScore}>
				{#snippet icon()}
					<CheckCircleContained />
				{/snippet}
			</StaticProgressBar>
			<StaticProgressBar
				title="Lexical resource"
				progress={lexicalScore * 10}
				points={lexicalScore}
			>
				{#snippet icon()}
					<Loader />
				{/snippet}
			</StaticProgressBar>
			<StaticProgressBar title="Coherence" progress={coherenceScore * 10} points={coherenceScore}>
				{#snippet icon()}
					<FlashOn />
				{/snippet}
			</StaticProgressBar>
		</div>
	</section>
{/if}
<section class="flex w-full flex-row gap-2 px-4 py-2">
	<button
		onclick={() => {
			questionsOpened = true;
		}}
		class="b-1 border-whisper-950 flex w-full flex-col items-start gap-2 rounded-md border-2 px-4 pb-3 pt-4"
	>
		<Questions />
		<p>Show questions</p>
	</button>

	<button
		onclick={() => {
			html2canvas(document.body).then((canvas) => {
				const link = document.createElement('a');
				link.download = `attempt-${attemptStat.id}.png`;
				link.href = canvas.toDataURL('image/png');
				link.click();
			});
		}}
		class="b-1 border-whisper-950 disabled:border-whisper-200 flex w-full flex-col items-start gap-2 rounded-md border-2 px-4 pb-3 pt-4 hover:cursor-pointer"
	>
		<Download />
		<p>Download results</p>
	</button>
</section>
<div class="flex flex-row gap-4 px-4 pb-2 pt-6">
	<button
		class={mrg('text-lg', tabState === 1 ? 'font-semibold' : 'font-regular')}
		onclick={() => (tabState = 1)}>Audio</button
	>
	<button
		class={mrg('text-lg', tabState === 2 ? 'font-semibold' : 'font-regular')}
		onclick={() => (tabState = 2)}
	>
		Transcript
	</button>
</div>

<section>
	{#if tabState === 1}
		<div class="flex flex-col gap-4 px-4 pb-2 pt-6">
			{#each urls as url}
				<AudioPlayer src={url} />
			{/each}
		</div>
	{:else if tabState === 2}
		<div class="mx-4 my-2 space-y-6 rounded-xl bg-white px-4 py-5">
			{#each answers as record, index}
				<div class="space-y-2">
					<h3 class="text-lg font-semibold">Part {index + 1}</h3>
					<p>
						{@html record.content}
					</p>
				</div>
			{/each}
		</div>
	{/if}
</section>
<section class="mx-4 mb-20 gap-5">
	<div class="border-whisper-100 my-6 flex flex-row justify-between border-b-2 px-2 pb-3">
		<h2 class="text-h3 flex flex-row items-center gap-2 font-semibold">
			<CheckCircleContained size={28} /> Grammar
		</h2>
		{#if !attemptStat.singlePart}
			<p class="text-h3 font-regular">{grammarScore.toFixed(1)}</p>
		{/if}
	</div>
	<div>
		<div class="prose">
			{@html grammarText}
		</div>
		<h3 class="pb-4 pt-5 text-2xl font-semibold">{grammarMistakes!.length} grammar mistakes</h3>
		<div class="space-y-2">
			{#each grammarMistakes! as grammarMistake, index}
				<article
					class="rounded-xl bg-white px-4 py-5"
					style:display={grammarHidden && index > 1 ? 'none' : 'block'}
				>
					<div class="mb-8 flex items-center justify-between">
						<div
							class="bg-whisper-950 flex max-w-min flex-row items-center gap-3 rounded-xl px-4 py-2"
						>
							<Pencil stroke={'var(--bg-white)'} />
							<span class="text-white"> Article </span>
						</div>
						<a href="https://ieltsliz.com/vocabulary/" class="flex items-center gap-2 underline"
							><span> Learn more </span>
							<ArrowRight />
						</a>
					</div>
					<div class="space-y-6">
						<div class="flex flex-row items-center gap-5">
							<CloseCircleContained />
							<p>...{grammarMistake.wrong}</p>
						</div>
						<div class="flex flex-row items-center gap-5">
							<CheckCircleContained
								stroke={'var(--color-mindaro-600)'}
								fill={'var(--color-mindaro-200)'}
							/>
							<p>...{grammarMistake.correct}</p>
						</div>
					</div>
				</article>
			{/each}
			{#if grammarHidden}
				<Button className="w-full" variant="outline" onclick={() => (grammarHidden = false)}>
					Show all
				</Button>
			{/if}
		</div>
	</div>
</section>
<section class="mx-4 mb-20 gap-5">
	<div class="border-whisper-100 my-6 flex flex-row justify-between border-b-2 px-2 pb-3">
		<h2 class="text-h3 flex flex-row items-center gap-2 font-semibold">
			<Loader size={28} /> Lexical Resources
		</h2>
		{#if !attemptStat.singlePart}
			<p class="text-h3 font-regular">{lexicalScore.toFixed(1)}</p>
		{/if}
	</div>
	<div>
		<div class="prose">{@html lexicalText}</div>

		<h3 class="pb-4 pt-5 text-2xl font-semibold">{lexicalMistakes!.length} lexical mistakes</h3>
		<div class="space-y-2">
			{#each lexicalMistakes! as lexicalMistake, index}
				<article
					style:display={lexicalHidden && index > 1 ? 'none' : 'block'}
					class="space-y-6 rounded-xl bg-white px-4 py-5"
				>
					<div class="space-y-4">
						<h4 class="bg-whisper-150 w-fit rounded-xl px-4 py-2">Original sentence</h4>
						<p>...{lexicalMistake!.wrong}</p>
					</div>
					<div class="space-y-4">
						<div class="flex items-center justify-between">
							<span
								class="bg-whisper-950 flex max-w-min flex-row items-center gap-3 rounded-xl px-4 py-2 text-white"
								>Rephrased
							</span>
							{#if !attemptStat.singlePart}
								<div class="hidden items-center gap-1 rounded-xl bg-white px-4 py-2">
									<span class="font-regular text-whisper-500 text-sm">{cefrScore}</span>
									<ArrowRight />
									<span class="text-sm">{cefrScore}</span>
								</div>
							{/if}
						</div>
						<p>
							...{lexicalMistake.correct}
						</p>
					</div>
				</article>
			{/each}
			{#if lexicalHidden}
				<Button className="w-full" variant="outline" onclick={() => (lexicalHidden = false)}
					>Show all
				</Button>
			{/if}
		</div>
	</div>
</section>
<section class="mx-4 mb-6 gap-5">
	<div class="border-whisper-100 my-6 flex flex-row justify-between border-b-2 px-2 pb-3">
		<h2 class="text-h3 flex flex-row items-center gap-2 font-semibold">
			<FlashOn size={28} /> Coherence
		</h2>
		{#if !attemptStat.singlePart}
			<p class="text-h3 font-regular">{coherenceScore.toFixed(1)}</p>
		{/if}
	</div>

	<div>
		<div class="prose mb-5">{@html coherenceText}</div>
		<div class="space-y-2">
			<article class="border-whisper-500 space-y-4 rounded-xl border-2 bg-white px-4 py-3">
				<h4 class="">Your speaking rate</h4>
				<div class="font-semibold">
					<p class="text-h3">{Math.round(coherenceSpeedSec * 60)}</p>
					<p class="text-sm">words per minute</p>
				</div>
			</article>
			<article class="space-y-4 rounded-xl bg-white px-4 py-3">
				<h4>Native speaker's rate</h4>
				<div class="font-semibold">
					<p class="text-h3">100-150</p>
					<p class="text-sm">words per minute</p>
				</div>
			</article>
		</div>
	</div>
</section>
