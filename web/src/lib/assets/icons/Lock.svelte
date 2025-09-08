<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}
	let { size = NaN, fill = 'black', width = 24, height = 24 }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || height}
	viewBox="0 0 24 24"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path
		fill-rule="evenodd"
		clip-rule="evenodd"
		d="M6.60078 7.88574C6.60078 4.84683 9.00935 2.40002 12.0008 2.40002C14.9922 2.40002 17.4008 4.84683 17.4008 7.88574V8.80002C18.3908 8.80002 19.2008 9.62288 19.2008 10.6286V19.7715C19.2008 20.7772 18.3908 21.6 17.4008 21.6H6.60078C5.61078 21.6 4.80078 20.7772 4.80078 19.7715V10.6286C4.80078 9.62288 5.61078 8.80002 6.60078 8.80002V7.88574ZM15.6008 7.88574C15.6008 5.80465 14.0494 4.2286 12.0008 4.2286C9.95221 4.2286 8.40078 5.80465 8.40078 7.88574V8.80002H15.6008V7.88574Z"
		{fill}
	/>
</svg>
