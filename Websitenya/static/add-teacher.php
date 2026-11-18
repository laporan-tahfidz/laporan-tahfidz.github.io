<?php
// add-teacher.php - Add a new teacher

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
    $nama = $_POST['nama'] ?? '';
    $tanggal_lahir = $_POST['tanggal_lahir'] ?? '';
    $jenis_kelamin = $_POST['jenis_kelamin'] ?? 'laki-laki';
    $alamat = $_POST['alamat'] ?? '';
    $nomor_hp = $_POST['nomor_hp'] ?? '';
    $email = $_POST['email'] ?? '';
    $mata_pelajaran = $_POST['mata_pelajaran'] ?? '';
    
    // Validate required fields
    if (empty($nama)) {
        echo json_encode(['success' => false, 'message' => 'Nama is required']);
        exit;
    }
    
    // Handle file upload if present
    $foto = null;
    if (isset($_FILES['foto']) && $_FILES['foto']['error'] === UPLOAD_ERR_OK) {
        $foto = handleFileUpload($_FILES['foto']);
    }
    
    // Create new teacher bean
    $teacher = R::dispense('pengajar');
    $teacher->nama = $nama;
    $teacher->tanggal_lahir = $tanggal_lahir;
    $teacher->jenis_kelamin = $jenis_kelamin;
    $teacher->alamat = $alamat;
    $teacher->nomor_hp = $nomor_hp;
    $teacher->email = $email;
    $teacher->mata_pelajaran = $mata_pelajaran;
    $teacher->foto = $foto;
    $teacher->created_at = date('Y-m-d H:i:s');
    $teacher->updated_at = date('Y-m-d H:i:s');
    
    // Store the teacher
    $id = R::store($teacher);
    
    echo json_encode([
        'success' => true,
        'message' => 'Teacher added successfully',
        'data' => [
            'id' => $id,
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