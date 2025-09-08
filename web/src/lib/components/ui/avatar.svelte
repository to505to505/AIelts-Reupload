<script lang="ts">
	import { mrg } from '$lib/helpers/mrg';
	import { Avatar } from 'bits-ui';
	import UserProfile from '$lib/assets/icons/userProfile.svelte';

	interface Props {
		src?: string;
		alt?: string;
		loadingStatus?: any | null;
		size?: number;
	}

	let { src = '', alt = '', loadingStatus = 'loading', size = 44 }: Props = $props();
</script>

<Avatar.Root
	bind:loadingStatus
	class={mrg('bg-gray outline-whisper-150 rounded-full text-[17px] font-medium uppercase outline', {
		'border-transparent': loadingStatus !== 'loaded'
	})}
>
	<div
		style:width={`${size}px`}
		style:height={`${size}px`}
		class="flex h-full w-full items-center justify-center overflow-hidden rounded-full border-transparent"
	>
		<Avatar.Image {src} {alt} draggable="false" />
		<Avatar.Fallback draggable="false"><UserProfile /></Avatar.Fallback>
	</div>
</Avatar.Root>
