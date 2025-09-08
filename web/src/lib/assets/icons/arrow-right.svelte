<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		stroke?: string;
	}
	let { size = NaN, width = 16, height = 16, stroke = '#141414' }: Props = $props();
</script>

<svg width={width || size} height={height || size} viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
	<path
		d="M8.88921 3.3335L13.3337 8.00016M13.3337 8.00016L8.88921 12.6668M13.3337 8.00016L2.66699 8.00016"
		{stroke}
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
