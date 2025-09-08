<script lang="ts">
	import { formatDateString } from '$lib/helpers/format-date-string';
	import { AttemptStatSchema } from '$lib/models/stat';
	import { z } from 'zod';

	let { attempt }: { attempt: z.infer<typeof AttemptStatSchema> } = $props();
</script>

<a href={`/attempts/${attempt.id}/result`} class="flex flex-col gap-y-4 rounded-lg bg-white p-4">
	<div class="flex justify-between">
		<div class="font-semibold">
			<p>Attempt: {attempt.id}</p>
			{#if !attempt.result}
				<div class="size-6 animate-spin rounded-full border-2 border-dashed border-amber-600"></div>
			{:else if attempt.result?.error}
				<span class="bg-danger rounded-full px-3 text-white">error :[</span>
			{/if}
		</div>
		<div class="w-fit">{formatDateString(attempt?.created)}</div>
	</div>

	<div class="flex justify-between">
		<span class="bg-whisper-100 rounded-full px-3">
			{#if attempt.singlePart}
				Single part
			{:else}
				Full Section
			{/if}
		</span>
		{#if !attempt.singlePart && attempt.result?.feedback}
			<span class="bg-whisper-100 rounded-full px-3">
				Band Score: {attempt.bandScore.toFixed(1)}
			</span>
		{/if}
	</div>
</a>
