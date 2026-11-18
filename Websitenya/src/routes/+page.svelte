<script>
	import { onMount, onDestroy } from 'svelte';
	import { browser } from '$app/environment';
	import { getPhpBackendBaseUrl, generateIdempotencyKey } from '$lib/utils.js';
	import { toast } from 'svelte-sonner';
	import jsQR from 'jsqr';
	import { formatDateMakassar } from '$lib/utils/timezone.js';
	import { getNextAchievement } from '$lib/utils/achievement.js';

	let videoRef;
	let canvasRef;
	let stream = null;
	let scanning = $state(false);
	let scannedData = $state(null);
	let errorMessage = $state('');
	let isMobile = $state(false);
	let animationFrameId = null;
	let activeTab = $state('setoran');
	let lastSetoranAchievement = $state(null);
	let lastTesAchievement = $state(null);
	let achievementType = $state('');
	let juz = $state('');
	let halaman = $state('');
	let posisi = $state('');
	let syahadah = $state('');
	let kesalahan = $state('');
	let catatan = $state('');
	let tesJuz = $state('');
	let tesStatus = $state('lancar');
	let submittedJuzList = $state([]);
	let lancarJuzList = $state([]);
	let penguji = $state('');
	let musyrifs = $state([]);
	let syahadahGuruList = $state([]);
	let selectedGuruId = $state('');

	// State variables for Laporan Sabtu
	let murajaahJuz = $state('');
	let murajaahEntries = $state([]);
	let hafalanJuz = $state('');
	let hafalanStartPage = $state('');
	let hafalanEndPage = $state('');
	let hafalanEntries = $state([]);

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
		}, 200);
	}

	async function startScanning() {
		scanning = true;
		errorMessage = '';

		if (browser) {
			// Check if we're on mobile
			isMobile = window.innerWidth <= 768;

			try {
				// Request camera access
				stream = await navigator.mediaDevices.getUserMedia({
					video: { facingMode: 'environment' }
				});

				if (videoRef) {
					videoRef.srcObject = stream;
					videoRef.play();
				}
			} catch (err) {
				console.error('Error accessing camera:', err);
				errorMessage = 'Gagal mengakses kamera. Pastikan izin telah diberikan.';
				scanning = false;
				return;
			}
		}
	}

	function stopScanning() {
		scanning = false;

		if (animationFrameId) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}

		if (stream) {
			stream.getTracks().forEach((track) => track.stop());
			stream = null;
		}
	}

	function scanCode() {
		if (!videoRef || !canvasRef || !scanning) {
			// If any condition is not met, stop scanning
			if (animationFrameId) {
				cancelAnimationFrame(animationFrameId);
				animationFrameId = null;
			}
			return;
		}

		// Check if video has valid dimensions
		if (videoRef.videoWidth === 0 || videoRef.videoHeight === 0) {
			// Video is not ready yet, continue scanning
			animationFrameId = requestAnimationFrame(scanCode);
			return;
		}

		const canvas = canvasRef;
		const context = canvas.getContext('2d');

		// Set canvas dimensions to match video
		canvas.width = videoRef.videoWidth;
		canvas.height = videoRef.videoHeight;

		// Draw video frame to canvas
		context.drawImage(videoRef, 0, 0, canvas.width, canvas.height);

		// Get image data from canvas
		const imageData = context.getImageData(0, 0, canvas.width, canvas.height);

		// Try to decode QR code
		const code = jsQR(imageData.data, imageData.width, imageData.height);

		if (code) {
			// QR code detected
			console.log('QR Code detected:', code.data);

			// Check if the QR code data is a NIK (Indonesian ID number)
			// NIK is typically 16 digits
			const nikPattern = /^\d{16}$/;
			if (nikPattern.test(code.data)) {
				// It's a NIK, fetch student data from backend
				fetchStudentByNik(code.data);
			} else {
				// Treat as other data format
				scannedData = {
					id: Date.now(),
					qr_data: code.data,
					nama: 'Data dari QR: ' + code.data.substring(0, 30) + '...',
					nis: 'N/A',
					kelas: 'N/A',
					status: 'Dari QR'
				};

				scanning = false;

				// Stop the camera stream
				if (stream) {
					stream.getTracks().forEach((track) => track.stop());
					stream = null;
				}

				// Play success sound
				playBeep();

				toast.success('QR Code berhasil discan!');
			}
		} else {
			// Continue scanning
			animationFrameId = requestAnimationFrame(scanCode);
		}
	}

	async function fetchStudentByNik(nik) {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-student-by-nik.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ nik })
			});

			const result = await response.json();

			if (result.success && result.student) {
				// Successfully fetched student data
				scannedData = {
					id: result.student.id,
					nama: result.student.nama_sesuai_kk,
					nis: result.student.nis || 'N/A',
					kelas: result.student.kelas || 'N/A', // assuming there's a kelas field
					status: result.student.status || 'N/A',
					nik: result.student.nik
				};

				scanning = false;

				// Stop the camera stream
				if (stream) {
					stream.getTracks().forEach((track) => track.stop());
					stream = null;
				}

				// Fetch last achievement for this student
				await fetchLastAchievement(result.student.nik);

				// If achievement type is juziyah, fetch the connected musyrif
				if (achievementType === 'juziyah') {
					await fetchConnectedMusyrif(result.student.nik);
				}

				// Play success sound
				playBeep();

				toast.success('Data santri berhasil diambil dari QR Code!');
			} else {
				// Student not found or error occurred
				scannedData = {
					id: Date.now(),
					qr_data: nik,
					nama: 'Santri tidak ditemukan',
					nis: 'N/A',
					kelas: 'N/A',
					status: 'Tidak ditemukan',
					nik: nik
				};

				scanning = false;

				// Stop the camera stream
				if (stream) {
					stream.getTracks().forEach((track) => track.stop());
					stream = null;
				}

				// Play success sound (since it's not an error per se)
				playBeep();

				toast.info('Santri tidak ditemukan di database');
			}
		} catch (error) {
			console.error('Error fetching student by NIK:', error);

			// Handle error case
			scannedData = {
				id: Date.now(),
				qr_data: nik,
				nama: 'Gagal mengambil data',
				nis: 'N/A',
				kelas: 'N/A',
				status: 'Error',
				nik: nik
			};

			scanning = false;

			// Stop the camera stream
			if (stream) {
				stream.getTracks().forEach((track) => track.stop());
				stream = null;
			}

			toast.error('Terjadi kesalahan saat mengambil data santri');
		}
	}

	async function fetchLastAchievement(nik) {
		try {
			// Fetch last setoran achievement
			const setoranResponse = await fetch(`${getPhpBackendBaseUrl()}/get-last-achievement.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ nik, type: 'setoran' })
			});

			const setoranResult = await setoranResponse.json();

			if (setoranResult.success && setoranResult.achievement) {
				// Set the last setoran achievement
				lastSetoranAchievement = setoranResult.achievement;
			} else {
				// No setoran achievement found for this student
				lastSetoranAchievement = null;
			}

			// Auto-determine next achievement target
			applyNextAchievement(lastSetoranAchievement);

			// Fetch last tes achievement
			const tesResponse = await fetch(`${getPhpBackendBaseUrl()}/get-last-tes.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ nik })
			});

			const tesResult = await tesResponse.json();

			if (tesResult.success) {
				lastTesAchievement = tesResult.tes || null;
				submittedJuzList = tesResult.submitted_juz || [];
				lancarJuzList = tesResult.lancar_juz || [];

				const unpassedJuz = submittedJuzList.filter((j) => !lancarJuzList.includes(j));
				if (unpassedJuz.length > 0) {
					const randomIndex = Math.floor(Math.random() * unpassedJuz.length);
					tesJuz = unpassedJuz[randomIndex].toString();
				} else if (submittedJuzList.length > 0) {
					const randomIndex = Math.floor(Math.random() * submittedJuzList.length);
					tesJuz = submittedJuzList[randomIndex].toString();
				} else {
					tesJuz = '';
				}
			} else {
				lastTesAchievement = null;
				submittedJuzList = [];
				lancarJuzList = [];
				tesJuz = '';
			}
		} catch (error) {
			console.error('Error fetching last achievements:', error);
			lastSetoranAchievement = null;
			lastTesAchievement = null;
			submittedJuzList = [];
			lancarJuzList = [];
			tesJuz = '';
			applyNextAchievement(null);
		}
	}

	function applyNextAchievement(last) {
		const next = getNextAchievement(last);
		achievementType = next.type;
		juz = next.juz ? next.juz.toString() : '';
		halaman = next.halaman || '';
		posisi = next.posisi || '';
		syahadah = next.syahadah || '';
	}

	async function handleVideoPlay() {
		if (!videoRef) return;

		// Start scanning once video is playing
		animationFrameId = requestAnimationFrame(scanCode);
	}

	function resetScanner() {
		scannedData = null;
		errorMessage = '';
		activeTab = 'setoran';
		lastSetoranAchievement = null;
		lastTesAchievement = null;
		achievementType = '';
		juz = '';
		halaman = '';
		posisi = '';
		syahadah = '';
		kesalahan = '';
		catatan = '';
		tesJuz = '';
		tesStatus = 'lancar';
		submittedJuzList = [];
		lancarJuzList = [];
		penguji = '';
		selectedGuruId = '';
		applyNextAchievement(null);
	}

	async function fetchConnectedMusyrif(nik) {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-connected-musyrif.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ nik: nik })
			});

			const result = await response.json();

			if (result.success && result.musyrif) {
				// Set the penguji to the connected musyrif's name
				penguji = result.musyrif.nama_lengkap;
			} else {
				// If no connected musyrif, leave the field as is or clear it
				console.log('No connected musyrif found for this student');
			}
		} catch (error) {
			console.error('Error fetching connected musyrif:', error);
		}
	}

	async function fetchSyahadahGuruList() {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-nama-guru.php`);
			if (response.ok) {
				const data = await response.json();
				if (Array.isArray(data)) {
					syahadahGuruList = data;
				}
			}
		} catch (error) {
			console.error('Error fetching syahadah guru list:', error);
		}
	}

	// Update penguji when achievement type changes to juziyah and we have a scanned student
	$effect(() => {
		if (achievementType === 'juziyah' && scannedData?.nik) {
			fetchConnectedMusyrif(scannedData.nik);
		}
		if (achievementType === 'syahadah') {
			if (syahadahGuruList.length === 0) {
				fetchSyahadahGuruList();
			}
		}
	});

	function isFormValid() {
		if (!achievementType) return false;

		switch (achievementType) {
			case 'ziyadah':
				return juz && halaman && kesalahan !== '';
			case 'setengah_juz':
				return juz && posisi && kesalahan !== '';
			case 'juziyah':
				return juz && kesalahan !== '';
			case 'syahadah':
				return syahadah && kesalahan !== '';
			default:
				return false;
		}
	}

	async function submitAchievement() {
		if (!isFormValid()) {
			toast.error('Harap isi semua field yang wajib');
			return;
		}

		// Prepare achievement data
		const achievementData = {
			type: achievementType,
			juz: parseInt(juz),
			kesalahan: parseInt(kesalahan),
			santri_id: scannedData.id,
			nik: scannedData.nik,
			idempotency_key: generateIdempotencyKey() // Add idempotency key
		};

		// Add specific fields based on type
		if (achievementType === 'ziyadah') {
			achievementData.halaman = halaman;
		} else if (achievementType === 'setengah_juz') {
			achievementData.posisi = posisi;
		} else if (achievementType === 'juziyah') {
			achievementData.catatan = catatan;
			achievementData.penguji = penguji;
		} else if (achievementType === 'syahadah') {
			achievementData.syahadah = syahadah;
			achievementData.catatan = catatan;
			achievementData.penguji = penguji;
			achievementData.id_guru = selectedGuruId;
		}

		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/save-achievement.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Idempotency-Key': achievementData.idempotency_key // Add idempotency key to header
				},
				body: JSON.stringify(achievementData)
			});

			const result = await response.json();

			if (result.success) {
				// Update last setoran achievement
				lastSetoranAchievement = { ...achievementData };

				// Apply next achievement values automatically
				applyNextAchievement(lastSetoranAchievement);
				kesalahan = '';
				catatan = '';
				selectedGuruId = '';

				// Play beep sound
				playBeep();

				toast.success('Pencapaian berhasil disimpan');
			} else {
				toast.error(result.message || 'Gagal menyimpan pencapaian');
			}
		} catch (error) {
			console.error('Error saving achievement:', error);
			toast.error('Terjadi kesalahan saat menyimpan pencapaian');
		}
	}

	async function submitTes() {
		if (!tesJuz) {
			toast.error('Harap pilih juz untuk tes');
			return;
		}

		const tesData = {
			juz: parseInt(tesJuz),
			status: tesStatus,
			santri_id: scannedData.id,
			nik: scannedData.nik,
			idempotency_key: generateIdempotencyKey() // Add idempotency key
		};

		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/save-tes.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Idempotency-Key': tesData.idempotency_key // Add idempotency key to header
				},
				body: JSON.stringify(tesData)
			});

			const result = await response.json();

			if (result.success) {
				// Update last tes achievement
				lastTesAchievement = { ...tesData, created_at: new Date().toISOString() };

				// Play beep sound
				playBeep();

				toast.success('Tes berhasil disimpan');

				// Refresh test data and auto-select next pending juz
				await fetchLastAchievement(scannedData.nik);
			} else {
				toast.error(result.message || 'Gagal menyimpan tes');
			}
		} catch (error) {
			console.error('Error saving tes:', error);
			toast.error('Terjadi kesalahan saat menyimpan tes');
		}
	}

	// Add a new entry to murajaah list
	function addMurajaahEntry() {
		if (!murajaahJuz) {
			toast.error('Harap pilih juz untuk Murajaah');
			return;
		}

		const entry = {
			id: Date.now(),
			juz: murajaahJuz
		};

		murajaahEntries = [...murajaahEntries, entry];

		// Reset form field
		murajaahJuz = '';
	}

	// Remove an entry from murajaah list
	function removeMurajaahEntry(id) {
		murajaahEntries = murajaahEntries.filter((entry) => entry.id !== id);
	}

	// Add a new entry to hafalan list
	function addHafalanEntry() {
		if (!hafalanJuz || !hafalanStartPage || !hafalanEndPage) {
			toast.error('Harap lengkapi semua field Hafalan Tidak Lancar');
			return;
		}

		// Validate that start page is not greater than end page
		const startPageNum = parseInt(hafalanStartPage);
		const endPageNum = parseInt(hafalanEndPage);

		if (startPageNum > endPageNum) {
			toast.error('Halaman awal tidak boleh lebih besar dari halaman akhir');
			return;
		}

		const entry = {
			id: Date.now(),
			juz: hafalanJuz,
			startPage: hafalanStartPage,
			endPage: hafalanEndPage
		};

		hafalanEntries = [...hafalanEntries, entry];

		// Reset form fields
		hafalanJuz = '';
		hafalanStartPage = '';
		hafalanEndPage = '';
	}

	// Remove an entry from hafalan list
	function removeHafalanEntry(id) {
		hafalanEntries = hafalanEntries.filter((entry) => entry.id !== id);
	}

	// Submit the Laporan Sabtu form
	async function submitLaporanSabtu() {
		if (murajaahEntries.length === 0 && hafalanEntries.length === 0) {
			toast.error('Harap isi setidaknya satu dari dua bagian: Murajaah atau Hafalan Tidak Lancar');
			return;
		}

		try {
			const reportData = {
				murajaah_entries: murajaahEntries,
				hafalan_entries: hafalanEntries,
				santri_id: scannedData.id,
				nik: scannedData.nik,
				idempotency_key: generateIdempotencyKey() // Add idempotency key
			};

			const response = await fetch(`${getPhpBackendBaseUrl()}/save-laporan-sabtu.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Idempotency-Key': reportData.idempotency_key // Add idempotency key to header
				},
				body: JSON.stringify(reportData)
			});

			const result = await response.json();

			if (result.success) {
				toast.success('Laporan Sabtu berhasil disimpan');

				// Reset form
				murajaahEntries = [];
				hafalanEntries = [];

				// Play beep sound
				playBeep();
			} else {
				toast.error(result.message || 'Gagal menyimpan laporan');
			}
		} catch (error) {
			console.error('Error submitting Laporan Sabtu:', error);
			toast.error('Terjadi kesalahan saat menyimpan laporan');
		}
	}

	async function loadMusyrifs() {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-all-musyrifs-public.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({})
			});
			const result = await response.json();

			if (result.success && result.musyrifs) {
				// Sort musyrifs by name
				musyrifs = result.musyrifs.sort((a, b) => a.nama_lengkap.localeCompare(b.nama_lengkap));
			} else {
				musyrifs = [];
				console.error('Failed to load musyrifs:', result.message || 'Unknown error');
			}
		} catch (error) {
			console.error('Error loading musyrifs:', error);
			musyrifs = [];
		}
	}

	onMount(() => {
		if (browser) {
			isMobile = window.innerWidth <= 768;

			// Load musyrifs when the page mounts
			loadMusyrifs();
			fetchSyahadahGuruList();

			// Listen for resize events to detect mobile/desktop
			const handleResize = () => {
				isMobile = window.innerWidth <= 768;
			};

			window.addEventListener('resize', handleResize);

			onDestroy(() => {
				window.removeEventListener('resize', handleResize);
				stopScanning();
			});
		}
	});
