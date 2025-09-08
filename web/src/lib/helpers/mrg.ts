import clsx, { type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * A utility function to combine Tailwind classes, handle conditional classes, and merge conflicting Tailwind classes.
 *
 * @param inputs - A list of class values that can be strings, arrays, objects, or other falsey values.
 * @returns A string of merged class names.
 */
export function mrg(...inputs: ClassValue[]): string {
	return twMerge(clsx(...inputs));
}
