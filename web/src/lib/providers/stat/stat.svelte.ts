import type { AttemptStatSchema, TaskStatMapSchema, UserStatSchema } from '$lib/models/stat';
import { z } from 'zod';
import { getTasksMap } from './tasks-stat';
import { getUserStat } from './user-stat';
import { setHistory } from './history';

class StatProvider {
	history: z.infer<typeof AttemptStatSchema>[] | null = $state(null);
	tasksMap: z.infer<typeof TaskStatMapSchema> = $derived(getTasksMap(this.history));
	user: z.infer<typeof UserStatSchema> = $derived(getUserStat(this.history));

	clearAll() {
		setHistory(null);
	}
}

export const statProvider = new StatProvider();
