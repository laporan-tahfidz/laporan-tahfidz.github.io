<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/functions-settings.php';
require_once __DIR__ . '/quran-mapping.php';

// Initialize the database connection directly
$dbPath = __DIR__ . '/everynight-in-my-dream.db';
R::setup("sqlite:$dbPath");
R::freeze(true);

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
$token = $input['token'] ?? '';
$semester = $input['semester'] ?? ''; // 'ganjil' or 'genap'
$tahunAjaran = $input['tahun_ajaran'] ?? ''; // e.g., '2024/2025'
$tanggalMulai = $input['tanggal_mulai'] ?? ''; // YYYY-MM-DD
$tanggalSelesai = $input['tanggal_selesai'] ?? ''; // YYYY-MM-DD

// Verify the token if provided
// if ($token && !verifyToken($token)) {
//     http_response_code(401);
//     echo json_encode(['success' => false, 'message' => 'Unauthorized']);
//     exit;
// }

if (empty($semester) || empty($tahunAjaran) || empty($tanggalMulai) || empty($tanggalSelesai)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Semester, tahun ajaran, dan rentang tanggal harus diisi']);
    exit;
}

try {
    // Get all students
    $students = R::getAll("SELECT * FROM santri ORDER BY nama_sesuai_kk ASC");
    
    // Get settings for class configuration
    $kelas1Year = getSetting('kelas1_year') ?: 'Ula';
    $kelas2Year = getSetting('kelas2_year') ?: 'Tsaniyah';
    $kelas3Year = getSetting('kelas3_year') ?: 'Tsalitsah';
    
    // Syahadah juz groupings
    $syahadahGroups = [
        'pertama' => [30, 29, 1, 2, 3],
        'kedua' => [4, 5, 6, 7, 8],
        'ketiga' => [9, 10, 11, 12, 13],
        'keempat' => [14, 15, 16, 17, 18],
        'kelima' => [19, 20, 21, 22, 23],
        'keenam' => [24, 25, 26, 27, 28],
    ];
    
    $rapotData = [];
    
    foreach ($students as $student) {
        $studentId = $student['id'];
        
        // Get achievements within date range
        $achievements = R::getAll("
            SELECT * FROM pencapaian 
            WHERE santri_id = ? 
            AND created_at >= ? 
            AND created_at <= ?
            ORDER BY created_at DESC
        ", [$studentId, $tanggalMulai . ' 00:00:00', $tanggalSelesai . ' 23:59:59']);
        
        if (empty($achievements)) {
            continue; // Skip students with no achievements
        }
        
        // Get the last achievement
        $lastAchievement = $achievements[0];
        $lastAchievementText = formatLastAchievement(
            $lastAchievement['type'],
            $lastAchievement['juz'],
            $lastAchievement['halaman']
        );
        
        // Determine marhalah based on student's tahun_masuk matching class configuration
        $marhalah = 'Ula'; // Default fallback
        $tahunMasuk = $student['tahun_masuk'] ?? '';
        
        if ($tahunMasuk == $kelas1Year) {
            $marhalah = 'Ula';
        } elseif ($tahunMasuk == $kelas2Year) {
            $marhalah = 'Tsaniyah';
        } elseif ($tahunMasuk == $kelas3Year) {
            $marhalah = 'Tsalitsah';
        } else {
            // If tahun_masuk doesn't match any class year, use the value from settings as fallback
            $marhalah = $kelas1Year;
        }
        
        // Process syahadah achievements
        $syahadahData = [];
        $juziyahData = [];
        
        foreach ($achievements as $achievement) {
            if ($achievement['type'] === 'syahadah') {
                $tingkatan = $achievement['syahadah']; // pertama, kedua, etc.
                if (isset($syahadahGroups[$tingkatan])) {
                    $juzList = $syahadahGroups[$tingkatan];
                    $totalKesalahan = 0;
                    $count = 0;
                    
                    // Calculate average kesalahan for this syahadah
                    $syahadahAchievements = array_filter($achievements, function($a) use ($tingkatan) {
                        return $a['type'] === 'syahadah' && $a['syahadah'] === $tingkatan;
                    });
                    
                    foreach ($syahadahAchievements as $sa) {
                        if ($sa['kesalahan'] !== null) {
                            $totalKesalahan += intval($sa['kesalahan']);
                            $count++;
                        }
                    }
                    
                    if ($count > 0) {
                        $avgKesalahan = $totalKesalahan / $count;
                        $nilaiKuantitatif = calculateSyahadahScore($avgKesalahan);
                        $nilaiKualitatif = getQualitativeValue('syahadah', $avgKesalahan);
                        
                        $syahadahData[] = [
                            'id' => $achievement['id'],
                            'tingkatan' => $tingkatan,
                            'juz' => implode(', ', $juzList),
                            'nilai_kuantitatif' => round($nilaiKuantitatif),
                            'nilai_kualitatif' => $nilaiKualitatif,
                            'catatan' => $achievement['catatan'] ?: '',
                        ];
                    }
                }
            } elseif ($achievement['type'] === 'juziyah') {
                // Check if this juz is not already included
                $juz = intval($achievement['juz']);
                $alreadyIncluded = false;
                foreach ($juziyahData as $jd) {
                    if (in_array($juz, $jd['juz_list'])) {
                        $alreadyIncluded = true;
                        break;
                    }
                }
                
                if (!$alreadyIncluded && $achievement['kesalahan'] !== null) {
                    $nilaiKuantitatif = calculateJuziyahScore(intval($achievement['kesalahan']));
                    $nilaiKualitatif = getQualitativeValue('juziyah', intval($achievement['kesalahan']));
                    
                    $juziyahData[] = [
                        'id' => $achievement['id'],
                        'juz' => $juz,
                        'juz_list' => [$juz],
                        'nilai_kuantitatif' => round($nilaiKuantitatif),
                        'nilai_kualitatif' => $nilaiKualitatif,
                        'catatan' => $achievement['catatan'] ?: '',
                    ];
                }
            }
        }
        
        // Sort juziyah by proper order: 30, 29, 1, 2, 3, 4, ..., 28
        usort($juziyahData, function($a, $b) {
            $order = [30, 29, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28];
            $posA = array_search($a['juz'], $order);
            $posB = array_search($b['juz'], $order);
            return $posA - $posB;
        });
        
        // Sort syahadah by proper order
        $syahadahOrder = ['pertama', 'kedua', 'ketiga', 'keempat', 'kelima', 'keenam'];
        usort($syahadahData, function($a, $b) use ($syahadahOrder) {
            $posA = array_search($a['tingkatan'], $syahadahOrder);
            $posB = array_search($b['tingkatan'], $syahadahOrder);
            return $posA - $posB;
        });
        
        $rapotData[] = [
            'student_id' => $studentId,
            'nama' => $student['nama_sesuai_kk'] ?: $student['nama_panggilan'],
            'nis' => $student['nis'],
            'marhalah' => $marhalah,
            'pencapaian_terakhir' => $lastAchievementText,
            'syahadah' => $syahadahData,
            'juziyah' => $juziyahData,
        ];
    }
    
    echo json_encode([
        'success' => true,
        'rapot_data' => $rapotData,
        'semester' => $semester,
        'tahun_ajaran' => $tahunAjaran,
        'tanggal_mulai' => $tanggalMulai,
        'tanggal_selesai' => $tanggalSelesai,
    ]);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat menghasilkan rapot: ' . $e->getMessage()]);
}

/**
 * Calculate Juziyah score (100 - errors, min 0)
 */
function calculateJuziyahScore($kesalahan) {
    return max(0, 100 - intval($kesalahan));
}

/**
 * Calculate Syahadah score (100 - errors, min 0)
 */
function calculateSyahadahScore($kesalahan) {
    return max(0, 100 - intval($kesalahan));
}

/**
 * Get qualitative value based on achievement type and number of errors
 */
function getQualitativeValue($type, $errors) {
    if ($type === 'juziyah') {
        if ($errors >= 0 && $errors <= 5) {
            return 'Mumtaz';
        } elseif ($errors > 5 && $errors <= 10) {
            return 'Jayyid Jiddan';
        } elseif ($errors > 10 && $errors <= 15) {
            return 'Jayyid';
        } elseif ($errors > 15 && $errors <= 20) {
            return 'Maqbul';
        } elseif ($errors > 20) {
            return 'Mardud';
        }
    } elseif ($type === 'syahadah') {
        if ($errors >= 0 && $errors <= 10) {
            return 'Mumtaz';
        } elseif ($errors > 10 && $errors <= 20) {
            return 'Jayyid Jiddan';
        } elseif ($errors > 20 && $errors <= 30) {
            return 'Jayyid';
        } elseif ($errors > 30 && $errors <= 40) {
            return 'Maqbul';
        } elseif ($errors > 40) {
            return 'Mardud';
        }
    }
    return 'Unknown';
}
?>
