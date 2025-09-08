<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}
	let { size = NaN, width = 32, height = 32, fill = '#141414' }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	viewBox="0 0 32 32"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		fill-rule="evenodd"
		clip-rule="evenodd"
		d="M8.813 17.1529L15.6656 10.2191C15.9541 9.92696 16.4201 9.92696 16.7094 10.2191L23.562 17.1529C23.9793 17.5746 23.9793 18.2608 23.562 18.6833C23.1447 19.105 22.4673 19.105 22.05 18.6833L16.1871 12.7518L10.3257 18.6833C9.90765 19.105 9.23033 19.105 8.813 18.6833C8.39567 18.2608 8.39567 17.5746 8.813 17.1529Z"
		{fill}
	/>
</svg>
