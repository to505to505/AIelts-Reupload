import type { z } from 'zod';

import type { AttemptSchema } from '$lib/models/attempt';
import { AttemptStatSchema } from '$lib/models/stat';

import { gradeRound } from './grade-round';

export function parseAttemptToStat(attempt: z.infer<typeof AttemptSchema>) {
	const grammarScore = attempt.result?.feedback?.grammar.criterion.score || 0;
	const lexicalScore = attempt.result?.feedback?.lexical.criterion.score || 0;
	const coherenceScore = attempt.result?.feedback?.coherence.criterion.score || 0;
	const bandScore = (grammarScore + lexicalScore + coherenceScore) / 3;

	return AttemptStatSchema.parse({
		id: attempt.id,
		bandScore: gradeRound(bandScore),
		grammarScore,
		lexicalScore,
		coherenceScore,
		singlePart: attempt.answers.length === 1,
		result: attempt.result,
		answered: attempt.answered,
		created: attempt.created,
		seen: attempt.seen,
		tasks: attempt.expand!.answers!.map((answer) => ({
			id: answer.expand!.task!.id,
			slug: answer.expand!.task!.slug
		}))
	});
}
