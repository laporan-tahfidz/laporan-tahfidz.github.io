<?php
// save-class-configuration.php - Save class configuration

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
$configuration = $input['configuration'] ?? [];

// Verify the token - function will check both request body and Authorization header
if (!verifyToken()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    // Validate input
    if (!isset($configuration['kelas1']) || !isset($configuration['kelas2']) || !isset($configuration['kelas3'])) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Konfigurasi kelas tidak lengkap']);
        exit;
    }

    // Save class configuration to settings
    $kelas1 = $configuration['kelas1'];
    $kelas2 = $configuration['kelas2'];
    $kelas3 = $configuration['kelas3'];

    // Save to database
    setSetting('kelas1_year', $kelas1);
    setSetting('kelas2_year', $kelas2);
    setSetting('kelas3_year', $kelas3);

    echo json_encode([
        'success' => true,
        'message' => 'Konfigurasi kelas berhasil disimpan'
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => 'Terjadi kesalahan saat menyimpan konfigurasi kelas: ' . $e->getMessage()
    ]);
}
?>