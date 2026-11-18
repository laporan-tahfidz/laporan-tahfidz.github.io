<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';

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

// Get the posted data
$data = $_POST;
$token = $data['token'] ?? '';
$id = $data['id'] ?? '';

// Verify the token if provided
if ($token && !verifyToken($token)) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

// Validate ID
if (empty($id)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'ID musyrif harus diisi']);
    exit;
}

// Get the form data
$nama = trim($data['nama'] ?? '');

// Validate required fields
if (empty($nama)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Nama musyrif harus diisi']);
    exit;
}

try {
    // Find the existing musyrif
    $musyrif = R::load('musyrif', $id);
    
    if (!$musyrif->id) {
        http_response_code(404);
        echo json_encode(['success' => false, 'message' => 'Musyrif tidak ditemukan']);
        exit;
    }

    // Check if another musyrif with the same name already exists (excluding current record)
    $existingMusyrif = R::findOne('musyrif', 'nama = ? AND id != ?', [$nama, $id]);
    
    if ($existingMusyrif) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Nama musyrif sudah terdaftar oleh musyrif lain']);
        exit;
    }

    // Update the musyrif
    $musyrif->nama = $nama;
    $musyrif->updated_at = R::isoDateTime();

    // Store the updated musyrif in the database
    R::store($musyrif);

    echo json_encode([
        'success' => true,
        'message' => 'Data musyrif berhasil diperbarui',
        'data' => [
            'id' => $musyrif->id,
            'nama' => $musyrif->nama,
            'created_at' => $musyrif->created_at,
            'updated_at' => $musyrif->updated_at
        ]
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat memperbarui data']);
}
?>