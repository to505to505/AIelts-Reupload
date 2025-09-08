<script lang="ts">
	type Word = { word: string; meaning: string; translation: string; example: string };
	type Collocation = { collocation: string; meaning: string; translation: string; example: string };
	type Mistake = { mistake: string; advice: string };
	type Expression = { expression: string; usage: string };
	type Idiom = { idiom: string; meaning: string };
	type Sample = { question: string; answer: string };
	type SynonymsAntonyms = {
		synonym: string;
		antonym: string;
		synonym_translation: string;
		antonym_translation: string;
	};

	interface Props {
		content: Word | Collocation | Mistake | Expression | Idiom | Sample | SynonymsAntonyms;
	}

	const { content } = $props<Props>();

	function getContentType(item: Props['content']) {
		if ('word' in item) return 'Word';
		if ('collocation' in item) return 'Collocation';
		if ('mistake' in item) return 'Mistake';
		if ('expression' in item) return 'Expression';
		if ('idiom' in item) return 'Idiom';
		if ('question' in item) return 'Sample';
		if ('synonym' in item) return 'SynonymsAntonyms';
		return 'Unknown';
	}

	const contentType = getContentType(content);
</script>

<li class="my-4 flex flex-col rounded-xl bg-white px-4 py-6">
	<section class="mb-3 flex flex-col gap-3">
		{#if contentType === 'Word'}
			<h2 class="text-lg font-semibold capitalize">{content.word}</h2>
			<p class="text-sm">{content.meaning}</p>
			<p class="text-sm font-semibold">RU: {content.translation}</p>
			<hr class="my-3 h-[2px] w-full" />
			<section class="flex flex-col gap-2">
				<h2 class="text-sm font-semibold">Example</h2>
				<p class="text-sm">{content.example}</p>
			</section>
		{:else if contentType === 'Collocation'}
			<h2 class="text-lg font-semibold capitalize">{content.collocation}</h2>
			<p class="text-sm">{content.meaning}</p>
			<p class="text-sm font-semibold">RU: {content.translation}</p>
			<hr class="my-3 h-[2px] w-full" />
			<section class="flex flex-col gap-2">
				<h2 class="text-sm font-semibold">Example</h2>
				<p class="text-sm">{content.example}</p>
			</section>
		{:else if contentType === 'Mistake'}
			<h2 class="text-lg font-semibold capitalize">Mistake</h2>
			<p class="text-sm">{content.mistake}</p>
			<hr class="my-3 h-[2px] w-full" />
			<section class="flex flex-col gap-2">
				<h2 class="text-sm font-semibold">Advice</h2>
				<p class="text-sm">{content.advice}</p>
			</section>
		{:else if contentType === 'Expression'}
			<h2 class="text-lg font-semibold capitalize">"{content.expression}"</h2>
			<p class="text-sm">{content.usage}</p>
		{:else if contentType === 'Idiom'}
			<h2 class="text-lg font-semibold capitalize">"{content.idiom}"</h2>
			<p class="text-sm">{content.meaning}</p>
		{:else if contentType === 'Sample'}
			<h2 class="text-sm font-semibold">Question</h2>
			<p class="text-sm">{content.question}</p>
			<hr class="my-3 h-[2px] w-full" />
			<section class="flex flex-col gap-2">
				<h2 class="text-sm font-semibold">Answer</h2>
				<p class="text-sm">{content.answer}</p>
			</section>
		{:else if contentType === 'SynonymsAntonyms'}
			<h2 class="text-lg font-semibold capitalize">{content.synonym}</h2>
			<p class="text-sm">{content.synonym_translation}</p>
			<hr class="my-3 h-[2px] w-full" />
			<h2 class="text-lg font-semibold capitalize">{content.antonym}</h2>
			<p class="text-sm">{content.antonym_translation}</p>
		{:else}
			<h2 class="text-lg font-semibold capitalize">Unknown Content</h2>
		{/if}
	</section>
</li>
