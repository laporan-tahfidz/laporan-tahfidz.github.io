<?php
// verify-otp.php - Verify OTP and generate token

require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/helpers-idempotency.php';

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
$phone = $input['phone'] ?? '';
$otp = $input['otp'] ?? '';

// Normalize phone number format for consistent database lookup
// Remove any leading '+' and normalize to 62... format
$normalizedPhone = ltrim($phone, '+');
if (substr($normalizedPhone, 0, 2) !== '62' && substr($normalizedPhone, 0, 1) === '0') {
    $normalizedPhone = '62' . substr($normalizedPhone, 1);
}
$phone = '+' . $normalizedPhone;

if (!$phone || !$otp) {
    $errorResponse = ['success' => false, 'message' => 'Nomor WhatsApp dan OTP diperlukan'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

// Debug: Log the phone number being checked
error_log("Verifying OTP for phone: " . $phone);

// Check if OTP exists and is valid in the database
$otpBeans = R::find('otp', ' phone = ? ', [$phone]);

if (empty($otpBeans)) {
    $errorResponse = ['success' => false, 'message' => 'OTP tidak ditemukan atau telah kadaluarsa'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

// Get the most recent OTP for this phone number
$otpBean = null;
foreach ($otpBeans as $bean) {
    if ($otpBean === null || $bean->created_at > $otpBean->created_at) {
        $otpBean = $bean;
    }
}

if (!$otpBean) {
    $errorResponse = ['success' => false, 'message' => 'OTP tidak ditemukan atau telah kadaluarsa'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

// Check if OTP has expired
if ($otpBean->expires_at < time()) {
    // Remove expired OTP from database
    R::trash($otpBean);
    $errorResponse = ['success' => false, 'message' => 'OTP telah kadaluarsa'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

// Check if OTP code matches
if ($otpBean->code !== $otp) {
    $errorResponse = ['success' => false, 'message' => 'OTP tidak valid'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

// OTP is valid, generate a token
$token = bin2hex(random_bytes(32)); // Generate a secure token

// Store the token in database with expiration (24 hours)
$tokenBean = R::dispense('token');
$tokenBean->token_hash = hash('sha256', $token); // Store hashed token for security
$tokenBean->phone = $phone;
$tokenBean->created_at = time();
$tokenBean->expires_at = time() + (24 * 60 * 60); // Token expires in 24 hours
R::store($tokenBean);

// Clean up the used OTP from database
R::trash($otpBean);

$successResponse = [
    'success' => true,
    'message' => 'OTP valid',
    'token' => $token
];

// Store the response for idempotency if key was provided
if ($idempotencyKey) {
    storeIdempotency($idempotencyKey, $successResponse, 'POST');
}

echo json_encode($successResponse);