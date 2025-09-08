import PocketBase from 'pocketbase';
import * as dotenv from 'dotenv';

dotenv.config();

let _pb: PocketBase | null = null;
export async function getAdminPB() {
	if (!_pb) {
		_pb = new PocketBase(process.env.POCKETBASE_URL);
		_pb.beforeSend = async (url, options) => {
			options.timeout = 10000;
			return { url, options };
		};
		await _pb
			.collection('_superusers')
			.authWithPassword(process.env.ADMIN_EMAIL!, process.env.ADMIN_PASSWORD!);
	}
	return _pb;
}
