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
	viewBox="0 0 24 24"
	fill="none"
	xmlns="http://www.w3.org/2000/svg"
>
	<path d="M17.6684 7.83484V4.64734L20.8559 4.64734L17.6684 7.83484Z" {fill} />
	<path d="M7.24035 15.0742V18.2617H4.05285L5.70546 16.609L7.24035 15.0742Z" {fill} />
	<path
		d="M6.48959 17.5104C6.20357 17.2244 5.94219 16.9231 5.70546 16.609M19.3525 6.46871C21.801 9.79488 21.5203 14.5005 18.5104 17.5104C16.3451 19.6757 13.3022 20.4286 10.5267 19.769M14.2152 3.1739C11.5105 2.61932 8.58797 3.39121 6.48959 5.48959C3.45616 8.52303 3.19478 13.2788 5.70546 16.609M5.70546 16.609L4.05285 18.2617H7.24035V15.0742L5.70546 16.609ZM17.6684 7.83484V4.64734L20.8559 4.64734L17.6684 7.83484Z"
		stroke={fill}
		stroke-linecap="round"
		stroke-linejoin="round"
	/>
</svg>
