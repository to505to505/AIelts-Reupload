<script lang="ts">
	export let size = NaN;
	export let width = 36;
	export let height = 36;
	export let fill = '#5E5E5E';
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
		d="M4 18C4 10.268 10.268 4 18 4C25.732 4 32 10.268 32 18C32 25.732 25.732 32 18 32C10.268 32 4 25.732 4 18Z"
		{fill}
	/>
</svg>
