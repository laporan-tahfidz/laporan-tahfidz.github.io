<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/functions.php';
require_once __DIR__ . '/functions-settings.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/everynight-in-my-dream.db');

// Set CORS headers
setCORSHeaders();

header('Content-Type: application/json');

// Check if request method is POST
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// Get the posted data
$input = json_decode(file_get_contents('php://input'), true);

$action = $input['action'] ?? '';

if ($action === 'get') {
    // Get the selected group ID from the database
    $selectedGroupId = getSelectedWhatsAppGroupId();
    
    echo json_encode([
        'success' => true,
        'selected_group_id' => $selectedGroupId
    ]);
} elseif ($action === 'set') {
    // Set the selected group ID in the database
    $groupId = $input['group_id'] ?? '';
    
    if (empty($groupId)) {
        http_response_code(400);
        echo json_encode([
            'success' => false,
            'message' => 'Group ID is required'
        ]);
        exit;
    }
    
    $result = setSelectedWhatsAppGroupId($groupId);
    
    if ($result) {
        echo json_encode([
            'success' => true,
            'message' => 'Group ID saved successfully'
        ]);
    } else {
        http_response_code(500);
        echo json_encode([
            'success' => false,
            'message' => 'Failed to save group ID'
        ]);
    }
} else {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => 'Invalid action. Use "get" or "set".'
    ]);
}

?>