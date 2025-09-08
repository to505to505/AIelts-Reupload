import type { TaskSchema } from '$lib/models/task';
import { z } from 'zod';

export function titleFromPath(
	path: string,
	tasks: z.infer<typeof TaskSchema>[] | null = null
): string {
	switch (true) {
		case path === '/home':
			return 'Home';
		case path === '/progress':
			return 'Progress & review';
		case path === '/profile':
			return 'Profile';
		case path === '/terms':
			return 'Terms of Service & Privacy Policy';
		case path === '/full-section':
			return 'Full section';
		case path === '/subscription':
			return 'Subscription';
		case path === '/email-confirm':
			return 'Email confirmation';

		case /^\/attempts\/[^/]+\/record\/[^/]+(?:\/[^/]+)?$/.test(path): {
			console.log('path', path);
			const taskSlug = path.split('/').at(-2);
			const task = tasks?.find((t) => t.slug === taskSlug);
			return task ? task.title : '<Task>';
		}
		case /^\/attempts\/[^/]+\/result$/.test(path):
			return 'Result';

		// NAVIGATE TOPICS AND TASKS
		case /^\/parts\/\d+\/topics$/.test(path):
			return 'Select a topic';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/tasks$/.test(path):
			return 'Select a task';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/tasks\/[^/]+\/completed$/.test(path):
			return 'Select a task';

		// TOPIC ESSENTIALS
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials$/.test(path):
			return 'Topic essentials';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/main-words$/.test(path):
			return 'Main words';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/adjectives$/.test(path):
			return 'Adjectives';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/phrasal-verbs$/.test(path):
			return 'Phrasal verbs';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/collocations$/.test(path):
			return 'Collocations';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/synonyms-antonyms$/.test(path):
			return 'Synonyms & antonyms';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/expressions-idioms$/.test(path):
			return 'Expressions & idioms';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/sample-answers$/.test(path):
			return 'Sample answers';
		case /^\/parts\/\d+\/[^/]+\/[^/]+\/essentials\/common-mistakes$/.test(path):
			return 'Common mistakes';

		// DEFAULT
		default:
			return '<You are the best!>';
	}
}
