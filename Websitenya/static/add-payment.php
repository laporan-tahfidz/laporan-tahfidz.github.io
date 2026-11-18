<?php
// add-payment.php - Add a new payment

require_once __DIR__ . '/init-session.php';
require_once __DIR__ . '/helpers.php';
require_once __DIR__ . '/helpers-idempotency.php';

header('Content-Type: application/json');

// Enable CORS
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, X-Idempotency-Key');

if ($_SERVER['REQUEST_METHOD'] == 'OPTIONS') {
    exit(0);
}

// Get the idempotency key from header or JSON input
$idempotencyKey = getIdempotencyKey();

// Check if this request has already been processed
if ($idempotencyKey) {
    $storedResponse = checkIdempotency($idempotencyKey, 'POST');
    if ($storedResponse) {
        // Return the stored response to prevent duplicate processing
        echo json_encode($storedResponse);
        exit;
    }
}

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);

// Verify token - function will check both request body and Authorization header
if (!verifyToken()) {
    $errorResponse = ['success' => false, 'message' => 'Unauthorized'];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
    exit;
}

try {
    initDB();

    // Get form data
    $student_id = $input['student_id'] ?? '';
    $amount = $input['amount'] ?? '';
    $payment_date = $input['payment_date'] ?? date('Y-m-d');
    $payment_method = $input['payment_method'] ?? 'transfer_bank';
    $status = $input['status'] ?? 'pending';
    $order_id = $input['order_id'] ?? '';
    $description = $input['description'] ?? '';

    // Validate required fields
    if (empty($student_id) || empty($amount)) {
        $errorResponse = ['success' => false, 'message' => 'Student ID and Amount are required'];

        // Store the response for idempotency if key was provided
        if ($idempotencyKey) {
            storeIdempotency($idempotencyKey, $errorResponse, 'POST');
        }

        echo json_encode($errorResponse);
        exit;
    }

    // Create new payment bean
    $payment = R::dispense('pembayaran');
    $payment->student_id = $student_id;
    $payment->amount = $amount;
    $payment->payment_date = $payment_date;
    $payment->payment_method = $payment_method;
    $payment->status = $status;
    $payment->order_id = $order_id;
    $payment->description = $description;
    $payment->created_at = date('Y-m-d H:i:s');
    $payment->updated_at = date('Y-m-d H:i:s');

    // Store the payment
    $id = R::store($payment);

    $successResponse = [
        'success' => true,
        'message' => 'Payment added successfully',
        'data' => [
            'id' => $id,
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
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $successResponse, 'POST');
    }

    echo json_encode($successResponse);
} catch (Exception $e) {
    $errorResponse = [
        'success' => false,
        'message' => 'Database error: ' . $e->getMessage()
    ];

    // Store the response for idempotency if key was provided
    if ($idempotencyKey) {
        storeIdempotency($idempotencyKey, $errorResponse, 'POST');
    }

    echo json_encode($errorResponse);
}