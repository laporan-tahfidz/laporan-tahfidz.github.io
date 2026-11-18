<script>
    import { onMount } from 'svelte';
    import { getPhpBackendBaseUrl } from '$lib/utils.js';
    import { toast } from 'svelte-sonner';
    import { formatDateMakassar, formatTimeMakassar } from '$lib/utils/timezone.js';

    let isVisible = $state(false);
    let studentId = $state(null);
    let studentName = $state('');
    let achievements = $state([]);
    let isLoading = $state(false);
    let isFixingJuz = $state(false);

    // Function to play beep sound
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

    // Global reference to control the sidebar from anywhere
    let instance = null;

    // Function to show the sidebar with student data
    function showSidebar(id, name) {
        studentId = id;
        studentName = name;
        isVisible = true;
        loadAchievements();
    }

    // Function to hide the sidebar
    function hideSidebar() {
        isVisible = false;
        studentId = null;
        studentName = '';
        achievements = [];
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

    // Expose the functions globally
    onMount(() => {
        // Store reference to this instance
        instance = { showSidebar, hideSidebar };

        // Make it globally accessible
        if (typeof window !== 'undefined') {
            window.studentSidebar = instance;
        }

        return () => {
            if (window.studentSidebar === instance) {
                window.studentSidebar = null;
            }
        };
    });
</script>

{#if isVisible}
    <div
        class="fixed top-4 left-4 w-96 bg-white shadow-2xl z-50 border-r border-gray-200"
        style="min-height: 200px;"
    >
        <div class="flex flex-col min-h-[200px]">
            <div class="bg-blue-600 text-white p-4 flex justify-between items-center">
                <h3 class="text-lg font-semibold">Riwayat Pencapaian - {studentName}</h3>
                <button
                    class="text-white hover:text-gray-200 focus:outline-none"
                    onclick={hideSidebar}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

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

            <div class="overflow-y-auto max-h-[60vh] p-4 bg-gray-50 flex-grow">
                {#if isLoading}
                    <div class="text-center py-8">
                        <div class="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
                        <p class="mt-2 text-gray-600">Memuat data pencapaian...</p>
                    </div>
                {:else}
                    {#if achievements.length > 0}
                        <div class="space-y-3">
                            {#each achievements as achievement (achievement.id)}
                                <div class="bg-white rounded-lg p-3 border border-gray-200 shadow-sm">
                                    <div class="flex justify-between items-start">
                                        <div>
                                            <span class="inline-block px-2 py-1 text-xs font-semibold rounded-full
                                                {achievement.type === 'ziyadah' ? 'bg-blue-100 text-blue-800' :
                                                 achievement.type === 'setengah_juz' ? 'bg-green-100 text-green-800' :
                                                 achievement.type === 'juziyah' ? 'bg-yellow-100 text-yellow-800' :
                                                 'bg-purple-100 text-purple-800'}">
                                                {achievement.type === 'ziyadah' ? 'Ziyadah' :
                                                 achievement.type === 'setengah_juz' ? 'Setengah Juz' :
                                                 achievement.type === 'juziyah' ? 'Juziyah' : 'Syahadah'}
                                            </span>
                                            <h4 class="font-medium mt-2 text-sm">
                                                {#if achievement.type === 'ziyadah'}
                                                    Juz: {achievement.juz}, Halaman: {achievement.halaman}
                                                {:else if achievement.type === 'setengah_juz'}
                                                    Juz: {achievement.juz}, Posisi: {achievement.posisi}
                                                {:else if achievement.type === 'juziyah'}
                                                    Juz: {achievement.juz}
                                                {:else}
                                                    Tingkatan: {achievement.syahadah}
                                                {/if}
                                            </h4>
                                            {#if achievement.catatan}
                                                <p class="text-xs text-gray-600 mt-1">Catatan: {achievement.catatan}</p>
                                            {/if}
                                        </div>
                                        <div class="text-right text-xs text-gray-500">
                                            <div>{formatDateMakassar(achievement.created_at)}</div>
                                            <div class="mt-1">{formatTimeMakassar(achievement.created_at)}</div>
                                            {#if achievement.kesalahan !== null}
                                                <div class="mt-1 text-red-600">Kesalahan: {achievement.kesalahan}</div>
                                            {/if}
                                        </div>
                                    </div>
                                </div>
                            {/each}
                        </div>
                    {:else}
                        <div class="text-center py-12 text-gray-500">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <p class="mt-4 text-lg">Belum ada riwayat pencapaian</p>
                            <p class="mt-1 text-sm">Data pencapaian untuk santri ini masih kosong</p>
                        </div>
                    {/if}
                {/if}
            </div>

            <div class="bg-gray-100 px-4 py-3 border-t border-gray-200">
                <button
                    class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none transition"
                    onclick={hideSidebar}
                >
                    Tutup
                </button>
            </div>
        </div>
    </div>
{/if}