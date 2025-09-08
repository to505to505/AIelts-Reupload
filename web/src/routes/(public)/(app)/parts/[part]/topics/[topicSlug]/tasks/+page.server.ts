import { z } from 'zod';

import { TaskSchema } from '$lib/models/task';
import { TopicSchema } from '$lib/models/topic';

import { topicEntries } from '$lib/generated/topic-entries';
import { topics } from '$lib/generated/topics';
import { tasks as taskRecs } from '$lib/generated/tasks';

export const entries = async () => {
	return topicEntries;
};

export const load = async ({ params }) => {
	const topic = TopicSchema.parse(topics.find((t) => t.slug === params.topicSlug));
	const tasks = z
		.array(TaskSchema)
		.parse(taskRecs)
		.filter((task) => task.topic === topic.id && task.part === Number(params.part));
	return { topic, tasks };
};
