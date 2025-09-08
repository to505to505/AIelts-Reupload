import { pb } from '$lib/config/pb';
import { subscribeHistory } from '$lib/providers/stat';
import { subscribeUser } from '$lib/providers/user/user.svelte';

export const signIn = async (email: string, password: string) => {
	await pb.collection('users').authWithPassword(email.toLowerCase(), password);
	await Promise.all([subscribeUser(), subscribeHistory()]);
};
