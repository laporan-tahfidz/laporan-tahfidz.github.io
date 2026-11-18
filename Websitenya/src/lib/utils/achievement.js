export const JUZ_SEQUENCE = [
	30, 29, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28
];

export const PAGES = [
	'1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B',
	'6A', '6B', '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B'
];

export const SYAHADAH_TRIGGER_MAP = {
	3: 'pertama',
	8: 'kedua',
	13: 'ketiga',
	18: 'keempat',
	23: 'kelima',
	28: 'keenam'
};

export const SYAHADAH_NEXT_JUZ_MAP = {
	pertama: 4,
	kedua: 9,
	ketiga: 14,
	keempat: 19,
	kelima: 24,
	keenam: 28
};

/**
 * Calculates the next achievement target based on the last achievement record.
 * @param {Object|null} last - The last achievement object or null if none exists.
 * @returns {{ type: string, juz: number|string, halaman: string, posisi: string, syahadah: string }}
 */
export function getNextAchievement(last) {
	if (!last || !last.type) {
		return { type: 'ziyadah', juz: 30, halaman: '1A', posisi: '', syahadah: '' };
	}

	const currentJuz = last.juz ? parseInt(last.juz, 10) : 30;

	if (last.type === 'ziyadah') {
		const hal = last.halaman || '1A';
		if (hal === '5B') {
			return { type: 'setengah_juz', juz: currentJuz, posisi: 'awal', halaman: '', syahadah: '' };
		} else if (hal === '10B') {
			return { type: 'setengah_juz', juz: currentJuz, posisi: 'akhir', halaman: '', syahadah: '' };
		} else {
			const pageIdx = PAGES.indexOf(hal);
			if (pageIdx !== -1 && pageIdx < PAGES.length - 1) {
				return { type: 'ziyadah', juz: currentJuz, halaman: PAGES[pageIdx + 1], posisi: '', syahadah: '' };
			} else {
				return { type: 'ziyadah', juz: currentJuz, halaman: '1A', posisi: '', syahadah: '' };
			}
		}
	} else if (last.type === 'setengah_juz') {
		if (last.posisi === 'awal') {
			return { type: 'ziyadah', juz: currentJuz, halaman: '6A', posisi: '', syahadah: '' };
		} else if (last.posisi === 'akhir') {
			return { type: 'juziyah', juz: currentJuz, halaman: '', posisi: '', syahadah: '' };
		} else {
			return { type: 'ziyadah', juz: currentJuz, halaman: '6A', posisi: '', syahadah: '' };
		}
	} else if (last.type === 'juziyah') {
		if (SYAHADAH_TRIGGER_MAP[currentJuz]) {
			return { type: 'syahadah', syahadah: SYAHADAH_TRIGGER_MAP[currentJuz], juz: '', halaman: '', posisi: '' };
		} else {
			const seqIdx = JUZ_SEQUENCE.indexOf(currentJuz);
			const nextJuz = (seqIdx !== -1 && seqIdx < JUZ_SEQUENCE.length - 1) ? JUZ_SEQUENCE[seqIdx + 1] : 30;
			return { type: 'ziyadah', juz: nextJuz, halaman: '1A', posisi: '', syahadah: '' };
		}
	} else if (last.type === 'syahadah') {
		const syahadahVal = (last.syahadah || '').toLowerCase();
		let nextJuz = 30;
		if (syahadahVal.includes('pertama') || syahadahVal === '1') nextJuz = 4;
		else if (syahadahVal.includes('kedua') || syahadahVal === '2') nextJuz = 9;
		else if (syahadahVal.includes('ketiga') || syahadahVal === '3') nextJuz = 14;
		else if (syahadahVal.includes('keempat') || syahadahVal === '4') nextJuz = 19;
		else if (syahadahVal.includes('kelima') || syahadahVal === '5') nextJuz = 24;
		else if (syahadahVal.includes('keenam') || syahadahVal === '6') nextJuz = 28;
		return { type: 'ziyadah', juz: nextJuz, halaman: '1A', posisi: '', syahadah: '' };
	}

	return { type: 'ziyadah', juz: 30, halaman: '1A', posisi: '', syahadah: '' };
}
