<?php
// fetch-student-data.php - Fetch student data from external API and store in local database

require_once __DIR__ . '/init-session.php';

// Allow requests from any origin during development
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With, X-Idempotency-Key');
header('Content-Type: application/json');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

try {
    // Fetch data from external API
    $externalApiUrl = 'https://insya-allah-berkah.mabaiz.com/data-santri.php';
    
    // Initialize cURL
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $externalApiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // Required for non-HTTPS connections
    curl_setopt($ch, CURLOPT_TIMEOUT, 30); // 30 second timeout
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    
    curl_close($ch);
    
    if ($error) {
        throw new Exception("cURL Error: " . $error);
    }
    
    if ($httpCode !== 200) {
        throw new Exception("HTTP Error: " . $httpCode);
    }
    
    if (!$response) {
        throw new Exception("Empty response from external API");
    }
    
    // Decode the JSON response
    $data = json_decode($response, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("JSON decode error: " . json_last_error_msg());
    }
    
    if (!$data || !isset($data['success']) || !$data['success'] || !isset($data['data'])) {
        throw new Exception("Invalid response format from external API");
    }
    
    // Get the students data
    $students = $data['data'];
    
    // Counter for successfully processed students
    $processedCount = 0;
    
    // Process each student
    foreach ($students as $studentData) {
        // Check if student already exists in the database
        $existingStudent = R::findOne('santri', 'external_id = ?', [$studentData['id']]);
        
        if ($existingStudent) {
            // Update existing student
            $student = $existingStudent;
        } else {
            // Create new student
            $student = R::dispense('santri');
        }
        
        // Map the external data to our local fields
        $student->external_id = $studentData['id'];
        $student->tahun_masuk = $studentData['tahun_masuk'] ?? '';
        $student->nama_sesuai_kk = $studentData['nama_sesuai_kk'] ?? '';
        $student->status = $studentData['Status'] ?? '';
        $student->nama_panggilan = $studentData['nama_panggilan'] ?? '';
        $student->no_kk = $studentData['no_kk'] ?? '';
        $student->nik = $studentData['nik'] ?? '';
        $student->nis = $studentData['nis'] ?? '';
        $student->nisn = $studentData['nisn'] ?? '';
        $student->asal_sekolah = $studentData['asal_sekolah'] ?? '';
        $student->alamat_sekolah = $studentData['alamat_sekolah'] ?? '';
        $student->tempat_lahir = $studentData['tempat_lahir'] ?? '';
        $student->tanggal_lahir = $studentData['tanggal_lahir'] ?? '';
        $student->jenis_kelamin = $studentData['jenis_kelamin'] ?? '';
        $student->anak_ke = $studentData['anak_ke'] ?? '';
        $student->jumlah_saudara = $studentData['jumlah_saudara'] ?? '';
        $student->status_anak = $studentData['status_anak'] ?? '';
        $student->tinggi_badan = $studentData['tinggi_badan'] ?? '';
        $student->berat_badan = $studentData['berat_badan'] ?? '';
        $student->alamat_sesuai_kk = $studentData['alamat_sesuai_kk'] ?? '';
        $student->alamat_sekarang = $studentData['alamat_sekarang'] ?? '';
        $student->gol_darah = $studentData['gol_darah'] ?? '';
        $student->penyakit_diderita = $studentData['penyakit_diderita'] ?? '';
        $student->cacat_fisik = $studentData['cacat_fisik'] ?? '';
        $student->alergi = $studentData['alergi'] ?? '';
        $student->imunisasi = $studentData['imunisasi'] ?? '';
        $student->nama_ayah = $studentData['nama_ayah'] ?? '';
        $student->wa_ayah = $studentData['wa_ayah'] ?? '';
        $student->nama_ibu = $studentData['nama_ibu'] ?? '';
        $student->wa_ibu = $studentData['wa_ibu'] ?? '';
        $student->pekerjaan_ayah = $studentData['pekerjaan_ayah'] ?? '';
        $student->pekerjaan_ibu = $studentData['pekerjaan_ibu'] ?? '';
        $student->updated_at = R::isoDateTime(); // Set the updated timestamp
        
        // If it's a new student, set the created timestamp
        if (!$existingStudent) {
            $student->created_at = R::isoDateTime();
        }
        
        // Store the student in the database
        R::store($student);
        $processedCount++;
    }
    
    // Return success response
    echo json_encode([
        'success' => true,
        'message' => 'Successfully fetched and stored student data',
        'count' => $processedCount
    ]);
    
} catch (Exception $e) {
    // Return error response
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}