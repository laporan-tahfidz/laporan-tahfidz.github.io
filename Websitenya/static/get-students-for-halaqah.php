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
    // Calculate the last 3 years
    $currentYear = date('Y');
    $year3Ago = $currentYear - 3;
    
    // Get students from the last 3 years
    // Using NIK as the identifier instead of ID
    $students = R::getAll("
        SELECT s.id, s.nama_sesuai_kk as nama, s.nik, s.tahun_masuk
        FROM santri s
        WHERE s.tahun_masuk >= ?
        ORDER BY s.nama_sesuai_kk ASC
    ", [$year3Ago]);

    echo json_encode([
        'success' => true,
        'data' => $students
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data santri']);
}
?>