<?php
// send-otp.php - Send OTP to WhatsApp using Sidobe API

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

// Normalize phone number format for consistent database storage
// Remove any leading '+' and normalize to 62... format
$normalizedPhone = ltrim($phone, '+');
if (substr($normalizedPhone, 0, 2) !== '62' && substr($normalizedPhone, 0, 1) === '0') {
    $normalizedPhone = '62' . substr($normalizedPhone, 1);
}
$phone = '+' . $normalizedPhone;

if (!$phone) {
    $errorResponse = ['success' => false, 'message' => 'Nomor WhatsApp diperlukan'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

// Generate a random 6-digit OTP
$otp = sprintf('%06d', rand(0, 999999));

// Store OTP in database
$otpBean = R::dispense('otp');
$otpBean->phone = $phone;
$otpBean->code = $otp;
$otpBean->expires_at = time() + 300; // 5 minutes expiry
$otpBean->created_at = time();
R::store($otpBean);

// Debug: Log the stored phone number
error_log("Stored OTP for phone: " . $phone . ", OTP: " . $otp);

// Send OTP via WhatsApp using Sidobe API
// TODO: Replace with your actual Sidobe API key
$sidobe_api_key = 'DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO'; // Get your API key from Sidobe dashboard

$curl = curl_init();

curl_setopt_array($curl, [
    CURLOPT_URL => 'https://api.sidobe.com/wa/v1/send-message',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode([
        'phone' => $phone,
        'message' => "Kode OTP Anda adalah: {$otp}. Kode ini berlaku selama 5 menit."
    ]),
    CURLOPT_HTTPHEADER => [
        'X-Secret-Key: ' . $sidobe_api_key,
        'Content-Type: application/json'
    ],
    CURLOPT_SSL_VERIFYPEER => false, // Allow non-HTTPS connections
]);

$response = curl_exec($curl);
$http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
curl_close($curl);

$result = json_decode($response, true);

if ($result && isset($result['is_success']) && $result['is_success'] === true) {
    $successResponse = ['success' => true, 'message' => 'OTP berhasil dikirim'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    echo json_encode($successResponse);
} else {
    $errorResponse = ['success' => false, 'message' => 'Gagal mengirim OTP: ' . ($result['message'] ?? 'Unknown error')];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
}