export function ieltsToCeft(score: number) {
    if (score >= 9) {
        return 'C2';
    } else if (score >= 7.5) {
        return 'C1';
    } else if (score >= 7) {
        return 'B2';
    } else if (score >= 6) {
        return 'B1';
    } else if (score >= 5) {
        return 'A2';
    } else if (score >= 4) {
        return 'A1';
    } else {
        return 'A1';
    }
}