<?php
// update-student.php - Update an existing student

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

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    initDB();
    
    // Get form data
    $id = $_POST['id'] ?? '';
    $nama = $_POST['nama'] ?? '';
    $tanggal_lahir = $_POST['tanggal_lahir'] ?? '';
    $jenis_kelamin = $_POST['jenis_kelamin'] ?? 'laki-laki';
    $alamat = $_POST['alamat'] ?? '';
    $nomor_hp = $_POST['nomor_hp'] ?? '';
    $email = $_POST['email'] ?? '';
    
    // Validate required fields
    if (empty($id) || empty($nama)) {
        echo json_encode(['success' => false, 'message' => 'ID and Nama are required']);
        exit;
    }
    
    // Find the existing student
    $student = R::load('santri', $id);
    if (!$student->id) {
        echo json_encode(['success' => false, 'message' => 'Student not found']);
        exit;
    }
    
    // Handle file upload if present
    if (isset($_FILES['foto']) && $_FILES['foto']['error'] === UPLOAD_ERR_OK) {
        // Delete old photo if exists
        if ($student->foto) {
            $oldPhotoPath = __DIR__ . '/images/' . $student->foto;
            if (file_exists($oldPhotoPath)) {
                unlink($oldPhotoPath);
            }
        }
        
        // Upload new photo
        $foto = handleFileUpload($_FILES['foto']);
        if ($foto) {
            $student->foto = $foto;
        }
    }
    
    // Update student properties
    $student->nama = $nama;
    $student->tanggal_lahir = $tanggal_lahir;
    $student->jenis_kelamin = $jenis_kelamin;
    $student->alamat = $alamat;
    $student->nomor_hp = $nomor_hp;
    $student->email = $email;
    $student->updated_at = date('Y-m-d H:i:s');
    
    // Store the updated student
    R::store($student);
    
    echo json_encode([
        'success' => true,
        'message' => 'Student updated successfully',
        'data' => [
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
        ]
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}