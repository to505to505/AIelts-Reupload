import { z } from 'zod';

export const IntroductionSchema = z.object({
	overview: z.string(),
	typical_questions: z.array(z.string())
});

// KEY WORDS AND PHRASES
export const WordSchema = z.object({
	word: z.string(),
	meaning: z.string(),
	translation: z.string(),
	example: z.string()
});

export const SynonymAntonymSchema = z.object({
	synonym: z.string(),
	antonym: z.string(),
	synonym_translation: z.string(),
	antonym_translation: z.string()
});

export const CollocationSchema = z.object({
	collocation: z.string(),
	meaning: z.string(),
	translation: z.string(),
	example: z.string()
});

export const KeyWordsAndPhrasesSchema = z.object({
	main_words: z.array(WordSchema),
	adjectives: z.array(WordSchema),
	phrasal_verbs: z.array(WordSchema),
	synonyms_antonyms: z.array(SynonymAntonymSchema),
	collocations: z.array(CollocationSchema)
});

// EXPRESSIONS AND IDIOMS
export const ExpressionSchema = z.object({
	expression: z.string(),
	usage: z.string()
});

export const IdiomSchema = z.object({
	idiom: z.string(),
	meaning: z.string()
});

export const ExpressionsAndIdiomsSchema = z.object({
	expressions: z.array(ExpressionSchema),
	idioms: z.array(IdiomSchema)
});

// USAGE TIPS
export const SampleAnswerSchema = z.object({
	question: z.string(),
	answer: z.string()
});

export const CommonMistakeSchema = z.object({
	mistake: z.string(),
	advice: z.string()
});

export const UsageTipsSchema = z.object({
	sample_answers: z.array(SampleAnswerSchema),
	common_mistakes: z.array(CommonMistakeSchema)
});

// TOPIC ESSENTIAL SCHEMA
export const TopicEssentialSchema = z.object({
	introduction: IntroductionSchema,
	key_words_and_phrases: KeyWordsAndPhrasesSchema,
	expressions_and_idioms: ExpressionsAndIdiomsSchema,
	usage_tips: UsageTipsSchema
});
