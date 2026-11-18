<script>
	let {
		configuration = { kelas1: '', kelas2: '', kelas3: '' },
		availableYears = [],
		onSave = async () => {},
		isSaving = false,
		onClose = () => {}
	} = $props();

	let selectedKelas1 = $state(configuration.kelas1 || '');
	let selectedKelas2 = $state(configuration.kelas2 || '');
	let selectedKelas3 = $state(configuration.kelas3 || '');

	// Synchronize when configuration prop changes
	$effect(() => {
		selectedKelas1 = configuration.kelas1 || '';
		selectedKelas2 = configuration.kelas2 || '';
		selectedKelas3 = configuration.kelas3 || '';
	});

	async function handleSubmit(e) {
		e.preventDefault();
		if (isSaving) return;
		await onSave({
			kelas1: selectedKelas1,
			kelas2: selectedKelas2,
			kelas3: selectedKelas3
		});
	}
</script>

<div class="mb-5 overflow-hidden rounded-2xl border border-slate-200/80 bg-white/95 p-4 shadow-sm backdrop-blur-sm transition-all duration-200">
	<div class="mb-3 flex items-center justify-between">
		<div class="flex items-center gap-2">
			<div class="flex h-8 w-8 items-center justify-center rounded-xl bg-indigo-50 text-indigo-600">
				<i class="fa-solid fa-sliders text-sm"></i>
			</div>
			<div>
				<h2 class="text-sm font-semibold text-slate-900">Atur Angkatan Kelas</h2>
				<p class="text-xs text-slate-500">Petakan tahun masuk untuk tiap tingkatan</p>
			</div>
		</div>
		<button
			type="button"
			onclick={onClose}
			class="flex h-7 w-7 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition"
			aria-label="Tutup pengaturan"
		>
			<i class="fa-solid fa-xmark text-xs"></i>
		</button>
	</div>

	<form onsubmit={handleSubmit} class="space-y-3">
		<div class="grid grid-cols-1 gap-2.5">
			<!-- Kelas 1 -->
			<div class="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/60 p-2.5">
				<div class="flex items-center gap-2">
					<span class="flex h-6 w-6 items-center justify-center rounded-lg bg-blue-100 text-[11px] font-bold text-blue-700">
						1
					</span>
					<div>
						<span class="text-xs font-semibold text-slate-800">Kelas 1</span>
						<span class="ml-1 text-[11px] text-slate-400">(Kelas 7)</span>
					</div>
				</div>
				<select
					bind:value={selectedKelas1}
					disabled={isSaving}
					class="w-36 rounded-lg border border-slate-200 bg-white px-2.5 py-1.5 text-xs font-medium text-slate-700 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50"
				>
					<option value="">Pilih Angkatan</option>
					{#each availableYears as year}
						<option value={year}>Angkatan {year}</option>
					{/each}
				</select>
			</div>

			<!-- Kelas 2 -->
			<div class="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/60 p-2.5">
				<div class="flex items-center gap-2">
					<span class="flex h-6 w-6 items-center justify-center rounded-lg bg-emerald-100 text-[11px] font-bold text-emerald-700">
						2
					</span>
					<div>
						<span class="text-xs font-semibold text-slate-800">Kelas 2</span>
						<span class="ml-1 text-[11px] text-slate-400">(Kelas 8)</span>
					</div>
				</div>
				<select
					bind:value={selectedKelas2}
					disabled={isSaving}
					class="w-36 rounded-lg border border-slate-200 bg-white px-2.5 py-1.5 text-xs font-medium text-slate-700 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50"
				>
					<option value="">Pilih Angkatan</option>
					{#each availableYears as year}
						<option value={year}>Angkatan {year}</option>
					{/each}
				</select>
			</div>

			<!-- Kelas 3 -->
			<div class="flex items-center justify-between rounded-xl border border-slate-100 bg-slate-50/60 p-2.5">
				<div class="flex items-center gap-2">
					<span class="flex h-6 w-6 items-center justify-center rounded-lg bg-purple-100 text-[11px] font-bold text-purple-700">
						3
					</span>
					<div>
						<span class="text-xs font-semibold text-slate-800">Kelas 3</span>
						<span class="ml-1 text-[11px] text-slate-400">(Kelas 9)</span>
					</div>
				</div>
				<select
					bind:value={selectedKelas3}
					disabled={isSaving}
					class="w-36 rounded-lg border border-slate-200 bg-white px-2.5 py-1.5 text-xs font-medium text-slate-700 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 disabled:opacity-50"
				>
					<option value="">Pilih Angkatan</option>
					{#each availableYears as year}
						<option value={year}>Angkatan {year}</option>
					{/each}
				</select>
			</div>
		</div>

		<div class="flex items-center justify-end gap-2 pt-1">
			<button
				type="button"
				onclick={onClose}
				disabled={isSaving}
				class="rounded-xl border border-slate-200 bg-white px-3.5 py-2 text-xs font-semibold text-slate-600 shadow-sm hover:bg-slate-50 disabled:opacity-50 transition"
			>
				Batal
			</button>
			<button
				type="submit"
				disabled={isSaving}
				class="flex items-center gap-1.5 rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white shadow-sm hover:bg-indigo-700 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed transition"
			>
				{#if isSaving}
					<i class="fa-solid fa-circle-notch fa-spin text-xs"></i>
					<span>Menyimpan...</span>
				{:else}
					<i class="fa-solid fa-check text-xs"></i>
					<span>Simpan & Terapkan</span>
				{/if}
			</button>
		</div>
	</form>
</div>
