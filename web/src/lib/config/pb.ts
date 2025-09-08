import { browser } from '$app/environment';
import { PUBLIC_POCKETBASE_URL } from '$env/static/public';
import { UserSchema } from '$lib/models/user';
import { userProvider } from '$lib/providers/user/user.svelte';
import PocketBase, { AsyncAuthStore } from 'pocketbase';

async function initUserProvider() {
	if (!browser) {
		return '';
	}
	const val = localStorage.getItem('pb_auth');
	if (val) {
		userProvider.set(UserSchema.parse(JSON.parse(val).record));
	}
	userProvider.setLoading(false);
	return val ?? '';
}

export const pbInitPromise = initUserProvider();

const store = new AsyncAuthStore({
	save: async (serialized: string) => {
		localStorage.setItem('pb_auth', serialized);
	},
	initial: pbInitPromise,
	clear: async () => {
		localStorage.removeItem('pb_auth');
	}
});

export const pb = new PocketBase(PUBLIC_POCKETBASE_URL, store);
