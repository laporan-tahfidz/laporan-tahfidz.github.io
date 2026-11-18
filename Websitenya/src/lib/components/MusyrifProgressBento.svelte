<script>
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { getPhpBackendBaseUrl } from '$lib/utils.js';
    import { toast } from 'svelte-sonner';

    let { className = '' } = $props();
    let isLoading = $state(true);
    let musyrifs = $state([]);
    let activeTab = $state(null);
    let progressData = $state({});
    let selectedStudent = $state(null);
    let isModalOpen = $state(false);

    onMount(async () => {
        if (browser) {
            try {
                const response = await fetch(`${getPhpBackendBaseUrl()}/get-musyrif-progress-public.php`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({})
                });

                const result = await response.json();

                if (result.success) {
                    musyrifs = result.data;
                    if (musyrifs.length > 0) {
                        activeTab = musyrifs[0].id;
                        progressData = result.data.reduce((acc, musyrif) => {
                            acc[musyrif.id] = musyrif.students;
                            return acc;
                        }, {});
                    }
                } else {
                    toast.error(`Gagal memuat data: ${result.message}`);
                }
            } catch (error) {
                console.error('Error loading musyrif progress:', error);
                toast.error('Terjadi kesalahan saat memuat data kemajuan santri');
            } finally {
                isLoading = false;
            }
        } else {
            isLoading = false;
        }
    });

    function setActiveTab(musyrifId) {
        activeTab = musyrifId;
    }

    // Function to show student achievement history
    function showStudentAchievementHistory(student) {
        console.log('Opening achievement history for student:', student);

        // Use the student sidebar
        if (window.studentSidebar) {
            const studentId = student.id || student.santri_id || student.nik;
            window.studentSidebar.showSidebar(studentId, student.nama_sesuai_kk || student.nama);
        } else {
            console.error('Student sidebar not available');
        }
    }

    // Function to close the modal
    function closeModal() {
        isModalOpen = false;
        selectedStudent = null;
    }

    // Function to get the CSS class for a cell based on progress
    function getProgressClass(status) {
        switch (status) {
            case 'tested-dark':
                return 'bg-green-700 text-white';
            case 'tested-medium':
                return 'bg-green-500 text-white';
            case 'tested-light':
                return 'bg-green-300 text-green-950';
            case 'tested-failed':
                return 'bg-red-500 text-white';
            case 'achieved':
                return 'bg-gray-400 text-white';
            default:
                return 'bg-gray-100 text-gray-700';
        }
    }

    // Function to get tooltip text for a cell
    function getTooltipText(status) {
        switch (status) {
            case 'tested-dark':
                return 'Sudah dites (3+ kali, Lancar)';
            case 'tested-medium':
                return 'Sudah dites (2 kali, Lancar)';
            case 'tested-light':
                return 'Sudah dites (1 kali, Lancar)';
            case 'tested-failed':
                return 'Sudah dites (Tidak Lancar)';
            case 'achieved':
                return 'Sudah setor';
            default:
                return 'Belum setor';
        }
    }
</script>

<div class={className}>
    {#if isLoading}
        <div class="flex items-center justify-center p-8">
            <div class="inline-block h-8 w-8 animate-spin rounded-full border-t-2 border-b-2 border-blue-500"></div>
        </div>
    {:else}
        <!-- Tab Navigation for Musyrifs -->
        <div class="mb-4 border-b border-gray-200">
            <nav class="-mb-px flex space-x-8 overflow-x-auto" aria-label="Tabs">
                {#each musyrifs as musyrif}
                    <button
                        onclick={() => setActiveTab(musyrif.id)}
                        class={`whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm ${
                            activeTab === musyrif.id
                                ? 'border-blue-500 text-blue-600'
                                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                        }`}
                    >
                        {musyrif.nama}
                    </button>
                {/each}
            </nav>
        </div>

        <!-- Progress Table for Selected Musyrif -->
        <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                    <tr>
                        <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider sticky left-0 bg-gray-50 z-10">
                            Nama Santri
                        </th>
                        {#each Array.from({ length: 30 }, (_, i) => i + 1) as juz}
                            <th scope="col" class="px-2 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider min-w-[32px]">
                                {juz}
                            </th>
                        {/each}
                    </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                    {#if activeTab && progressData[activeTab]}
                        {#each progressData[activeTab] as student}
                            <tr>
                                <td class="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900 sticky left-0 bg-white z-10 min-w-[150px]">
                                    <button 
                                        onclick={() => showStudentAchievementHistory(student)} 
                                        class="hover:underline text-left text-blue-600 font-medium hover:text-blue-800 transition-colors cursor-pointer"
                                    >
                                        {student.nama_sesuai_kk}
                                    </button>
                                </td>
                                {#each Array.from({ length: 30 }, (_, i) => i + 1) as juz}
                                    <td class="p-1 text-center">
                                        <div 
                                            class={`w-6 h-6 mx-auto rounded flex items-center justify-center ${getProgressClass(student.progress[juz])}`}
                                            title={getTooltipText(student.progress[juz])}
                                        ></div>
                                    </td>
                                {/each}
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>

        <!-- Legend -->
        <div class="mt-4 flex flex-wrap gap-4 text-sm">
            <div class="flex items-center">
                <div class="w-4 h-4 rounded bg-gray-100 mr-2"></div>
                <span>Belum setor</span>
            </div>
            <div class="flex items-center">
                <div class="w-4 h-4 rounded bg-gray-400 mr-2"></div>
                <span>Sudah setor</span>
            </div>
            <div class="flex items-center">
                <div class="w-4 h-4 rounded bg-green-300 mr-2"></div>
                <span>Lancar (1x)</span>
            </div>
            <div class="flex items-center">
                <div class="w-4 h-4 rounded bg-green-500 mr-2"></div>
                <span>Lancar (2x)</span>
            </div>
            <div class="flex items-center">
                <div class="w-4 h-4 rounded bg-green-700 mr-2"></div>
                <span>Lancar (3+x)</span>
            </div>
            <div class="flex items-center">
                <div class="w-4 h-4 rounded bg-red-500 mr-2"></div>
                <span>Tidak Lancar</span>
            </div>
        </div>
    {/if}

    <!-- Modal is now handled globally -->
</div>