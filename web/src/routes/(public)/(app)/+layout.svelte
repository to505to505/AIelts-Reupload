<script lang="ts">
	import App from '$lib/components/layouts/App.svelte';

	let { children } = $props();
</script>

<App>
	{@render children()}
</App>
