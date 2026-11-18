<script>
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { getPhpBackendBaseUrl, generateIdempotencyKey } from '$lib/utils.js';
	import { toast } from 'svelte-sonner';
	import ClassAssignmentBento from '$lib/components/ClassAssignmentBento.svelte';
	import ClassDistributionVisualization from '$lib/components/ClassDistributionVisualization.svelte';
	import MusyrifProgressBento from '$lib/components/MusyrifProgressBento.svelte';
	import CoordinatorAttentionBento from '$lib/components/CoordinatorAttentionBento.svelte';
	import MusyrifAttentionBento from '$lib/components/MusyrifAttentionBento.svelte';
	import StudentSidebar from '$lib/components/StudentSidebarEmbedded.svelte';
	import AchievementStatisticsChart from '$lib/components/AchievementStatisticsChart.svelte';

	let isLoading = $state(true);
	let studentCount = $state(0);
	let groups = $state([]);
	let selectedGroupId = $state('');
	let isRefreshing = $state(false);
	let musyrifs = $state([]);
	let students = $state([]);
	let selectedMusyrif = $state(null);
	let availableStudents = $state([]); // Students not assigned to the selected musyrif
	let assignedStudents = $state([]); // Students assigned to the selected musyrif
	let searchQuery = $state('');
	let backgroundImage = $state('');
	let classConfig = $state({
		kelas1: '',
		kelas2: '',
		kelas3: ''
	});
	let availableYears = $state([]);
	let isSaving = $state(false);
	let classDistribution = $state({
		'Kelas 1': 0,
		'Kelas 2': 0,
		'Kelas 3': 0,
		Lainnya: 0
	});

	// Admin authentication state
	let isAdminAuthenticated = $state(false);
	let showLoginModal = $state(false);
	let otpPhone = $state('+6281545143654');
	let otpCode = $state('');
	let isSendingOtp = $state(false);
	let isVerifyingOtp = $state(false);

	onMount(async () => {
		if (browser) {
			// Check if admin token exists and is valid
			const adminToken = localStorage.getItem('tokenAdmin');
			if (adminToken) {
				const isValid = await verifyAdminToken(adminToken);
				isAdminAuthenticated = isValid;
			}

			// Load background image from localStorage
			const savedBackgroundImage = localStorage.getItem('gambar');
			if (savedBackgroundImage) {
				backgroundImage = savedBackgroundImage;
			}

			// Get the count of students in the database
			await getStudentCount();
			// Load groups from localStorage or fetch from API
			await loadGroups();
			// Load musyrif and student data
			await loadMusyrifs();
			await loadStudents();
			// Load class configuration and available years
			await loadClassConfiguration();
			await loadAvailableYears();
			await loadClassDistribution();
		}
		isLoading = false;
	});

	// Function to verify admin token
	async function verifyAdminToken(token) {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/verify-admin-token.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ token })
			});

			const result = await response.json();
			return result.valid === true;
		} catch (error) {
			console.error('Error verifying admin token:', error);
			return false;
		}
	}

	// Function to send OTP
	async function sendOtp() {
		isSendingOtp = true;
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/send-otp-admin.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ phone: otpPhone })
			});

			const result = await response.json();

			if (result.success) {
				toast.success('Kode OTP telah dikirim ke WhatsApp Anda');
				playBeep();
			} else {
				toast.error(result.message || 'Gagal mengirim kode OTP');
			}
		} catch (error) {
			console.error('Error sending OTP:', error);
			toast.error('Terjadi kesalahan saat mengirim kode OTP');
		} finally {
			isSendingOtp = false;
		}
	}

	// Function to verify OTP
	async function verifyOtp() {
		isVerifyingOtp = true;
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/verify-otp-admin.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ phone: otpPhone, code: otpCode })
			});

			const result = await response.json();

			if (result.success) {
				// Store the admin token
				localStorage.setItem('tokenAdmin', result.token);
				isAdminAuthenticated = true;
				showLoginModal = false;

				toast.success('Autentikasi admin berhasil');
				playBeep();
			} else {
				toast.error(result.message || 'Kode OTP tidak valid');
			}
		} catch (error) {
			console.error('Error verifying OTP:', error);
			toast.error('Terjadi kesalahan saat memverifikasi kode OTP');
		} finally {
			isVerifyingOtp = false;
		}
	}

	// Function to handle login modal
	function openLoginModal() {
		showLoginModal = true;
		otpCode = '';
	}

	// Function to close login modal
	function closeLoginModal() {
		showLoginModal = false;
		otpCode = '';
	}

	// Function to show student list in sidebar
	function showStudentListInSidebar() {
		if (window.studentSidebar && typeof window.studentSidebar.showStudentList === 'function') {
			window.studentSidebar.showStudentList();
		}
	}

	async function getStudentCount() {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-student-count.php`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			const result = await response.json();

			if (result.success) {
				studentCount = result.count;
			}
		} catch (error) {
			console.error('Error getting student count:', error);
		}
	}

	async function logout() {
		// Since this page is now public, we don't need to redirect to login
		// Just remove the token if it exists
		if (browser) {
			localStorage.removeItem('tokenSuper');
		}
	}

	// Function to fetch student data from external API
	async function fetchStudentData() {
		const button = document.getElementById('fetch-student-data-btn');
		button.disabled = true;
		button.textContent = 'Mengambil data...';

		try {
			const idempotencyKey = generateIdempotencyKey(); // Generate idempotency key
			const response = await fetch(`${getPhpBackendBaseUrl()}/fetch-student-data.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-Idempotency-Key': idempotencyKey // Add idempotency key to header
				},
				body: JSON.stringify({
					token: localStorage.getItem('tokenSuper') || '',
					idempotency_key: idempotencyKey // Add idempotency key to body as well
				})
			});

			const result = await response.json();

			if (result.success) {
				toast.success(`Berhasil mengambil dan menyimpan ${result.count} data santri`);
				// Refresh the student count
				await getStudentCount();
				// Reload students
				await loadStudents();

				// Play beep sound on success
				playBeep();
			} else {
				toast.error(`Gagal mengambil data: ${result.message}`);
			}
		} catch (error) {
			console.error('Error fetching student data:', error);
			toast.error('Terjadi kesalahan saat mengambil data');
		} finally {
			button.disabled = false;
			button.textContent = 'Ambil Data Santri';
		}
	}

	let isFixingAllJuz = $state(false);

	// Function to automatically fix out-of-order juz for all students
	async function fixAllStudentsJuz() {
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
			console.error('Error fixing all juz:', error);
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

	// Functions for WhatsApp Groups Management
	async function loadGroups() {
		// Load groups from localStorage on mount
		const savedGroups = localStorage.getItem('grup');
		if (savedGroups) {
			try {
				groups = JSON.parse(savedGroups);
				// Set the selected group from database
				if (groups.length > 0) {
					await loadSelectedGroupId();
				}
			} catch (error) {
				console.error('Error parsing groups from localStorage:', error);
				// If there's an error, fetch fresh data
				await fetchGroups();
			}
		} else {
			// If no data in localStorage, fetch it
			await fetchGroups();
		}
	}

	async function fetchGroups() {
		if (isRefreshing) return; // Prevent multiple simultaneous requests

		isRefreshing = true;
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-whatsapp-groups.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({})
			});

			const result = await response.json();

			if (result.success) {
				groups = result.data || [];
				groups = groups.sort((a, b) => (a.name > b.name ? 1 : -1));

				// Save to localStorage
				localStorage.setItem('grup', JSON.stringify(groups));

				// Load the selected group ID from database after fetching groups
				if (groups.length > 0) {
					await loadSelectedGroupId();
				}
			}
		} catch (error) {
			console.error('Error fetching groups:', error);
		} finally {
			isRefreshing = false;
		}
	}

	async function handleGroupChange(event) {
		selectedGroupId = event.target.value;
		// Save the selected group to database
		await saveSelectedGroupId(selectedGroupId);
	}

	// Function to load selected group ID from database
	async function loadSelectedGroupId() {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/save-selected-group.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					action: 'get'
				})
			});

			const result = await response.json();

			if (result.success) {
				if (result.selected_group_id) {
					selectedGroupId = result.selected_group_id;
				} else {
					// If no selected group ID in database, use the first group as default
					if (groups.length > 0) {
						selectedGroupId = groups[0].id;
						// Save this default selection to database
						await saveSelectedGroupId(selectedGroupId);
					}
				}
			} else {
				console.error('Error loading selected group ID:', result.message);
				// Fallback to first group if there's an error
				if (groups.length > 0) {
					selectedGroupId = groups[0].id;
				}
			}
		} catch (error) {
			console.error('Error loading selected group ID:', error);
			// Fallback to first group if there's an error
			if (groups.length > 0) {
				selectedGroupId = groups[0].id;
			}
		}
	}

	// Function to save selected group ID to database
	async function saveSelectedGroupId(groupId) {
		try {
			const response = await fetch(`${getPhpBackendBaseUrl()}/save-selected-group.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					action: 'set',
					group_id: groupId
				})
			});

			const result = await response.json();

			if (!result.success) {
				console.error('Error saving selected group ID:', result.message);
			}
		} catch (error) {
			console.error('Error saving selected group ID:', error);
		}
	}

	// Functions for Musyrif and Halaqah Management
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
			}
		} catch (error) {
			console.error('Error loading musyrifs:', error);
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
			}
		} catch (error) {
			console.error('Error loading students:', error);
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
			}
		} catch (error) {
			console.error('Error loading musyrif students:', error);
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
			alert('Silakan pilih musyrif terlebih dahulu');
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
				// Update the musyrif's assigned count in the list
				const updatedMusyrifs = musyrifs.map((m) =>
					m.id === selectedMusyrif.id
						? { ...m, assigned_students_count: assignedStudents.length }
						: m
				);
				musyrifs = updatedMusyrifs;
			}
		} catch (error) {
			console.error('Error saving musyrif assignments:', error);
		}
	}

	function setBackgroundImage(imageUrl) {
		if (imageUrl) {
			localStorage.setItem('gambar', imageUrl);
			backgroundImage = imageUrl;
			toast.success('Gambar background berhasil diubah');
			playBeep();
		} else {
			localStorage.removeItem('gambar');
			backgroundImage = '';
			toast.success('Gambar background berhasil dihapus');
			playBeep();
		}
	}

	// Functions for Class Configuration Management
	async function loadClassDistribution() {
		try {
			const token = localStorage.getItem('tokenSuper') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-class-distribution.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({})
			});

			const result = await response.json();

			if (result.success) {
				classDistribution = result.distribution || {
					'Kelas 1': 0,
					'Kelas 2': 0,
					'Kelas 3': 0,
					Lainnya: 0
				};
			} else {
				toast.error('Gagal memuat distribusi kelas');
			}
		} catch (error) {
			console.error('Error loading class distribution:', error);
			toast.error('Terjadi kesalahan saat memuat distribusi kelas');
		}
	}

	async function loadClassConfiguration() {
		try {
			const token = localStorage.getItem('tokenSuper') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-class-configuration.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({})
			});

			const result = await response.json();

			if (result.success) {
				classConfig = {
					kelas1: result.configuration.kelas1 || '',
					kelas2: result.configuration.kelas2 || '',
					kelas3: result.configuration.kelas3 || ''
				};
			} else {
				toast.error('Gagal memuat konfigurasi kelas');
			}
		} catch (error) {
			console.error('Error loading class configuration:', error);
			toast.error('Terjadi kesalahan saat memuat konfigurasi kelas');
		}
	}

	async function loadAvailableYears() {
		try {
			const token = localStorage.getItem('tokenSuper') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/get-available-years.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({})
			});

			const result = await response.json();

			if (result.success) {
				availableYears = result.years || [];
			} else {
				toast.error('Gagal memuat tahun tersedia');
			}
		} catch (error) {
			console.error('Error loading available years:', error);
			toast.error('Terjadi kesalahan saat memuat tahun tersedia');
		}
	}

	async function saveConfiguration(configuration) {
		isSaving = true;

		try {
			const token = localStorage.getItem('tokenSuper') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/save-class-configuration.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({
					configuration: configuration
				})
			});

			const result = await response.json();

			if (result.success) {
				classConfig = configuration; // Update local state
				toast.success('Konfigurasi kelas berhasil disimpan');
				playBeep();

				// Refresh the class distribution after saving
				await loadClassDistribution();
			} else {
				toast.error(`Gagal menyimpan konfigurasi: ${result.message}`);
			}
		} catch (error) {
			console.error('Error saving class configuration:', error);
			toast.error('Terjadi kesalahan saat menyimpan konfigurasi');
		} finally {
			isSaving = false;
		}
	}

	async function autoConfigureClasses() {
		isSaving = true;

		try {
			const token = localStorage.getItem('tokenSuper') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/auto-configure-classes.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${token}`
				},
				body: JSON.stringify({})
			});

			const result = await response.json();

			if (result.success) {
				toast.success('Kelas berhasil dikonfigurasi otomatis');
				// Reload the configuration to reflect the changes
				await loadClassConfiguration();
				// Refresh the class distribution after auto-configuring
				await loadClassDistribution();
				playBeep();
			} else {
				toast.error(`Gagal mengkonfigurasi kelas otomatis: ${result.message}`);
			}
		} catch (error) {
			console.error('Error auto configuring classes:', error);
			toast.error('Terjadi kesalahan saat mengkonfigurasi kelas otomatis');
		} finally {
			isSaving = false;
		}
	}
