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
	<path d="M34.5833 10H50V33.9583H34.5833V10Z" {fill} />
	<path d="M50 10H65.4167V33.9583H50V10Z" {fill} />
	<path d="M34.5833 33.9583H50C50 45.004 45.629 50 34.5833 50V33.9583Z" {fill} />
	<path d="M50 33.9583H65.4167V50C54.371 50 50 45.004 50 33.9583Z" {fill} />
	<path d="M65.4167 33.9583H90V50H65.4167V33.9583Z" {fill} />
	<path d="M10 33.9583H34.5833V50H10V33.9583Z" {fill} />
	<path d="M10 50H34.5833V64.75H10V50Z" {fill} />
	<path d="M34.5833 50C45.629 50 50 53.7043 50 64.75H34.5833V50Z" {fill} />
	<path d="M50 64.75C50 53.7043 54.371 50 65.4167 50V64.75H50Z" {fill} />
	<path d="M65.4167 50H90V64.75H65.4167V50Z" {fill} />
	<path d="M50 64.75H65.4167V90H50V64.75Z" {fill} />
	<path d="M34.5833 64.75H50V90H34.5833V64.75Z" {fill} />
</svg>
