<?php
// server.php - Simple PHP server for development

// This file is used to serve the PHP backend files during development
// Run with: php -S localhost:4848 server.php

// Define the port based on the port file
$port = 4848;

// Handle routing for API endpoints
$request_uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Map API routes to corresponding PHP files
$routes = [
    '/send-otp.php' => __DIR__ . '/static/send-otp.php',
    '/verify-otp.php' => __DIR__ . '/static/verify-otp.php',
    '/verify-token.php' => __DIR__ . '/static/verify-token.php',
    '/fetch-student-data.php' => __DIR__ . '/static/fetch-student-data.php',
    '/init-database.php' => __DIR__ . '/static/init-database.php',
    '/get-student-count.php' => __DIR__ . '/static/get-student-count.php',
    '/get-whatsapp-groups.php' => __DIR__ . '/static/get-whatsapp-groups.php',
    '/get-musyrifs.php' => __DIR__ . '/static/get-musyrifs.php',
    '/add-musyrif.php' => __DIR__ . '/static/add-musyrif.php',
    '/update-musyrif.php' => __DIR__ . '/static/update-musyrif.php',
    '/delete-musyrif.php' => __DIR__ . '/static/delete-musyrif.php',
    '/get-musyrif-with-students.php' => __DIR__ . '/static/get-musyrif-with-students.php',
    '/get-musyrif-students.php' => __DIR__ . '/static/get-musyrif-students.php',
    '/assign-students-to-musyrif.php' => __DIR__ . '/static/assign-students-to-musyrif.php',
    '/get-musyrif-progress.php' => __DIR__ . '/static/get-musyrif-progress.php',
    '/add-attendance.php' => __DIR__ . '/static/add-attendance.php',
    '/add-lesson.php' => __DIR__ . '/static/add-lesson.php',
    '/add-payment.php' => __DIR__ . '/static/add-payment.php',
    '/add-student.php' => __DIR__ . '/static/add-student.php',
    '/add-teacher.php' => __DIR__ . '/static/add-teacher.php',
    '/delete-attendance.php' => __DIR__ . '/static/delete-attendance.php',
    '/delete-lesson.php' => __DIR__ . '/static/delete-lesson.php',
    '/delete-payment.php' => __DIR__ . '/static/delete-payment.php',
    '/delete-student.php' => __DIR__ . '/static/delete-student.php',
    '/delete-teacher.php' => __DIR__ . '/static/delete-teacher.php',
    '/get-attendances.php' => __DIR__ . '/static/get-attendances.php',
    '/get-lessons.php' => __DIR__ . '/static/get-lessons.php',
    '/get-payments.php' => __DIR__ . '/static/get-payments.php',
    '/get-reports.php' => __DIR__ . '/static/get-reports.php',
    '/get-students.php' => __DIR__ . '/static/get-students.php',
    '/get-teachers.php' => __DIR__ . '/static/get-teachers.php',
    '/get-students-for-halaqah.php' => __DIR__ . '/static/get-students-for-halaqah.php',
    '/update-attendance.php' => __DIR__ . '/static/update-attendance.php',
    '/update-lesson.php' => __DIR__ . '/static/update-lesson.php',
    '/update-payment.php' => __DIR__ . '/static/update-payment.php',
    '/update-student.php' => __DIR__ . '/static/update-student.php',
    '/update-teacher.php' => __DIR__ . '/static/update-teacher.php',
    '/get-all-musyrifs.php' => __DIR__ . '/static/get-all-musyrifs.php',
    '/get-report-data.php' => __DIR__ . '/static/get-report-data.php',
];

if (isset($routes[$request_uri])) {
    require_once $routes[$request_uri];
    exit;
}

// Check if the request is for a PHP file in the static directory
$requestedFile = __DIR__ . '/static' . $request_uri;
if (preg_match('/\.php$/', $request_uri) && file_exists($requestedFile)) {
    require_once $requestedFile;
    exit;
}

// For other requests, return a 404
http_response_code(404);
echo json_encode(['error' => 'Not Found']);