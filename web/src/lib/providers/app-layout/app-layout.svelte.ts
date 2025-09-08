import { page } from '$app/state';
import { titleFromPath } from '$lib/providers/app-layout/title-from-path';
import { typeFromPath } from '$lib/providers/app-layout/type-from-path';

import { activeAttemptProvider } from '../active-attempt/active-attempt.svelte';

class AppLayoutProvider {
	_activeAttempt = $derived(activeAttemptProvider.attempt);

	_tasks = $derived(
		this._activeAttempt?.expand?.answers
			? this._activeAttempt.expand.answers
					.map((answer) => answer.expand?.task)
					.filter((task): task is NonNullable<typeof task> => task !== undefined)
			: null
	);
	title = $derived(titleFromPath(page.url.pathname, this._tasks));
	type = $derived(typeFromPath(page.url.pathname));
}

export const appLayoutProvider = new AppLayoutProvider();
