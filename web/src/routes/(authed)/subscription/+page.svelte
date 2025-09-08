<script lang="ts">
	import Close from '$lib/assets/icons/close.svelte';
	import FlashOn from '$lib/assets/icons/flashOn.svelte';
	import Lightbulb from '$lib/assets/icons/lightbulb.svelte';
	import Loader from '$lib/assets/icons/loader.svelte';
	import Stars from '$lib/assets/icons/stars.svelte';
	import Part1 from '$lib/assets/icons/Part 1.svelte';
	import Part2 from '$lib/assets/icons/Part 2.svelte';
	import Part3 from '$lib/assets/icons/Part 3.svelte';
	import Button from '$lib/components/ui/button.svelte';
	import { calculateSubscriptionPrice } from '$lib/helpers/calculate-price';

	import SubscriptionCard from './SubscriptionCard.svelte';

	// const monthlyBasePrice = 1500;
	const monthlyBasePrice = 0

	const serviceCons = [
		{
			icon: FlashOn,
			iconColor: 'chimera-700',
			heading: 'Сотни тестов',
			content: 'Получите доступ ко всем темам и тестам с неограниченным количеством попыток'
		},
		{
			icon: Stars,
			iconColor: 'mindaro-600',
			heading: 'Обратная связь от ИИ',
			content: 'Получите персонализированную обратную связь от ИИ для улучшения результатов'
		},
		{
			icon: Lightbulb,
			iconColor: 'rapture-600',
			heading: 'Изучение разнообразных тем',
			content: 'Научитесь обсуждать широкий спектр тем, расширяя при этом свой словарный запас'
		},
		{
			icon: Loader,
			iconColor: 'whisper-950',
			heading: 'Отслеживание уровня языка',
			content: 'Следите за своим уровнем речи с легким доступом к вашей статистике'
		}
	];

	const subscriptionPlans = [
		{ period: '1 месяц', months: 1, discount: 0, icon: Part1, color: 'mindaro' },
		{ period: '3 месяца', months: 3, discount: 20, icon: Part2, color: 'chimera' },
		{ period: '6 месяцев', months: 6, discount: 50, icon: Part3, color: 'rapture' }
	];

	let cardClientWidth = $state(0);
	let selectedSubscriptionPlan = $state<null | number>(null);
	let activeCardIndex = $state(0);
	let scrollContainer: HTMLElement | null = null;

	const selectCard = (index: number) => {
		selectedSubscriptionPlan = index;
		scrollToCard(index);
	};

	const scrollToCard = (index: number) => {
		if (scrollContainer) {
			const scrollLeft = index * (cardClientWidth + 24);
			scrollContainer.scrollTo({ left: scrollLeft, behavior: 'smooth' });
		}
	};

	const handleScroll = () => {
		if (scrollContainer) {
			const index = Math.round(scrollContainer.scrollLeft / (cardClientWidth + 24));
			activeCardIndex = index;
		}
	};
</script>

<h1 class="text-h3 max-w-[312px] pb-2 pl-6 pr-6 pt-4 font-semibold">Подписка</h1>

<ul class="space-y-1 px-2 pb-6 pt-2">
	{#each serviceCons as card}
		{@const BenefitIcon = card.icon}
		<li class="flex flex-row gap-4">
			<BenefitIcon stroke={`var(--${card.iconColor})`} />
			<div>
				<h3 class="text-md font-semibold">{card.heading}</h3>
				<p class="font-regular text-sm">{card.content}</p>
			</div>
		</li>
	{/each}
</ul>

<h2 class="pb-3 pl-4 pr-4 pt-6 text-lg font-semibold">Выберите свой тариф</h2>

<section
	bind:this={scrollContainer}
	onscroll={handleScroll}
	class="bg-gray scrollbar-hide flex w-full snap-x snap-mandatory gap-6 overflow-x-auto px-4 pb-2 pt-4"
>
	{#each subscriptionPlans as plan, i}
		<SubscriptionCard
			color={plan.color}
			months={plan.months}
			discount={plan.discount}
			subscriptionPeriod={plan.period}
			price={monthlyBasePrice}
			isSelected={selectedSubscriptionPlan === i}
			bind:clientWidth={cardClientWidth}
			onclick={() => selectCard(i)}
		>
			{#snippet icon()}
				{@const SubscriptionIcon = plan.icon}
				<SubscriptionIcon fill={`var(--color-${plan.color}-200)`} size={cardClientWidth / 1.5} />
			{/snippet}
		</SubscriptionCard>
	{/each}
</section>

<div class="my-2 flex justify-center gap-2">
	{#each subscriptionPlans as _, i}
		<button
			class="h-3 w-3 rounded-full transition-colors"
			aria-label="Pagination button"
			class:bg-whisper-950={activeCardIndex === i}
			class:bg-whisper-300={activeCardIndex !== i}
			onclick={() => selectCard(i)}
		></button>
	{/each}
</div>
<section class="w-full px-4 pb-12 pt-6 text-center text-white *:my-2">
	<Button disabled={selectedSubscriptionPlan === null} className="w-full font-semibold py-6 px-3"
		>{selectedSubscriptionPlan !== null
			? `Купить за ${calculateSubscriptionPrice(monthlyBasePrice, subscriptionPlans[selectedSubscriptionPlan].months, subscriptionPlans[selectedSubscriptionPlan].discount)[1]}₽/${subscriptionPlans[selectedSubscriptionPlan].period}`
			: 'Выберите подписку'}</Button
	>
	<p class="text-whisper-700 text-sm">Вы можете сменить или отменить подписку в любое время</p>
</section>
