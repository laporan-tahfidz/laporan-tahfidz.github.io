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
$input = json_decode(file_get_contents('php://input'), true);
$token = $input['token'] ?? '';
$id = $input['id'] ?? '';

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

try {
    // Find the existing musyrif
    $musyrif = R::load('musyrif', $id);

    if (!$musyrif->id) {
        http_response_code(404);
        echo json_encode(['success' => false, 'message' => 'Musyrif tidak ditemukan']);
        exit;
    }

    // Delete the musyrif from the database
    R::trash($musyrif);

    echo json_encode([
        'success' => true,
        'message' => 'Musyrif berhasil dihapus'
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat menghapus data']);
}
?>