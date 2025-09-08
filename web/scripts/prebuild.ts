// prebuild.ts
import { writeFile, mkdir } from 'fs/promises';
import { join } from 'path';
import { z } from 'zod';

import { TopicSchema } from '../src/lib/models/topic';
import { TaskSchema } from '../src/lib/models/task';

import { parts } from './parts';
import { getAdminPB } from './admin-pb';

async function fetchTopics() {
	const pb = await getAdminPB();
	const topicRecords = await pb.collection('topics').getFullList();
	const topics = z.array(TopicSchema).parse(topicRecords);
	return topics;
}

async function fetchTasks() {
	const pb = await getAdminPB();
	const taskRecords = await pb.collection('tasks').getFullList({ expand: 'topic' });
	const tasks = z.array(TaskSchema).parse(taskRecords);
	return tasks;
}

async function generateTopicEntries() {
	const topics = await fetchTopics();
	const slugs = topics.map((topic) => topic.slug);
	const entries = slugs.flatMap((topicSlug) =>
		parts.map((part) => ({
			part,
			topicSlug
		}))
	);
	return entries;
}

async function generateTaskEntries() {
	const [topics, tasks] = await Promise.all([fetchTopics(), fetchTasks()]);
	const validTopicSlugs = new Set(topics.map((t) => t.slug));

	const validTasks = tasks.filter((task) => {
		const topicSlug = task.expand?.topic?.slug;
		return topicSlug && validTopicSlugs.has(topicSlug);
	});

	const entries = parts.flatMap((part) =>
		topics.flatMap((topic) => {
			const tasksForCombination = validTasks.filter(
				(task) => String(task.part) === String(part) && task.topic === topic.id
			);
			return tasksForCombination.map((task) => ({
				part: String(task.part),
				topicSlug: task.expand!.topic!.slug,
				taskSlug: task.slug
			}));
		})
	);

	return entries;
}

async function writeGeneratedFiles() {
	const generatedDir = join(process.cwd(), 'src', 'lib', 'generated');
	await mkdir(generatedDir, { recursive: true });

	console.log('Получаем topics...');
	const topics = await fetchTopics();

	console.log('Получаем tasks...');
	const tasks = await fetchTasks();

	console.log('Генерируем topicEntries...');
	const topicEntries = await generateTopicEntries();

	console.log('Генерируем taskEntries...');
	const taskEntries = await generateTaskEntries();

	const topicsContent = `// Этот файл сгенерирован автоматически. Не редактируйте его вручную.
import type { Topic } from '$lib/models/topic';
export const topics: Topic[] = ${JSON.stringify(topics, null, 2)};
`;
	const tasksContent = `// Этот файл сгенерирован автоматически. Не редактируйте его вручную.
import type { Task } from '$lib/models/task';
export const tasks: Task[] = ${JSON.stringify(tasks, null, 2)};
`;
	const topicEntriesContent = `// Этот файл сгенерирован автоматически. Не редактируйте его вручную.
export const topicEntries = ${JSON.stringify(topicEntries, null, 2)};
`;
	const taskEntriesContent = `// Этот файл сгенерирован автоматически. Не редактируйте его вручную.
export const taskEntries = ${JSON.stringify(taskEntries, null, 2)};
`;

	await writeFile(join(generatedDir, 'topics.ts'), topicsContent, 'utf-8');
	await writeFile(join(generatedDir, 'tasks.ts'), tasksContent, 'utf-8');
	await writeFile(join(generatedDir, 'topic-entries.ts'), topicEntriesContent, 'utf-8');
	await writeFile(join(generatedDir, 'task-entries.ts'), taskEntriesContent, 'utf-8');

	console.log('Файлы успешно сгенерированы в', generatedDir);
}

writeGeneratedFiles().catch((err) => {
	console.error('Ошибка при генерации файлов:', err);
	process.exit(1);
});
