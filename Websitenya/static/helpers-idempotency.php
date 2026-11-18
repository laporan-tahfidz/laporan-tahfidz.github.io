<?php
/**
 * Helper functions for implementing idempotency keys in API requests
 */

/**
 * Creates or retrieves an idempotency key from the request
 */
function getIdempotencyKey() {
    // Check for idempotency key in header first
    $idempotencyKey = $_SERVER['HTTP_X_IDEMPOTENCY_KEY'] ?? null;
    
    // If not in header, check in POST data
    if (!$idempotencyKey && isset($_POST['idempotency_key'])) {
        $idempotencyKey = $_POST['idempotency_key'];
    }
    
    // If not in POST data, check in JSON input
    if (!$idempotencyKey) {
        $input = json_decode(file_get_contents('php://input'), true);
        if (isset($input['idempotency_key'])) {
            $idempotencyKey = $input['idempotency_key'];
        }
    }
    
    return $idempotencyKey;
}

/**
 * Checks if a request with the given idempotency key has already been processed
 */
function checkIdempotency($idempotencyKey, $requestMethod = null) {
    if (!$idempotencyKey) {
        return null; // No idempotency key provided, skip idempotency check
    }
    
    // Find existing idempotency record
    $idempotencyRecord = R::findOne('idempotency', 'key = ?', [$idempotencyKey]);
    
    if ($idempotencyRecord) {
        // Return the stored response if this request was already processed
        return json_decode($idempotencyRecord->response, true);
    }
    
    return null; // Request hasn't been processed yet
}

/**
 * Stores the result of a processed request with its idempotency key
 */
function storeIdempotency($idempotencyKey, $response, $requestMethod = null) {
    if (!$idempotencyKey) {
        return; // No idempotency key provided, skip storing
    }
    
    // Check if record already exists
    $idempotencyRecord = R::findOne('idempotency', 'key = ?', [$idempotencyKey]);
    
    if (!$idempotencyRecord) {
        // Create new idempotency record
        $idempotencyRecord = R::dispense('idempotency');
        $idempotencyRecord->key = $idempotencyKey;
    }
    
    $idempotencyRecord->response = json_encode($response);
    $idempotencyRecord->method = $requestMethod ?: $_SERVER['REQUEST_METHOD'];
    $idempotencyRecord->request_data = json_encode($_POST ?: json_decode(file_get_contents('php://input'), true) ?: []);
    $idempotencyRecord->created_at = R::isoDateTime();
    $idempotencyRecord->updated_at = R::isoDateTime();
    
    R::store($idempotencyRecord);
}

/**
 * Initializes the idempotency table if it doesn't exist
 */
function initIdempotencyTable() {
    try {
        // Check if idempotency table exists
        $tables = R::inspect();
        
        if (!in_array('idempotency', $tables)) {
            // Create the idempotency table
            $createTableSQL = "
                CREATE TABLE idempotency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    response TEXT,
                    method TEXT,
                    request_data TEXT,
                    created_at DATETIME,
                    updated_at DATETIME
                )
            ";
            
            R::exec($createTableSQL);
        }
    } catch (Exception $e) {
        error_log("Error initializing idempotency table: " . $e->getMessage());
    }
}

/**
 * Validates the idempotency key format
 */
function isValidIdempotencyKey($key) {
    // Idempotency keys should be UUIDs or similar unique identifiers
    // Basic validation: alphanumeric, hyphens, and underscores, length between 8 and 128 chars
    return preg_match('/^[a-zA-Z0-9_-]{8,128}$/', $key);
}
?>