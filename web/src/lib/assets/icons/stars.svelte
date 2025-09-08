<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		stroke?: string;
	}

	let { size = NaN, width = 24, height = 24, stroke = '#587807' }: Props = $props();
</script>

<svg
	width={width || size}
	height={height || size}
	viewBox="0 0 25 24"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		d="M15.3234 2.3999L17.1537 7.34611L22.0999 9.17637L17.1537 11.0066L15.3234 15.9528L13.4932 11.0066L8.54696 9.17637L13.4932 7.34611L15.3234 2.3999Z"
		{stroke}
		stroke-linejoin="round"
	/>
	<path
		d="M6.85284 13.694L8.45167 16.0481L10.8058 17.647L8.45167 19.2458L6.85284 21.5999L5.25402 19.2458L2.8999 17.647L5.25402 16.0481L6.85284 13.694Z"
		{stroke}
		stroke-linejoin="round"
	/>
</svg>
