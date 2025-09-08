import { z } from 'zod';
import { TopicSchema } from '$lib/models/topic.js';
import { TaskSchema } from '$lib/models/task.js';

import { topics as rawTopics } from '$lib/generated/topics.js';
import { tasks as rawTasks } from '$lib/generated/tasks.js';

export const entries = () => {
	return [{ part: '1' }, { part: '2' }, { part: '3' }];
};

export const load = async () => {
	const topics = z.array(TopicSchema).parse(rawTopics);

	for (let index = 0; index < topics.length; index++) {
		const tasks = z
			.array(TaskSchema)
			.parse(rawTasks)
			.filter((task) => task.topic === topics[index].id);
		const freeTopic = tasks.some((task) => task.free);
		topics[index].free = freeTopic;
	}

	return { topics };
};
