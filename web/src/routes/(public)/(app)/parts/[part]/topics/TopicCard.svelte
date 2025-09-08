<script lang="ts">
	import z from 'zod';
	import { page } from '$app/state';

	import type { TopicSchema } from '$lib/models/topic';
	import { getPartColor } from '$lib/helpers/get-part-color';
	import Lock from '$lib/assets/icons/Lock.svelte';
	import { userProvider } from '$lib/providers/user/user.svelte';

	interface Props {
		topic: z.infer<typeof TopicSchema>;
	}

	let { topic }: Props = $props();

	const userSubscribed = $derived(userProvider.subscribed);

	let part = $derived(page.params.part);

	let locked = $derived(!userSubscribed && !topic?.free);
</script>

<a
	href={`/parts/${part}/topics/${topic.slug}/tasks`}
	class="relative flex min-h-[130px] flex-col rounded-lg bg-white p-4"
>
	<p class:opacity-40={locked} class="w-5/6 font-semibold">
		{topic.title}
	</p>
	<div
		style:color={`var(--color-${getPartColor(part)}-200)`}
		class={'absolute right-0 h-fit w-fit'}
	>
		{#if locked}
			<div class="absolute right-1/2 top-1/2 -translate-y-1/2 translate-x-1/2 z-10">
				<Lock fill={`var(--color-${getPartColor(part)}-600)`} />
			</div>
		{/if}
		<div class:opacity-40={locked}>
			{@html topic.icon}
		</div>
	</div>
</a>
