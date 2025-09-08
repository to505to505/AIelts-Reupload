<script lang="ts">
	import { goto } from '$app/navigation';
	import { pbInitPromise } from '$lib/config/pb';
	import { userProvider } from '$lib/providers/user/user.svelte';
	import { onMount } from 'svelte';

	const user = $derived(userProvider.user);
	const userLoading = $derived(userProvider.loading);

	onMount(async () => {
		await pbInitPromise;
		if (user && !userLoading) {
			goto('/home');
		} else {
			goto('/welcome');
		}
	});
</script>
