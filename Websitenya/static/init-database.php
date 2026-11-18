<?php
// init-database.php - Initialize database tables if they don't exist

require_once __DIR__ . '/init-session.php';

try {
    // Test connection by trying to find records in the santri table
    // This will create the table if it doesn't exist
    $test = R::find('santri', 'id > 0 LIMIT 1');

    // Also initialize the musyrif table
    $testMusyrif = R::find('musyrif', 'id > 0 LIMIT 1');

    // Also initialize the musyrfst table
    $testMusyrfst = R::find('musyrfst', 'id > 0 LIMIT 1');

    // Ensure idempotency table exists
    $tables = R::inspect();

    if (!in_array('idempotency', $tables)) {
        // Create the idempotency table
        $createTableSQL = "
            CREATE TABLE idempotency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                response TEXT,
                method TEXT,
                request_data TEXT,
                created_at DATETIME,
                updated_at DATETIME
            )
        ";

        R::exec($createTableSQL);
    }

    echo json_encode([
        'success' => true,
        'message' => 'Database initialized successfully'
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}