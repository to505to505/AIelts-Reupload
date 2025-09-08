export const calculateSubscriptionPrice = (
	price: number,
	months: number,
	discount?: number
): [discountedMonthly: number, discountedTotal: number] => {
	if (discount === undefined) discount = 0;
	const discountedMonthlyPrice = discount > 0 ? price - (price * discount) / 100 : price;
	const discountedTotalPrice = discountedMonthlyPrice * months;
	return [discountedMonthlyPrice, discountedTotalPrice];
};
