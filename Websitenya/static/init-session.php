<?php
// init-session.php - Initialize RedBeanPHP (no longer using sessions for OTP/token storage)

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/library/rb-sqlite.php';

// Initialize RedBeanPHP with SQLite database
R::setup('sqlite:./everynight-in-my-dream.db');

// Force creation of the santri table by dispensing and storing a temporary bean
$santriBean = R::dispense('santri');
$id = R::store($santriBean);
R::trash($santriBean); // Clean up the temporary entry

// Force creation of the musyrif table by dispensing and storing a temporary bean
$musyrifBean = R::dispense('musyrif');
$id = R::store($musyrifBean);
R::trash($musyrifBean); // Clean up the temporary entry

// Force creation of the musyrfst table by dispensing and storing a temporary bean
$musyrfstBean = R::dispense('musyrfst');
$id = R::store($musyrfstBean);
R::trash($musyrfstBean); // Clean up the temporary entry

// Start session if not already started (still needed for other session data if any)
if (session_status() == PHP_SESSION_NONE) {
    session_start();
}