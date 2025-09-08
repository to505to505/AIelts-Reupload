<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';

	import Book from '$lib/assets/icons/book.svelte';
	import Shuffle from '$lib/assets/icons/shuffle.svelte';
	import { getPartColor } from '$lib/helpers/get-part-color.js';
	import Lock from '$lib/assets/icons/Lock.svelte';
	import { statProvider } from '$lib/providers/stat/stat.svelte.js';
	import { userProvider } from '$lib/providers/user/user.svelte.js';
	import { Tabs } from 'bits-ui';

	const part = $derived(page.params.part);

	let { data } = $props();

	const tasksMap = $derived(statProvider.tasksMap);

	const completedTaskIDs = $derived(
		new Set(
			Object.entries(tasksMap ?? {})
				.filter(([_, task]) => {
					return task.subhistory.some((attempt) => attempt.answered);
				})
				.map(([taskID]) => taskID)
		)
	);

	const user = $derived(userProvider.user);
	const userSubscribed = $derived(userProvider.subscribed);

	const todoTasks = $derived(
		data.tasks
			.filter((task) => !completedTaskIDs.has(task.id))
			.sort((a, b) => Number(b.free) - Number(a.free))
	);

	const completedTasks = $derived(data.tasks.filter((task) => completedTaskIDs.has(task.id)));

	const filters = [
		{
			value: 'recent',
			label: 'Recent tries'
		}
	];

	let filterValue = $state<string>('');
	const selectedFilterLabel = $derived(
		filterValue ? filters.find((f) => f.value === filterValue)?.label : 'Select a theme'
	);

	const pickRandomTask = () => {
		const randomIndex = Math.floor(Math.random() * data.tasks.length);
		goto(`tasks/${data.tasks[randomIndex].slug}/prepare`);
	};
</script>

<aside class="pb-2 pt-4">
	<div class="px-6">
		<h3 class="text-h3 mb-2 font-semibold">{data.topic.title}</h3>
		<p>{completedTasks.length}/{completedTasks.length + todoTasks.length}</p>
	</div>
	<div class="flex space-x-2 px-4 py-2">
		<a href="essentials" class="border-whisper-500 flex-1 space-y-2 rounded-lg border px-4 py-3">
			<Book />
			<p>Useful vocabulary</p>
		</a>
		<button
			class:opacity-40={!userSubscribed}
			disabled={!userSubscribed}
			onclick={pickRandomTask}
			class="border-whisper-500 relative flex-1 space-y-2 rounded-lg border px-4 py-3 text-left hover:cursor-pointer"
		>
			<Shuffle fill={`var(--color-${getPartColor(part)}-600)`} />
			<p>Random task</p>
			{#if !userSubscribed}
				<div class="top-2/5 absolute right-6 h-fit w-fit">
					<Lock fill={`var(--color-${getPartColor(part)}-600)`} />
				</div>
			{/if}
		</button>
	</div>
</aside>

<main class="">
	<Tabs.Root value="todo">
		<Tabs.List>
			<header class="px-4">
				<div class="border-whisper-100 flex space-x-4 border-b px-2 pb-3">
					<Tabs.Trigger
						value="todo"
						class="border-whisper-500 text-lg font-semibold transition data-[state=active]:border-b"
					>
						To do
					</Tabs.Trigger>

					<Tabs.Trigger
						value="completed"
						class="border-whisper-500 text-lg font-semibold transition data-[state=active]:border-b"
					>
						Completed
					</Tabs.Trigger>
				</div>
			</header>
		</Tabs.List>

		<Tabs.Content value="todo">
			<ul class="space-y-2 p-4">
				{#each todoTasks as task (task.id)}
					<a
						href={userSubscribed || (user?.verified && task.free)
							? `tasks/${task.slug}/prepare`
							: user?.verified
								? '/subscription'
								: '/email-confirm'}
						class="border-whisper-150 relative block space-y-2 rounded-lg border bg-white p-4"
					>
						{#if !userSubscribed && !task.free}
							<div class="absolute right-6 h-fit w-fit">
								<Lock fill={`var(--color-${getPartColor(part)}-600)`} />
							</div>
						{/if}
						<h5 class:opacity-40={!userSubscribed && !task.free} class="font-semibold">
							{task.title}
						</h5>
					</a>
				{/each}
			</ul>
		</Tabs.Content>

		<Tabs.Content class="px-4" value="completed">
			<ul class="space-y-2 py-2">
				{#each completedTasks as task (task.id)}
					<a href={`tasks/${task.slug}/completed`} class="block space-y-2 rounded-lg bg-white p-4">
						<header class="text-whisper-800 flex justify-between space-x-2">
							<h5 class="font-semibold">{task.title}</h5>
							<p class="text-sm">
								last try: <span class="font-semibold">29.10.2024</span> 15:47
							</p>
						</header>
						<footer class="flex justify-end gap-x-1">
							<div class="bg-whisper-150 rounded-lg px-4 py-1">
								Tries {tasksMap[task.id!]?.subhistory.length}
							</div>
							<div
								style:background-color={`var(--color-${getPartColor(part)}-200)`}
								class="hidden rounded-lg px-4 py-1"
							>
								Max Score: {tasksMap[task.id!]?.maxBandScore.toFixed(1)}
							</div>
						</footer>
					</a>
				{/each}
			</ul>
		</Tabs.Content>
	</Tabs.Root>
</main>
