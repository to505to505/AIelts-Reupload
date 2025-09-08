<script lang="ts">
	import { goto } from '$app/navigation';
	import Button from '$lib/components/ui/button.svelte';

	import { portraits } from '$lib/data/portraits';

	import CheckMark from '$lib/assets/icons/checkMark.svelte';

	import { phoneFeatures } from '$lib/data/phone-features';
	import { appFeatures } from '$lib/data/app-features';

	import Avatar from '$lib/components/ui/avatar.svelte';
	import DragSlider from '$lib/components/ui/drag-slider.svelte';

	import { feedbacks } from '$lib/data/feedbacks';

	import Accordion from '$lib/components/ui/accordion.svelte';
	import { faqItems } from '$lib/data/faq-items';

	import Logo from '$lib/assets/icons/Logo.svelte';
	import { mrg } from '$lib/helpers/mrg';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	import PhoneFrame from '$lib/assets/images/phone-frame.png';
	import bgTAMobile from '$lib/assets/images/backgrounds/bg-TA-mobile.webp';
	import bgTADesktop from '$lib/assets/images/backgrounds/bg-TA-desktop.webp';
	//@ts-ignore
	import offerSrcSet from '$lib/assets/images/offer-mobile.webp?w=400;800;1200&format=webp&as=srcset';

	let openedCookies = $state(false);

	onMount(() => {
		const timeout = setTimeout(() => {
			if (localStorage.getItem('useCookies')) return;
			openedCookies = true;
		}, 2000);

		return () => clearTimeout(timeout);
	});

	const closeCookies = () => {
		localStorage.setItem('useCookies', 'true');
		openedCookies = false;
	};
</script>

<svelte:head>
	<link rel="preconnect" href="https://www.youtube.com" />
</svelte:head>

<header class="flex items-center justify-between px-4 py-6">
	<Logo />
	<Button onclick={() => goto('/sign-up')} variant="outline" size="small">Sign Up</Button>
</header>

