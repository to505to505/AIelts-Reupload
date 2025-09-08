import { z } from 'zod';

import { AttemptStatSchema, UserStatSchema } from '$lib/models/stat';

export const getUserStat = (history: z.infer<typeof AttemptStatSchema>[] | null) => {
	const sucessHistory = history?.filter((a) => a.result?.feedback && !a.singlePart);
	const completedAttempts = sucessHistory ? sucessHistory.length : 0;

	let totalGrammar = 0;
	let totalLexical = 0;
	let totalCoherence = 0;

	if (sucessHistory) {
		for (const attempt of sucessHistory) {
			totalGrammar += attempt.grammarScore;
			totalLexical += attempt.lexicalScore;
			totalCoherence += attempt.coherenceScore;
		}
	}

	const avgGrammar = completedAttempts > 0 ? totalGrammar / completedAttempts : 0;
	const avgLexical = completedAttempts > 0 ? totalLexical / completedAttempts : 0;
	const avgCoherence = completedAttempts > 0 ? totalCoherence / completedAttempts : 0;

	const userStat = {
		CompletedAttempts: completedAttempts,
		AverageGrammarScore: avgGrammar,
		AverageLexicalScore: avgLexical,
		AverageCoherenceScore: avgCoherence
	};

	return UserStatSchema.parse(userStat);
};
