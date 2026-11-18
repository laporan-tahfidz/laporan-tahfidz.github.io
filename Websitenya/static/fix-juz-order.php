<?php
// fix-juz-order.php - Otomatis memperbaiki nomor juz santri agar berurutan
error_reporting(E_ALL & ~E_DEPRECATED);

require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/library/rb-sqlite.php';

// Set CORS headers
setCORSHeaders();

header('Content-Type: application/json');

// Handle preflight OPTIONS
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed. Gunakan metode POST.']);
    exit();
}

// Initialize database
initDB();

// Read input
$input = json_decode(file_get_contents('php://input'), true);
$token = $input['token'] ?? '';
$studentIdInput = $input['studentId'] ?? '';

// Verify token if provided
if ($token && !verifyToken($token)) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized. Token tidak valid atau kadaluarsa.']);
    exit();
}

/**
 * Konversi halaman hafalan ke nomor urut halaman (1A -> 1, 1B -> 2, ..., 10B -> 20)
 */
function pageOrder($hal) {
    if (!$hal) return null;
    $trimmed = trim($hal);
    $num = intval(substr($trimmed, 0, -1));
    $side = strtoupper(substr($trimmed, -1));
    if ($num < 1 || $num > 10) return null;
    return ($num - 1) * 2 + ($side === 'B' ? 2 : 1);
}

/**
 * Segmentasi riwayat pencapaian santri ke dalam blok-blok juz berdasarkan alur halaman dan jenis ujian
 */
function segmentStudentRecords($rows) {
    $blocks = [];
    $currentBlock = [];

    $prevWasJuziyah = false;
    $maxPageOrdInBlock = 0;

    foreach ($rows as $r) {
        $pOrd = pageOrder($r['halaman'] ?? '');
        $isNewBlock = false;

        if (empty($currentBlock)) {
            $isNewBlock = true;
        } else {
            // Kondisi 1: Catatan sebelumnya adalah juziyah/syahadah, dan catatan sekarang memulai ziyadah baru
            if ($prevWasJuziyah) {
                if ($r['type'] === 'ziyadah' && $pOrd !== null && $pOrd <= 4) {
                    $isNewBlock = true;
                } elseif ($r['type'] === 'ziyadah' && $pOrd !== null && $maxPageOrdInBlock >= 16) {
                    $isNewBlock = true;
                }
            }

            // Kondisi 2: Nomor halaman turun signifikan (misal dari >= 5B / 10 ke <= 1B / 2, atau >= 8A ke <= 2B)
            if (!$isNewBlock && $pOrd !== null) {
                if (($pOrd <= 2 && $maxPageOrdInBlock >= 10) || ($pOrd <= 4 && $maxPageOrdInBlock >= 16)) {
                    $isNewBlock = true;
                }
            }

            // Kondisi 3: Catatan sebelumnya adalah setengah_juz akhir dan catatan sekarang ziyadah halaman awal (<= 2B)
            $lastRec = end($currentBlock);
            if (!$isNewBlock && $lastRec['type'] === 'setengah_juz' && $lastRec['posisi'] === 'akhir' && $r['type'] === 'ziyadah' && $pOrd !== null && $pOrd <= 4) {
                $isNewBlock = true;
            }
        }

        if ($isNewBlock && !empty($currentBlock)) {
            $blocks[] = $currentBlock;
            $currentBlock = [];
            $maxPageOrdInBlock = 0;
        }

        $currentBlock[] = $r;
        if ($pOrd !== null && $pOrd > $maxPageOrdInBlock) {
            $maxPageOrdInBlock = $pOrd;
        }

        if ($r['type'] === 'juziyah' || $r['type'] === 'syahadah') {
            $prevWasJuziyah = true;
        } else {
            $prevWasJuziyah = false;
        }
    }

    if (!empty($currentBlock)) {
        $blocks[] = $currentBlock;
    }

    return $blocks;
}

/**
 * Hitung daftar perbaikan juz untuk santri tertentu
 */
