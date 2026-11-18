<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Set CORS headers
setCORSHeaders();

header('Content-Type: application/json');

// Check if request method is GET (for manual trigger)
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

try {
    // Get the selected group ID from the database
    $settings = R::findOne('settings', 'key = ?', ['whatsapp_group_id']);
    
    if (!$settings || empty($settings->value)) {
        http_response_code(400);
        echo json_encode([
            'success' => false, 
            'message' => 'Grup WhatsApp tujuan belum dipilih di halaman /super'
        ]);
        exit;
    }
    
    $groupId = $settings->value;
    
    // Prepare the message
    $message = "Assalamualaikum ustadz-ustadzah, untuk Laporan Sabtu, kita pengisiannya di website tahfidz.mabaiz.com\n\n";
    $message .= "Untuk tutorialnya bisa dicek di https://youtube.com/shorts/O1GmEprXIGU?si=EFbjU2xnFpYPRfWE\n\n";
    $message .= "Terima kasih\n\n";
    $message .= "Jangan lupa juga untuk mengisi di website setelah santri setoran ziyadah, setengah juz, juziyah, syahadah, dan tes satu juz. Tutorialnya ada di https://youtube.com/shorts/Fncf6xdg-1E?si=UfwHet7qfvjUtJ6j";

    // Send the message via Sidobe API
    $curl = curl_init();
    
    curl_setopt_array($curl, [
        CURLOPT_URL => 'https://api.sidobe.com/wa/v1/send-message',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode([
            'group_id' => $groupId,
            'message' => $message
        ]),
        CURLOPT_HTTPHEADER => [
            'X-Secret-Key: DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO',
            'Content-Type: application/json'
        ],
        CURLOPT_SSL_VERIFYPEER => false, // Allow insecure connections for local development
        CURLOPT_TIMEOUT => 30
    ]);

    $response = curl_exec($curl);
    $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    $error = curl_error($curl);
    
    curl_close($curl);

    if ($error) {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'message' => 'Error sending message: ' . $error
        ]);
        exit;
    }

    $responseData = json_decode($response, true);
    
    if ($httpCode !== 200 || !$responseData || !isset($responseData['is_success']) || !$responseData['is_success']) {
        http_response_code($httpCode ?: 500);
        echo json_encode([
            'success' => false,
            'message' => 'Failed to send message via Sidobe API',
            'sidobe_response' => $responseData
        ]);
        exit;
    }

    // Return success response
    echo json_encode([
        'success' => true,
        'message' => 'Pesan Laporan Sabtu berhasil dikirim ke grup WhatsApp',
        'data' => $responseData['data'] ?? null
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false, 
        'message' => 'Terjadi kesalahan saat mengirim pesan: ' . $e->getMessage()
    ]);
}

R::close();
?>