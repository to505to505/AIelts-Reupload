<script lang="ts">
	import ChevronLeft from '$lib/assets/icons/chevronLeft.svelte';
	import Close from '$lib/assets/icons/close.svelte';
	import { statProvider } from '$lib/providers/stat';
	import { slide } from 'svelte/transition';
	import { pb } from '$lib/config/pb';

	let open = $state(false);

	const userHistory = $derived(statProvider.history?.filter((a) => !a.result || !a.seen) || []);

	$effect(() => {
		if (userHistory.length === 0) {
			open = false;
		}
	});

	const markAttempt = (attemptId: string) => {
		return async () => {
			pb.collection('attempts').update(attemptId, { seen: true });
			open = false;
		};
	};

	const selectColor = () => {
		for (const attempt of userHistory) {
			if (attempt.result?.error) {
				return 'red';
			} else if (attempt.result?.feedback) {
				return 'green';
			}
		}

		if (userHistory.length > 0) {
			return 'amber';
		}
		return 'gray';
	};
</script>

<div class={['absolute -top-2 right-0', userHistory.length === 0 && 'hidden']}>
	<button
		style:border-color={`var(--color-${selectColor()}-600)`}
		style:color={`var(--color-${selectColor()}-600)`}
		class="flex size-10 w-fit items-center justify-center rounded-full border-2 pl-3 text-2xl hover:cursor-pointer"
		onclick={() => {
			if (userHistory.length === 0) return;
			open = !open;
		}}
	>
		<p>
			{userHistory.length}
		</p>
		{#if !open}
			<div class="-rotate-90">
				<ChevronLeft fill={`var(--color-${selectColor()}-600)`} />
			</div>
		{:else}
			<div>
				<Close fill={`var(--color-${selectColor()}-600)`} />
			</div>
		{/if}
	</button>
</div>

{#if open}
	<ul
		transition:slide
		class="z-99 absolute right-4 top-8 space-y-1 rounded border bg-white px-1 py-2"
	>
		{#each userHistory as attempt (attempt.id)}
			<li class="flex justify-between rounded-full">
				{#if !attempt.result}
					<a
						class="flex items-center gap-2 rounded bg-amber-400 py-1 pl-2 pr-1"
						href={`/attempts/${attempt.id}/result`}
					>
						<p>{attempt.id.slice(0, 5)}...</p>
						<div class="size-4 animate-spin rounded-full border-2 border-dashed"></div>
					</a>
				{:else if attempt.result.error}
					<a class="flex items-center gap-2" href={`/attempts/${attempt.id}/result`}>
						<p>{attempt.id.slice(0, 5)}...</p>
					</a>
					<button onclick={markAttempt(attempt.id)} class="hover:cursor-pointer">
						<Close size={24} fill="var(--color-whisper-800)" />
					</button>
				{:else if attempt.result.feedback}
					<a class="flex items-center gap-2" href={`/attempts/${attempt.id}/result`}>
						<p>{attempt.id.slice(0, 5)}...</p>
					</a>
					<button onclick={markAttempt(attempt.id)} class="hover:cursor-pointer">
						<Close size={24} fill="var(--color-whisper-800)" />
					</button>
				{/if}
			</li>
		{/each}
	</ul>
{/if}
