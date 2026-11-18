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
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get the posted data
$input = json_decode(file_get_contents('php://input'), true);
$phone = $input['phone'] ?? '';
$code = $input['code'] ?? '';

// Validate inputs
if (empty($phone) || empty($code)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Phone number and code are required']);
    exit;
}

try {
    // Find the OTP entry in the database
    $otpEntry = R::findOne('adminotps', 'phone = ? AND code = ?', [$phone, $code]);
    
    if (!$otpEntry) {
        echo json_encode(['success' => false, 'message' => 'Invalid OTP code']);
        exit;
    }
    
    // Check if OTP has expired
    $expiresAt = new DateTime($otpEntry->expires_at);
    $now = new DateTime();
    
    if ($now > $expiresAt) {
        // OTP has expired, remove it from the database
        R::trash($otpEntry);
        echo json_encode(['success' => false, 'message' => 'OTP has expired']);
        exit;
    }
    
    // OTP is valid, generate a new admin token
    $token = bin2hex(random_bytes(32)); // 64 character hex string

    // Store the token in the token table (using the same structure as the existing system)
    $tokenBean = R::dispense('token');
    $tokenBean->token_hash = hash('sha256', $token); // Hash the token for security
    $tokenBean->expires_at = time() + (24 * 60 * 60); // Token expires in 24 hours
    $tokenBean->created_at = R::isoDateTime();

    R::store($tokenBean);

    // Remove the used OTP from the database
    R::trash($otpEntry);

    echo json_encode([
        'success' => true,
        'message' => 'OTP verified successfully',
        'token' => $token
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Server error: ' . $e->getMessage()]);
}
?>