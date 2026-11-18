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
$musyrif_id = $input['musyrif_id'] ?? '';

// Verify the token if provided
if ($token && !verifyToken($token)) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

// Validate musyrif_id
if (empty($musyrif_id)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'ID musyrif harus diisi']);
    exit;
}

try {
    // Get students assigned to the specific musyrif
    $assignedStudents = R::getAll("
        SELECT ms.id as assignment_id, s.nama_sesuai_kk as nama, s.nik as nik
        FROM musyrfst ms
        JOIN santri s ON ms.santri_nik = s.nik
        WHERE ms.musyrif_id = ?
        ORDER BY s.nama_sesuai_kk ASC
    ", [$musyrif_id]);

    echo json_encode([
        'success' => true,
        'data' => $assignedStudents
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data santri musyrif']);
}
?>