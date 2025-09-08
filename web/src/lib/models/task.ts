import { z } from 'zod';
import { TopicSchema } from './topic';

export const TaskSchema = z.object({
	id: z.string(),
	examType: z.enum(['general', 'academic']),
	section: z.enum(['writing', 'speaking']),
	part: z.number().min(1).max(3),
	topic: z.string(),
	title: z.string(),
	slug: z.string(),
	questions: z.string(),
	free: z.boolean(),
	expand: z
		.object({
			topic: TopicSchema.optional()
		})
		.optional()
});
