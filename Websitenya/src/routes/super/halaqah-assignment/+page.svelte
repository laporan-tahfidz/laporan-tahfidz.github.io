<script>
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { getPhpBackendBaseUrl } from '$lib/utils.js';
	import { toast } from 'svelte-sonner';

	// State variables
	let musyrifs = $state([]);
	let students = $state([]);
	let selectedMusyrif = $state(null);
	let availableStudents = $state([]); // Students not assigned to the selected musyrif
	let assignedStudents = $state([]); // Students assigned to the selected musyrif
	let isLoading = $state(true);
	let searchQuery = $state('');

	onMount(async () => {
		await loadMusyrifs();
		await loadStudents();
		isLoading = false;
	});

	async function loadMusyrifs() {
		try {
			const token = localStorage.getItem('tokenSuper') || '';

			const response = await fetch(`${getPhpBackendBaseUrl()}/get-musyrif-with-students.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ token })
			});

			const result = await response.json();

			if (result.success) {
				musyrifs = result.data || [];
			} else {
				toast.error(result.message || 'Gagal memuat data musyrif');
			}
		} catch (error) {
			console.error('Error loading musyrifs:', error);
			toast.error('Terjadi kesalahan saat memuat data musyrif');
		}
	}

	async function loadStudents() {
		try {
			const token = localStorage.getItem('tokenSuper') || '';

			const response = await fetch(`${getPhpBackendBaseUrl()}/get-students-for-halaqah.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ token })
			});

			const result = await response.json();

			if (result.success) {
				students = result.data || [];
			} else {
				toast.error(result.message || 'Gagal memuat data santri');
			}
		} catch (error) {
			console.error('Error loading students:', error);
			toast.error('Terjadi kesalahan saat memuat data santri');
		}
	}

	async function selectMusyrif(musyrif) {
		selectedMusyrif = musyrif;

		// Load students assigned to this musyrif
		try {
			const token = localStorage.getItem('tokenSuper') || '';

			const response = await fetch(`${getPhpBackendBaseUrl()}/get-musyrif-students.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					token,
					musyrif_id: musyrif.id
				})
			});

			const result = await response.json();

			if (result.success) {
				assignedStudents = result.data || [];

				// Calculate available students (those not assigned to this musyrif)
				const assignedNiks = new Set(assignedStudents.map((s) => s.nik));
				availableStudents = students.filter((s) => !assignedNiks.has(s.nik));
			} else {
				toast.error(result.message || 'Gagal memuat data santri musyrif');
			}
		} catch (error) {
			console.error('Error loading musyrif students:', error);
			toast.error('Terjadi kesalahan saat memuat data santri musyrif');
		}
	}

	function resetSelection() {
		selectedMusyrif = null;
		assignedStudents = [];
		availableStudents = [];
		searchQuery = '';
	}

	// Filter available students based on search query
	function getFilteredAvailableStudents() {
		if (!searchQuery.trim()) {
			return availableStudents;
		}

		const query = searchQuery.toLowerCase();
		return availableStudents.filter(
			(student) => student.nama.toLowerCase().includes(query) || student.nik.includes(query)
		);
	}

	// Drag and drop functions
	function handleDragStart(e, student, source) {
		e.dataTransfer.setData('text/plain', JSON.stringify({ student, source }));
	}

	function handleDragOver(e) {
		e.preventDefault();
	}

	async function handleDrop(e, target) {
		e.preventDefault();

		if (!selectedMusyrif) {
			toast.error('Silakan pilih musyrif terlebih dahulu');
			return;
		}

		const data = JSON.parse(e.dataTransfer.getData('text/plain'));
		const { student, source } = data;

		// Move student from source to target
		if (source === 'available' && target === 'assigned') {
			// Move from available to assigned
			availableStudents = availableStudents.filter((s) => s.nik !== student.nik);
			assignedStudents = [...assignedStudents, student];
		} else if (source === 'assigned' && target === 'available') {
			// Move from assigned to available
			assignedStudents = assignedStudents.filter((s) => s.nik !== student.nik);
			availableStudents = [...availableStudents, student];
		}

		// Save the changes to the backend
		await saveMusyrifAssignments();
	}

	async function saveMusyrifAssignments() {
		if (!selectedMusyrif) return;

		const token = localStorage.getItem('tokenSuper') || '';

		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/assign-students-to-musyrif.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					token,
					musyrif_id: selectedMusyrif.id,
					student_niks: assignedStudents.map((s) => s.nik)
				})
			});

			const result = await response.json();

			if (result.success) {
				toast.success('Anggota musyrif berhasil diperbarui');

				// Update the musyrif's assigned count in the list
				const updatedMusyrifs = musyrifs.map((m) =>
					m.id === selectedMusyrif.id
						? { ...m, assigned_students_count: assignedStudents.length }
						: m
				);
				musyrifs = updatedMusyrifs;

				// Play beep sound on success
				playBeep();
			} else {
				toast.error(result.message || 'Gagal memperbarui anggota musyrif');
			}
		} catch (error) {
			console.error('Error saving musyrif assignments:', error);
			toast.error('Terjadi kesalahan saat menyimpan anggota musyrif');
		}
	}

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
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
	<div class="mx-auto max-w-7xl">
		<header class="mb-6 rounded-xl bg-white p-6 shadow">
			<div class="flex items-center justify-between">
				<h1 class="text-2xl font-bold text-gray-800">Manajemen Musyrif Tahfidz</h1>
			</div>
		</header>

		{#if isLoading}
			<div class="rounded-xl bg-white p-8 text-center shadow">
				<div class="mx-auto h-12 w-12 animate-spin rounded-full border-b-2 border-blue-600"></div>
				<p class="mt-4 text-gray-600">Memuat data...</p>
			</div>
		{:else}
			<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
				<!-- Left column: Musyrif list -->
				<div class="lg:col-span-1">
					<div class="rounded-xl bg-white p-6 shadow">
						<h2 class="mb-4 text-xl font-semibold text-gray-800">Daftar Musyrif</h2>

						<div class="max-h-[600px] space-y-3 overflow-y-auto pr-2">
							{#each musyrifs as musyrif (musyrif.id)}
								<div
									class={`cursor-pointer rounded-lg border p-4 transition ${
										selectedMusyrif && selectedMusyrif.id === musyrif.id
											? 'border-blue-500 bg-blue-50'
											: 'border-gray-200 hover:bg-gray-50'
									}`}
									onclick={() => selectMusyrif(musyrif)}
								>
									<div class="flex items-start justify-between">
										<div>
											<h3 class="font-medium text-gray-800">{musyrif.nama}</h3>
											<p class="mt-1 text-sm text-gray-600">
												Jumlah Santri: {musyrif.assigned_students_count}
											</p>
										</div>
									</div>
								</div>
							{:else}
								<div class="text-center py-8 text-gray-500">Belum ada musyrif</div>
							{/each}
						</div>
					</div>
				</div>

				<!-- Right column: Student assignment -->
				<div class="lg:col-span-2">
					{#if selectedMusyrif}
						<div class="rounded-xl bg-white p-6 shadow">
							<div class="mb-6 flex items-center justify-between">
								<h2 class="text-xl font-semibold text-gray-800">
									Anggota Musyrif: {selectedMusyrif.nama}
								</h2>
								<p class="text-gray-600">
									Jumlah Santri: {assignedStudents.length}
								</p>
							</div>

							<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
								<!-- Available students (left side) -->
								<div>
									<div class="mb-3 flex items-center justify-between">
										<h3 class="font-medium text-gray-800">Santri Tersedia</h3>
										<input
											type="text"
											bind:value={searchQuery}
											placeholder="Cari santri..."
											class="rounded-md border border-gray-300 px-3 py-1 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
										/>
									</div>
									<div
										class="min-h-[400px] overflow-y-auto rounded-lg border border-gray-200 bg-gray-50 p-3"
										ondragover={handleDragOver}
										ondrop={(e) => handleDrop(e, 'available')}
									>
										{#if getFilteredAvailableStudents().length > 0}
											{#each getFilteredAvailableStudents() as student (student.nik)}
												<div
													class="mb-2 flex cursor-move items-center justify-between rounded-lg border border-gray-200 bg-white p-3 hover:bg-gray-50"
													draggable="true"
													ondragstart={(e) => handleDragStart(e, student, 'available')}
												>
													<div>
														<div>{student.nama}</div>
														<div class="text-xs text-gray-500">NIK: {student.nik}</div>
													</div>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														class="h-5 w-5 text-gray-400"
														fill="none"
														viewBox="0 0 24 24"
														stroke="currentColor"
													>
														<path
															stroke-linecap="round"
															stroke-linejoin="round"
															stroke-width="2"
															d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"
														/>
													</svg>
												</div>
											{/each}
										{:else}
											<div class="py-8 text-center text-gray-500">
												{#if searchQuery}
													Tidak ditemukan santri dengan kata kunci "{searchQuery}"
												{:else}
													Tidak ada santri tersedia
												{/if}
											</div>
										{/if}
									</div>
								</div>

								<!-- Assigned students (right side) -->
								<div>
									<h3 class="mb-3 font-medium text-gray-800">Santri Ditugaskan</h3>
									<div
										class="min-h-[400px] overflow-y-auto rounded-lg border border-green-200 bg-green-50 p-3"
										ondragover={handleDragOver}
										ondrop={(e) => handleDrop(e, 'assigned')}
									>
										{#if assignedStudents.length > 0}
											{#each assignedStudents as student (student.nik)}
												<div
													class="mb-2 flex cursor-move items-center justify-between rounded-lg border border-green-200 bg-white p-3 hover:bg-green-50"
													draggable="true"
													ondragstart={(e) => handleDragStart(e, student, 'assigned')}
												>
													<div>
														<div>{student.nama}</div>
														<div class="text-xs text-gray-500">NIK: {student.nik}</div>
													</div>
													<svg
														xmlns="http://www.w3.org/2000/svg"
														class="h-5 w-5 text-gray-400"
														fill="none"
														viewBox="0 0 24 24"
														stroke="currentColor"
													>
														<path
															stroke-linecap="round"
															stroke-linejoin="round"
															stroke-width="2"
															d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"
														/>
													</svg>
												</div>
											{/each}
										{:else}
											<div class="py-8 text-center text-gray-500">Seret santri ke sini</div>
										{/if}
									</div>
								</div>
							</div>
						</div>
					{:else}
						<div class="rounded-xl bg-white p-12 text-center shadow">
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
									d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
								/>
							</svg>
							<h3 class="mt-4 text-lg font-medium text-gray-900">Pilih Musyrif</h3>
							<p class="mt-2 text-gray-500">
								Silakan pilih musyrif dari daftar di sebelah kiri untuk mulai mengatur santrinya.
							</p>
						</div>
					{/if}
				</div>
			</div>
		{/if}
	</div>
</div>
