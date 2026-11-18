<?php
$lines = file('nomor-halaman.txt', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
$mapping = [];

foreach ($lines as $line) {
    // Juz 1, halaman 1A, surat Al-Baqarah, ayat 5
    if (preg_match('/Juz (\d+), halaman (\d+)([AB]), surat (.+), ayat (\d+)/', $line, $matches)) {
        $juz = intval($matches[1]);
        $pageNum = intval($matches[2]);
        $pageSuffix = $matches[3];
        $surah = trim($matches[4]);
        $ayah = intval($matches[5]);
        
        $pageIndex = ($pageNum - 1) * 2 + ($pageSuffix === 'A' ? 1 : 2);
        
        if (!isset($mapping[$juz])) {
            $mapping[$juz] = [];
        }
        
        $mapping[$juz][$pageIndex] = [
            'surah' => $surah,
            'ayah' => $ayah
        ];
    }
}

echo "function getQuranMapping() {\n";
echo "    return [\n";
foreach ($mapping as $juz => $pages) {
    echo "        $juz => [\n";
    foreach ($pages as $index => $data) {
        echo "            $index => ['surah' => '" . addslashes($data['surah']) . "', 'ayah' => {$data['ayah']}],\n";
    }
    echo "        ],\n";
}
echo "    ];\n";
echo "}\n";
