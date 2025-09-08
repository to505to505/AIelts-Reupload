<script lang="ts">
	import { cva, type VariantProps } from 'class-variance-authority';
	import { mrg } from '$lib/helpers/mrg';
	import type { ClassValue } from 'clsx';
	import { onMount, type Snippet } from 'svelte';

	const inputVars = cva(
		`w-full px-4 py-3 rounded-sm text-whisper-950
  disabled:opacity-40 placeholder:text-whisper-500
  focus:placeholder:text-black/0 focus:text-whisper-950 placeholder:capitalize`,
		{
			variants: {
				variant: {
					default: '',
					outline: `border border-whisper-500`,
					solid: `bg-gray`,
					ghost: ''
				}
			},
			defaultVariants: {
				variant: 'default'
			}
		}
	);

	type InputVars = VariantProps<typeof inputVars>;

	interface Props {
		icon: Snippet<[boolean, boolean]>;
		name: string;
		error: Snippet;
		isError?: boolean;
		required?: boolean;
		placeholder?: string;
		type?: 'email' | 'password' | 'text' | 'number' | null | undefined;
		variant?: InputVars['variant'];
		disabled?: boolean;
		className?: ClassValue[] | string;
		value?: string;
		focus?: boolean;
	}

	let {
		icon,
		name,
		error,
		isError = false,
		required = false,
		placeholder = '',
		type = undefined,
		variant = 'default',
		disabled = false,
		className = '',
		value = $bindable(''),
		focus = false
	}: Props = $props();

	let inputRef: null | HTMLInputElement = $state(null);

	let errorClasses = $state('');
	if (isError) {
		switch (variant) {
			case 'outline':
				errorClasses = 'border-danger';
				break;
			case 'solid':
				errorClasses = 'bg-danger';
				break;
			default:
				errorClasses = '';
		}
	}

	onMount(() => {
		if (Boolean(focus)) {
			inputRef?.focus();
		}
	});
</script>

<div>
	<label class="relative inline-flex w-full items-center justify-between">
		<input
			{required}
			onfocusin={() => (focus = true)}
			onfocusout={() => (focus = false)}
			{name}
			{placeholder}
			bind:value
			{...{ type }}
			{disabled}
			bind:this={inputRef}
			class={mrg(inputVars({ variant, className }), errorClasses)}
		/>
		<div class="absolute right-3">
			{@render icon(isError, focus)}
		</div>
	</label>
	{#if isError}
		<p class="text-danger px-2 text-sm font-semibold">
			{@render error()}
		</p>
	{/if}
</div>
