<script>
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { getPhpBackendBaseUrl, generateIdempotencyKey } from '$lib/utils.js';
    import { toast } from 'svelte-sonner';

    let musyrifs = $state([]);
    let isLoading = $state(true);
    let showForm = $state(false);
    let editingMusyrif = $state(null);

    // Form fields
    let nama = $state('');

    onMount(async () => {
        await loadMusyrifs();
    });

    async function loadMusyrifs() {
        try {
            const token = localStorage.getItem('tokenSuper') || '';

            const response = await fetch(`${getPhpBackendBaseUrl()}/get-musyrifs.php`, {
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
                toast.error(result.message || 'Gagal memuat data musyrif tahfidz');
            }
        } catch (error) {
            console.error('Error loading musyrifs:', error);
            toast.error('Terjadi kesalahan saat memuat data musyrif tahfidz');
        } finally {
            isLoading = false;
        }
    }

    function openAddForm() {
        editingMusyrif = null;
        nama = '';
        showForm = true;
    }

    function openEditForm(musyrif) {
        editingMusyrif = musyrif;
        nama = musyrif.nama || '';
        showForm = true;
    }

    function closeForm() {
        showForm = false;
        editingMusyrif = null;
    }

    async function submitNewMusyrif() {
        if (!nama.trim()) {
            toast.error('Nama musyrif harus diisi');
            return;
        }

        const token = localStorage.getItem('tokenSuper') || '';

        try {
            const idempotencyKey = generateIdempotencyKey(); // Generate idempotency key
            const formData = new FormData();
            formData.append('nama', nama);
            formData.append('token', token);
            formData.append('idempotency_key', idempotencyKey); // Add idempotency key to form data

            const response = await fetch(`${getPhpBackendBaseUrl()}/add-musyrif.php`, {
                method: 'POST',
                headers: {
                    'X-IdempotencyKey': idempotencyKey // Add idempotency key to header
                },
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                toast.success('Musyrif baru berhasil ditambahkan');
                await loadMusyrifs();

                // Clear the input field
                nama = '';

                // Play beep sound on success
                playBeep();
            } else {
                toast.error(result.message || 'Gagal menambahkan musyrif');
            }
        } catch (error) {
            console.error('Error submitting new musyrif:', error);
            toast.error('Terjadi kesalahan saat menyimpan data musyrif');
        }
    }

    async function submitForm() {
        if (!nama.trim()) {
            toast.error('Nama musyrif harus diisi');
            return;
        }

        const token = localStorage.getItem('tokenSuper') || '';

        try {
            const idempotencyKey = generateIdempotencyKey(); // Generate idempotency key
            const formData = new FormData();
            formData.append('nama', nama);
            formData.append('token', token);
            formData.append('idempotency_key', idempotencyKey); // Add idempotency key to form data

            if (editingMusyrif) {
                formData.append('id', editingMusyrif.id);
            }

            const url = editingMusyrif
                ? `${getPhpBackendBaseUrl()}/update-musyrif.php`
                : `${getPhpBackendBaseUrl()}/add-musyrif.php`;

            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-Idempotency-Key': idempotencyKey // Add idempotency key to header
                },
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                toast.success(editingMusyrif ? 'Data musyrif berhasil diperbarui' : 'Musyrif baru berhasil ditambahkan');
                closeForm();

                // Clear the input field in case it's used for the inline form
                if (!editingMusyrif) {
                    nama = '';
                }

                await loadMusyrifs();

                // Play beep sound on success
                playBeep();
            } else {
                toast.error(result.message || (editingMusyrif ? 'Gagal memperbarui data musyrif' : 'Gagal menambahkan musyrif'));
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            toast.error('Terjadi kesalahan saat menyimpan data musyrif');
        }
    }

    async function deleteMusyrif(id) {
        if (!confirm('Apakah Anda yakin ingin menghapus musyrif ini?')) {
            return;
        }

        const token = localStorage.getItem('tokenSuper') || '';

        try {
            const response = await fetch(`${getPhpBackendBaseUrl()}/delete-musyrif.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id,
                    token
                })
            });

            const result = await response.json();

            if (result.success) {
                toast.success('Musyrif berhasil dihapus');
                await loadMusyrifs();

                // Play beep sound on success
                playBeep();
            } else {
                toast.error(result.message || 'Gagal menghapus musyrif');
            }
        } catch (error) {
            console.error('Error deleting musyrif:', error);
            toast.error('Terjadi kesalahan saat menghapus musyrif');
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
    <div class="max-w-6xl mx-auto">
        <header class="bg-white rounded-xl shadow p-6 mb-6">
            <div class="flex justify-between items-center">
                <h1 class="text-2xl font-bold text-gray-800">Manajemen Musyrif Tahfidz</h1>
                <div class="flex space-x-3">
                    <a
                        href="/super"
                        class="bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition"
                    >
                        Kembali
                    </a>
                </div>
            </div>

            <!-- Inline Add Form -->
            <div class="mt-6 p-4 bg-blue-50 rounded-lg">
                <h2 class="text-lg font-semibold text-gray-800 mb-3">Tambah Musyrif Baru</h2>
                <div class="flex gap-3">
                    <input
                        type="text"
                        bind:value={nama}
                        class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                        placeholder="Nama lengkap musyrif"
                        onkeypress={(e) => {
                            if (e.key === 'Enter') {
                                e.preventDefault();
                                submitNewMusyrif();
                            }
                        }}
                    />
                    <button
                        onclick={submitNewMusyrif}
                        class="bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded-lg transition disabled:opacity-50"
                        disabled={nama.trim() === ''}
                    >
                        Tambah
                    </button>
                </div>
            </div>
        </header>

        {#if isLoading}
            <div class="bg-white rounded-xl shadow p-8 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-4 text-gray-600">Memuat data musyrif tahfidz...</p>
            </div>
        {:else}
            <div class="bg-white rounded-xl shadow overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nama</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Jumlah Santri</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Aksi</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            {#each musyrifs as musyrif (musyrif.id)}
                                <tr>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm font-medium text-gray-900">{musyrif.nama}</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-gray-900">{musyrif.assigned_students_count || 0}</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                        <button
                                            onclick={() => openEditForm(musyrif)}
                                            class="text-indigo-600 hover:text-indigo-900 mr-3"
                                        >
                                            Edit
                                        </button>
                                        <button
                                            onclick={() => deleteMusyrif(musyrif.id)}
                                            class="text-red-600 hover:text-red-900"
                                        >
                                            Hapus
                                        </button>
                                    </td>
                                </tr>
                            {:else}
                                <tr>
                                    <td colspan="3" class="px-6 py-4 text-center text-sm text-gray-500">
                                        Belum ada data musyrif tahfidz
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            </div>
        {/if}
    </div>

    <!-- Musyrif Form Modal -->
    {#if showForm}
        <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div class="bg-white rounded-xl shadow-lg w-full max-w-md max-h-[90vh] overflow-y-auto">
                <div class="p-6">
                    <h2 class="text-xl font-bold text-gray-800 mb-4">
                        {editingMusyrif ? 'Edit Musyrif' : 'Tambah Musyrif Baru'}
                    </h2>

                    <form onsubmit={x => submitForm(x)}>
                        <div class="mb-4">
                            <label class="block text-sm font-medium text-gray-700 mb-1">Nama *</label>
                            <input
                                type="text"
                                bind:value={nama}
                                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                placeholder="Nama lengkap musyrif"
                            />
                        </div>

                        <div class="flex justify-end space-x-3 pt-4">
                            <button
                                type="button"
                                onclick={closeForm}
                                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                            >
                                Batal
                            </button>
                            <button
                                type="submit"
                                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                                disabled={nama.trim() === ''}
                            >
                                {editingMusyrif ? 'Perbarui' : 'Simpan'}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    {/if}
</div>