<main>
	<!-- HERO SECTION -->
	<section
		class={mrg(
			'pb-12 pt-4',
			'grid-cols-2 grid-rows-[3fr_1fr] md:grid md:pb-[50px] md:pl-[40px]',
			'lg:pb-[100px] lg:pl-[80px]'
		)}
	>
		<div class={mrg('space-y-3 px-6', 'md:pb-[70px] md:pt-[50px]', 'lg:pt-[100px]')}>
			<h1
				class={mrg(
					'text-h2 font-semibold',
					'md:text-[34px] md:leading-[44px]',
					'lg:text-[45px] lg:leading-[56px]'
				)}
			>
				Prepare for IELTS Speaking with an AI
			</h1>
			<p class={mrg('text-xl', 'md:text-xl', 'lg:text-h3')}>
				Get a month of AI-enhanced preparation at the price of one tutoring session
			</p>
		</div>

		<img
			loading="eager"
			class="col-start-2 row-span-2 block aspect-square md:w-full"
			srcset={offerSrcSet}
			sizes="(max-width: 768px) 100vw, 50vw"
			src={offerSrcSet.split(',')[1].split(' ')[0]}
			alt="offer girl"
		/>

		<div class={mrg('flex justify-center px-6 pt-4', 'md:items-start md:justify-start')}>
			<Button
				onclick={() => goto('/sign-up')}
				className="max-h-[60px] text-md py-3"
				variant="solid"
				size="large"
			>
				<span class="px-6 text-white"> Start preparation </span>
			</Button>
		</div>
	</section>

	<!-- PORTRAITS -->
	<section class="rounded-4xl relative min-h-[300px] overflow-hidden bg-center pb-12 pt-5">
		<picture>
			<source src={bgTAMobile} media="(max-width: 768px)" />
			<source src={bgTADesktop} media="(min-width: 769px)" />
			<img
				loading="lazy"
				class="absolute inset-0 z-[-1] h-full w-full object-cover"
				src={bgTAMobile}
				alt=""
			/>
		</picture>
		<h2 class={mrg('px-8 py-4 text-xl font-semibold', 'md:text-h3')}>Take your chance!</h2>

		<ul
			class={mrg(
				'flex flex-col gap-2 px-8 *:rounded-xl *:bg-white *:px-5 *:py-4',
				'md:flex-row md:space-x-3 md:space-y-0'
			)}
		>
			{#each portraits as portrait}
				<li class="md:space-y-3">
					<portrait.img />
					<h3 class={mrg('font-semibold', 'md:text-xl')}>{portrait.heading}</h3>
					<p class={mrg('text-sm')}>{portrait.content}</p>
				</li>
			{/each}
		</ul>
	</section>

	<!-- APP FEATURES -->
	<section class="mt-7 pb-12">
		<div class="flex flex-col items-center space-y-4 pb-4 pt-8">
			<div>
				<Logo />
			</div>
			<p class={mrg('max-w-[300px] text-center', 'md:text-h3 md:max-w-[630px]')}>
				aiELTS — is an AI-based language practice platform, designed specifically to evaluate skills
				for IELTS Speaking
			</p>
		</div>

		<ul class={mrg('space-y-2 px-6 py-5', 'md:mx-auto md:max-w-[700px] md:space-y-[22px]')}>
			<li
				class={mrg(
					'bg-chimera-100 max-w-[280px] rounded-lg px-5 py-4 text-sm',
					'md:max-w-[550px]  md:text-lg'
				)}
			>
				<p>
					The evaluation of speaking test is accomplished by an <span class="font-bold"
						>advanced GPT-4o model,</span
					> fine-tuned on a large dataset of speaking exams graded by IELTS experts.
				</p>
			</li>

			<li
				class={mrg(
					'bg-mindaro-200 relative ml-auto max-w-[280px] rounded-lg px-5 py-4 text-sm',
					'md:w-full md:max-w-[550px]'
				)}
			>
				<p class="text-sm md:block md:text-lg">
					94% of the simulator's scores match the IELTS expert's assessment with an accuracy of ±0.5
					points
				</p>
			</li>
		</ul>

		<ul class={mrg('space-y-6 px-6 pt-4', 'grid-cols-2 grid-rows-2 gap-8 md:grid md:space-y-0')}>
			{#each appFeatures as point}
				<li class="flex items-center space-x-4">
					<div>
						<CheckMark />
					</div>
					<div>
						<h3 class="text-lg font-semibold">{point.heading}</h3>
						<p>{@html point.content}</p>
					</div>
				</li>
			{/each}
		</ul>
	</section>

	<!-- PHONE FEATURES -->
	<section
		class={mrg(
			'bg-whisper-950 relative mx-6 flex min-h-[690px] flex-col rounded-xl pb-12 pt-4',
			'md:justify-between md:p-0'
		)}
	>
		<h2
			class={mrg(
				'max-w-[328px] px-8 py-4 text-lg font-bold text-white ',
				'md:text-h2 md:ml-[26rem] md:mt-28 md:max-w-[539px]'
			)}
		>
			Excel in your exam performance&nbsp;with aiELTS
		</h2>
		<div
			class={mrg(
				'relative mx-auto mb-10 overflow-hidden rounded-lg',
				'h-full md:absolute md:w-full'
			)}
		>
			<img
				class={mrg('relative z-10', 'md:my-[3.75rem] md:ml-16 md:mr-auto md:w-[272px]')}
				src={PhoneFrame}
				alt=""
			/>
		</div>
		<DragSlider modifiers="self-end md:mb-36">
			{#each phoneFeatures as card}
				<li class="h-fit min-w-[312px] list-none overflow-hidden rounded-lg">
					<h3 class={['px-5 pb-3 pt-4 text-lg font-semibold', card.headerColor]}>
						{@html card.heading}
					</h3>
					<p class={['px-5 py-4', card.primaryColor]}>
						{card.content}
					</p>
				</li>
			{/each}
		</DragSlider>
	</section>

	<!-- VIDEO AND FEEDBACKS -->
	<section class="pt-4">
		<h2 class="hidden px-8 py-4 text-center text-xl font-semibold">Watch video how it works!</h2>

		<iframe
			class="mx-auto mb-12 hidden h-[200px] min-h-[100] w-[310px] min-w-[140px] rounded-lg md:mb-[100px] md:h-[360px] md:w-[800px]"
			title="Service showcase"
			src="https://www.youtube.com/embed/tgbNymZ7vqY"
		>
		</iframe>

		<div
			class={mrg(
				'rounded-4xl relative overflow-hidden bg-[url(/bg-TA-mobile.webp)] bg-cover bg-center pb-12 pt-5',
				'bg-[url(/bg-TA-desktop.webp)]'
			)}
		>
			<h2 class="px-8 py-4 text-xl font-semibold">Users' Feedback</h2>

			<DragSlider>
				{#each feedbacks as comment}
					<div class="h-fit min-w-[312px] max-w-[312px] space-y-3 rounded-lg bg-white px-5 py-4">
						<div class="flex items-center space-x-3 px-2">
							<Avatar src={comment.avatar} />
							<div>
								<h4 class="font-semibold">{comment.name}</h4>
								<p>{comment.username}</p>
							</div>
						</div>
						<p class="text-sm">
							{comment.comment}
						</p>
					</div>
				{/each}
			</DragSlider>
		</div>
	</section>

	<!-- FAQS -->
	<section id="faq" class="mb-12 pt-4">
		<h2 class="px-8 py-4 text-center text-xl font-semibold">FAQs</h2>

		<div class="flex justify-center px-6">
			<Accordion items={faqItems} />
		</div>
	</section>
</main>

<footer
	class={mrg('bg-whisper-100 rounded-t-xl px-6 pb-[100px] pt-10 md:flex md:space-x-8', 'xl:mx-9')}
>
	<div>
		<h3 class="mb-2 text-xl font-semibold">Resourses</h3>
		<ul class="mb-5">
			<li class="text-lg"><a href="/">About IELTS</a></li>
			<li class="text-lg"><a href="/terms">Privacy Policy</a></li>
			<li class="text-lg"><a href="/terms">Term and Conditions</a></li>
			<li class="text-lg"><a href="/">Refund and Cancellation</a></li>
		</ul>
	</div>

	<div>
		<h3 class="mb-2 text-xl font-semibold">Contact Us</h3>
	</div>
</footer>

{#if openedCookies}
	<div
		class="fixed bottom-4 right-4 z-50 w-72 rounded-lg border border-gray-200 bg-white p-4 shadow-md"
		transition:fade
	>
		<h3 class="mb-2 text-lg font-semibold">Мы используем файлы cookie</h3>
		<p class="mb-4 text-sm">
			Они улучшают работу сайта. Продолжая использовать сайт, вы соглашаетесь с нашей
			<a href="/terms" class="text-blue-600 underline">Политикой конфиденциальности</a>.
		</p>
		<button
			class="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
			onclick={closeCookies}
		>
			Отлично
		</button>
	</div>
{/if}
