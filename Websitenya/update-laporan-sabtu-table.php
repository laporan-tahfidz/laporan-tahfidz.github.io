<?php
require_once __DIR__ . '/static/library/rb-sqlite.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/static/everynight-in-my-dream.db');

try {
    // Force RedBeanPHP to create the table by temporarily freezing it
    R::freeze(false); // Unfreeze first if needed

    // Create or update the laporan_sabtu table
    // RedBeanPHP will automatically create the table if it doesn't exist
    // or update it if needed when we store a bean

    $testBean = R::dispense('laporansabtu'); // Using the actual table name without underscores
    $testBean->murajaah_juz = 1;
    $testBean->hafalan_entries = json_encode([]);
    $testBean->created_at = R::isoDateTime();

    $id = R::store($testBean);
    R::trash($testBean); // Remove the test entry

    echo "Database structure updated successfully. The 'laporansabtu' table is ready.\n";
} catch (Exception $e) {
    echo "Error updating database structure: " . $e->getMessage() . "\n";
}

R::close();
?>