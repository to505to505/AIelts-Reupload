<script lang="ts">
	import { cva, type VariantProps } from 'class-variance-authority';
	import { mrg } from '$lib/helpers/mrg';
	import type { ClassValue } from 'clsx';
	import type { Snippet } from 'svelte';

	const buttonVars = cva(
		`hover:cursor-pointer font-semibold active:scale-95 transition-all inline-flex items-center justify-center whitespace-nowrap transition-colors
    focus-visible:outline-none focus-visible:ring-3 focus-visible:ring-blue-500 disabled:pointer-events-none`,
		{
			variants: {
				variant: {
					default: 'bg-whisper-950 text-bg-white disabled:bg-whisper-150',
					solid: 'bg-whisper-950 text-bg-white disabled:bg-whisper-150',
					outline:
						'border border-whisper-500 text-whisper-950 disabled:text-whisper-150 disabled:border-whisper-150',
					light: 'border-none text-whisper-950'
				},
				size: {
					default: 'px-6 py-3 space-x-[0.625rem] rounded-md',
					large: 'text-xl px-9 py-4 space-x-[0.625rem] rounded-md',
					medium: 'px-6 py-3 space-x-[0.625rem] rounded-sm',
					small: 'px-4 py-2 space-x-2 rounded-tiny'
				}
			},
			defaultVariants: {
				variant: 'default',
				size: 'default'
			}
		}
	);

	type ButtonVars = VariantProps<typeof buttonVars>;
	interface Props {
		children: Snippet;
		type?: 'submit' | 'reset' | 'button' | null | undefined;
		variant?: ButtonVars['variant'];
		size?: ButtonVars['size'];
		disabled?: boolean;
		className?: ClassValue[] | string;
		onclick?: (e: MouseEvent) => void;
	}

	let {
		children,
		type = undefined,
		variant = 'default',
		size = 'default',
		disabled = false,
		className = '',
		onclick
	}: Props = $props();
</script>

<button {type} {onclick} {disabled} class={mrg(buttonVars({ variant, size, className }))}>
	{@render children()}
</button>
