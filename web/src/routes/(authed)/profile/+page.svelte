<script lang="ts">
	import { type Component } from 'svelte';

	import UserProfile from '$lib/assets/icons/userProfile.svelte';
	import Email from '$lib/assets/icons/Email.svelte';
	import EyeClosed from '$lib/assets/icons/eyeClosed.svelte';
	import EyeOpen from '$lib/assets/icons/eyeOpen.svelte';
	import Account from '$lib/assets/icons/account.svelte';
	import Pencil from '$lib/assets/icons/pencil.svelte';
	import ChevronRight from '$lib/assets/icons/chevronRight.svelte';

	import Input from '$lib/components/ui/input.svelte';
	import Button from '$lib/components/ui/button.svelte';
	import ButtonLikeLink from '$lib/components/ui/button-like-link.svelte';
	import { goto } from '$app/navigation';
	import { unsubscribeUser, userProvider } from '$lib/providers/user/user.svelte';
	import { pb } from '$lib/config/pb';
	import { unsubscribeHistory } from '$lib/providers/stat';
	import { signOut } from '$lib/features/auth/sign-out';

	const user = $derived(userProvider.user);

	const settingsFields = $derived([
		{ heading: 'name', data: user?.name || '<Noname>' },
		{ heading: 'email', data: user?.email },
		{ heading: 'password' }
	]);

	const formIcons: Component[] = [UserProfile, Email];

	let inputsArray: HTMLDivElement[] = $state([]);

	let isPasswordVisible = $state(false);
	let isFormBeingEdited = $state(false);

	const editProfile = async () => {
		if (!pb.authStore.isValid) return;

		const formValues = inputsArray.map((div) => div.querySelector('input')!.value);
		const newValuse: { name?: string; email?: string; password?: string } = {};

		if (user?.name !== formValues[0]) newValuse['name'] = formValues[0];
		// if (user?.email !== formValues[1]) newValuse['email'] = formValues[1];
		// if (formValues[2]) newValuse['password'] = formValues[2];

		await pb.collection('users').update(pb.authStore.record!.id, newValuse);
		isFormBeingEdited = false;
	};
</script>

<section class="flex flex-row items-end gap-4 pb-4 pl-6 pr-4 pt-4">
	<Account height={80} width={80} />
	<div class="flex flex-col">
		<h1 class="text-h3 font-semibold">{user?.name || `id: ${user?.id.slice(0, 5)}`}</h1>
		<p class="text-md font-regular text-whisper-800">{user?.email}</p>
	</div>
</section>
<section>
	<h2 class="pb-2 pl-6 pr-4 pt-4 text-lg font-semibold">Account</h2>
	<form
		onsubmit={async (e: Event) => {
			e.preventDefault();
			await editProfile();
		}}
		class="mx-4 my-2 flex flex-col gap-4 rounded-md bg-white px-4 py-2"
	>
		{#each settingsFields as field, index}
			{#if isFormBeingEdited}
				<div class="w-full" bind:this={inputsArray[index]}>
					<Input
						variant="solid"
						type={field.heading === 'password' ? (isPasswordVisible ? 'text' : 'password') : 'text'}
						name={field.heading}
						isError={false}
						placeholder={field.heading}
						value={field.data}
					>
						{#snippet icon(isError: boolean, focus: boolean)}
							{#if field.heading === 'password'}
								<button
									class="flex items-center"
									onclick={(event) => {
										event.preventDefault();
										isPasswordVisible = !isPasswordVisible;
									}}
									type="button"
									>{#if !isPasswordVisible}
										<EyeClosed
											fill={isError
												? 'var(--danger)'
												: focus
													? 'var(--color-whisper-700)'
													: 'var(--color-whisper-500)'}
										/>
									{:else}
										<EyeOpen
											fill={isError
												? 'var(--danger)'
												: focus
													? 'var(--color-whisper-700)'
													: 'var(--color-whisper-500)'}
										/>
									{/if}
								</button>
							{:else}
								{@const AnotherIcon = formIcons[index]}
								<AnotherIcon
									fill={isError
										? 'var(--danger)'
										: focus
											? 'var(--color-whisper-700)'
											: 'var(--color-whisper-500)'}
								/>
							{/if}
						{/snippet}
						{#snippet error()}
							<p class="text-danger px-2 text-sm font-semibold">hiuguigui</p>
						{/snippet}
					</Input>
				</div>
			{:else}
				<div class="flex flex-row items-center justify-between">
					<div>
						<h3 class="text-whisper-800 capitalize">
							{field.heading}
						</h3>
						<p class="text-whisper-950 font-semibold">
							{field.data ?? '***********'}
						</p>
					</div>
					<button
						onclick={() => {
							isFormBeingEdited = true;
						}}
					>
						<Pencil size={20} />
					</button>
				</div>
			{/if}
		{/each}
		{#if isFormBeingEdited}
			<Button type="submit" className={'w-1/2 self-center text-white'}>Edit profile</Button>
		{/if}
	</form>
</section>
<section>
	<h2 class="pb-2 pl-6 pr-4 pt-4 text-lg font-semibold">Subscription</h2>
	<div class="flex flex-col gap-2 px-4 py-2">
		{#if !user?.expired || new Date(user?.expired) > new Date()}
			<a
				href="/subscription"
				class="bg-whisper-950 flex w-full flex-row items-center justify-between rounded-md p-4 text-white"
			>
				<span class="text-md font-semibold"> Get aiELTS Pro </span>
				<ChevronRight stroke={'var(--bg-white)'} />
			</a>
		{:else}
			<ButtonLikeLink caption={'Manage Subscription'} href={'/subscription'} />
			<ButtonLikeLink classNames="hidden" caption={'Change pay methods'} href={'/payment'} />
		{/if}
	</div>
</section>
<section>
	<h2 class="pb-2 pl-6 pr-4 pt-4 text-lg font-semibold">Help & Support</h2>
	<div class="flex flex-col gap-2 px-4 py-2">
		<ButtonLikeLink classNames="hidden" caption={'FAQ'} href={'/welcome#faq'} />
		<ButtonLikeLink caption={'Help Center'} href={'https://t.me/aielts_help'} newTab />
		<ButtonLikeLink caption={'Send feedback'} href={'https://forms.gle/5LqFjvCMUyQFVYHWA'} newTab />
	</div>
</section>
<section>
	<h2 class="pb-2 pl-6 pr-4 pt-4 text-lg font-semibold">About aiELTS</h2>
	<div class="flex flex-col gap-2 px-4 py-2">
		<ButtonLikeLink classNames="hidden" caption={'Terms & Conditions'} href={'/terms'} />
		<ButtonLikeLink caption={'Privacy Policy'} href={'/terms'} />
	</div>
</section>
<section class="px-4 py-6">
	<Button
		onclick={async () => {
			await signOut();
			goto('/sign-in');
		}}
		className="w-full bg-transparent border-2 border-rapture-600 text-rapture-600 hover:bg-rapture-600 hover:text-white rounded-tiny"
	>
		Log Out
	</Button>
</section>
