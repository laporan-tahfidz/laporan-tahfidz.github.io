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
    echo json_encode(['valid' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get the posted data
$input = json_decode(file_get_contents('php://input'), true);
$token = $input['token'] ?? '';

// Check if token exists in the database
if (empty($token)) {
    echo json_encode(['valid' => false, 'message' => 'Token is required']);
    exit;
}

try {
    // Use the existing verifyToken function which follows the same pattern
    // as the super admin token verification
    $isValid = verifyToken($token);

    if ($isValid) {
        echo json_encode(['valid' => true]);
    } else {
        echo json_encode(['valid' => false, 'message' => 'Invalid or expired token']);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['valid' => false, 'message' => 'Server error']);
}
?>