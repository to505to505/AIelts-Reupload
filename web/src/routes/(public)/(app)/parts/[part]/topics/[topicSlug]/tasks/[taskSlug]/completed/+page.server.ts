import { TaskSchema } from '$lib/models/task';
import { TopicSchema } from '$lib/models/topic';

import { taskEntries } from '$lib/generated/task-entries';
import { topics } from '$lib/generated/topics.js';
import { tasks } from '$lib/generated/tasks.js';

export const entries = async () => {
	return taskEntries;
};

export const load = async ({ params }) => {
	const topic = TopicSchema.parse(topics.find((t) => t.slug === params.topicSlug));
	const task = TaskSchema.parse(tasks.find((t) => t.slug === params.taskSlug));
	return { topic, task };
};
