import { z } from 'zod';

const CriterionSchema = z.object({
	score: z.number(),
	text: z.string()
});

const GrammarMistakeSchema = z.object({
	wrong: z.string(),
	correct: z.string(),
	type: z.string()
});

const LexicalMistakeSchema = z.object({
	wrong: z.string(),
	correct: z.string()
});

const GrammarSchema = z.object({
	criterion: CriterionSchema,
	mistakes: z.array(GrammarMistakeSchema).nullable()
});

const LexicalSchema = z.object({
	criterion: CriterionSchema,
	mistakes: z.array(LexicalMistakeSchema).nullable()
});

const CoherenceSchema = z.object({
	criterion: CriterionSchema,
	speed: z.number()
});

export const FeedbackSchema = z.object({
	grammar: GrammarSchema,
	lexical: LexicalSchema,
	coherence: CoherenceSchema
});

export const ResultSchema = z.object({
	error: z
		.object({
			code: z.number(),
			message: z.string()
		})
		.optional(),
	feedback: FeedbackSchema.optional()
});
