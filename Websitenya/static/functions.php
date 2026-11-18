<?php
// functions.php - Common utility functions

date_default_timezone_set('Asia/Makassar');

require_once __DIR__ . '/library/rb-sqlite.php';

/**
 * Set CORS headers
 */
function setCORSHeaders() {
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Idempotency-Key');

    // Handle preflight OPTIONS request
    if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
        http_response_code(200);
        exit();
    }
}

/**
 * Initialize the database connection
 */
function initDB() {
    // Check if database is already connected
    try {
        if (!R::testConnection()) {
            $dbPath = __DIR__ . '/everynight-in-my-dream.db';
            R::setup("sqlite:$dbPath");
            R::freeze(false);
        }
    } catch (Exception $e) {
        // If testConnection throws an exception, the database hasn't been set up yet
        $dbPath = __DIR__ . '/everynight-in-my-dream.db';
        R::setup("sqlite:$dbPath");
        R::freeze(false);
    }

    try {
        $tesCols = R::inspect('tes');
        if (!empty($tesCols) && !isset($tesCols['status'])) {
            R::exec("ALTER TABLE tes ADD COLUMN status TEXT DEFAULT 'lancar'");
            R::exec("UPDATE tes SET status = 'lancar' WHERE status IS NULL OR status = ''");
        }
    } catch (Exception $ex) {
        // Ignore if table does not exist yet
    }
}

/**
 * Verify super admin token
 * Accepts token either as a parameter or from the Authorization header
 */
function verifyToken($token = null) {
    // If no token provided, try to get it from the Authorization header
    if (!$token) {
        $authHeader = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
        
        // Check if it starts with 'Bearer '
        if (preg_match('/^Bearer\s+(.+)$/i', $authHeader, $matches)) {
            $token = trim($matches[1]);
        }
    }

    if (!$token) {
        return false;
    }

    // Check if token exists and is valid in the database
    $tokenBean = R::findOne('token', ' token_hash = ? ', [hash('sha256', $token)]);

    if (!$tokenBean) {
        return false;
    }

    // Check if token has expired (tokens expire after 24 hours)
    if ($tokenBean->expires_at < time()) {
        // Remove expired token from database
        R::trash($tokenBean);
        return false;
    }

    return true;
}

/**
 * Validate and sanitize input data
 */
function validateInput($data, $rules) {
    $errors = [];

    foreach ($rules as $field => $rule) {
        $value = $data[$field] ?? null;

        if (strpos($rule, 'required') !== false && empty($value)) {
            $errors[] = "$field is required";
        }

        if (!empty($value)) {
            if (strpos($rule, 'email') !== false && !filter_var($value, FILTER_VALIDATE_EMAIL)) {
                $errors[] = "$field must be a valid email";
            }

            if (strpos($rule, 'numeric') !== false && !is_numeric($value)) {
                $errors[] = "$field must be numeric";
            }

            if (strpos($rule, 'date') !== false && !strtotime($value)) {
                $errors[] = "$field must be a valid date";
            }

            if (strpos($rule, 'phone') !== false && !preg_match('/^\+?[1-9]\d{1,14}$/', $value)) {
                $errors[] = "$field must be a valid phone number";
            }
        }
    }

    return $errors;
}

/**
 * Convert Indonesian phone number to international format
 * Converts 081234567890 to +6281234567890
 */
function convertToInternationalPhone($phoneNumber) {
    // Remove any spaces, dashes, or parentheses
    $cleanNumber = preg_replace('/[^0-9]/', '', $phoneNumber);

    // If starts with '08', replace with '+628'
    if (substr($cleanNumber, 0, 1) === '0' && strlen($cleanNumber) >= 10) {
        $cleanNumber = '+62' . substr($cleanNumber, 1);
    } elseif (substr($cleanNumber, 0, 2) === '62' && strlen($cleanNumber) >= 11) {
        // If starts with '62', add '+' prefix
        $cleanNumber = '+' . $cleanNumber;
    } elseif (substr($cleanNumber, 0, 3) === '+62' && strlen($cleanNumber) >= 11) {
        // Already in correct format
        return $cleanNumber;
    }

    return $cleanNumber;
}

/**
 * Handle file uploads
 */
function handleFileUpload($file, $targetDir = 'images/') {
    if (!$file || $file['error'] !== UPLOAD_ERR_OK) {
        return null;
    }

    $targetDir = __DIR__ . '/' . $targetDir;

    // Create directory if it doesn't exist
    if (!is_dir($targetDir)) {
        mkdir($targetDir, 0755, true);
    }

    $fileName = uniqid() . '_' . basename($file['name']);
    $targetPath = $targetDir . $fileName;

    if (move_uploaded_file($file['tmp_name'], $targetPath)) {
        return $fileName;
    }

    return null;
}