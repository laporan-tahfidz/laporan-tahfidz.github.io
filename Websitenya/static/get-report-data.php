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
$startDate = $input['start_date'] ?? '';
$endDate = $input['end_date'] ?? '';

// Validate dates
if (empty($startDate) || empty($endDate)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Tanggal mulai dan tanggal selesai harus diisi']);
    exit;
}

// Validate date format (YYYY-MM-DD)
if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $startDate) || !preg_match('/^\d{4}-\d{2}-\d{2}$/', $endDate)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Format tanggal tidak valid. Gunakan format YYYY-MM-DD']);
    exit;
}

// Validate that end date is not before start date
if (strtotime($endDate) < strtotime($startDate)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Tanggal selesai tidak boleh sebelum tanggal mulai']);
    exit;
}

try {
    // Get all musyrifs with their assigned students
    $musyrifs = R::getAll("
        SELECT m.id, m.nama
        FROM musyrif m
        ORDER BY m.nama ASC
    ");

    // Process each musyrif and their students
    foreach ($musyrifs as &$musyrif) {
        // Get students assigned to this musyrif
        $students = R::getAll("
            SELECT s.id as santri_id, s.nama_sesuai_kk, s.nama_panggilan, s.nik, s.tahun_masuk
            FROM musyrfst ms
            JOIN santri s ON ms.santri_nik = s.nik
            WHERE ms.musyrif_id = ?
            ORDER BY s.nama_sesuai_kk ASC
        ", [$musyrif['id']]);

        $musyrif['students'] = [];

        foreach ($students as &$student) {
            // Get all achievements for this student during the specified period
            $achievements = R::getAll("
                SELECT type, juz, halaman, posisi, syahadah, kesalahan, created_at
                FROM pencapaian
                WHERE nik = ?
                AND DATE(created_at) BETWEEN ? AND ?
                ORDER BY created_at DESC
            ", [$student['nik'], $startDate, $endDate]);

            // Get the last achievement for this student (before the end date)
            $lastAchievement = R::getRow("
                SELECT type, juz, halaman, posisi, syahadah, kesalahan, created_at
                FROM pencapaian
                WHERE nik = ?
                AND DATE(created_at) <= ?
                ORDER BY created_at DESC
                LIMIT 1
            ", [$student['nik'], $endDate]);
            
            // Also get all achievements during the specified period
            $achievementsDuringPeriod = R::getAll("
                SELECT type, juz, halaman, posisi, syahadah, kesalahan, created_at
                FROM pencapaian
                WHERE nik = ?
                AND DATE(created_at) BETWEEN ? AND ?
                ORDER BY created_at ASC
            ", [$student['nik'], $startDate, $endDate]);

            // Get all laporan sabtu for this student during the specified period
            $laporanSabtu = R::getAll("
                SELECT murajaahentries, hafalanentries, created_at
                FROM laporansabtu
                WHERE nik = ?
                AND DATE(created_at) BETWEEN ? AND ?
                ORDER BY created_at ASC
            ", [$student['nik'], $startDate, $endDate]);

            // Get all tes entries for this student during the specified period
            $tesEntries = R::getAll("
                SELECT juz, status, created_at
                FROM tes
                WHERE nik = ?
                AND DATE(created_at) BETWEEN ? AND ?
                ORDER BY created_at ASC
            ", [$student['nik'], $startDate, $endDate]);

            // Add achievements, laporan sabtu, and tes entries to the student data
            $student['achievements'] = $achievementsDuringPeriod; // Use achievements during the period for calculations
            $student['last_hafalan'] = $lastAchievement;
            $student['laporan_sabtu'] = $laporanSabtu;
            $student['tes_entries'] = $tesEntries;

            $musyrif['students'][] = $student;
        }
    }

    echo json_encode([
        'success' => true,
        'data' => [
            'musyrifs' => $musyrifs,
            'start_date' => $startDate,
            'end_date' => $endDate
        ]
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Terjadi kesalahan saat mengambil data laporan: ' . $e->getMessage()
    ]);
}

R::close();
?>