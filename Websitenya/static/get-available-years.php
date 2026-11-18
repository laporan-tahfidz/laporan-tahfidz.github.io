<?php
// get-available-years.php - Get available years from students

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

// Verify the token - function will check both request body and Authorization header
if (!verifyToken()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    // Get distinct years from students
    $years = R::getCol("SELECT DISTINCT tahun_masuk FROM santri ORDER BY tahun_masuk DESC");

    echo json_encode([
        'success' => true,
        'years' => $years
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => 'Terjadi kesalahan saat mengambil tahun tersedia: ' . $e->getMessage()
    ]);
}
?>