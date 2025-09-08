<script lang="ts">
	import { page } from '$app/state';
	import Feedback from './feedback.svelte';
	import { goto } from '$app/navigation';
	import { pb, pbInitPromise } from '$lib/config/pb';
	import { statProvider } from '$lib/providers/stat';
	import { onMount } from 'svelte';

	const attempt = $derived(statProvider.history?.find((a) => a.id === page.params.attemptId));

	$effect(() => {
		if (attempt?.result && !attempt.seen) {
			pb.collection('attempts').update(page.params.attemptId, { seen: true });
		}
	});

	onMount(async () => {
		await pbInitPromise;
		try {
			await pb.collection('attempts').getOne(page.params.attemptId);
		} catch (e) {
			console.error(e);
			goto('/home');
		}
	});
</script>

{#if !attempt}{:else if !attempt?.result}
	<div class="mx-auto w-fit space-y-6 px-8 py-4 text-center">
		<h3 class="text-h3 font-semibold">
			Your attempt is being analyzed by our algorithm right now.
		</h3>
		<p class="text-lg">
			You can safely leave this page, the attempt will appear in your /progress.
		</p>
		<div class="mx-auto size-16 animate-spin rounded-full border-2 border-dashed"></div>
	</div>
{:else if attempt?.result?.error}
	<p class="text-center text-xl">{attempt.result.error?.message}</p>
{:else if attempt?.result?.feedback}
	<Feedback attemptStat={attempt} />
{/if}
