<?php
require_once __DIR__ . '/static/library/rb-sqlite.php';
require_once __DIR__ . '/static/functions.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/static/everynight-in-my-dream.db');

echo "Detailed Analysis of Students:\n";
echo "=============================\n";

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
$kelas1Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas1_year'");
$kelas2Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas2_year'");
$kelas3Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas3_year'");

$classConfiguration = [
    'kelas1' => $kelas1Year,
    'kelas2' => $kelas2Year,
    'kelas3' => $kelas3Year
];

echo "Class Configuration:\n";
var_dump($classConfiguration);
echo "\n";

$currentWeekStart = new DateTime('monday this week');
$currentWeekEnd = new DateTime('sunday this week');
echo "Current week: " . $currentWeekStart->format('Y-m-d') . " to " . $currentWeekEnd->format('Y-m-d') . "\n\n";

foreach ($studentsWithDetails as $student) {
    echo "Student: {$student['nama']} (ID: {$student['santri_id']}) - Tahun Masuk: {$student['tahun_masuk']}\n";
    echo "  Musyrif: " . ($student['musyrif_nama'] ?: 'None') . "\n";
    
    if (empty($student['last_achievement_type'])) {
        echo "  No achievements recorded\n\n";
        continue;
    }
    
    echo "  Last Achievement: {$student['last_achievement_type']} - ";
    if ($student['last_achievement_type'] === 'ziyadah') {
        echo "Halaman: {$student['last_achievement_halaman']}";
    } elseif ($student['last_achievement_type'] === 'juziyah') {
        echo "Juz: {$student['last_achievement_juz']}";
    } else {
        echo (isset($student['last_achievement_posisi']) ? $student['last_achievement_posisi'] : '') . ' ' . (isset($student['last_achievement_syahadah']) ? $student['last_achievement_syahadah'] : '');
    }
    echo " at {$student['last_achievement_created_at']}\n";
    
    // Determine student's class based on tahun_masuk and class configuration
    $studentClass = 0; // Default to 0 if not determined
    if (!empty($classConfiguration)) {
        if ($student['tahun_masuk'] == (isset($classConfiguration['kelas1']) ? $classConfiguration['kelas1'] : '')) {
            $studentClass = 1;
            echo "  Determined Class: 1\n";
        } elseif ($student['tahun_masuk'] == (isset($classConfiguration['kelas2']) ? $classConfiguration['kelas2'] : '')) {
            $studentClass = 2;
            echo "  Determined Class: 2\n";
        } elseif ($student['tahun_masuk'] == (isset($classConfiguration['kelas3']) ? $classConfiguration['kelas3'] : '')) {
            $studentClass = 3;
            echo "  Determined Class: 3\n";
        } else {
            echo "  Determined Class: None (no match)\n";
        }
    } else {
        echo "  Determined Class: None (no config)\n";
    }
    
    // Get all ziyadah achievements for the current week for this student
    $ziyadahAchievements = R::getAll("
        SELECT halaman, created_at
        FROM pencapaian 
        WHERE santri_id = ? 
          AND type = 'ziyadah' 
          AND DATE(created_at) BETWEEN ? AND ?
        ORDER BY created_at ASC
    ", [
        $student['santri_id'],
        $currentWeekStart->format('Y-m-d'),
        $currentWeekEnd->format('Y-m-d')
    ]);

    echo "  Ziyadah Achievements This Week:\n";
    foreach ($ziyadahAchievements as $achievement) {
        echo "    - {$achievement['halaman']} at {$achievement['created_at']}\n";
    }
    
    // Calculate the total number of pages covered by considering the sequence of hafalan pages
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
        $sequence = [];
        for ($i = 1; $i <= 10; $i++) {
            $sequence[] = $i . 'A';
            $sequence[] = $i . 'B';
        }

        // Filter the sequence to only include pages that are in the input array
        $filteredSequence = array_filter($sequence, function($page) use ($uniquePages) {
            return in_array($page, $uniquePages);
        });

        $sortedPages = array_values($filteredSequence);
        $ziyadahPagesCovered = count($sortedPages);
        
        echo "  Unique Ziyadah Pages This Week: [" . implode(', ', $sortedPages) . "] (Total: $ziyadahPagesCovered)\n";
    } else {
        echo "  No ziyadah achievements this week\n";
    }
    
    // Check if student meets ziyadah requirements based on class
    $ziyadahRequirementMet = false;
    if ($studentClass == 1 || $studentClass == 2) {
        // Classes 1 and 2 need at least 3 pages of ziyadah per week
        if ($ziyadahPagesCovered >= 3) {
            $ziyadahRequirementMet = true;
        }
        echo "  Requirement: At least 3 pages (Class 1/2) - Met: " . ($ziyadahRequirementMet ? 'YES' : 'NO') . "\n";
    } elseif ($studentClass == 3) {
        // Class 3 needs at least 6 pages of ziyadah per week
        if ($ziyadahPagesCovered >= 6) {
            $ziyadahRequirementMet = true;
        }
        echo "  Requirement: At least 6 pages (Class 3) - Met: " . ($ziyadahRequirementMet ? 'YES' : 'NO') . "\n";
    } else {
        echo "  Requirement: Cannot determine (unknown class)\n";
    }
    
    // Check if last achievement was ziyadah at 10B or juziyah at special juz
    $lastAchievementWasSpecial = false;
    if ($student['last_achievement_type'] === 'ziyadah' && $student['last_achievement_halaman'] === '10B') {
        $lastAchievementWasSpecial = true;
        echo "  Last achievement was special (ziyadah at 10B)\n";
    } elseif ($student['last_achievement_type'] === 'juziyah') {
        $specialJuz = [3, 8, 13, 18, 23, 28];
        if (in_array($student['last_achievement_juz'], $specialJuz)) {
            $lastAchievementWasSpecial = true;
            echo "  Last achievement was special (juziyah at juz {$student['last_achievement_juz']})\n";
        } else {
            echo "  Last achievement was not special (juziyah at juz {$student['last_achievement_juz']})\n";
        }
    } else {
        echo "  Last achievement was not special\n";
    }
    
    $needsAttention = false;
    if (!$ziyadahRequirementMet || $lastAchievementWasSpecial) {
        $needsAttention = true;
        echo "  -> NEEDS ATTENTION\n";
    } else {
        echo "  -> Does not need attention\n";
    }
    
    echo "\n";
}

echo "Analysis completed.\n";
?>