<script>
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';
    import { getPhpBackendBaseUrl } from '$lib/utils.js';

    let { className = '', title = 'Placeholder Title', description = 'Placeholder Description', attentionType = 'coordinator' } = $props();
    let attentionData = $state([]);
    let isLoading = $state(true);
    let selectedStudent = $state(null);
    let isModalOpen = $state(false);

    onMount(async () => {
        if (browser) {
            await loadAttentionNeededStudents();
        } else {
            isLoading = false;
        }
    });

    async function loadAttentionNeededStudents() {
        try {
            const token = localStorage.getItem('tokenSuper') || '';

            const response = await fetch(`${getPhpBackendBaseUrl()}/get-attention-needed-students.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token })
            });

            const result = await response.json();

            if (result.success) {
                if (attentionType === 'coordinator') {
                    attentionData = result.coordinator_attention;
                } else {
                    attentionData = result.musyrif_attention;
                }
            } else {
                console.error('Failed to load attention needed students:', result.message);
            }
        } catch (error) {
            console.error('Error loading attention needed students:', error);
        } finally {
            isLoading = false;
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

    // Function to show student achievement history
    function showStudentAchievementHistory(student) {
        console.log('Opening achievement history for student:', student);

        // Use the student sidebar
        if (window.studentSidebar) {
            const studentId = student.id || student.santri_id || student.nik;
            window.studentSidebar.showSidebar(studentId, student.nama);
        } else {
            console.error('Student sidebar not available');
        }
    }

    // Function to close the modal
    function closeModal() {
        isModalOpen = false;
        selectedStudent = null;
    }
</script>

<div class={className}>
    <div class="bg-white rounded-xl shadow p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">{title}</h2>
        <p class="text-gray-600 mb-6">{description}</p>

        {#if isLoading}
            <div class="flex justify-center items-center py-8">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
        {:else}
            {#if attentionData.length > 0}
                {#each attentionData as group}
                    <div class="mb-6">
                        <h3 class="text-lg font-medium text-gray-800 mb-3">{group.musyrif_nama}</h3>
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Nama
                                        </th>
                                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Keterangan
                                        </th>
                                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Lama Persiapan
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    {#each group.students as student}
                                        <tr>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                                <button
                                                    class="text-blue-600 hover:text-blue-800 underline cursor-pointer"
                                                    onclick={() => showStudentAchievementHistory(student)}
                                                >
                                                    {student.nama}
                                                </button>
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {student.keterangan}
                                            </td>
                                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                                {student.lama_persiapan}
                                            </td>
                                        </tr>
                                    {/each}
                                </tbody>
                            </table>
                        </div>
                    </div>
                {/each}
            {:else}
                <div class="bg-green-50 border-l-4 border-green-400 p-4">
                    <div class="flex">
                        <div class="flex-shrink-0">
                            <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                            </svg>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm text-green-700">
                                Tidak ada santri yang perlu perhatian saat ini.
                            </p>
                        </div>
                    </div>
                </div>
            {/if}
        {/if}
    </div>

    <!-- Modal is now handled globally -->
</div>