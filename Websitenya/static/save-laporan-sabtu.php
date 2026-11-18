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
$murajaahEntries = $input['murajaah_entries'] ?? [];
$hafalanEntries = $input['hafalan_entries'] ?? [];
$santriId = $input['santri_id'] ?? '';
$nik = $input['nik'] ?? '';

// Validate input data
if (empty($murajaahEntries) && empty($hafalanEntries)) {
    $errorResponse = ['success' => false, 'message' => 'Setidaknya satu dari Murajaah atau Hafalan Tidak Lancar harus diisi'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(400);
    echo json_encode($errorResponse);
    exit;
}

// Validate required santri info
if (empty($santriId) || empty($nik)) {
    $errorResponse = ['success' => false, 'message' => 'Informasi santri tidak lengkap'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(400);
    echo json_encode($errorResponse);
    exit;
}

// If Murajaah entries are provided, validate them
if (!empty($murajaahEntries)) {
    foreach ($murajaahEntries as $entry) {
        if (!isset($entry['juz'])) {
            $errorResponse = ['success' => false, 'message' => 'Data Murajaah tidak lengkap'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }

        if (!is_numeric($entry['juz']) || $entry['juz'] < 1 || $entry['juz'] > 30) {
            $errorResponse = ['success' => false, 'message' => 'Juz Murajaah tidak valid'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
    }
}

// If Hafalan entries are provided, validate them
if (!empty($hafalanEntries)) {
    foreach ($hafalanEntries as $entry) {
        if (!isset($entry['juz']) || !isset($entry['startPage']) || !isset($entry['endPage'])) {
            $errorResponse = ['success' => false, 'message' => 'Data Hafalan Tidak Lancar tidak lengkap'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }

        if (!is_numeric($entry['juz']) || $entry['juz'] < 1 || $entry['juz'] > 30) {
            $errorResponse = ['success' => false, 'message' => 'Juz Hafalan Tidak Lancar tidak valid'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }

        // Validate page format (should be like "1A", "2B", etc.)
        if (!preg_match('/^[1-9][0-9]?[AB]$/', $entry['startPage']) || !preg_match('/^[1-9][0-9]?[AB]$/', $entry['endPage'])) {
            $errorResponse = ['success' => false, 'message' => 'Format halaman Hafalan Tidak Lancar tidak valid'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }

        // Extract page numbers and ayah letters
        preg_match('/^([1-9][0-9]?)([AB])$/', $entry['startPage'], $startMatches);
        preg_match('/^([1-9][0-9]?)([AB])$/', $entry['endPage'], $endMatches);

        $startPageNum = intval($startMatches[1]);
        $startAyah = $startMatches[2];
        $endPageNum = intval($endMatches[1]);
        $endAyah = $endMatches[2];

        // Validate page numbers
        if ($startPageNum < 1 || $startPageNum > 10 || $endPageNum < 1 || $endPageNum > 10) {
            $errorResponse = ['success' => false, 'message' => 'Nomor halaman harus antara 1-10'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }

        // Check if start page is greater than end page
        if ($startPageNum > $endPageNum) {
            $errorResponse = ['success' => false, 'message' => 'Halaman awal tidak boleh lebih besar dari halaman akhir'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }

        // If pages are equal, check ayah ordering
        if ($startPageNum === $endPageNum && $startAyah > $endAyah) {
            $errorResponse = ['success' => false, 'message' => 'Ayat awal tidak boleh lebih besar dari ayat akhir'];

            // Store the response for idempotency if key was provided
            if ($idempotencyKey) {
                storeIdempotency($idempotencyKey, $errorResponse, 'POST');
            }

            http_response_code(400);
            echo json_encode($errorResponse);
            exit;
        }
    }
}

try {
    // Create a new laporan sabtu record
    $report = R::dispense('laporansabtu');
    $report->santri_id = $santriId;
    $report->nik = $nik;
    $report->created_at = R::isoDateTime();

    // Store the murajaah and hafalan entries as JSON
    $report->murajaahentries = json_encode($murajaahEntries);
    $report->hafalanentries = json_encode($hafalanEntries);

    // Save the report
    $reportId = R::store($report);

    $successResponse = [
        'success' => true,
        'message' => 'Laporan Sabtu berhasil disimpan',
        'report_id' => $reportId
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    // Return success response
    echo json_encode($successResponse);
} catch (Exception $e) {
    $errorResponse = ['success' => false, 'message' => 'Terjadi kesalahan saat menyimpan laporan: ' . $e->getMessage()];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(500);
    echo json_encode($errorResponse);
}
?>