<script lang="ts">
	let { data } = $props();

	const content = $derived(data.topic.essentials);
</script>

<main>
	<section class="px-6 py-6">
		<h1 class="text-h3 mb-5 font-semibold">{data.topic.title}</h1>
		<p>{content.introduction.overview}</p>
	</section>

	<section>
		<ul class="flex w-full flex-wrap justify-center gap-2 px-4">
			<a
				href="essentials/main-words"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-mindaro-600 mb-2 size-6 rounded-full border"></div>
				<p>Main words</p>
			</a>

			<a
				href="essentials/adjectives"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-chimera-600 mb-2 size-6 rounded-full border"></div>
				<p>Adjectives</p>
			</a>

			<a
				href="essentials/phrasal-verbs"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-rapture-600 mb-2 size-6 rounded-full border"></div>
				<p>Phrasal Verbs</p>
			</a>

			<a
				href="essentials/collocations"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-mindaro-600 mb-2 size-6 rounded-full border"></div>
				<p>Collocations</p>
			</a>

			<a
				href="essentials/synonyms-antonyms"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-chimera-600 mb-2 size-6 rounded-full border"></div>
				<p>Synonyms & Antonyms</p>
			</a>

			<a
				href="essentials/expressions-idioms"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-rapture-600 mb-2 size-6 rounded-full border"></div>
				<p>Expressions & Idioms</p>
			</a>

			<a
				href="essentials/sample-answers"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-mindaro-600 mb-2 size-6 rounded-full border"></div>
				<p>Sample Answers</p>
			</a>

			<a
				href="essentials/common-mistakes"
				class="border-whisper-500 flex min-h-[84px] w-[calc(50%-3%)] flex-col rounded border px-4 pb-3 pt-4"
			>
				<div class="border-chimera-600 mb-2 size-6 rounded-full border"></div>
				<p>Common Mistakes</p>
			</a>
		</ul>
	</section>
</main>
