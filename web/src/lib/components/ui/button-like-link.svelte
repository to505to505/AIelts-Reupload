<script lang="ts">
	import ChevronRight from '$lib/assets/icons/chevronRight.svelte';

	interface Props {
		href: string;
		caption: string;
		classNames?: string;
		newTab?: boolean;
		chevronStroke?: string;
	}

	let {
		caption,
		href = '#',
		classNames = '',
		newTab = false,
		chevronStroke = '#141414'
	}: Props = $props();
</script>

<a
	{href}
	target={newTab ? '_blank' : ''}
	class={classNames +
		' bg-whisper-950 text-whisper-800 text-regular flex w-full flex-row items-center justify-between rounded-md bg-white p-4 font-semibold'}
>
	<span>
		{caption}
	</span>
	<ChevronRight stroke={chevronStroke} />
</a>
