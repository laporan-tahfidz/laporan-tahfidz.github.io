<?php
require_once __DIR__ . '/static/library/rb-sqlite.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/static/everynight-in-my-dream.db');

// Check if database connection works
echo "Database connected successfully\n";

// Get all students
$students = R::findAll('santri', 'ORDER BY nama_sesuai_kk ASC');
echo "Total students: " . count($students) . "\n";

foreach ($students as $s) {
    echo 'Student: ' . $s->nama_sesuai_kk . ' (NIK: ' . $s->nik . ')' . PHP_EOL;
    
    // Check if this is the student mentioned in the issue
    if (strpos(strtolower($s->nama_sesuai_kk), 'rizky') !== false) {
        echo "  -> Found student with 'rizky' in name!\n";
        
        // Get their achievements
        $achievements = R::findAll('pencapaian', 'nik = ?', [$s->nik]);
        echo "  -> Total achievements: " . count($achievements) . "\n";
        
        foreach ($achievements as $a) {
            echo "    ID: {$a->id}, Type: {$a->type}, Juz: {$a->juz}, Created: {$a->created_at}\n";
        }
    }
}

R::close();
?>