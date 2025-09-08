export function typeFromPath(path: string): 'default' | 'home' | 'prepare' | 'record' {
	if (path === '/home') {
		return 'home';
	} else if (path.endsWith('/prepare')) {
		return 'prepare';
	} else if (path.includes('/record')) {
		return 'record';
	} else {
		return 'default';
	}
}
