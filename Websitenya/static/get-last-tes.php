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

try {
    // Find the last tes for the student
    $lastTes = R::findOne('tes', 'nik = ? ORDER BY created_at DESC', [$nik]);

    // Define standard juz sequence: 30, 29, 1, 2, ..., 28
    $sequence = [30, 29];
    for ($i = 1; $i <= 28; $i++) {
        $sequence[] = $i;
    }

    // Get all achievements for this student
    $achievements = R::getAll("
        SELECT type, juz, syahadah 
        FROM pencapaian 
        WHERE nik = ?
    ", [$nik]);

    $maxPosition = 0;
    $explicitJuz = [];

    foreach ($achievements as $ach) {
        $juz = null;
        if ($ach['type'] === 'syahadah' && !empty($ach['syahadah'])) {
            $sVal = strtolower((string)$ach['syahadah']);
            if (strpos($sVal, 'pertama') !== false || strpos($sVal, '1') !== false) $juz = 3;
            elseif (strpos($sVal, 'kedua') !== false || strpos($sVal, '2') !== false) $juz = 8;
            elseif (strpos($sVal, 'ketiga') !== false || strpos($sVal, '3') !== false) $juz = 13;
            elseif (strpos($sVal, 'keempat') !== false || strpos($sVal, '4') !== false) $juz = 18;
            elseif (strpos($sVal, 'kelima') !== false || strpos($sVal, '5') !== false) $juz = 23;
            elseif (strpos($sVal, 'keenam') !== false || strpos($sVal, '6') !== false) $juz = 28;
        } elseif (!empty($ach['juz'])) {
            $juz = (int)$ach['juz'];
            $explicitJuz[] = $juz;
        }

        if ($juz !== null) {
            $pos = array_search($juz, $sequence);
            if ($pos !== false && ($pos + 1) > $maxPosition) {
                $maxPosition = $pos + 1;
            }
        }
    }

    $submittedJuzMap = [];
    for ($pos = 0; $pos < $maxPosition; $pos++) {
        $submittedJuzMap[$sequence[$pos]] = true;
    }
    foreach ($explicitJuz as $j) {
        $submittedJuzMap[$j] = true;
    }

    // Order submitted juz according to sequence
    $submittedJuz = [];
    foreach ($sequence as $j) {
        if (isset($submittedJuzMap[$j])) {
            $submittedJuz[] = $j;
        }
    }

    // Get all distinct lancar juz from tes for this student
    $lancarJuzRaw = R::getCol("
        SELECT DISTINCT juz
        FROM tes
        WHERE nik = ? AND juz IS NOT NULL AND (status IS NULL OR status = 'lancar' OR status != 'tidak_lancar')
        ORDER BY CAST(juz AS INTEGER) ASC
    ", [$nik]);

    $lancarJuz = array_map('intval', $lancarJuzRaw);

    echo json_encode([
        'success' => true,
        'tes' => $lastTes ? [
            'id' => $lastTes->id,
            'juz' => $lastTes->juz,
            'status' => $lastTes->status ?? 'lancar',
            'santri_id' => $lastTes->santri_id,
            'nik' => $lastTes->nik,
            'created_at' => $lastTes->created_at,
            'updated_at' => $lastTes->updated_at
        ] : null,
        'submitted_juz' => $submittedJuz,
        'lancar_juz' => $lancarJuz
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data tes']);
}
?>