<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}

	let { size = NaN, width = 36, height = 36, fill = '#5E5E5E' }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	viewBox="0 0 36 36"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		fill-rule="evenodd"
		clip-rule="evenodd"
		d="M4 18C4 10.268 10.268 4 18 4C25.732 4 32 10.268 32 18C32 25.732 25.732 32 18 32C10.268 32 4 25.732 4 18ZM25.3624 15.7374C26.0459 15.054 26.0459 13.946 25.3624 13.2626C24.679 12.5791 23.571 12.5791 22.8876 13.2626L16.25 19.9001L13.9874 17.6376C13.304 16.9541 12.196 16.9541 11.5126 17.6376C10.8291 18.321 10.8291 19.429 11.5126 20.1124L15.0126 23.6124C15.696 24.2959 16.804 24.2959 17.4874 23.6124L25.3624 15.7374Z"
		{fill}
	/>
</svg>
