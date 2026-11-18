<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/functions-settings.php';
require_once __DIR__ . '/helpers.php';

// Initialize the database connection
initDB();

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

// Verify the token - function will check both request body and Authorization header
if (!verifyToken()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    // Get class year configurations from settings
    $kelas1Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas1_year'");
    $kelas2Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas2_year'");
    $kelas3Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas3_year'");

    // Get all musyrifs with their assigned students
    $musyrifs = R::getAll("
        SELECT m.id, m.nama
        FROM musyrif m
        ORDER BY m.nama ASC
    ");

    // For each musyrif, get their assigned students and their progress
    foreach ($musyrifs as &$musyrif) {
        // Get students assigned to this musyrif with their tahun_masuk
        $students = R::getAll("
            SELECT s.id as santri_id, s.nama_sesuai_kk, s.nik, s.tahun_masuk
            FROM musyrfst ms
            JOIN santri s ON ms.santri_nik = s.nik
            WHERE ms.musyrif_id = ?
            ORDER BY s.nama_sesuai_kk ASC
        ", [$musyrif['id']]);

        $musyrif['students'] = [];

        foreach ($students as &$student) {
            // Determine the class based on tahun_masuk
            $class = 0; // Default: not in any class
            if ($student['tahun_masuk'] == $kelas1Year) {
                $class = 1;
            } elseif ($student['tahun_masuk'] == $kelas2Year) {
                $class = 2;
            } elseif ($student['tahun_masuk'] == $kelas3Year) {
                $class = 3;
            }
            $student['class'] = $class;
            // Get achievement data for this student (for each juz)
            // Include all types of achievements that represent hafalan progress
            $achievements = R::getAll("
                SELECT DISTINCT juz
                FROM pencapaian
                WHERE nik = ?
                AND type IN ('ziyadah', 'setengah_juz', 'juziyah', 'syahadah')
            ", [$student['nik']]);

            // Get test data for this student (for each juz)
            $tests = R::getAll("
                SELECT juz, status, created_at
                FROM tes
                WHERE nik = ? AND juz IS NOT NULL
                ORDER BY created_at ASC
            ", [$student['nik']]);

            // Create a map of latest test status and count per juz
            $testStatusMap = [];
            $testCountMap = [];
            foreach ($tests as $test) {
                $juz = (int)$test['juz'];
                $testStatusMap[$juz] = $test['status'] ?? 'lancar';
                $testCountMap[$juz] = ($testCountMap[$juz] ?? 0) + 1;
            }

            // Determine all achieved juz based on the sequence: 30, 29, 1, 2, 3, ..., 28
            // Position mapping: [30, 29, 1, 2, 3, 4, ..., 28]
            // If a student has achieved a certain juz, they have also achieved all previous juz in the sequence
            $achievedJuz = [];

            // Convert the sequence to a position mapping
            $sequence = [30, 29]; // positions 1 and 2
            for ($i = 1; $i <= 28; $i++) {
                $sequence[] = $i; // positions 3 to 30 (juz 1 to juz 28)
            }

            // Find the highest position achieved by this student in the sequence
            $maxPosition = 0;
            foreach ($achievements as $achievement) {
                $juz = $achievement['juz'];
                // Find the position of this juz in the sequence
                $position = array_search($juz, $sequence);
                if ($position !== false && $position + 1 > $maxPosition) { // +1 because array_search is 0-indexed
                    $maxPosition = $position + 1;
                }
            }

            // Mark all juz in the sequence up to the highest achieved position as achieved
            for ($pos = 0; $pos < $maxPosition; $pos++) {
                $juzInPosition = $sequence[$pos];
                $achievedJuz[$juzInPosition] = true;
            }

            // Create progress data for each juz (1-30)
            $progress = [];
            for ($juz = 1; $juz <= 30; $juz++) {
                if (isset($testStatusMap[$juz])) {
                    if ($testStatusMap[$juz] === 'tidak_lancar') {
                        $progress[$juz] = 'tested-failed'; // Red for Tidak Lancar
                    } else {
                        $c = $testCountMap[$juz] ?? 1;
                        if ($c >= 3) {
                            $progress[$juz] = 'tested-dark'; // Dark green for 3+ tests
                        } elseif ($c >= 2) {
                            $progress[$juz] = 'tested-medium'; // Medium green for 2 tests
                        } else {
                            $progress[$juz] = 'tested-light'; // Light green for 1 test
                        }
                    }
                } else {
                    // Check if student has achieved this juz based on the sequence
                    if (isset($achievedJuz[$juz])) {
                        $progress[$juz] = 'achieved'; // Grey for achieved but not tested
                    } else {
                        $progress[$juz] = 'not-achieved'; // Default (no color)
                    }
                }
            }
            
            // Determine final target juz based on class (only the last juz in the sequence)
            $finalTargetJuz = 0; // Default: no target
            if ($student['class'] == 1) {
                // Class 1: final target is juz 3
                $finalTargetJuz = 3;
            } elseif ($student['class'] == 2) {
                // Class 2: final target is juz 8
                $finalTargetJuz = 8;
            } elseif ($student['class'] == 3) {
                // Class 3: final target is juz 13
                $finalTargetJuz = 13;
            }

            $student['final_target_juz'] = $finalTargetJuz;
            $student['progress'] = $progress;
            $musyrif['students'][] = $student;
        }
    }
    
    echo json_encode([
        'success' => true,
        'data' => $musyrifs
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Terjadi kesalahan: ' . $e->getMessage()
    ]);
}

R::close();