</script>

	<div
		class="min-h-screen p-4"
		style={backgroundImage
			? `background: linear-gradient(rgba(239, 246, 255, 0), rgba(239, 246, 255, 0)), url('${backgroundImage}') center/cover no-repeat fixed;`
			: 'background: linear-gradient(to bottom right, #eff6ff, #e0e7ff);'}
	>
		<div class="mx-auto flex max-w-[2000px] flex-col md:flex-row">
			<!-- Student Sidebar - Permanent element on the left (top on mobile) -->
			<div class="md:mr-6 mb-6 md:mb-0 w-full md:w-80">
				<StudentSidebar />
			</div>
			<div class="flex-1 w-full">
				<header class="mb-6 rounded-xl bg-white p-6 shadow">
					<div class="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
						<h1 class="text-2xl font-bold text-gray-800">Dashboard Super Admin</h1>

						<div class="flex flex-wrap gap-3">
							<!-- Show Student List Button -->
							<!-- <button
								class="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
								onclick={showStudentListInSidebar}
							>
								Lihat Daftar Santri
							</button> -->
							
							<!-- Background Image Upload -->
							<div class="relative">
								<input
									type="file"
									accept="image/*"
									class="absolute inset-0 h-full w-full cursor-pointer opacity-0"
									onchange={(e) => {
										const file = e.target.files[0];
										if (file) {
											const reader = new FileReader();
											reader.onload = (event) => {
												setBackgroundImage(event.target.result);
											};
											reader.readAsDataURL(file);
										}
									}}
								/>
								<button
									class="rounded-lg bg-purple-600 px-4 py-2 font-medium text-white transition hover:bg-purple-700"
								>
									Ganti Background
								</button>
							</div>

						</div>
					</div>
				</header>

				<!-- Progress Monitoring Section -->
				<section id="progress-monitoring" class="my-12 space-y-6">
					<!-- Musyrif Progress Monitoring Bento -->
					<div class="rounded-xl bg-white p-6 shadow">
						<h2 class="mb-4 text-xl font-semibold text-gray-800">
							Monitoring Kemajuan Hafalan Santri
						</h2>
						<p class="mb-6 text-gray-600">
							Monitor kemajuan hafalan santri berdasarkan juz dan musyrif pembimbing
						</p>

						<MusyrifProgressBento className="w-full" />
					</div>

					<!-- Attention Bentos Section -->
					<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
						<!-- Coordinator Attention Bento -->
						<CoordinatorAttentionBento className="" />

						<!-- Musyrif Attention Bento -->
						<MusyrifAttentionBento className="" />
					</div>
				</section>

				<main class="grid grid-cols-1 gap-6 lg:grid-cols-3">
					<!-- Full Width Chart Section -->
					<div class="lg:col-span-3 mb-6">
						<AchievementStatisticsChart className="w-full" />
					</div>

					<!-- Left Column: Student Sync and WhatsApp Groups -->
					<div class="space-y-6 lg:col-span-1">
						<!-- Student Sync Section -->
						{#if isAdminAuthenticated}
						<div class="rounded-xl bg-white p-6 shadow">
							<h2 class="mb-4 text-xl font-semibold text-gray-800">Sinkronisasi Data Santri</h2>
							<p class="mb-4 text-gray-600">
								Ambil data santri terbaru dari sistem eksternal dan simpan ke database lokal.
							</p>

							<div class="mb-6 flex items-center gap-4">
								<div class="rounded-lg bg-blue-100 p-4">
									<p class="text-sm text-blue-800">Total Santri</p>
									<p class="text-2xl font-bold text-blue-600">{studentCount}</p>
								</div>

								<button
									id="fetch-student-data-btn"
									onclick={fetchStudentData}
									class="flex items-center rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
								>
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="mr-2 h-5 w-5"
										viewBox="0 0 20 20"
										fill="currentColor"
									>
										<path
											fill-rule="evenodd"
											d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
											clip-rule="evenodd"
										/>
									</svg>
									Ambil Data Santri
								</button>

								<button
									onclick={fixAllStudentsJuz}
									disabled={isFixingAllJuz}
									class="flex items-center rounded-lg bg-indigo-600 px-6 py-3 font-medium text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50 cursor-pointer"
									title="Periksa dan perbaiki urutan juz semua santri otomatis"
								>
									<i class="fa-solid {isFixingAllJuz ? 'fa-spinner fa-spin' : 'fa-wand-magic-sparkles'} mr-2"></i>
									{isFixingAllJuz ? 'Memperbaiki...' : 'Perbaiki Urutan Juz'}
								</button>
							</div>

							<div class="rounded-lg border border-blue-100 bg-blue-50 p-4">
								<h3 class="mb-2 font-medium text-blue-800">Catatan Penting:</h3>
								<ul class="list-disc space-y-1 pl-5 text-sm text-blue-700">
									<li>Data yang diambil akan disimpan secara lokal di database aplikasi</li>
									<li>Jika data sudah ada, maka akan diperbarui dengan data terbaru</li>
									<li>
										Proses sinkronisasi hanya akan menyimpan data yang belum ada atau memperbarui
										data yang sudah ada
									</li>
								</ul>
							</div>
						</div>
						{:else}
						<div class="rounded-xl bg-white p-6 shadow">
							<div class="text-center py-8">
								<h2 class="mb-4 text-xl font-semibold text-gray-800">Sinkronisasi Data Santri</h2>
								<p class="mb-6 text-gray-600">Fitur ini hanya tersedia untuk admin terautentikasi.</p>
								<button
									onclick={openLoginModal}
									class="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
								>
									Masuk sebagai Admin
								</button>
							</div>
						</div>
						{/if}

						<!-- WhatsApp Groups Section -->
						{#if isAdminAuthenticated}
						<div class="rounded-xl bg-white p-6 shadow">
							<h2 class="mb-4 text-xl font-semibold text-gray-800">Manajemen Grup WhatsApp</h2>

							<div class="mb-6">
								<label for="group-select" class="mb-2 block text-sm font-medium text-gray-700">
									Pilih Grup WhatsApp Tujuan
								</label>

								<div class="flex items-end gap-4">
									<div class="flex-grow">
										<select
											id="group-select"
											class="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
											bind:value={selectedGroupId}
											onchange={handleGroupChange}
										>
											{#if groups.length > 0}
												{#each groups as group}
													<option value={group.id}>
														{group.name}
													</option>
												{/each}
											{:else}
												<option value="">Tidak ada grup ditemukan</option>
											{/if}
										</select>

										<p class="mt-2 text-sm text-gray-500">
											Pesan yang dikirim akan dikirim ke grup yang dipilih di atas
										</p>
									</div>

									<button
										class="flex items-center rounded-md bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
										onclick={fetchGroups}
										disabled={isRefreshing}
									>
										{#if isRefreshing}
											<svg
												class="mr-2 -ml-1 h-4 w-4 animate-spin text-white"
												xmlns="http://www.w3.org/2000/svg"
												fill="none"
												viewBox="0 0 24 24"
											>
												<circle
													class="opacity-25"
													cx="12"
													cy="12"
													r="10"
													stroke="currentColor"
													stroke-width="4"
												></circle>
												<path
													class="opacity-75"
													fill="currentColor"
													d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
												></path>
											</svg>
											Memuat...
										{:else}
											<svg
												xmlns="http://www.w3.org/2000/svg"
												class="mr-1 h-5 w-5"
												viewBox="0 0 20 20"
												fill="currentColor"
											>
												<path
													fill-rule="evenodd"
													d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
													clip-rule="evenodd"
												/>
											</svg>
											Tarik Ulang
										{/if}
									</button>
								</div>
							</div>
						</div>
						{:else}
						<div class="rounded-xl bg-white p-6 shadow">
							<div class="text-center py-8">
								<h2 class="mb-4 text-xl font-semibold text-gray-800">Manajemen Grup WhatsApp</h2>
								<p class="mb-6 text-gray-600">Fitur ini hanya tersedia untuk admin terautentikasi.</p>
								<button
									onclick={openLoginModal}
									class="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
								>
									Masuk sebagai Admin
								</button>
							</div>
						</div>
						{/if}
					</div>

					<!-- Middle and Right Columns: Musyrif and Halaqah Management -->
					<div class="space-y-6 lg:col-span-2">
						<!-- Musyrif List -->
						{#if isAdminAuthenticated}
						<div class="rounded-xl bg-white p-6 shadow">
							<div class="mb-4 flex items-center justify-between">
								<h2 class="text-xl font-semibold text-gray-800">Daftar Musyrif</h2>
								<a
									href="/super/musyrif"
									class="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700"
								>
									Kelola Musyrif
								</a>
							</div>

							<div class="grid max-h-[300px] grid-cols-1 gap-4 overflow-y-auto pr-2 md:grid-cols-2">
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
									<div class="text-center py-8 text-gray-500 col-span-2">Belum ada musyrif</div>
								{/each}
							</div>
						</div>
						{:else}
						<div class="rounded-xl bg-white p-6 shadow">
							<div class="text-center py-8">
								<h2 class="mb-4 text-xl font-semibold text-gray-800">Daftar Musyrif</h2>
								<p class="mb-6 text-gray-600">Fitur ini hanya tersedia untuk admin terautentikasi.</p>
								<button
									onclick={openLoginModal}
									class="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white transition hover:bg-blue-700"
								>
									Masuk sebagai Admin
								</button>
							</div>
						</div>
						{/if}

						<!-- Student Assignment -->
						<div class="rounded-xl bg-white p-6 shadow">
							{#if selectedMusyrif}
								<div>
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
												class="max-h-96 overflow-y-auto rounded-lg border border-gray-200 bg-gray-50 p-3"
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
												class="max-h-96 overflow-y-auto rounded-lg border border-green-200 bg-green-50 p-3"
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
								<div class="py-12 text-center">
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
										Silakan pilih musyrif dari daftar di atas untuk mulai mengatur santrinya.
									</p>
								</div>
							{/if}
						</div>
					</div>
				</main>

				<!-- Class Assignment Section -->
				<section id="class-assignment" class="mt-12 space-y-6">
					<!-- Removed Class Configuration Section as per new requirements -->
				</section>
			</div>
		</div>
	</div>

	<!-- Admin Login Modal -->
	{#if showLoginModal}
		<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
			<div class="bg-white rounded-xl shadow-lg w-full max-w-md">
				<div class="p-6">
					<div class="flex justify-between items-center mb-4">
						<h2 class="text-xl font-bold text-gray-800">Masuk sebagai Admin</h2>
						<button
							onclick={closeLoginModal}
							class="text-gray-500 hover:text-gray-700"
						>
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
							</svg>
						</button>
					</div>

					<p class="text-gray-600 mb-6">Masukkan kode OTP yang dikirimkan ke WhatsApp Anda.</p>

					<div class="space-y-4">
						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1">Nomor WhatsApp</label>
							<input
								type="text"
								bind:value={otpPhone}
								class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
								placeholder="+6281234567890"
								disabled
							/>
						</div>

						<div>
							<label class="block text-sm font-medium text-gray-700 mb-1">Kode OTP</label>
							<input
								type="text"
								bind:value={otpCode}
								class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
								placeholder="Masukkan kode OTP"
								maxlength="6"
							/>
						</div>

						<div class="flex space-x-3 pt-2">
							<button
								onclick={sendOtp}
								class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
								disabled={isSendingOtp}
							>
								{#if isSendingOtp}
									<span class="flex items-center justify-center">
										<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
											<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
											<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
										</svg>
										Mengirim...
									</span>
								{:else}
									Kirim OTP
								{/if}
							</button>

							<button
								onclick={verifyOtp}
								class="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
								disabled={isVerifyingOtp || otpCode.length !== 6}
							>
								{#if isVerifyingOtp}
									<span class="flex items-center justify-center">
										<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
											<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
											<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
										</svg>
										Verifikasi...
									</span>
								{:else}
									Verifikasi
								{/if}
							</button>
						</div>
					</div>
				</div>
			</div>
		</div>
	{/if}
