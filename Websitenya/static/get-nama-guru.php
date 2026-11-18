<?php
require_once __DIR__ . '/functions.php';

setCORSHeaders();
header('Content-Type: application/json');

$ch = curl_init('https://insya-allah-berkah.mabaiz.com/nama-guru.php');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_SSL_VERIFYPEER => false,
    CURLOPT_TIMEOUT => 15
]);
$response = curl_exec($ch);
curl_close($ch);

if ($response) {
    echo $response;
} else {
    echo json_encode([]);
}
