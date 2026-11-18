<?php
/**
 * CRON Job script to check students who haven't made deposits for a week or more
 * Sends a WhatsApp message to the group defined in settings
 */

require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/helpers.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

try {
    // Get the WhatsApp group ID from settings
    $whatsappGroupIdSetting = R::findOne('settings', 'key = ?', ['whatsapp_group_id']);
    if (!$whatsappGroupIdSetting || empty($whatsappGroupIdSetting->value)) {
        echo "Error: WhatsApp group ID not found in settings.\n";
        exit(1);
    }
    $whatsappGroupId = $whatsappGroupIdSetting->value;

    // Calculate the date 7 days ago using Asia/Makassar timezone
    $makassarTime = new DateTime('now', new DateTimeZone('Asia/Makassar'));
    $makassarTime->modify('-7 days');
    $sevenDaysAgo = $makassarTime->format('Y-m-d H:i:s');

    // Get students with their last achievement (any type: ziyadah, setengah juz, juziyah, or syahadah)
    // Only include students who had their most recent achievement more than 7 days ago
    // For students without current musyrif, use their most recent previous musyrif assignment
    $studentsWithOldAchievements = R::getAll("
        WITH current_assignment AS (
            SELECT 
                santri_nik,
                musyrif_id,
                ROW_NUMBER() OVER (PARTITION BY santri_nik ORDER BY created_at DESC) as rn
            FROM musyrfst
            WHERE musyrif_id IS NOT NULL
        ),
        latest_assignment AS (
            SELECT 
                santri_nik,
                musyrif_id,
                ROW_NUMBER() OVER (PARTITION BY santri_nik ORDER BY created_at DESC) as rn
            FROM musyrfst
        )
        SELECT 
            s.nama_panggilan,
            s.nama_sesuai_kk,
            COALESCE(m_current.nama, m_prev.nama) AS musyrif_nama,
            p.type AS last_achievement_type,
            p.created_at AS last_achievement_date
        FROM santri s
        INNER JOIN (
            SELECT 
                nik,
                type,
                created_at,
                ROW_NUMBER() OVER (PARTITION BY nik ORDER BY created_at DESC) as rn
            FROM pencapaian
        ) p ON s.nik = p.nik AND p.rn = 1
        LEFT JOIN latest_assignment la ON s.nik = la.santri_nik AND la.rn = 1
        LEFT JOIN current_assignment ca ON s.nik = ca.santri_nik AND ca.rn = 1
        LEFT JOIN musyrif m_current ON ca.musyrif_id = m_current.id
        LEFT JOIN musyrif m_prev ON la.musyrif_id = m_prev.id AND m_current.id IS NULL
        WHERE p.created_at <= ? AND COALESCE(m_current.nama, m_prev.nama) IS NOT NULL
        ORDER BY COALESCE(m_current.nama, m_prev.nama), 
                 s.nama_panggilan
    ", [$sevenDaysAgo]);

    if (empty($studentsWithOldAchievements)) {
        echo "No students found with achievements older than 7 days.\n";
        exit(0);
    }

    // Group students by musyrif
    $groupedStudents = [];
    foreach ($studentsWithOldAchievements as $student) {
        $musyrifName = $student['musyrif_nama'];
        if (!isset($groupedStudents[$musyrifName])) {
            $groupedStudents[$musyrifName] = [];
        }
        
        // Calculate days since last achievement using Asia/Makassar timezone
        $lastAchievementDate = new DateTime($student['last_achievement_date'], new DateTimeZone('Asia/Makassar'));
        $now = new DateTime('now', new DateTimeZone('Asia/Makassar'));
        $interval = $lastAchievementDate->diff($now);
        $daysSince = $interval->days;
        
        // Convert achievement type to Indonesian name
        $achievementType = '';
        switch ($student['last_achievement_type']) {
            case 'ziyadah':
                $achievementType = 'Ziyadah';
                break;
            case 'setengah_juz':
                $achievementType = 'Setengah Juz';
                break;
            case 'juziyah':
                $achievementType = 'Juziyah';
                break;
            case 'syahadah':
                $achievementType = 'Syahadah';
                break;
            default:
                $achievementType = ucfirst(str_replace('_', ' ', $student['last_achievement_type']));
        }
        
        $groupedStudents[$musyrifName][] = [
            'name' => $student['nama_panggilan'] ?: $student['nama_sesuai_kk'],
            'achievement_type' => $achievementType,
            'days_since' => $daysSince
        ];
    }

    // Format the message
    $message = "*SANTRI YANG LAMA NGGAK SETORAN*\n\n";
    
    foreach ($groupedStudents as $musyrifName => $students) {
        $message .= "Halaqah " . $musyrifName . "\n\n";
        
        $counter = 1;
        foreach ($students as $student) {
            $message .= "$counter. {$student['name']} ({$student['achievement_type']}, {$student['days_since']} hari yang lalu)\n";
            $counter++;
        }
        
        $message .= "\n";
    }
    
    $message .= "Untuk data selengkapnya, bisa dicek di https://tahfidz.mabaiz.com/super";

    // Send the WhatsApp message
    $sendResult = sendWhatsAppMessageToGroup($whatsappGroupId, $message);

    if ($sendResult['success']) {
        echo "WhatsApp message sent successfully to group ID: $whatsappGroupId\n";
        echo "Message: $message\n";
    } else {
        echo "Failed to send WhatsApp message: " . $sendResult['message'] . "\n";
        exit(1);
    }

} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
    exit(1);
} finally {
    // Close the database connection
    R::close();
}

/**
 * Function to send WhatsApp message to a group
 */
function sendWhatsAppMessageToGroup($groupId, $message) {
    $curl = curl_init();
    
    $payload = json_encode([
        'group_id' => $groupId,
        'message' => $message
    ]);
    
    curl_setopt_array($curl, [
        CURLOPT_URL => 'https://api.sidobe.com/wa/v1/send-message',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_HTTPHEADER => [
            'X-Secret-Key: DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO',
            'Content-Type: application/json'
        ],
        CURLOPT_SSL_VERIFYPEER => false, // Allow connections without SSL verification
        CURLOPT_SSL_VERIFYHOST => 0      // Don't verify SSL certificate host
    ]);
    
    $response = curl_exec($curl);
    $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    $error = curl_error($curl);
    
    curl_close($curl);
    
    if ($error) {
        return [
            'success' => false,
            'message' => 'cURL Error: ' . $error
        ];
    }
    
    $responseData = json_decode($response, true);
    
    if ($httpCode >= 200 && $httpCode < 300 && isset($responseData['is_success']) && $responseData['is_success']) {
        return [
            'success' => true,
            'message' => 'Message sent successfully'
        ];
    } else {
        return [
            'success' => false,
            'message' => 'API Error: ' . $response
        ];
    }
}
?>