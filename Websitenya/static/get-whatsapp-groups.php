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

// For security, you might want to verify a token here
// $token = $input['token'] ?? '';
// if (!verifyToken($token)) {
//     http_response_code(401);
//     echo json_encode(['success' => false, 'message' => 'Unauthorized']);
//     exit;
// }

try {
    // Call the Sidobe API to get WhatsApp groups
    $curl = curl_init();
    
    curl_setopt_array($curl, [
        CURLOPT_URL => 'https://api.sidobe.com/wa/v1/whatsapp-groups',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_ENCODING => '',
        CURLOPT_MAXREDIRS => 10,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => 'GET',
        CURLOPT_HTTPHEADER => [
            'X-Secret-Key: DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO', // Sidobe secret key
            'Content-Type: application/json'
        ],
        CURLOPT_SSL_VERIFYPEER => false, // Disable SSL certificate verification
        CURLOPT_SSL_VERIFYHOST => false, // Disable SSL host verification
    ]);

    $response = curl_exec($curl);
    $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    $err = curl_error($curl);
    
    curl_close($curl);

    if ($err) {
        throw new Exception("cURL Error #: " . $err);
    }

    if ($httpCode !== 200) {
        throw new Exception("HTTP Error: " . $httpCode . " - Response: " . $response);
    }

    $responseData = json_decode($response, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("JSON Decode Error: " . json_last_error_msg());
    }

    if (isset($responseData['is_success']) && $responseData['is_success'] === true) {
        echo json_encode([
            'success' => true,
            'data' => $responseData['data'] ?? []
        ]);
    } else {
        // If the API response doesn't have the expected format, return the raw data
        // or handle the error appropriately
        echo json_encode([
            'success' => false,
            'message' => 'Failed to fetch groups from Sidobe API',
            'raw_response' => $responseData
        ]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => 'Terjadi kesalahan saat mengambil data grup: ' . $e->getMessage()
    ]);
}
?>