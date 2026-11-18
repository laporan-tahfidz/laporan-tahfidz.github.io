<script>
	import { onMount } from 'svelte';
	import { format } from 'date-fns';
	import { id } from 'date-fns/locale';
	import { getPhpBackendBaseUrl } from '$lib/utils.js';
	import CustomCalendar from '$lib/components/CustomCalendar.svelte';
	import { Popover, PopoverContent, PopoverTrigger } from '$lib/components/ui/popover/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { toMakassarTime } from '$lib/utils/timezone.js';

	let startDate = $state('');
	let endDate = $state('');
	let reportData = $state(null);
	let isLoading = $state(false);
	let error = $state('');

	// Format date to Indonesian format with Asia/Makassar timezone
	const formatDateToIndonesian = (dateString) => {
		if (!dateString) return '';
		const date = toMakassarTime(dateString);
		return format(date, 'EEEE, dd MMMM yyyy', { locale: id });
	};

	// Calculate the number of juz from the last hafalan
	// According to the specification: if hafalan terakhir is juz 30, it's 1 juz; if juz 29, it's 2 juz; if juz 1, it's 3 juz; etc.
	const calculateJumlahHafalan = (lastHafalanJuz) => {
		if (!lastHafalanJuz) return 0;

		// The sequence is: 30 (1 juz), 29 (2 juz), 1 (3 juz), 2 (4 juz), 3 (5 juz), ..., 28 (30 juz)
		const sequence = [30, 29];
		for (let i = 1; i <= 28; i++) {
			sequence.push(i);
		}

		const position = sequence.indexOf(lastHafalanJuz);
		if (position === -1) return 0;

		// Return the number of juz from the beginning of the sequence (position + 1)
		return position + 1;
	};

	// Calculate achievement during the period
	const calculateCapaianHafalan = (achievements, startDate, endDate) => {
		if (!achievements || !startDate || !endDate) return 0;

		const start = new Date(startDate);
		const end = new Date(endDate);

		// Count ziyadah achievements during the period
		return achievements.filter((a) => {
			const achievementDate = new Date(a.created_at);
			return a?.type === 'ziyadah' && achievementDate >= start && achievementDate <= end;
		}).length;
	};

	// Get the last achievement of a specific type before the end date
	const getLastAchievementOfType = (achievements, type, endDate) => {
		if (!achievements || !type || !endDate) return null;

		const end = new Date(endDate);

		// Filter achievements of the specified type that happened before or on the end date
		const filtered = achievements.filter((a) => {
			const achievementDate = new Date(a?.created_at);
			return a?.type === type && achievementDate <= end;
		});

		// Return the most recent one
		return filtered.length > 0 ? filtered[0] : null;
	};

	// Get lancar tes entries for a student during the period
	const getLancarDuringPeriod = (tesEntries, startDate, endDate) => {
		if (!tesEntries || !startDate || !endDate) return [];

		const start = new Date(startDate);
		const end = new Date(endDate);

		const lancarSet = new Set(); // Use Set to avoid duplicates

		tesEntries.forEach((entry) => {
			const entryDate = new Date(entry?.created_at);
			if (entryDate >= start && entryDate <= end) {
				const status = entry?.status || 'lancar';
				if (status === 'lancar' || status !== 'tidak_lancar') {
					if (entry?.juz) {
						lancarSet.add(`Juz ${entry.juz}`);
					}
				}
			}
		});

		return Array.from(lancarSet);
	};

	// Get tidak lancar tes entries for a student during the period
	const getTidakLancarDuringPeriod = (tesEntries, startDate, endDate) => {
		if (!tesEntries || !startDate || !endDate) return [];

		const start = new Date(startDate);
		const end = new Date(endDate);

		const tidakLancarSet = new Set(); // Use Set to avoid duplicates

		tesEntries.forEach((entry) => {
			const entryDate = new Date(entry?.created_at);
			if (entryDate >= start && entryDate <= end) {
				if (entry?.status === 'tidak_lancar') {
					if (entry?.juz) {
						tidakLancarSet.add(`Juz ${entry.juz}`);
					}
				}
			}
		});

		return Array.from(tidakLancarSet);
	};

	// Get the last achievement of any type before the end date
	const getLastAnyAchievement = (achievements, endDate) => {
		if (!achievements || !endDate) return null;

		const end = new Date(endDate);

		// Filter achievements that happened before or on the end date
		const filtered = achievements.filter((a) => {
			const achievementDate = new Date(a?.created_at);
			return achievementDate <= end;
		});

		// Return the most recent one
		return filtered.length > 0 ? filtered[0] : null;
	};

	// Fetch report data from backend
	const fetchReportData = async () => {
		if (!startDate || !endDate) {
			error = 'Silakan pilih rentang tanggal terlebih dahulu';
			return;
		}

		// Validate date format
		if (isNaN(Date.parse(startDate)) || isNaN(Date.parse(endDate))) {
			error = 'Format tanggal tidak valid';
			return;
		}

		isLoading = true;
		error = '';

		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-report-data.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					start_date: dateToISO(startDate),
					end_date: dateToISO(endDate)
				})
			});

			const result = await response.json();

			if (result.success) {
				reportData = result.data;
				playBeep(); // Play beep when data is successfully loaded
			} else {
				error = result.message || 'Gagal mengambil data laporan';
			}
		} catch (err) {
			console.error('Error fetching report data:', err);
			error = 'Terjadi kesalahan saat mengambil data laporan';
		} finally {
			isLoading = false;
		}
	};

	// Play beep sound function
	function playBeep() {
		const audioContext = new (window.AudioContext || window.webkitAudioContext)();
		const oscillator = audioContext.createOscillator();
		const gainNode = audioContext.createGain();

		oscillator.connect(gainNode);
		gainNode.connect(audioContext.destination);

		oscillator.frequency.value = 800;
		oscillator.type = 'square';

		gainNode.gain.value = 0.3;

		oscillator.start();
		setTimeout(() => {
			oscillator.stop();
			audioContext.close();
		}, 200);
	}

	// Print the report
	const printReport = () => {
		playBeep(); // Play beep when printing
		setTimeout(() => {
			window.print();
		}, 250);
	};

	// Format date for display
	const formatDisplayDate = (dateString) => {
		if (!dateString) return '';
		const date = new Date(dateString);
		return format(date, 'dd/MM/yyyy');
	};

	// Convert date to ISO string for API calls
	const dateToISO = (dateString) => {
		if (!dateString) return '';
		const date = new Date(dateString);
		return date.toISOString().split('T')[0];
	};
