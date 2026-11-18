<?php
// get-attendances.php - Get all attendance records

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
    
    // Get all attendance records from the database
    $attendances = R::findAll('kehadiran', 'ORDER BY date DESC');
    
    // Convert RedBean objects to arrays
    $attendancesArray = [];
    foreach ($attendances as $attendance) {
        $attendancesArray[] = [
            'id' => $attendance->id,
            'student_id' => $attendance->student_id,
            'date' => $attendance->date,
            'status' => $attendance->status,
            'notes' => $attendance->notes,
            'created_at' => $attendance->created_at,
            'updated_at' => $attendance->updated_at
        ];
    }
    
    echo json_encode([
        'success' => true,
        'data' => $attendancesArray
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}