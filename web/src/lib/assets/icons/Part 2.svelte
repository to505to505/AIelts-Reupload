<script lang="ts">
	interface Props {
		size?: number;
		width?: number;
		height?: number;
		fill?: string;
	}
	let { size = NaN, width = 100, height = 100, fill = '#999999' }: Props = $props();
</script>

<svg
	width={size || width}
	height={size || width}
	viewBox="0 0 100 100"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path d="M14 86C33.8822 86 50 69.8822 50 50H14V86Z" {fill} />
	<path d="M50 50C50 30.1177 66.1178 14 86 14V50L50 50Z" {fill} />
	<path d="M50 50C30.1178 50 14 33.8822 14 14L50 14L50 50Z" {fill} />
	<path d="M86 86C86 66.1178 69.8823 50 50 50L50 86H86Z" {fill} />
</svg>
