<?php
// update-lesson.php - Update an existing lesson

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
    
    // Get form data
    $id = $input['id'] ?? '';
    $judul = $input['judul'] ?? '';
    $deskripsi = $input['deskripsi'] ?? '';
    $tingkat_kelas = $input['tingkat_kelas'] ?? '';
    $durasi = $input['durasi'] ?? '';
    
    // Validate required fields
    if (empty($id) || empty($judul)) {
        echo json_encode(['success' => false, 'message' => 'ID and Judul are required']);
        exit;
    }
    
    // Find the existing lesson
    $lesson = R::load('materi', $id);
    if (!$lesson->id) {
        echo json_encode(['success' => false, 'message' => 'Lesson not found']);
        exit;
    }
    
    // Update lesson properties
    $lesson->judul = $judul;
    $lesson->deskripsi = $deskripsi;
    $lesson->tingkat_kelas = $tingkat_kelas;
    $lesson->durasi = $durasi;
    $lesson->updated_at = date('Y-m-d H:i:s');
    
    // Store the updated lesson
    R::store($lesson);
    
    echo json_encode([
        'success' => true,
        'message' => 'Lesson updated successfully',
        'data' => [
            'id' => $lesson->id,
            'judul' => $lesson->judul,
            'deskripsi' => $lesson->deskripsi,
            'tingkat_kelas' => $lesson->tingkat_kelas,
            'durasi' => $lesson->durasi,
            'created_at' => $lesson->created_at,
            'updated_at' => $lesson->updated_at
        ]
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}