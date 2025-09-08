import { z } from 'zod';
import { ResultSchema } from './feedback';

export const UserStatSchema = z.object({
	CompletedAttempts: z.number().int(),
	AverageGrammarScore: z.number(),
	AverageLexicalScore: z.number(),
	AverageCoherenceScore: z.number()
});

export const AttemptStatSchema = z.object({
	id: z.string(),
	bandScore: z.number(),
	grammarScore: z.number(),
	lexicalScore: z.number(),
	coherenceScore: z.number(),
	singlePart: z.boolean(),
	result: ResultSchema.nullable(),
	answered: z.string(),
	created: z.string(),
	seen: z.boolean(),
	tasks: z.array(z.object({ id: z.string(), slug: z.string() }))
});

export const TaskStatSchema = z.object({
	slug: z.string(),
	subhistory: z.array(AttemptStatSchema),
	averageBandScore: z.number(),
	maxBandScore: z.number(),
	minBandScore: z.number()
});

export const TaskStatMapSchema = z.record(z.string(), TaskStatSchema);
