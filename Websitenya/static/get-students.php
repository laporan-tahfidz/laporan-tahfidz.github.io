<?php
// get-students.php - Get all students

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
    
    // Get all students from the database
    $students = R::findAll('santri', 'ORDER BY created_at DESC');
    
    // Convert RedBean objects to arrays
    $studentsArray = [];
    foreach ($students as $student) {
        $studentsArray[] = [
            'id' => $student->id,
            'nama' => $student->nama,
            'tanggal_lahir' => $student->tanggal_lahir,
            'jenis_kelamin' => $student->jenis_kelamin,
            'alamat' => $student->alamat,
            'nomor_hp' => $student->nomor_hp,
            'email' => $student->email,
            'foto' => $student->foto,
            'created_at' => $student->created_at,
            'updated_at' => $student->updated_at
        ];
    }
    
    echo json_encode([
        'success' => true,
        'data' => $studentsArray
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}