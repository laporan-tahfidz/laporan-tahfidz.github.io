<?php
// update-payment.php - Update an existing payment

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
    
    // Get form data
    $id = $input['id'] ?? '';
    $student_id = $input['student_id'] ?? '';
    $amount = $input['amount'] ?? '';
    $payment_date = $input['payment_date'] ?? '';
    $payment_method = $input['payment_method'] ?? '';
    $status = $input['status'] ?? '';
    $order_id = $input['order_id'] ?? '';
    $description = $input['description'] ?? '';
    
    // Validate required fields
    if (empty($id)) {
        echo json_encode(['success' => false, 'message' => 'ID is required']);
        exit;
    }
    
    // Find the existing payment
    $payment = R::load('pembayaran', $id);
    if (!$payment->id) {
        echo json_encode(['success' => false, 'message' => 'Payment not found']);
        exit;
    }
    
    // Update payment properties
    if (!empty($student_id)) $payment->student_id = $student_id;
    if (!empty($amount)) $payment->amount = $amount;
    if (!empty($payment_date)) $payment->payment_date = $payment_date;
    if (!empty($payment_method)) $payment->payment_method = $payment_method;
    if (!empty($status)) $payment->status = $status;
    if (!empty($order_id)) $payment->order_id = $order_id;
    if (!empty($description)) $payment->description = $description;
    $payment->updated_at = date('Y-m-d H:i:s');
    
    // Store the updated payment
    R::store($payment);
    
    echo json_encode([
        'success' => true,
        'message' => 'Payment updated successfully',
        'data' => [
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
        ]
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ]);
}