<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';

setCORSHeaders();
header('Content-Type: application/json');

try {
    initDB();
    
    $logs = [];
    
    // Check 'tes' table columns
    $tesCols = R::inspect('tes');
    if (!empty($tesCols)) {
        if (!isset($tesCols['status'])) {
            R::exec("ALTER TABLE tes ADD COLUMN status TEXT DEFAULT 'lancar'");
            R::exec("UPDATE tes SET status = 'lancar' WHERE status IS NULL OR status = ''");
            $logs[] = "Added column 'status' to table 'tes'";
        }
    } else {
        $logs[] = "Table 'tes' does not exist yet";
    }

    echo json_encode([
        'success' => true,
        'message' => 'Migration executed successfully',
        'logs' => $logs
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Migration failed: ' . $e->getMessage()
    ]);
}
R::close();
