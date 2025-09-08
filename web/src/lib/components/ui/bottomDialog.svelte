<script lang="ts">
	import { fade, slide } from 'svelte/transition';
	import { Dialog } from 'bits-ui';

	import Close from '$lib/assets/icons/close.svg';
	import type { Snippet } from 'svelte';

	interface Props {
		title: Snippet;
		description: Snippet;
		open?: boolean;
	}
	let { title, description, open = $bindable(false) }: Props = $props();
</script>

<Dialog.Root bind:open>
	<Dialog.Portal>
		<Dialog.Overlay
			transition={fade}
			transitionConfig={{ duration: 250 }}
			class="fixed inset-0 z-50 bg-whisper-950 opacity-90"
		/>
		<Dialog.Content
			transition={slide}
			class="fixed bottom-0 z-50 h-3/4 max-h-[75%] w-screen overflow-y-scroll rounded-xl bg-whisper-100 pb-6 pl-6"
		>
			<Dialog.Title class="fixed w-4/5 bg-whisper-100 pb-4 pt-10">
				{@render title()}
			</Dialog.Title>

			<Dialog.Close class="fixed right-0 p-4">
				<img src={Close} alt="close" />
			</Dialog.Close>

			<Dialog.Description class="pr-6 pt-20">
				{@render description()}
			</Dialog.Description>
		</Dialog.Content>
	</Dialog.Portal>
</Dialog.Root>
