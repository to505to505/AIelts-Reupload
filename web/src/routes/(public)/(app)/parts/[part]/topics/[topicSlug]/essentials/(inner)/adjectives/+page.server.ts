import { topicEntries } from '$lib/generated/topic-entries';
import { topics } from '$lib/generated/topics.js';
import { TopicSchema } from '$lib/models/topic';

export const entries = async () => {
	return topicEntries;
};

export const load = async ({ params }) => {
	const topic = TopicSchema.parse(topics.find((t) => t.slug === params.topicSlug));
	return { topic };
};
