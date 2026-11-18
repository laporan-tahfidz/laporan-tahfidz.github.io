<?php
// get-class-distribution.php - Get class distribution data

require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/functions-settings.php';
require_once __DIR__ . '/helpers.php';

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
    // Get all students
    $students = R::findAll('santri');

    // Count students by class
    $distribution = [
        'Kelas 1' => 0,
        'Kelas 2' => 0,
        'Kelas 3' => 0,
        'Lainnya' => 0
    ];

    foreach ($students as $student) {
        $classLevel = determineClassLevel($student->tahun_masuk);
        
        if (isset($distribution[$classLevel])) {
            $distribution[$classLevel]++;
        } else {
            $distribution['Lainnya']++;
        }
    }

    echo json_encode([
        'success' => true,
        'distribution' => $distribution
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => 'Terjadi kesalahan saat mengambil distribusi kelas: ' . $e->getMessage()
    ]);
}
?>