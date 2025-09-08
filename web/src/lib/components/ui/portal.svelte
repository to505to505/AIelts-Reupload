<script lang="ts" module>
	import { onDestroy, tick } from 'svelte';

	export const portal = (el: HTMLElement, target: HTMLElement | string = 'body') => {
		let targetEl;

		async function update(newTarget: HTMLElement | string) {
			target = newTarget;
			if (typeof target === 'string') {
				targetEl = document.querySelector(target);
				if (targetEl === null) {
					await tick();
					targetEl = document.querySelector(target);
				}
				if (targetEl === null) {
					throw new Error(`No element found matching css selector: "${target}"`);
				}
			} else if (target instanceof HTMLElement) {
				targetEl = target;
			} else {
				throw new TypeError(
					`Unknown portal target type: ${
						target === null ? 'null' : typeof target
					}. Allowed types: string (CSS selector) or HTMLElement.`
				);
			}
			targetEl.appendChild(el);

			document.body.classList.add('overflow-hidden');
			el.hidden = false;
		}

		function destroy() {
			if (el.parentNode) {
				el.parentNode.removeChild(el);
				document.body.classList.remove('overflow-hidden');
			}
		}

		update(target);
		return {
			update,
			destroy
		};
	};
</script>

<script lang="ts">
	import type { Snippet } from 'svelte';
	import { fade } from 'svelte/transition';

	interface Props {
		children: Snippet;
		target?: HTMLElement | string;
		opened?: boolean;
	}

	let { target = 'body', opened = $bindable(), children }: Props = $props();
</script>

	<div
		id="modal-portal"
		class="fixed left-0 top-0 z-[9999] flex h-screen w-full flex-col justify-end"
		use:portal={target}
	>
		<div
			transition:fade
			tabindex="0"
			role="button"
			class="absolute left-0 top-0 h-full w-full bg-black bg-opacity-20"
			onclick={() => (opened = false)}
		></div>
		{@render children()}
	</div>
