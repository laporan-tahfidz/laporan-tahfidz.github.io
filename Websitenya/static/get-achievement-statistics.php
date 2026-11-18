<?php
require_once __DIR__ . '/library/rb-sqlite.php';
require_once __DIR__ . '/cors.php';

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    cors();
    http_response_code(200);
    exit();
}

// Enable CORS for all requests
cors();

// Get the input data
$input = json_decode(file_get_contents('php://input'), true);
$token = $input['token'] ?? '';

// Validate token (simplified validation - in real app, validate against DB)
if ($token) {
    // If a token is provided, verify it
    require_once __DIR__ . '/functions.php';
    if (!verifyToken($token)) {
        http_response_code(401);
        echo json_encode(['success' => false, 'message' => 'Unauthorized']);
        exit;
    }
}

try {
    R::setup('sqlite:./everynight-in-my-dream.db');

    // Get the current year
    $currentYear = date('Y');
    
    // Prepare data arrays for each achievement type
    $data = [
        'ziyadah' => [],
        'setengah_juz' => [],
        'juziyah' => [],
        'syahadah' => []
    ];
    
    // Query for each achievement type
    foreach ($data as $type => $value) {
        // Get all records for the type ordered by date
        $allRecordsSql = "";
        switch ($type) {
            case 'ziyadah':
                $allRecordsSql = "SELECT created_at FROM pencapaian WHERE type = 'ziyadah' ORDER BY created_at";
                break;
            case 'setengah_juz':
                $allRecordsSql = "SELECT created_at FROM pencapaian WHERE type = 'setengah_juz' ORDER BY created_at";
                break;
            case 'juziyah':
                $allRecordsSql = "SELECT created_at FROM pencapaian WHERE type = 'juziyah' ORDER BY created_at";
                break;
            case 'syahadah':
                $allRecordsSql = "SELECT created_at FROM pencapaian WHERE type = 'syahadah' ORDER BY created_at";
                break;
        }

        if ($allRecordsSql) {
            $allRecords = R::getAll($allRecordsSql);

            // Debug: Log the number of records for each type
            error_log("Achievement type: $type, Records count: " . count($allRecords));

            // If there are no records for this type, set empty array
            if (count($allRecords) === 0) {
                $data[$type] = [];
                continue;
            }

            // Determine the date range based on actual data
            $datesWithData = [];
            foreach ($allRecords as $record) {
                // Extract only the date part (YYYY-MM-DD) from the datetime
                $recordDate = substr($record['created_at'], 0, 10);

                // Only include records from the current year
                if (substr($recordDate, 0, 4) == $currentYear) {
                    $datesWithData[] = $recordDate;
                }
            }

            // If no records from current year, set empty array
            if (empty($datesWithData)) {
                $data[$type] = [];
                continue;
            }

            // Sort the dates to find the earliest and latest
            sort($datesWithData);
            $firstDate = $datesWithData[0];
            $lastDate = end($datesWithData);

            // Create a date range from the first to the last date with data
            $startDate = new DateTime($firstDate);
            $endDate = new DateTime($lastDate);
            $interval = new DateInterval('P1D');
            $dateRange = new DatePeriod($startDate, $interval, $endDate);

            // Create a map of dates to counts for the current year
            $dateCounts = [];
            foreach ($allRecords as $record) {
                // Extract only the date part (YYYY-MM-DD) from the datetime
                $recordDate = substr($record['created_at'], 0, 10);

                // Only count records from the current year
                if (substr($recordDate, 0, 4) == $currentYear) {
                    if (!isset($dateCounts[$recordDate])) {
                        $dateCounts[$recordDate] = 0;
                    }
                    $dateCounts[$recordDate]++;
                }
            }

            // Debug: Log the date counts
            error_log("Date counts for $type: " . print_r($dateCounts, true));

            $dailyResults = [];

            foreach ($dateRange as $date) {
                $dateStr = $date->format('Y-m-d');

                // Use the daily count if available, otherwise 0
                $dailyCount = isset($dateCounts[$dateStr]) ? $dateCounts[$dateStr] : 0;

                $dailyResults[] = [
                    'date' => $dateStr,
                    'total' => $dailyCount
                ];
            }

            $data[$type] = $dailyResults;
        }
    }

    R::close();

    echo json_encode([
        'success' => true,
        'data' => $data
    ]);
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => $e->getMessage()
    ]);
}
?>