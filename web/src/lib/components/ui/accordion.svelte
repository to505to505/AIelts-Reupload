<script lang="ts">
	import { Accordion } from 'bits-ui';
	import { slide } from 'svelte/transition';
	import Back from '$lib/assets/icons/back.svelte';

	export let items: { title: string; content: string }[];
</script>

<Accordion.Root class="w-full sm:max-w-[70%]" type="multiple">
	{#each items as item, i}
		<Accordion.Item value="${i}" class="border-dark-10 group border-b px-1.5">
			<Accordion.Header>
				<Accordion.Trigger
					class="flex w-full flex-1 items-center justify-between py-5 text-left text-[15px] font-semibold transition-all [&[data-state=open]>span>svg]:rotate-180 "
				>
					{item.title}
					<span
						class="hover:bg-dark-10 inline-flex size-8 rotate-180 items-center justify-center rounded-[7px] bg-transparent transition-all"
					>
						<Back />
					</span>
				</Accordion.Trigger>
			</Accordion.Header>

			<Accordion.Content class="pb-[25px] text-sm tracking-[-0.01em]" forceMount>
				{#snippet child({ props, open })}
					{#if open}
						<div {...props} transition:slide={{ duration: 200 }}>
							{item.content}
						</div>
					{/if}
				{/snippet}
			</Accordion.Content>
		</Accordion.Item>
	{/each}
</Accordion.Root>