function calculateFixesForStudent($studentId) {
    $intStudentId = intval($studentId);
    $rows = R::getAll("
        SELECT id, santri_id, type, juz, halaman, posisi, syahadah, catatan, kesalahan, created_at
        FROM pencapaian
        WHERE santri_id = ?
        ORDER BY created_at ASC, id ASC
    ", [$intStudentId]);

    if (empty($rows)) {
        return ['fixes' => [], 'blocks' => []];
    }

    $blocks = segmentStudentRecords($rows);
    $blockConsensus = [];

    // Pass 1: Tentukan juz konsensus tiap blok dengan pembobotan
    foreach ($blocks as $idx => $b) {
        $juzCounts = [];
        foreach ($b as $r) {
            if (!empty($r['juz'])) {
                $j = intval($r['juz']);
                if ($j > 0) {
                    $weight = ($r['type'] === 'juziyah' ? 5 : ($r['type'] === 'setengah_juz' ? 2 : 1));
                    $juzCounts[$j] = ($juzCounts[$j] ?? 0) + $weight;
                }
            }
        }
        if (!empty($juzCounts)) {
            arsort($juzCounts);
            $blockConsensus[$idx] = key($juzCounts);
        } else {
            $blockConsensus[$idx] = null;
        }
    }

    // Pass 2: Penghalusan sekuensial jika ada blok yang tidak memiliki konsensus jelas
    for ($i = 0; $i < count($blocks); $i++) {
        $prev = ($i > 0 && isset($blockConsensus[$i - 1])) ? $blockConsensus[$i - 1] : null;
        $next = ($i < count($blocks) - 1 && isset($blockConsensus[$i + 1])) ? $blockConsensus[$i + 1] : null;

        if ($blockConsensus[$i] === null) {
            if ($prev !== null && $next !== null && $next === $prev + 2) {
                $blockConsensus[$i] = $prev + 1;
            } elseif ($prev !== null && $next !== null && $next === $prev - 2) {
                $blockConsensus[$i] = $prev - 1;
            } elseif ($prev !== null) {
                $blockConsensus[$i] = $prev + 1;
            } elseif ($next !== null) {
                $blockConsensus[$i] = $next - 1;
            }
        }
    }

    // Pass 3: Kumpulkan catatan yang berbeda dari konsensus juz bloknya
    $fixes = [];
    foreach ($blocks as $idx => $b) {
        $targetJuz = $blockConsensus[$idx];
        if (!$targetJuz) continue;

        foreach ($b as $r) {
            if ($r['type'] === 'syahadah' && empty($r['juz'])) {
                continue;
            }
            if (intval($r['juz']) !== intval($targetJuz)) {
                $fixes[] = [
                    'id' => intval($r['id']),
                    'old_juz' => $r['juz'],
                    'new_juz' => $targetJuz,
                    'type' => $r['type'],
                    'halaman' => $r['halaman'],
                    'posisi' => $r['posisi'],
                    'created_at' => $r['created_at']
                ];
            }
        }
    }

    return [
        'fixes' => $fixes,
        'blocks' => $blockConsensus
    ];
}

/**
 * Terapkan perbaikan juz ke database
 */
function applyFixes($fixes) {
    $now = date('Y-m-d H:i:s');
    $count = 0;
    foreach ($fixes as $fix) {
        $bean = R::load('pencapaian', $fix['id']);
        if ($bean && $bean->id) {
            $bean->juz = intval($fix['new_juz']);
            $bean->updated_at = $now;
            R::store($bean);
            $count++;
        }
    }
    return $count;
}

try {
    // Mode 1: Perbaiki untuk satu santri tertentu
    if (!empty($studentIdInput) && $studentIdInput !== 'all') {
        $realStudentId = null;
        $studentName = '';

        // Cari berdasarkan id numerik
        if (is_numeric($studentIdInput)) {
            $sBean = R::load('santri', intval($studentIdInput));
            if ($sBean && $sBean->id) {
                $realStudentId = $sBean->id;
                $studentName = $sBean->nama_sesuai_kk ?: ($sBean->nama ?: "Santri #{$sBean->id}");
            }
        }

        // Jika belum ketemu, cari berdasarkan NIK
        if (!$realStudentId) {
            $sRow = R::getRow("SELECT id, nama, nama_sesuai_kk FROM santri WHERE nik = ?", [$studentIdInput]);
            if ($sRow) {
                $realStudentId = $sRow['id'];
                $studentName = $sRow['nama_sesuai_kk'] ?: ($sRow['nama'] ?: "Santri #{$sRow['id']}");
            }
        }

        if (!$realStudentId) {
            http_response_code(404);
            echo json_encode(['success' => false, 'message' => "Data santri dengan ID/NIK '{$studentIdInput}' tidak ditemukan."]);
            exit();
        }

        $calc = calculateFixesForStudent($realStudentId);
        $fixes = $calc['fixes'];

        if (empty($fixes)) {
            echo json_encode([
                'success' => true,
                'message' => "Urutan juz untuk {$studentName} sudah benar, tidak ada catatan yang perlu diperbaiki.",
                'fixedCount' => 0,
                'details' => []
            ]);
            exit();
        }

        $applied = applyFixes($fixes);

        echo json_encode([
            'success' => true,
            'message' => "Berhasil memperbaiki {$applied} catatan juz untuk {$studentName} agar urut.",
            'fixedCount' => $applied,
            'details' => $fixes
        ]);
        exit();
    }

    // Mode 2: Perbaiki untuk semua santri
    $allStudents = R::getAll("SELECT id, nama, nama_sesuai_kk FROM santri ORDER BY id ASC");
    $totalFixed = 0;
    $studentsFixedCount = 0;
    $allDetails = [];

    foreach ($allStudents as $s) {
        $calc = calculateFixesForStudent($s['id']);
        if (!empty($calc['fixes'])) {
            $applied = applyFixes($calc['fixes']);
            if ($applied > 0) {
                $totalFixed += $applied;
                $studentsFixedCount++;
                $sName = $s['nama_sesuai_kk'] ?: ($s['nama'] ?: "Santri #{$s['id']}");
                $allDetails[] = [
                    'student_id' => $s['id'],
                    'student_name' => $sName,
                    'fixed_count' => $applied,
                    'fixes' => $calc['fixes']
                ];
            }
        }
    }

    if ($totalFixed === 0) {
        echo json_encode([
            'success' => true,
            'message' => "Semua urutan juz santri sudah benar, tidak ada catatan yang perlu diperbaiki.",
            'fixedCount' => 0,
            'studentsCount' => 0,
            'details' => []
        ]);
        exit();
    }

    echo json_encode([
        'success' => true,
        'message' => "Berhasil memperbaiki {$totalFixed} catatan juz pada {$studentsFixedCount} santri agar urut.",
        'fixedCount' => $totalFixed,
        'studentsCount' => $studentsFixedCount,
        'details' => $allDetails
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Terjadi kesalahan saat memperbaiki urutan juz: ' . $e->getMessage()
    ]);
}
