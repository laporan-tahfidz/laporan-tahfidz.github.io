<?php
/**
 * WhatsApp Queue Processor
 * 
 * This file processes the WhatsApp message queue (antrianwhatsapp table).
 * It should be called periodically (e.g., via cron job) to send queued messages.
 * 
 * Usage: php wa.php OR access via website.com/wa.php
 * 
 * Timezone: Asia/Makassar (WITA, UTC+8)
 */

require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/config.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Ensure timezone is set to Asia/Makassar
date_default_timezone_set('Asia/Makassar');

/**
 * Send WhatsApp message via Sidobe API
 */
function sendWhatsAppMessage($phoneNumber, $message) {
    $sidobe_api_key = 'DCfkgRISvKPeivhUkndWGEUmezbbaxIKxvgTPkfPgohEOoBeNO';
    
    $curl = curl_init();
    
    curl_setopt_array($curl, [
        CURLOPT_URL => 'https://api.sidobe.com/wa/v1/send-message',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode([
            'phone' => $phoneNumber,
            'message' => $message
        ]),
        CURLOPT_HTTPHEADER => [
            'X-Secret-Key: ' . $sidobe_api_key,
            'Content-Type: application/json'
        ],
        CURLOPT_SSL_VERIFYPEER => false,
    ]);
    
    $response = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);
    
    $result = json_decode($response, true);
    
    if ($result && isset($result['is_success']) && $result['is_success'] === true) {
        return ['success' => true, 'message' => 'Message sent successfully'];
    } else {
        return ['success' => false, 'message' => 'Failed to send message: ' . ($result['message'] ?? 'Unknown error')];
    }
}

/**
 * Send WhatsApp message to group via Sidobe API
 */
function sendWhatsAppMessageToGroup($groupId, $message) {
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
        CURLOPT_SSL_VERIFYPEER => false,
    ]);
    
    $response = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);
    
    $result = json_decode($response, true);
    
    if ($result && isset($result['is_success']) && $result['is_success'] === true) {
        return ['success' => true, 'message' => 'Message sent to group successfully'];
    } else {
        return ['success' => false, 'message' => 'Failed to send to group: ' . ($result['message'] ?? 'Unknown error')];
    }
}

try {
    // Get one random message from the queue
    $queueItem = R::findOne('antrianwhatsapp', '1=1 ORDER BY RANDOM() LIMIT 1');
    
    if (!$queueItem) {
        echo json_encode([
            'success' => true,
            'message' => 'No messages in queue',
            'queue_length' => 0
        ]);
        exit;
    }
    
    // Determine if it's a group or personal message
    $sendResult = null;
    if (!empty($queueItem->group_id)) {
        // Send to group
        $sendResult = sendWhatsAppMessageToGroup($queueItem->group_id, $queueItem->pesan);
    } elseif (!empty($queueItem->phone_number)) {
        // Send to personal number
        $sendResult = sendWhatsAppMessage($queueItem->phone_number, $queueItem->pesan);
    } else {
        // Invalid queue item
        echo json_encode([
            'success' => false,
            'message' => 'Invalid queue item: missing phone_number or group_id',
            'queue_id' => $queueItem->id
        ]);
        R::trash($queueItem);
        exit;
    }
    
    // If successfully sent, delete from queue
    if ($sendResult['success']) {
        R::trash($queueItem);
        
        echo json_encode([
            'success' => true,
            'message' => 'Message sent and removed from queue',
            'queue_id' => $queueItem->id,
            'timestamp' => date('Y-m-d H:i:s') // This will be in Asia/Makassar timezone
        ]);
    } else {
        // Log the error but keep in queue for retry
        echo json_encode([
            'success' => false,
            'message' => 'Failed to send message, will retry later',
            'queue_id' => $queueItem->id,
            'error' => $sendResult['message'],
            'timestamp' => date('Y-m-d H:i:s') // This will be in Asia/Makassar timezone
        ]);
    }
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Error processing queue: ' . $e->getMessage(),
        'timestamp' => date('Y-m-d H:i:s') // This will be in Asia/Makassar timezone
    ]);
}
