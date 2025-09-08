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
	viewBox="0 0 20 20"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		d="M15.8111 9.11445C16.9498 9.74903 16.9539 10.5473 15.8111 11.2647L6.98023 17.2205C5.87065 17.8126 5.11705 17.463 5.03794 16.1817L5.00047 3.71652C4.97549 2.53629 5.94767 2.20283 6.87406 2.7687L15.8111 9.11445Z"
		{stroke}
		stroke-width="1.4"
	/>
</svg>
