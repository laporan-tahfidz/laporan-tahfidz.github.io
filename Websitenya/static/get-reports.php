<?php
// get-reports.php - Get all reports

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/helpers.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    initDB();
    
    // Get all reports from the database
    $reports = R::findAll('laporan', 'ORDER BY created_at DESC');
    
    // Convert RedBean objects to arrays
    $reportsArray = [];
    foreach ($reports as $report) {
        $reportsArray[] = [
            'id' => $report->id,
            'title' => $report->title,
            'period' => $report->period,
            'summary' => $report->summary,
            'created_at' => $report->created_at,
            'updated_at' => $report->updated_at
        ];
    }
    
    echo json_encode([
        'success' => true,
        'data' => $reportsArray
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}