<script lang="ts">
	import { onMount } from 'svelte';
	import { onNavigate } from '$app/navigation';

	import { subscribeHistory, unsubscribeHistory } from '$lib/providers/stat';
	import { subscribeUser, unsubscribeUser } from '$lib/providers/user/user.svelte';

	import '../app.css';
	import ViewTransitions from '$lib/components/ui/ViewTransitions.svelte';

	let { children } = $props();

	onMount(() => {
		subscribeUser();
		subscribeHistory();

		return () => {
			unsubscribeUser();
			unsubscribeHistory();
		};
	});

	onNavigate((navigation) => {
		if (!document.startViewTransition) return;

		return new Promise((resolve) => {
			document.startViewTransition(async () => {
				resolve();
				await navigation.complete;
			});
		});
	});
</script>

<div class="mx-auto max-w-[1280px]">
	{@render children()}
</div>

<ViewTransitions />
