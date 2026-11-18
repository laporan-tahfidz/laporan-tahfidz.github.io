<script>
	import { onMount } from 'svelte';
	import { getPhpBackendBaseUrl, generateIdempotencyKey, isAdminAuthenticated } from '$lib/utils.js';
	import { toast } from 'svelte-sonner';
	import { formatDateMakassar, formatTimeMakassar } from '$lib/utils/timezone.js';

	let isVisible = $state(false);
	let viewMode = $state('achievements'); // 'achievements' or 'list'
	let studentId = $state(null);
	let studentName = $state('');
	let achievements = $state([]);
	let isLoading = $state(false);
	let students = $state([]);
	let isStudentsLoading = $state(false);
	let showDeleteConfirmation = $state(null); // Holds the student ID for confirmation
	let showDeleteAchievementConfirmation = $state(null); // Holds the achievement ID for confirmation
	let isAdmin = $state(false);
	let isFixingJuz = $state(false);
	let isFixingAllJuz = $state(false);

	// Global reference to control the sidebar from anywhere
	let instance = null;

	// Check admin authentication status on mount
	onMount(() => {
		isAdmin = isAdminAuthenticated();
	});

	// Function to show the sidebar with student data
	function showSidebar(id, name) {
		studentId = id;
		studentName = name;
		isVisible = true;
		viewMode = 'achievements';
		loadAchievements();
	}

	// Function to show the list of all students
	function showStudentList() {
		isVisible = true;
		viewMode = 'list';
		loadStudents();
	}

	// Function to hide the sidebar
	function hideSidebar() {
		isVisible = false;
		studentId = null;
		studentName = '';
		achievements = [];
		students = [];
		viewMode = 'achievements';
	}

	async function loadAchievements() {
		if (!studentId) return;

		isLoading = true;
		try {
			const token = localStorage.getItem('tokenSuper') || '';

			const response = await fetch(`${getPhpBackendBaseUrl()}/get-student-achievements.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ token, studentId })
			});

			const result = await response.json();

			if (result.success) {
				achievements = result.achievements || [];
			} else {
				console.error('Failed to load achievements:', result.message);
				achievements = [];
			}
		} catch (error) {
			console.error('Error loading achievements:', error);
			achievements = [];
		} finally {
			isLoading = false;
		}
	}

	async function loadStudents() {
		isStudentsLoading = true;
		try {
			const token = localStorage.getItem('tokenSuper') || '';

			const response = await fetch(`${getPhpBackendBaseUrl()}/get-students.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ token })
			});

			const result = await response.json();

			if (result.success) {
				students = result.data || [];  // Changed from 'students' to 'data'
			} else {
				console.error('Failed to load students:', result.message);
				students = [];
			}
		} catch (error) {
			console.error('Error loading students:', error);
			students = [];
		} finally {
			isStudentsLoading = false;
		}
	}

	// Function to delete a student
	async function deleteStudent(studentId, studentName) {
		showDeleteConfirmation = null;
		
		try {
			const token = localStorage.getItem('tokenSuper') || '';
			const idempotencyKey = generateIdempotencyKey();

			const response = await fetch(`${getPhpBackendBaseUrl()}/delete-student.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Idempotency-Key': idempotencyKey
				},
				body: JSON.stringify({ 
					token,
					id: studentId,
					idempotency_key: idempotencyKey
				})
			});

			const result = await response.json();

			if (result.success) {
				// Remove the deleted student from the local list
				students = students.filter(s => s.id !== studentId);
				
				toast.success(`Santri ${studentName} berhasil dihapus`);
				
				// Play beep sound on success
				playBeep();
			} else {
				toast.error(`Gagal menghapus santri: ${result.message}`);
			}
		} catch (error) {
			console.error('Error deleting student:', error);
			toast.error('Terjadi kesalahan saat menghapus santri');
		}
	}

	// Function to delete an achievement
	async function deleteAchievement(achievementId, achievementType) {
		showDeleteAchievementConfirmation = null;

		// Check if user is authenticated - try super admin token first, then admin token
		const token = localStorage.getItem('tokenSuper') || localStorage.getItem('tokenAdmin') || '';
		if (!token) {
			toast.error('Silakan login terlebih dahulu');
			return;
		}

		try {
			const idempotencyKey = generateIdempotencyKey();

			const response = await fetch(`${getPhpBackendBaseUrl()}/delete-achievement.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`,
					'X-Idempotency-Key': idempotencyKey
				},
				body: JSON.stringify({
					id: achievementId,
					idempotency_key: idempotencyKey
				})
			});

			const result = await response.json();

			if (result.success) {
				// Remove the deleted achievement from the local list
				achievements = achievements.filter(a => a.id !== achievementId);

				toast.success(`Pencapaian ${achievementType} berhasil dihapus`);

				// Play beep sound on success
				playBeep();
			} else {
				toast.error(`Gagal menghapus pencapaian: ${result.message}`);
			}
		} catch (error) {
			console.error('Error deleting achievement:', error);
			toast.error('Terjadi kesalahan saat menghapus pencapaian');
		}
	}

	// Function to automatically fix out-of-order juz for the current student
	async function autoFixJuzOrder() {
		if (!studentId) return;

		isFixingJuz = true;
		try {
			const token = localStorage.getItem('tokenSuper') || localStorage.getItem('tokenAdmin') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/fix-juz-order.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({
					token,
					studentId
				})
			});

			const result = await response.json();
			if (result.success) {
				if (result.fixedCount > 0) {
					toast.success(result.message || `Berhasil memperbaiki ${result.fixedCount} catatan juz`);
					playBeep();
					await loadAchievements();
				} else {
					toast.info(result.message || 'Urutan juz sudah benar');
				}
			} else {
				toast.error(result.message || 'Gagal memperbaiki urutan juz');
			}
		} catch (error) {
			console.error('Error fixing juz order:', error);
			toast.error('Terjadi kesalahan saat memperbaiki urutan juz');
		} finally {
			isFixingJuz = false;
		}
	}

	// Function to automatically fix out-of-order juz for all students
	async function autoFixAllJuzOrder() {
		isFixingAllJuz = true;
		try {
			const token = localStorage.getItem('tokenSuper') || localStorage.getItem('tokenAdmin') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/fix-juz-order.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({
					token,
					studentId: 'all'
				})
			});

			const result = await response.json();
			if (result.success) {
				if (result.fixedCount > 0) {
					toast.success(result.message || `Berhasil memperbaiki ${result.fixedCount} catatan juz`);
					playBeep();
				} else {
					toast.info(result.message || 'Semua urutan juz santri sudah benar');
				}
			} else {
				toast.error(result.message || 'Gagal memperbaiki urutan juz');
			}
		} catch (error) {
			console.error('Error fixing all juz order:', error);
			toast.error('Terjadi kesalahan saat memperbaiki urutan juz');
		} finally {
			isFixingAllJuz = false;
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

	// Expose the functions globally
	onMount(() => {
		// Store reference to this instance
		instance = { showSidebar, hideSidebar, showStudentList };

		// Make it globally accessible
		if (typeof window !== 'undefined') {
			// Store the original reference in case there's already one
			if (!window.originalStudentSidebar) {
				window.originalStudentSidebar = window.studentSidebar;
			}
			window.studentSidebar = instance;
		}

		return () => {
			if (window.studentSidebar === instance) {
				// Restore the original reference if it existed
				window.studentSidebar = window.originalStudentSidebar || null;
				window.originalStudentSidebar = undefined;
			}
		};
	});
</script>

<div class="top-5 flex-shrink-0 sm:sticky sm:w-80 md:w-full md:max-w-xs">
	<div class="h-full overflow-hidden rounded-lg border border-gray-200 bg-white shadow-xl">
		<div class="flex h-full flex-col">
			<div class="flex items-center justify-between bg-blue-600 p-4 text-white">
				{#if isVisible}
					{#if viewMode === 'achievements'}
						<h3 class="truncate text-lg font-semibold">{studentName}</h3>
					{:else}
						<h3 class="truncate text-lg font-semibold">Daftar Santri</h3>
					{/if}
					<div class="flex space-x-2">
						{#if viewMode === 'achievements'}
							<button
								class="text-white hover:text-gray-200 focus:outline-none"
								title="Lihat Daftar Semua Santri"
								onclick={() => showStudentList()}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-5 w-5"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M4 6h16M4 10h16M4 14h16M4 18h16"
									/>
								</svg>
							</button>
						{/if}
						<button
							class="text-white hover:text-gray-200 focus:outline-none"
							onclick={() => {
								isVisible = false;
								studentId = null;
								studentName = '';
								achievements = [];
								students = [];
								viewMode = 'achievements';
							}}
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
				{:else}
					<h3 class="text-lg font-semibold">Daftar Santri</h3>
					<!-- Placeholder for close button when not visible -->
					<div class="invisible h-6 w-6"></div>
				{/if}
			</div>

			{#if isVisible}
				{#if viewMode === 'achievements' && studentId}
					<div class="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-2.5 shadow-xs">
						<span class="text-xs font-medium text-gray-600">
							{achievements.length} Pencapaian
						</span>
						<button
							type="button"
							disabled={isFixingJuz || isLoading || achievements.length === 0}
							onclick={autoFixJuzOrder}
							class="inline-flex items-center gap-1.5 rounded-md bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 hover:bg-blue-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
							title="Otomatis memperbaiki nomor juz agar berurutan"
						>
							<i class="fa-solid {isFixingJuz ? 'fa-spinner fa-spin' : 'fa-wand-magic-sparkles'}"></i>
							<span>{isFixingJuz ? 'Memperbaiki...' : 'Perbaiki Urutan Juz'}</span>
						</button>
					</div>
				{:else if viewMode === 'list'}
					<div class="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-2.5 shadow-xs">
						<span class="text-xs font-medium text-gray-600">
							{students.length} Santri
						</span>
						<button
							type="button"
							disabled={isFixingAllJuz || isStudentsLoading}
							onclick={autoFixAllJuzOrder}
							class="inline-flex items-center gap-1.5 rounded-md bg-indigo-50 px-2.5 py-1 text-xs font-semibold text-indigo-700 hover:bg-indigo-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
							title="Otomatis periksa & perbaiki urutan juz semua santri"
						>
							<i class="fa-solid {isFixingAllJuz ? 'fa-spinner fa-spin' : 'fa-wand-magic-sparkles'}"></i>
							<span>{isFixingAllJuz ? 'Memperbaiki...' : 'Perbaiki Semua Juz'}</span>
						</button>
					</div>
				{/if}
			{/if}

			<div class="flex-grow overflow-y-auto bg-gray-50 p-4 max-h-[calc(100vh-180px)]">
				{#if isVisible}
					{#if viewMode === 'achievements'}
						{#if isLoading}
							<div class="py-8 text-center">
								<div
									class="inline-block h-8 w-8 animate-spin rounded-full border-t-2 border-b-2 border-blue-500"
								></div>
								<p class="mt-2 text-gray-600">Memuat data pencapaian...</p>
							</div>
						{:else if achievements.length > 0}
							<div class="space-y-3">
								{#each achievements as achievement (achievement.id)}
									<div class="rounded-lg border border-gray-200 bg-white p-3 shadow-sm">
										<div class="flex items-start justify-between">
											<div>
												<span
													class="inline-block rounded-full px-2 py-1 text-xs font-semibold
														{achievement.type === 'ziyadah'
														? 'bg-blue-100 text-blue-800'
														: achievement.type === 'setengah_juz'
															? 'bg-green-100 text-green-800'
															: achievement.type === 'juziyah'
																? 'bg-yellow-100 text-yellow-800'
																: 'bg-purple-100 text-purple-800'}"
												>
													{achievement.type === 'ziyadah'
														? 'Ziyadah'
														: achievement.type === 'setengah_juz'
															? 'Setengah Juz'
															: achievement.type === 'juziyah'
																? 'Juziyah'
																: 'Syahadah'}
												</span>
												<h4 class="mt-2 text-sm font-medium">
													{#if achievement.type === 'ziyadah'}
														Juz: {achievement.juz}, Halaman: {achievement.halaman}
													{:else if achievement.type === 'setengah_juz'}
														Juz: {achievement.juz}, Posisi: {achievement.posisi}
													{:else if achievement.type === 'juziyah'}
														Juz: {achievement.juz}
													{:else}
														Tingkatan: {achievement.syahadah}
														{#if achievement.juz}
															, Juz: {achievement.juz}
														{/if}
													{/if}
												</h4>
												{#if achievement.catatan}
													<p class="mt-1 text-xs text-gray-600">Catatan: {achievement.catatan}</p>
												{/if}
											</div>
											<div class="flex flex-col items-end">
												<div class="text-right text-xs text-gray-500">
													<div>
														{formatDateMakassar(achievement.created_at)}
													</div>
													<div class="mt-1">
														{formatTimeMakassar(achievement.created_at)}
													</div>
													{#if achievement.kesalahan !== null}
														<div class="mt-1 text-red-600">Kesalahan: {achievement.kesalahan}</div>
													{/if}
												</div>
												{#if isAdmin}
													<button
														class="mt-2 text-red-600 hover:text-red-800"
														title="Hapus Pencapaian"
														onclick={() => showDeleteAchievementConfirmation = achievement.id}
													>
														<svg
															xmlns="http://www.w3.org/2000/svg"
															class="h-4 w-4"
															fill="none"
															viewBox="0 0 24 24"
															stroke="currentColor"
														>
															<path
																stroke-linecap="round"
																stroke-linejoin="round"
																stroke-width="2"
																d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
															/>
														</svg>
													</button>
												{/if}
											</div>
										</div>
									</div>
								{/each}
							</div>
						{:else}
							<div class="py-12 text-center text-gray-500">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="mx-auto h-12 w-12 text-gray-400"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
									/>
								</svg>
								<p class="mt-4 text-lg">Belum ada riwayat pencapaian</p>
								<p class="mt-1 text-sm">Data pencapaian untuk santri ini masih kosong</p>
							</div>
						{/if}
					{:else if viewMode === 'list'}
						{#if isStudentsLoading}
							<div class="py-8 text-center">
								<div
									class="inline-block h-8 w-8 animate-spin rounded-full border-t-2 border-b-2 border-blue-500"
								></div>
								<p class="mt-2 text-gray-600">Memuat daftar santri...</p>
							</div>
						{:else if students.length > 0}
							<div class="space-y-2">
								{#each students as student (student.id)}
									<div class="rounded-lg border border-gray-200 bg-white p-3 shadow-sm flex justify-between items-center">
										<div class="truncate">
											<div class="font-medium truncate">{student.nama}</div>
											<div class="text-xs text-gray-500">NIK: {student.nik}</div>
										</div>
										<div class="flex space-x-2">
											<button
												class="text-blue-600 hover:text-blue-800"
												title="Lihat Riwayat"
												onclick={() => showSidebar(student.id, student.nama)}
											>
												<svg
													xmlns="http://www.w3.org/2000/svg"
													class="h-5 w-5"
													fill="none"
													viewBox="0 0 24 24"
													stroke="currentColor"
												>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
													/>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
													/>
												</svg>
											</button>
											<button
												class="text-red-600 hover:text-red-800"
												title="Hapus Santri"
												onclick={() => showDeleteConfirmation = student.id}
											>
												<svg
													xmlns="http://www.w3.org/2000/svg"
													class="h-5 w-5"
													fill="none"
													viewBox="0 0 24 24"
													stroke="currentColor"
												>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														stroke-width="2"
														d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
													/>
												</svg>
											</button>
										</div>
									</div>
								{/each}
							</div>
						{:else}
							<div class="py-12 text-center text-gray-500">
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="mx-auto h-12 w-12 text-gray-400"
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
								<p class="mt-4 text-lg">Tidak ada santri</p>
								<p class="mt-1 text-sm">Belum ada data santri dalam sistem</p>
							</div>
						{/if}
					{/if}
				{:else}
					<!-- Placeholder content when no student is selected -->
					<div class="py-12 text-center text-gray-500">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="mx-auto h-12 w-12 text-gray-400"
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
						<p class="mt-4 text-lg">Daftar Santri</p>
						<p class="mt-1 text-sm">Klik tombol di bawah untuk melihat daftar semua santri</p>
						<button
							class="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
							onclick={() => showStudentList()}
						>
							Tampilkan Daftar Santri
						</button>
					</div>
				{/if}
			</div>

			<div class="border-t border-gray-200 bg-gray-100 px-4 py-3">
				{#if isVisible}
					{#if viewMode === 'list'}
						<button
							class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700 focus:outline-none"
							onclick={() => {
								isVisible = false;
								studentId = null;
								studentName = '';
								achievements = [];
								students = [];
								viewMode = 'achievements';
							}}
						>
							Tutup
						</button>
					{:else}
						<button
							class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700 focus:outline-none"
							onclick={() => {
								isVisible = false;
								studentId = null;
								studentName = '';
								achievements = [];
								students = [];
								viewMode = 'achievements';
							}}
						>
							Tutup
						</button>
					{/if}
				{:else}
					<!-- Placeholder for button when not visible -->
					<div class="w-full cursor-default rounded-lg bg-gray-300 px-4 py-2 text-white opacity-50">
						Tutup
					</div>
				{/if}
			</div>
		</div>
	</div>
	
	<!-- Delete Confirmation Modal -->
	{#if showDeleteConfirmation !== null}
		{@const student = students.find(s => s.id === showDeleteConfirmation)}
		<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
			<div class="bg-white rounded-xl shadow-lg w-full max-w-md">
				<div class="p-6">
					<div class="flex justify-between items-center mb-4">
						<h2 class="text-xl font-bold text-gray-800">Konfirmasi Hapus</h2>
						<button
							onclick={() => showDeleteConfirmation = null}
							class="text-gray-500 hover:text-gray-700"
						>
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					</div>

					<p class="text-gray-600 mb-6">Apakah Anda yakin ingin menghapus santri <strong>{student?.nama}</strong>? Tindakan ini tidak dapat dibatalkan.</p>

					<div class="flex space-x-3 pt-2">
						<button
							onclick={() => showDeleteConfirmation = null}
							class="flex-1 px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400"
						>
							Batal
						</button>
						<button
							onclick={() => deleteStudent(showDeleteConfirmation, student?.nama)}
							class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
						>
							Hapus
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}
	<!-- Delete Achievement Confirmation Modal -->
	{#if showDeleteAchievementConfirmation !== null}
		{@const achievement = achievements.find(a => a.id === showDeleteAchievementConfirmation)}
		<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
			<div class="bg-white rounded-xl shadow-lg w-full max-w-md">
				<div class="p-6">
					<div class="flex justify-between items-center mb-4">
						<h2 class="text-xl font-bold text-gray-800">Konfirmasi Hapus Pencapaian</h2>
						<button
							onclick={() => showDeleteAchievementConfirmation = null}
							class="text-gray-500 hover:text-gray-700"
						>
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					</div>

					<p class="text-gray-600 mb-6">
						Apakah Anda yakin ingin menghapus pencapaian 
						<strong>
							{achievement?.type === 'ziyadah' ? 'Ziyadah' :
							achievement?.type === 'setengah_juz' ? 'Setengah Juz' :
							achievement?.type === 'juziyah' ? 'Juziyah' : 'Syahadah'}
						</strong> 
						tanggal <strong>{formatDateMakassar(achievement?.created_at)}</strong>? 
						Tindakan ini tidak dapat dibatalkan.
					</p>

					<div class="flex space-x-3 pt-2">
						<button
							onclick={() => showDeleteAchievementConfirmation = null}
							class="flex-1 px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400"
						>
							Batal
						</button>
						<button
							onclick={() => deleteAchievement(showDeleteAchievementConfirmation, 
								achievement?.type === 'ziyadah' ? 'Ziyadah' :
								achievement?.type === 'setengah_juz' ? 'Setengah Juz' :
								achievement?.type === 'juziyah' ? 'Juziyah' : 'Syahadah')}
							class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
						>
							Hapus
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
