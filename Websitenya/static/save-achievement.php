<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/helpers-idempotency.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Set CORS headers
setCORSHeaders();

header('Content-Type: application/json');

// Check if request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get the idempotency key from header or JSON input
$idempotencyKey = getIdempotencyKey();

// Check if this request has already been processed
if ($idempotencyKey) {
    $storedResponse = checkIdempotency($idempotencyKey, 'POST');
    if ($storedResponse) {
        // Return the stored response to prevent duplicate processing
        echo json_encode($storedResponse);
        exit;
    }
}

// Get the posted data
$input = json_decode(file_get_contents('php://input'), true);

// Validate required fields
$type = $input['type'] ?? '';
$juz = $input['juz'] ?? null;
$kesalahan = $input['kesalahan'] ?? '';
$nik = $input['nik'] ?? '';

// For syahadah type, juz might be handled differently, so we'll validate after determining the type
if ($type === '' || (!isset($input['kesalahan']) || $kesalahan === '') || $nik === '') {
    $errorResponse = ['success' => false, 'message' => 'Semua field wajib diisi'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(400);
    echo json_encode($errorResponse);
    exit;
}

// Validate juz is provided for all types except syahadah
if (($type !== 'syahadah') && ($juz === null || $juz === '')) {
    $errorResponse = ['success' => false, 'message' => 'Juz wajib diisi'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(400);
    echo json_encode($errorResponse);
    exit;
}

// Validate type
$validTypes = ['ziyadah', 'setengah_juz', 'juziyah', 'syahadah'];
if (!in_array($type, $validTypes)) {
    $errorResponse = ['success' => false, 'message' => 'Tipe pencapaian tidak valid'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(400);
    echo json_encode($errorResponse);
    exit;
}

// Validate juz range (1-30) for all types except syahadah
if (($type !== 'syahadah') && $juz !== null && $juz !== '') {
    if ($juz < 1 || $juz > 30) {
        $errorResponse = ['success' => false, 'message' => 'Juz harus antara 1-30'];

        // Store the response for idempotency if key was provided
        if ($idempotencyKey) {
            storeIdempotency($idempotencyKey, $errorResponse, 'POST');
        }

        http_response_code(400);
        echo json_encode($errorResponse);
        exit;
    }
}

// Validate kesalahan based on type
switch ($type) {
    case 'ziyadah':
        if ($juz === null || $juz === '') {
            $errorResponse = ['success' => false, 'message' => 'Juz wajib diisi untuk ziyadah'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        if (!is_numeric($juz) || $juz < 1 || $juz > 30) {
            $errorResponse = ['success' => false, 'message' => 'Juz harus antara 1-30'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        if (!is_numeric($kesalahan) || $kesalahan < 0 || $kesalahan > 3) {
            $errorResponse = ['success' => false, 'message' => 'Kesalahan untuk ziyadah harus antara 0-3'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        break;
    case 'setengah_juz':
        if ($juz === null || $juz === '') {
            $errorResponse = ['success' => false, 'message' => 'Juz wajib diisi untuk setengah juz'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        if (!is_numeric($juz) || $juz < 1 || $juz > 30) {
            $errorResponse = ['success' => false, 'message' => 'Juz harus antara 1-30'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        if (!is_numeric($kesalahan) || $kesalahan < 0 || $kesalahan > 11) {
            $errorResponse = ['success' => false, 'message' => 'Kesalahan untuk setengah juz harus antara 0-11'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        break;
    case 'juziyah':
        if ($juz === null || $juz === '') {
            $errorResponse = ['success' => false, 'message' => 'Juz wajib diisi untuk juziyah'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        if (!is_numeric($juz) || $juz < 1 || $juz > 30) {
            $errorResponse = ['success' => false, 'message' => 'Juz harus antara 1-30'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        if (!is_numeric($kesalahan) || $kesalahan < 0 || $kesalahan > 20) {
            $errorResponse = ['success' => false, 'message' => 'Kesalahan untuk juziyah harus antara 0-20'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        break;
    case 'syahadah':
        // For syahadah, juz is not applicable and should not be validated
        if (!is_numeric($kesalahan) || $kesalahan < 0 || $kesalahan > 40) {
            $errorResponse = ['success' => false, 'message' => 'Kesalahan untuk syahadah harus antara 0-40'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        break;
}

try {
    // Find the student by NIK
    $student = R::findOne('santri', 'nik = ?', [$nik]);

    if (!$student) {
        $errorResponse = ['success' => false, 'message' => 'Santri tidak ditemukan'];

        // Store the response for idempotency if key was provided
        if ($idempotencyKey) {
            storeIdempotency($idempotencyKey, $errorResponse, 'POST');
        }

        http_response_code(404);
        echo json_encode($errorResponse);
        exit;
    }

    // Create a new achievement record
    $achievement = R::dispense('pencapaian');
    $achievement->type = $type;
    // For syahadah, juz might be null, so only set it if it has a value
    if ($juz !== null && $juz !== '') {
        $achievement->juz = $juz;
    }
    $achievement->kesalahan = $kesalahan;
    $achievement->santri_id = $student->id;
    $achievement->nik = $nik;
    $achievement->created_at = R::isoDateTime();
    $achievement->updated_at = R::isoDateTime();

    // Add specific fields based on type
    if ($type === 'ziyadah') {
        $halaman = $input['halaman'] ?? '';
        if ($halaman === '') {
            $errorResponse = ['success' => false, 'message' => 'Halaman wajib diisi untuk ziyadah'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        $achievement->halaman = $halaman;
    } elseif ($type === 'setengah_juz') {
        $posisi = $input['posisi'] ?? '';
        if ($posisi === '') {
            $errorResponse = ['success' => false, 'message' => 'Posisi wajib diisi untuk setengah juz'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        $achievement->posisi = $posisi;
    } elseif ($type === 'juziyah') {
        $achievement->catatan = $input['catatan'] ?? '';
        $achievement->penguji = $input['penguji'] ?? '';
    } elseif ($type === 'syahadah') {
        $syahadah = $input['syahadah'] ?? '';
        if ($syahadah === '') {
            $errorResponse = ['success' => false, 'message' => 'Syahadah wajib diisi'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
        $achievement->syahadah = $syahadah;
        $achievement->catatan = $input['catatan'] ?? '';
        $achievement->penguji = $input['penguji'] ?? '';
    }

    // Store the achievement
    $id = R::store($achievement);

    // Send WhatsApp notification if this is a juziyah or syahadah achievement
    if ($type === 'juziyah' || $type === 'syahadah') {
        // Get student data
        $studentData = [
            'id' => $student->id,
            'nama_sesuai_kk' => $student->nama_sesuai_kk,
            'tahun_masuk' => $student->tahun_masuk
        ];

        // Prepare achievement data for notification
        $achievementData = [
            'type' => $type,
            'juz' => $juz,
            'kesalahan' => $kesalahan,
            'catatan' => $achievement->catatan ?? '',
            'syahadah' => $achievement->syahadah ?? '',
            'penguji' => $achievement->penguji ?? ''
        ];

        // Include the syahadah value in the achievement data
        if ($type === 'syahadah') {
            $achievementData['syahadah'] = $syahadah;
        }

        // Send WhatsApp notification
        require_once __DIR__ . '/helpers.php';
        $notificationResult = sendAchievementNotification($achievementData, $studentData);

        // Log the notification result (optional)
        error_log("WhatsApp notification result: " . json_encode($notificationResult));
    }

    // Save to webhooksyahadah table if type is syahadah
    if ($type === 'syahadah') {
        $syahadahMap = [
            'pertama' => 1, '1' => 1,
            'kedua' => 2, '2' => 2,
            'ketiga' => 3, '3' => 3,
            'keempat' => 4, '4' => 4,
            'kelima' => 5, '5' => 5,
            'keenam' => 6, '6' => 6
        ];
        $syahadahStr = strtolower((string)$syahadah);
        $syahadahKe = isset($syahadahMap[$syahadahStr]) ? $syahadahMap[$syahadahStr] : intval($syahadah);

        $kesalahanVal = intval($kesalahan);
        if ($kesalahanVal <= 10) {
            $nilai = 'Mumtaz';
        } elseif ($kesalahanVal <= 20) {
            $nilai = 'Jayyid Jiddan';
        } elseif ($kesalahanVal <= 30) {
            $nilai = 'Jayyid';
        } elseif ($kesalahanVal <= 40) {
            $nilai = 'Maqbul';
        } else {
            $nilai = 'Mardud';
        }

        date_default_timezone_set('Asia/Makassar');

        $webhookSyahadah = R::dispense('webhooksyahadah');
        $webhookSyahadah->id_guru = isset($input['id_guru']) && $input['id_guru'] !== '' ? (int)$input['id_guru'] : null;
        $webhookSyahadah->nik_santri = (string)$nik;
        $webhookSyahadah->tanggal = date('Y-m-d H:i:s');
        $webhookSyahadah->id_tahfidz = (int)$id;
        $webhookSyahadah->nama_santri = (string)$student->nama_sesuai_kk;
        $webhookSyahadah->syahadah_ke = (int)$syahadahKe;
        $webhookSyahadah->nilai = (string)$nilai;
        $webhookSyahadah->tahun_masuk = (string)$student->tahun_masuk;
        $webhookSyahadah->kirim_ke_web_utama = false;
        $webhookSyahadah->kirim_ke_web_surat = false;
        R::store($webhookSyahadah);
    }

    // Save to webhookjuziyah table if type is juziyah
    if ($type === 'juziyah') {
        $kesalahanVal = intval($kesalahan);
        if ($kesalahanVal <= 5) {
            $nilai = 'Mumtaz';
        } elseif ($kesalahanVal <= 10) {
            $nilai = 'Jayyid Jiddan';
        } elseif ($kesalahanVal <= 15) {
            $nilai = 'Jayyid';
        } elseif ($kesalahanVal <= 20) {
            $nilai = 'Maqbul';
        } else {
            $nilai = 'Mardud';
        }

        $idGuru = null;
        if (isset($input['id_guru']) && $input['id_guru'] !== '') {
            $idGuru = (int)$input['id_guru'];
        } else {
            $musyrifConn = R::findOne('musyrfst', 'santri_nik = ?', [$nik]);
            if ($musyrifConn && !empty($musyrifConn->musyrif_id)) {
                $idGuru = (int)$musyrifConn->musyrif_id;
            }
        }

        date_default_timezone_set('Asia/Makassar');

        $webhookJuziyah = R::dispense('webhookjuziyah');
        $webhookJuziyah->id_guru = $idGuru;
        $webhookJuziyah->nik_santri = (string)$nik;
        $webhookJuziyah->tanggal = date('Y-m-d H:i:s');
        $webhookJuziyah->id_tahfidz = (int)$id;
        $webhookJuziyah->nama_santri = (string)$student->nama_sesuai_kk;
        $webhookJuziyah->juz = is_numeric($juz) ? (int)$juz : (string)$juz;
        $webhookJuziyah->nilai = (string)$nilai;
        $webhookJuziyah->tahun_masuk = (string)$student->tahun_masuk;
        $webhookJuziyah->kirim_ke_web_surat = false;
        R::store($webhookJuziyah);
    }

    $successResponse = [
        'success' => true,
        'message' => 'Pencapaian berhasil disimpan',
        'id' => $id
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    echo json_encode($successResponse);
} catch (Exception $e) {
    $errorResponse = ['success' => false, 'message' => 'Terjadi kesalahan saat menyimpan pencapaian'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(500);
    echo json_encode($errorResponse);
}
?>