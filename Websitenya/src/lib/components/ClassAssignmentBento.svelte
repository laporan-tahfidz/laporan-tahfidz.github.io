<script>
    import { cn } from '$lib/utils.js';
    import { onMount } from 'svelte';

    // Props using $props() for Svelte 5 runes mode
    let {
        classConfig = {
            kelas1: '',
            kelas2: '',
            kelas3: ''
        },
        availableYears = [],
        onSave = () => {},
        onAutoConfigure = () => {},
        isSaving = false,
        className = ''
    } = $props();

    // Local state
    let selectedKelas1 = $state(classConfig.kelas1);
    let selectedKelas2 = $state(classConfig.kelas2);
    let selectedKelas3 = $state(classConfig.kelas3);

    // Update local state when props change
    $effect(() => {
        selectedKelas1 = classConfig.kelas1;
        selectedKelas2 = classConfig.kelas2;
        selectedKelas3 = classConfig.kelas3;
    });

    // Handle save
    function handleSave() {
        const newConfig = {
            kelas1: selectedKelas1,
            kelas2: selectedKelas2,
            kelas3: selectedKelas3
        };
        onSave(newConfig);
    }

    // Handle auto configure
    function handleAutoConfigure() {
        onAutoConfigure();
    }

    // Get display text for class
    function getClassDisplay(year, defaultText) {
        return year ? `Tahun Masuk: ${year}` : defaultText;
    }
</script>

<div class={cn('grid grid-cols-1 md:grid-cols-3 gap-6 w-full', className)}>
    <!-- Kelas 1 Bento Card -->
    <div class="bg-white rounded-2xl shadow-lg p-6 border border-blue-100 hover:shadow-xl transition-shadow duration-300 flex flex-col">
        <div class="flex items-center gap-3 mb-4">
            <div class="bg-blue-100 p-3 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">Kelas 1</h3>
        </div>
        
        <p class="text-gray-600 mb-4">Tentukan tahun masuk untuk kelas 1</p>
        
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Tahun Masuk
            </label>
            <select
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                bind:value={selectedKelas1}
            >
                <option value="">Pilih tahun</option>
                {#each availableYears as year}
                    <option value={year}>{year}</option>
                {/each}
            </select>
        </div>
        
        <div class="mt-auto pt-4 border-t border-gray-100">
            <p class="text-sm text-gray-500">
                {getClassDisplay(selectedKelas1, 'Belum ditentukan')}
            </p>
        </div>
    </div>

    <!-- Kelas 2 Bento Card -->
    <div class="bg-white rounded-2xl shadow-lg p-6 border border-green-100 hover:shadow-xl transition-shadow duration-300 flex flex-col">
        <div class="flex items-center gap-3 mb-4">
            <div class="bg-green-100 p-3 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">Kelas 2</h3>
        </div>
        
        <p class="text-gray-600 mb-4">Tentukan tahun masuk untuk kelas 2</p>
        
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Tahun Masuk
            </label>
            <select
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
                bind:value={selectedKelas2}
            >
                <option value="">Pilih tahun</option>
                {#each availableYears as year}
                    <option value={year}>{year}</option>
                {/each}
            </select>
        </div>
        
        <div class="mt-auto pt-4 border-t border-gray-100">
            <p class="text-sm text-gray-500">
                {getClassDisplay(selectedKelas2, 'Belum ditentukan')}
            </p>
        </div>
    </div>

    <!-- Kelas 3 Bento Card -->
    <div class="bg-white rounded-2xl shadow-lg p-6 border border-purple-100 hover:shadow-xl transition-shadow duration-300 flex flex-col">
        <div class="flex items-center gap-3 mb-4">
            <div class="bg-purple-100 p-3 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800">Kelas 3</h3>
        </div>
        
        <p class="text-gray-600 mb-4">Tentukan tahun masuk untuk kelas 3</p>
        
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Tahun Masuk
            </label>
            <select
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                bind:value={selectedKelas3}
            >
                <option value="">Pilih tahun</option>
                {#each availableYears as year}
                    <option value={year}>{year}</option>
                {/each}
            </select>
        </div>
        
        <div class="mt-auto pt-4 border-t border-gray-100">
            <p class="text-sm text-gray-500">
                {getClassDisplay(selectedKelas3, 'Belum ditentukan')}
            </p>
        </div>
    </div>
</div>

<!-- Action Buttons -->
<div class="mt-8 flex flex-wrap gap-4">
    <button
        onclick={handleSave}
        disabled={isSaving}
        class="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
    >
        {#if isSaving}
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Menyimpan...
        {:else}
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            Simpan Konfigurasi
        {/if}
    </button>

    <button
        onclick={handleAutoConfigure}
        disabled={isSaving}
        class="bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
    >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01-.61-1.276z" clip-rule="evenodd" />
        </svg>
        Konfigurasi Otomatis
    </button>
</div>