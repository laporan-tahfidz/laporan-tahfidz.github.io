<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';

date_default_timezone_set('Asia/Makassar');
setCORSHeaders();
header('Content-Type: application/json');

if (!R::testConnection()) {
    R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');
}

try {
    $record = R::findOne('webhooksyahadah', ' kirim_ke_web_utama = 0 OR kirim_ke_web_utama = false OR kirim_ke_web_utama IS NULL ');

    if (!$record) {
        echo json_encode(['success' => true, 'message' => 'Tidak ada data syahadah yang perlu dikirim ke web utama']);
        exit;
    }

    $payload = [
        'id_guru' => (int)$record->id_guru,
        'nik_santri' => (string)$record->nik_santri,
        'tanggal' => (string)$record->tanggal,
        'id_tahfidz' => (int)$record->id_tahfidz
    ];

    $ch = curl_init('https://insya-allah-berkah.mabaiz.com/webhook-syahadah.php');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => json_encode($payload),
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_SSL_VERIFYPEER => false,
        CURLOPT_TIMEOUT => 30
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $record->kirim_ke_web_utama = true;
    R::store($record);

    echo json_encode([
        'success' => true,
        'message' => 'Berhasil mengirim data ke web utama',
        'http_code' => $httpCode,
        'response' => $response,
        'data' => $payload
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => $e->getMessage()]);
}
