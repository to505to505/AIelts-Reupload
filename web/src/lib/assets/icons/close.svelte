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
	{fill}
	viewBox="0 0 38 38"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		fill-rule="evenodd"
		clip-rule="evenodd"
		d="M10.9393 10.9393C11.5251 10.3536 12.4749 10.3536 13.0607 10.9393L19 16.8787L24.9393 10.9393C25.5251 10.3536 26.4749 10.3536 27.0607 10.9393C27.6464 11.5251 27.6464 12.4749 27.0607 13.0607L21.1213 19L27.0607 24.9393C27.6464 25.5251 27.6464 26.4749 27.0607 27.0607C26.4749 27.6464 25.5251 27.6464 24.9393 27.0607L19 21.1213L13.0607 27.0607C12.4749 27.6464 11.5251 27.6464 10.9393 27.0607C10.3536 26.4749 10.3536 25.5251 10.9393 24.9393L16.8787 19L10.9393 13.0607C10.3536 12.4749 10.3536 11.5251 10.9393 10.9393Z"
		{fill}
	/>
</svg>
