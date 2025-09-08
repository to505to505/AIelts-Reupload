<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}
	let { size = NaN, width = 140, height = 140, fill = '#999999' }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	viewBox="0 0 100 100"
	{fill}
	xmlns="http://www.w3.org/2000/svg"
	shape-rendering="geometricPrecision"
>
	<path
		d="M50 8L86 28.7959V70.3877L50 91.1836L14 70.3877V28.7959L50 8Z"
		{fill}
		vector-effect="non-scaling-stroke"
	/>
</svg>
