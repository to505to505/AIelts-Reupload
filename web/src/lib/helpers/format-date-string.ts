export const formatDateString = (dataStr: string): string => {
	const date = new Date(dataStr);
	return (
		date.toLocaleDateString('ru-RU', {
			day: '2-digit',
			month: '2-digit',
			year: 'numeric'
		}) +
		' ' +
		date.toLocaleTimeString('ru-RU', {
			hour: '2-digit',
			minute: '2-digit'
		})
	);
};
