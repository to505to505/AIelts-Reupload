import { z } from 'zod';

import { AttemptSchema } from '$lib/models/attempt';

import { statProvider } from './stat.svelte';
import { parseAttemptToStat } from '$lib/helpers/parse-attempt-to-stat';
import { activeAttemptProvider } from '../active-attempt/active-attempt.svelte';
import { pb, pbInitPromise } from '$lib/config/pb';

export const setHistory = (attemptRecords: z.infer<typeof AttemptSchema>[] | null) => {
	if (!attemptRecords) {
		statProvider.history = null;
		return;
	}
	const attempts = z.array(AttemptSchema).parse(attemptRecords);
	statProvider.history = attempts.map(parseAttemptToStat);
	console.log('Setting history:', statProvider.history);
};

const updateHistory = (attemptRecord: z.infer<typeof AttemptSchema> | null) => {
	if (!attemptRecord) return;

	const attempt = AttemptSchema.parse(attemptRecord);
	const newStat = parseAttemptToStat(attempt);

	if (!statProvider.history) {
		statProvider.history = [newStat];
	} else {
		const index = statProvider.history.findIndex((stat) => stat.id === newStat.id);
		if (index !== -1) {
			Object.assign(statProvider.history[index], newStat);
		} else {
			statProvider.history.unshift(newStat);
		}
	}

	console.log('Updated history:', statProvider.history);
};

export async function subscribeHistory() {
	await pbInitPromise;
	await unsubscribeHistory();

	const attemptRecords = await pb.collection('attempts').getFullList({
		filter: `(user = "${pb.authStore.record?.id}") && (answered != null)`,
		expand: 'answers,answers.task',
		sort: '-created'
	});
	const attempts = z.array(AttemptSchema).parse(attemptRecords);
	setHistory(attempts);

	pb.collection('attempts').subscribe(
		'*',
		(e) => {
			console.log('Event attempts received:', e);
			const attempt = AttemptSchema.parse(e.record);

			if (!attempt.answered) {
				activeAttemptProvider.setAttempt(attempt);
			} else {
				updateHistory(attempt);
			}
		},
		{ expand: 'answers,answers.task' }
	);
}

export async function unsubscribeHistory() {
	console.log('Unsubscribing from history');
	activeAttemptProvider.clearAll();
	statProvider.clearAll();
	await pb.collection('attempts').unsubscribe();
}
