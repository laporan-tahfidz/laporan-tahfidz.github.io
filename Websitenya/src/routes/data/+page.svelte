<script>
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { getPhpBackendBaseUrl } from '$lib/utils.js';
	import ClassYearSettings from '$lib/components/ClassYearSettings.svelte';

	let data = $state([]);
	let configuration = $state({ kelas1: '', kelas2: '', kelas3: '' });
	let availableYears = $state([]);
	let showSettings = $state(false);
	let isSaving = $state(false);
	let loading = $state(true);
	let error = $state('');

	async function loadData() {
		loading = true;
		error = '';
		try {
			const res = await fetch(`${getPhpBackendBaseUrl()}/data.php`);
			if (!res.ok) {
				throw new Error(`HTTP error ${res.status}`);
			}
			const json = await res.json();
			if (json.success && Array.isArray(json.data)) {
				data = json.data;
				if (json.configuration) {
					configuration = json.configuration;
				}
				if (json.available_years) {
					availableYears = json.available_years;
				}
			} else {
				throw new Error(json.message || 'Gagal memuat data dari database');
			}
		} catch (err) {
			console.error('Error fetching data:', err);
			error = 'Gagal memuat data dari database: ' + (err?.message || err);
		} finally {
			loading = false;
		}
	}

	async function handleSaveConfiguration(newConfig) {
		isSaving = true;
		try {
			const res = await fetch(`${getPhpBackendBaseUrl()}/data.php`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					action: 'save_configuration',
					...newConfig
				})
			});

			if (!res.ok) {
				throw new Error(`HTTP error ${res.status}`);
			}

			const json = await res.json();
			if (json.success) {
				data = json.data || [];
				if (json.configuration) configuration = json.configuration;
				if (json.available_years) availableYears = json.available_years;
				showSettings = false;
				toast.success('Pengaturan angkatan kelas berhasil disimpan & diterapkan');
			} else {
				throw new Error(json.message || 'Gagal menyimpan pengaturan');
			}
		} catch (err) {
			console.error('Error saving configuration:', err);
			toast.error('Gagal menyimpan pengaturan: ' + (err?.message || err));
		} finally {
			isSaving = false;
		}
	}

	onMount(() => {
		loadData();
	});
</script>

<svelte:head>
	<title>Data Pencapaian Hafalan</title>
</svelte:head>

