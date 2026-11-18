<?php
// auto-configure-classes.php - Auto configure classes based on logic

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
    // Get the most recent 3 years from students
    $recentYears = R::getCol("SELECT DISTINCT tahun_masuk FROM santri ORDER BY tahun_masuk DESC LIMIT 3");

    if (count($recentYears) < 1) {
        http_response_code(400);
        echo json_encode(['success' => false, 'message' => 'Tidak ditemukan data tahun masuk santri']);
        exit;
    }

    // Assign the most recent year to kelas 1, next to kelas 2, and so on
    $kelas1 = $recentYears[0] ?? '';
    $kelas2 = isset($recentYears[1]) ? $recentYears[1] : '';
    $kelas3 = isset($recentYears[2]) ? $recentYears[2] : '';

    // Save to database
    setSetting('kelas1_year', $kelas1);
    setSetting('kelas2_year', $kelas2);
    setSetting('kelas3_year', $kelas3);

    echo json_encode([
        'success' => true,
        'message' => 'Kelas berhasil dikonfigurasi otomatis',
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
        'message' => 'Terjadi kesalahan saat mengkonfigurasi kelas otomatis: ' . $e->getMessage()
    ]);
}
?>