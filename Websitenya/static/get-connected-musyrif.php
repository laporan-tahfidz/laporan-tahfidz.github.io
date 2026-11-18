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

// Validate required fields
$nik = $input['nik'] ?? '';

if (empty($nik)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'NIK is required']);
    exit;
}

try {
    // Find the connection between musyrif and student using NIK
    $connection = R::findOne('musyrfst', 'santri_nik = ?', [$nik]);

    if (!$connection) {
        // No musyrif connected to this student
        echo json_encode([
            'success' => true,
            'musyrif' => null,
            'message' => 'No connected musyrif found for this student'
        ]);
        exit;
    }

    // Get the musyrif details
    $musyrif = R::load('musyrif', $connection->musyrif_id);

    if (!$musyrif) {
        // Musyrif not found in the database
        echo json_encode([
            'success' => true,
            'musyrif' => null,
            'message' => 'Connected musyrif not found in database'
        ]);
        exit;
    }

    // Return the musyrif details
    echo json_encode([
        'success' => true,
        'musyrif' => [
            'id' => $musyrif->id,
            'nama_lengkap' => $musyrif->nama,
            'nip' => $musyrif->nip ?? '',
            'no_hp' => $musyrif->no_hp ?? ''
        ]
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data musyrif']);
}
?>