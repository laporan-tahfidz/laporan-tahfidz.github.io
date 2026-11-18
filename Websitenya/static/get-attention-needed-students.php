<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Set CORS headers
setCORSHeaders();

header('Content-Type: application/json');

// Prevent direct execution when included for testing
if (!isset($_SERVER['REQUEST_METHOD']) && !isset($argv)) {
    return; // Return early if included for testing purposes
}

// Check if request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get the posted data
$input = json_decode(file_get_contents('php://input'), true);
$token = $input['token'] ?? '';

// Verify the token if provided
if ($token && !verifyToken($token)) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    // Get all students with their latest achievement and musyrif assignment
    $studentsWithDetails = R::getAll("
        SELECT
            s.id as santri_id,
            s.nama_sesuai_kk as nama,
            s.nik,
            s.tahun_masuk,
            m.nama as musyrif_nama,
            m.id as musyrif_id,
            p.type as last_achievement_type,
            p.juz as last_achievement_juz,
            p.halaman as last_achievement_halaman,
            p.posisi as last_achievement_posisi,
            p.syahadah as last_achievement_syahadah,
            p.created_at as last_achievement_created_at
        FROM santri s
        LEFT JOIN musyrfst ms ON s.nik = ms.santri_nik
        LEFT JOIN musyrif m ON ms.musyrif_id = m.id
        LEFT JOIN (
            SELECT DISTINCT
                p1.santri_id,
                p1.type,
                p1.juz,
                p1.halaman,
                p1.posisi,
                p1.syahadah,
                p1.created_at
            FROM pencapaian p1
            INNER JOIN (
                SELECT santri_id, MAX(created_at) as max_date
                FROM pencapaian
                GROUP BY santri_id
            ) p2 ON p1.santri_id = p2.santri_id AND p1.created_at = p2.max_date
        ) p ON s.id = p.santri_id
        WHERE LOWER(s.status) = 'aktif'
        ORDER BY m.nama ASC, s.nama_sesuai_kk ASC
    ");

    // Get class configuration to determine class levels
    // Get individual year values for each class
    $kelas1Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas1_year'");
    $kelas2Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas2_year'");
    $kelas3Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas3_year'");

    $classConfiguration = [
        'kelas1' => $kelas1Year,
        'kelas2' => $kelas2Year,
        'kelas3' => $kelas3Year
    ];

    // Process students to determine which ones need attention based on the four criteria
    $coordinatorAttention = [];
    $musyrifAttention = [];

    foreach ($studentsWithDetails as $student) {
        // Skip if student doesn't have a musyrif assigned
        if (empty($student['musyrif_nama'])) {
            continue;
        }

        // Skip if student doesn't have any achievement yet
        if (empty($student['last_achievement_type'])) {
            continue;
        }

        $lastAchievementDate = new DateTime($student['last_achievement_created_at'], new DateTimeZone('Asia/Makassar'));
        $now = new DateTime('now', new DateTimeZone('Asia/Makassar'));
        $daysSinceLastAchievement = $now->diff($lastAchievementDate)->days;

        $lamaPersiapan = $daysSinceLastAchievement . ' hari';

        // Convert days to months if more than 30 days
        if ($daysSinceLastAchievement >= 30) {
            $months = floor($daysSinceLastAchievement / 30);
            $remainingDays = $daysSinceLastAchievement % 30;
            $lamaPersiapan = $months . ' bulan';
            if ($remainingDays > 0) {
                $lamaPersiapan .= ' ' . $remainingDays . ' hari';
            }
        }

        // Check COORDINATOR ATTENTION CRITERIA:
        // 1. Persiapan Setengah juz sudah 11 hari (ziyadah at 5B/10B and 11+ days ago)
        // 2. Persiapan Juziyah sudah 22 hari (setengah_juz akhir and 22+ days ago)
        // 3. Persiapan Syahadah sudah 52 hari (juziyah at special juz and 52+ days ago)

        $needsCoordinatorAttention = false;
        $needsMusyrifAttention = false;
        $keterangan = '';

        // COORDINATOR CRITERIA 1: Persiapan Setengah juz sudah 11 hari
        if ($student['last_achievement_type'] === 'ziyadah' &&
            ($student['last_achievement_halaman'] === '5B' || $student['last_achievement_halaman'] === '10B') &&
            $daysSinceLastAchievement >= 11) {
            $needsCoordinatorAttention = true;
            $keterangan = 'Persiapan Setengah Juz';
        }
        // COORDINATOR CRITERIA 2: Persiapan Juziyah sudah 22 hari
        elseif ($student['last_achievement_type'] === 'setengah_juz' &&
                $student['last_achievement_posisi'] === 'akhir' &&
                $daysSinceLastAchievement >= 22) {
            $needsCoordinatorAttention = true;
            $keterangan = 'Persiapan Juziyah';
        }
        // COORDINATOR CRITERIA 3: Persiapan Syahadah sudah 52 hari
        elseif ($student['last_achievement_type'] === 'juziyah') {
            $specialJuz = [3, 8, 13, 18, 23, 28];
            if (in_array($student['last_achievement_juz'], $specialJuz) && $daysSinceLastAchievement >= 52) {
                $needsCoordinatorAttention = true;
                $keterangan = 'Persiapan Syahadah';
            }
        }

        // COORDINATOR CRITERIA 4: Belum Ziyadah minimal 1 halaman per 2 hari (dihitung dari Senin, masuk koordinator jika sudah 3+ hari / Rabu ke atas)
        if (!$needsCoordinatorAttention) {
            $todayDateZ = new DateTime('now', new DateTimeZone('Asia/Makassar'));
            $todayDateOnlyZ = new DateTime($todayDateZ->format('Y-m-d'), new DateTimeZone('Asia/Makassar'));
            $dayOfWeekZ = (int)$todayDateOnlyZ->format('N'); // 1 (Mon) to 7 (Sun)
            $currentWeekStartZ = clone $todayDateOnlyZ;
            $currentWeekStartZ->modify('-' . ($dayOfWeekZ - 1) . ' days');
            $totalDaysZ = $dayOfWeekZ;

            if ($totalDaysZ >= 3) {
                $safePeriodActiveZ = false;
                $specialZiyadahZ = R::getAll("
                    SELECT halaman, created_at
                    FROM pencapaian
                    WHERE santri_id = ?
                      AND (type = 'ziyadah' OR type = 'ziadah')
                      AND halaman IN ('5B', '10B')
                    ORDER BY created_at DESC
                    LIMIT 1
                ", [$student['santri_id']]);

                if (!empty($specialZiyadahZ)) {
                    $specialItemZ = $specialZiyadahZ[0];
                    $specialDateZ = new DateTime($specialItemZ['created_at'], new DateTimeZone('Asia/Makassar'));
                    $specialDateOnlyZ = new DateTime($specialDateZ->format('Y-m-d'), new DateTimeZone('Asia/Makassar'));
                    $daysDiffZ = (int)$specialDateOnlyZ->diff($todayDateOnlyZ)->format('%r%a');

                    if ($daysDiffZ >= 0) {
                        if ($specialItemZ['halaman'] === '5B' && $daysDiffZ <= 3) {
                            $safePeriodActiveZ = true;
                        } elseif ($specialItemZ['halaman'] === '10B' && $daysDiffZ <= 7) {
                            $safePeriodActiveZ = true;
                        }
                    }
                }

                if (!$safePeriodActiveZ) {
                    $otherAchievementsZ = R::getAll("
                        SELECT type, created_at
                        FROM pencapaian
                        WHERE santri_id = ?
                          AND (type = 'setengah_juz' OR type = 'juziyah' OR type = 'syahadah')
                          AND DATE(created_at) BETWEEN ? AND ?
                    ", [
                        $student['santri_id'],
                        $currentWeekStartZ->format('Y-m-d'),
                        $todayDateOnlyZ->format('Y-m-d')
                    ]);

                    if (!empty($otherAchievementsZ)) {
                        $earliestAchievementDateZ = null;
                        foreach ($otherAchievementsZ as $achievementZ) {
                            $achievementDateZ = new DateTime($achievementZ['created_at'], new DateTimeZone('Asia/Makassar'));
                            if (!$earliestAchievementDateZ || $achievementDateZ < $earliestAchievementDateZ) {
                                $earliestAchievementDateZ = $achievementDateZ;
                            }
                        }
                        $remainingDaysZ = max(0, (int)$earliestAchievementDateZ->diff($todayDateOnlyZ)->format('%r%a'));
                        $targetPagesZ = $remainingDaysZ * 0.5;
                    } else {
                        $targetPagesZ = $totalDaysZ * 0.5;
                    }

                    $targetPagesIntZ = (int) ceil($targetPagesZ);

                    $ziyadahAchievementsZ = R::getAll("
                        SELECT halaman, created_at
                        FROM pencapaian
                        WHERE santri_id = ?
                          AND (type = 'ziyadah' OR type = 'ziadah')
                          AND DATE(created_at) BETWEEN ? AND ?
                        ORDER BY created_at ASC
                    ", [
                        $student['santri_id'],
                        $currentWeekStartZ->format('Y-m-d'),
                        $todayDateOnlyZ->format('Y-m-d')
                    ]);

                    $ziyadahPagesCoveredZ = 0;
                    if (!empty($ziyadahAchievementsZ)) {
                        $uniquePagesZ = [];
                        foreach ($ziyadahAchievementsZ as $achievementZ) {
                            $pageZ = $achievementZ['halaman'];
                            if (!in_array($pageZ, $uniquePagesZ)) {
                                $uniquePagesZ[] = $pageZ;
                            }
                        }
                        $sortedPagesZ = sortHafalanPages($uniquePagesZ);
                        $ziyadahPagesCoveredZ = count($sortedPagesZ);
                    }

                    if ($ziyadahPagesCoveredZ < $targetPagesIntZ) {
                        $needsCoordinatorAttention = true;
                        $keterangan = 'Belum Ziyadah';
                    }
                }
            }
        }

        // If student meets coordinator criteria, add to coordinator attention
        if ($needsCoordinatorAttention) {
            $studentInfo = [
                'id' => $student['santri_id'],
                'nik' => $student['nik'],
                'nama' => $student['nama'],
                'keterangan' => $keterangan,
                'lama_persiapan' => $lamaPersiapan,
                'musyrif_nama' => $student['musyrif_nama'],
                'musyrif_id' => $student['musyrif_id']
            ];

            $coordinatorAttention[] = $studentInfo;
        }

        // Check MUSYRIF ATTENTION CRITERIA (the original 4 criteria):
        // 1. Persiapan Setengah juz sudah 4 hari (ziyadah at 5B/10B and 4+ days ago)
        // 2. Persiapan Juziyah sudah 8 hari (setengah_juz akhir and 8+ days ago)
        // 3. Persiapan Syahadah sudah 31 hari (juziyah at special juz and 31+ days ago)
        // 4. Weekly ziyadah requirements not met

        $needsMusyrifAttention = false;
        $keterangan = '';

        // MUSYRIF CRITERIA 1: Persiapan Setengah juz sudah 4 hari
        if ($student['last_achievement_type'] === 'ziyadah' &&
            ($student['last_achievement_halaman'] === '5B' || $student['last_achievement_halaman'] === '10B') &&
            $daysSinceLastAchievement >= 4 && $daysSinceLastAchievement < 11) { // Exclude those already in coordinator attention
            $needsMusyrifAttention = true;
            $keterangan = 'Persiapan Setengah Juz';
        }
        // MUSYRIF CRITERIA 2: Persiapan Juziyah sudah 8 hari
        elseif ($student['last_achievement_type'] === 'setengah_juz' &&
                $student['last_achievement_posisi'] === 'akhir' &&
                $daysSinceLastAchievement >= 8 && $daysSinceLastAchievement < 22) { // Exclude those already in coordinator attention
            $needsMusyrifAttention = true;
            $keterangan = 'Persiapan Juziyah';
        }
        // MUSYRIF CRITERIA 3: Persiapan Syahadah sudah 31 hari
        elseif ($student['last_achievement_type'] === 'juziyah') {
            $specialJuz = [3, 8, 13, 18, 23, 28];
            if (in_array($student['last_achievement_juz'], $specialJuz) &&
                $daysSinceLastAchievement >= 31 && $daysSinceLastAchievement < 52) { // Exclude those already in coordinator attention
                $needsMusyrifAttention = true;
                $keterangan = 'Persiapan Syahadah';
            }
        }
        // MUSYRIF CRITERIA 4: Daily ziyadah requirements
        // Check if student hasn't met ziyadah requirements based on daily targets (0.5 pages per day)
        // Also account for achievements that might have affected the target (Setengah Juz, Juziyah, Syahadah)
        elseif (!$needsCoordinatorAttention) { // Only check this if not already flagged for coordinator attention
            $currentWeekStart = new DateTime('monday this week', new DateTimeZone('Asia/Makassar'));
            $today = new DateTime('now', new DateTimeZone('Asia/Makassar')); // Today

            // Check if student has 5B or 10B ziyadah achievement with safe period (3 days for 5B, 7 days for 10B)
            $safePeriodActive = false;
            $specialZiyadah = R::getAll("
                SELECT halaman, created_at
                FROM pencapaian
                WHERE santri_id = ?
                  AND (type = 'ziyadah' OR type = 'ziadah')
                  AND halaman IN ('5B', '10B')
                ORDER BY created_at DESC
                LIMIT 1
            ", [$student['santri_id']]);

            if (!empty($specialZiyadah)) {
                $specialItem = $specialZiyadah[0];
                $specialDate = new DateTime($specialItem['created_at'], new DateTimeZone('Asia/Makassar'));
                $specialDateOnly = new DateTime($specialDate->format('Y-m-d'), new DateTimeZone('Asia/Makassar'));
                $todayDateOnly = new DateTime($today->format('Y-m-d'), new DateTimeZone('Asia/Makassar'));
                
                $daysDiff = (int)$specialDateOnly->diff($todayDateOnly)->format('%r%a');
                
                if ($daysDiff >= 0) {
                    if ($specialItem['halaman'] === '5B' && $daysDiff <= 3) {
                        $safePeriodActive = true;
                    } elseif ($specialItem['halaman'] === '10B' && $daysDiff <= 7) {
                        $safePeriodActive = true;
                    }
                }
            }

            if (!$safePeriodActive) {
                // Calculate the number of days from Monday to today
                $totalDays = $currentWeekStart->diff($today)->days + 1; // +1 to include today

                // Check for any Setengah Juz, Juziyah, or Syahadah achievements during this period
                $otherAchievements = R::getAll("
                    SELECT type, created_at
                    FROM pencapaian
                    WHERE santri_id = ?
                      AND (type = 'setengah_juz' OR type = 'juziyah' OR type = 'syahadah')
                      AND DATE(created_at) BETWEEN ? AND ?
                ", [
                    $student['santri_id'],
                    $currentWeekStart->format('Y-m-d'),
                    $today->format('Y-m-d')
                ]);

                // If there are other achievements, adjust the target based on remaining days
                if (!empty($otherAchievements)) {
                    // Find the earliest achievement date among setengah_juz, juziyah, or syahadah
                    $earliestAchievementDate = null;
                    foreach ($otherAchievements as $achievement) {
                        $achievementDate = new DateTime($achievement['created_at'], new DateTimeZone('Asia/Makassar'));
                        if (!$earliestAchievementDate || $achievementDate < $earliestAchievementDate) {
                            $earliestAchievementDate = $achievementDate;
                        }
                    }

                    // Calculate remaining days after the achievement
                    $remainingDays = max(0, $earliestAchievementDate->diff($today)->days);
                    $targetPages = $remainingDays * 0.5; // 0.5 pages per day
                } else {
                    // No other achievements, calculate target based on full period
                    $targetPages = $totalDays * 0.5; // 0.5 pages per day
                }

                // Get all ziyadah achievements for the current week (Monday until today) for this student
                $ziyadahAchievements = R::getAll("
                    SELECT halaman, created_at
                    FROM pencapaian
                    WHERE santri_id = ?
                      AND (type = 'ziyadah' OR type = 'ziadah')
                      AND DATE(created_at) BETWEEN ? AND ?
                    ORDER BY created_at ASC
                ", [
                    $student['santri_id'],
                    $currentWeekStart->format('Y-m-d'),
                    $today->format('Y-m-d')
                ]);

                // Calculate the total number of unique pages covered by considering the sequence of hafalan pages
                $ziyadahPagesCovered = 0;
                if (!empty($ziyadahAchievements)) {
                    // Create an array of all unique ziyadah pages achieved this week
                    $uniquePages = [];
                    foreach ($ziyadahAchievements as $achievement) {
                        $page = $achievement['halaman'];
                        if (!in_array($page, $uniquePages)) {
                            $uniquePages[] = $page;
                        }
                    }

                    // Sort the pages according to the hafalan sequence (1A, 1B, 2A, 2B, ..., 10B)
                    $sortedPages = sortHafalanPages($uniquePages);
                    $ziyadahPagesCovered = count($sortedPages);
                }

                // Check if student meets ziyadah requirements based on calculated target
                $targetPagesInt = (int) ceil($targetPages); // Round up to nearest integer for comparison
                if ($ziyadahPagesCovered < $targetPagesInt) {
                    $needsMusyrifAttention = true;
                    $keterangan = 'Belum mencapai target ziyadah minggu ini (' . $ziyadahPagesCovered . '/' . $targetPagesInt . ')';
                }
            }
        }

        // If student meets musyrif criteria (and not coordinator), add to musyrif attention
        if ($needsMusyrifAttention && !$needsCoordinatorAttention) {
            $studentInfo = [
                'id' => $student['santri_id'],
                'nik' => $student['nik'],
                'nama' => $student['nama'],
                'keterangan' => $keterangan,
                'lama_persiapan' => $lamaPersiapan,
                'musyrif_nama' => $student['musyrif_nama'],
                'musyrif_id' => $student['musyrif_id']
            ];

            $musyrifAttention[] = $studentInfo;
        }
    }

    // Group students by musyrif
    $coordinatorAttentionGrouped = [];
    foreach ($coordinatorAttention as $student) {
        $musyrifId = $student['musyrif_id'];
        $musyrifName = $student['musyrif_nama'];
        
        if (!isset($coordinatorAttentionGrouped[$musyrifId])) {
            $coordinatorAttentionGrouped[$musyrifId] = [
                'musyrif_nama' => $musyrifName,
                'students' => []
            ];
        }
        
        $coordinatorAttentionGrouped[$musyrifId]['students'][] = $student;
    }

    $musyrifAttentionGrouped = [];
    foreach ($musyrifAttention as $student) {
        $musyrifId = $student['musyrif_id'];
        $musyrifName = $student['musyrif_nama'];
        
        if (!isset($musyrifAttentionGrouped[$musyrifId])) {
            $musyrifAttentionGrouped[$musyrifId] = [
                'musyrif_nama' => $musyrifName,
                'students' => []
            ];
        }
        
        $musyrifAttentionGrouped[$musyrifId]['students'][] = $student;
    }

    echo json_encode([
        'success' => true,
        'coordinator_attention' => array_values($coordinatorAttentionGrouped),
        'musyrif_attention' => array_values($musyrifAttentionGrouped)
    ]);

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Terjadi kesalahan saat mengambil data santri yang perlu perhatian: ' . $e->getMessage()]);
}

/**
 * Helper function to sort hafalan pages according to the sequence (1A, 1B, 2A, 2B, ..., 10B)
 */
function sortHafalanPages($pages) {
    // Define the sequence of hafalan pages
    $sequence = [];
    for ($i = 1; $i <= 10; $i++) {
        $sequence[] = $i . 'A';
        $sequence[] = $i . 'B';
    }

    // Filter the sequence to only include pages that are in the input array
    $filteredSequence = array_filter($sequence, function($page) use ($pages) {
        return in_array($page, $pages);
    });

    return array_values($filteredSequence);
}
?>