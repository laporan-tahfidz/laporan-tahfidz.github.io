<?php
// get-teachers.php - Get all teachers

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/helpers.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    initDB();
    
    // Get all teachers from the database
    $teachers = R::findAll('pengajar', 'ORDER BY created_at DESC');
    
    // Convert RedBean objects to arrays
    $teachersArray = [];
    foreach ($teachers as $teacher) {
        $teachersArray[] = [
            'id' => $teacher->id,
            'nama' => $teacher->nama,
            'tanggal_lahir' => $teacher->tanggal_lahir,
            'jenis_kelamin' => $teacher->jenis_kelamin,
            'alamat' => $teacher->alamat,
            'nomor_hp' => $teacher->nomor_hp,
            'email' => $teacher->email,
            'mata_pelajaran' => $teacher->mata_pelajaran,
            'foto' => $teacher->foto,
            'created_at' => $teacher->created_at,
            'updated_at' => $teacher->updated_at
        ];
    }
    
    echo json_encode([
        'success' => true,
        'data' => $teachersArray
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}