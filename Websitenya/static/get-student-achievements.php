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
$token = $input['token'] ?? '';
$studentId = $input['studentId'] ?? '';

// Verify the token if provided
if ($token && !verifyToken($token)) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

if (empty($studentId)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Student ID is required']);
    exit;
}

try {
    // Convert studentId to integer to ensure proper comparison
    $intStudentId = intval($studentId);

    // Get all achievements for the student ordered by creation date (most recent first)
    // First, try to find by santri_id (which is the id in the santri table)
    $achievements = R::getAll("
        SELECT
            id,
            type,
            juz,
            halaman,
            posisi,
            syahadah,
            kesalahan,
            catatan,
            created_at
        FROM pencapaian
        WHERE santri_id = ?
        ORDER BY created_at DESC
    ", [$intStudentId]);

    // If no achievements found by santri_id, try to find by nik
    if (empty($achievements)) {
        // First get the student id from the santri table using the nik
        $studentRecord = R::getRow("SELECT id FROM santri WHERE nik = ?", [$studentId]);
        if ($studentRecord) {
            $realStudentId = $studentRecord['id'];
            $achievements = R::getAll("
                SELECT
                    id,
                    type,
                    juz,
                    halaman,
                    posisi,
                    syahadah,
                    kesalahan,
                    catatan,
                    created_at
                FROM pencapaian
                WHERE santri_id = ?
                ORDER BY created_at DESC
            ", [$realStudentId]);
        }
    }

    echo json_encode([
        'success' => true,
        'achievements' => $achievements
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data pencapaian: ' . $e->getMessage()]);
}
?>