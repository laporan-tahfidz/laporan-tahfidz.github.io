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
$juz = $input['juz'] ?? '';
$nik = $input['nik'] ?? '';
$status = $input['status'] ?? 'lancar';

if (!in_array($status, ['lancar', 'tidak_lancar'])) {
    $status = 'lancar';
}

if (empty($juz) || empty($nik)) {
    $errorResponse = ['success' => false, 'message' => 'Juz dan NIK wajib diisi'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(400);
    echo json_encode($errorResponse);
    exit;
}

// Validate juz range (1-30)
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

    // Create a new test record
    $test = R::dispense('tes');
    $test->juz = $juz;
    $test->status = $status;
    $test->santri_id = $student->id;
    $test->nik = $nik;
    $test->created_at = R::isoDateTime();
    $test->updated_at = R::isoDateTime();

    // Store the test
    $id = R::store($test);

    $successResponse = [
        'success' => true,
        'message' => 'Tes berhasil disimpan',
        'id' => $id
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    echo json_encode($successResponse);
} catch (Exception $e) {
    $errorResponse = ['success' => false, 'message' => 'Terjadi kesalahan saat menyimpan tes'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(500);
    echo json_encode($errorResponse);
}
?>