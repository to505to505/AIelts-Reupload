export const calculateBandScore = (
	grammarScore: number,
	lexicalScore: number,
	coherenceScore: number
): number => Math.round(((grammarScore + lexicalScore + coherenceScore) / 3) * 2) / 2;
