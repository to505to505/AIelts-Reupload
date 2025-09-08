<script lang="ts">
  interface Props {
    size?: number;
    width?: number;
    height?: number;
    stroke?: string;
    fill?: string;
  }

  let { size = NaN, width = 24, height = 24, stroke = '#141414' }: Props = $props();
</script>

<svg
  width={size | width}
  height={size | height}
  viewBox="0 0 32 32"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
>
  <path
    d="M15.9987 22V22.0527M13 12.3067C13 10.6185 14.3431 9.25 16 9.25C17.6569 9.25 19 10.6185 19 12.3067C19 13.9948 17.6569 15.3633 16 15.3633C16 15.3633 15.9987 16.2757 15.9987 17.4011M28 16C28 22.6274 22.6274 28 16 28C9.37258 28 4 22.6274 4 16C4 9.37258 9.37258 4 16 4C22.6274 4 28 9.37258 28 16Z"
    {stroke}
    stroke-width="1.4"
    stroke-linecap="round"
    stroke-linejoin="round"
  />
</svg>
