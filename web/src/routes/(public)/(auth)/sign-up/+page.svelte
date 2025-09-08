<script lang="ts">
	import { ClientResponseError } from 'pocketbase';
	import { goto } from '$app/navigation';

	import Button from '$lib/components/ui/button.svelte';
	import Input from '$lib/components/ui/input.svelte';
	import Email from '$lib/assets/icons/Email.svelte';
	import EyeOpen from '$lib/assets/icons/eyeOpen.svelte';
	import EyeClosed from '$lib/assets/icons/eyeClosed.svelte';
	import { pb } from '$lib/config/pb';
	import { signIn } from '$lib/features/auth/sign-in';

	interface AuthError {
		message: string;
		email: string;
		password: string;
	}

	let formError: AuthError | null = $state(null);

	let email = $state('');
	let password = $state('');
	let isPasswordVisible = $state(false);
	let agree = $state(false);

	const oauth2 = async () => {
		formError = null;
		const userResult = await pb.collection('users').authWithOAuth2({ provider: 'yandex' });
		if (!userResult) {
			return;
		}
		const userRecord = userResult.record;
		await pb.collection('users').update(userRecord.id, {
			credits: 0
		});

		goto('/home');
	};

	const signup = async (e: Event) => {
		e.preventDefault();
		formError = null;

		try {
			await pb.collection('users').create({
				email: email.toLowerCase(),
				password,
				passwordConfirm: password
			});

			await pb.collection('users').requestVerification(email.toLowerCase());
			await signIn(email.toLowerCase(), password);
			goto('/email-confirm');
		} catch (err) {
			if (err instanceof ClientResponseError) {
				console.error('Error details:', err.data);
				formError = {
					message: err.data?.message,
					email: err.data?.data.email?.message,
					password: err.data?.data.password?.message
				};
			} else {
				console.error('Unexpected error:', err);
			}
			return;
		}
	};
</script>

<h1 class="text-h2 p-6 text-center font-semibold">Sign up to start practicing!</h1>

<div class="w-full px-6 py-4">
	{#if formError}
		<p class="text-danger text-sm">{formError.message}</p>
	{/if}
	<Button onclick={oauth2} className="w-full" variant="outline" size="small">
		<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 1000 1000"
			><path
				fill="red"
				d="M177.188 0C79.032 0 0 79.032 0 177.188v645.625c0 98.156 79.032 177.188 177.188 177.188h475.188l347.625-499.875L652.376.001zm266.094 182.563h112.906c6.932 0 10.906 2.535 10.906 8.5v622.25c0 4.234-1.995 6.781-7.938 6.781H497.75c-3.934 0-6.906-3.396-6.906-5.938V583.781h-49.563L303.625 814.156c-1.976 4.239-5.932 5.938-11.875 5.938h-70.313c-7.9 0-12.854-5.937-7.906-13.594l151.5-234.625c-81.187-30.602-126.75-92.656-126.75-176.813c0-140.264 94.091-212.5 205-212.5zm-2.969 54.375c-60.412 0-119.844 43.352-119.844 149.625c0 102.011 63.389 142.813 128.75 142.813h41.625V236.938z"
			/></svg
		>
		<p>Yandex</p>
	</Button>
</div>

<form onsubmit={signup} class="mx-auto flex flex-col px-6">
	<div class="mb-2 flex items-center justify-center">
		<span class="bg-whisper-100 inline-block h-[1px] w-[100px]"></span>
		<span class="relative bottom-1 mx-2">or</span>
		<span class="bg-whisper-100 inline-block h-[1px] w-[100px]"></span>
	</div>

	<div class="mb-5 space-y-2">
		<Input
			isError={Boolean(formError?.email)}
			variant="solid"
			bind:value={email}
			name="email"
			required
			type="email"
			placeholder="Enter your email"
		>
			{#snippet icon(isError: boolean, focus: boolean)}
				<Email
					fill={isError ? 'var(--danger)' : focus ? 'var(--whisper-700)' : 'var(--whisper-500)'}
				/>
			{/snippet}
			{#snippet error()}
				{#if formError?.email}
					<p class="text-danger px-2 text-sm font-semibold">{formError?.email}</p>
				{/if}
			{/snippet}
		</Input>

		<Input
			isError={Boolean(formError?.password)}
			variant="solid"
			bind:value={password}
			name="password"
			required
			type={isPasswordVisible ? 'text' : 'password'}
			placeholder="Set a password"
		>
			{#snippet icon(isError: boolean, focus: boolean)}
				<button
					class="flex items-center"
					onclick={(event) => {
						event.preventDefault();
						isPasswordVisible = !isPasswordVisible;
					}}
					type="button"
				>
					{#if !isPasswordVisible}
						<EyeClosed
							fill={isError ? 'var(--danger)' : focus ? 'var(--whisper-700)' : 'var(--whisper-500)'}
						/>
					{:else}
						<EyeOpen
							fill={isError ? 'var(--danger)' : focus ? 'var(--whisper-700)' : 'var(--whisper-500)'}
						/>
					{/if}
				</button>
			{/snippet}
			{#snippet error()}
				{#if formError?.password}
					<p class="text-danger px-2 text-sm font-semibold">{formError?.password}</p>
				{/if}
			{/snippet}
		</Input>
	</div>

	<div class="mb-4 flex items-center space-x-2">
		<input
			id="agree"
			name="agree"
			bind:checked={agree}
			class="h-4 w-4 border border-gray-300"
			required
			type="checkbox"
		/>
		<label for="agree" class="text-sm">
			Я принимаю
			<a href="/terms" class="text-blue-600 underline">Политику конфиденциальности</a>
			и
			<a href="/terms" class="text-blue-600 underline">Условия использования</a>
		</label>
	</div>

	<div class="mx-6 mb-4">
		<Button disabled={!email || !password || !agree} className="w-full text-white" variant="solid">
			Sign up with email
		</Button>
	</div>

	<p class="pt-12 text-center">
		<a href="/sign-in">
			Already have an account?
			<span class="ml-1 font-semibold underline">Log In</span>
		</a>
	</p>
</form>
