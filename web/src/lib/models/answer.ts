import { z } from 'zod';
import { TaskSchema } from './task';

export const AnswerSchema = z.object({
	id: z.string(),
	task: z.string(), // Relation to task collection by ID
	content: z.string().optional(),
	audio: z.string().optional(), // Relation to audio collection by ID
	expand: z
		.object({
			task: TaskSchema.optional()
		})
		.optional()
});
