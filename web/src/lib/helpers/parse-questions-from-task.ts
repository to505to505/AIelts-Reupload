import z from 'zod';
import type { TaskSchema } from '$lib/models/task';

export function parseQuestionsFromTask(task: z.infer<typeof TaskSchema>) {
	if (task.part === 2) {
		return [task.questions];
	} else {
		const parser = new DOMParser();
		const doc = parser.parseFromString(task.questions, 'text/html');
		return Array.from(doc.querySelectorAll('li')).map((li) => li.textContent!.trim());
	}
}