<div class="mx-auto min-h-screen max-w-[500px] bg-slate-50/50 p-4 pb-12 font-sans antialiased text-slate-800">
	<!-- Top Navigation / Header -->
	<header class="mb-4 pt-2">
		<div class="flex items-center justify-between gap-3">
			<div>
				<h1 class="text-xl font-bold tracking-tight text-slate-900">Data Pencapaian</h1>
				<p class="text-xs text-slate-500">Rekap hafalan santri per tingkatan kelas</p>
			</div>
			<button
				type="button"
				onclick={() => (showSettings = !showSettings)}
				class="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 shadow-sm hover:bg-slate-50 active:scale-95 transition"
				aria-expanded={showSettings}
			>
				<i class="fa-solid fa-sliders text-indigo-600 text-xs"></i>
				<span>{showSettings ? 'Tutup' : 'Atur Kelas'}</span>
			</button>
		</div>

		<!-- Badges ringkasan mapping kelas -->
		<div class="mt-3 flex items-center gap-1.5 overflow-x-auto text-[11px]">
			<span class="text-slate-400 font-medium">Angkatan:</span>
			<button
				type="button"
				onclick={() => (showSettings = true)}
				class="inline-flex items-center gap-1 rounded-lg bg-blue-50 px-2 py-0.5 font-medium text-blue-700 border border-blue-100/80 hover:bg-blue-100 transition"
			>
				<span>K1 (7):</span>
				<strong class="font-semibold">{configuration.kelas1 || '-'}</strong>
			</button>
			<button
				type="button"
				onclick={() => (showSettings = true)}
				class="inline-flex items-center gap-1 rounded-lg bg-emerald-50 px-2 py-0.5 font-medium text-emerald-700 border border-emerald-100/80 hover:bg-emerald-100 transition"
			>
				<span>K2 (8):</span>
				<strong class="font-semibold">{configuration.kelas2 || '-'}</strong>
			</button>
			<button
				type="button"
				onclick={() => (showSettings = true)}
				class="inline-flex items-center gap-1 rounded-lg bg-purple-50 px-2 py-0.5 font-medium text-purple-700 border border-purple-100/80 hover:bg-purple-100 transition"
			>
				<span>K3 (9):</span>
				<strong class="font-semibold">{configuration.kelas3 || '-'}</strong>
			</button>
		</div>
	</header>

	<!-- Settings Card (Collapsible) -->
	{#if showSettings}
		<ClassYearSettings
			{configuration}
			{availableYears}
			{isSaving}
			onSave={handleSaveConfiguration}
			onClose={() => (showSettings = false)}
		/>
	{/if}

	<!-- Content State -->
	{#if loading}
		<div class="flex flex-col items-center justify-center rounded-2xl border border-slate-200/60 bg-white py-12 text-center shadow-sm">
			<i class="fa-solid fa-circle-notch fa-spin text-2xl text-indigo-600 mb-2"></i>
			<span class="text-xs text-slate-500">Memuat data santri...</span>
		</div>
	{:else if error}
		<div class="rounded-2xl border border-rose-200 bg-rose-50/70 p-4 text-center">
			<div class="mb-2 flex items-center justify-center text-rose-600">
				<i class="fa-solid fa-triangle-exclamation text-lg"></i>
			</div>
			<p class="text-xs font-medium text-rose-700">{error}</p>
			<button
				type="button"
				onclick={loadData}
				class="mt-3 inline-flex items-center gap-1.5 rounded-lg bg-white px-3 py-1.5 text-xs font-semibold text-rose-600 border border-rose-200 shadow-sm hover:bg-rose-50 active:scale-95 transition"
			>
				<i class="fa-solid fa-arrow-rotate-right text-[11px]"></i>
				<span>Coba lagi</span>
			</button>
		</div>
	{:else if data.length === 0}
		<div class="flex flex-col items-center justify-center rounded-2xl border border-slate-200/60 bg-white py-12 px-4 text-center shadow-sm">
			<div class="mb-2 flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 text-slate-400">
				<i class="fa-solid fa-user-slash"></i>
			</div>
			<p class="text-xs font-semibold text-slate-700">Tidak ada santri ditemukan</p>
			<p class="mt-1 text-[11px] text-slate-400">Periksa kembali pengaturan angkatan untuk kelas 1, 2, atau 3.</p>
			<button
				type="button"
				onclick={() => (showSettings = true)}
				class="mt-3 inline-flex items-center gap-1 rounded-lg bg-indigo-50 px-3 py-1.5 text-xs font-semibold text-indigo-600 hover:bg-indigo-100 transition"
			>
				<i class="fa-solid fa-sliders text-xs"></i>
				<span>Atur Angkatan</span>
			</button>
		</div>
	{:else}
		<div class="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm">
			<div class="flex items-center justify-between border-b border-slate-100 bg-slate-50/70 px-3.5 py-2.5 text-xs font-semibold text-slate-600">
				<span>Daftar Santri</span>
				<span class="rounded-full bg-slate-200/70 px-2 py-0.5 text-[11px] font-medium text-slate-700">
					{data.length} santri
				</span>
			</div>
			<div class="overflow-x-auto">
				<table class="w-full text-left text-xs">
					<thead>
						<tr class="border-b border-slate-100 bg-slate-50/30 text-[11px] font-semibold uppercase tracking-wider text-slate-400">
							<th class="py-2.5 pl-3.5 pr-1 text-center w-8">No</th>
							<th class="py-2.5 px-2">Nama</th>
							<th class="py-2.5 px-2 text-center w-14">Kelas</th>
							<th class="py-2.5 pr-3.5 pl-2 text-left">Pencapaian</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-slate-100">
						{#each data as item (item.no)}
							<tr class="hover:bg-slate-50/80 transition-colors">
								<td class="py-2.5 pl-3.5 pr-1 text-center text-slate-400 font-medium">
									{item.no}
								</td>
								<td class="py-2.5 px-2 font-medium text-slate-900">
									{item.nama}
								</td>
								<td class="py-2.5 px-2 text-center">
									<span
										class="inline-block rounded-md px-1.5 py-0.5 text-[11px] font-bold {item.kelas === 7 ? 'bg-blue-50 text-blue-700' : item.kelas === 8 ? 'bg-emerald-50 text-emerald-700' : 'bg-purple-50 text-purple-700'}"
									>
										{item.kelas}
									</span>
								</td>
								<td class="py-2.5 pr-3.5 pl-2 text-slate-600 font-medium">
									{item.pencapaian}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	{/if}
</div>
