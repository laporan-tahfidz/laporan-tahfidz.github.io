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

// Validate phone number
if (empty($phone)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Phone number is required']);
    exit;
}

// Only allow specific admin phone numbers
$allowedPhones = ['+6281545143654']; // Add other allowed numbers as needed
if (!in_array($phone, $allowedPhones)) {
    http_response_code(403);
    echo json_encode(['success' => false, 'message' => 'Phone number not authorized']);
    exit;
}

try {
    // Generate a 6-digit OTP code
    $otpCode = sprintf('%06d', rand(0, 999999));
    
    // Store the OTP in the database with expiration time (5 minutes)
    $otpEntry = R::dispense('adminotps');
    $otpEntry->phone = $phone;
    $otpEntry->code = $otpCode;
    $otpEntry->expires_at = date('Y-m-d H:i:s', strtotime('+5 minutes')); // Expires in 5 minutes
    $otpEntry->created_at = R::isoDateTime();

    R::store($otpEntry);
    
    // Send the OTP via WhatsApp using Sidobe API
    $sidobe_api_key = 'DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO';

    $curl = curl_init();

    curl_setopt_array($curl, [
        CURLOPT_URL => 'https://api.sidobe.com/wa/v1/send-message',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode([
            'phone' => $phone,
            'message' => "Kode OTP Anda untuk autentikasi admin sistem tahfidz adalah: {$otpCode}. Kode ini berlaku selama 5 menit."
        ]),
        CURLOPT_HTTPHEADER => [
            'X-Secret-Key: ' . $sidobe_api_key,
            'Content-Type: application/json'
        ],
        CURLOPT_SSL_VERIFYPEER => false, // Allow non-HTTPS connections
    ]);

    $response = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    $error = curl_error($curl);
    $errno = curl_errno($curl);
    curl_close($curl);

    // Log the error for debugging purposes
    error_log("WhatsApp API Error - errno: $errno, error: $error, httpCode: $http_code");

    $responseData = json_decode($response, true);

    if ($responseData && isset($responseData['is_success']) && $responseData['is_success'] === true) {
        echo json_encode([
            'success' => true,
            'message' => 'OTP sent successfully'
        ]);
    } else {
        $errorMessage = $responseData['message'] ?? 'Unknown error';
        if ($error) {
            $errorMessage .= ' (cURL error: ' . $error . ')';
        }

        // Even if WhatsApp sending fails, we still consider the OTP generated
        // as it might be retrieved through other means
        echo json_encode([
            'success' => true,
            'message' => 'OTP generated but failed to send via WhatsApp: ' . $errorMessage
        ]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Server error: ' . $e->getMessage()]);
}
?>