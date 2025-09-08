<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { PUBLIC_GEN_URL } from '$env/static/public';
	import Stopwatch from '$lib/assets/icons/stopwatch.svelte';
	import Waveform from '$lib/assets/icons/waveform.svelte';
	import Button from '$lib/components/ui/button.svelte';
	import { pb } from '$lib/config/pb';
	import { getPartColor } from '$lib/helpers/get-part-color';
	import { AttemptSchema } from '$lib/models/attempt';
	import { TaskSchema } from '$lib/models/task';
	import { activeAttemptProvider } from '$lib/providers/active-attempt/active-attempt.svelte';
	import { mediaRecorderProvider } from '$lib/providers/recorder/recorder.svelte';
	import { onMount } from 'svelte';
	import { Tween } from 'svelte/motion';

	const attempt = $derived(activeAttemptProvider.attempt);
	const tasks = $derived(
		attempt?.expand?.answers?.map((answer) => TaskSchema.parse(answer.expand?.task)) || []
	);
	const currentTask = $derived(tasks.find((task) => task.part === Number(page.params.part)));

	let maxRecordingSeconds = $derived(currentTask?.part === 2 ? 120 : 180);
	let maxPrepareSeconds = $derived(currentTask?.part === 2 ? 60 : 3);

	let questions: string[] = $state([]);
	let questionIndex = $state(0);
	let questionOffsets = $state([0]);

	const lastQuestion = $derived(questionIndex === questions.length - 1);
	const lastTask = $derived(currentTask?.id === tasks[tasks.length - 1]?.id);

	const recorder = $derived(mediaRecorderProvider.recorder);
	const recording = $derived(mediaRecorderProvider.recording);

	let prepareSeconds = $state(0);
	let recording100MSeconds = $state(0);

	const onStartRecording = () => {
		recorder?.start();
	};

	const onStopRecording = () => {
		recorder?.stop();
		questionIndex = 0;
		prepareSeconds = 0;
		recording100MSeconds = 0;
	};

	const progressValuePercentage = new Tween(0);
	$effect(() => {
		if (recording) {
			progressValuePercentage.target = (recording100MSeconds / (maxRecordingSeconds * 10)) * 100;
		} else {
			progressValuePercentage.target = 100 - (prepareSeconds / maxPrepareSeconds) * 100;
		}
	});

	$effect(() => {
		if (currentTask?.part === 2) {
			questions = [currentTask.questions];
		} else if (currentTask && currentTask?.part !== 2) {
			const parser = new DOMParser();
			const doc = parser.parseFromString(currentTask.questions, 'text/html');
			questions = Array.from(doc.querySelectorAll('li')).map((li) => li.textContent!.trim());
		}
	});

	onMount(() => {
		// PREPARE INTERVAL
		let prepareInterval = setInterval(() => {
			if (recording) return;
			prepareSeconds++;
			if (prepareSeconds >= maxPrepareSeconds) {
				onStartRecording();
			}
		}, 1000);

		// RECORDING INTERVAL
		let recordingInterval = setInterval(() => {
			if (!recording) return;
			recording100MSeconds++;
			if (recording100MSeconds >= maxRecordingSeconds * 10) {
				onStopRecording();
			}
		}, 100);

		// CALLBACK FOR MEDIA RECORDER
		mediaRecorderProvider.setProcessAudio(async (audioFile: File) => {
			const attempt = AttemptSchema.parse(
				await pb
					.collection('attempts')
					.getOne(page.params.attemptId, { expand: 'answers,answers.task' })
			);
			attempt.expand?.answers?.sort((a, b) => a.expand!.task!.part - b.expand!.task!.part);
			const answer = attempt.expand!.answers!.find(
				(answer) => answer.expand?.task?.slug === page.params.taskSlug
			)!;
			const tasks = attempt.expand!.answers!.map((answer) => TaskSchema.parse(answer.expand!.task));
			const task = tasks.find((task) => task.id === answer.task)!;

			const nextTask = tasks.find((t) => t.part === task.part + 1);

			(async () => {
				await pb.collection('answers').update(answer.id, {
					audio: audioFile,
					questionOffsets
				});
				questionOffsets = [0];

				fetch(`${PUBLIC_GEN_URL}/api/audio/${answer.id}/transcribe?attempt_id=${attempt.id}`, {
					method: 'POST'
				});
			})();

			if (attempt.expand?.answers?.filter((a) => a.audio).length === tasks.length - 1) {
				pb.collection('attempts').update(attempt.id, { answered: new Date() });
				goto(`/attempts/${attempt.id}/result`, { replaceState: true });
			} else {
				goto(`/attempts/${attempt.id}/record/${nextTask?.slug}/${nextTask?.part}`, {
					replaceState: true
				});
			}
		});

		return () => {
			if (prepareInterval) clearInterval(prepareInterval);
			if (recordingInterval) clearInterval(recordingInterval);
			recorder?.stream.getTracks().forEach((track) => track.stop());
			// mediaRecorderProvider.clearAll();
		};
	});
