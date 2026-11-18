<?php
// update-teacher.php - Update an existing teacher

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
    $mata_pelajaran = $_POST['mata_pelajaran'] ?? '';
    
    // Validate required fields
    if (empty($id) || empty($nama)) {
        echo json_encode(['success' => false, 'message' => 'ID and Nama are required']);
        exit;
    }
    
    // Find the existing teacher
    $teacher = R::load('pengajar', $id);
    if (!$teacher->id) {
        echo json_encode(['success' => false, 'message' => 'Teacher not found']);
        exit;
    }
    
    // Handle file upload if present
    if (isset($_FILES['foto']) && $_FILES['foto']['error'] === UPLOAD_ERR_OK) {
        // Delete old photo if exists
        if ($teacher->foto) {
            $oldPhotoPath = __DIR__ . '/images/' . $teacher->foto;
            if (file_exists($oldPhotoPath)) {
                unlink($oldPhotoPath);
            }
        }
        
        // Upload new photo
        $foto = handleFileUpload($_FILES['foto']);
        if ($foto) {
            $teacher->foto = $foto;
        }
    }
    
    // Update teacher properties
    $teacher->nama = $nama;
    $teacher->tanggal_lahir = $tanggal_lahir;
    $teacher->jenis_kelamin = $jenis_kelamin;
    $teacher->alamat = $alamat;
    $teacher->nomor_hp = $nomor_hp;
    $teacher->email = $email;
    $teacher->mata_pelajaran = $mata_pelajaran;
    $teacher->updated_at = date('Y-m-d H:i:s');
    
    // Store the updated teacher
    R::store($teacher);
    
    echo json_encode([
        'success' => true,
        'message' => 'Teacher updated successfully',
        'data' => [
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
        ]
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}