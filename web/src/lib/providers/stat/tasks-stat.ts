import { z } from 'zod';

import { AttemptStatSchema, TaskStatMapSchema, TaskStatSchema } from '$lib/models/stat';

export const getTasksMap = (history: z.infer<typeof AttemptStatSchema>[] | null) => {
	const sucessHistory = history?.filter((a) => a?.result?.feedback);
	const taskMap = new Map<string, z.infer<typeof TaskStatSchema>>();

	for (const attemptStat of sucessHistory || []) {
		for (const task of attemptStat.tasks) {
			let taskStat = taskMap.get(task.id);
			if (!taskStat) {
				taskStat = {
					slug: task.slug,
					subhistory: [],
					averageBandScore: 0,
					maxBandScore: -Infinity,
					minBandScore: Infinity
				};
				taskMap.set(task.id, taskStat);
			}

			taskStat.subhistory.push(attemptStat);

			const totalScore = taskStat.subhistory.reduce((acc, curr) => acc + curr.bandScore, 0);
			const count = taskStat.subhistory.length;
			taskStat.averageBandScore = totalScore / count;
			taskStat.maxBandScore = Math.max(taskStat.maxBandScore, attemptStat.bandScore);
			taskStat.minBandScore = Math.min(taskStat.minBandScore, attemptStat.bandScore);
		}
	}

	for (const taskStat of taskMap.values()) {
		taskStat.subhistory.sort((a, b) => {
			const dateA = new Date(a.created || 0);
			const dateB = new Date(b.created || 0);
			return dateB.getTime() - dateA.getTime();
		});
	}

	return TaskStatMapSchema.parse(Object.fromEntries(taskMap));
};