</script>

<div
	class="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4"
>
	<div
		class={isMobile
			? 'w-full max-w-full rounded-xl bg-white p-6 shadow-lg'
			: 'w-full max-w-md rounded-xl bg-white p-6 shadow-lg'}
	>
		<h1 class="mb-6 text-center text-2xl font-bold text-gray-800">Scan QR Code Santri</h1>

		{#if scannedData}
			<div class="mb-6 rounded-lg border border-green-200 bg-green-50 p-4">
				<h2 class="mb-2 text-lg font-semibold text-green-800">Data Santri Ditemukan!</h2>
				<div class="space-y-2">
					<p><span class="font-medium">Nama:</span> {scannedData.nama}</p>
					<p><span class="font-medium">NIS:</span> {scannedData.nis}</p>
					<p><span class="font-medium">Kelas:</span> {scannedData.kelas}</p>
					<p><span class="font-medium">Status:</span> {scannedData.status}</p>
				</div>

				<!-- Tabs for Setoran and Tes -->
				<div class="mt-6">
					<div class="border-b border-gray-200">
						<nav class="-mb-px flex space-x-8">
							<button
								class={`border-b-2 px-1 py-2 text-sm font-medium ${
									activeTab === 'setoran'
										? 'border-blue-500 text-blue-600'
										: 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
								}`}
								onclick={() => (activeTab = 'setoran')}
							>
								Setoran
							</button>
							<button
								class={`border-b-2 px-1 py-2 text-sm font-medium ${
									activeTab === 'tes'
										? 'border-blue-500 text-blue-600'
										: 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
								}`}
								onclick={() => (activeTab = 'tes')}
							>
								Tes
							</button>
							<button
								class={`border-b-2 px-1 py-2 text-sm font-medium ${
									activeTab === 'laporan-sabtu'
										? 'border-blue-500 text-blue-600'
										: 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
								}`}
								onclick={() => (activeTab = 'laporan-sabtu')}
							>
								Laporan Sabtu
							</button>
						</nav>
					</div>

					<!-- Setoran Tab Content -->
					{#if activeTab === 'setoran'}
						<div class="mt-4">
							<!-- Last Achievement -->
							{#if lastSetoranAchievement}
								<div class="mb-4 rounded-lg border border-blue-200 bg-blue-50 p-4">
									<h3 class="mb-2 font-medium text-blue-800">Pencapaian Terakhir</h3>
									<p>Tipe: {lastSetoranAchievement.type}</p>
									{#if lastSetoranAchievement.juz && !isNaN(lastSetoranAchievement.juz)}<p>
											Juz: {lastSetoranAchievement.juz}
										</p>{/if}
									{#if lastSetoranAchievement.halaman}<p>
											Halaman: {lastSetoranAchievement.halaman}
										</p>{/if}
									{#if lastSetoranAchievement.posisi}<p>
											Posisi: {lastSetoranAchievement.posisi}
										</p>{/if}
									{#if lastSetoranAchievement.syahadah}<p>
											Syahadah: {lastSetoranAchievement.syahadah}
										</p>{/if}
									<p>Kesalahan: {lastSetoranAchievement.kesalahan}</p>
									{#if lastSetoranAchievement.catatan}<p>
											Catatan: {lastSetoranAchievement.catatan}
										</p>{/if}
								</div>
							{/if}

							<!-- Add New Achievement Form -->
							<div class="rounded-lg border border-gray-200 bg-white p-4">
								<h3 class="mb-3 font-medium text-gray-800">Tambah Pencapaian Baru</h3>

								<div class="space-y-4">
									<div>
										<label class="mb-1 block text-sm font-medium text-gray-700">Keterangan</label>
										<select
											bind:value={achievementType}
											class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
										>
											<option value="">Pilih Jenis Setoran</option>
											<option value="ziyadah">Ziyadah</option>
											<option value="setengah_juz">Setengah Juz</option>
											<option value="juziyah">Juziyah</option>
											<option value="syahadah">Syahadah</option>
										</select>
									</div>

									{#if achievementType === 'ziyadah'}
										<div class="mb-4 rounded-lg border border-yellow-200 bg-yellow-50 p-4">
											<p class="text-sm font-medium text-yellow-800">
												Catatan Penting: Pastikan santri sudah dites dulu hafalannya dari 1A atau 6A
											</p>
										</div>
										<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Juz</label>
												<select
													bind:value={juz}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Juz</option>
													{#each Array.from({ length: 30 }, (_, i) => i + 1) as num}
														<option value={num.toString()}>{num}</option>
													{/each}
												</select>
											</div>

											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Halaman</label>
												<select
													bind:value={halaman}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Halaman</option>
													{#each Array.from( { length: 10 }, (_, i) => (i + 1).toString() ) as pageNum}
														<option value="{pageNum}A">{pageNum}A</option>
														<option value="{pageNum}B">{pageNum}B</option>
													{/each}
												</select>
											</div>

											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Kesalahan</label
												>
												<select
													bind:value={kesalahan}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Kesalahan</option>
													{#each Array.from({ length: 4 }, (_, i) => i) as num}
														<option value={num.toString()}>{num}</option>
													{/each}
												</select>
											</div>
										</div>
									{/if}

									{#if achievementType === 'setengah_juz'}
										<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Juz</label>
												<select
													bind:value={juz}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Juz</option>
													{#each Array.from({ length: 30 }, (_, i) => i + 1) as num}
														<option value={num.toString()}>{num}</option>
													{/each}
												</select>
											</div>

											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Posisi</label>
												<select
													bind:value={posisi}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Posisi</option>
													<option value="awal">Awal</option>
													<option value="akhir">Akhir</option>
												</select>
											</div>

											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Kesalahan</label
												>
												<select
													bind:value={kesalahan}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Kesalahan</option>
													{#each Array.from({ length: 12 }, (_, i) => i) as num}
														<option value={num.toString()}>{num}</option>
													{/each}
												</select>
											</div>
										</div>
									{/if}

									{#if achievementType === 'juziyah'}
										<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Juz</label>
												<select
													bind:value={juz}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Juz</option>
													{#each Array.from({ length: 30 }, (_, i) => i + 1) as num}
														<option value={num.toString()}>{num}</option>
													{/each}
												</select>
											</div>

											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Kesalahan</label
												>
												<select
													bind:value={kesalahan}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Kesalahan</option>
													{#each Array.from({ length: 21 }, (_, i) => i) as num}
														<option value={num.toString()}>{num}</option>
													{/each}
												</select>
											</div>

											<div class="md:col-span-2">
												<label class="mb-1 block text-sm font-medium text-gray-700"
													>Penguji (Musyrif)</label
												>
												<select
													bind:value={penguji}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Musyrif</option>
													{#each musyrifs as musyrif}
														<option value={musyrif.nama_lengkap}>{musyrif.nama_lengkap}</option>
													{/each}
												</select>
											</div>

											<div class="md:col-span-2">
												<label class="mb-1 block text-sm font-medium text-gray-700">Catatan</label>
												<textarea
													bind:value={catatan}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
													rows="3"
													placeholder="Catatan tambahan"
												></textarea>
											</div>
										</div>
									{/if}

									{#if achievementType === 'syahadah'}
										<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700"
													>Syahadah Ke</label
												>
												<select
													bind:value={syahadah}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Syahadah</option>
													<option value="pertama">Pertama: Juz 30, 29, 1, 2, 3</option>
													<option value="kedua">Kedua: Juz 4, 5, 6, 7, 8</option>
													<option value="ketiga">Ketiga: Juz 9, 10, 11, 12, 13</option>
													<option value="keempat">Keempat: Juz 14, 15, 16, 17, 18</option>
													<option value="kelima">Kelima: Juz 19, 20, 21, 22, 23</option>
													<option value="keenam">Keenam: Juz 24, 25, 26, 27, 28</option>
												</select>
											</div>

											<div>
												<label class="mb-1 block text-sm font-medium text-gray-700">Kesalahan</label
												>
												<select
													bind:value={kesalahan}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Kesalahan</option>
													{#each Array.from({ length: 41 }, (_, i) => i) as num}
														<option value={num}>{num}</option>
													{/each}
												</select>
											</div>

											<div class="md:col-span-3">
												<label class="mb-1 block text-sm font-medium text-gray-700">Penguji</label>
												<select
													bind:value={selectedGuruId}
													onchange={(e) => {
														const selected = syahadahGuruList.find((g) => String(g.id) === e.target.value);
														penguji = selected ? selected.nama : '';
													}}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Penguji</option>
													{#each syahadahGuruList as guru}
														<option value={guru.id}>{guru.nama}</option>
													{/each}
												</select>
											</div>

											<div class="md:col-span-3">
												<label class="mb-1 block text-sm font-medium text-gray-700">Catatan</label>
												<textarea
													bind:value={catatan}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
													rows="3"
													placeholder="Catatan tambahan"
												></textarea>
											</div>
										</div>
									{/if}

									<div class="pt-4">
										<button
											class="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:opacity-50"
											onclick={submitAchievement}
											disabled={!isFormValid()}
										>
											Simpan Pencapaian
										</button>
									</div>
								</div>
							</div>
						</div>
					{/if}

					<!-- Tes Tab Content -->
					{#if activeTab === 'tes'}
						<div class="mt-4">
							<!-- Last Achievement -->
							{#if lastTesAchievement}
								<div class="mb-4 rounded-lg border border-blue-200 bg-blue-50 p-4">
									<h3 class="mb-2 font-medium text-blue-800">Tes Terakhir</h3>
									<p>Juz: {lastTesAchievement.juz}</p>
									<p>
										Status: <span
											class="font-semibold {lastTesAchievement.status === 'tidak_lancar'
												? 'text-red-600'
												: 'text-green-600'}"
											>{lastTesAchievement.status === 'tidak_lancar'
												? 'Tidak Lancar'
												: 'Lancar'}</span
										>
									</p>
									{#if lastTesAchievement.created_at}
										<p>Tanggal: {formatDateMakassar(lastTesAchievement.created_at)}</p>
									{/if}
								</div>
							{/if}

							<div class="rounded-lg border border-gray-200 bg-white p-4">
								<h3 class="mb-3 font-medium text-gray-800">Tes</h3>

								<div class="space-y-4">
									<div>
										<label class="mb-1 block text-sm font-medium text-gray-700">Juz</label>
										<select
											bind:value={tesJuz}
											class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
										>
											<option value="">Pilih Juz</option>
											{#each submittedJuzList as num}
												<option value={num.toString()}
													>Juz {num}{#if lancarJuzList.includes(num)} (Lancar){/if}</option
												>
											{/each}
										</select>
										{#if submittedJuzList.length === 0}
											<p class="mt-1 text-xs text-amber-600">
												Santri belum memiliki riwayat setoran hafalan.
											</p>
										{/if}
									</div>

									<div>
										<label class="mb-1 block text-sm font-medium text-gray-700">Hasil Tes</label>
										<div class="grid grid-cols-2 gap-3">
											<button
												type="button"
												class="flex items-center justify-center gap-2 rounded-lg border px-4 py-2 font-medium transition {tesStatus ===
												'lancar'
													? 'border-green-600 bg-green-50 text-green-700 ring-2 ring-green-500'
													: 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'}"
												onclick={() => (tesStatus = 'lancar')}
											>
												<span class="h-2.5 w-2.5 rounded-full bg-green-500"></span>
												Lancar
											</button>
											<button
												type="button"
												class="flex items-center justify-center gap-2 rounded-lg border px-4 py-2 font-medium transition {tesStatus ===
												'tidak_lancar'
													? 'border-red-600 bg-red-50 text-red-700 ring-2 ring-red-500'
													: 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'}"
												onclick={() => (tesStatus = 'tidak_lancar')}
											>
												<span class="h-2.5 w-2.5 rounded-full bg-red-500"></span>
												Tidak Lancar
											</button>
										</div>
									</div>

									<div class="pt-4">
										<button
											class="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:opacity-50"
											onclick={submitTes}
											disabled={!tesJuz}
										>
											Simpan Tes
										</button>
									</div>
								</div>
							</div>
						</div>
					{/if}

					<!-- Laporan Sabtu Tab Content -->
					{#if activeTab === 'laporan-sabtu'}
						<div class="mt-4">
							<div class="rounded-lg border border-gray-200 bg-white p-4">
								<h3 class="mb-3 font-medium text-gray-800">Laporan Sabtu</h3>

								<div class="space-y-6">
									<!-- Murajaah Section -->
									<div>
										<h4 class="mb-2 font-medium text-gray-700">Murajaah</h4>

										<div class="mb-4 grid grid-cols-1 gap-4 md:grid-cols-2">
											<div>
												<label class="mb-2 block text-sm font-medium text-gray-700">Pilih Juz</label
												>
												<select
													bind:value={murajaahJuz}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Juz</option>
													{#each Array.from({ length: 30 }, (_, i) => i + 1) as num}
														<option value={num}>Juz {num}</option>
													{/each}
												</select>
											</div>

											<div class="flex items-end">
												<button
													type="button"
													class="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
													onclick={addMurajaahEntry}
												>
													Tambahkan ke Daftar
												</button>
											</div>
										</div>

										<!-- Display Murajaah entries -->
										{#if murajaahEntries.length > 0}
											<div class="mt-4">
												<h5 class="mb-2 font-medium text-gray-700">Daftar Murajaah</h5>
												<div class="overflow-x-auto">
													<table class="min-w-full divide-y divide-gray-200">
														<thead class="bg-gray-50">
															<tr>
																<th
																	scope="col"
																	class="px-4 py-2 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
																	>Juz</th
																>
																<th
																	scope="col"
																	class="px-4 py-2 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
																	>Aksi</th
																>
															</tr>
														</thead>
														<tbody class="divide-y divide-gray-200 bg-white">
															{#each murajaahEntries as entry (entry.id)}
																<tr>
																	<td class="px-4 py-2 text-sm whitespace-nowrap text-gray-800"
																		>Juz {entry.juz}</td
																	>
																	<td class="px-4 py-2 text-sm whitespace-nowrap">
																		<button
																			class="text-red-600 hover:text-red-900"
																			onclick={() => removeMurajaahEntry(entry.id)}
																		>
																			Hapus
																		</button>
																	</td>
																</tr>
															{/each}
														</tbody>
													</table>
												</div>
											</div>
										{/if}
									</div>

									<!-- Hafalan Tidak Lancar Section -->
									<div>
										<h4 class="mb-2 font-medium text-gray-700">Hafalan Tidak Lancar</h4>

										<div class="mb-4 grid grid-cols-1 gap-4 md:grid-cols-2">
											<div>
												<label class="mb-2 block text-sm font-medium text-gray-700">Juz</label>
												<select
													bind:value={hafalanJuz}
													class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
												>
													<option value="">Pilih Juz</option>
													{#each Array.from({ length: 30 }, (_, i) => i + 1) as num}
														<option value={num}>Juz {num}</option>
													{/each}
												</select>
											</div>

											<div class="grid grid-cols-2 gap-4">
												<div>
													<label class="mb-2 block text-sm font-medium text-gray-700"
														>Halaman Awal</label
													>
													<div class="flex gap-2">
														<select
															bind:value={hafalanStartPage}
															class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
														>
															<option value="">Pilih Hal</option>
															{#each Array.from( { length: 10 }, (_, i) => (i + 1).toString() ) as pageNum}
																<option value="{pageNum}A">{pageNum}A</option>
																<option value="{pageNum}B">{pageNum}B</option>
															{/each}
														</select>
													</div>
												</div>

												<div>
													<label class="mb-2 block text-sm font-medium text-gray-700"
														>Halaman Akhir</label
													>
													<div class="flex gap-2">
														<select
															bind:value={hafalanEndPage}
															class="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
														>
															<option value="">Pilih Hal</option>
															{#each Array.from( { length: 10 }, (_, i) => (i + 1).toString() ) as pageNum}
																<option value="{pageNum}A">{pageNum}A</option>
																<option value="{pageNum}B">{pageNum}B</option>
															{/each}
														</select>
													</div>
												</div>
											</div>
										</div>

										<div class="flex justify-end">
											<button
												type="button"
												class="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
												onclick={addHafalanEntry}
											>
												Tambahkan ke Daftar
											</button>
										</div>

										<!-- Display Hafalan Tidak Lancar entries -->
										{#if hafalanEntries.length > 0}
											<div class="mt-4">
												<h5 class="mb-2 font-medium text-gray-700">Daftar Hafalan Tidak Lancar</h5>
												<div class="overflow-x-auto">
													<table class="min-w-full divide-y divide-gray-200">
														<thead class="bg-gray-50">
															<tr>
																<th
																	scope="col"
																	class="px-4 py-2 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
																	>Juz</th
																>
																<th
																	scope="col"
																	class="px-4 py-2 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
																	>Rentang Halaman</th
																>
																<th
																	scope="col"
																	class="px-4 py-2 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
																	>Aksi</th
																>
															</tr>
														</thead>
														<tbody class="divide-y divide-gray-200 bg-white">
															{#each hafalanEntries as entry (entry.id)}
																<tr>
																	<td class="px-4 py-2 text-sm whitespace-nowrap text-gray-800"
																		>Juz {entry.juz}</td
																	>
																	<td class="px-4 py-2 text-sm whitespace-nowrap text-gray-800"
																		>{entry.startPage} sampai {entry.endPage}</td
																	>
																	<td class="px-4 py-2 text-sm whitespace-nowrap">
																		<button
																			class="text-red-600 hover:text-red-900"
																			onclick={() => removeHafalanEntry(entry.id)}
																		>
																			Hapus
																		</button>
																	</td>
																</tr>
															{/each}
														</tbody>
													</table>
												</div>
											</div>
										{/if}
									</div>

									<div class="pt-4">
										<button
											class="w-full rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:opacity-50"
											onclick={submitLaporanSabtu}
											disabled={!murajaahJuz && hafalanEntries.length === 0}
										>
											Simpan Laporan Sabtu
										</button>
									</div>
								</div>
							</div>
						</div>
					{/if}
				</div>

				<div class="mt-4 flex justify-center">
					<button
						class="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
						onclick={resetScanner}
					>
						Scan Lagi
					</button>
				</div>
			</div>
		{/if}

		{#if errorMessage}
			<div class="mb-6 rounded-lg border border-red-200 bg-red-50 p-4">
				<p class="text-red-800">{errorMessage}</p>
			</div>
		{/if}

		{#if !scannedData}
			<div class="space-y-6">
				{#if scanning}
					<div class="relative">
						<video
							bind:this={videoRef}
							class="h-auto max-h-[70vh] w-full rounded-lg border border-gray-300"
							autoplay
							muted
							playsinline
							onplay={handleVideoPlay}
						/>
						<!-- Hidden canvas for QR code scanning -->
						<canvas bind:this={canvasRef} class="hidden" />
						<div class="pointer-events-none absolute inset-0 flex items-center justify-center">
							<div
								class="flex h-64 w-64 items-center justify-center rounded-lg border-2 border-blue-500 md:h-48 md:w-48"
							>
								<div
									class="h-48 w-48 animate-pulse rounded-xl border-4 border-dashed border-blue-300 md:h-32 md:w-32"
								></div>
							</div>
						</div>
						<button
							class="absolute top-4 right-4 rounded-full bg-red-600 p-2 text-white hover:bg-red-700"
							onclick={stopScanning}
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-6 w-6"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M6 18L18 6M6 6l12 12"
								/>
							</svg>
						</button>
					</div>
					<p class="text-center text-gray-600">Arahkan kamera ke QR Code santri</p>
				{:else}
					<div
						class="mb-4 flex aspect-square items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-100"
					>
						<div class="p-4 text-center">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="mx-auto h-16 w-16 text-gray-400"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z"
								/>
							</svg>
							<p class="mt-2 text-gray-600">Camera Preview</p>
						</div>
					</div>
					<button
						class="w-full rounded-lg bg-blue-600 px-4 py-3 font-medium text-white transition hover:bg-blue-700"
						onclick={startScanning}
					>
						Mulai Scan QR Code
					</button>
				{/if}
			</div>
		{/if}
	</div>
</div>
