import { z } from 'zod';

import { AttemptSchema } from '$lib/models/attempt';

class ActiveAttemptProvider {
	attempt: z.infer<typeof AttemptSchema> | null = $state(null);
	aborting = $state(false);

	setAttempt(attempt: z.infer<typeof AttemptSchema> | null) {
		if (!attempt) {
			this.attempt = null;
			return;
		}
		attempt.expand?.answers?.sort((a, b) => a.expand!.task!.part - b.expand!.task!.part);
		this.attempt = attempt;
	}

	switchAbort(abort: boolean) {
		this.aborting = abort;
	}

	clearAll() {
		this.setAttempt(null);
		this.switchAbort(false);
	}
}

export const activeAttemptProvider = new ActiveAttemptProvider();
