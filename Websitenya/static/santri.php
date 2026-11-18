<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/functions-settings.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Set CORS headers
setCORSHeaders();

header('Content-Type: application/json');

// Check if request method is GET
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get NIK from query parameter
$nik = $_GET['nik'] ?? '';

// Validate NIK
if (empty($nik)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Parameter ?nik=[nik] harus diisi']);
    exit;
}

try {
    // Check if student exists
    $student = R::findOne('santri', 'nik = ?', [$nik]);
    
    if (!$student) {
        http_response_code(404);
        echo json_encode(['success' => false, 'message' => 'Santri dengan NIK tersebut tidak ditemukan']);
        exit;
    }
    
    // ==========================================
    // 1. PENCAPAIAN JUZ
    // ==========================================

    // Define the juz sequence: [30, 29, 1, 2, 3, ..., 28]
    $sequence = [30, 29];
    for ($i = 1; $i <= 28; $i++) {
        $sequence[] = $i;
    }

    // Get all distinct juz that student has achieved (from pencapaian table)
    $achievedJuzRaw = R::getCol("
        SELECT DISTINCT juz
        FROM pencapaian
        WHERE nik = ? AND juz IS NOT NULL
    ", [$nik]);

    // Find the highest position achieved in the sequence
    $maxPosition = 0;
    foreach ($achievedJuzRaw as $juz) {
        $position = array_search($juz, $sequence);
        if ($position !== false && $position + 1 > $maxPosition) {
            $maxPosition = $position + 1;
        }
    }

    // Mark all juz in the sequence up to the highest achieved position as achieved
    $achievedJuz = [];
    for ($pos = 0; $pos < $maxPosition; $pos++) {
        $achievedJuz[] = $sequence[$pos];
    }

    // Get all distinct juz that student has been tested and passed (from tes table)
    $lancarJuz = R::getCol("
        SELECT DISTINCT juz
        FROM tes
        WHERE nik = ? AND juz IS NOT NULL
    ", [$nik]);

    // Calculate juz that are achieved but not yet tested (tidak lancar)
    $tidakLancarJuz = array_values(array_diff($achievedJuz, $lancarJuz));

    $pencapaianJuz = [
        'juzYangDicapai' => array_map('intval', $achievedJuz),
        'juzYangLancar' => array_map('intval', $lancarJuz),
        'juzYangTidakLancar' => array_map('intval', $tidakLancarJuz)
    ];
    
    // ==========================================
    // 2. PENCAPAIAN TERAKHIR (Last Ziyadah)
    // ==========================================
    
    // First try to get the last achievement
    $lastAchievement = R::getRow("
        SELECT type, juz, halaman, kesalahan, created_at
        FROM pencapaian
        WHERE nik = ? AND type IS NOT NULL
        ORDER BY created_at DESC
        LIMIT 1
    ", [$nik]);
    
    $pencapaianTerakhir = null;
    
    if ($lastAchievement) {
        // If the last achievement is not ziyadah, find the last ziyadah
        if ($lastAchievement['type'] !== 'ziyadah') {
            $lastZiyadah = R::getRow("
                SELECT juz, halaman, kesalahan, created_at
                FROM pencapaian
                WHERE nik = ? AND type = 'ziyadah'
                ORDER BY created_at DESC
                LIMIT 1
            ", [$nik]);
            
            if ($lastZiyadah) {
                $pencapaianTerakhir = [
                    'tanggal' => $lastZiyadah['created_at'],
                    'juz' => intval($lastZiyadah['juz']),
                    'halaman' => $lastZiyadah['halaman'],
                    'kesalahan' => intval($lastZiyadah['kesalahan'])
                ];
            }
        } else {
            $pencapaianTerakhir = [
                'tanggal' => $lastAchievement['created_at'],
                'juz' => intval($lastAchievement['juz']),
                'halaman' => $lastAchievement['halaman'],
                'kesalahan' => intval($lastAchievement['kesalahan'])
            ];
        }
    }
    
    // ==========================================
    // 3. TARGET HAFALAN
    // ==========================================
    
    // Get class year configurations
    $kelas1Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas1_year'");
    $kelas2Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas2_year'");
    $kelas3Year = R::getCell("SELECT value FROM settings WHERE key = 'kelas3_year'");
    
    // Determine target based on class
    $targetHafalan = 0;
    $tahunMasuk = $student->tahun_masuk;
    
    if ($tahunMasuk == $kelas1Year) {
        $targetHafalan = 3;
    } elseif ($tahunMasuk == $kelas2Year) {
        $targetHafalan = 8;
    } elseif ($tahunMasuk == $kelas3Year) {
        $targetHafalan = 13;
    }
    
    // ==========================================
    // 4. JUZIYAH (Descending order)
    // ==========================================
    
    $juziyahRecords = R::getAll("
        SELECT juz, kesalahan, created_at as tanggal
        FROM pencapaian
        WHERE nik = ? AND type = 'juziyah'
        ORDER BY created_at DESC
    ", [$nik]);
    
    $juziyah = array_map(function($record) {
        return [
            'tanggal' => $record['tanggal'],
            'juz' => intval($record['juz']),
            'kesalahan' => intval($record['kesalahan'])
        ];
    }, $juziyahRecords);
    
    // ==========================================
    // 5. SYAHADAH (Descending order)
    // ==========================================
    
    $syahadahRecords = R::getAll("
        SELECT syahadah as tingkatan, kesalahan, created_at as tanggal
        FROM pencapaian
        WHERE nik = ? AND type = 'syahadah'
        ORDER BY created_at DESC
    ", [$nik]);
    
    $syahadah = array_map(function($record) {
        return [
            'tanggal' => $record['tanggal'],
            'tingkatan' => $record['tingkatan'],
            'kesalahan' => intval($record['kesalahan'])
        ];
    }, $syahadahRecords);
    
    // ==========================================
    // 6. 10 LOG TERAKHIR (Last 10 activities)
    // ==========================================
    
    $last10Logs = R::getAll("
        SELECT type, juz, halaman, posisi, syahadah, kesalahan, created_at
        FROM pencapaian
        WHERE nik = ? AND type IS NOT NULL
        ORDER BY created_at DESC
        LIMIT 10
    ", [$nik]);
    
    $logTerakhir = array_map(function($log) {
        $entry = [
            'tipe' => ucfirst(str_replace('_', ' ', $log['type'])),
            'tanggal' => $log['created_at']
        ];
        
        if (in_array($log['type'], ['ziyadah', 'juziyah'])) {
            $entry['juz'] = intval($log['juz']);
            if ($log['halaman']) {
                $entry['halaman'] = $log['halaman'];
            }
        } elseif ($log['type'] === 'syahadah') {
            $entry['tingkatan'] = $log['syahadah'];
        } elseif ($log['type'] === 'setengah_juz') {
            $entry['juz'] = intval($log['juz']);
            $entry['posisi'] = $log['posisi'];
        }
        
        $entry['kesalahan'] = intval($log['kesalahan']);
        
        return $entry;
    }, $last10Logs);
    
    // ==========================================
    // 7. KECEPATAN (Speed Analysis)
    // ==========================================

    // Calculate ziyadah speed: time between current ziyadah and previous record (any type)
    $ziyadahRecords = R::getAll("
        SELECT created_at
        FROM pencapaian
        WHERE nik = ? AND type = 'ziyadah'
        ORDER BY created_at ASC
    ", [$nik]);

    $ziyadahSpeed = 0;
    $ziyadahRecordCount = count($ziyadahRecords);

    if ($ziyadahRecordCount > 1) {
        $totalDays = 0;
        $intervals = 0;
        
        for ($i = 1; $i < $ziyadahRecordCount; $i++) {
            $currentTime = new DateTime($ziyadahRecords[$i]['created_at']);
            
            // Find the record immediately before this ziyadah (any type)
            $previousRecord = R::getRow("
                SELECT created_at
                FROM pencapaian
                WHERE nik = ? AND created_at < ?
                ORDER BY created_at DESC
                LIMIT 1
            ", [$nik, $ziyadahRecords[$i]['created_at']]);
            
            if ($previousRecord) {
                $previousTime = new DateTime($previousRecord['created_at']);
                $diff = $currentTime->diff($previousTime);
                $totalDays += $diff->days;
                $intervals++;
            }
        }
        
        $ziyadahSpeed = $intervals > 0 ? round($totalDays / $intervals) : 0;
    }

    // Calculate juziyah speed: time between current juziyah and previous record (any type)
    $juziyahAllRecords = R::getAll("
        SELECT created_at
        FROM pencapaian
        WHERE nik = ? AND type = 'juziyah'
        ORDER BY created_at ASC
    ", [$nik]);

    $juziyahSpeed = 0;
    if (count($juziyahAllRecords) > 1) {
        $totalDays = 0;
        $intervals = 0;
        
        for ($i = 1; $i < count($juziyahAllRecords); $i++) {
            $currentTime = new DateTime($juziyahAllRecords[$i]['created_at']);
            
            // Find the record immediately before this juziyah (any type)
            $previousRecord = R::getRow("
                SELECT created_at
                FROM pencapaian
                WHERE nik = ? AND created_at < ?
                ORDER BY created_at DESC
                LIMIT 1
            ", [$nik, $juziyahAllRecords[$i]['created_at']]);
            
            if ($previousRecord) {
                $previousTime = new DateTime($previousRecord['created_at']);
                $diff = $currentTime->diff($previousTime);
                $totalDays += $diff->days;
                $intervals++;
            }
        }
        
        $juziyahSpeed = $intervals > 0 ? round($totalDays / $intervals) : 0;
    }

    // Calculate syahadah speed: time between current syahadah and previous record (any type)
    $syahadahAllRecords = R::getAll("
        SELECT created_at
        FROM pencapaian
        WHERE nik = ? AND type = 'syahadah'
        ORDER BY created_at ASC
    ", [$nik]);

    $syahadahSpeed = 0;
    if (count($syahadahAllRecords) > 1) {
        $totalDays = 0;
        $intervals = 0;
        
        for ($i = 1; $i < count($syahadahAllRecords); $i++) {
            $currentTime = new DateTime($syahadahAllRecords[$i]['created_at']);
            
            // Find the record immediately before this syahadah (any type)
            $previousRecord = R::getRow("
                SELECT created_at
                FROM pencapaian
                WHERE nik = ? AND created_at < ?
                ORDER BY created_at DESC
                LIMIT 1
            ", [$nik, $syahadahAllRecords[$i]['created_at']]);
            
            if ($previousRecord) {
                $previousTime = new DateTime($previousRecord['created_at']);
                $diff = $currentTime->diff($previousTime);
                $totalDays += $diff->days;
                $intervals++;
            }
        }
        
        $syahadahSpeed = $intervals > 0 ? round($totalDays / $intervals) : 0;
    }

    $kecepatan = [
        'ziyadah' => $ziyadahSpeed,
        'juziyah' => $juziyahSpeed,
        'syahadah' => $syahadahSpeed
    ];
    
    // ==========================================
    // 8. PREDIKSI (Prediction)
    // ==========================================

    // Calculate current position in the juz sequence
    $currentPosition = $maxPosition; // Position in sequence (0-30)
    
    // Check if student has completed at least one full juz (reached 10B)
    $hasCompletedJuz = R::getCell("
        SELECT COUNT(*) FROM pencapaian 
        WHERE nik = ? AND type = 'ziyadah' AND halaman = '10B'
    ", [$nik]) > 0;
    
    // Define targets based on sequence positions:
    // 15 Juz target = position 15 in sequence (juz 1-13, 29, 30)
    // 30 Juz target = position 30 in sequence (all juz 1-30)
    $target15JuzPosition = 15;
    $target30JuzPosition = 30;

    // Predict days to reach 15 juz (position 15 in sequence) and 30 juz (position 30)
    $daysTo15Juz = null; // null means insufficient data
    $daysTo30Juz = null;

    // Only calculate prediction if we have sufficient data (at least 2 ziyadah records)
    if ($ziyadahSpeed > 0 && $ziyadahRecordCount > 1) {
        // Each juz has approximately 20 half-pages (1A-10B = 20 pages)
        $pagesPerJuz = 20;

        // Count total ziyadah records to estimate pages completed
        $totalZiyadahRecords = R::getCell("
            SELECT COUNT(*) FROM pencapaian WHERE nik = ? AND type = 'ziyadah'
        ", [$nik]);

        // Estimate: each ziyadah record is roughly one page
        $pagesCompleted = $totalZiyadahRecords;

        // Check if targets are already achieved based on sequence position
        $alreadyAchieved15 = $currentPosition >= $target15JuzPosition;
        $alreadyAchieved30 = $currentPosition >= $target30JuzPosition;

        // Calculate remaining juz to complete (not pages)
        $remainingJuzTo15 = max(0, $target15JuzPosition - $currentPosition);
        $remainingJuzTo30 = max(0, $target30JuzPosition - $currentPosition);

        // Calculate days per juz based on actual progress
        // Use ziyadah speed to estimate: pages_per_juz * days_per_page
        $daysPerJuz = $pagesPerJuz * $ziyadahSpeed;

        // Calculate active learning days (excluding Sundays and school holidays)
        // Sundays: ~52 Sundays per year, so roughly 1 Sunday per 7 days
        // School holidays: 2 months per year = ~60 days per year
        // Active learning days per year: 365 - 52 - 60 = 253 days
        // Inactive ratio: (52 + 60) / 365 = 112 / 365 ≈ 0.307 (30.7% of days are inactive)
        $sundaysPerYear = 52;
        $schoolHolidayDays = 60; // 2 months
        $totalInactiveDaysPerYear = $sundaysPerYear + $schoolHolidayDays;
        $inactiveRatio = $totalInactiveDaysPerYear / 365;
        $activeRatio = 1 - $inactiveRatio;

        // Calculate raw days needed based on remaining juz
        $rawDaysTo15Juz = 0;
        $rawDaysTo30Juz = 0;

        if (!$alreadyAchieved15 && $remainingJuzTo15 > 0) {
            $rawDaysTo15Juz = $remainingJuzTo15 * $daysPerJuz;
        }

        if (!$alreadyAchieved30 && $remainingJuzTo30 > 0) {
            $rawDaysTo30Juz = $remainingJuzTo30 * $daysPerJuz;
        }

        // Adjust for inactive days (Sundays + holidays)
        // If we need 100 active days, and active ratio is 0.693, 
        // then calendar days = 100 / 0.693 ≈ 144 days
        if ($rawDaysTo15Juz > 0) {
            $daysTo15Juz = ceil($rawDaysTo15Juz / $activeRatio);
        } else {
            $daysTo15Juz = 0; // Already achieved
        }

        if ($rawDaysTo30Juz > 0) {
            $daysTo30Juz = ceil($rawDaysTo30Juz / $activeRatio);
        } else {
            $daysTo30Juz = 0; // Already achieved
        }
    }
    // If insufficient data, both remain null

    $prediksi = [
        '15Juz' => $daysTo15Juz !== null ? intval($daysTo15Juz) : null,
        '30Juz' => $daysTo30Juz !== null ? intval($daysTo30Juz) : null,
        'catatan' => $ziyadahRecordCount < 2 ? 'Data belum cukup untuk prediksi. Minimal 2 record ziyadah diperlukan.' : null,
        'asumsi' => $ziyadahRecordCount >= 2 ? 'Perhitungan sudah memperhitungkan hari Ahad dan libur sekolah (2 bulan/tahun)' : null
    ];
    
    // ==========================================
    // 9. DATA TAMBAHAN (Additional Insights)
    // ==========================================
    
    // Total achievements count
    $totalAchievements = R::getCell("
        SELECT COUNT(*) FROM pencapaian WHERE nik = ? AND type IS NOT NULL
    ", [$nik]);
    
    // Total tests count
    $totalTests = R::getCell("
        SELECT COUNT(*) FROM tes WHERE nik = ?
    ", [$nik]);
    
    // Average error rate
    $avgErrors = R::getCell("
        SELECT AVG(kesalahan) FROM pencapaian WHERE nik = ? AND type IS NOT NULL
    ", [$nik]);
    
    // First and last activity dates
    $firstActivity = R::getCell("
        SELECT MIN(created_at) FROM pencapaian WHERE nik = ? AND type IS NOT NULL
    ", [$nik]);
    
    $lastActivity = R::getCell("
        SELECT MAX(created_at) FROM pencapaian WHERE nik = ? AND type IS NOT NULL
    ", [$nik]);
    
    // Days since first activity (learning duration)
    $learningDays = 0;
    if ($firstActivity) {
        $date1 = new DateTime($firstActivity);
        $date2 = new DateTime();
        $learningDays = $date1->diff($date2)->days;
    }
    
    // Musyrif information
    $musyrifInfo = R::getAll("
        SELECT m.nama
        FROM musyrif m
        JOIN musyrfst ms ON m.id = ms.musyrif_id
        WHERE ms.santri_nik = ?
    ", [$nik]);
    
    $musyrifList = array_column($musyrifInfo, 'nama');
    
    // Attendance data (if exists in laporansabtu)
    $saturdayReports = R::getAll("
        SELECT murajaahentries, hafalanentries, created_at
        FROM laporansabtu
        WHERE nik = ?
        ORDER BY created_at DESC
        LIMIT 5
    ", [$nik]);
    
    $dataTambahan = [
        'totalPencapaian' => intval($totalAchievements),
        'totalTes' => intval($totalTests),
        'rataRataKesalahan' => $avgErrors ? round(floatval($avgErrors), 2) : 0,
        'aktivitasPertama' => $firstActivity,
        'aktivitasTerakhir' => $lastActivity,
        'hariBelajar' => intval($learningDays),
        'musyrif' => $musyrifList,
        'laporanSabtu' => count($saturdayReports)
    ];

    // ==========================================
    // 10. REKOMENDASI UNTUK WALI SANTRI
    // ==========================================

    // Generate a unique recommendation based on student's specific data
    // Create a hash from all key data points to ensure uniqueness
    $jenisKelamin = strtolower($student->jenis_kelamin ?? '');
    $dataSignature = md5(
        $nik . 
        count($achievedJuz) . 
        count($lancarJuz) . 
        $ziyadahSpeed . 
        $juziyahSpeed . 
        $syahadahSpeed . 
        ($daysTo15Juz ?? 'null') . 
        ($daysTo30Juz ?? 'null') .
        $totalAchievements .
        $totalTests .
        ($avgErrors ?? 0) .
        $currentPosition .
        ($targetHafalan ?? 0) .
        count($juziyah) .
        count($syahadah) .
        $learningDays .
        $jenisKelamin
    );
    
    // Convert hash to number for seeding
    $seed = hexdec(substr($dataSignature, 0, 8));
    mt_srand($seed);
    
    // Comprehensive recommendation pool (50+ recommendations)
    $rekomendasiPool = [
        // FAST PROGRESS (ziyadah speed 1-2 days)
        [
            'condition' => $ziyadahSpeed >= 1 && $ziyadahSpeed <= 2 && count($achievedJuz) >= 10,
            'rekomendasi' => "Alhamdulillah, hafalan {$student->nama_panggilan} sangat cepat! Saat kunjungan bulan depan, bawakan kurma ajwa atau madu murni untuk menjaga stamina. Pastikan dia tidur cukup 8-9 jam. Saat telepon, ingatkan untuk konsisten murajaah."
        ],
        [
            'condition' => $ziyadahSpeed >= 1 && $ziyadahSpeed <= 2 && count($achievedJuz) < 10,
            'rekomendasi' => "Masya Allah, {$student->nama_panggilan} punya kecepatan hafalan yang bagus! Saat telepon, berikan semangat agar tetap istiqomah. Bawakan Al-Quran terjemahan saat kunjungan untuk membantu pemahaman."
        ],
        
        // MODERATE PROGRESS (ziyadah speed 3-5 days)
        [
            'condition' => $ziyadahSpeed >= 3 && $ziyadahSpeed <= 5 && count($lancarJuz) < count($achievedJuz) / 2,
            'rekomendasi' => "{$student->nama_panggilan} sedang dalam proses yang baik. Saat kunjungan, fokus tanyakan tentang murajaah juz yang belum lancar (juz " . implode(', ', array_slice($tidakLancarJuz, 0, 3)) . "). Ingatkan untuk mengulang hafalan setiap ba'da sholat."
        ],
        [
            'condition' => $ziyadahSpeed >= 3 && $ziyadahSpeed <= 5 && count($lancarJuz) >= count($achievedJuz) / 2,
            'rekomendasi' => "Alhamdulillah, {$student->nama_panggilan} memiliki keseimbangan antara setoran dan murajaah. Saat telepon, pujilah perkembangannya dan berikan hadiah kecil saat ada pencapaian baru. Tanyakan juga tentang kondisi teman-teman di pesantren."
        ],
        
        // SLOW PROGRESS (ziyadah speed 6+ days)
        [
            'condition' => $ziyadahSpeed >= 6 && $learningDays > 60,
            'rekomendasi' => "{$student->nama_panggilan} butuh dukungan lebih. Saat kunjungan Selasa malam, bicarakan langsung dengan musyrif tentang metode pembelajaran yang tepat. Bawakan buku catatan hafalan dan minta dia mencatat progress setiap hari."
        ],
        [
            'condition' => $ziyadahSpeed >= 6 && $learningDays <= 60,
            'rekomendasi' => "{$student->nama_panggilan} masih dalam masa penyesuaian di pesantren. Bersabarlah. Saat telepon, jangan terlalu banyak tanya hafalan dulu, tanyakan dulu tentang kenyamanan, teman, dan ustadz. Bawakan makanan favorit saat kunjungan."
        ],
        
        // HIGH ERROR RATE
        [
            'condition' => ($avgErrors ?? 0) > 5 && count($achievedJuz) > 5,
            'rekomendasi' => "Kesalahan {$student->nama_panggilan} cukup tinggi (rata-rata " . number_format($avgErrors ?? 0, 1) . "). Saat kunjungan, belikan buku tajwid praktis dan minta dia praktekkan bacaannya di depan Anda. Ingatkan untuk tadarus dengan teman yang bacaannya bagus."
        ],
        [
            'condition' => ($avgErrors ?? 0) > 3 && ($avgErrors ?? 0) <= 5,
            'rekomendasi' => "Perhatikan tajwid {$student->nama_panggilan}. Saat kunjungan Selasa malam, belikan buku tajwid berwarna yang mudah dipahami. Tanyakan tentang kesulitan membaca Al-Quran dan dengarkan keluhannya."
        ],
        
        // LOW ERROR RATE
        [
            'condition' => ($avgErrors ?? 0) <= 2 && count($achievedJuz) > 10,
            'rekomendasi' => "Masya Allah, bacaan {$student->nama_panggilan} sangat baik! Saat kunjungan, berikan hadiah spesial seperti Al-Quran premium atau sajadah bagus. Targetkan untuk setoran lebih banyak dan minta dia mengajari adik kelas."
        ],
        
        // JUZIYAH PROGRESS
        [
            'condition' => count($juziyah) >= 3 && $juziyahSpeed > 0 && $juziyahSpeed <= 30,
            'rekomendasi' => "{$student->nama_panggilan} rutin mengikuti ujian juziyah. Sebelum ujian berikutnya, bawakan vitamin dan makanan bergizi. Saat telepon, tanyakan 'Ujian juziyah kapan? Sudah siap belum?' dan berikan semangat."
        ],
        [
            'condition' => count($juziyah) >= 3 && $juziyahSpeed > 30,
            'rekomendasi' => "Jarak antara ujian juziyah {$student->nama_panggilan} cukup lama. Saat kunjungan, dorong dia untuk lebih sering ikut ujian. Belikan buku catatan progress hafalan agar dia bisa melihat perkembangan sendiri."
        ],
        [
            'condition' => count($juziyah) < 2 && $hasCompletedJuz,
            'rekomendasi' => "{$student->nama_panggilan} sudah punya dasar hafalan yang bagus. Saat kunjungan Selasa malam, sarankan untuk ikut ujian juziyah. Tanyakan ke musyrif: 'Apakah {$student->nama_panggilan} sudah siap ujian?'"
        ],
        
        // SYAHADAH PROGRESS
        [
            'condition' => count($syahadah) >= 2,
            'rekomendasi' => "Alhamdulillah, {$student->nama_panggilan} sudah mengikuti syahadah beberapa kali. Ini tanda keseriusan! Saat kunjungan, berikan hadiah istimewa dan tekankan pentingnya menjaga hafalan dengan murajaah setiap hari."
        ],
        [
            'condition' => count($syahadah) == 1,
            'rekomendasi' => "{$student->nama_panggilan} sudah pernah syahadah. Saat telepon, tanyakan 'Bagaimana pengalaman syahadah dulu? Apa yang perlu diperbaiki untuk syahadah berikutnya?' Belikan buku motivasi islami."
        ],
        
        // PREDICTION-BASED
        [
            'condition' => ($daysTo15Juz ?? 0) > 0 && ($daysTo15Juz ?? 9999) < 365,
            'rekomendasi' => "Dengan kecepatan saat ini, {$student->nama_panggilan} diprediksi bisa menyelesaikan 15 juz dalam waktu kurang dari 1 tahun. Ini luar biasa! Saat kunjungan, bicarakan target wisuda 15 juz dan rayakan setiap pencapaiannya."
        ],
        [
            'condition' => ($daysTo30Juz ?? 0) > 0 && ($daysTo30Juz ?? 9999) < 730,
            'rekomendasi' => "Insya Allah, {$student->nama_panggilan} bisa menyelesaikan 30 juz dalam 2 tahun ke depan. Saat kunjungan Selasa malam, buat target bersama dan berikan reward system untuk setiap juz yang diselesaikan."
        ],
        [
            'condition' => ($daysTo30Juz ?? 0) > 1000,
            'rekomendasi' => "Untuk mencapai 30 juz, {$student->nama_panggilan} butuh waktu yang cukup panjang. Saat telepon, jangan putus asa, tetap ingatkan istiqomah. Bantu dengan membuat target-target kecil (per 5 juz) dan rayakan setiap milestone."
        ],
        
        // ACHIEVEMENT MILESTONES
        [
            'condition' => count($achievedJuz) >= 15 && count($achievedJuz) < 20,
            'rekomendasi' => "Masya Allah, {$student->nama_panggilan} sudah mencapai lebih dari 15 juz! Hampir setengah Al-Quran. Saat kunjungan bulan depan, berikan hadiah istimewa dan buat perayaan kecil bersama teman-temannya."
        ],
        [
            'condition' => count($achievedJuz) >= 20 && count($achievedJuz) < 25,
            'rekomendasi' => "{$student->nama_panggilan} sudah di atas 20 juz! Tinggal sedikit lagi menuju 30 juz. Saat kunjungan Selasa malam, perkuat motivasi dengan sering mengingatkan keutamaan menghafal Al-Quran."
        ],
        [
            'condition' => count($achievedJuz) >= 25,
            'rekomendasi' => "Alhamdulillah, {$student->nama_panggilan} sudah sangat dekat dengan 30 juz! Saat kunjungan, fokuskan pada persiapan ujian akhir. Tanyakan: 'Juz berapa yang masih perlu dimurajaah?' dan doakan."
        ],
        
        // TESTING STATUS
        [
            'condition' => count($tidakLancarJuz) > 10 && count($achievedJuz) > 10,
            'rekomendasi' => "{$student->nama_panggilan} punya banyak juz yang belum dites (juz " . implode(', ', array_slice($tidakLancarJuz, 0, 5)) . "). Saat kunjungan, minta musyrif untuk mengatur jadwal tes. Di rumah saat liburan, bantu dengan menguji hafalan sederhana."
        ],
        [
            'condition' => count($lancarJuz) > count($achievedJuz) * 0.7 && count($achievedJuz) > 5,
            'rekomendasi' => "Alhamdulillah, sebagian besar hafalan {$student->nama_panggilan} sudah lancar! Saat telepon, berikan reward untuk menjaga semangat. Tanyakan tentang rencana setoran berikutnya."
        ],
        
        // LEARNING DURATION
        [
            'condition' => $learningDays < 30,
            'rekomendasi' => "{$student->nama_panggilan} masih baru di pesantren. Saat kunjungan pertama, jangan terlalu banyak tanya hafalan. Tanyakan tentang kenyamanan, teman sekamar, makanan, dan ustadz. Bawakan barang yang dia butuhkan."
        ],
        [
            'condition' => $learningDays >= 30 && $learningDays < 180,
            'rekomendasi' => "{$student->nama_panggilan} sudah cukup nyaman di pesantren. Mulai tanyakan target hafalan saat telepon. Saat kunjungan, bawakan makanan favorit atau buku-buku islami yang dia sukai."
        ],
        [
            'condition' => $learningDays >= 180 && $learningDays < 365,
            'rekomendasi' => "{$student->nama_panggilan} sudah menjalani pesantren selama " . round($learningDays / 30) . " bulan. Saat kunjungan Selasa malam, evaluasi progress bersama musyrif. Buat target bersama untuk 6 bulan ke depan."
        ],
        [
            'condition' => $learningDays >= 365,
            'rekomendasi' => "Alhamdulillah, {$student->nama_panggilan} sudah menjalani pesantren lebih dari 1 tahun. Saat kunjungan, lihat pencapaian dan buat evaluasi menyeluruh. Berikan apresiasi atas perjalanan yang sudah dilalui."
        ],
        
        // CLASS/TARGET BASED
        [
            'condition' => $targetHafalan == 3 && count($achievedJuz) < 3,
            'rekomendasi' => "{$student->nama_panggilan} di kelas pertama dengan target juz 3. Saat kunjungan, bawakan Al-Quran yang nyaman dibaca dan buku catatan hafalan. Tanyakan progress setiap kunjungan."
        ],
        [
            'condition' => $targetHafalan == 3 && count($achievedJuz) >= 3,
            'rekomendasi' => "Alhamdulillah, {$student->nama_panggilan} sudah mencapai target kelas pertama! Saat kunjungan, persiapkan untuk kenaikan kelas dengan meningkatkan intensitas murajaah. Berikan hadiah pencapaian."
        ],
        [
            'condition' => $targetHafalan == 8 && count($achievedJuz) < 8,
            'rekomendasi' => "{$student->nama_panggilan} sedang menuju target 8 juz. Saat telepon, tanyakan 'Sudah sampai juz berapa?' dan ingatkan untuk rajin murajaah. Bawakan buku-buku pendukung saat kunjungan."
        ],
        [
            'condition' => $targetHafalan == 13 && count($achievedJuz) < 13,
            'rekomendasi' => "{$student->nama_panggilan} di kelas lanjutan dengan target 13 juz. Ini target yang menantang. Saat kunjungan Selasa malam, pastikan kebutuhan belajar terpenuhi dan berikan support ekstra."
        ],
        
        // GENERAL SUPPORT RECOMMENDATIONS (PHONE CALLS)
        [
            'condition' => true,
            'rekomendasi' => "Saat menelepon {$student->nama_panggilan}, awali dengan menanyakan kabar, kesehatan, dan kebahagiaan. Baru depois tanyakan tentang hafalan. Pastikan dia makan teratur, tidur cukup, dan tidak stres. Anak yang bahagia lebih mudah menghafal."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat telepon {$student->nama_panggilan}, hindari pertanyaan yang membuat stres seperti 'Kenapa hafalan lambat?' atau 'Kok belum naik juz?' Ganti dengan 'Ada yang bisa Ayah/Bunda bantu?' atau 'Semangat ya, Nak!'"
        ],
        [
            'condition' => true,
            'rekomendasi' => "Telepon {$student->nama_panggilan} secara rutin, minimal seminggu sekali. Tanyakan tentang teman sekamar, kegiatan harian, dan makanan di pesantren. Ini menunjukkan Anda peduli pada kebahagiaannya, bukan hanya hafalan."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat menelepon {$student->nama_panggilan}, dengarkan keluhannya tanpa menghakimi. Kalau dia cerita tentang kesulitan, berikan semangat bukan kritik. Biarkan dia merasa nyaman bercerita pada Anda."
        ],
        
        // GENERAL SUPPORT RECOMMENDATIONS (VISITS)
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan bulanan, bawakan makanan bergizi seperti kurma, madu, susu, atau kacang. Hindari makanan cepat saji.{$student->nama_panggilan} butuh gizi baik untuk konsentrasi hafalan di pesantren."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan Selasa malam, luangkan waktu untuk sholat bersama {$student->nama_panggilan} di masjid pesantren. Ini menunjukkan dukungan spiritual dan memperkuat ikatan. Afterwards, tanya tentang hafalan dengan santai."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan, bawakan {$student->nama_panggilan} perlengkapan belajar yang nyaman: pena bagus, buku catatan baru, atau Al-Quran terjemahan. Hal kecil seperti ini bisa meningkatkan semangat belajar di pesantren."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan ke pesantren, sisihkan waktu untuk bicara dengan musyrif {$student->nama_panggilan}. Tanyakan: 'Bagaimana perkembangan {$student->nama_panggilan}? Apa yang perlu saya bantu dari rumah?'"
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan, ajak {$student->nama_panggilan} jalan-jalan santai di sekitar pesantren. Bicara tentang mimpi dan cita-citanya. Mendengarkan ceritanya akan membuatnya merasa didukung dan semakin termotivasi."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan bulan depan, buat sistem reward untuk {$student->nama_panggilan}. Misalnya, setiap mencapai juz baru, berikan hadiah. Ini akan memotivasi dia untuk terus bersemangat menghafal di pesantren."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan Selasa malam, pastikan {$student->nama_panggilan} punya waktu istirahat yang cukup. Jangan terlalu memaksakan target jika kondisi fisik atau mental sedang tidak baik. Kesehatan lebih penting."
        ],
        
        // EMOTIONAL SUPPORT
        [
            'condition' => true,
            'rekomendasi' => "Perhatikan aspek emosional {$student->nama_panggilan}. Saat kunjungan atau telepon, tanyakan tentang perasaan, persahabatan, dan kebahagiaan di pesantren. Anak yang bahagia akan lebih mudah menghafal."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat {$student->nama_panggilan} sedang down atau lelah, jangan langsung tanya hafalan. Beri kata-kata motivasi: 'Ayah/Bunda bangga sama kamu. Istirahat dulu kalau capek, besok semangat lagi ya!'"
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan, peluk {$student->nama_panggilan} dan katakan 'Ayah/Bunda sayang kamu, bangga sama perjuangan kamu menghafal Al-Quran.' Ini akan membuatnya sangat termotivasi."
        ],
        
        // PRACTICAL SUPPORT
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan, bawakan {$student->nama_panggilan} audio murottal dari qari terkenal (seperti Abdul Basit, Al-Hussary, atau Mishary Rashid). Ini membantu pemahaman dan kualitas hafalan saat murojaah mandiri."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Saat kunjungan Selasa malam, belikan {$student->nama_panggilan} buku 'Rahasia Menghafal Al-Quran' atau buku motivasi islami. Ini bisa dibaca saat waktu luang di pesantren."
        ],
        [
            'condition' => true,
            'rekomendasi' => "Setiap kunjungan, tanyakan pada {$student->nama_panggilan}: 'Apa yang kamu butuhkan untuk membantu hafalan? Buku? Pena? Al-Quran baru?' Lalu penuhi kebutuhannya. Ini menunjukkan support nyata."
        ],
        
        // GENDER-SPECIFIC: MALE (Laki-laki)
        [
            'condition' => $jenisKelamin === 'laki-laki',
            'rekomendasi' => "Saat kunjungan, bawakan {$student->nama_panggilan} olahraga ringan seperti bola atau resistance band. Anak laki-laki butuh aktivitas fisik untuk menjaga stamina hafalan. Ingatkan untuk tidak terlalu banyak main game."
        ],
        [
            'condition' => $jenisKelamin === 'laki-laki',
            'rekomendasi' => "Saat menelepon {$student->nama_panggilan}, tanyakan tentang kegiatan olahraga di pesantren. Anak laki-laki yang aktif secara fisik biasanya lebih mudah fokus menghafal."
        ],
        [
            'condition' => $jenisKelamin === 'laki-laki',
            'rekomendasi' => "{$student->nama_panggilan} sebagai anak laki-laki, butuh role model pria yang sholeh. Saat kunjungan, ceritakan tentang sahabat Nabi atau ulama besar yang menghafal Al-Quran di usia muda."
        ],
        [
            'condition' => $jenisKelamin === 'laki-laki',
            'rekomendasi' => "Saat kunjungan, belikan {$student->nama_panggilan} pakaian koko atau sarung bagus. Anak laki-laki senang dengan hadiah praktis yang bisa dipakai sehari-hari di pesantren."
        ],
        [
            'condition' => $jenisKelamin === 'laki-laki',
            'rekomendasi' => "Saat menelepon {$student->nama_panggilan}, hindari bertanya terlalu detail tentang perasaan. Anak laki-laki lebih nyaman dengan pertanyaan langsung seperti 'Hafalan sudah berapa?' atau 'Butuh apa nggak?'"
        ],
        [
            'condition' => $jenisKelamin === 'laki-laki' && $ziyadahSpeed <= 2,
            'rekomendasi' => "Masya Allah, {$student->nama_panggilan} hafalannya sangat cepat! Sebagai anak laki-laki, dia punya potensi jadi hafidz yang hebat. Dorong dia untuk nanti bisa mengajari adik-adik di pesantren."
        ],
        [
            'condition' => $jenisKelamin === 'laki-laki' && count($achievedJuz) >= 15,
            'rekomendasi' => "{$student->nama_panggilan} sudah mencapai 15+ juz. Sebagai anak laki-laki, ini modal besar untuk jadi imam dan pemimpin masa depan. Saat kunjungan, tekankan tanggung jawabnya untuk menjaga dan mengamalkan Al-Quran."
        ],
        
        // GENDER-SPECIFIC: FEMALE (Perempuan)
        [
            'condition' => $jenisKelamin === 'perempuan',
            'rekomendasi' => "Saat kunjungan, bawakan {$student->nama_panggilan} skincare halal atau mukena cantik. Anak perempuan senang dengan hadiah yang membuat dia merasa diperhatikan dan cantik."
        ],
        [
            'condition' => $jenisKelamin === 'perempuan',
            'rekomendasi' => "Saat menelepon {$student->nama_panggilan}, tanyakan tentang teman-temannya dan suasana hati. Anak perempuan butuh didengarkan perasaannya, bukan hanya ditanya hafalan."
        ],
        [
            'condition' => $jenisKelamin === 'perempuan',
            'rekomendasi' => "{$student->nama_panggilan} sebagai anak perempuan, butuh role model wanita sholehah. Saat kunjungan, ceritakan tentang istri-istri Nabi atau wanita ulama yang menghafal Al-Quran."
        ],
        [
            'condition' => $jenisKelamin === 'perempuan',
            'rekomendasi' => "Saat kunjungan, belikan {$student->nama_panggilan} jilbab atau baju muslim yang dia suka. Anak perempuan senang dengan hadiah fashion yang bisa dipakai di pesantren."
        ],
        [
            'condition' => $jenisKelamin === 'perempuan',
            'rekomendasi' => "Saat menelepon {$student->nama_panggilan}, lebih peka terhadap perubahan suaranya. Jika terdengar sedih atau lelah, berikan kata-kata lembut. Anak perempuan lebih sensitif secara emosional."
        ],
        [
            'condition' => $jenisKelamin === 'perempuan' && $ziyadahSpeed <= 2,
            'rekomendasi' => "Masya Allah, {$student->nama_panggilan} hafalannya sangat cepat! Sebagai anak perempuan, ini bekal luar biasa untuk jadi ibu yang mendidik generasi penghafal Al-Quran masa depan."
        ],
        [
            'condition' => $jenisKelamin === 'perempuan' && count($achievedJuz) >= 15,
            'rekomendasi' => "{$student->nama_panggilan} sudah mencapai 15+ juz. Sebagai anak perempuan, ini modal besar untuk jadi ibu yang mendidik anak-anak penghafal Al-Quran. Saat kunjungan, tekankan keutamaan wanita penghafal Al-Quran."
        ],
    ];
    
    // Filter recommendations based on conditions
    $matchingRekomendasi = [];
    foreach ($rekomendasiPool as $rek) {
        if ($rek['condition']) {
            $matchingRekomendasi[] = $rek['rekomendasi'];
        }
    }
    
    // Select one recommendation based on hash
    $selectedRekomendasi = null;
    if (!empty($matchingRekomendasi)) {
        $selectedIndex = mt_rand(0, count($matchingRekomendasi) - 1);
        $selectedRekomendasi = $matchingRekomendasi[$selectedIndex];
    }
    
    $rekomendasi = $selectedRekomendasi;

    // ==========================================
    // FINAL RESPONSE
    // ==========================================

    $response = [
        'success' => true,
        'santri' => [
            'nik' => $student->nik,
            'nama' => $student->nama_sesuai_kk,
            'namaPanggilan' => $student->nama_panggilan,
            'jenisKelamin' => $student->jenis_kelamin ?? null,
            'status' => $student->status,
            'pencapaianJuz' => $pencapaianJuz,
            'pencapaianTerakhir' => $pencapaianTerakhir,
            'targetHafalan' => $targetHafalan,
            'juziyah' => $juziyah,
            'syahadah' => $syahadah,
            '10LogTerakhir' => $logTerakhir,
            'kecepatan' => $kecepatan,
            'prediksi' => $prediksi,
            'dataTambahan' => $dataTambahan,
            'rekomendasi' => $rekomendasi
        ]
    ];
    
    echo json_encode($response);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Terjadi kesalahan: ' . $e->getMessage()
    ]);
}
?>
