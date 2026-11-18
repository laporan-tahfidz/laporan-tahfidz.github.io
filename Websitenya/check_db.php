<?php
require_once __DIR__ . '/static/library/rb-sqlite.php';
R::setup('sqlite:' . __DIR__ . '/static/everynight-in-my-dream.db');
$count = R::count('santri');
echo "Number of students in database: $count\n";
$activeCount = R::getCell('SELECT COUNT(*) FROM santri WHERE status = "aktif"');
echo "Number of active students in database: $activeCount\n";

// Show some sample students
$students = R::findAll('santri', 'LIMIT 5');
echo "Sample students:\n";
foreach ($students as $student) {
    echo "- ID: {$student->id}, Name: {$student->nama_sesuai_kk}, Status: {$student->status}, Year: {$student->tahun_masuk}\n";
}
?>