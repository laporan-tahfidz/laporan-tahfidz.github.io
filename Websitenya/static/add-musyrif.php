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

// Get the idempotency key from header or POST data
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
$data = $_POST;
$token = $data['token'] ?? '';

// Verify the token if provided
if ($token && !verifyToken($token)) {
    $errorResponse = ['success' => false, 'message' => 'Unauthorized'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(401);
    echo json_encode($errorResponse);
    exit;
}

// Get the form data
$nama = trim($data['nama'] ?? '');

// Validate required fields
if (empty($nama)) {
    $errorResponse = ['success' => false, 'message' => 'Nama musyrif harus diisi'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(400);
    echo json_encode($errorResponse);
    exit;
}

try {
    // Check if a musyrif with the same name already exists
    $existingMusyrif = R::findOne('musyrif', 'nama = ?', [$nama]);

    if ($existingMusyrif) {
        $errorResponse = ['success' => false, 'message' => 'Nama musyrif sudah terdaftar'];

        // Store the response for idempotency if key was provided
        if ($idempotencyKey) {
            storeIdempotency($idempotencyKey, $errorResponse, 'POST');
        }

        http_response_code(400);
        echo json_encode($errorResponse);
        exit;
    }

    // Create a new musyrif
    $musyrif = R::dispense('musyrif');
    $musyrif->nama = $nama;
    $musyrif->created_at = R::isoDateTime();
    $musyrif->updated_at = R::isoDateTime();

    // Store the musyrif in the database
    $id = R::store($musyrif);

    $successResponse = [
        'success' => true,
        'message' => 'Musyrif berhasil ditambahkan',
        'data' => [
            'id' => $id,
            'nama' => $musyrif->nama,
            'created_at' => $musyrif->created_at,
            'updated_at' => $musyrif->updated_at
        ]
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    echo json_encode($successResponse);
} catch (Exception $e) {
    $errorResponse = ['success' => false, 'message' => 'Terjadi kesalahan saat menyimpan data'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    http_response_code(500);
    echo json_encode($errorResponse);
}
?>