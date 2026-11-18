<?php
// update-achievement-catatan.php - Update the catatan of an achievement record

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/functions.php'; // Include functions for initDB
require_once __DIR__ . '/helpers.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Initialize database connection
try {
    if (!R::testConnection()) {
        initDB();
    }
} catch (Exception $e) {
    initDB();
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);
$id = $input['id'] ?? '';
$catatan = $input['catatan'] ?? '';
// Authorization check removed per user request

try {
    // Validate required fields
    if (empty($id)) {
        echo json_encode(['success' => false, 'message' => 'ID is required']);
        exit;
    }

    // Find the achievement
    $achievement = R::load('pencapaian', $id);
    if (!$achievement->id) {
        echo json_encode(['success' => false, 'message' => 'Achievement not found']);
        exit;
    }

    // Update the catatan
    $achievement->catatan = $catatan;
    $achievement->updated_at = date('Y-m-d H:i:s');
    R::store($achievement);

    echo json_encode([
        'success' => true,
        'message' => 'Catatan berhasil diperbarui'
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}
