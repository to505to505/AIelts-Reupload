<script lang="ts">
	import { goto } from '$app/navigation';
	import { pb } from '$lib/config/pb';
	import { userProvider } from '$lib/providers/user/user.svelte';
	import { onMount } from 'svelte';

	const user = $derived(userProvider.user);

	let wait = $state(false);

	$effect(() => {
		if (user?.verified) {
			goto('/home');
		}
	});

	const setWaitInterval = () => {
		let waitInterval = setTimeout(() => {
			wait = false;
			clearInterval(waitInterval);
		}, 1000);
	};

	onMount(() => {
		if (user?.verified) {
			goto('/home');
		}
	});
</script>

{#if !user?.verified}
	<section class="space-y-6 px-6 pt-20">
		<h1 class="text-h2 line-clamp-2 max-w-[350px] font-semibold">Let’s confirm you email</h1>
		<div>
			<p class="mb-2">
				Please, check your inbox and click the link we sent on email below to activate your account
			</p>
			<p class="font-semibold">{user?.email}</p>
		</div>
		<p class="pt-6 text-center">
			<button
				class="disabled:opacity-50"
				disabled={wait}
				onclick={() => {
					if (!user?.email || wait) return;
					wait = true;
					setWaitInterval();
					pb.collection('users').requestVerification(user.email);
				}}
			>
				Didn't receive the link? <span class="ml-1 font-semibold underline">Resend it</span>
			</button>
		</p>
	</section>
{:else}
	<section class="space-y-6 px-6">
		<h1 class="text-h2 line-clamp-2 max-w-[250px] font-semibold">Already confirmed!</h1>
		<p class="font-semibold">{user?.email}</p>
		<p class="pt-6 text-center">
			<a href="/">
				<span class="ml-1 font-semibold underline">Go to application</span>
			</a>
		</p>
	</section>
{/if}
