<?php
require_once __DIR__ . '/library/rb-sqlite.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

try {
    // Create the settings table if it doesn't exist
    $pdo = R::getDatabaseAdapter()->getDatabase()->getPDO();
    
    // Check if the settings table already exists
    $tablesStmt = $pdo->query("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'");
    $tableExists = $tablesStmt->fetch();
    
    if (!$tableExists) {
        // Create the settings table
        $pdo->exec("
            CREATE TABLE settings (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE NOT NULL,
                value TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ");

        echo "Settings table created successfully.\n";
    } else {
        echo "Settings table already exists.\n";
    }
    
    // Insert the default WhatsApp group ID setting if it doesn't exist
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM settings WHERE key = ?");
    $stmt->execute(['whatsapp_group_id']);
    $count = $stmt->fetchColumn();
    
    if ($count == 0) {
        $insertStmt = $pdo->prepare("INSERT INTO settings (key, value) VALUES (?, ?)");
        $insertStmt->execute(['whatsapp_group_id', '']);
        echo "WhatsApp group ID setting added to the database.\n";
    } else {
        echo "WhatsApp group ID setting already exists.\n";
    }
    
    echo "Database setup completed successfully.\n";
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

R::close();
?>