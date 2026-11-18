<?php
require_once __DIR__ . '/static/library/rb-sqlite.php';

// Initialize the database connection
R::setup('sqlite:' . __DIR__ . '/static/everynight-in-my-dream.db');

// Create the adminotps table if it doesn't exist
try {
    // Check if the table exists by trying to get its info
    $columns = R::inspect('adminotps');
    echo "adminotps table already exists.\n";
} catch (Exception $e) {
    // Table doesn't exist, create it
    echo "Creating adminotps table...\n";

    // Create the table by dispensing and trashing a bean to force table creation
    $otp = R::dispense('adminotps');
    $otp->phone = '+6281234567890';
    $otp->code = '123456';
    $otp->expires_at = '2023-01-01 00:00:00';
    $otp->created_at = '2023-01-01 00:00:00';

    $id = R::store($otp);
    R::trash($otp);

    echo "adminotps table created successfully.\n";
}

// Also ensure the sessions table exists
try {
    $columns = R::inspect('sessions');
    echo "sessions table already exists.\n";
} catch (Exception $e) {
    // Table doesn't exist, create it
    echo "Creating sessions table...\n";

    // Create the table by dispensing and trashing a bean to force table creation
    $session = R::dispense('sessions');
    $session->token = 'sample_token';
    $session->user_id = 'sample_user';
    $session->created_at = '2023-01-01 00:00:00';
    $session->expires_at = '2023-01-02 00:00:00';

    $id = R::store($session);
    R::trash($session);

    echo "sessions table created successfully.\n";
}

// Ensure the token table exists
try {
    $columns = R::inspect('token');
    echo "token table already exists.\n";
} catch (Exception $e) {
    // Table doesn't exist, create it
    echo "Creating token table...\n";

    // Create the table by dispensing and trashing a bean to force table creation
    $token = R::dispense('token');
    $token->token_hash = 'sample_token_hash';
    $token->expires_at = time() + (24 * 60 * 60); // 24 hours from now
    $token->created_at = R::isoDateTime();

    $id = R::store($token);
    R::trash($token);

    echo "token table created successfully.\n";
}

echo "Database setup completed.\n";
?>