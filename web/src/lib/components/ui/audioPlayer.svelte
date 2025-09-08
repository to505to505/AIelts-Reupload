<script module>
	let current: HTMLAudioElement | null = $state(null);
</script>

<script lang="ts">
	import { Tween } from 'svelte/motion';

	import FinishRecording from '$lib/assets/icons/finishRecording.svelte';
	import Play from '$lib/assets/icons/play.svelte';

	interface Props {
		src: string;
	}

	let { src }: Props = $props();

	let paused = $state(true);
	let time = $state(0);
	let duration = $state(0);

	let progress = new Tween(0, {
		duration: 10
	});
	$effect(() => {
		progress.target = (time / duration) * 100;
	});

	function format(time: number) {
		if (isNaN(time)) return '...';

		const minutes = Math.floor(time / 60);
		const seconds = Math.floor(time % 60);

		return `${minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
	}
</script>

<div>
	<audio
		onended={() => (time = 0)}
		onplay={(event) => {
			const audio = event.currentTarget;
			if (audio !== current) {
				current?.pause();
				if (current) current.currentTime = 0;

				current = audio;
			}
		}}
		{src}
		bind:duration
		bind:currentTime={time}
		bind:paused
	>
	</audio>

	<div class="bg-gray flex items-center gap-3 rounded-lg pb-4 pl-3 pr-4 pt-4">
		<button
			onclick={() => (paused = !paused)}
			aria-label={paused ? 'play' : 'pause'}
			class="bg-whisper-950 max-w-min rounded-full p-3"
		>
			{#if paused}
				<Play />
			{:else}
				<FinishRecording />
			{/if}
		</button>
		<div class="w-full space-y-2">
			<div class="flex w-full justify-between">
				<p class="text-sm font-semibold">{format(time)}</p>
				<p class="text-sm font-semibold">{format(duration)}</p>
			</div>
			<div
				class="bg-whisper-150 h-1.5 w-full overflow-hidden rounded-sm hover:cursor-pointer active:h-2 active:cursor-grab"
				onpointerdown={(e) => {
					const div = e.currentTarget;

					function seek(e: PointerEvent) {
						const { left, width } = div.getBoundingClientRect();

						let p = (e.clientX - left) / width;
						if (p < 0) p = 0;
						if (p > 1) p = 1;

						time = p * duration;
					}

					seek(e);

					window.addEventListener('pointermove', seek);

					window.addEventListener(
						'pointerup',
						() => {
							window.removeEventListener('pointermove', seek);
							paused = false;
						},
						{
							once: true
						}
					);
				}}
			>
				<div class="bg-whisper-950 h-full rounded-r-md" style:width={`${progress.current}%`}></div>
			</div>
		</div>
	</div>
</div>
