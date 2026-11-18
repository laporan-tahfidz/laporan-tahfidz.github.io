<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Set CORS headers (for browser requests)
setCORSHeaders();

header('Content-Type: application/json');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Support both GET and POST methods
$isGetMethod = $_SERVER['REQUEST_METHOD'] === 'GET';
$isPostMethod = $_SERVER['REQUEST_METHOD'] === 'POST';

if (!$isGetMethod && !$isPostMethod) {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get parameters (from GET or POST)
$action = '';
$token = '';

if ($isGetMethod) {
    $action = $_GET['action'] ?? '';
} else { // POST method
    $input = json_decode(file_get_contents('php://input'), true);
    $action = $input['action'] ?? '';
    $token = $input['token'] ?? '';

    // Verify the token for POST requests that require authentication
    if (in_array($action, ['get_selected_group', 'set_selected_group']) && $token && !verifyToken($token)) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'Unauthorized']);
        exit;
    }
}

// For cron job (GET request without action), default to sending attention message
if ($isGetMethod && empty($action)) {
    $action = 'send_attention_message';
}

try {
    if ($action === 'get_selected_group') {
        // Get the selected group ID from settings
        $selectedGroupId = R::getCell("SELECT value FROM settings WHERE key = 'whatsapp_group_id'");

        echo json_encode([
            'success' => true,
            'selected_group_id' => $selectedGroupId
        ]);
    } elseif ($action === 'set_selected_group') {
        // Set the selected group ID in settings
        $groupId = $input['group_id'] ?? '';

        if (empty($groupId)) {
            throw new Exception('Group ID is required');
        }

        // Check if the setting already exists
        $existingSetting = R::findOne('settings', ' key = ? ', ['whatsapp_group_id']);

        if ($existingSetting) {
            $existingSetting->value = $groupId;
            R::store($existingSetting);
        } else {
            $newSetting = R::dispense('settings');
            $newSetting->key = 'whatsapp_group_id';
            $newSetting->value = $groupId;
            R::store($newSetting);
        }

        echo json_encode([
            'success' => true,
            'message' => 'Selected group ID saved successfully'
        ]);
    } elseif ($action === 'send_attention_message') {
        // For cron job (GET request), no token verification needed
        // For POST request with action 'send_attention_message', verify token if provided
        if ($isPostMethod && $token && !verifyToken($token)) {
            http_response_code(401);
            echo json_encode(['success' => false, 'message' => 'Unauthorized']);
            exit;
        }

        // Get the selected group ID
        $selectedGroupId = R::getCell("SELECT value FROM settings WHERE key = 'whatsapp_group_id'");

        if (empty($selectedGroupId)) {
            throw new Exception('No WhatsApp group selected');
        }

        // Get all students with their latest achievement and musyrif assignment
        $studentsWithDetails = R::getAll("
            SELECT
                s.id as santri_id,
                s.nama_sesuai_kk as nama,
                s.nik,
                s.jenis_kelamin,
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

        // Determine 2-day evaluation period
        $todayDate = new DateTime('now', new DateTimeZone('Asia/Makassar'));
        $todayDateOnly = new DateTime($todayDate->format('Y-m-d'), new DateTimeZone('Asia/Makassar'));
        $todayDateStr = $todayDateOnly->format('Y-m-d');
        $dayOfWeek = (int)$todayDateOnly->format('N'); // 1 (Mon) to 7 (Sun)

        if ($dayOfWeek === 2) { // Selasa: evaluasi Senin & Selasa
            $startDateStr = (clone $todayDateOnly)->modify('-1 day')->format('Y-m-d');
            $endDateStr = $todayDateStr;
        } elseif ($dayOfWeek === 4) { // Kamis: evaluasi Rabu & Kamis
            $startDateStr = (clone $todayDateOnly)->modify('-1 day')->format('Y-m-d');
            $endDateStr = $todayDateStr;
        } elseif ($dayOfWeek === 6) { // Sabtu: evaluasi Jumat & Sabtu
            $startDateStr = (clone $todayDateOnly)->modify('-1 day')->format('Y-m-d');
            $endDateStr = $todayDateStr;
        } elseif ($dayOfWeek === 7) { // Minggu: evaluasi Jumat & Sabtu terakhir
            $startDateStr = (clone $todayDateOnly)->modify('-2 days')->format('Y-m-d');
            $endDateStr = (clone $todayDateOnly)->modify('-1 day')->format('Y-m-d');
        } else { // Senin (1), Rabu (3), Jumat (5)
            $startDateStr = $todayDateStr;
            $endDateStr = $todayDateStr;
        }

        // Process students to determine which ones need attention based on criteria
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
            $lastAchievementDateOnly = new DateTime($lastAchievementDate->format('Y-m-d'), new DateTimeZone('Asia/Makassar'));
            $daysSinceLastAchievement = (int)$lastAchievementDateOnly->diff($todayDateOnly)->format('%r%a');
            if ($daysSinceLastAchievement < 0) {
                $daysSinceLastAchievement = 0;
            }

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

            $needsCoordinatorAttention = false;
            $needsMusyrifAttention = false;
            $keterangan = '';
            $kurang = null;

            // Kategori Persiapan:
            // 1. Persiapan Setengah Juz: Ziyadah di halaman 5B atau 10B. Batas maksimal persiapan: 3 hari.
            //    - <= 3 hari: masih persiapan -> TIDAK mengikuti karantina tahfidz
            //    - >= 4 hari: melebihi batas waktu maksimal persiapan -> wajib karantina (Musyrif)
            //    - >= 11 hari: melebihi batas koordinator -> wajib karantina (Koordinator)
            // 2. Persiapan Juziyah: Setengah juz posisi akhir. Batas maksimal persiapan: 7 hari.
            //    - <= 7 hari: masih persiapan -> TIDAK mengikuti karantina tahfidz
            //    - >= 8 hari: melebihi batas waktu maksimal persiapan -> wajib karantina (Musyrif)
            //    - >= 22 hari: melebihi batas koordinator -> wajib karantina (Koordinator)
            // 3. Persiapan Syahadah: Juziyah pada juz khusus (3, 8, 13, 18, 23, 28). Batas maksimal persiapan: 30 hari.
            //    - <= 30 hari: masih persiapan -> TIDAK mengikuti karantina tahfidz
            //    - >= 31 hari: melebihi batas waktu maksimal persiapan -> wajib karantina (Musyrif)
            //    - >= 52 hari: melebihi batas koordinator -> wajib karantina (Koordinator)

            $isPersiapanSetengahJuz = (
                $student['last_achievement_type'] === 'ziyadah' &&
                ($student['last_achievement_halaman'] === '5B' || $student['last_achievement_halaman'] === '10B')
            );

            $isPersiapanJuziyah = (
                $student['last_achievement_type'] === 'setengah_juz' &&
                $student['last_achievement_posisi'] === 'akhir'
            );

            $specialJuz = [3, 8, 13, 18, 23, 28];
            $isPersiapanSyahadah = (
                $student['last_achievement_type'] === 'juziyah' &&
                in_array((int)$student['last_achievement_juz'], $specialJuz)
            );

            $isSedangPersiapan = false;

            if ($isPersiapanSetengahJuz) {
                if ($daysSinceLastAchievement >= 11) {
                    $needsCoordinatorAttention = true;
                    $keterangan = 'Persiapan Setengah Juz';
                } elseif ($daysSinceLastAchievement >= 4) {
                    $needsMusyrifAttention = true;
                    $keterangan = 'Persiapan Setengah Juz';
                } else {
                    // Masih dalam batas waktu maksimal persiapan (<= 3 hari), tidak ikut karantina
                    $isSedangPersiapan = true;
                }
            } elseif ($isPersiapanJuziyah) {
                if ($daysSinceLastAchievement >= 22) {
                    $needsCoordinatorAttention = true;
                    $keterangan = 'Persiapan Juziyah';
                } elseif ($daysSinceLastAchievement >= 8) {
                    $needsMusyrifAttention = true;
                    $keterangan = 'Persiapan Juziyah';
                } else {
                    // Masih dalam batas waktu maksimal persiapan (<= 7 hari), tidak ikut karantina
                    $isSedangPersiapan = true;
                }
            } elseif ($isPersiapanSyahadah) {
                if ($daysSinceLastAchievement >= 52) {
                    $needsCoordinatorAttention = true;
                    $keterangan = 'Persiapan Syahadah';
                } elseif ($daysSinceLastAchievement >= 31) {
                    $needsMusyrifAttention = true;
                    $keterangan = 'Persiapan Syahadah';
                } else {
                    // Masih dalam batas waktu maksimal persiapan (<= 30 hari), tidak ikut karantina
                    $isSedangPersiapan = true;
                }
            }

            // Evaluasi Target Ziyadah:
            // Hanya untuk santri yang TIDAK melebihi waktu persiapan dan TIDAK sedang dalam masa persiapan yang sah
            if (!$needsCoordinatorAttention && !$needsMusyrifAttention && !$isSedangPersiapan) {
                $targetPages = 1;

                // Cek apakah santri menyelesaikan Setengah Juz, Juziyah, atau Syahadah pada periode ini
                $examAchievements = R::getAll("
                    SELECT type, created_at
                    FROM pencapaian
                    WHERE santri_id = ?
                      AND (type = 'setengah_juz' OR type = 'juziyah' OR type = 'syahadah')
                      AND DATE(created_at) BETWEEN ? AND ?
                    ORDER BY created_at DESC
                ", [
                    $student['santri_id'],
                    $startDateStr,
                    $endDateStr
                ]);

                // Jika selesai Syahadah, Juziyah, atau setengah juz pada hari H ($endDateStr):
                // maka tidak ada target minimal ziyadah 1 halaman
                $finishedToday = false;
                foreach ($examAchievements as $ach) {
                    $achDateOnly = (new DateTime($ach['created_at'], new DateTimeZone('Asia/Makassar')))->format('Y-m-d');
                    if ($achDateOnly === $endDateStr) {
                        $finishedToday = true;
                        break;
                    }
                }

                if ($finishedToday) {
                    $targetPages = 0;
                }

                // Jika ada target, hitung pencapaian ziyadah santri pada periode ini
                if ($targetPages > 0) {
                    $ziyadahAchievements = R::getAll("
                        SELECT halaman, created_at
                        FROM pencapaian
                        WHERE santri_id = ?
                          AND (type = 'ziyadah' OR type = 'ziadah')
                          AND DATE(created_at) BETWEEN ? AND ?
                        ORDER BY created_at ASC
                    ", [
                        $student['santri_id'],
                        $startDateStr,
                        $endDateStr
                    ]);

                    $ziyadahPagesCovered = 0;
                    if (!empty($ziyadahAchievements)) {
                        $uniquePages = [];
                        foreach ($ziyadahAchievements as $achievement) {
                            $page = $achievement['halaman'];
                            if (!in_array($page, $uniquePages)) {
                                $uniquePages[] = $page;
                            }
                        }
                        $sortedPages = sortHafalanPages($uniquePages);
                        $ziyadahPagesCovered = count($sortedPages);
                    }

                    if ($ziyadahPagesCovered < $targetPages) {
                        $needsMusyrifAttention = true;
                        $kurang = ($targetPages - $ziyadahPagesCovered) . ' halaman';
                        $keterangan = 'Belum Mencapai Target Ziyadah';
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
                    'jenis_kelamin' => $student['jenis_kelamin'],
                    'musyrif_nama' => $student['musyrif_nama'],
                    'musyrif_id' => $student['musyrif_id']
                ];

                $coordinatorAttention[] = $studentInfo;
            }

            // If student meets musyrif criteria (and not coordinator), add to musyrif attention
            if ($needsMusyrifAttention && !$needsCoordinatorAttention) {
                $studentInfo = [
                    'id' => $student['santri_id'],
                    'nama' => $student['nama'],
                    'keterangan' => $keterangan,
                    'lama_persiapan' => $lamaPersiapan,
                    'jenis_kelamin' => $student['jenis_kelamin'],
                    'musyrif_nama' => $student['musyrif_nama'],
                    'musyrif_id' => $student['musyrif_id']
                ];

                // Add kurang info if it's a ziyadah requirement issue
                if (!empty($kurang)) {
                    $studentInfo['kurang'] = $kurang;
                }

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

        // Format the message according to the specified structure
        $message = "";

        // Sort coordinator attention musyrifs alphabetically
        if (!empty($coordinatorAttentionGrouped)) {
            $message .= "⚠️ *KARANTINA TAHFIDZ - BUTUH PERHATIAN KOORDINATOR TAHFIDZ:*\n\n";
            ksort($coordinatorAttentionGrouped);

            foreach ($coordinatorAttentionGrouped as $musyrifGroup) {
                $musyrifName = $musyrifGroup['musyrif_nama'];
                $students = $musyrifGroup['students'];

                if (!empty($students)) {
                    $message .= "Halaqah {$musyrifName}:\n";

                    foreach ($students as $student) {
                        $message .= "- {$student['nama']} ({$student['keterangan']})\n";
                    }

                    $message .= "\n"; // Extra newline after each musyrif's list
                }
            }
        }

        // Add Musyrif attention section if there are students needing musyrif attention
        if (!empty($musyrifAttentionGrouped)) {
            $message .= "⚠️ *KARANTINA TAHFIDZ - BUTUH PERHATIAN MUSYRIF:*\n\n";

            // Separate male and female students
            $putra = array_filter($musyrifAttention, function($student) {
                return strtolower($student['jenis_kelamin']) === 'laki-laki';
            });

            $putri = array_filter($musyrifAttention, function($student) {
                return strtolower($student['jenis_kelamin']) === 'perempuan';
            });

            // Format PUTRA section
            if (!empty($putra)) {
                $message .= "*PUTRA*\n\n";

                // Group by keterangan
                $putraByKeterangan = [];
                foreach ($putra as $student) {
                    $kategori = $student['keterangan'];
                    if (!isset($putraByKeterangan[$kategori])) {
                        $putraByKeterangan[$kategori] = [];
                    }
                    $putraByKeterangan[$kategori][] = $student;
                }

                // Add each category
                foreach ($putraByKeterangan as $kategori => $students) {
                    $message .= "*{$kategori}*\n";
                    if ($kategori === 'Belum Mencapai Target Ziyadah') {
                        $byMusyrif = [];
                        foreach ($students as $student) {
                            $mName = $student['musyrif_nama'];
                            if (!isset($byMusyrif[$mName])) {
                                $byMusyrif[$mName] = [];
                            }
                            $byMusyrif[$mName][] = $student;
                        }
                        ksort($byMusyrif);
                        foreach ($byMusyrif as $mName => $mStudents) {
                            $message .= "Halaqah {$mName}:\n";
                            foreach ($mStudents as $student) {
                                $message .= "- {$student['nama']} - Kurang : {$student['kurang']}\n";
                            }
                            $message .= "\n";
                        }
                    } else {
                        foreach ($students as $student) {
                            $message .= "- {$student['nama']} - Lama persiapan : {$student['lama_persiapan']}\n";
                        }
                        $message .= "\n";
                    }
                }
            }

            // Format PUTRI section
            if (!empty($putri)) {
                if (!empty($putra)) {
                    $message .= "\n"; // Add extra newline if putra section exists
                }
                $message .= "*PUTRI*\n\n";

                // Group by keterangan
                $putriByKeterangan = [];
                foreach ($putri as $student) {
                    $kategori = $student['keterangan'];
                    if (!isset($putriByKeterangan[$kategori])) {
                        $putriByKeterangan[$kategori] = [];
                    }
                    $putriByKeterangan[$kategori][] = $student;
                }

                // Add each category
                foreach ($putriByKeterangan as $kategori => $students) {
                    $message .= "*{$kategori}*\n";
                    if ($kategori === 'Belum Mencapai Target Ziyadah') {
                        $byMusyrif = [];
                        foreach ($students as $student) {
                            $mName = $student['musyrif_nama'];
                            if (!isset($byMusyrif[$mName])) {
                                $byMusyrif[$mName] = [];
                            }
                            $byMusyrif[$mName][] = $student;
                        }
                        ksort($byMusyrif);
                        foreach ($byMusyrif as $mName => $mStudents) {
                            $message .= "Halaqah {$mName}:\n";
                            foreach ($mStudents as $student) {
                                $message .= "- {$student['nama']} - Kurang : {$student['kurang']}\n";
                            }
                            $message .= "\n";
                        }
                    } else {
                        foreach ($students as $student) {
                            $message .= "- {$student['nama']} - Lama persiapan : {$student['lama_persiapan']}\n";
                        }
                        $message .= "\n";
                    }
                }
            }
        }

        // If no students need attention, send a message indicating that
        if (empty($coordinatorAttentionGrouped) && empty($musyrifAttentionGrouped)) {
            $message .= "Tidak ada santri yang perlu perhatian saat ini.";
        }

        // Send the message to the WhatsApp group using Sidobe API
        $curl = curl_init();

        $postData = json_encode(array(
            'group_id' => $selectedGroupId,
            'message' => $message
        ));

        curl_setopt_array($curl, array(
            CURLOPT_URL => 'https://api.sidobe.com/wa/v1/send-message',
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_ENCODING => '',
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 30, // Set a reasonable timeout
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => 'POST',
            CURLOPT_POSTFIELDS => $postData,
            CURLOPT_HTTPHEADER => array(
                'X-Secret-Key: DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO',
                'Content-Type: application/json'
            ),
            CURLOPT_SSL_VERIFYPEER => false, // Disable SSL certificate verification
            CURLOPT_SSL_VERIFYHOST => false, // Disable host verification
        ));

        $response = curl_exec($curl);
        $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        $error = curl_error($curl);
        curl_close($curl);

        // Log the request and response for debugging
        error_log("WhatsApp API Request: " . $postData);
        error_log("WhatsApp API Response: " . $response);
        error_log("WhatsApp API HTTP Code: " . $httpCode);
        error_log("WhatsApp API Error: " . $error);

        $responseData = json_decode($response, true);

        if ($httpCode === 200 && isset($responseData['is_success']) && $responseData['is_success'] === true) {
            echo json_encode([
                'success' => true,
                'message' => 'Message sent successfully to WhatsApp group',
                'sent_message' => $message
            ]);
        } else {
            $errorMessage = $responseData['message'] ?? 'Unknown error';
            if ($error) {
                $errorMessage .= ' (cURL error: ' . $error . ')';
            }
            throw new Exception('Failed to send message to WhatsApp group: ' . $errorMessage);
        }
    } else {
        throw new Exception('Invalid action specified');
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => $e->getMessage()]);
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
