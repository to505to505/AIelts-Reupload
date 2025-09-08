import { pb, pbInitPromise } from '$lib/config/pb';
import { UserSchema } from '$lib/models/user';
import { z } from 'zod';

// REACTIVE PROVIDER CLASS
class UserProvider {
	user: z.infer<typeof UserSchema> | null = $state(null);
	loading = $state(true);

	subscribed = $derived(
		this.user?.expired && new Date(this.user.expired) > new Date() && this.user.credits > 0
	);

	set(user: z.infer<typeof UserSchema> | null) {
		this.user = user;
	}
	setLoading(loading: boolean) {
		this.loading = loading;
	}

	clearAll() {
		this.set(null);
		this.setLoading(false);
	}
}
export const userProvider = new UserProvider();

// SSE REACTIVE FLOW
export async function subscribeUser() {
	await pbInitPromise;
	await unsubscribeUser();

	console.log('Subscribing to user', pb.authStore.record?.id);
	if (!pb.authStore.record) return;

	userProvider.set(UserSchema.parse(pb.authStore.record));

	pb.collection('users').subscribe(pb.authStore.record.id, async (e) => {
		userProvider.setLoading(true);
		console.log('Event user recieved:', e);

		console.log('BEFORE', pb.authStore.record);
		const authResponse = await pb.collection('users').authRefresh();
		pb.authStore.save(authResponse.token, authResponse.record);
		userProvider.set(UserSchema.parse(pb.authStore.record));
		console.log('AFTER', pb.authStore.record);
		userProvider.setLoading(false);
	});
}

export async function unsubscribeUser() {
	console.log('Unsubscribing from user: ', pb.authStore.record?.id);
	userProvider.clearAll();
	if (!pb.authStore.record) return;
	await pb.collection('users').unsubscribe(pb.authStore.record.id);
}
