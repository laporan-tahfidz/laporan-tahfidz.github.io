<?php
// get-class-configuration.php - Get class configuration

require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/functions-settings.php';

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

// Verify the token - function will check both request body and Authorization header
if (!verifyToken()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    // Get class configuration from settings
    $kelas1 = getSetting('kelas1_year') ?: '';
    $kelas2 = getSetting('kelas2_year') ?: '';
    $kelas3 = getSetting('kelas3_year') ?: '';

    echo json_encode([
        'success' => true,
        'configuration' => [
            'kelas1' => $kelas1,
            'kelas2' => $kelas2,
            'kelas3' => $kelas3
        ]
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => 'Terjadi kesalahan saat mengambil konfigurasi kelas: ' . $e->getMessage()
    ]);
}
?>