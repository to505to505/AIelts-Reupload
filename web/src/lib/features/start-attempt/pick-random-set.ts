import { z } from 'zod';

import { TopicSchema } from '$lib/models/topic';
import { TaskSchema } from '$lib/models/task';
import { AttemptSchema } from '$lib/models/attempt';
import { userProvider } from '$lib/providers/user/user.svelte';
import { pb } from '$lib/config/pb';

const pickRandom = <T>(array: T[]): T => array[Math.floor(Math.random() * array.length)];

export const pickRandomFullSection = async () => {
	try {
		const topics = z.array(TopicSchema).parse(await pb.collection('topics').getFullList());
		const topic = pickRandom(topics);

		const user = userProvider.user;
		const freeAttempt =
			user?.verified && (new Date(user.expired) < new Date() || !user.expired || user.credits < 2);

		const [part1Tasks, part2Tasks, part3Tasks] = await Promise.all([
			pb
				.collection('tasks')
				.getFullList({
					filter: `part = 1 ${freeAttempt ? '&& free = true' : ''}`,
					requestKey: 'part1'
				})
				.then((data) => z.array(TaskSchema).parse(data)),
			pb
				.collection('tasks')
				.getFullList({
					filter: `part = 2 ${freeAttempt ? '&& free = true' : `&& topic = '${topic.id}'`}`,
					requestKey: 'part2'
				})
				.then((data) => z.array(TaskSchema).parse(data)),
			pb
				.collection('tasks')
				.getFullList({
					filter: `part = 3 ${freeAttempt ? '&& free = true' : `&& topic = '${topic.id}'`}`,
					requestKey: 'part3'
				})
				.then((data) => z.array(TaskSchema).parse(data))
		]);

		const taskPart1 = pickRandom(part1Tasks);
		const taskPart2 = pickRandom(part2Tasks);
		const taskPart3 = pickRandom(part3Tasks);

		const [answerPart1, answerPart2, answerPart3] = await Promise.all([
			pb
				.collection('answers')
				.create({ task: taskPart1.id, user: pb.authStore.record!.id }, { requestKey: 'answer1' }),
			pb
				.collection('answers')
				.create({ task: taskPart2.id, user: pb.authStore.record!.id }, { requestKey: 'answer2' }),
			pb
				.collection('answers')
				.create({ task: taskPart3.id, user: pb.authStore.record!.id }, { requestKey: 'answer3' })
		]);

		const attemptRecord = await pb.collection('attempts').create(
			{
				user: pb.authStore.record!.id,
				section: 'speaking',
				answers: [answerPart1.id, answerPart2.id, answerPart3.id]
			},
			{ expand: 'answers,answers.task' }
		);

		await pb.collection('users').update(pb.authStore.record!.id, {
			credits: user!.credits - 2
		});

		return AttemptSchema.parse(attemptRecord);
	} catch (error) {
		console.error(error);
		throw error;
	}
};
