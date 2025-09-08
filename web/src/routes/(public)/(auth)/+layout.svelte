<script lang="ts">
	import { goto } from '$app/navigation';
	import Logo from '$lib/assets/icons/Logo.svelte';
	import { userProvider } from '$lib/providers/user/user.svelte';

	let { children } = $props();

	const user = $derived(userProvider.user);

	$effect(() => {
		if (user) goto('/home');
	});
</script>

<header class="flex items-center justify-between px-4 py-6">
	<a href="/welcome"><Logo /></a>
</header>

<div class="mx-auto max-w-2xl">
	{@render children()}
</div>
