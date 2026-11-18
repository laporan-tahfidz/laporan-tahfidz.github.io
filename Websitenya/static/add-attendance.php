<?php
// add-attendance.php - Add a new attendance record

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/helpers-idempotency.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Get the idempotency key from header or JSON input
$idempotencyKey = getIdempotencyKey();

// Check if this request has already been processed
if ($idempotencyKey) {
    $storedResponse = checkIdempotency($idempotencyKey, 'POST');
    if ($storedResponse) {
        // Return the stored response to prevent duplicate processing
        echo json_encode($storedResponse);
        exit;
    }
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    $errorResponse = ['success' => false, 'message' => 'Unauthorized'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

try {
    initDB();

    // Get form data
    $student_id = $input['student_id'] ?? '';
    $date = $input['date'] ?? date('Y-m-d');
    $status = $input['status'] ?? 'hadir';
    $notes = $input['notes'] ?? '';

    // Validate required fields
    if (empty($student_id) || empty($date)) {
        $errorResponse = ['success' => false, 'message' => 'Student ID and Date are required'];

        // Store the response for idempotency if key was provided
        if ($idempotencyKey) {
            storeIdempotency($idempotencyKey, $errorResponse, 'POST');
        }

        echo json_encode($errorResponse);
        exit;
    }

    // Create new attendance bean
    $attendance = R::dispense('kehadiran');
    $attendance->student_id = $student_id;
    $attendance->date = $date;
    $attendance->status = $status;
    $attendance->notes = $notes;
    $attendance->created_at = date('Y-m-d H:i:s');
    $attendance->updated_at = date('Y-m-d H:i:s');

    // Store the attendance
    $id = R::store($attendance);

    $successResponse = [
        'success' => true,
        'message' => 'Attendance added successfully',
        'data' => [
            'id' => $id,
            'student_id' => $attendance->student_id,
            'date' => $attendance->date,
            'status' => $attendance->status,
            'notes' => $attendance->notes,
            'created_at' => $attendance->created_at,
            'updated_at' => $attendance->updated_at
        ]
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    echo json_encode($successResponse);
} catch (Exception $e) {
    $errorResponse = [
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
}