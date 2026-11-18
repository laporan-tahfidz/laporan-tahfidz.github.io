<script>
    import { toast } from 'svelte-sonner';
    import { getPhpBackendBaseUrl, generateIdempotencyKey } from '$lib/utils.js';

    let { isOpen = false, onClose, onVerified, actionDescription = '' } = $props();
    let phoneNumber = $state('');
    let otp = $state('');
    let isLoading = $state(false);
    let isSendingOtp = $state(false);
    let showOtpInput = $state(false);

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
                toast.success('Verifikasi berhasil!');
                
                // Play beep sound on success
                playBeep();
                
                // Call the callback function to indicate successful verification
                if (onVerified) {
                    onVerified();
                }
                
                // Close the modal
                handleClose();
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

    function handleClose() {
        // Reset state
        phoneNumber = '';
        otp = '';
        showOtpInput = false;
        
        // Call the close callback
        if (onClose) {
            onClose();
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
    
    // Handle Escape key press
    $effect(() => {
        if (isOpen) {
            const handleEsc = (e) => {
                if (e.key === 'Escape') {
                    handleClose();
                }
            };
            
            window.addEventListener('keydown', handleEsc);
            
            return () => {
                window.removeEventListener('keydown', handleEsc);
            };
        }
    });
</script>

{#if isOpen}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
        <div class="bg-white rounded-xl shadow-xl w-full max-w-md p-6">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold text-gray-800">Verifikasi Akses</h2>
                <button 
                    onclick={handleClose}
                    class="text-gray-500 hover:text-gray-700"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            
            {#if actionDescription}
                <p class="text-gray-600 mb-4">Anda mencoba mengakses: <strong>{actionDescription}</strong>. Silakan verifikasi dengan OTP.</p>
            {/if}
            
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

                <div class="flex gap-3 pt-2">
                    <button
                        type="button"
                        onclick={() => {
                            if (!showOtpInput) {
                                sendOtp();
                            } else {
                                verifyOtp();
                            }
                        }}
                        class="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
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
                    
                    <button
                        type="button"
                        onclick={handleClose}
                        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100 transition"
                    >
                        Batal
                    </button>
                </div>
            </div>

            <div class="mt-6 pt-4 border-t border-gray-200">
                <p class="text-xs text-gray-500 text-center">
                    Hanya nomor berikut yang dapat digunakan untuk akses super admin:
                </p>
                <div class="flex justify-center gap-2 mt-2 flex-wrap">
                    {#each validNumbers as number}
                        <span class="text-xs bg-gray-100 px-2 py-1 rounded">{number}</span>
                    {/each}
                </div>
            </div>
        </div>
    </div>
{/if}