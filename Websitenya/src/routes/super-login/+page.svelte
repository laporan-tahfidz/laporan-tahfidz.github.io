<script>
    import { onMount } from 'svelte';
    import { browser } from '$app/environment';
    import { goto } from '$app/navigation';
    import { getPhpBackendBaseUrl, generateIdempotencyKey } from '$lib/utils.js';
    import { toast } from 'svelte-sonner';

    let phoneNumber = $state('');
    let otp = $state('');
    let isLoading = $state(false);
    let isSendingOtp = $state(false);
    let showOtpInput = $state(false);
    let token = $state('');

    const validNumbers = ['081545143654', '082274180206', '085111037215'];

    async function sendOtp() {
        if (!phoneNumber) {
            toast.error('Nomor WhatsApp harus diisi');
            return;
        }

        // Format phone number to Indonesian format if needed
        let formattedPhone = phoneNumber.replace(/\D/g, '');
        if (formattedPhone.startsWith('62')) {
            formattedPhone = '62' + formattedPhone.substring(2);
        } else if (formattedPhone.startsWith('0')) {
            formattedPhone = '62' + formattedPhone.substring(1);
        } else if (!formattedPhone.startsWith('62')) {
            formattedPhone = '62' + formattedPhone;
        }

        // Check against valid numbers in both formats (original and formatted)
        const originalFormat = phoneNumber.replace(/\D/g, '');
        if (!validNumbers.includes(originalFormat) && !validNumbers.includes(formattedPhone.replace('62', '0'))) {
            toast.error('Nomor WhatsApp tidak valid untuk akses super admin');
            return;
        }

        isSendingOtp = true;

        try {
            const idempotencyKey = generateIdempotencyKey(); // Generate idempotency key
            const response = await fetch(`${getPhpBackendBaseUrl()}/send-otp.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Idempotency-Key': idempotencyKey // Add idempotency key to header
                },
                body: JSON.stringify({
                    phone: `+${formattedPhone}`,
                    idempotency_key: idempotencyKey // Add idempotency key to body as well
                })
            });

            const result = await response.json();

            if (result.success) {
                toast.success('OTP telah dikirim ke nomor WhatsApp Anda');
                showOtpInput = true;
            } else {
                toast.error(result.message || 'Gagal mengirim OTP');
            }
        } catch (error) {
            toast.error('Terjadi kesalahan saat mengirim OTP');
            console.error('Error sending OTP:', error);
        } finally {
            isSendingOtp = false;
        }
    }

    async function verifyOtp() {
        if (!otp) {
            toast.error('OTP harus diisi');
            return;
        }

        isLoading = true;

        try {
            // Format phone number consistently with sendOtp function
            let formattedPhone = phoneNumber.replace(/\D/g, '');
            if (formattedPhone.startsWith('62')) {
                formattedPhone = '62' + formattedPhone.substring(2);
            } else if (formattedPhone.startsWith('0')) {
                formattedPhone = '62' + formattedPhone.substring(1);
            } else if (!formattedPhone.startsWith('62')) {
                formattedPhone = '62' + formattedPhone;
            }

            const idempotencyKey = generateIdempotencyKey(); // Generate idempotency key
            const response = await fetch(`${getPhpBackendBaseUrl()}/verify-otp.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Idempotency-Key': idempotencyKey // Add idempotency key to header
                },
                body: JSON.stringify({
                    phone: `+${formattedPhone}`,
                    otp,
                    idempotency_key: idempotencyKey // Add idempotency key to body as well
                })
            });

            const result = await response.json();

            if (result.success) {
                token = result.token;

                if (browser) {
                    localStorage.setItem('tokenSuper', result.token);
                }

                toast.success('Login berhasil!');
                setTimeout(() => {
                    goto('/super');
                }, 1000);

                // Play beep sound on success
                playBeep();
            } else {
                toast.error(result.message || 'OTP tidak valid');
            }
        } catch (error) {
            toast.error('Terjadi kesalahan saat verifikasi OTP');
            console.error('Error verifying OTP:', error);
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

    // Play beep when showing success toast
    $effect(() => {
        if (showOtpInput) {
            playBeep();
        }
    });
</script>

<div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
    <div class="w-full max-w-md bg-white rounded-xl shadow-lg p-8 space-y-6">
        <div class="text-center">
            <h1 class="text-2xl font-bold text-gray-800">Login Super Admin</h1>
            <p class="text-gray-600 mt-2">Masukkan nomor WhatsApp Anda untuk mendapatkan OTP</p>
        </div>

        <div class="space-y-4">
            <div>
                <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Nomor WhatsApp</label>
                <input
                    id="phone"
                    type="tel"
                    bind:value={phoneNumber}
                    placeholder="Contoh: 081234567890"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                    disabled={showOtpInput || isSendingOtp || isLoading}
                />
            </div>

            {#if showOtpInput}
                <div>
                    <label for="otp" class="block text-sm font-medium text-gray-700 mb-1">OTP</label>
                    <input
                        id="otp"
                        type="text"
                        bind:value={otp}
                        placeholder="Masukkan kode OTP"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                        maxlength="6"
                        disabled={isLoading}
                    />
                </div>
            {/if}

            <button
                type="button"
                onclick={() => {
                    if (!showOtpInput) {
                        sendOtp();
                    } else {
                        verifyOtp();
                    }
                }}
                class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={isSendingOtp || isLoading}
            >
                {#if isSendingOtp}
                    Mengirim OTP...
                {:else if isLoading && showOtpInput}
                    Memverifikasi...
                {:else if showOtpInput}
                    Verifikasi OTP
                {:else}
                    Kirim OTP
                {/if}
            </button>
        </div>

        <div class="mt-6 pt-6 border-t border-gray-200">
            <p class="text-xs text-gray-500 text-center">
                Hanya nomor berikut yang dapat digunakan untuk akses super admin:
            </p>
            <div class="flex justify-center gap-4 mt-2">
                {#each validNumbers as number}
                    <span class="text-xs bg-gray-100 px-2 py-1 rounded">{number}</span>
                {/each}
            </div>
        </div>
    </div>
</div>