import { pb } from '$lib/config/pb';
import { AttemptSchema } from '$lib/models/attempt';
import { TaskSchema } from '$lib/models/task';
import { userProvider } from '$lib/providers/user/user.svelte';

export const startAttemptByTask = async (taskId: string) => {
	try {
		const user = userProvider.user;
		const freeAttempt =
			user?.verified && (new Date(user.expired) < new Date() || !user.expired || user.credits < 2);

		const task = TaskSchema.parse(await pb.collection('tasks').getOne(taskId));

		if (freeAttempt) {
			const freeTask = await pb
				.collection('tasks')
				.getFirstListItem(`part = ${task.part} ${freeAttempt ? '&& free = true' : ''}`);
			taskId = freeTask.id;
		}

		const answerRecord = await pb.collection('answers').create({
			user: pb.authStore.record?.id,
			task: taskId
		});
		const attemptRecord = await pb.collection('attempts').create(
			{
				user: pb.authStore.record?.id,
				section: 'speaking',
				answers: [answerRecord.id]
			},
			{ expand: 'answers,answers.task' }
		);

		await pb.collection('users').update(pb.authStore.record!.id, {
			credits: user!.credits - 1
		});

		return AttemptSchema.parse(attemptRecord);
	} catch (error) {
		console.error(error);
		throw error;
	}
};
