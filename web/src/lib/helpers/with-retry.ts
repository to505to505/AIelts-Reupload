export async function withRetry<T>(fn: () => Promise<T>, retries = 0, delay = 5000): Promise<T> {
	let error;

	if (retries === 0) {
		while (true) {
			try {
				return await fn();
			} catch (e) {
				error = e;
				await new Promise((r) => setTimeout(r, delay));
			}
		}
	} else {
		for (let i = 0; i < retries; i++) {
			try {
				return await fn();
			} catch (e) {
				error = e;
				await new Promise((r) => setTimeout(r, delay));
			}
		}
	}
	throw error;
}
