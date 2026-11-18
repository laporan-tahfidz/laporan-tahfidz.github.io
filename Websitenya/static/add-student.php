<?php
// add-student.php - Add a new student

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/helpers-idempotency.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
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

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    $errorResponse = ['success' => false, 'message' => 'Unauthorized'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

try {
    initDB();

    // Get form data
    $nama = $_POST['nama'] ?? '';
    $tanggal_lahir = $_POST['tanggal_lahir'] ?? '';
    $jenis_kelamin = $_POST['jenis_kelamin'] ?? 'laki-laki';
    $alamat = $_POST['alamat'] ?? '';
    $nomor_hp = $_POST['nomor_hp'] ?? '';
    $email = $_POST['email'] ?? '';

    // Validate required fields
    if (empty($nama)) {
        $errorResponse = ['success' => false, 'message' => 'Nama is required'];

        // Store the response for idempotency if key was provided
        if ($idempotencyKey) {
            storeIdempotency($idempotencyKey, $errorResponse, 'POST');
        }

        echo json_encode($errorResponse);
        exit;
    }

    // Handle file upload if present
    $foto = null;
    if (isset($_FILES['foto']) && $_FILES['foto']['error'] === UPLOAD_ERR_OK) {
        $foto = handleFileUpload($_FILES['foto']);
    }

    // Create new student bean
    $student = R::dispense('santri');
    $student->nama = $nama;
    $student->tanggal_lahir = $tanggal_lahir;
    $student->jenis_kelamin = $jenis_kelamin;
    $student->alamat = $alamat;
    $student->nomor_hp = $nomor_hp;
    $student->email = $email;
    $student->foto = $foto;
    $student->created_at = date('Y-m-d H:i:s');
    $student->updated_at = date('Y-m-d H:i:s');

    // Store the student
    $id = R::store($student);

    $successResponse = [
        'success' => true,
        'message' => 'Student added successfully',
        'data' => [
            'id' => $id,
            'nama' => $student->nama,
            'tanggal_lahir' => $student->tanggal_lahir,
            'jenis_kelamin' => $student->jenis_kelamin,
            'alamat' => $student->alamat,
            'nomor_hp' => $student->nomor_hp,
            'email' => $student->email,
            'foto' => $student->foto,
            'created_at' => $student->created_at,
            'updated_at' => $student->updated_at
        ]
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    echo json_encode($successResponse);
} catch (Exception $e) {
    $errorResponse = [
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
}