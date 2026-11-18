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
$nik = $input['nik'] ?? '';
$type = $input['type'] ?? '';

// Validate NIK
if (empty($nik)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'NIK harus diisi']);
    exit;
}

try {
    // Find the last achievement for the student
    $whereClause = 'nik = ?';
    $params = [$nik];

    if ($type === 'setoran') {
        $whereClause .= ' AND type IS NOT NULL'; // For setoran achievements (pencapaian records)
    }

    $lastAchievement = R::findOne('pencapaian', $whereClause . ' ORDER BY created_at DESC', $params);

    if ($lastAchievement) {
        // Return the last achievement data
        echo json_encode([
            'success' => true,
            'achievement' => [
                'id' => $lastAchievement->id,
                'type' => $lastAchievement->type,
                'juz' => $lastAchievement->juz,
                'halaman' => $lastAchievement->halaman ?? null,
                'posisi' => $lastAchievement->posisi ?? null,
                'syahadah' => $lastAchievement->syahadah ?? null,
                'kesalahan' => $lastAchievement->kesalahan,
                'catatan' => $lastAchievement->catatan ?? null,
                'santri_id' => $lastAchievement->santri_id,
                'nik' => $lastAchievement->nik,
                'created_at' => $lastAchievement->created_at,
                'updated_at' => $lastAchievement->updated_at
            ]
        ]);
    } else {
        // No achievement found for this student
        echo json_encode([
            'success' => true,
            'achievement' => null
        ]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data pencapaian']);
}
?>