<script lang="ts">
	interface Props {
		width?: number;
		height?: number;
		size?: number;
		stroke?: string;
	}
	let { width = 20, height = 20, size = NaN, stroke = 'white' }: Props = $props();
</script>

<svg
	width={width || size}
	height={height || size}
	viewBox="0 0 24 24"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		d="M18 2.3999C19.9882 2.3999 21.6 4.01168 21.6 5.9999V18C21.6 19.9882 19.9882 21.6 18 21.6H6.00002C4.0118 21.6 2.40002 19.9882 2.40002 18L2.40003 5.9999C2.40003 4.01168 4.0118 2.3999 6.00003 2.3999L18 2.3999Z"
		{stroke}
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
