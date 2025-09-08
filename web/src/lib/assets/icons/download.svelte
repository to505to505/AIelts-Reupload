<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		stroke?: string;
	}

	let { size = NaN, width = 24, height = 24, stroke = '#141414' }: Props = $props();
</script>

<svg
	width={width | size}
	height={height | size}
	viewBox="0 0 24 25"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		d="M4 15.3483L4 18.6267C4 19.1235 4.21071 19.6 4.58579 19.9513C4.96086 20.3026 5.46957 20.5 6 20.5H18C18.5304 20.5 19.0391 20.3026 19.4142 19.9513C19.7893 19.6 20 19.1235 20 18.6267V15.3483M12.0011 4.5V15.1155M12.0011 15.1155L16.5725 11.0594M12.0011 15.1155L7.42969 11.0594"
		{stroke}
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
