<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}

	let { size = NaN, width = 56, height = 57, fill = '#141414' }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	viewBox="0 0 24 24"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		d="M4 15V9M12 20V4M8 17V7M20 9V15M16 7L16 17"
		stroke={fill}
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
