import { z } from 'zod';
import { TopicEssentialSchema } from './topic-essentials';

export const TopicSchema = z.object({
	id: z.string(),
	title: z.string(),
	slug: z.string(),
	essentials: TopicEssentialSchema,
	icon: z.string(),
	free: z.boolean().optional(),
	expand: z.any().optional()
});
