<?php
// check-db-schema.php - Script to check the database schema

require_once __DIR__ . '/init-session.php';

try {
    // Get all tables from the database
    $tablesResult = R::getAll('SELECT name FROM sqlite_master WHERE type = "table"');
    
    echo "Tables in the database:\n";
    foreach ($tablesResult as $table) {
        echo "- " . $table['name'] . "\n";
        
        // Get columns for each table
        $columnsResult = R::getAll("PRAGMA table_info({$table['name']})");
        echo "  Columns:\n";
        foreach ($columnsResult as $column) {
            echo "  - {$column['name']} ({$column['type']})\n";
        }
        echo "\n";
    }
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}