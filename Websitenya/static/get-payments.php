<?php
// get-payments.php - Get all payments

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/helpers.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    echo json_encode(['success' => false, 'message' => 'Unauthorized']);
    exit;
}

try {
    initDB();
    
    // Get all payments from the database
    $payments = R::findAll('pembayaran', 'ORDER BY payment_date DESC');
    
    // Convert RedBean objects to arrays
    $paymentsArray = [];
    foreach ($payments as $payment) {
        $paymentsArray[] = [
            'id' => $payment->id,
            'student_id' => $payment->student_id,
            'amount' => $payment->amount,
            'payment_date' => $payment->payment_date,
            'payment_method' => $payment->payment_method,
            'status' => $payment->status,
            'order_id' => $payment->order_id,
            'description' => $payment->description,
            'created_at' => $payment->created_at,
            'updated_at' => $payment->updated_at
        ];
    }
    
    echo json_encode([
        'success' => true,
        'data' => $paymentsArray
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}