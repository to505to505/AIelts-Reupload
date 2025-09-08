<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';

	import Button from '$lib/components/ui/button.svelte';
	import { startAttemptByTask } from '$lib/features/start-attempt/start-task';
	import { userProvider } from '$lib/providers/user/user.svelte.js';
	import {
		initMediaRecorder,
		mediaRecorderProvider
	} from '$lib/providers/recorder/recorder.svelte.js';
	import { onMount } from 'svelte';

	let { data } = $props();

	const part = $derived(page.params.part);

	const user = $derived(userProvider.user);
	const recorder = $derived(mediaRecorderProvider.recorder);

	let startingAttempt = $state(false);

	const startAttempt = async () => {
		if (!recorder) {
			alert('Please allow access to your microphone');
			return;
		}

		if (!user?.verified) {
			goto('/email-confirm');
			return;
		}

		startingAttempt = true;

		try {
			const attempt = await startAttemptByTask(data.task.id);
			const firstTask = attempt.expand!.answers![0].expand!.task!;
			console.log(attempt);
			goto(`/attempts/${attempt.id}/record/${firstTask.slug}/${firstTask.part}`);
		} catch (error) {
			console.error(error);
		}
		startingAttempt = false;
	};

	onMount(() => {
		initMediaRecorder();
	});
</script>

<main class="flex-1 px-4 py-6">
	<div>
		<h3 class="text-h3 font-semibold">Task: {data.task.title}</h3>
		<p class="text-h3">Speaking part {part}</p>
		<p class="text-h3">{data.topic.title}</p>
	</div>
</main>

<footer>
	<p class="px-4 text-lg">
		Once you're prepared, hit the button to start the recording!The questions will show up right
		at the start
	</p>
	<div class="px-4 pb-12 pt-4">
		<Button disabled={startingAttempt} onclick={startAttempt} className="w-full text-white">
			Start task
		</Button>
	</div>
</footer>
