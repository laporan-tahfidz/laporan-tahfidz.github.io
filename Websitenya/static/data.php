<?php
// Suppress deprecation warnings on PHP 8.4+
error_reporting(E_ALL & ~E_DEPRECATED);

// Set timezone to Asia/Makassar according to user rule
date_default_timezone_set('Asia/Makassar');

// CORS headers
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Idempotency-Key');

if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

header('Content-Type: application/json; charset=utf-8');

require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions-settings.php';

try {
    if (!R::testConnection()) {
        R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');
    }

    function formatHalamanToCount($hal) {
        if (!$hal) return '';
        $hal = strtoupper(trim($hal));
        if (preg_match('/^(\d+)([AB])$/', $hal, $matches)) {
            $num = (int)$matches[1];
            $letter = $matches[2];
            return ($num - 1) * 2 + ($letter === 'A' ? 1 : 2);
        }
        return $hal;
    }

    // Handle POST request to save configuration
    if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST') {
        $input = json_decode(file_get_contents('php://input'), true);
        if (isset($input['action']) && $input['action'] === 'save_configuration') {
            if (!empty($input['kelas1'])) {
                setSetting('kelas1_year', (string)$input['kelas1']);
            }
            if (!empty($input['kelas2'])) {
                setSetting('kelas2_year', (string)$input['kelas2']);
            }
            if (!empty($input['kelas3'])) {
                setSetting('kelas3_year', (string)$input['kelas3']);
            }
        }
    }

    // Get class configuration from query parameters or database settings
    $k1 = (!empty($_GET['kelas1'])) ? (string)$_GET['kelas1'] : (getSetting('kelas1_year') ?: '2026');
    $k2 = (!empty($_GET['kelas2'])) ? (string)$_GET['kelas2'] : (getSetting('kelas2_year') ?: '2025');
    $k3 = (!empty($_GET['kelas3'])) ? (string)$_GET['kelas3'] : (getSetting('kelas3_year') ?: '2024');

    // Available years from santri table
    $availableYears = R::getCol("SELECT DISTINCT tahun_masuk FROM santri WHERE tahun_masuk IS NOT NULL AND tahun_masuk != '' ORDER BY tahun_masuk DESC");
    if (empty($availableYears)) {
        $availableYears = ['2026', '2025', '2024'];
    }

    // User specification:
    // Kelas 7 = kelas 1 di database
    // Kelas 8 = kelas 2 di database
    // Kelas 9 = kelas 3 di database
    $classMap = [
        $k1 => 7,
        $k2 => 8,
        $k3 => 9
    ];

    $results = [];
    $counter = 1;

    foreach ($classMap as $year => $kelasDisplay) {
        $students = R::findAll('santri', 'tahun_masuk = ? AND status = ? ORDER BY nama_sesuai_kk ASC', [$year, 'Aktif']);
        
        foreach ($students as $student) {
            $nik = $student->nik;
            $latest = R::findOne('pencapaian', 'nik = ? ORDER BY created_at DESC, id DESC', [$nik]);
            
            $pencapaian = '-';
            if ($latest) {
                if ($latest->type === 'ziyadah') {
                    $halCount = formatHalamanToCount($latest->halaman);
                    $pencapaian = "Juz {$latest->juz}, {$halCount} halaman";
                } elseif ($latest->type === 'juziyah' || $latest->type === 'syahadah') {
                    $pencapaian = "Juz {$latest->juz}, 20 halaman";
                } elseif ($latest->type === 'setengah_juz') {
                    $halCount = (isset($latest->posisi) && $latest->posisi === 'awal') ? 10 : 20;
                    $pencapaian = "Juz {$latest->juz}, {$halCount} halaman";
                } else {
                    $pencapaian = "Juz {$latest->juz}";
                }
            }
            
            $results[] = [
                'no' => $counter++,
                'nama' => $student->nama_sesuai_kk,
                'kelas' => $kelasDisplay,
                'pencapaian' => $pencapaian
            ];
        }
    }

    echo json_encode([
        'success' => true,
        'configuration' => [
            'kelas1' => (string)$k1,
            'kelas2' => (string)$k2,
            'kelas3' => (string)$k3
        ],
        'available_years' => array_values($availableYears),
        'total' => count($results),
        'data' => $results
    ], JSON_UNESCAPED_UNICODE);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}