</script>

<div class="container mx-auto max-w-6xl p-4">
	<h1 class="mb-6 text-center text-2xl font-bold">Laporan Perkembangan Tahfidz Santri</h1>

	<div class="mb-6 rounded-lg bg-white p-6 shadow-md">
		<div class="mb-4 grid grid-cols-1 gap-4 md:grid-cols-2">
			<div>
				<label class="mb-1 block text-sm font-medium text-gray-700">Tanggal Mulai</label>
				<Popover>
					<PopoverTrigger asChild>
						<Button
							variant="outline"
							class="w-full justify-start rounded-lg border border-gray-300 px-3 py-2 text-left font-normal focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="mr-2 h-4 w-4 opacity-70"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
								/>
							</svg>
							{startDate ? format(new Date(startDate), 'dd/MM/yyyy') : 'Pilih tanggal...'}
						</Button>
					</PopoverTrigger>
					<PopoverContent class="z-[100] w-auto p-0">
						<CustomCalendar
							selectedDate={startDate}
							onDateSelect={(date) => {
								// Format date to YYYY-MM-DD in local timezone
								const year = date.getFullYear();
								const month = String(date.getMonth() + 1).padStart(2, '0');
								const day = String(date.getDate()).padStart(2, '0');
								startDate = `${year}-${month}-${day}`;

								// Close the popover after selection
								setTimeout(() => {
									const activeElement = document.activeElement;
									if (activeElement instanceof HTMLElement) {
										activeElement.blur();
									}
								}, 100);
							}}
						/>
					</PopoverContent>
				</Popover>
			</div>
			<div>
				<label class="mb-1 block text-sm font-medium text-gray-700">Tanggal Selesai</label>
				<Popover>
					<PopoverTrigger asChild>
						<Button
							variant="outline"
							class="w-full justify-start rounded-lg border border-gray-300 px-3 py-2 text-left font-normal focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="mr-2 h-4 w-4 opacity-70"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
								/>
							</svg>
							{endDate ? format(new Date(endDate), 'dd/MM/yyyy') : 'Pilih tanggal...'}
						</Button>
					</PopoverTrigger>
					<PopoverContent class="z-[100] w-auto p-0">
						<CustomCalendar
							selectedDate={endDate}
							onDateSelect={(date) => {
								// Format date to YYYY-MM-DD in local timezone
								const year = date.getFullYear();
								const month = String(date.getMonth() + 1).padStart(2, '0');
								const day = String(date.getDate()).padStart(2, '0');
								endDate = `${year}-${month}-${day}`;

								// Close the popover after selection
								setTimeout(() => {
									const activeElement = document.activeElement;
									if (activeElement instanceof HTMLElement) {
										activeElement.blur();
									}
								}, 100);
							}}
						/>
					</PopoverContent>
				</Popover>
			</div>
		</div>

		<div class="flex flex-col gap-3 sm:flex-row">
			<button
				class="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:opacity-50 sm:w-auto"
				onclick={fetchReportData}
				disabled={isLoading}
			>
				{#if isLoading}
					Memuat...
				{:else}
					Tampilkan Laporan
				{/if}
			</button>

			{#if reportData}
				<button
					class="w-full rounded-lg bg-green-600 px-4 py-2 font-medium text-white transition hover:bg-green-700 sm:w-auto"
					onclick={printReport}
				>
					Cetak Laporan
				</button>
			{/if}
		</div>

		{#if error}
			<div class="mt-4 rounded-lg bg-red-100 p-3 text-red-700">
				{error}
			</div>
		{/if}
	</div>

	<!-- Report Content -->
	{#if reportData}
		<div class="print-container">
			<div class="mb-6 rounded-lg bg-white p-6 shadow-md">
				<h2 class="mb-4 text-center text-xl font-bold">
					LAPORAN PERKEMBANGAN TAHFIDZ SANTRI MADRASAH AL-QURAN BAITUL IZZAH
				</h2>

				<div class="mb-6 text-center">
					<p>
						Tanggal: {formatDateToIndonesian(startDate)} sampai {formatDateToIndonesian(endDate)}
					</p>
				</div>

				{#each reportData.musyrifs as musyrif}
					<div class="mb-8">
						<h3 class="mb-4 text-lg font-bold">MUSYRIF : {musyrif.nama.toUpperCase()}</h3>

						<div class="overflow-x-auto">
							<table class="min-w-full divide-y divide-gray-200 border border-gray-300">
								<thead class="bg-gray-50">
									<tr>
										<th
											class="px-4 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Nama</th
										>
										<th
											class="px-4 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Hafalan Terakhir</th
										>
										<th
											class="px-4 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Capaian Hafalan</th
										>
										<!-- <th
											class="px-4 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Jumlah Hafalan</th
										> -->
										<th
											class="px-4 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Keterangan</th
										>
										<th
											class="px-4 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Lancar</th
										>
										<th
											class="px-4 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Tidak Lancar</th
										>
									</tr>
								</thead>
								<tbody class="divide-y divide-gray-200 bg-white">
									{#each musyrif.students as student, index}
										<tr>
											<td class="px-4 py-3 text-sm font-medium whitespace-nowrap text-gray-900"
												>{student.nama_panggilan || student.nama_sesuai_kk} ({student.tahun_masuk})</td
											>
											<td class="px-4 py-3 text-sm whitespace-nowrap text-gray-500">
												{#if student.last_hafalan}
													Juz {student.last_hafalan?.juz}, {student.last_hafalan?.halaman ||
														student.last_hafalan?.posisi ||
														student.last_hafalan?.syahadah ||
														''}
												{:else}
													-
												{/if}
											</td>
											<td class="px-4 py-3 text-sm whitespace-nowrap text-gray-500">
												{calculateCapaianHafalan(student.achievements, startDate, endDate)} halaman
											</td>
											<!-- <td class="px-4 py-3 text-sm whitespace-nowrap text-gray-500">
												{calculateJumlahHafalan(student.last_hafalan?.juz || 0)} juz
											</td> -->
											<td class="px-4 py-3 text-sm whitespace-nowrap text-gray-500">
												{#if student.last_hafalan}
													{#if student.last_hafalan?.type === 'ziyadah'}Ziyadah
													{:else if student.last_hafalan?.type === 'setengah_juz'}Setengah Juz
													{:else if student.last_hafalan?.type === 'juziyah'}Juziyah
													{:else if student.last_hafalan?.type === 'syahadah'}Syahadah
													{:else}-{/if}
												{:else}
													-
												{/if}
											</td>
											<td class="px-4 py-3 text-sm text-gray-500">
												{#if getLancarDuringPeriod(student.tes_entries, startDate, endDate).length > 0}
													{#each getLancarDuringPeriod(student.tes_entries, startDate, endDate) as lancar, i}
														{lancar}{#if i < getLancarDuringPeriod(student.tes_entries, startDate, endDate).length - 1}<br
															/>{/if}
													{/each}
												{:else}
													-
												{/if}
											</td>
											<td class="px-4 py-3 text-sm text-gray-500">
												{#if getTidakLancarDuringPeriod(student.tes_entries, startDate, endDate).length > 0}
													{#each getTidakLancarDuringPeriod(student.tes_entries, startDate, endDate) as tidakLancar, i}
														{tidakLancar}{#if i < getTidakLancarDuringPeriod(student.tes_entries, startDate, endDate).length - 1}<br
															/>{/if}
													{/each}
												{:else}
													-
												{/if}
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	@media print {
		body {
			background-color: white;
			font-size: 12px;
		}

		.print-container {
			width: 100%;
			margin: 0;
			padding: 0;
			box-shadow: none;
			font-size: 12px;
		}

		button {
			display: none;
		}

		.no-print {
			display: none;
		}

		table {
			font-size: 10px;
			width: 100%;
		}

		th,
		td {
			padding: 4px;
			text-align: left;
			border: 1px solid #000;
		}

		.page-break {
			page-break-before: always;
		}
	}
</style>
