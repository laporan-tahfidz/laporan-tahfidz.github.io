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

// Verify the token if provided
if ($token && !verifyToken($token)) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    // Get all musyrif with their assigned students count
    $musyrifs = R::getAll("
        SELECT m.id, m.nama,
               COUNT(ms.santri_nik) as assigned_students_count
        FROM musyrif m
        LEFT JOIN musyrfst ms ON m.id = ms.musyrif_id
        GROUP BY m.id, m.nama
        ORDER BY m.nama ASC
    ");

    echo json_encode([
        'success' => true,
        'data' => $musyrifs
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data musyrif']);
}
?>