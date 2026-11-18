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

// Validate NIK
if (empty($nik)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'NIK harus diisi']);
    exit;
}

// Validate NIK format (16 digits)
if (!preg_match('/^\d{16}$/', $nik)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Format NIK tidak valid']);
    exit;
}

try {
    // Find student by NIK
    $student = R::findOne('santri', 'nik = ?', [$nik]);

    if ($student) {
        // Return student data
        echo json_encode([
            'success' => true,
            'student' => [
                'id' => $student->id,
                'external_id' => $student->external_id ?? '',
                'tahun_masuk' => $student->tahun_masuk ?? '',
                'nama_sesuai_kk' => $student->nama_sesuai_kk ?? '',
                'status' => $student->status ?? '',
                'nama_panggilan' => $student->nama_panggilan ?? '',
                'no_kk' => $student->no_kk ?? '',
                'nik' => $student->nik ?? '',
                'nis' => $student->nis ?? '',
                'nisn' => $student->nisn ?? '',
                'asal_sekolah' => $student->asal_sekolah ?? '',
                'alamat_sekolah' => $student->alamat_sekolah ?? '',
                'tempat_lahir' => $student->tempat_lahir ?? '',
                'tanggal_lahir' => $student->tanggal_lahir ?? '',
                'jenis_kelamin' => $student->jenis_kelamin ?? '',
                'anak_ke' => $student->anak_ke ?? '',
                'jumlah_saudara' => $student->jumlah_saudara ?? '',
                'status_anak' => $student->status_anak ?? '',
                'tinggi_badan' => $student->tinggi_badan ?? '',
                'berat_badan' => $student->berat_badan ?? '',
                'alamat_sesuai_kk' => $student->alamat_sesuai_kk ?? '',
                'alamat_sekarang' => $student->alamat_sekarang ?? '',
                'gol_darah' => $student->gol_darah ?? '',
                'penyakit_diderita' => $student->penyakit_diderita ?? '',
                'cacat_fisik' => $student->cacat_fisik ?? '',
                'alergi' => $student->alergi ?? '',
                'imunisasi' => $student->imunisasi ?? '',
                'nama_ayah' => $student->nama_ayah ?? '',
                'wa_ayah' => $student->wa_ayah ?? '',
                'nama_ibu' => $student->nama_ibu ?? '',
                'wa_ibu' => $student->wa_ibu ?? '',
                'pekerjaan_ayah' => $student->pekerjaan_ayah ?? '',
                'pekerjaan_ibu' => $student->pekerjaan_ibu ?? '',
                'created_at' => $student->created_at ?? '',
                'updated_at' => $student->updated_at ?? ''
            ]
        ]);
    } else {
        // Student not found
        echo json_encode([
            'success' => false,
            'message' => 'Santri dengan NIK tersebut tidak ditemukan'
        ]);
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data santri']);
}
?>