<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}
	let { size = NaN, width = 32, height = 32, fill = 'none' }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	fill="none"
	viewBox="0 0 32 32"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		d="M19.0002 22.6665L12.3335 15.9998L19.0002 9.33317"
		stroke={fill}
		stroke-width="1.4"
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
