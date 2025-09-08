<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import Account from '$lib/assets/icons/account.svelte';
	import ChevronLeft from '$lib/assets/icons/chevronLeft.svelte';
	import Close from '$lib/assets/icons/close.svelte';
	import BottomModal from '$lib/components/ui/bottomModal.svelte';
	import Button from '$lib/components/ui/button.svelte';
	import { pb } from '$lib/config/pb';
	import { getPartColor } from '$lib/helpers/get-part-color';
	import { activeAttemptProvider } from '$lib/providers/active-attempt/active-attempt.svelte';
	import { appLayoutProvider } from '$lib/providers/app-layout/app-layout.svelte';
	import { userProvider } from '$lib/providers/user/user.svelte';
	import AttemptNotifications from '../widgets/AttemptNotifications.svelte';

	let { children } = $props();

	const part = $derived(page.params.part);
	const fullSectionPrepare = $derived(page.url.pathname.endsWith('/full-section/prepare'));

	const appLayout = $derived(appLayoutProvider);
	const user = $derived(userProvider.user);

	const activeAttempt = $derived(activeAttemptProvider.attempt);
</script>

<div
	style:background-color={appLayout.type === 'prepare'
		? fullSectionPrepare
			? `var(--color-whisper-150)`
			: `var(--color-${getPartColor(part)}-200)`
		: 'var(--color-gray)'}
	class={[
		' border-whisper-150 relative mx-auto min-h-screen max-w-3xl border-x',
		(appLayout.type === 'prepare' || appLayout.type === 'record') && 'flex flex-col'
	]}
>
	{#if appLayout.type !== 'prepare'}
		<div class="absolute right-2 top-4">
			<AttemptNotifications />
		</div>
	{/if}

	{#if appLayout.type === 'home'}
		<header class="border-whisper-150 border-b p-4">
			<a class="flex items-center" href="/profile">
				<Account />
				{#if user?.name}
					<p class="ml-4 text-lg">Hi, {user.name}</p>
				{:else}
					<p class="ml-4 text-lg">Hi! You will crack IELTs!</p>
				{/if}
			</a>
		</header>
	{:else if appLayout.type === 'default'}
		<header
			class="border-whisper-150 bg-gray top-0 z-10 flex w-full max-w-3xl items-center border-b p-4"
		>
			{#if page.url.pathname === '/email-confirm'}
				<button class="absolute hover:cursor-pointer" onclick={() => goto('/home')}>
					<ChevronLeft fill={'var(--color-whisper-950)'} />
				</button>
			{:else}
				<button class="absolute hover:cursor-pointer" onclick={() => history.back()}>
					<ChevronLeft fill={'var(--color-whisper-950)'} />
				</button>
			{/if}
			<p class="mx-auto">{appLayout.title}</p>
		</header>
	{:else if appLayout.type === 'prepare'}
		<header class="flex justify-end p-4">
			<button class="hover:cursor-pointer" onclick={() => history.back()}>
				<Close fill="var(--color-whisper-950)" />
			</button>
		</header>
	{:else if appLayout.type === 'record'}
		<header
			class="border-whisper-150 bg-gray top-0 z-10 flex w-full max-w-3xl items-center border-b p-4"
		>
			<button
				class="absolute hover:cursor-pointer"
				onclick={() => {
					activeAttemptProvider.switchAbort(true);
				}}
			>
				<Close fill="var(--color-whisper-950)" />
			</button>
			<p class="mx-auto">{appLayout.title}</p>
		</header>
	{/if}

	{@render children()}
</div>

<!-- ABORT BOTTOM MODAL -->
{#if appLayout.type === 'record'}
	<BottomModal
		className="text-center h-1/2"
		heading="Once you leave the test, your responses will be discarded"
		opened={activeAttemptProvider?.aborting || false}
	>
		<div class="space-y-2 text-center">
			<p class="mb-6 px-6">Once you leave the test, your responses will be discarded</p>

			<div class="mx-4 flex flex-col gap-4">
				<Button
					className="text-white"
					onclick={async () => {
						if (!activeAttempt) return;

						activeAttempt.answers.map((answerId) => {
							pb.collection('answers').delete(answerId, { requestKey: answerId });
						});

						activeAttemptProvider.setAttempt(null);
						activeAttemptProvider.switchAbort(false);
						goto('/home');
					}}
				>
					Exit attempt
				</Button>
				<Button
					onclick={() => {
						activeAttemptProvider.switchAbort(false);
					}}
					variant="outline"
				>
					Continue
				</Button>
			</div>
		</div>
	</BottomModal>
{/if}
