<?php
// helpers.php - Common helper functions

require_once __DIR__ . '/functions.php'; // Include functions.php to reuse common functions


/**
 * Send WhatsApp notification for achievements
 */
function sendAchievementNotification($achievementData, $studentData) {
    // Determine if this is a juziyah or syahadah achievement
    if ($achievementData['type'] !== 'juziyah' && $achievementData['type'] !== 'syahadah') {
        // Only send notifications for juziyah and syahadah achievements
        return ['success' => true, 'message' => 'Not a juziyah or syahadah achievement, no notification sent'];
    }

    // Format the message with Asia/Makassar timezone (WITA, UTC+8)
    $today = new DateTime('now', new DateTimeZone('Asia/Makassar'));
    $formattedDate = $today->format('l, j F Y'); // e.g., "Wednesday, 2 December 2025"

    // Convert day and month names to Indonesian
    $dayNames = [
        'Monday' => 'Senin', 'Tuesday' => 'Selasa', 'Wednesday' => 'Rabu',
        'Thursday' => 'Kamis', 'Friday' => 'Jumat', 'Saturday' => 'Sabtu', 'Sunday' => 'Minggu'
    ];
    $monthNames = [
        'January' => 'Januari', 'February' => 'Februari', 'March' => 'Maret', 'April' => 'April',
        'May' => 'Mei', 'June' => 'Juni', 'July' => 'Juli', 'August' => 'Agustus',
        'September' => 'September', 'October' => 'Oktober', 'November' => 'November', 'December' => 'Desember'
    ];

    $formattedDate = strtr($formattedDate, $dayNames);
    $formattedDate = strtr($formattedDate, $monthNames);

    // Determine class level based on year of entry
    $kelas = determineClassLevel($studentData['tahun_masuk'] ?? date('Y'));

    // Determine evaluator based on achievement type
    $evaluator = '';
    if ($achievementData['type'] === 'juziyah') {
        // For juziyah, use the penguji from the achievement data
        // If not provided, try to get from musyrif connection as fallback
        if (!empty($achievementData['penguji'])) {
            $evaluator = $achievementData['penguji'];
        } else {
            // Find the musyrif connected to this student as fallback
            $connection = R::findOne('musyrif_santri', 'santri_id = ?', [$studentData['id']]);
            if ($connection) {
                $musyrif = R::load('musyrif', $connection->musyrif_id);
                if ($musyrif) {
                    $evaluator = $musyrif->nama_lengkap;
                } else {
                    $evaluator = 'Musyrif';
                }
            } else {
                $evaluator = 'Musyrif';
            }
        }
    } elseif ($achievementData['type'] === 'syahadah') {
        $evaluator = $achievementData['penguji'] ?? 'Penguji';
    }

    // Determine rating based on errors
    $rating = determineRating($achievementData['type'], $achievementData['kesalahan']);

    // Format the achievement information
    $achievementInfo = '';
    if ($achievementData['type'] === 'juziyah') {
        $achievementInfo = "Juz : {$achievementData['juz']} ({$achievementData['kesalahan']} kesalahan, {$rating})";
    } elseif ($achievementData['type'] === 'syahadah') {
        $achievementInfo = "Syahadah : {$achievementData['syahadah']} ({$achievementData['kesalahan']} kesalahan, {$rating})";
    }

    // Format the message header based on achievement type
    $header = ($achievementData['type'] === 'syahadah') ? "✏️ SYAHADAH:" : "✏️ JUZIYYAH:";

    $message = "$header\n\n" .
               "Tanggal : {$formattedDate}\n" .
               "Nama : {$studentData['nama_sesuai_kk']}\n" .
               "Angkatan : {$studentData['tahun_masuk']}\n" .
               "{$achievementInfo}\n" .
               "Penguji : {$evaluator}\n" .
               "Catatan : " . ($achievementData['catatan'] ?? '');

    // Get the selected WhatsApp group ID
    require_once __DIR__ . '/functions-settings.php';
    $groupId = getSelectedWhatsAppGroupId();

    if (empty($groupId)) {
        return ['success' => false, 'message' => 'No WhatsApp group selected'];
    }

    // Send message via Sidobe API
    $sidobe_api_key = 'DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO';

    $curl = curl_init();

    curl_setopt_array($curl, [
        CURLOPT_URL => 'https://api.sidobe.com/wa/v1/send-message',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode([
            'group_id' => $groupId,
            'message' => $message
        ]),
        CURLOPT_HTTPHEADER => [
            'X-Secret-Key: ' . $sidobe_api_key,
            'Content-Type: application/json'
        ],
        CURLOPT_SSL_VERIFYPEER => false, // Allow non-HTTPS connections
    ]);

    $response = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);

    $result = json_decode($response, true);

    if ($result && isset($result['is_success']) && $result['is_success'] === true) {
        return ['success' => true, 'message' => 'WhatsApp notification sent successfully'];
    } else {
        return ['success' => false, 'message' => 'Failed to send WhatsApp notification: ' . ($result['message'] ?? 'Unknown error')];
    }
}

/**
 * Determine class level based on year of entry
 */
function determineClassLevel($entryYear) {
    if (!$entryYear) {
        return 'N/A';
    }

    // Get class configuration from settings
    require_once __DIR__ . '/functions-settings.php';

    $kelas1Year = getSetting('kelas1_year');
    $kelas2Year = getSetting('kelas2_year');
    $kelas3Year = getSetting('kelas3_year');

    // If configuration exists, use it to determine class
    if ($kelas1Year && $entryYear == $kelas1Year) {
        return 'Kelas 1';
    } elseif ($kelas2Year && $entryYear == $kelas2Year) {
        return 'Kelas 2';
    } elseif ($kelas3Year && $entryYear == $kelas3Year) {
        return 'Kelas 3';
    } else {
        // Fallback to previous logic if no configuration exists
        $currentYear = date('Y');
        $yearDiff = $currentYear - $entryYear;

        // Assuming the class levels are based on years since entry
        // Ula = first year, Tsaniyah = second year, Tsalitsah = third year, etc.
        switch ($yearDiff) {
            case 0:
                return 'Ula';
            case 1:
                return 'Tsaniyah';
            case 2:
                return 'Tsalitsah';
            case 3:
                return 'Rabi\'ah';
            case 4:
                return 'Khamsyah';
            case 5:
                return 'Sadiyah';
            case 6:
                return 'Sab\'iyah';
            case 7:
                return 'Samaniyah';
            case 8:
                return 'Tis\'iyah';
            default:
                return 'Tahsin';
        }
    }
}

/**
 * Determine rating based on achievement type and number of errors
 */
function determineRating($type, $errors) {
    if ($type === 'juziyah') {
        if ($errors >= 0 && $errors <= 5) {
            return 'Mumtaz';
        } elseif ($errors >= 6 && $errors <= 10) {
            return 'Jayyid Jiddan';
        } elseif ($errors >= 11 && $errors <= 15) {
            return 'Jayyid';
        } elseif ($errors >= 16 && $errors <= 20) {
            return 'Maqbul';
        } elseif ($errors >= 21) {
            return 'Mardud';
        }
    } elseif ($type === 'syahadah') {
        if ($errors >= 0 && $errors <= 10) {
            return 'Mumtaz';
        } elseif ($errors >= 11 && $errors <= 20) {
            return 'Jayyid Jiddan';
        } elseif ($errors >= 21 && $errors <= 30) {
            return 'Jayyid';
        } elseif ($errors >= 31 && $errors <= 40) {
            return 'Maqbul';
        } elseif ($errors >= 41) {
            return 'Mardud';
        }
    }

    return 'Unknown';
}