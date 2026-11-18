<?php
require_once __DIR__ . '/static/library/rb-sqlite.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/static/everynight-in-my-dream.db');

// Create a temporary record to ensure the table structure is correct
$tempRecord = R::dispense('musyrfst');
$tempRecord->musyrif_id = 0;
$tempRecord->santri_nik = '0';
$tempRecord->created_at = R::isoDateTime();
$tempRecord->updated_at = R::isoDateTime();

// Store and immediately trash to ensure table structure exists
$id = R::store($tempRecord);
R::trash($tempRecord);

echo "Database table structure ensured.\n";

// Now test the query
$musyrifs = R::getAll('SELECT m.id, m.nama, m.created_at, m.updated_at, (SELECT COUNT(*) FROM musyrfst ms WHERE ms.musyrif_id = m.id) as assigned_students_count FROM musyrif m ORDER BY m.nama ASC');

echo "Query results: " . count($musyrifs) . " records found.\n";
foreach ($musyrifs as $musyrif) {
    echo "ID: {$musyrif['id']}, Nama: {$musyrif['nama']}, Students: {$musyrif['assigned_students_count']}\n";
}
?>