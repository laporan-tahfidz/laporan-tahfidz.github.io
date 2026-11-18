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
    $results = [];

    // 1. Process webhooksyahadah
    $recordSyahadah = R::findOne('webhooksyahadah', ' kirim_ke_web_surat = 0 OR kirim_ke_web_surat = false OR kirim_ke_web_surat IS NULL ');
    if ($recordSyahadah) {
        $payloadSyahadah = [
            'nama_santri' => (string)$recordSyahadah->nama_santri,
            'syahadah_ke' => (int)$recordSyahadah->syahadah_ke,
            'nilai' => (string)$recordSyahadah->nilai,
            'tahun_masuk' => (string)$recordSyahadah->tahun_masuk
        ];

        $ch = curl_init('https://surat.mabaiz.com/webhook-syahadah.php');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode($payloadSyahadah),
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_TIMEOUT => 30
        ]);
        $responseSyahadah = curl_exec($ch);
        $httpCodeSyahadah = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        $recordSyahadah->kirim_ke_web_surat = true;
        R::store($recordSyahadah);

        $results['syahadah'] = [
            'sent' => true,
            'http_code' => $httpCodeSyahadah,
            'response' => $responseSyahadah,
            'data' => $payloadSyahadah
        ];
    } else {
        $results['syahadah'] = [
            'sent' => false,
            'message' => 'Tidak ada data syahadah yang perlu dikirim ke web surat'
        ];
    }

    // 2. Process webhookjuziyah
    $recordJuziyah = R::findOne('webhookjuziyah', ' kirim_ke_web_surat = 0 OR kirim_ke_web_surat = false OR kirim_ke_web_surat IS NULL ');
    if ($recordJuziyah) {
        $payloadJuziyah = [
            'nama_santri' => (string)$recordJuziyah->nama_santri,
            'juz' => is_numeric($recordJuziyah->juz) ? (int)$recordJuziyah->juz : (string)$recordJuziyah->juz,
            'nilai' => (string)$recordJuziyah->nilai,
            'tahun_masuk' => (string)$recordJuziyah->tahun_masuk
        ];

        $ch = curl_init('https://surat.mabaiz.com/webhook-juziyah.php');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode($payloadJuziyah),
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_TIMEOUT => 30
        ]);
        $responseJuziyah = curl_exec($ch);
        $httpCodeJuziyah = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        $recordJuziyah->kirim_ke_web_surat = true;
        R::store($recordJuziyah);

        $results['juziyah'] = [
            'sent' => true,
            'http_code' => $httpCodeJuziyah,
            'response' => $responseJuziyah,
            'data' => $payloadJuziyah
        ];
    } else {
        $results['juziyah'] = [
            'sent' => false,
            'message' => 'Tidak ada data juziyah yang perlu dikirim ke web surat'
        ];
    }

    echo json_encode([
        'success' => true,
        'message' => 'Berhasil me-request pengiriman data ke web surat',
        'results' => $results
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => $e->getMessage()]);
}
