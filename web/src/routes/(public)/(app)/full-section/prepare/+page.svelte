<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/button.svelte';
	import { pickRandomFullSection } from '$lib/features/start-attempt/pick-random-set';
	import { userProvider } from '$lib/providers/user/user.svelte';
	import {
		initMediaRecorder,
		mediaRecorderProvider
	} from '$lib/providers/recorder/recorder.svelte';
	import { onMount } from 'svelte';

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
		const attempt = await pickRandomFullSection();
		attempt.expand?.answers?.sort((a, b) => a.expand!.task!.part - b.expand!.task!.part);
		startingAttempt = false;
		goto(`/attempts/${attempt.id}/record/${attempt.expand!.answers![0].expand!.task!.slug}/1`);
	};

	onMount(() => {
		initMediaRecorder();
		// return () => {
		// 	mediaRecorderProvider.clearAll();
		// };
	});
</script>

<main class="flex flex-1 flex-col justify-between px-4 py-4">
	<div>
		<h3 class="text-h3 mb-4 font-semibold">Speaking Full Test (Part 1, Part 2, Part 3)</h3>
		<ul class="space-y-2 pl-4 pr-8">
			<li class="text-md list-disc">You’re about to do a complete IELTS Speaking Test.</li>
			<li class="list-disc">It consists of 3 parts that go one after another.</li>
			<li class="list-disc">
				After that, the model will take some time to assess your skills and give you feedback and a
				grade for the speaking test!
			</li>
		</ul>
	</div>

	<p class="text-lg">
		Once you're prepared, hit the button to start the recording!The questions will show up right
		at the start
	</p>
</main>

<footer class="px-4 pb-10 pt-4">
	<Button disabled={startingAttempt} onclick={startAttempt} className="w-full text-white">
		Start Random Test
	</Button>
</footer>
