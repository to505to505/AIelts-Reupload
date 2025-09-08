import { z } from 'zod';
import { ResultSchema } from './feedback';
import { UserSchema } from './user';
import { AnswerSchema } from './answer';

export const AttemptSchema = z.object({
	id: z.string(),
	section: z.enum(['writing', 'speaking']),
	user: z.string(), // Relation to user collection by ID
	answers: z.array(z.string()), // Relation to records collection by ID
	result: ResultSchema.nullable(),
	answered: z.string(),
	created: z.string(),
	updated: z.string(),
	seen: z.boolean(),
	expand: z
		.object({
			user: UserSchema.optional(),
			answers: z.array(AnswerSchema).optional()
		})
		.optional()
});