</script>

<main class="flex-1 pt-4">
	{#if currentTask?.part !== 2}
		<ul class="flex gap-x-2 px-4 pb-4">
			{#each Array.from({ length: questions.length }, (_, index) => index) as index}
				<li
					class="border-whisper-200 flex size-8 items-center justify-center rounded-full"
					style:background-color={index === questionIndex
						? `var(--color-${getPartColor(String(currentTask?.part) || '1')}-200)`
						: ''}
					class:border={index !== questionIndex}
				>
					{index + 1}
				</li>
			{/each}
		</ul>
	{:else if currentTask?.part === 2}
		<div class="pl-2 text-lg font-semibold">
			{#if recording}
				<p
					class="border-whisper-500 text-whisper-500 w-fit rounded-lg border px-4 py-1 text-center"
				>
					Time to prepare is over
				</p>
			{:else}
				<p
					class="border-mindaro-600 text-mindaro-600 bordertext-center w-fit rounded-lg border px-4 py-1"
				>
					You have 1 minute to prepare
				</p>
			{/if}
		</div>
	{/if}
	<p class="text-whisper-800 mt-2 text-center text-sm">
		You have {maxRecordingSeconds / 60} minutes maximum to complete the whole part!
	</p>
	<div class="flex h-6 items-center px-6">
		<div class="bg-whisper-100 relative mr-4 h-[6px] flex-1 rounded-xl">
			<div
				style:background-color={`var(--color-${getPartColor(String(currentTask?.part) || '1')}-600)`}
				style:width={`${progressValuePercentage.current}%`}
				class="absolute left-0 top-0 h-full rounded-xl"
			></div>
		</div>
		<div class="mr-[0.45rem]"><Stopwatch fill={'var(--color-whisper-950)'} /></div>
		<div>
			{#if recording}
				{Math.floor(Math.round(recording100MSeconds / 10) / 60) < 10 ? 0 : ''}
				{Math.floor(Math.round(recording100MSeconds / 10) / 60)}
				:
				{Math.floor(Math.round(recording100MSeconds / 10) % 60) < 10 ? 0 : ''}
				{Math.floor(Math.round(recording100MSeconds / 10) % 60)}
			{:else}
				{Math.floor((maxPrepareSeconds - prepareSeconds) / 60) < 10 ? 0 : ''}
				{Math.floor((maxPrepareSeconds - prepareSeconds) / 60)}
				:
				{Math.floor((maxPrepareSeconds - prepareSeconds) % 60) < 10 ? 0 : ''}
				{Math.floor((maxPrepareSeconds - prepareSeconds) % 60)}
			{/if}
		</div>
	</div>

	<section class="flex-1 px-4 py-6">
		{#if currentTask?.part !== 2}
			<div class="flex h-full items-center justify-center pt-36">
				<p class="justify-self-center text-center text-2xl">
					{questions[questionIndex]}
				</p>
			</div>
		{:else}
			<div class="prose text-whisper-950 px-8 text-lg">
				{@html questions[0]}
			</div>
		{/if}
	</section>
</main>

<footer class="mt-auto px-4 pb-12 pt-4 *:w-full">
	<div class="flex items-center justify-center">
		<Waveform height={50} fill={'var(--whisper-200)'} />
	</div>
	{#if lastQuestion && lastTask && recording}
		<Button
			className="text-white"
			disabled={!recording}
			onclick={() => {
				onStopRecording();
			}}
		>
			Finish
		</Button>
	{:else if !recording && currentTask?.part === 2}
		<Button
			className="text-white"
			onclick={() => {
				onStartRecording();
			}}
		>
			Start immediately
		</Button>
	{:else if lastQuestion}
		<Button
			className="text-white"
			onclick={() => {
				onStopRecording();
			}}
		>
			Next task
		</Button>
	{:else}
		<Button
			disabled={!recording}
			className={[
				'text-white',
				currentTask?.part === 1
					? 'bg-chimera-600'
					: currentTask?.part === 2
						? 'bg-mindaro-600'
						: 'bg-rapture-600'
			]}
			onclick={() => {
				questionOffsets.push(recording100MSeconds / 10);
				questionIndex++;
			}}
		>
			Next question
		</Button>
	{/if}
</footer>
