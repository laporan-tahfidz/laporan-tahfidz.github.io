<?php
// delete-student.php - Delete a student

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
$id = $input['id'] ?? '';

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    initDB();
    
    // Validate required fields
    if (empty($id)) {
        echo json_encode(['success' => false, 'message' => 'ID is required']);
        exit;
    }
    
    // Find the student
    $student = R::load('santri', $id);
    if (!$student->id) {
        echo json_encode(['success' => false, 'message' => 'Student not found']);
        exit;
    }
    
    // Delete the student's photo if exists
    if ($student->foto) {
        $photoPath = __DIR__ . '/images/' . $student->foto;
        if (file_exists($photoPath)) {
            unlink($photoPath);
        }
    }
    
    // Delete the student
    R::trash($student);
    
    echo json_encode([
        'success' => true,
        'message' => 'Student deleted successfully'
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}