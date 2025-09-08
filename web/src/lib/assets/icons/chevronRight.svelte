<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		stroke?: string;
		strokeWidth?: string;
	}
	let { size = NaN, width = 32, height = 32, stroke = '141414', strokeWidth="1.4" }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	fill="none"
	viewBox="0 0 32 32"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		d="M13.3333 9.3335L20 16.0002L13.3333 22.6668"
		{stroke}
		stroke-width={strokeWidth}
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
