<?php
// get-lessons.php - Get all lessons

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/helpers.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    initDB();
    
    // Get all lessons from the database
    $lessons = R::findAll('materi', 'ORDER BY created_at DESC');
    
    // Convert RedBean objects to arrays
    $lessonsArray = [];
    foreach ($lessons as $lesson) {
        $lessonsArray[] = [
            'id' => $lesson->id,
            'judul' => $lesson->judul,
            'deskripsi' => $lesson->deskripsi,
            'tingkat_kelas' => $lesson->tingkat_kelas,
            'durasi' => $lesson->durasi,
            'created_at' => $lesson->created_at,
            'updated_at' => $lesson->updated_at
        ];
    }
    
    echo json_encode([
        'success' => true,
        'data' => $lessonsArray
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}