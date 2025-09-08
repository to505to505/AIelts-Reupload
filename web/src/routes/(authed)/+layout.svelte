<script lang="ts">
	import { goto } from '$app/navigation';
	import App from '$lib/components/layouts/App.svelte';
	import { pbInitPromise } from '$lib/config/pb';
	import { userProvider } from '$lib/providers/user/user.svelte';
	import { onMount } from 'svelte';

	let { children } = $props();

	const user = $derived(userProvider.user);
	const loadingUser = $derived(userProvider.loading);

	onMount(async () => {
		await pbInitPromise;
		if (!user && !loadingUser) {
			goto('/sign-in');
		}
	});
</script>

<App>
	{@render children()}
</App>
