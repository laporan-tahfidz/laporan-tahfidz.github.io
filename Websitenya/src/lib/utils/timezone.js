/**
 * Helper to parse a date string or Date object assumed to be in Asia/Makassar timezone (WITA, UTC+8)
 * @param {string|Date} dateInput
 * @returns {Date}
 */
export function parseMakassarDate(dateInput) {
	if (!dateInput) return new Date();
	if (dateInput instanceof Date) return dateInput;

	let str = String(dateInput).trim();
	// Replace space between date and time with T
	str = str.replace(' ', 'T');

	// If string lacks timezone information (no Z and no +/- offset at end)
	const hasTimezone = /[Zz]|\+\d{2}:?\d{2}|-\d{2}:?\d{2}$/.test(str);
	if (!hasTimezone) {
		str += '+08:00';
	}

	const parsed = new Date(str);
	return isNaN(parsed.getTime()) ? new Date() : parsed;
}

/**
 * Convert a date to Asia/Makassar timezone Date object
 * @param {string|Date} dateString - The date string or Date object to convert
 * @returns {Date} Date object
 */
export function toMakassarTime(dateString) {
	return parseMakassarDate(dateString);
}

/**
 * Format date to Indonesian locale with Asia/Makassar timezone
 * @param {string|Date} dateString - The date string or Date object to format
 * @param {Object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date string
 */
export function formatMakassarTime(dateString, options = {}) {
	const dateObj = parseMakassarDate(dateString);
	const { locale = 'id-ID', ...formatOptions } = options;

	return dateObj.toLocaleString(locale, {
		timeZone: 'Asia/Makassar',
		...formatOptions
	});
}

/**
 * Format date only (without time) in Asia/Makassar timezone
 * @param {string|Date} dateString - The date string or Date object to format
 * @returns {string} Formatted date string
 */
export function formatDateMakassar(dateString) {
	return formatMakassarTime(dateString, {
		day: 'numeric',
		month: 'short',
		year: 'numeric'
	});
}

/**
 * Format time only in Asia/Makassar timezone
 * @param {string|Date} dateString - The date string or Date object to format
 * @returns {string} Formatted time string
 */
export function formatTimeMakassar(dateString) {
	return formatMakassarTime(dateString, {
		hour: '2-digit',
		minute: '2-digit',
		hour12: false
	});
}

/**
 * Format full date and time in Asia/Makassar timezone
 * @param {string|Date} dateString - The date string or Date object to format
 * @returns {string} Formatted date and time string
 */
export function formatDateTimeMakassar(dateString) {
	return formatMakassarTime(dateString, {
		weekday: 'short',
		day: 'numeric',
		month: 'short',
		year: 'numeric',
		hour: '2-digit',
		minute: '2-digit',
		hour12: false
	});
}
