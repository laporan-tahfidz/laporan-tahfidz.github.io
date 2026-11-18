<?php
// config.php - Basic PHP configuration

// Set timezone to Asia/Makassar (WITA, UTC+8)
date_default_timezone_set('Asia/Makassar');

// Session configuration
ini_set('session.cookie_httponly', 1);
ini_set('session.use_strict_mode', 1);
ini_set('session.cookie_secure', 0); // Set to 1 in production with HTTPS
ini_set('session.cookie_samesite', 'Strict');

// Error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);