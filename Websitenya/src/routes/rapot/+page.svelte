<script>
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { format } from 'date-fns';
	import { getPhpBackendBaseUrl } from '$lib/utils.js';
	import { toast } from 'svelte-sonner';
	import CustomCalendar from '$lib/components/CustomCalendar.svelte';
	import { Popover, PopoverContent, PopoverTrigger } from '$lib/components/ui/popover/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import logoMabaiz from '../../gambar/logo-mabaiz.png';

	let isLoading = $state(false);
	let semester = $state('');
	let tahunAjaran = $state('');
	let tanggalMulai = $state('');
	let tanggalSelesai = $state('');
	let rapotData = $state(null);
	let isGenerating = $state(false);

	onMount(() => {
		if (browser) {
			// Set default tanggal mulai and selesai
			const today = new Date();
			const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
			const lastDayOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);

			tanggalMulai = formatDateForInput(firstDayOfMonth);
			tanggalSelesai = formatDateForInput(lastDayOfMonth);

			// Set default semester and tahun ajaran
			const currentMonth = today.getMonth() + 1;
			if (currentMonth >= 7) {
				// July-December: Semester Ganjil
				semester = 'ganjil';
				tahunAjaran = `${today.getFullYear()}/${today.getFullYear() + 1}`;
			} else {
				// January-June: Semester Genap
				semester = 'genap';
				tahunAjaran = `${today.getFullYear() - 1}/${today.getFullYear()}`;
			}
		}
	});

	function formatDateForInput(date) {
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		return `${year}-${month}-${day}`;
	}

	async function generateRapot() {
		// Validate inputs
		if (!semester) {
			toast.error('Silakan pilih semester');
			return;
		}
		if (!tahunAjaran) {
			toast.error('Silakan isi tahun ajaran');
			return;
		}
		if (!tanggalMulai || !tanggalSelesai) {
			toast.error('Silakan isi rentang tanggal');
			return;
		}

		isGenerating = true;
		isLoading = true;

		try {
			const token = localStorage.getItem('tokenSuper') || '';

			const response = await fetch(`${getPhpBackendBaseUrl()}/generate-rapot.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					token,
					semester,
					tahun_ajaran: tahunAjaran,
					tanggal_mulai: tanggalMulai,
					tanggal_selesai: tanggalSelesai
				})
			});

			const result = await response.json();

			if (result.success) {
				rapotData = result.rapot_data;
				toast.success(`Rapot berhasil dihasilkan untuk ${rapotData.length} santri`);
				playBeep();
			} else {
				toast.error(`Gagal menghasilkan rapot: ${result.message}`);
			}
		} catch (error) {
			console.error('Error generating rapot:', error);
			toast.error('Terjadi kesalahan saat menghasilkan rapot');
		} finally {
			isLoading = false;
			isGenerating = false;
		}
	}

	function printRapot() {
		window.print();
	}

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

	function getSemesterLabel() {
		return semester === 'ganjil' ? 'GANJIL' : 'GENAP';
	}

	function formatTanggalIndo(dateStr) {
		if (!dateStr) return '';
		const date = new Date(dateStr);
		const months = [
			'Januari',
			'Februari',
			'Maret',
			'April',
			'Mei',
			'Juni',
			'Juli',
			'Agustus',
			'September',
			'Oktober',
			'November',
			'Desember'
		];
		return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`;
	}

	async function saveCatatan(id, elementId, btnElement) {
		const el = document.getElementById(elementId);
		if (!el) return;
		const catatan = el.innerText.trim();

		// Disable button to prevent duplicate submit
		if (btnElement) {
			btnElement.disabled = true;
			btnElement.innerText = 'Menyimpan...';
		}

		try {
			const token = localStorage.getItem('tokenSuper') || '';
			const response = await fetch(`${getPhpBackendBaseUrl()}/update-achievement-catatan.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': token ? `Bearer ${token}` : ''
				},
				body: JSON.stringify({
					token,
					id,
					catatan
				})
			});

			const result = await response.json();

			if (result.success) {
				toast.success('Catatan berhasil diperbarui');
			} else {
				toast.error(`Gagal memperbarui catatan: ${result.message}`);
			}
		} catch (error) {
			console.error('Error saving catatan:', error);
			toast.error('Terjadi kesalahan saat memperbarui catatan');
		} finally {
			if (btnElement) {
				btnElement.disabled = false;
				btnElement.innerText = 'Simpan';
			}
		}
	}
</script>

<svelte:head>
	<title>Rapot Tahfidz</title>
</svelte:head>

<div class="app-container">
	<!-- Control Panel - Hidden when printing -->
	<div class="control-panel no-print">
		<div class="container">
			<h1 class="page-title">Rapot Tahfidz</h1>
			<p class="page-subtitle">Generate laporan tahfidz semester untuk semua santri</p>

			<form
				onsubmit={(e) => {
					e.preventDefault();
					generateRapot();
				}}
			>
				<div class="form-grid">
					<!-- Semester Selection -->
					<div class="form-group">
						<label class="form-label"> Semester </label>
						<select bind:value={semester} class="form-input" required>
							<option value="">Pilih Semester</option>
							<option value="ganjil">Ganjil</option>
							<option value="genap">Genap</option>
						</select>
					</div>

					<!-- Tahun Ajaran -->
					<div class="form-group">
						<label class="form-label"> Tahun Ajaran </label>
						<input
							type="text"
							bind:value={tahunAjaran}
							placeholder="Contoh: 2024/2025"
							class="form-input"
							required
						/>
					</div>

					<!-- Date Range -->
					<div class="form-group">
						<label class="form-label"> Tanggal Mulai </label>
						<Popover>
							<PopoverTrigger asChild>
								<Button variant="outline" class="date-button">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="calendar-icon"
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
									{tanggalMulai ? format(new Date(tanggalMulai), 'dd/MM/yyyy') : 'Pilih tanggal...'}
								</Button>
							</PopoverTrigger>
							<PopoverContent class="z-[100] w-auto p-0">
								<CustomCalendar
									selectedDate={tanggalMulai}
									onDateSelect={(date) => {
										const year = date.getFullYear();
										const month = String(date.getMonth() + 1).padStart(2, '0');
										const day = String(date.getDate()).padStart(2, '0');
										tanggalMulai = `${year}-${month}-${day}`;

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

					<div class="form-group">
						<label class="form-label"> Tanggal Selesai </label>
						<Popover>
							<PopoverTrigger asChild>
								<Button variant="outline" class="date-button">
									<svg
										xmlns="http://www.w3.org/2000/svg"
										class="calendar-icon"
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
									{tanggalSelesai
										? format(new Date(tanggalSelesai), 'dd/MM/yyyy')
										: 'Pilih tanggal...'}
								</Button>
							</PopoverTrigger>
							<PopoverContent class="z-[100] w-auto p-0">
								<CustomCalendar
									selectedDate={tanggalSelesai}
									onDateSelect={(date) => {
										const year = date.getFullYear();
										const month = String(date.getMonth() + 1).padStart(2, '0');
										const day = String(date.getDate()).padStart(2, '0');
										tanggalSelesai = `${year}-${month}-${day}`;

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

				<div class="button-group">
					<button type="submit" disabled={isGenerating} class="submit-button">
						{#if isGenerating}
							<span class="button-content">
								<svg class="spinner" viewBox="0 0 24 24" fill="none">
									<circle
										class="opacity-25"
										cx="12"
										cy="12"
										r="10"
										stroke="currentColor"
										stroke-width="4"
									/>
									<path
										class="opacity-75"
										fill="currentColor"
										d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
									/>
								</svg>
								Menghasilkan Rapot...
							</span>
						{:else}
							Generate Rapot
						{/if}
					</button>

					{#if rapotData && rapotData.length > 0}
						<button type="button" onclick={printRapot} class="print-button">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="button-icon"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
								/>
							</svg>
							Cetak Rapot
						</button>
					{/if}
				</div>
			</form>
		</div>
	</div>

	<!-- Loading State -->
	{#if isLoading}
		<div class="loading-container">
			<div class="spinner-large"></div>
			<p class="loading-text">Menghasilkan rapot...</p>
		</div>
	{/if}

	<!-- Rapot Results - A4 Print Layout -->
	{#if rapotData && rapotData.length > 0}
		<div class="rapot-results">
			{#each rapotData as studentRapot}
				<div class="rapot-page a4-page">
					<!-- Header -->
					<div class="rapot-header">
						<!-- Logo -->
						<img src={logoMabaiz} alt="Logo" class="logo-image" />
						<h2 class="report-title">
							LAPORAN TAHFIDZ SEMESTER {getSemesterLabel()}
						</h2>
						<h3 class="report-subtitle">
							TAHUN AJARAN {tahunAjaran}
						</h3>
					</div>

					<!-- Student Info Table (No Border) -->
					<div class="student-info">
						<table class="info-table">
							<tbody>
								<tr>
									<td class="info-label">Nama Santri</td>
									<td class="info-separator">:</td>
									<td class="info-value">{studentRapot.nama}</td>
								</tr>
								<tr>
									<td class="info-label">NIS</td>
									<td class="info-separator">:</td>
									<td class="info-value">{studentRapot.nis}</td>
								</tr>
								<tr>
									<td class="info-label">Marhalah</td>
									<td class="info-separator">:</td>
									<td class="info-value">{studentRapot.marhalah}</td>
								</tr>
								<tr>
									<td class="info-label">Pencapaian Terakhir</td>
									<td class="info-separator">:</td>
									<td class="info-value">{studentRapot.pencapaian_terakhir}</td>
								</tr>
							</tbody>
						</table>
					</div>

					<!-- Syahadah Section -->
					{#if studentRapot.syahadah && studentRapot.syahadah.length > 0}
						<div class="achievement-section">
							<h4 class="section-title">Syahadah</h4>
							<table class="achievement-table">
								<thead>
									<tr>
										<th class="th-juz juz-syahadah" rowspan="2">Juz</th>
										<th class="th-nilai" colspan="2">Nilai</th>
										<th class="th-catatan" rowspan="2">Catatan</th>
									</tr>
									<tr>
										<th class="th-kuantitatif">Kuantitatif</th>
										<th class="th-kualitatif">Kualitatif</th>
									</tr>
								</thead>
								<tbody>
									{#each studentRapot.syahadah as sya}
										<tr>
											<td class="td-juz">{sya.juz}</td>
											<td class="td-nilai">{sya.nilai_kuantitatif}</td>
											<td class="td-nilai">{sya.nilai_kualitatif}</td>
											<td class="td-catatan-cell">
												<div
													contenteditable
													class="td-catatan-edit"
													id="catatan-syahadah-{sya.id}"
												>
													{sya.catatan}
												</div>
												<button
													type="button"
													class="save-note-btn no-print"
													onclick={(e) => saveCatatan(sya.id, `catatan-syahadah-${sya.id}`, e.currentTarget)}
												>
													Simpan
												</button>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					{/if}

					<!-- Juziyah Section -->
					{#if studentRapot.juziyah && studentRapot.juziyah.length > 0}
						<div class="achievement-section">
							<h4 class="section-title">Juziyah</h4>
							<table class="achievement-table">
								<thead>
									<tr>
										<th class="th-juz juz-juziyah" rowspan="2">Juz</th>
										<th class="th-nilai" colspan="2">Nilai</th>
										<th class="th-catatan" rowspan="2">Catatan</th>
									</tr>
									<tr>
										<th class="th-kuantitatif">Kuantitatif</th>
										<th class="th-kualitatif">Kualitatif</th>
									</tr>
								</thead>
								<tbody>
									{#each studentRapot.juziyah as juz}
										<tr>
											<td class="td-juz">{juz.juz}</td>
											<td class="td-nilai">{juz.nilai_kuantitatif}</td>
											<td class="td-nilai">{juz.nilai_kualitatif}</td>
											<td class="td-catatan-cell">
												<div
													contenteditable
													class="td-catatan-edit"
													id="catatan-juziyah-{juz.id}"
												>
													{juz.catatan}
												</div>
												<button
													type="button"
													class="save-note-btn no-print"
													onclick={(e) => saveCatatan(juz.id, `catatan-juziyah-${juz.id}`, e.currentTarget)}
												>
													Simpan
												</button>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					{/if}

					<!-- Signature Section -->
					<div class="signature-section">
						<p class="signature-date">
							Samarinda, {formatTanggalIndo(new Date().toISOString().split('T')[0])}
						</p>
						<p class="signature-title">Koordinator Tahfidz</p>
						<div class="signature-space"></div>
						<p class="signature-name">Imanuddin, Lc., M.E</p>
					</div>
				</div>
			{/each}
		</div>
	{:else if !isLoading && rapotData}
		<!-- No Data State -->
		<div class="no-data-container">
			<svg
				xmlns="http://www.w3.org/2000/svg"
				class="no-data-icon"
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
			<p class="no-data-title">Tidak ada data rapot</p>
			<p class="no-data-subtitle">Tidak ada pencapaian santri pada rentang tanggal yang dipilih</p>
		</div>
	{/if}
</div>

<style>
	/* App Container */
	.app-container {
		min-height: 100vh;
		background: #f9fafb;
	}

	/* Control Panel - Desktop Layout */
	.control-panel {
		background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
		padding: 2rem 1rem;
	}

	.container {
		max-width: 1200px;
		margin: 0 auto;
	}

	.page-title {
		font-size: 2rem;
		font-weight: 700;
		color: #1f2937;
		margin-bottom: 0.5rem;
	}

	.page-subtitle {
		font-size: 1rem;
		color: #6b7280;
		margin-bottom: 2rem;
	}

	.form-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 1.5rem;
		margin-bottom: 1.5rem;
	}

	.form-group {
		display: flex;
		flex-direction: column;
	}

	.form-label {
		font-size: 0.875rem;
		font-weight: 500;
		color: #374151;
		margin-bottom: 0.5rem;
	}

	.form-input,
	.date-button {
		width: 100%;
		padding: 0.75rem 1rem;
		border: 1px solid #d1d5db;
		border-radius: 0.5rem;
		font-size: 0.875rem;
		background: white;
		transition: all 0.2s;
	}

	.form-input:focus,
	.date-button:focus {
		outline: none;
		border-color: #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
	}

	.date-button {
		display: flex;
		align-items: center;
		justify-content: flex-start;
		gap: 0.5rem;
	}

	.calendar-icon {
		height: 1rem;
		width: 1rem;
		opacity: 0.7;
	}

	.button-group {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.submit-button,
	.print-button {
		padding: 0.875rem 2rem;
		font-weight: 500;
		border-radius: 0.5rem;
		transition: all 0.2s;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		border: none;
		cursor: pointer;
	}

	.submit-button {
		background: #2563eb;
		color: white;
	}

	.submit-button:hover:not(:disabled) {
		background: #1d4ed8;
	}

	.submit-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.print-button {
		background: #16a34a;
		color: white;
	}

	.print-button:hover {
		background: #15803d;
	}

	.button-icon {
		height: 1.25rem;
		width: 1.25rem;
	}

	.button-content {
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}

	.spinner {
		height: 1.25rem;
		width: 1.25rem;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	/* Loading State */
	.loading-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 4rem 1rem;
		background: white;
	}

	.spinner-large {
		height: 3rem;
		width: 3rem;
		border: 4px solid #e5e7eb;
		border-top: 4px solid #3b82f6;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.loading-text {
		margin-top: 1rem;
		color: #6b7280;
		font-size: 1.125rem;
	}

	/* No Data State */
	.no-data-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 4rem 1rem;
		background: white;
		text-align: center;
	}

	.no-data-icon {
		height: 4rem;
		width: 4rem;
		color: #9ca3af;
	}

	.no-data-title {
		margin-top: 1rem;
		font-size: 1.25rem;
		font-weight: 600;
		color: #374151;
	}

	.no-data-subtitle {
		margin-top: 0.5rem;
		font-size: 0.875rem;
		color: #6b7280;
	}

	/* Rapot Results */
	.rapot-results {
		background: white;
	}

	.rapot-page {
		width: 210mm;
		min-height: 297mm;
		padding: 20mm;
		margin: 0 auto;
		background: white;
		position: relative;
	}

	/* Rapot Header */
	.rapot-header {
		text-align: center;
		margin-bottom: 2rem;
	}

	.logo-image {
		width: 80px;
		height: 80px;
		object-fit: contain;
		margin: 0 auto 1rem;
		display: block;
	}

	.report-title {
		font-size: 1.5rem;
		font-weight: 700;
		color: #1f2937;
		margin-bottom: 0.5rem;
	}

	.report-subtitle {
		font-size: 1.125rem;
		font-weight: 600;
		color: #374151;
	}

	/* Student Info */
	.student-info {
		margin-bottom: 2rem;
	}

	.info-table {
		width: 100%;
		font-size: 0.875rem;
	}

	.info-table tr {
		display: table-row;
	}

	.info-table td {
		padding: 0.375rem 0;
		vertical-align: top;
	}

	.info-label {
		width: 180px;
		font-weight: 600;
		color: #374151;
	}

	.info-separator {
		width: 20px;
	}

	.info-value {
		color: #1f2937;
	}

	/* Achievement Sections */
	.achievement-section {
		margin-bottom: 2rem;
	}

	.section-title {
		font-size: 1.125rem;
		font-weight: 700;
		color: #1f2937;
		margin-bottom: 0.75rem;
	}

	.achievement-table {
		width: 100%;
		border-collapse: collapse;
		font-size: 0.875rem;
	}

	.achievement-table thead {
		background: #f3f4f6;
	}

	.achievement-table th,
	.achievement-table td {
		border: 1px solid #d1d5db;
		padding: 0.5rem 0.75rem;
		/* text-align: left; */
		text-align: center;
	}

	.th-juz {
		/* width: 40%; */
		text-align: left;
	}
	.juz-juziyah {
		width: 0%;
	}
	.juz-syahadah {
		width: 15%;
	}

	.th-nilai {
		width: 30%;
		text-align: center;
	}

	.th-catatan {
		width: 30%;
		text-align: left;
	}

	.th-kuantitatif,
	.th-kualitatif {
		text-align: center;
	}

	.td-juz {
		text-align: left;
	}

	.td-nilai {
		text-align: center;
	}

	.td-catatan {
		text-align: left;
	}

	.td-catatan-cell {
		text-align: left;
		position: relative;
		padding-bottom: 2.2rem !important;
	}

	.td-catatan-edit {
		outline: none;
		min-height: 1.5rem;
		text-align: left;
	}

	.save-note-btn {
		position: absolute;
		bottom: 4px;
		right: 4px;
		background: #2563eb;
		color: white;
		border: none;
		padding: 4px 8px;
		font-size: 0.75rem;
		font-weight: 500;
		border-radius: 0.25rem;
		cursor: pointer;
		opacity: 0.9;
		transition: all 0.2s;
	}

	.save-note-btn:hover {
		background: #1d4ed8;
		opacity: 1;
	}

	.save-note-btn:disabled {
		background: #9ca3af;
		cursor: not-allowed;
	}

	/* Signature Section */
	.signature-section {
		margin-top: 3rem;
		text-align: right;
	}

	.signature-date {
		font-size: 0.875rem;
		color: #374151;
		margin-bottom: 0.5rem;
	}

	.signature-title {
		font-size: 0.875rem;
		font-weight: 700;
		color: #1f2937;
		margin-bottom: 4rem;
	}

	.signature-space {
		height: 60px;
	}

	.signature-name {
		font-size: 0.875rem;
		font-weight: 700;
		color: #1f2937;
	}

	/* Print Styles */
	@media print {
		.no-print {
			display: none !important;
		}

		@page {
			/* size: A4; */
			size: 210mm 330mm;
			margin: 0;
		}

		body {
			margin: 0;
			padding: 0;
			background: white;
			font-size: 10px !important;
			-webkit-print-color-adjust: exact;
			print-color-adjust: exact;
		}

		.app-container {
			background: white;
		}

		.rapot-results {
			background: white;
		}

		.rapot-page {
			page-break-after: always;
			page-break-inside: avoid;
			width: 210mm;
			height: 330mm;
			padding: 20mm;
			margin: 0;
			box-shadow: none;
		}

		.rapot-page:last-child {
			page-break-after: auto;
		}

		/* Maintain font sizes when printing */
		.report-title {
			font-size: 16pt !important;
		}

		.report-subtitle {
			font-size: 14pt !important;
		}

		.section-title {
			font-size: 13pt !important;
		}

		.info-table,
		.achievement-table {
			font-size: 11pt !important;
		}

		.info-table td,
		.achievement-table th,
		.achievement-table td {
			padding: 0.5rem 0.75rem;
			font-size: 11pt !important;
		}

		.td-catatan-cell {
			padding-bottom: 0.5rem !important;
		}

		.signature-date,
		.signature-title,
		.signature-name {
			font-size: 11pt !important;
		}
		img.logo-image {
			width: 60px !important;
			height: auto !important;
		}

		h2.report-title {
			font-size: 12px !important;
			margin-bottom: 0 !important;
		}

		h3.report-subtitle {
			font-size: 12px !important;
			font-weight: 700 !important;
		}

		table.info-table {
			font-size: 11px !important;
		}

		td.info-value {
			padding: 0 !important;
		}

		td.info-separator {
			padding: 0 !important;
		}

		td.info-label {
			padding: 0 !important;
		}

		h4.section-title {
			font-size: 12px !important;
		}
		table.achievement-table * {
			border-color: black !important;
		}

		table.achievement-table * {
			padding: 0 10px !important;
		}
		table.achievement-table *,
		table.info-table *,
		.signature-section * {
			font-size: 12px !important;
		}
	}

	/* Responsive for screen viewing */
	@media screen and (max-width: 1024px) {
		.rapot-page {
			width: 100%;
			padding: 2rem;
		}

		.form-grid {
			grid-template-columns: 1fr;
		}
	}
</style>
