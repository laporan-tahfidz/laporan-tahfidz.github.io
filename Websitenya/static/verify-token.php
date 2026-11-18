<?php
// verify-token.php - Verify the super admin token

require_once __DIR__ . '/library/rb-sqlite.php';



// Initialize RedBeanPHP with SQLite database
R::setup('sqlite:./everynight-in-my-dream.db');

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
$token = $input['token'] ?? '';

if (!$token) {
    echo json_encode(['valid' => false, 'message' => 'Token diperlukan']);
    exit;
}

// Check if token exists and is valid in the database
$tokenBean = R::findOne('token', ' token_hash = ? ', [hash('sha256', $token)]);

if (!$tokenBean) {
    echo json_encode(['valid' => false, 'message' => 'Token tidak valid']);
    exit;
}

// Check if token has expired (tokens expire after 24 hours)
if ($tokenBean->expires_at < time()) {
    // Remove expired token from database
    R::trash($tokenBean);
    echo json_encode(['valid' => false, 'message' => 'Token telah kadaluarsa']);
    exit;
}

echo json_encode([
    'valid' => true,
    'message' => 'Token valid'
]);