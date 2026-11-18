<?php
// delete-achievement.php - Delete an individual achievement record

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/functions.php'; // Include functions for initDB
require_once __DIR__ . '/helpers.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Initialize database connection if not already connected
try {
    if (!R::testConnection()) {
        initDB();
    }
} catch (Exception $e) {
    // If testConnection throws an exception, the database hasn't been set up yet
    initDB();
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);
$id = $input['id'] ?? '';

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    // Add some debugging info to help troubleshoot
    $tokenFromBody = $input['token'] ?? null;
    $authHeader = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
    $method = $_SERVER['REQUEST_METHOD'] ?? 'UNKNOWN';

    error_log("Unauthorized access attempt to delete-achievement.php.");
    error_log("Request method: " . $method);
    error_log("Token from request body: " . ($tokenFromBody ? 'present' : 'missing'));
    error_log("Authorization header: " . ($authHeader ? 'present' : 'missing'));
    if ($authHeader) {
        error_log("Authorization header value: " . $authHeader);
        // Check if it contains 'Bearer' prefix
        if (strpos($authHeader, 'Bearer') === 0) {
            error_log("Authorization header has correct Bearer format");
        } else {
            error_log("Authorization header does not have correct Bearer format");
        }
    }
    // Log all headers for debugging
    foreach (getallheaders() as $key => $value) {
        error_log("Header: $key = $value");
    }

    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    // Validate required fields
    if (empty($id)) {
        echo json_encode(['success' => false, 'message' => 'ID is required']);
        exit;
    }

    // Find the achievement
    $achievement = R::load('pencapaian', $id);
    if (!$achievement->id) {
        echo json_encode(['success' => false, 'message' => 'Achievement not found']);
        exit;
    }

    // Delete the achievement
    R::trash($achievement);

    echo json_encode([
        'success' => true,
        'message' => 'Achievement deleted successfully'
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}