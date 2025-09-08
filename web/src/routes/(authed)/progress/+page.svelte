<script lang="ts">
	import CheckCircleContained from '$lib/assets/icons/checkCircleContained.svelte';
	import ChevronLeft from '$lib/assets/icons/chevronLeft.svelte';
	import FlashOn from '$lib/assets/icons/flashOn.svelte';
	import Loader from '$lib/assets/icons/loader.svelte';
	import AttemptCard from '$lib/components/widgets/AttemptCard.svelte';
	import { statProvider } from '$lib/providers/stat';
	import { Select } from 'bits-ui';

	const filters = [
		{ label: 'All', value: 'all' },
		{ label: 'Full Section', value: 'full' },
		{ label: 'Single Part', value: 'single' }
	];
	let selectedFilter = $state('full');
	let selectedFilterLabel = $derived(filters.find((f) => f.value === selectedFilter)?.label);

	const userHistory = $derived(statProvider.history || []);
	const userStat = $derived(statProvider.user);

	const filteredHistory = $derived(
		userHistory.filter((attempt) => {
			if (selectedFilter === 'all') return true;
			if (selectedFilter === 'full') return !attempt.singlePart;
			if (selectedFilter === 'single') return attempt.singlePart;
			return false;
		})
	);

	const userBandScore = $derived(
		(
			(userStat?.AverageGrammarScore! +
				userStat?.AverageLexicalScore! +
				userStat?.AverageCoherenceScore!) /
			3
		).toFixed(1)
	);

	const toLanguageLevel = (score: number) => {
		if (score <= 1) return 'A0';
		if (score <= 3) return 'A1';
		if (score <= 5) return 'A2';
		if (score <= 6) return 'B1';
		if (score <= 7) return 'B2';
		if (score <= 8) return 'C1';
		if (score <= 9) return 'C2';
		return '-';
	};
</script>

<main class="bg-bg-gray px-4 pt-4">
	<h1 class="text-h3 pb-2 font-semibold">Statistic</h1>
	<section class="rounded-lg bg-white p-4">
		<p class="text-h2 font-semibold">{toLanguageLevel(+userBandScore)}</p>
		<h2 class="mb-4">Speaking level</h2>
		<div
			class="border-whisper-500 text-md mb-2 flex items-center justify-between rounded-lg border p-4"
		>
			<p>Completed Attempts</p>
			<p class="text-h3 font-semibold">{userStat?.CompletedAttempts}</p>
		</div>
		<div
			class="border-whisper-500 text-md mb-4 flex items-center justify-between rounded-lg border p-4"
		>
			<p>Average band score</p>
			<p class="text-h3 font-semibold">
				{userBandScore}
			</p>
		</div>
		<ul class="space-y-4">
			<li class="flex justify-between">
				<div class="mr-3 mt-1">
					<CheckCircleContained />
				</div>
				<div class="flex-1 text-left">
					<p>Grammar</p>
					<div class="bg-whisper-100 h-[6px] rounded">
						<div
							class="bg-whisper-950 h-full rounded"
							style:width={`${(userStat?.AverageGrammarScore! / 9) * 100}%`}
						></div>
					</div>
				</div>
				<p>{userStat?.AverageGrammarScore.toFixed(1)}</p>
			</li>
			<li class="flex justify-between">
				<div class="mr-3 mt-1">
					<Loader />
				</div>
				<div class="flex-1 text-left">
					<p>Lexical resource</p>
					<div class="bg-whisper-100 h-[6px] rounded">
						<div
							class="bg-whisper-950 h-full rounded"
							style:width={`${(userStat?.AverageLexicalScore! / 9) * 100}%`}
						></div>
					</div>
				</div>
				<p>{userStat?.AverageLexicalScore.toFixed(1)}</p>
			</li>
			<li class="flex justify-between">
				<div class="mr-3 mt-1">
					<FlashOn />
				</div>
				<div class="flex-1 text-left">
					<p>Coherence</p>
					<div class="bg-whisper-100 h-[6px] rounded">
						<div
							class="bg-whisper-950 h-full rounded"
							style:width={`${(userStat?.AverageCoherenceScore! / 9) * 100}%`}
						></div>
					</div>
				</div>
				<p>{userStat?.AverageCoherenceScore.toFixed(1)}</p>
			</li>
		</ul>
	</section>
	<section>
		<h2 class="text-h3 px-4 py-6 pb-2 font-semibold">Previous Attempts</h2>

		<Select.Root value={selectedFilter} type="single" onValueChange={(v) => (selectedFilter = v)} items={filters}>
			<Select.Trigger
				class="border-whisper-500 mb-4 flex w-fit min-w-[150px] items-center justify-between rounded-lg border py-1 pl-4 pr-2"
			>
				<p>{selectedFilterLabel}</p>
				<div class="-rotate-90">
					<ChevronLeft fill={'var(--color-whisper-800)'} />
				</div>
			</Select.Trigger>

			<Select.Portal>
				<Select.Content class="rounded-lg bg-white">
					<Select.Viewport class="p-1">
						{#each filters as filter, i (i + filter.value)}
							<Select.Item
								class="rounded-button data-highlighted:bg-muted outline-hidden data-disabled:opacity-50 flex h-10 w-full select-none items-center py-3 pl-5 pr-1.5 text-sm  capitalize"
								value={filter.value}
								label={filter.label}
							>
								{#snippet children({ selected })}
									{filter.label}
									{#if selected}
										<div class="ml-auto -rotate-90">
											<ChevronLeft fill={'var(--color-whisper-800)'} />
										</div>
									{/if}
								{/snippet}
							</Select.Item>
						{/each}
					</Select.Viewport>
				</Select.Content>
			</Select.Portal>
		</Select.Root>

		<ul class="space-y-2 pb-8">
			{#each filteredHistory as attempt (attempt.id)}
				<li>
					<AttemptCard {attempt} />
				</li>
			{/each}
		</ul>
	</section>
</main>
