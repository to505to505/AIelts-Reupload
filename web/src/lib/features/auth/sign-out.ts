import { pb } from "$lib/config/pb";
import { unsubscribeHistory } from "$lib/providers/stat";
import { unsubscribeUser } from "$lib/providers/user/user.svelte";

export const signOut = async () => {
	await Promise.all([unsubscribeUser(), unsubscribeHistory()]);
	pb.authStore.clear();
};
