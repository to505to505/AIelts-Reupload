export function gradeRound(value: number): number {
	const integerPart = Math.floor(value);
	const decimalPart = Math.round((value - integerPart) * 10);

	let roundedDecimal;

	if (decimalPart <= 2) {
		roundedDecimal = 0;
	} else if (decimalPart <= 7) {
		roundedDecimal = 5;
	} else if (decimalPart <= 9) {
		roundedDecimal = 0;
		return integerPart + 1;
	}

	return integerPart + roundedDecimal! / 10;
}
