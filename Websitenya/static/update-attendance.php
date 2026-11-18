<?php
// update-attendance.php - Update an existing attendance record

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
    $student_id = $input['student_id'] ?? '';
    $date = $input['date'] ?? '';
    $status = $input['status'] ?? '';
    $notes = $input['notes'] ?? '';
    
    // Validate required fields
    if (empty($id)) {
        echo json_encode(['success' => false, 'message' => 'ID is required']);
        exit;
    }
    
    // Find the existing attendance
    $attendance = R::load('kehadiran', $id);
    if (!$attendance->id) {
        echo json_encode(['success' => false, 'message' => 'Attendance not found']);
        exit;
    }
    
    // Update attendance properties
    if (!empty($student_id)) $attendance->student_id = $student_id;
    if (!empty($date)) $attendance->date = $date;
    if (!empty($status)) $attendance->status = $status;
    if (!empty($notes)) $attendance->notes = $notes;
    $attendance->updated_at = date('Y-m-d H:i:s');
    
    // Store the updated attendance
    R::store($attendance);
    
    echo json_encode([
        'success' => true,
        'message' => 'Attendance updated successfully',
        'data' => [
            'id' => $attendance->id,
            'student_id' => $attendance->student_id,
            'date' => $attendance->date,
            'status' => $attendance->status,
            'notes' => $attendance->notes,
            'created_at' => $attendance->created_at,
            'updated_at' => $attendance->updated_at
        ]
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}