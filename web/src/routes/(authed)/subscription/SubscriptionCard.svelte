<script lang="ts">
	import type { Snippet } from 'svelte';
	import { mrg } from '$lib/helpers/mrg';
	import { calculateSubscriptionPrice } from '$lib/helpers/calculate-price';

	interface Props {
		price: number;
		discount: number;
		subscriptionPeriod: string;
		months: number;
		icon: Snippet;
		color: string;
		clientWidth: number;
		isSelected: boolean;
		onclick?: () => void;
	}

	let {
		price,
		discount,
		subscriptionPeriod,
		clientWidth = $bindable(),
		isSelected = false,
		months,
		onclick,
		icon,
		color
	}: Props = $props();

	const [discountedMonthlyPrice, discountedTotalPrice] = calculateSubscriptionPrice(
		price,
		months,
		discount
	);
</script>

<div
	bind:clientWidth
	{onclick}
	role="button"
	onkeydown={(e) => {
		if (e.key === ' ' || e.key === 'Enter') {
			onclick!();
		}
	}}
	tabindex="0"
	class={mrg(
		'relative flex h-auto w-[90%] shrink-0 cursor-pointer snap-center flex-col gap-6 overflow-hidden rounded bg-white p-5 text-lg font-semibold transition-all duration-300',
		isSelected ? `scale-105 border-2` : ''
	)}
	style:border-color={isSelected ? `var(--color-${color}-600)` : ''}
>
	<div class="z-10 flex items-center justify-between gap-8">
		<h3>{subscriptionPeriod}</h3>
		{#if discount > 0}
			<div
				style:background-color={`var(--color-${color}-600)`}
				class={mrg('rounded px-4 py-1 text-sm text-white')}
			>
				Сэкономьте {discount}%
			</div>
		{/if}
	</div>
	<div class="relative z-10 *:my-1">
		<p class="text-h3">
			{#if discount > 0}
				<span class="text-whisper-700 line-through">{price.toFixed(0)}₽</span>
				{discountedMonthlyPrice.toFixed(0)}₽
			{:else}
				{price.toFixed(0)}₽
			{/if}
		</p>
		<p class="font-semibold">
			{discountedTotalPrice.toFixed(0)}₽ <span class="h-2 w-2 rounded-full bg-black"></span>
			{months === 1 ? 'каждый месяц' : `каждые ${subscriptionPeriod}`}
		</p>
	</div>
	<div class="absolute -right-10 -top-10 z-0">
		{@render icon()}
	</div>
</div>
