<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}
	let { size = NaN, width = 40, height = 40, fill = 'none' }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	viewBox="0 0 40 40"
	{fill}
	xmlns="http://www.w3.org/2000/svg"
>
	<rect width="40" height="40" rx="20" fill="#141414" />
	<path
		d="M28.399 29.5999L28.3993 26.0002C28.3995 24.0119 26.7876 22.3999 24.7993 22.3999H15.2C13.2119 22.3999 11.6002 24.0114 11.6 25.9995L11.5996 29.5999M23.5996 13.9999C23.5996 15.9881 21.9878 17.5999 19.9996 17.5999C18.0114 17.5999 16.3996 15.9881 16.3996 13.9999C16.3996 12.0117 18.0114 10.3999 19.9996 10.3999C21.9878 10.3999 23.5996 12.0117 23.5996 13.9999Z"
		stroke="white"
		stroke-width="1.4"
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
