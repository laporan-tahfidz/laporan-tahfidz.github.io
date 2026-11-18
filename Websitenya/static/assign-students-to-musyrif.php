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
$musyrif_id = $input['musyrif_id'] ?? '';
$student_niks = $input['student_niks'] ?? [];

// Verify the token if provided
if ($token && !verifyToken($token)) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

// Validate inputs
if (empty($musyrif_id)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'ID musyrif harus diisi']);
    exit;
}

if (!is_array($student_niks)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Daftar NIK santri harus berupa array']);
    exit;
}

// Limit to 9 students per musyrif
if (count($student_niks) > 9) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Maksimal 9 santri per musyrif']);
    exit;
}

try {
    // First, remove all existing assignments for this musyrif
    $existingAssignments = R::find('musyrfst', 'musyrif_id = ?', [$musyrif_id]);
    foreach ($existingAssignments as $assignment) {
        R::trash($assignment);
    }

    // Then add the new assignments based on the array
    foreach ($student_niks as $nik) {
        // Verify that the student exists
        $student = R::findOne('santri', 'nik = ?', [$nik]);
        if ($student) {
            // Create a new musyrif student assignment
            $assignment = R::dispense('musyrfst');
            $assignment->musyrif_id = $musyrif_id;
            $assignment->santri_nik = $nik;
            $assignment->created_at = R::isoDateTime();
            $assignment->updated_at = R::isoDateTime();

            R::store($assignment);
        }
    }

    echo json_encode([
        'success' => true,
        'message' => 'Anggota musyrif berhasil diperbarui'
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat menyimpan data anggota musyrif']);
}
?>