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
    // 1. Clean webhooksyahadah
    $recordsSyahadah = R::find('webhooksyahadah', ' (kirim_ke_web_utama = 1 OR kirim_ke_web_utama = "1" OR kirim_ke_web_utama = true) AND (kirim_ke_web_surat = 1 OR kirim_ke_web_surat = "1" OR kirim_ke_web_surat = true) ');
    $deletedSyahadah = count($recordsSyahadah);
    if ($deletedSyahadah > 0) {
        R::trashAll($recordsSyahadah);
    }

    // 2. Clean webhookjuziyah
    $recordsJuziyah = R::find('webhookjuziyah', ' kirim_ke_web_surat = 1 OR kirim_ke_web_surat = "1" OR kirim_ke_web_surat = true ');
    $deletedJuziyah = count($recordsJuziyah);
    if ($deletedJuziyah > 0) {
        R::trashAll($recordsJuziyah);
    }

    $totalDeleted = $deletedSyahadah + $deletedJuziyah;

    echo json_encode([
        'success' => true,
        'message' => 'Berhasil membersihkan data syahadah dan juziyah eksternal yang sudah terkirim',
        'deleted_syahadah_count' => $deletedSyahadah,
        'deleted_juziyah_count' => $deletedJuziyah,
        'deleted_count' => $totalDeleted
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => $e->getMessage()]);
}
