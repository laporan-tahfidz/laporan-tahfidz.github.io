<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/cors.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Set CORS headers
cors();

header('Content-Type: application/json');

// Check if request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    // http_response_code(405);
    // echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    // exit;
}

try {
    // Step 1: Get all musyrif
    $musyrifs = R::getAll("SELECT id, nama FROM musyrif ORDER BY nama ASC");
    
    $output = "📖 *DATA MURAJAAH SANTRI*\n\n";
    
    foreach ($musyrifs as $musyrif) {
        // Step 2: Get students assigned to this musyrif
        $students = R::getAll("
            SELECT s.nik, s.nama_sesuai_kk as nama
            FROM musyrfst ms
            JOIN santri s ON ms.santri_nik = s.nik
            WHERE ms.musyrif_id = ?
            ORDER BY s.nama_sesuai_kk ASC
        ", [$musyrif['id']]);
        
        if (empty($students)) {
            continue;
        }
        
        $musyrifOutput = "";
        
        foreach ($students as $student) {
            // Step 3: Get all juz that student has been tested (lancar)
            $testedJuz = R::getCol("
                SELECT DISTINCT juz 
                FROM tes 
                WHERE nik = ? AND juz IS NOT NULL
            ", [$student['nik']]);
            
            $lancarCount = count($testedJuz);
            
            // Step 4: Get last achievement
            $lastAchievement = R::findOne('pencapaian', 'nik = ? AND (juz IS NOT NULL OR syahadah IS NOT NULL) ORDER BY created_at DESC', [$student['nik']]);
            
            $lastJuz = 30;
            if ($lastAchievement) {
                if ($lastAchievement->type === 'syahadah') {
                    $syahadahVal = strtolower((string)$lastAchievement->syahadah);
                    $syahadahJuzMap = [
                        'pertama' => 3, '1' => 3,
                        'kedua' => 8, '2' => 8,
                        'ketiga' => 13, '3' => 13,
                        'keempat' => 18, '4' => 18,
                        'kelima' => 23, '5' => 23,
                        'keenam' => 28, '6' => 28,
                    ];
                    foreach ($syahadahJuzMap as $key => $jNum) {
                        if (strpos($syahadahVal, $key) !== false) {
                            $lastJuz = $jNum;
                            break;
                        }
                    }
                } elseif (!empty($lastAchievement->juz)) {
                    $lastJuz = $lastAchievement->juz;
                }
            } else {
                $submittedJuz = R::getCol("
                    SELECT DISTINCT juz 
                    FROM pencapaian 
                    WHERE nik = ? AND juz IS NOT NULL
                    ORDER BY CAST(juz AS INTEGER) ASC
                ", [$student['nik']]);
                if (!empty($submittedJuz)) {
                    $lastJuz = end($submittedJuz);
                }
            }
            
            $musyrifOutput .= "- {$student['nama']} _(lancar {$lancarCount} juz, hafalan terakhir Juz {$lastJuz})_\n";
        }
        
        if (!empty($musyrifOutput)) {
            $output .= "*" . strtoupper($musyrif['nama']) . "*\n";
            $output .= $musyrifOutput;
            $output .= "\n";
        }
    }
    
    $output .= "_Jazakumullahu khairan_ 🤲";
    
    // SIBAIZ WhatsApp Group ID
    $sibaiz_group_id = "6281545143654-1598842563@g.us";
    
    // Send to WhatsApp via Sidobe API
    $sidobe_api_url = "https://api.sidobe.com/wa/v1/send-message";
    $sidobe_secret_key = "DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO";
    
    $curl = curl_init();
    curl_setopt_array($curl, [
        CURLOPT_URL => $sidobe_api_url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode([
            "group_id" => $sibaiz_group_id,
            "message" => $output
        ]),
        CURLOPT_HTTPHEADER => [
            'X-Secret-Key: ' . $sidobe_secret_key,
            'Content-Type: application/json'
        ],
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_SSL_VERIFYHOST => false
    ]);
    
    $response = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    $err = curl_error($curl);
    curl_close($curl);
    
    if ($err) {
        http_response_code(500);
        echo json_encode([
            'success' => false, 
            'message' => 'cURL Error: ' . $err
        ]);
        exit;
    }
    
    $response_data = json_decode($response, true);
    
    if ($http_code === 200 && isset($response_data['is_success']) && $response_data['is_success']) {
        echo json_encode([
            'success' => true,
            'message' => 'Pesan murajaah berhasil dikirim ke grup SIBAIZ',
            'sidobe_response' => $response_data
        ]);
    } else {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'message' => 'Gagal mengirim pesan WhatsApp',
            'response' => $response_data,
            'http_code' => $http_code
        ]);
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Terjadi kesalahan: ' . $e->getMessage()
    ]);
}
?>
