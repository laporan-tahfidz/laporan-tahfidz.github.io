import json
import os
import re

with open('full_report_dataset.json', encoding='utf-8') as f:
    dataset = json.load(f)

json_data_str = json.dumps(dataset, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Laporan & Evaluasi Capaian Tahfidz Santri | Dashboard Eksekutif</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Amiri:wght@400;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            arabic: ['"Amiri"', 'serif']
          },
          colors: {
            emerald: {
              50: '#ecfdf5',
              100: '#d1fae5',
              200: '#a7f3d0',
              300: '#6ee7b7',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
              800: '#065f46',
              900: '#064e3b',
              950: '#022c22',
            },
            teal: {
              50: '#f0fdfa',
              100: '#ccfbf1',
              500: '#14b8a6',
              600: '#0d9488',
              700: '#0f766e',
              900: '#134e4a',
            }
          }
        }
      }
    }
  </script>
  
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  
  <!-- Lucide Icons CDN -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    .dark ::-webkit-scrollbar-track { background: #1e293b; }
    ::-webkit-scrollbar-thumb { background: #94a3b8; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #64748b; }
    
    /* Print Styles */
    @media print {
      body { background: white !important; color: black !important; }
      .no-print { display: none !important; }
      .print-break { page-break-before: always; }
      .shadow-sm, .shadow-md, .shadow-lg, .shadow-xl { box-shadow: none !important; border: 1px solid #e2e8f0; }
    }
    
    /* Subtle Pulse Animation */
    @keyframes gentlePulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.85; transform: scale(0.98); }
    }
    .animate-gentle { animation: gentlePulse 3s infinite ease-in-out; }
    
    /* Badge styling */
    .badge-mumtaz { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .dark .badge-mumtaz { background: #064e3b; color: #86efac; border-color: #059669; }
    
    .badge-jayyid-jiddan { background: #e0f2fe; color: #0369a1; border: 1px solid #7dd3fc; }
    .dark .badge-jayyid-jiddan { background: #0c4a6e; color: #7dd3fc; border-color: #0284c7; }
    
    .badge-jayyid { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
    .dark .badge-jayyid { background: #78350f; color: #fde68a; border-color: #d97706; }
    
    .badge-lancar { background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    .dark .badge-lancar { background: #064e3b; color: #a7f3d0; border-color: #047857; }
    
    .badge-belum-tes { background: #fef9c3; color: #854d0e; border: 1px solid #fef08a; }
    .dark .badge-belum-tes { background: #713f12; color: #fef08a; border-color: #ca8a04; }
    
    .badge-tidak-lancar { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    .dark .badge-tidak-lancar { background: #7f1d1d; color: #fca5a5; border-color: #dc2626; }
  </style>
</head>

<body class="bg-slate-50 text-slate-800 dark:bg-slate-950 dark:text-slate-100 antialiased min-h-screen flex flex-col font-sans transition-colors duration-200">

  <!-- TOP ANNOUNCEMENT & CONTEXT BAR -->
  <div class="bg-emerald-900 text-emerald-100 text-xs py-2 px-4 border-b border-emerald-800 flex flex-wrap items-center justify-between gap-2 no-print">
    <div class="flex items-center gap-2">
      <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
        Live DB Snapshot
      </span>
      <span>Basis Data Terpadu: <code class="font-mono bg-emerald-950/60 px-1.5 py-0.5 rounded text-emerald-300">everynight-in-my-dream.db</code></span>
      <span class="hidden md:inline text-emerald-400/60">•</span>
      <span class="hidden md:inline text-emerald-300">Waktu Evaluasi: Asia/Makassar (WITA)</span>
    </div>
    <div class="flex items-center gap-4 text-emerald-200">
      <span class="flex items-center gap-1">
        <i data-lucide="users" class="w-3.5 h-3.5 text-emerald-400"></i>
        <span>115 Santri Total</span>
      </span>
      <span class="flex items-center gap-1">
        <i data-lucide="award" class="w-3.5 h-3.5 text-emerald-400"></i>
        <span>26 Pemegang Syahadah</span>
      </span>
      <span class="flex items-center gap-1">
        <i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-emerald-400"></i>
        <span>540 Juz Diselesaikan</span>
      </span>
    </div>
  </div>

  <!-- MAIN HEADER -->
  <header class="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 shadow-sm sticky top-0 z-40 transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-20">
        
        <!-- Brand / Identity -->
        <div class="flex items-center gap-3.5">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-600/20">
            <i data-lucide="book-open" class="w-6 h-6"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Laporan Capaian Tahfidz</h1>
              <span class="bg-emerald-100 text-emerald-800 text-[11px] font-semibold px-2 py-0.5 rounded-full dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800">
                Terlengkap & Detail
              </span>
            </div>
            <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 flex items-center gap-1.5 mt-0.5">
              <span>Pesantren Tahfidzul Quran</span>
              <span>•</span>
              <span class="text-emerald-600 dark:text-emerald-400 font-medium">Dashboard Eksekutif, Kelas, Halaqah, Syahadah & Kelancaran</span>
            </p>
          </div>
        </div>

        <!-- Header Actions -->
        <div class="flex items-center gap-2.5 no-print">
          <!-- Dark Mode Toggle -->
          <button id="themeToggleBtn" onclick="toggleTheme()" title="Ubah Tema Gelap/Terang"
            class="p-2.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800 border border-slate-200 dark:border-slate-700 transition">
            <i data-lucide="moon" id="themeIcon" class="w-4 h-4"></i>
          </button>

          <!-- Export CSV -->
          <button onclick="exportToCSV()" title="Unduh Spreadsheet Santri"
            class="hidden sm:inline-flex items-center gap-1.5 px-3 py-2 text-xs font-semibold rounded-lg bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-700 transition">
            <i data-lucide="download" class="w-3.5 h-3.5 text-slate-500"></i>
            <span>Export CSV</span>
          </button>

          <!-- Print / PDF -->
          <button onclick="window.print()" title="Cetak atau Simpan PDF"
            class="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm shadow-emerald-600/30 transition">
            <i data-lucide="printer" class="w-3.5 h-3.5"></i>
            <span>Cetak / PDF</span>
          </button>
        </div>

      </div>

      <!-- MAIN NAVIGATION TABS -->
      <nav class="flex space-x-1 sm:space-x-2 border-t border-slate-100 dark:border-slate-800 overflow-x-auto py-2 no-print" id="mainTabs">
        <button onclick="switchTab('ringkasan')" id="tab-ringkasan" class="tab-btn active px-3.5 py-2 text-xs sm:text-sm font-semibold rounded-lg transition flex items-center gap-2 whitespace-nowrap bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/80">
          <i data-lucide="bar-chart-3" class="w-4 h-4"></i>
          <span>1. Ringkasan Eksekutif</span>
        </button>
        <button onclick="switchTab('syahadah')" id="tab-syahadah" class="tab-btn px-3.5 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-2 whitespace-nowrap text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800">
          <i data-lucide="award" class="w-4 h-4"></i>
          <span>2. Laporan Syahadah</span>
          <span class="ml-1 px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200">26</span>
        </button>
        <button onclick="switchTab('kelancaran')" id="tab-kelancaran" class="tab-btn px-3.5 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-2 whitespace-nowrap text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800">
          <i data-lucide="check-check" class="w-4 h-4"></i>
          <span>3. Status Kelancaran</span>
        </button>
        <button onclick="switchTab('grouping')" id="tab-grouping" class="tab-btn px-3.5 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-2 whitespace-nowrap text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800">
          <i data-lucide="layers" class="w-4 h-4"></i>
          <span>4. Grouping Kelas & Halaqah</span>
        </button>
        <button onclick="switchTab('santri')" id="tab-santri" class="tab-btn px-3.5 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-2 whitespace-nowrap text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800">
          <i data-lucide="user-check" class="w-4 h-4"></i>
          <span>5. Direktori & Detail Santri</span>
          <span class="ml-1 px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300">115</span>
        </button>
        <button onclick="switchTab('panduan')" id="tab-panduan" class="tab-btn px-3.5 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-2 whitespace-nowrap text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-400 dark:hover:text-slate-100 dark:hover:bg-slate-800">
          <i data-lucide="help-circle" class="w-4 h-4"></i>
          <span>6. Panduan Awam & Glosarium</span>
        </button>
      </nav>

    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full">

    <!-- ========================================================================================= -->
    <!-- TAB 1: RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY) -->
    <!-- ========================================================================================= -->
    <section id="content-ringkasan" class="tab-content space-y-6">

      <!-- Layman Explanatory Welcome Banner -->
      <div class="rounded-2xl bg-gradient-to-r from-emerald-800 via-teal-800 to-slate-900 text-white p-6 sm:p-8 shadow-lg relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-white/5 rounded-full blur-2xl pointer-events-none"></div>
        <div class="relative z-10 max-w-3xl">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-400/20 text-emerald-200 border border-emerald-400/30 mb-3">
            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-emerald-300"></i>
            <span>Ringkasan Singkat untuk Awam & Wali Santri</span>
          </div>
          <h2 class="text-2xl sm:text-3xl font-extrabold tracking-tight leading-snug">
            Kilas Kinerja & Kemajuan Tahfidz Santri Saat Ini
          </h2>
          <p class="mt-2 text-slate-200 text-sm sm:text-base leading-relaxed">
            Laporan ini menyajikan ringkasan utuh mengenai perjalanan hafalan santri di pesantren kita. 
            Mulai dari setoran hafalan baru harian (<span class="text-emerald-300 font-semibold">Ziyadah</span>), 
            ujian penuntasan satu juz (<span class="text-emerald-300 font-semibold">Juziyah</span>), 
            hingga ujian kelulusan akbar per 5 juz mutqin (<span class="text-emerald-300 font-semibold">Syahadah</span>). 
            Semua data dianalisis secara objektif agar para ustadz, orang tua, maupun masyarakat luas dapat memahami capaian dan kebutuhan pembinaan setiap anak.
          </p>
          <div class="mt-5 flex flex-wrap gap-3">
            <button onclick="switchTab('syahadah')" class="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white text-xs sm:text-sm font-semibold rounded-lg shadow-sm transition flex items-center gap-2">
              <i data-lucide="award" class="w-4 h-4"></i>
              Lihat Siapa Saja yang Lulus Syahadah
            </button>
            <button onclick="switchTab('kelancaran')" class="px-4 py-2 bg-white/10 hover:bg-white/20 text-white text-xs sm:text-sm font-semibold rounded-lg backdrop-blur-sm border border-white/20 transition flex items-center gap-2">
              <i data-lucide="check-check" class="w-4 h-4"></i>
              Lihat Analisis Kelancaran
            </button>
            <button onclick="switchTab('panduan')" class="px-4 py-2 bg-slate-800/80 hover:bg-slate-800 text-emerald-300 text-xs sm:text-sm font-semibold rounded-lg transition flex items-center gap-2">
              <i data-lucide="book" class="w-4 h-4"></i>
              Pelajari Istilah Tahfidz
            </button>
          </div>
        </div>
      </div>

      <!-- 6 METRIC CARDS -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        
        <!-- Total Santri -->
        <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group hover:border-emerald-500 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400">Total Santri</span>
            <div class="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <i data-lucide="users" class="w-4 h-4"></i>
            </div>
          </div>
          <div class="mt-3">
            <span class="text-2xl font-bold text-slate-900 dark:text-white" id="stat-total-santri">115</span>
            <span class="text-xs text-slate-400 ml-1">santri</span>
          </div>
          <p class="text-[11px] text-emerald-600 dark:text-emerald-400 mt-1 font-medium flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            <span id="stat-santri-aktif">97 Santri Aktif</span>
          </p>
        </div>

        <!-- Pemegang Syahadah -->
        <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group hover:border-amber-500 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400">Lulus Syahadah</span>
            <div class="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-950 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <i data-lucide="award" class="w-4 h-4"></i>
            </div>
          </div>
          <div class="mt-3">
            <span class="text-2xl font-bold text-amber-600 dark:text-amber-400" id="stat-santri-syahadah">26</span>
            <span class="text-xs text-slate-400 ml-1">santri</span>
          </div>
          <p class="text-[11px] text-amber-600 dark:text-amber-400 mt-1 font-medium">
            29 Sertifikat diterbitkan
          </p>
        </div>

        <!-- Akumulasi Juz Dihafal -->
        <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group hover:border-emerald-500 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400">Juz Diselesaikan</span>
            <div class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <i data-lucide="book-open-check" class="w-4 h-4"></i>
            </div>
          </div>
          <div class="mt-3">
            <span class="text-2xl font-bold text-emerald-600 dark:text-emerald-400" id="stat-juz-dihafal">540</span>
            <span class="text-xs text-slate-400 ml-1">juz</span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
            Akumulasi seluruh santri
          </p>
        </div>

        <!-- Teruji Mutqin / Lancar -->
        <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group hover:border-teal-500 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400">Teruji Lancar</span>
            <div class="w-8 h-8 rounded-lg bg-teal-50 dark:bg-teal-950 text-teal-600 dark:text-teal-400 flex items-center justify-center">
              <i data-lucide="check-circle" class="w-4 h-4"></i>
            </div>
          </div>
          <div class="mt-3">
            <span class="text-2xl font-bold text-teal-600 dark:text-teal-400" id="stat-juz-lancar">96</span>
            <span class="text-xs text-slate-400 ml-1">juz</span>
          </div>
          <p class="text-[11px] text-teal-600 dark:text-teal-400 mt-1 font-medium">
            Lulus Ujian Tes 1 Juz
          </p>
        </div>

        <!-- Total Setoran & Aktivitas -->
        <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group hover:border-purple-500 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400">Riwayat Setoran</span>
            <div class="w-8 h-8 rounded-lg bg-purple-50 dark:bg-purple-950 text-purple-600 dark:text-purple-400 flex items-center justify-center">
              <i data-lucide="activity" class="w-4 h-4"></i>
            </div>
          </div>
          <div class="mt-3">
            <span class="text-2xl font-bold text-purple-600 dark:text-purple-400">4.228</span>
            <span class="text-xs text-slate-400 ml-1">kali</span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
            Ziyadah & ujian disimak
          </p>
        </div>

        <!-- Evaluasi Mingguan -->
        <div class="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-200 dark:border-slate-800 shadow-sm relative overflow-hidden group hover:border-rose-500 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs font-medium text-slate-500 dark:text-slate-400">Evaluasi Laporan</span>
            <div class="w-8 h-8 rounded-lg bg-rose-50 dark:bg-rose-950 text-rose-600 dark:text-rose-400 flex items-center justify-center">
              <i data-lucide="clipboard-list" class="w-4 h-4"></i>
            </div>
          </div>
          <div class="mt-3">
            <span class="text-2xl font-bold text-rose-600 dark:text-rose-400">364</span>
            <span class="text-xs text-slate-400 ml-1">laporan</span>
          </div>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
            Evaluasi Sabtu terdokumentasi
          </p>
        </div>

      </div>

      <!-- CHARTS ROW 1 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Chart 1: Perbandingan Capaian & Kelancaran per Jenjang Kelas -->
        <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-bold text-slate-900 dark:text-white text-base">Capaian & Kelancaran Rata-Rata per Kelas</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400">Berapa juz yang sudah dihafal vs berapa juz yang sudah teruji mutqin lancar</p>
            </div>
            <span class="px-2.5 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 text-xs font-semibold rounded-lg">
              Per Jenjang
            </span>
          </div>
          <div class="relative h-64">
            <canvas id="chartKelasComparison"></canvas>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500">
            <span><strong class="text-emerald-600 dark:text-emerald-400">Kelas 3 (Ulya)</strong> memimpin dengan rata-rata 11,8 Juz dicapai.</span>
            <button onclick="switchTab('grouping')" class="text-emerald-600 hover:underline font-medium">Detail Kelas &rarr;</button>
          </div>
        </div>

        <!-- Chart 2: Komposisi Status Syahadah Seluruh Santri -->
        <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h3 class="font-bold text-slate-900 dark:text-white text-base">Kesiapan & Kelulusan Ujian Syahadah</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400">Distribusi seluruh santri berdasarkan status sertifikasi 5-Juz</p>
            </div>
            <span class="px-2.5 py-1 bg-amber-50 text-amber-700 dark:bg-amber-950 dark:text-amber-300 text-xs font-semibold rounded-lg">
              Status Syahadah
            </span>
          </div>
          <div class="relative h-64 flex items-center justify-center">
            <canvas id="chartSyahadahStatus"></canvas>
          </div>
          <div class="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500">
            <span><strong class="text-amber-600 dark:text-amber-400">20 Santri</strong> sudah hafal &ge;5 juz dan siap ujian Syahadah 1!</span>
            <button onclick="switchTab('syahadah')" class="text-amber-600 hover:underline font-medium">Detail Syahadah &rarr;</button>
          </div>
        </div>

      </div>

      <!-- CHARTS ROW 2: TOP PERFORMERS & JUZ KENDALA -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Top 5 Santri Hafalan Tertinggi -->
        <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-900 dark:text-white text-sm flex items-center gap-2">
              <i data-lucide="crown" class="w-4 h-4 text-amber-500"></i>
              Top Santri Paling Maju
            </h3>
            <span class="text-[11px] text-slate-400">Berdasarkan Total Juz</span>
          </div>
          <div class="space-y-3 mt-4" id="list-top-achievers">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- Top 5 Santri Paling Lancar (Mutqin) -->
        <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-900 dark:text-white text-sm flex items-center gap-2">
              <i data-lucide="award" class="w-4 h-4 text-emerald-500"></i>
              Top Santri Paling Mutqin
            </h3>
            <span class="text-[11px] text-slate-400">Juz Teruji Lancar</span>
          </div>
          <div class="space-y-3 mt-4" id="list-top-fluent">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- 5 Juz Paling Sering Mengalami Kendala -->
        <div class="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-900 dark:text-white text-sm flex items-center gap-2">
              <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-500"></i>
              Juz Paling Menantang
            </h3>
            <span class="text-[11px] text-slate-400">Frekuensi Tidak Lancar</span>
          </div>
          <div class="space-y-3 mt-4" id="list-challenging-juz">
            <!-- Dynamically populated -->
          </div>
        </div>

      </div>

      <!-- EXECUTIVE SUMMARY CARDS: APA YANG HARUS DILAKUKAN? -->
      <div class="bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/80 rounded-2xl p-6">
        <h3 class="font-bold text-emerald-900 dark:text-emerald-200 text-base flex items-center gap-2">
          <i data-lucide="compass" class="w-5 h-5 text-emerald-600 dark:text-emerald-400"></i>
          Rekomendasi & Langkah Strategis Pembinaan
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4 text-xs sm:text-sm text-emerald-950 dark:text-emerald-200">
          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-emerald-200 dark:border-emerald-800 shadow-sm">
            <div class="font-bold text-slate-900 dark:text-white mb-1 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-amber-500"></span>
              Jadwalkan 20 Calon Syahadah
            </div>
            <p class="text-slate-600 dark:text-slate-300 text-xs leading-relaxed">
              Ada 20 santri yang telah menyelesaikan minimal 5 juz bahkan ada yang 15 juz (seperti M. Alvin & Wildan Akhram) namun belum diuji Syahadah 1. Diperlukan pekan khusus ujian Syahadah.
            </p>
          </div>
          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-emerald-200 dark:border-emerald-800 shadow-sm">
            <div class="font-bold text-slate-900 dark:text-white mb-1 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-rose-500"></span>
              Fokus Penguatan Juz 1 & 2
            </div>
            <p class="text-slate-600 dark:text-slate-300 text-xs leading-relaxed">
              Juz 1 dan 2 tercatat 321 kali mengalami kendala di laporan Sabtu dan tes kelancaran. Diperlukan program "Takhassus Al-Baqarah" agar pondasi hafalan santri tidak goyah saat melaju ke juz berikutnya.
            </p>
          </div>
          <div class="bg-white dark:bg-slate-900 p-4 rounded-xl border border-emerald-200 dark:border-emerald-800 shadow-sm">
            <div class="font-bold text-slate-900 dark:text-white mb-1 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              Pendampingan Intensif Kelas 1
            </div>
            <p class="text-slate-600 dark:text-slate-300 text-xs leading-relaxed">
              Santri Kelas 1 (Ula) saat ini stabil dengan rata-rata 3 juz (Juz 30 & 29). Target semester berikutnya adalah menuntaskan Juz 1, 2, dan 3 agar siap menyusul Syahadah 1 bersama.
            </p>
          </div>
        </div>
      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 2: LAPORAN SYAHADAH -->
    <!-- ========================================================================================= -->
    <section id="content-syahadah" class="tab-content hidden space-y-6">
      
      <!-- Syahadah Header Info -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800 mb-2">
              <i data-lucide="award" class="w-3.5 h-3.5"></i>
              Ujian Akbar Mutqin 5-Juz
            </div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Laporan Khusus Syahadah Santri</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-3xl">
              Syahadah adalah ujian puncak kelayakan mutqin yang disimak langsung oleh dewan penguji tahfidz pesantren secara akumulatif per 5 juz dalam sekali duduk. 
              Berikut adalah rincian siapa saja yang telah lulus, tingkatan yang diraih, nilai predikat, serta daftar santri yang belum mengambil syahadah.
            </p>
          </div>
          <!-- Syahadah Quick Stats Pill -->
          <div class="flex items-center gap-2 bg-slate-50 dark:bg-slate-800/80 p-3 rounded-xl border border-slate-200 dark:border-slate-700">
            <div class="text-center px-3 border-r border-slate-200 dark:border-slate-700">
              <div class="text-xs text-slate-400">Telah Syahadah</div>
              <div class="text-xl font-bold text-amber-600 dark:text-amber-400">26 Santri</div>
            </div>
            <div class="text-center px-3 border-r border-slate-200 dark:border-slate-700">
              <div class="text-xs text-slate-400">Total Sertifikat</div>
              <div class="text-xl font-bold text-emerald-600 dark:text-emerald-400">29 Event</div>
            </div>
            <div class="text-center px-3">
              <div class="text-xs text-slate-400">Belum Syahadah</div>
              <div class="text-xl font-bold text-slate-600 dark:text-slate-300">89 Santri</div>
            </div>
          </div>
        </div>

        <!-- 4 Tiers of Syahadah Achieved Overview -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-slate-100 dark:border-slate-800">
          <div class="p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800">
            <div class="text-xs text-amber-800 dark:text-amber-300 font-semibold">Syahadah 1 (5 Juz)</div>
            <div class="text-2xl font-black text-amber-700 dark:text-amber-400 mt-1">12 <span class="text-xs font-normal text-amber-600">Santri</span></div>
            <div class="text-[11px] text-amber-700/80 dark:text-amber-300/80 mt-1">Juz 30, 29, 1, 2, 3</div>
          </div>
          <div class="p-3.5 rounded-xl bg-teal-50 dark:bg-teal-950/40 border border-teal-200 dark:border-teal-800">
            <div class="text-xs text-teal-800 dark:text-teal-300 font-semibold">Syahadah 2 (10 Juz)</div>
            <div class="text-2xl font-black text-teal-700 dark:text-teal-400 mt-1">10 <span class="text-xs font-normal text-teal-600">Santri</span></div>
            <div class="text-[11px] text-teal-700/80 dark:text-teal-300/80 mt-1">Juz 4, 5, 6, 7, 8</div>
          </div>
          <div class="p-3.5 rounded-xl bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800">
            <div class="text-xs text-blue-800 dark:text-blue-300 font-semibold">Syahadah 3 (15 Juz)</div>
            <div class="text-2xl font-black text-blue-700 dark:text-blue-400 mt-1">4 <span class="text-xs font-normal text-blue-600">Santri</span></div>
            <div class="text-[11px] text-blue-700/80 dark:text-blue-300/80 mt-1">Juz 9, 10, 11, 12, 13</div>
          </div>
          <div class="p-3.5 rounded-xl bg-purple-50 dark:bg-purple-950/40 border border-purple-200 dark:border-purple-800">
            <div class="text-xs text-purple-800 dark:text-purple-300 font-semibold">Syahadah 4 (20 Juz)</div>
            <div class="text-2xl font-black text-purple-700 dark:text-purple-400 mt-1">3 <span class="text-xs font-normal text-purple-600">Santri</span></div>
            <div class="text-[11px] text-purple-700/80 dark:text-purple-300/80 mt-1">Juz 14, 15, 16, 17, 18</div>
          </div>
        </div>

      </div>

      <!-- SYAHADAH SUB-TABS -->
      <div class="flex items-center gap-2 border-b border-slate-200 dark:border-slate-800 pb-2 overflow-x-auto no-print">
        <button onclick="filterSyahadahTab('semua')" id="subtab-sy-semua" class="subtab-btn active px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white transition">
          Semua Lulusan Syahadah (29)
        </button>
        <button onclick="filterSyahadahTab('keempat')" id="subtab-sy-keempat" class="subtab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
          Syahadah 4 (20 Juz) - 3 Santri
        </button>
        <button onclick="filterSyahadahTab('ketiga')" id="subtab-sy-ketiga" class="subtab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
          Syahadah 3 (15 Juz) - 4 Santri
        </button>
        <button onclick="filterSyahadahTab('kedua')" id="subtab-sy-kedua" class="subtab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
          Syahadah 2 (10 Juz) - 10 Santri
        </button>
        <button onclick="filterSyahadahTab('pertama')" id="subtab-sy-pertama" class="subtab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition">
          Syahadah 1 (5 Juz) - 12 Santri
        </button>
        <button onclick="filterSyahadahTab('belum_siap')" id="subtab-sy-belum-siap" class="subtab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold text-amber-700 bg-amber-50 dark:bg-amber-950 dark:text-amber-300 hover:bg-amber-100 transition">
          Belum Syahadah: Siap Ujian (20 Santri)
        </button>
        <button onclick="filterSyahadahTab('belum_proses')" id="subtab-sy-belum-proses" class="subtab-btn px-3.5 py-1.5 rounded-lg text-xs font-semibold text-blue-700 bg-blue-50 dark:bg-blue-950 dark:text-blue-300 hover:bg-blue-100 transition">
          Belum Syahadah: Berproses (17 Santri)
        </button>
      </div>

      <!-- SYAHADAH DATA TABLE -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div class="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-900/50">
          <div>
            <h3 class="font-bold text-slate-900 dark:text-white text-sm" id="syahadah-table-title">Daftar Santri Pemegang Sertifikasi Syahadah</h3>
            <p class="text-xs text-slate-500" id="syahadah-table-subtitle">Menampilkan riwayat ujian akbar resmi 5 juz yang telah diselesaikan santri</p>
          </div>
          <div class="text-xs text-slate-500 font-medium" id="syahadah-table-count">
            Total 29 Catatan
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs sm:text-sm">
            <thead class="bg-slate-100/70 dark:bg-slate-800/70 text-slate-600 dark:text-slate-300 uppercase text-[11px] font-bold tracking-wider">
              <tr>
                <th class="py-3 px-4">Santri</th>
                <th class="py-3 px-4">Kelas & Halaqah</th>
                <th class="py-3 px-4">Tingkat Syahadah</th>
                <th class="py-3 px-4">Juz Diuji</th>
                <th class="py-3 px-4">Predikat & Nilai</th>
                <th class="py-3 px-4">Penguji & Tanggal</th>
                <th class="py-3 px-4">Catatan Evaluasi</th>
                <th class="py-3 px-4 text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800" id="syahadah-table-body">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- DETAILED BREAKDOWN: SIAPA SAJA YANG BELUM SYAHADAH? -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Kolom 1: Siap Ujian (>= 5 Juz tapi belum syahadah) -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-amber-200 dark:border-amber-900/50 shadow-sm">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300 flex items-center justify-center font-bold">
              <i data-lucide="bell-ring" class="w-4 h-4"></i>
            </div>
            <div>
              <h3 class="font-bold text-slate-900 dark:text-white text-sm">Prioritas Ujian: Hafalan Sudah &ge;5 Juz</h3>
              <p class="text-xs text-slate-500">Santri yang telah memenuhi syarat kuantitas juz untuk Syahadah 1</p>
            </div>
          </div>
          <p class="text-xs text-slate-600 dark:text-slate-300 mb-4 bg-amber-50 dark:bg-amber-950/30 p-3 rounded-xl border border-amber-200 dark:border-amber-900/60 leading-relaxed">
            Santri-santri ini telah menyetorkan 5 hingga 15 juz namun belum tercatat mengambil ujian resmi Syahadah. 
            Direkomendasikan agar musyrif segera mengagendakan simulasi dan ujian syahadah resmi.
          </p>
          <div class="space-y-2.5 max-h-96 overflow-y-auto pr-1" id="list-syahadah-ready">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- Kolom 2: Analisis Belum Syahadah per Jenjang Kelas -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm">
          <div class="flex items-center gap-2 mb-3">
            <div class="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300 flex items-center justify-center font-bold">
              <i data-lucide="pie-chart" class="w-4 h-4"></i>
            </div>
            <div>
              <h3 class="font-bold text-slate-900 dark:text-white text-sm">Distribusi Belum Syahadah per Kelas</h3>
              <p class="text-xs text-slate-500">Mengapa santri di tiap kelas belum syahadah dan target berikutnya</p>
            </div>
          </div>

          <div class="space-y-3 mt-4 text-xs">
            <!-- Kelas 1 -->
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
              <div class="flex justify-between font-bold text-slate-900 dark:text-white">
                <span>Kelas 1 (Ula - Angkatan 2026)</span>
                <span class="text-slate-500">11 dari 11 Belum Syahadah (100%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px]">
                <strong>Alasan wajar:</strong> Santri baru tingkat pertama. Rata-rata capaian 3 Juz (Juz 30 & 29). Sedang menuntaskan Juz 1, 2, dan 3 menuju target Syahadah 1 di semester genap.
              </p>
            </div>

            <!-- Kelas 2 -->
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
              <div class="flex justify-between font-bold text-slate-900 dark:text-white">
                <span>Kelas 2 (Wustho - Angkatan 2025)</span>
                <span class="text-amber-600 dark:text-amber-400">8 dari 16 Belum Syahadah (50%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px]">
                <strong>Kondisi:</strong> 4 santri sudah mencapai 5 juz dan siap ujian (Ammar Maududi, Aina Talita, Erina Liyana, Nur Humaira). 4 santri lainnya sedang menyelesaikan Juz 2 dan 3.
              </p>
            </div>

            <!-- Kelas 3 -->
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
              <div class="flex justify-between font-bold text-slate-900 dark:text-white">
                <span>Kelas 3 (Ulya - Angkatan 2024)</span>
                <span class="text-emerald-600 dark:text-emerald-400">6 dari 17 Belum Syahadah (35%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px]">
                <strong>Kondisi:</strong> 5 santri sudah mencapai 10-15 juz (M. Alvin [15 juz], M. Rizky [10 juz], Yusuf Kamil [10 juz], Sabila Farrah [10 juz], Khalid Fayyadh [5 juz]). Mereka sangat siap diuji!
              </p>
            </div>

            <!-- Angkatan 2023 -->
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
              <div class="flex justify-between font-bold text-slate-900 dark:text-white">
                <span>Angkatan 2023 (Senior)</span>
                <span class="text-purple-600 dark:text-purple-400">13 dari 20 Belum Syahadah (65%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px]">
                <strong>Kondisi:</strong> 11 santri memiliki hafalan antara 5 hingga 15 juz (Wildan Akhram [15 juz], Audrey Callysta [10 juz], Ahmad Kholish [10 juz], dll).
              </p>
            </div>

          </div>
        </div>

      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 3: STATUS KELANCARAN -->
    <!-- ========================================================================================= -->
    <section id="content-kelancaran" class="tab-content hidden space-y-6">
      
      <!-- Kelancaran Header Info -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-300 border border-teal-300 dark:border-teal-800 mb-2">
              <i data-lucide="check-check" class="w-3.5 h-3.5"></i>
              Uji Mutqin & Laporan Evaluasi Sabtu
            </div>
            <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Analisis Kelancaran Hafalan Santri</h2>
            <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-3xl">
              "Menghafal itu mudah, menjaganya yang butuh perjuangan." 
              Di sistem kita, kelancaran hafalan dinilai melalui dua indikator nyata: 
              <strong>Ujian Tes 1 Juz Utuh</strong> (kelulusan mutqin) dan <strong>Laporan Evaluasi Sabtu</strong> (pendeteksian ayat/halaman yang rapuh).
            </p>
          </div>
          <!-- Kelancaran Pill -->
          <div class="flex items-center gap-2 bg-slate-50 dark:bg-slate-800/80 p-3 rounded-xl border border-slate-200 dark:border-slate-700">
            <div class="text-center px-3 border-r border-slate-200 dark:border-slate-700">
              <div class="text-xs text-slate-400">Total Uji Tes</div>
              <div class="text-xl font-bold text-slate-800 dark:text-slate-100">221 Kali</div>
            </div>
            <div class="text-center px-3 border-r border-slate-200 dark:border-slate-700">
              <div class="text-xs text-slate-400">Lulus Lancar</div>
              <div class="text-xl font-bold text-emerald-600 dark:text-emerald-400">116 Juz</div>
            </div>
            <div class="text-center px-3">
              <div class="text-xs text-slate-400">Perlu Remidi</div>
              <div class="text-xl font-bold text-rose-600 dark:text-rose-400">105 Ujian</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2 TABLES: SIAPA SAJA YANG LANCAR vs YANG TIDAK LANCAR -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        <!-- Table 1: Siapa yang Lancar? (Santri Teruji Mutqin) -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
          <div class="p-4 border-b border-slate-200 dark:border-slate-800 bg-emerald-50/50 dark:bg-emerald-950/20 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <h3 class="font-bold text-slate-900 dark:text-white text-sm">Santri dengan Hafalan Lancar Terbanyak</h3>
            </div>
            <span class="text-xs text-emerald-700 dark:text-emerald-400 font-semibold">Tuntas Tes Musyrif</span>
          </div>
          <div class="p-3 overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="text-slate-500 uppercase text-[10px] font-bold border-b border-slate-100 dark:border-slate-800">
                <tr>
                  <th class="py-2 px-3">Santri</th>
                  <th class="py-2 px-3">Kelas / Halaqah</th>
                  <th class="py-2 px-3">Juz Lancar</th>
                  <th class="py-2 px-3">Daftar Juz Mutqin</th>
                  <th class="py-2 px-3 text-center">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-800" id="table-fluent-students">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Table 2: Siapa yang Belum Lancar? (Perlu Bimbingan & Remidi) -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
          <div class="p-4 border-b border-slate-200 dark:border-slate-800 bg-rose-50/50 dark:bg-rose-950/20 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              <h3 class="font-bold text-slate-900 dark:text-white text-sm">Santri yang Memerlukan Penguatan & Remidi</h3>
            </div>
            <span class="text-xs text-rose-700 dark:text-rose-400 font-semibold">Catatan Evaluasi</span>
          </div>
          <div class="p-3 overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="text-slate-500 uppercase text-[10px] font-bold border-b border-slate-100 dark:border-slate-800">
                <tr>
                  <th class="py-2 px-3">Santri</th>
                  <th class="py-2 px-3">Kelas / Halaqah</th>
                  <th class="py-2 px-3">Juz Belum Lulus</th>
                  <th class="py-2 px-3">Catatan Sabtu</th>
                  <th class="py-2 px-3 text-center">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-800" id="table-need-attention-students">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ANALISIS KENDALA PER JUZ AL-QURAN -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h3 class="font-bold text-slate-900 dark:text-white text-base">Peta Kesulitan & Kendala Seluruh 30 Juz</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Juz mana saja yang paling sering mengalami kebuntuan atau tidak lulus tes</p>
          </div>
          <div class="flex items-center gap-2 text-xs">
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 font-medium">
              <span class="w-2 h-2 rounded-full bg-rose-500"></span>
              Paling Sering Macet: Juz 1, 2, 29, 3
            </span>
          </div>
        </div>

        <div class="relative h-72">
          <canvas id="chartJuzIssuesFull"></canvas>
        </div>

        <!-- Layman Explanation of why certain juz are difficult -->
        <div class="mt-6 pt-5 border-t border-slate-100 dark:border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-600 dark:text-slate-300">
          <div class="bg-slate-50 dark:bg-slate-800/60 p-3.5 rounded-xl border border-slate-200 dark:border-slate-700">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">Mengapa Juz 2 Paling Sering Macet (165x)?</h4>
            <p class="text-[11px] leading-relaxed">
              Juz 2 memuat hukum syariat yang padat di Surah Al-Baqarah (kiblat, haji, puasa, qishash) serta banyak ayat mutasyabihat (ujung ayat yang mirip). Santri mudah tertukar jika tidak diiringi pemahaman makna ayat.
            </p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800/60 p-3.5 rounded-xl border border-slate-200 dark:border-slate-700">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">Mengapa Juz 1 Menantang (156x)?</h4>
            <p class="text-[11px] leading-relaxed">
              Juz 1 adalah gerbang awal Al-Quran besar setelah juz 30 dan 29. Transisi dari surah-surah pendek ke kisah panjang Bani Israil membutuhkan daya tahan nafas dan konsentrasi tinggi.
            </p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800/60 p-3.5 rounded-xl border border-slate-200 dark:border-slate-700">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">Mengapa Juz 29 Sering Rapuh (138x)?</h4>
            <p class="text-[11px] leading-relaxed">
              Juz 29 memiliki 11 surah dengan irama fawashil (akhiran) yang beragam namun ritmenya rapat (Al-Mulk s.d. Al-Mursalat). Jika jarang di-murajaah, awalan ayat di surah Al-Qalam, Al-Ma'arij, dan Al-Jin mudah terlupa.
            </p>
          </div>
        </div>

      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 4: GROUPING KELAS & HALAQAH -->
    <!-- ========================================================================================= -->
    <section id="content-grouping" class="tab-content hidden space-y-6">
      
      <!-- Grouping Header -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 mb-2">
          <i data-lucide="layers" class="w-3.5 h-3.5"></i>
          Struktur & Pengelompokan Pembinaan
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Grouping Berdasarkan Jenjang Kelas & Halaqah Musyrif</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-3xl">
          Setiap santri di pesantren dibina dalam struktur kelas berjenjang (Ula, Wustho, Ulya) dan dibimbing secara personal dalam kelompok halaqah kecil oleh musyrif/musyrifah. 
          Berikut adalah evaluasi perbandingan kinerja tiap jenjang dan halaqah.
        </p>
      </div>

      <!-- SECTION 1: PER JENJANG KELAS -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <i data-lucide="graduation-cap" class="w-5 h-5 text-emerald-600"></i>
            Analisis Capaian per Jenjang Kelas
          </h3>
          <span class="text-xs text-slate-500">Klik kelas untuk memfilter daftar santri</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4" id="cards-classes-grid">
          <!-- Dynamically populated -->
        </div>
      </div>

      <!-- SECTION 2: PER HALAQAH / MUSYRIF -->
      <div class="space-y-4 pt-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="users" class="w-5 h-5 text-teal-600"></i>
              Analisis Capaian per Halaqah Musyrif
            </h3>
            <p class="text-xs text-slate-500">6 Halaqah aktif pengampu harian para santri</p>
          </div>
          <span class="text-xs text-slate-500">Rasio kelulusan & rata-rata juz</span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="cards-halaqah-grid">
          <!-- Dynamically populated -->
        </div>
      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 5: DIREKTORI & DETAIL SANTRI -->
    <!-- ========================================================================================= -->
    <section id="content-santri" class="tab-content hidden space-y-6">
      
      <!-- Filter & Search Controls -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 class="text-lg font-bold text-slate-900 dark:text-white flex items-center gap-2">
              <i data-lucide="search" class="w-5 h-5 text-emerald-600"></i>
              Direktori & Profil Seluruh Santri
            </h2>
            <p class="text-xs text-slate-500 dark:text-slate-400">Cari dan filter data santri secara instan berdasarkan kriteria apa pun</p>
          </div>
          <button onclick="resetFilters()" class="text-xs font-semibold text-rose-600 dark:text-rose-400 hover:underline flex items-center gap-1 self-start sm:self-auto">
            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
            Reset Filter
          </button>
        </div>

        <!-- Filter Inputs Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          
          <!-- Search box -->
          <div class="lg:col-span-2 relative">
            <label class="block text-[11px] font-semibold text-slate-600 dark:text-slate-300 mb-1">Cari Nama / NIS / NIK</label>
            <div class="relative">
              <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Ketik nama santri..."
                class="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-2.5"></i>
            </div>
          </div>

          <!-- Filter Kelas -->
          <div>
            <label class="block text-[11px] font-semibold text-slate-600 dark:text-slate-300 mb-1">Kelas / Angkatan</label>
            <select id="filterKelas" onchange="applyFilters()"
              class="w-full py-2 px-3 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="semua">Semua Kelas</option>
              <option value="kelas_1">Kelas 1 (Ula)</option>
              <option value="kelas_2">Kelas 2 (Wustho)</option>
              <option value="kelas_3">Kelas 3 (Ulya)</option>
              <option value="angkatan_2023">Angkatan 2023 (Senior)</option>
              <option value="alumni">Alumni (2020-2022)</option>
            </select>
          </div>

          <!-- Filter Halaqah -->
          <div>
            <label class="block text-[11px] font-semibold text-slate-600 dark:text-slate-300 mb-1">Halaqah Musyrif</label>
            <select id="filterHalaqah" onchange="applyFilters()"
              class="w-full py-2 px-3 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="semua">Semua Halaqah</option>
              <!-- Populated by JS -->
            </select>
          </div>

          <!-- Filter Syahadah -->
          <div>
            <label class="block text-[11px] font-semibold text-slate-600 dark:text-slate-300 mb-1">Status Syahadah</label>
            <select id="filterSyahadah" onchange="applyFilters()"
              class="w-full py-2 px-3 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="semua">Semua Status</option>
              <option value="sudah_syahadah">Sudah Lulus Syahadah</option>
              <option value="siap_syahadah">Siap Ujian (>= 5 Juz)</option>
              <option value="berproses">Sedang Berproses (1-4 Juz)</option>
              <option value="belum_syahadah">Belum Syahadah (Semua)</option>
            </select>
          </div>

          <!-- Filter Kelancaran -->
          <div>
            <label class="block text-[11px] font-semibold text-slate-600 dark:text-slate-300 mb-1">Kelancaran</label>
            <select id="filterKelancaran" onchange="applyFilters()"
              class="w-full py-2 px-3 text-xs rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="semua">Semua Kelancaran</option>
              <option value="mutqin">Sangat Lancar (Mutqin)</option>
              <option value="mayoritas">Mayoritas Lancar</option>
              <option value="perhatian">Perlu Perhatian / Remidi</option>
              <option value="proses">Dalam Proses Setoran</option>
            </select>
          </div>

        </div>

        <!-- Filter Count Pill -->
        <div class="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100 dark:border-slate-800">
          <span>Menampilkan <strong id="filterResultCount" class="text-slate-900 dark:text-white">115</strong> dari 115 santri</span>
          <span class="text-[11px] text-slate-400">Klik nama santri atau tombol aksi untuk membuka Rapor 30 Juz</span>
        </div>
      </div>

      <!-- Santri Data Table -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs sm:text-sm">
            <thead class="bg-slate-100/70 dark:bg-slate-800/70 text-slate-600 dark:text-slate-300 uppercase text-[11px] font-bold tracking-wider cursor-pointer select-none">
              <tr>
                <th class="py-3 px-4" onclick="sortSantriTable('nama')">
                  <div class="flex items-center gap-1.5">
                    <span>Santri</span>
                    <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i>
                  </div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('kelas')">
                  <div class="flex items-center gap-1.5">
                    <span>Kelas & Angkatan</span>
                    <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i>
                  </div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('halaqah')">
                  <div class="flex items-center gap-1.5">
                    <span>Halaqah Musyrif</span>
                    <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i>
                  </div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('juz_dicapai')">
                  <div class="flex items-center gap-1.5">
                    <span>Juz Dicapai</span>
                    <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i>
                  </div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('juz_lancar')">
                  <div class="flex items-center gap-1.5">
                    <span>Juz Lancar</span>
                    <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i>
                  </div>
                </th>
                <th class="py-3 px-4">Syahadah</th>
                <th class="py-3 px-4">Status Kelancaran</th>
                <th class="py-3 px-4 text-center">Rapor / Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800" id="santriTableBody">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 6: PANDUAN AWAM & GLOSARIUM -->
    <!-- ========================================================================================= -->
    <section id="content-panduan" class="tab-content hidden space-y-6">
      
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800 mb-2">
          <i data-lucide="book-marked" class="w-3.5 h-3.5"></i>
          Panduan Lengkap untuk Orang Awam & Wali Santri
        </div>
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Memahami Sistem & Istilah Tahfidz Al-Quran</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1 max-w-3xl">
          Agar orang tua dan masyarakat awam tidak bingung dengan istilah teknis di pondok, berikut adalah panduan sederhana mengenai alur belajar, arti istilah, standar penilaian, dan cara menyikapi laporan ini.
        </p>
      </div>

      <!-- ALUR BELAJAR FLOWCHART -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 class="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
          <i data-lucide="git-branch" class="w-5 h-5 text-emerald-600"></i>
          Alur Perjalanan Menghafal Al-Quran di Pesantren Kita
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-5 gap-3 text-xs">
          
          <!-- Step 1 -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 relative">
            <div class="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center text-xs mb-2">1</div>
            <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-1">Ziyadah Harian</h4>
            <p class="text-slate-500 leading-relaxed text-[11px]">
              Santri menyetorkan hafalan ayat/halaman baru setiap hari (halaman 1A s.d. 10B). Target umum: 0,5 sampai 1 halaman per hari.
            </p>
          </div>

          <!-- Step 2 -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 relative">
            <div class="w-6 h-6 rounded-full bg-teal-600 text-white font-bold flex items-center justify-center text-xs mb-2">2</div>
            <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-1">Setengah Juz</h4>
            <p class="text-slate-500 leading-relaxed text-[11px]">
              Setelah hafal 10 halaman (1A-5B atau 6A-10B), santri menyetorkan 10 halaman sekaligus dalam sekali duduk untuk menguji ketahanan.
            </p>
          </div>

          <!-- Step 3 -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 relative">
            <div class="w-6 h-6 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-xs mb-2">3</div>
            <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-1">Ujian Juziyah (1 Juz)</h4>
            <p class="text-slate-500 leading-relaxed text-[11px]">
              Ujian formal 1 juz utuh (20 halaman) dari awal sampai akhir juz di hadapan musyrif. Menentukan kelulusan juz tersebut.
            </p>
          </div>

          <!-- Step 4 -->
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 relative">
            <div class="w-6 h-6 rounded-full bg-purple-600 text-white font-bold flex items-center justify-center text-xs mb-2">4</div>
            <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-1">Ujian Tes Kelancaran</h4>
            <p class="text-slate-500 leading-relaxed text-[11px]">
              Tes sambung ayat dan kelancaran untuk memastikan juz yang sudah dihafal tidak luntur (status: Lancar vs Perlu Remidi).
            </p>
          </div>

          <!-- Step 5 -->
          <div class="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800 relative">
            <div class="w-6 h-6 rounded-full bg-amber-500 text-white font-bold flex items-center justify-center text-xs mb-2">5</div>
            <h4 class="font-bold text-amber-900 dark:text-amber-200 text-sm mb-1">Ujian Akbar Syahadah</h4>
            <p class="text-amber-800/80 dark:text-amber-300/80 leading-relaxed text-[11px]">
              Ujian puncak 5 juz berturut-turut dalam sekali duduk tanpa mushaf. Menghasilkan sertifikat mutqin berpredikat (Mumtaz s.d. Maqbul).
            </p>
          </div>

        </div>
      </div>

      <!-- GLOSARIUM KATA / ISTILAH PENTING -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Kolom Istilah Kurikulum -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
            <i data-lucide="book" class="w-5 h-5 text-emerald-600"></i>
            Kamus Istilah Tahfidz (Glosarium)
          </h3>

          <div class="space-y-3 text-xs">
            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
              <strong class="text-emerald-700 dark:text-emerald-400 text-sm">Ziyadah:</strong>
              <p class="text-slate-600 dark:text-slate-300 mt-1">
                Artinya "penambahan". Yaitu setoran hafalan baru per lembar/halaman Al-Quran dari santri kepada musyrif.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
              <strong class="text-emerald-700 dark:text-emerald-400 text-sm">Murajaah:</strong>
              <p class="text-slate-600 dark:text-slate-300 mt-1">
                Artinya "mengulang kembali". Kegiatan menyimak atau mengulang hafalan-hafalan lama yang telah disetorkan agar tetap melekat kuat di memori.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
              <strong class="text-emerald-700 dark:text-emerald-400 text-sm">Mutqin:</strong>
              <p class="text-slate-600 dark:text-slate-300 mt-1">
                Hafalan yang sangat kokoh, lancar di luar kepala, fasih makhraj tajwidnya, dan tidak terbata-bata saat diuji sambung ayat acak.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
              <strong class="text-emerald-700 dark:text-emerald-400 text-sm">Syahadah:</strong>
              <p class="text-slate-600 dark:text-slate-300 mt-1">
                Artinya "kesaksian/sertifikasi". Ujian resmi kelipatan 5 Juz (5, 10, 15, 20, 25, 30 Juz) yang disaksikan penguji berkompeten.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
              <strong class="text-emerald-700 dark:text-emerald-400 text-sm">Urutan 30, 29, 1 s.d. 28:</strong>
              <p class="text-slate-600 dark:text-slate-300 mt-1">
                Metode tahfidz di pondok mendahulukan Juz 30 (Juz 'Amma) dan Juz 29 (Tabarak) karena surahnya sering dibaca dalam shalat, baru kemudian memulai Juz 1 (Al-Baqarah) sampai tuntas Juz 28.
              </p>
            </div>
          </div>
        </div>

        <!-- Kolom Standar Nilai Pesantren -->
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 class="font-bold text-slate-900 dark:text-white text-base flex items-center gap-2">
            <i data-lucide="check-circle-2" class="w-5 h-5 text-emerald-600"></i>
            Standar Predikat Nilai Pesantren
          </h3>

          <div class="space-y-3 text-xs">
            <div class="p-3 rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800">
              <div class="flex items-center justify-between font-bold text-emerald-800 dark:text-emerald-300">
                <span class="text-sm">Mumtaz (ممتاز) - Istimewa</span>
                <span>0 - 10 Kesalahan</span>
              </div>
              <p class="text-emerald-700/80 dark:text-emerald-400/80 mt-1 text-[11px]">
                Hafalan sangat sempurna. Makhraj, shifat huruf, mad, dan dengung ditunaikan dengan sangat teliti.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-800">
              <div class="flex items-center justify-between font-bold text-blue-800 dark:text-blue-300">
                <span class="text-sm">Jayyid Jiddan (جيد جداً) - Sangat Baik</span>
                <span>11 - 20 Kesalahan</span>
              </div>
              <p class="text-blue-700/80 dark:text-blue-400/80 mt-1 text-[11px]">
                Hafalan lancar dan kokoh dengan sedikit koreksi harakat atau waqaf yang tidak fatal.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800">
              <div class="flex items-center justify-between font-bold text-amber-800 dark:text-amber-300">
                <span class="text-sm">Jayyid (جيد) - Baik</span>
                <span>21 - 30 Kesalahan</span>
              </div>
              <p class="text-amber-700/80 dark:text-amber-400/80 mt-1 text-[11px]">
                Lulus standar hafalan. Perlu pengulangan mandiri di beberapa halaman yang sempat tersendat.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-orange-50 dark:bg-orange-950/40 border border-orange-200 dark:border-orange-800">
              <div class="flex items-center justify-between font-bold text-orange-800 dark:text-orange-300">
                <span class="text-sm">Maqbul (مقبول) - Cukup / Lulus Bersyarat</span>
                <span>31 - 40 Kesalahan</span>
              </div>
              <p class="text-orange-700/80 dark:text-orange-400/80 mt-1 text-[11px]">
                Lulus bersyarat dengan kewajiban murajaah intensif sebelum diizinkan menambah juz baru.
              </p>
            </div>

            <div class="p-3 rounded-lg bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800">
              <div class="flex items-center justify-between font-bold text-rose-800 dark:text-rose-300">
                <span class="text-sm">Mardud (مردود) - Tidak Lulus / Remidi</span>
                <span>> 40 Kesalahan</span>
              </div>
              <p class="text-rose-700/80 dark:text-rose-400/80 mt-1 text-[11px]">
                Hafalan belum memenuhi standar minimal. Wajib mengikuti program karantina murajaah dan mengulang ujian.
              </p>
            </div>
          </div>
        </div>

      </div>

      <!-- TIPS UNTUK WALI SANTRI -->
      <div class="bg-gradient-to-r from-teal-50 to-emerald-50 dark:from-teal-950/30 dark:to-emerald-950/30 p-6 rounded-2xl border border-teal-200 dark:border-teal-800">
        <h3 class="font-bold text-teal-900 dark:text-teal-200 text-base mb-3 flex items-center gap-2">
          <i data-lucide="heart" class="w-5 h-5 text-rose-500"></i>
          Pesan & Tips untuk Ayah/Bunda Wali Santri
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-teal-950 dark:text-teal-200">
          <div class="bg-white/80 dark:bg-slate-900/80 p-4 rounded-xl border border-teal-100 dark:border-teal-900">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">1. Apresiasi Proses, Bukan Hanya Jumlah</h4>
            <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
              Santri yang baru mencapai 3 juz dengan lancar sama mulianya dengan santri yang hafal 10 juz. Jangan bandingkan capaian anak Anda dengan santri lain, karena tiap anak memiliki ritme menghafal yang unik.
            </p>
          </div>
          <div class="bg-white/80 dark:bg-slate-900/80 p-4 rounded-xl border border-teal-100 dark:border-teal-900">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">2. Dukung saat Mengulang / Remidi</h4>
            <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
              Jika ananda tercatat "Perlu Remidi" di suatu juz, jangan berkecil hati. Remidi adalah bentuk kasih sayang musyrif agar hafalan ananda tidak hilang di kemudian hari.
            </p>
          </div>
          <div class="bg-white/80 dark:bg-slate-900/80 p-4 rounded-xl border border-teal-100 dark:border-teal-900">
            <h4 class="font-bold text-slate-900 dark:text-white mb-1">3. Jaga Suasana saat Liburan</h4>
            <p class="text-slate-600 dark:text-slate-300 text-[11px] leading-relaxed">
              Saat ananda pulang liburan ke rumah, luangkan waktu 15-30 menit setelah shalat untuk menyimak hafalan juz yang sudah dicapai, terutama juz-juz yang tercatat di laporan Sabtu.
            </p>
          </div>
        </div>
      </div>

    </section>

  </main>

  <!-- ========================================================================================= -->
  <!-- MODAL: RAPOR & DETAIL SANTRI (30 JUZ VISUAL GRID) -->
  <!-- ========================================================================================= -->
  <div id="santriModal" class="fixed inset-0 z-50 bg-slate-950/70 backdrop-blur-sm hidden flex items-center justify-center p-4 overflow-y-auto no-print">
    <div class="bg-white dark:bg-slate-900 rounded-3xl max-w-4xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden transform transition-all duration-200 scale-95" id="santriModalCard">
      
      <!-- Modal Header -->
      <div class="p-5 sm:p-6 border-b border-slate-200 dark:border-slate-800 bg-gradient-to-r from-emerald-800 to-teal-900 text-white flex items-center justify-between relative">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-2xl bg-white/10 backdrop-blur border border-white/20 flex items-center justify-center text-white text-2xl font-bold font-arabic shadow-inner" id="modal-avatar">
            س
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-xl font-bold text-white" id="modal-nama">Nama Santri</h3>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/20 text-white border border-white/30" id="modal-status">Aktif</span>
            </div>
            <div class="flex flex-wrap items-center gap-2 text-xs text-emerald-200 mt-1">
              <span id="modal-nis">NIS: -</span>
              <span>•</span>
              <span id="modal-kelas">Kelas: -</span>
              <span>•</span>
              <span id="modal-halaqah">Halaqah: -</span>
              <span>•</span>
              <span id="modal-jk">Gender</span>
            </div>
          </div>
        </div>
        <button onclick="closeSantriModal()" class="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center transition border border-white/10">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Modal Body (Scrollable) -->
      <div class="p-6 overflow-y-auto space-y-6 text-slate-800 dark:text-slate-100 flex-1">
        
        <!-- 4 Summary Stat Mini-Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
            <span class="text-xs text-slate-500 dark:text-slate-400">Total Juz Dicapai</span>
            <div class="text-xl font-bold text-emerald-600 dark:text-emerald-400 mt-1" id="modal-juz-dicapai">0 Juz</div>
            <span class="text-[10px] text-slate-400">Ziyadah diselesaikan</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
            <span class="text-xs text-slate-500 dark:text-slate-400">Juz Teruji Lancar</span>
            <div class="text-xl font-bold text-teal-600 dark:text-teal-400 mt-1" id="modal-juz-lancar">0 Juz</div>
            <span class="text-[10px] text-slate-400">Mutqin lolos tes</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
            <span class="text-xs text-slate-500 dark:text-slate-400">Syahadah Diraih</span>
            <div class="text-xl font-bold text-amber-600 dark:text-amber-400 mt-1" id="modal-syahadah-highest">-</div>
            <span class="text-[10px] text-slate-400" id="modal-syahadah-count">0 Sertifikat</span>
          </div>
          <div class="p-3.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
            <span class="text-xs text-slate-500 dark:text-slate-400">Status Kelancaran</span>
            <div class="text-xs font-bold text-slate-800 dark:text-slate-200 mt-1.5" id="modal-fluency-badge">-</div>
            <span class="text-[10px] text-slate-400" id="modal-tidak-lancar-count">0 Catatan kendala</span>
          </div>
        </div>

        <!-- Target Syahadah Progress -->
        <div class="p-4 rounded-xl bg-emerald-50/70 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-800/60">
          <div class="flex items-center justify-between text-xs font-semibold text-emerald-900 dark:text-emerald-200 mb-2">
            <span id="modal-target-title">Target Milestone Berikutnya</span>
            <span id="modal-target-pct">0%</span>
          </div>
          <div class="w-full bg-emerald-200/60 dark:bg-emerald-900/60 rounded-full h-2.5 overflow-hidden">
            <div id="modal-target-bar" class="bg-emerald-600 dark:bg-emerald-400 h-2.5 rounded-full transition-all duration-500" style="width: 0%"></div>
          </div>
          <p class="text-[11px] text-emerald-800/80 dark:text-emerald-300/80 mt-2" id="modal-target-desc">-</p>
        </div>

        <!-- 30-JUZ VISUAL INTERACTIVE GRID -->
        <div>
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
            <div>
              <h4 class="font-bold text-slate-900 dark:text-white text-sm flex items-center gap-2">
                <i data-lucide="layout-grid" class="w-4 h-4 text-emerald-600"></i>
                Peta Visual 30 Juz Santri
              </h4>
              <p class="text-xs text-slate-500">Klik atau arahkan kursor ke tiap juz untuk melihat status kelancaran dan surah</p>
            </div>
            <!-- Grid Legend -->
            <div class="flex flex-wrap items-center gap-2 text-[10px]">
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-emerald-500"></span>Lancar</span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-amber-400"></span>Sudah Hafal (Belum Tes)</span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-rose-500"></span>Tidak Lancar</span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-slate-200 dark:bg-slate-700"></span>Belum Mulai</span>
            </div>
          </div>

          <!-- The 30 Juz Grid -->
          <div class="grid grid-cols-5 sm:grid-cols-6 md:grid-cols-10 gap-2" id="modal-juz-grid">
            <!-- Dynamically populated 30 blocks -->
          </div>
        </div>

        <!-- TABEL RIWAYAT SYAHADAH SANTRI -->
        <div id="modal-syahadah-section">
          <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-2 flex items-center gap-2">
            <i data-lucide="award" class="w-4 h-4 text-amber-500"></i>
            Riwayat Ujian Syahadah
          </h4>
          <div class="space-y-2" id="modal-syahadah-list">
            <!-- Populated -->
          </div>
        </div>

        <!-- CATATAN EVALUASI & REMIDI SABTU -->
        <div id="modal-evaluasi-section">
          <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-2 flex items-center gap-2">
            <i data-lucide="alert-circle" class="w-4 h-4 text-rose-500"></i>
            Catatan Halaman Rapuh (Evaluasi Sabtu)
          </h4>
          <div class="space-y-2" id="modal-evaluasi-list">
            <!-- Populated -->
          </div>
        </div>

        <!-- REKOMENDASI UNTUK SANTRI & WALI -->
        <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200 dark:border-slate-700">
          <h4 class="font-bold text-slate-900 dark:text-white text-xs mb-1.5 flex items-center gap-1.5">
            <i data-lucide="info" class="w-4 h-4 text-emerald-600"></i>
            Rekomendasi Musyrif untuk Santri Ini
          </h4>
          <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed" id="modal-rekomendasi">
            -
          </p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/60 flex items-center justify-between">
        <span class="text-xs text-slate-400">Pesantren Tahfidzul Quran • Sistem Informasi Santri</span>
        <button onclick="closeSantriModal()" class="px-4 py-2 bg-slate-200 dark:bg-slate-800 hover:bg-slate-300 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-semibold rounded-lg transition">
          Tutup Rapor
        </button>
      </div>

    </div>
  </div>

  <!-- FOOTER -->
  <footer class="bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 py-6 mt-12 text-center text-xs text-slate-500 dark:text-slate-400 no-print transition-colors">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <div class="w-6 h-6 rounded-md bg-emerald-600 text-white flex items-center justify-center font-bold text-xs">TQ</div>
        <span class="font-semibold text-slate-700 dark:text-slate-300">Sistem Laporan Capaian Tahfidz Santri</span>
      </div>
      <div>
        <span>Dibuat berdasarkan basis data aktual <code class="font-mono text-emerald-600 dark:text-emerald-400">everynight-in-my-dream.db</code></span>
      </div>
      <div class="text-[11px] text-slate-400">
        Timezone: Asia/Makassar (WITA) • 115 Santri • 540 Juz
      </div>
    </div>
  </footer>

  <!-- EMBEDDED DATASET SCRIPT -->
  <script id="embedded-data" type="application/json">
DATA_JSON_PLACEHOLDER
  </script>

  <!-- JAVASCRIPT APPLICATION CODE -->
  <script>
    // 1. DATA INITIALIZATION
    const rawDataElem = document.getElementById('embedded-data');
    let DB = JSON.parse(rawDataElem.textContent);
    let ALL_SANTRI = DB.santri_list;
    let filteredSantri = [...ALL_SANTRI];
    let currentSort = { column: 'nama', asc: true };

    // 2. THEME HANDLING
    function initTheme() {
      const savedTheme = localStorage.getItem('tahfidz_theme');
      if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        document.getElementById('themeIcon').setAttribute('data-lucide', 'sun');
      } else {
        document.documentElement.classList.remove('dark');
        document.getElementById('themeIcon').setAttribute('data-lucide', 'moon');
      }
    }
    function toggleTheme() {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('tahfidz_theme', isDark ? 'dark' : 'light');
      document.getElementById('themeIcon').setAttribute('data-lucide', isDark ? 'sun' : 'moon');
      lucide.createIcons();
      // Re-render charts for theme colors
      renderAllCharts();
    }

    // 3. TAB SWITCHING
    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-emerald-50', 'text-emerald-700', 'dark:bg-emerald-950/60', 'dark:text-emerald-300', 'border', 'border-emerald-200', 'dark:border-emerald-800/80');
        btn.classList.add('text-slate-600', 'dark:text-slate-400');
      });
      document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));

      const activeBtn = document.getElementById('tab-' + tabId);
      const activeContent = document.getElementById('content-' + tabId);
      if (activeBtn && activeContent) {
        activeBtn.classList.add('active', 'bg-emerald-50', 'text-emerald-700', 'dark:bg-emerald-950/60', 'dark:text-emerald-300', 'border', 'border-emerald-200', 'dark:border-emerald-800/80');
        activeBtn.classList.remove('text-slate-600', 'dark:text-slate-400');
        activeContent.classList.remove('hidden');
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
      lucide.createIcons();
    }

    // 4. POPULATE EXECUTIVE SUMMARY HIGHLIGHTS
    function populateExecutiveHighlights() {
      // Top 5 Achievers
      const topAchievers = [...ALL_SANTRI].sort((a,b) => b.total_juz_dicapai - a.total_juz_dicapai).slice(0, 5);
      const topAchElem = document.getElementById('list-top-achievers');
      topAchElem.innerHTML = topAchievers.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 hover:bg-emerald-50/70 dark:hover:bg-slate-800 cursor-pointer transition border border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-3">
            <span class="w-6 h-6 rounded-full bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 flex items-center justify-center text-xs font-bold">${idx + 1}</span>
            <div>
              <div class="font-bold text-xs text-slate-900 dark:text-white">${s.nama}</div>
              <div class="text-[10px] text-slate-400">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right">
            <div class="font-black text-emerald-600 dark:text-emerald-400 text-sm">${s.total_juz_dicapai} Juz</div>
            <div class="text-[10px] text-slate-400">${s.total_juz_lancar} lancar</div>
          </div>
        </div>
      `).join('');

      // Top 5 Fluent
      const topFluent = [...ALL_SANTRI].sort((a,b) => (b.total_juz_lancar - a.total_juz_lancar) || (b.total_juz_dicapai - a.total_juz_dicapai)).slice(0, 5);
      const topFluElem = document.getElementById('list-top-fluent');
      topFluElem.innerHTML = topFluent.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 hover:bg-emerald-50/70 dark:hover:bg-slate-800 cursor-pointer transition border border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-3">
            <span class="w-6 h-6 rounded-full bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 flex items-center justify-center text-xs font-bold">${idx + 1}</span>
            <div>
              <div class="font-bold text-xs text-slate-900 dark:text-white">${s.nama}</div>
              <div class="text-[10px] text-slate-400">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right">
            <div class="font-black text-teal-600 dark:text-teal-400 text-sm">${s.total_juz_lancar} Juz</div>
            <div class="text-[10px] text-slate-400">${s.total_juz_dicapai} juz dicapai</div>
          </div>
        </div>
      `).join('');

      // Top 5 Challenging Juz
      const juzWithIssues = [...DB.juz_stats].map(j => ({
        ...j,
        total_issues: j.tes_tidak_lancar + j.sabtu_issues
      })).sort((a,b) => b.total_issues - a.total_issues).slice(0, 5);

      const topJuzElem = document.getElementById('list-challenging-juz');
      topJuzElem.innerHTML = juzWithIssues.map(j => `
        <div class="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-3">
            <span class="w-7 h-7 rounded-lg bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 flex items-center justify-center text-xs font-bold">Juz ${j.juz}</span>
            <div>
              <div class="font-bold text-xs text-slate-900 dark:text-white">${j.surah}</div>
              <div class="text-[10px] text-slate-400">${j.hafal_count} santri hafal juz ini</div>
            </div>
          </div>
          <div class="text-right">
            <div class="font-bold text-rose-600 dark:text-rose-400 text-xs">${j.total_issues}x Kendala</div>
            <div class="text-[10px] text-slate-400">${j.tes_tidak_lancar}x gagal tes</div>
          </div>
        </div>
      `).join('');
    }

    // 5. CHARTS INITIALIZATION
    let chartInstanceKelas = null;
    let chartInstanceSyahadah = null;
    let chartInstanceJuz = null;

    function renderAllCharts() {
      const isDark = document.documentElement.classList.contains('dark');
      const textColor = isDark ? '#cbd5e1' : '#475569';
      const gridColor = isDark ? '#334155' : '#e2e8f0';

      // 1. Chart Kelas Comparison
      const ctxKelas = document.getElementById('chartKelasComparison')?.getContext('2d');
      if (ctxKelas) {
        if (chartInstanceKelas) chartInstanceKelas.destroy();
        const classes = Object.values(DB.classes_summary).filter(c => c.total_santri > 0);
        chartInstanceKelas = new Chart(ctxKelas, {
          type: 'bar',
          data: {
            labels: classes.map(c => c.name),
            datasets: [
              {
                label: 'Rata-rata Juz Dicapai',
                data: classes.map(c => c.avg_juz_dicapai),
                backgroundColor: '#10b981',
                borderRadius: 6
              },
              {
                label: 'Rata-rata Juz Lancar',
                data: classes.map(c => c.avg_juz_lancar),
                backgroundColor: '#14b8a6',
                borderRadius: 6
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: textColor, font: { size: 11, family: 'Plus Jakarta Sans' } } }
            },
            scales: {
              x: { ticks: { color: textColor, font: { size: 10 } }, grid: { display: false } },
              y: { ticks: { color: textColor, font: { size: 10 } }, grid: { color: gridColor }, beginAtZero: true }
            }
          }
        });
      }

      // 2. Chart Syahadah Status Doughnut
      const ctxSyahadah = document.getElementById('chartSyahadahStatus')?.getContext('2d');
      if (ctxSyahadah) {
        if (chartInstanceSyahadah) chartInstanceSyahadah.destroy();
        chartInstanceSyahadah = new Chart(ctxSyahadah, {
          type: 'doughnut',
          data: {
            labels: [
              'Sudah Syahadah (' + DB.summary.santri_dengan_syahadah + ')',
              'Siap Ujian Syahadah (' + DB.summary.ready_for_syahadah_count + ')',
              'Sedang Berproses (' + DB.summary.in_progress_non_syahadah_count + ')',
              'Tahap Awal / Arsip (' + DB.summary.unstarted_non_syahadah_count + ')'
            ],
            datasets: [{
              data: [
                DB.summary.santri_dengan_syahadah,
                DB.summary.ready_for_syahadah_count,
                DB.summary.in_progress_non_syahadah_count,
                DB.summary.unstarted_non_syahadah_count
              ],
              backgroundColor: ['#f59e0b', '#10b981', '#3b82f6', '#94a3b8'],
              borderWidth: 0
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { position: 'bottom', labels: { color: textColor, font: { size: 10 } } }
            },
            cutout: '65%'
          }
        });
      }

      // 3. Chart Juz Issues Full (Tab Kelancaran)
      const ctxJuz = document.getElementById('chartJuzIssuesFull')?.getContext('2d');
      if (ctxJuz) {
        if (chartInstanceJuz) chartInstanceJuz.destroy();
        const sortedJuz = [...DB.juz_stats].sort((a,b) => (b.tes_tidak_lancar + b.sabtu_issues) - (a.tes_tidak_lancar + a.sabtu_issues));
        chartInstanceJuz = new Chart(ctxJuz, {
          type: 'bar',
          data: {
            labels: sortedJuz.map(j => 'Juz ' + j.juz),
            datasets: [
              {
                label: 'Gagal Ujian Tes 1 Juz',
                data: sortedJuz.map(j => j.tes_tidak_lancar),
                backgroundColor: '#ef4444',
                borderRadius: 4
              },
              {
                label: 'Catatan Rapuh di Laporan Sabtu',
                data: sortedJuz.map(j => j.sabtu_issues),
                backgroundColor: '#f97316',
                borderRadius: 4
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: textColor, font: { size: 11 } } }
            },
            scales: {
              x: { stacked: true, ticks: { color: textColor, font: { size: 9 } }, grid: { display: false } },
              y: { stacked: true, ticks: { color: textColor, font: { size: 10 } }, grid: { color: gridColor }, beginAtZero: true }
            }
          }
        });
      }
    }

    // 6. SYAHADAH TAB DATA POPULATION & FILTERING
    let currentSyahadahFilter = 'semua';
    function filterSyahadahTab(filterKey) {
      currentSyahadahFilter = filterKey;
      document.querySelectorAll('.subtab-btn').forEach(btn => btn.classList.remove('active', 'bg-emerald-600', 'text-white'));
      const activeBtn = document.getElementById('subtab-sy-' + filterKey.replace('_', '-'));
      if (activeBtn) activeBtn.classList.add('active', 'bg-emerald-600', 'text-white');

      renderSyahadahTable();
    }

    function renderSyahadahTable() {
      const tbody = document.getElementById('syahadah-table-body');
      const titleElem = document.getElementById('syahadah-table-title');
      const countElem = document.getElementById('syahadah-table-count');

      // Flatten syahadah records
      let records = [];

      if (currentSyahadahFilter === 'belum_siap') {
        titleElem.textContent = 'Daftar Santri yang Belum Syahadah Namun Sudah Hafal >= 5 Juz (Siap Ujian)';
        const readySantri = ALL_SANTRI.filter(s => !s.has_syahadah && s.total_juz_dicapai >= 5);
        countElem.textContent = `Total ${readySantri.length} Santri`;
        tbody.innerHTML = readySantri.map(s => `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <td class="py-3 px-4 font-bold text-slate-900 dark:text-white">
              ${s.nama}
              <div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <span class="font-medium">${s.kelas_name}</span>
              <div class="text-[11px] text-slate-400">${s.musyrif_nama}</div>
            </td>
            <td class="py-3 px-4">
              <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 border border-amber-300 dark:border-amber-800">
                Siap Syahadah 1
              </span>
            </td>
            <td class="py-3 px-4 text-xs font-bold text-emerald-600 dark:text-emerald-400">
              ${s.total_juz_dicapai} Juz Dicapai
              <div class="text-[10px] text-slate-400 font-normal">${s.achieved_juz_str}</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <span class="text-amber-600 font-medium">${s.juziyah_count} Juziyah Tuntas</span>
            </td>
            <td class="py-3 px-4 text-xs text-slate-500">
              Belum Mengikuti Ujian
            </td>
            <td class="py-3 px-4 text-xs text-slate-500 max-w-xs">
              Santri telah menyelesaikan batas 5 juz. Direkomendasikan segera diuji Syahadah 1 (Juz 30, 29, 1, 2, 3).
            </td>
            <td class="py-3 px-4 text-center">
              <button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition">
                Rapor
              </button>
            </td>
          </tr>
        `).join('');
        return;
      }

      if (currentSyahadahFilter === 'belum_proses') {
        titleElem.textContent = 'Daftar Santri yang Sedang Berproses Menuju Syahadah 1 (1 - 4 Juz)';
        const inProgress = ALL_SANTRI.filter(s => !s.has_syahadah && s.total_juz_dicapai > 0 && s.total_juz_dicapai < 5);
        countElem.textContent = `Total ${inProgress.length} Santri`;
        tbody.innerHTML = inProgress.map(s => {
          const needed = 5 - s.total_juz_dicapai;
          return `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <td class="py-3 px-4 font-bold text-slate-900 dark:text-white">
              ${s.nama}
              <div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <span class="font-medium">${s.kelas_name}</span>
              <div class="text-[11px] text-slate-400">${s.musyrif_nama}</div>
            </td>
            <td class="py-3 px-4">
              <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300">
                Proses Menuju Syahadah 1
              </span>
            </td>
            <td class="py-3 px-4 text-xs font-bold text-blue-600 dark:text-blue-400">
              ${s.total_juz_dicapai} dari 5 Juz
              <div class="text-[10px] text-slate-400 font-normal">${s.achieved_juz_str}</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <span class="font-bold text-emerald-600">${s.total_juz_lancar} Juz Lancar</span>
            </td>
            <td class="py-3 px-4 text-xs text-slate-500">
              Sedang Ziyadah
            </td>
            <td class="py-3 px-4 text-xs text-slate-500 max-w-xs">
              Kurang ${needed} Juz lagi untuk dapat mengambil Ujian Syahadah 1.
            </td>
            <td class="py-3 px-4 text-center">
              <button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition">
                Rapor
              </button>
            </td>
          </tr>
        `;}).join('');
        return;
      }

      // Default: show actual syahadah holders
      ALL_SANTRI.forEach(s => {
        if (s.has_syahadah) {
          s.syahadahs.forEach(sy => {
            if (currentSyahadahFilter === 'semua' || sy.tingkat === currentSyahadahFilter) {
              records.push({ santri: s, syahadah: sy });
            }
          });
        }
      });

      titleElem.textContent = 'Daftar Santri Pemegang Sertifikasi Syahadah Resmi';
      countElem.textContent = `Total ${records.length} Catatan`;

      if (records.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-400">Tidak ada catatan syahadah untuk filter ini.</td></tr>`;
        return;
      }

      tbody.innerHTML = records.map(r => {
        const s = r.santri;
        const sy = r.syahadah;
        let badgeClass = 'badge-mumtaz';
        if (sy.predikat.includes('Jayyid Jiddan')) badgeClass = 'badge-jayyid-jiddan';
        else if (sy.predikat.includes('Jayyid')) badgeClass = 'badge-jayyid';

        return `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
            <td class="py-3 px-4 font-bold text-slate-900 dark:text-white">
              ${s.nama}
              <div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <span class="font-medium">${s.kelas_name}</span>
              <div class="text-[11px] text-slate-400">${s.musyrif_nama}</div>
            </td>
            <td class="py-3 px-4">
              <span class="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-50 dark:bg-amber-950 text-amber-800 dark:text-amber-200 border border-amber-300 dark:border-amber-700">
                Syahadah ${sy.tingkat.toUpperCase()}
              </span>
            </td>
            <td class="py-3 px-4 text-xs font-medium text-slate-700 dark:text-slate-300">
              ${sy.juz_cakupan_str}
            </td>
            <td class="py-3 px-4">
              <span class="px-2 py-0.5 rounded text-xs font-bold ${badgeClass}">
                ${sy.predikat}
              </span>
              <div class="text-[10px] text-slate-500 mt-0.5">${sy.kesalahan} kesalahan</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <div class="font-medium text-slate-800 dark:text-slate-200">${sy.penguji}</div>
              <div class="text-[10px] text-slate-400">${sy.created_at}</div>
            </td>
            <td class="py-3 px-4 text-xs text-slate-600 dark:text-slate-300 max-w-xs">
              <span class="italic text-[11px]">"${sy.catatan}"</span>
            </td>
            <td class="py-3 px-4 text-center">
              <button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-950 dark:hover:bg-emerald-900 text-emerald-700 dark:text-emerald-300 transition">
                Rapor 30 Juz
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    // Populate ready for syahadah list
    function populateSyahadahReadyList() {
      const readySantri = ALL_SANTRI.filter(s => !s.has_syahadah && s.total_juz_dicapai >= 5).sort((a,b) => b.total_juz_dicapai - a.total_juz_dicapai);
      const container = document.getElementById('list-syahadah-ready');
      container.innerHTML = readySantri.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 hover:bg-amber-50/60 dark:hover:bg-slate-800 cursor-pointer transition border border-slate-200 dark:border-slate-700 flex items-center justify-between">
          <div>
            <div class="font-bold text-xs text-slate-900 dark:text-white flex items-center gap-1.5">
              <span>${s.nama}</span>
              <span class="px-1.5 py-0.2 rounded text-[10px] bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-300 font-semibold">${s.total_juz_dicapai} Juz</span>
            </div>
            <div class="text-[10px] text-slate-400">${s.kelas_name} • ${s.musyrif_nama}</div>
          </div>
          <button class="text-xs font-bold text-amber-600 dark:text-amber-400 hover:underline">
            Siap Syahadah &rarr;
          </button>
        </div>
      `).join('');
    }

    // 7. STATUS KELANCARAN TAB TABLES
    function populateKelancaranTables() {
      // 1. Fluent Students Table
      const fluentStudents = [...ALL_SANTRI].filter(s => s.total_juz_lancar > 0).sort((a,b) => b.total_juz_lancar - a.total_juz_lancar);
      const fluentTbody = document.getElementById('table-fluent-students');
      fluentTbody.innerHTML = fluentStudents.map(s => `
        <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
          <td class="py-2 px-3 font-bold text-slate-900 dark:text-white">
            ${s.nama}
          </td>
          <td class="py-2 px-3 text-[11px] text-slate-500">
            ${s.kelas_name}
          </td>
          <td class="py-2 px-3 font-bold text-emerald-600 dark:text-emerald-400">
            ${s.total_juz_lancar} Juz
          </td>
          <td class="py-2 px-3 text-[11px] text-slate-600 dark:text-slate-300 max-w-xs truncate">
            ${s.lancar_juz_str}
          </td>
          <td class="py-2 px-3 text-center">
            <button onclick="openSantriModal(${s.id})" class="px-2 py-0.5 text-[11px] font-semibold rounded bg-emerald-50 text-emerald-700 hover:bg-emerald-100 dark:bg-emerald-950 dark:text-emerald-300">
              Lihat
            </button>
          </td>
        </tr>
      `).join('');

      // 2. Need Attention Table
      const needAttention = [...ALL_SANTRI].filter(s => s.total_tidak_lancar > 0 || s.sabtu_issues_count > 0).sort((a,b) => (b.total_tidak_lancar + b.sabtu_issues_count) - (a.total_tidak_lancar + a.sabtu_issues_count));
      const attnTbody = document.getElementById('table-need-attention-students');
      attnTbody.innerHTML = needAttention.map(s => `
        <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition">
          <td class="py-2 px-3 font-bold text-slate-900 dark:text-white">
            ${s.nama}
          </td>
          <td class="py-2 px-3 text-[11px] text-slate-500">
            ${s.kelas_name}
          </td>
          <td class="py-2 px-3 font-bold text-rose-600 dark:text-rose-400 text-[11px]">
            ${s.total_tidak_lancar > 0 ? s.tidak_lancar_str : 'Lolos Ujian'}
          </td>
          <td class="py-2 px-3 text-[11px] text-amber-600 dark:text-amber-400 font-medium">
            ${s.sabtu_issues_count} catatan rapuh
          </td>
          <td class="py-2 px-3 text-center">
            <button onclick="openSantriModal(${s.id})" class="px-2 py-0.5 text-[11px] font-semibold rounded bg-rose-50 text-rose-700 hover:bg-rose-100 dark:bg-rose-950 dark:text-rose-300">
              Bimbing
            </button>
          </td>
        </tr>
      `).join('');
    }

    // 8. GROUPING KELAS & HALAQAH CARDS
    function populateGroupingCards() {
      // Classes Grid
      const classContainer = document.getElementById('cards-classes-grid');
      const classes = Object.values(DB.classes_summary).filter(c => c.total_santri > 0);
      classContainer.innerHTML = classes.map(c => `
        <div onclick="filterByGroup('kelas', '${c.id}')" class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-emerald-500 cursor-pointer transition group">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-bold text-slate-900 dark:text-white text-sm group-hover:text-emerald-600 transition">${c.name}</h4>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300">
              ${c.total_santri} Santri
            </span>
          </div>
          <div class="space-y-2 text-xs">
            <div class="flex justify-between text-slate-500">
              <span>Santri Aktif:</span>
              <strong class="text-slate-700 dark:text-slate-200">${c.aktif}</strong>
            </div>
            <div class="flex justify-between text-slate-500">
              <span>Rata-rata Juz Dicapai:</span>
              <strong class="text-emerald-600 dark:text-emerald-400 font-bold">${c.avg_juz_dicapai} Juz</strong>
            </div>
            <div class="flex justify-between text-slate-500">
              <span>Rata-rata Teruji Lancar:</span>
              <strong class="text-teal-600 dark:text-teal-400 font-bold">${c.avg_juz_lancar} Juz</strong>
            </div>
            <div class="flex justify-between text-slate-500">
              <span>Pemegang Syahadah:</span>
              <strong class="text-amber-600 font-bold">${c.syahadah_holders} (${c.syahadah_pct}%)</strong>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[11px] text-emerald-600 font-semibold">
            <span>Lihat Daftar Santri</span>
            <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </div>
        </div>
      `).join('');

      // Halaqah Grid
      const halaqahContainer = document.getElementById('cards-halaqah-grid');
      const halaqahs = Object.values(DB.halaqah_summary);
      halaqahContainer.innerHTML = halaqahs.map(h => `
        <div onclick="filterByGroup('halaqah', '${h.musyrif_nama}')" class="bg-white dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 shadow-sm hover:border-teal-500 cursor-pointer transition group">
          <div class="flex items-center justify-between mb-3">
            <h4 class="font-bold text-slate-900 dark:text-white text-sm group-hover:text-teal-600 transition truncate max-w-[200px]" title="${h.musyrif_nama}">
              ${h.musyrif_nama}
            </h4>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-50 dark:bg-teal-950 text-teal-700 dark:text-teal-300">
              ${h.total_santri} Santri
            </span>
          </div>
          <div class="space-y-2 text-xs">
            <div class="flex justify-between text-slate-500">
              <span>Santri Aktif:</span>
              <strong class="text-slate-700 dark:text-slate-200">${h.aktif}</strong>
            </div>
            <div class="flex justify-between text-slate-500">
              <span>Total Juz Diselesaikan:</span>
              <strong class="text-emerald-600 dark:text-emerald-400 font-bold">${h.total_juz_dicapai} Juz</strong>
            </div>
            <div class="flex justify-between text-slate-500">
              <span>Rata-rata per Santri:</span>
              <strong class="text-slate-700 dark:text-slate-200">${h.avg_juz_dicapai} Juz</strong>
            </div>
            <div class="flex justify-between text-slate-500">
              <span>Lulus Syahadah:</span>
              <strong class="text-amber-600 font-bold">${h.syahadah_holders} Santri (${h.syahadah_pct}%)</strong>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[11px] text-teal-600 font-semibold">
            <span>Buka Halaqah Ini</span>
            <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </div>
        </div>
      `).join('');
    }

    function filterByGroup(type, val) {
      switchTab('santri');
      if (type === 'kelas') {
        document.getElementById('filterKelas').value = val;
      } else if (type === 'halaqah') {
        document.getElementById('filterHalaqah').value = val;
      }
      applyFilters();
    }

    // 9. SANTRI DIRECTORY TABLE, FILTERS & MODAL
    function initHalaqahFilterDropdown() {
      const select = document.getElementById('filterHalaqah');
      const halaqahNames = Object.keys(DB.halaqah_summary);
      select.innerHTML = '<option value="semua">Semua Halaqah</option>' + 
        halaqahNames.map(name => `<option value="${name}">${name}</option>`).join('');
    }

    function applyFilters() {
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const k = document.getElementById('filterKelas').value;
      const h = document.getElementById('filterHalaqah').value;
      const sy = document.getElementById('filterSyahadah').value;
      const kl = document.getElementById('filterKelancaran').value;

      filteredSantri = ALL_SANTRI.filter(s => {
        // Search text
        if (q) {
          const matchName = s.nama.toLowerCase().includes(q);
          const matchNis = s.nis.toLowerCase().includes(q);
          const matchNik = s.nik.toLowerCase().includes(q);
          if (!matchName && !matchNis && !matchNik) return false;
        }

        // Kelas
        if (k !== 'semua') {
          if (k === 'alumni') {
            if (!s.kelas_name.includes('Alumni')) return false;
          } else {
            if (s.kelas_id !== k) return false;
          }
        }

        // Halaqah
        if (h !== 'semua' && s.musyrif_nama !== h) return false;

        // Syahadah
        if (sy === 'sudah_syahadah' && !s.has_syahadah) return false;
        if (sy === 'siap_syahadah' && (s.has_syahadah || s.total_juz_dicapai < 5)) return false;
        if (sy === 'berproses' && (s.has_syahadah || s.total_juz_dicapai === 0 || s.total_juz_dicapai >= 5)) return false;
        if (sy === 'belum_syahadah' && s.has_syahadah) return false;

        // Kelancaran
        if (kl === 'mutqin' && s.fluency_label !== 'Sangat Lancar (Mutqin)') return false;
        if (kl === 'mayoritas' && s.fluency_label !== 'Mayoritas Lancar') return false;
        if (kl === 'perhatian' && s.fluency_label !== 'Perlu Perhatian & Murajaah') return false;
        if (kl === 'proses' && s.fluency_label !== 'Dalam Proses Setoran') return false;

        return true;
      });

      // Sort
      sortFilteredSantri();
      renderSantriTable();
    }

    function resetFilters() {
      document.getElementById('searchInput').value = '';
      document.getElementById('filterKelas').value = 'semua';
      document.getElementById('filterHalaqah').value = 'semua';
      document.getElementById('filterSyahadah').value = 'semua';
      document.getElementById('filterKelancaran').value = 'semua';
      applyFilters();
    }

    function sortSantriTable(col) {
      if (currentSort.column === col) {
        currentSort.asc = !currentSort.asc;
      } else {
        currentSort.column = col;
        currentSort.asc = true;
      }
      sortFilteredSantri();
      renderSantriTable();
    }

    function sortFilteredSantri() {
      filteredSantri.sort((a,b) => {
        let valA, valB;
        if (currentSort.column === 'nama') {
          valA = a.nama.toLowerCase();
          valB = b.nama.toLowerCase();
        } else if (currentSort.column === 'kelas') {
          valA = a.kelas_name;
          valB = b.kelas_name;
        } else if (currentSort.column === 'halaqah') {
          valA = a.musyrif_nama;
          valB = b.musyrif_nama;
        } else if (currentSort.column === 'juz_dicapai') {
          valA = a.total_juz_dicapai;
          valB = b.total_juz_dicapai;
        } else if (currentSort.column === 'juz_lancar') {
          valA = a.total_juz_lancar;
          valB = b.total_juz_lancar;
        }
        if (valA < valB) return currentSort.asc ? -1 : 1;
        if (valA > valB) return currentSort.asc ? 1 : -1;
        return 0;
      });
    }

    function renderSantriTable() {
      document.getElementById('filterResultCount').textContent = filteredSantri.length;
      const tbody = document.getElementById('santriTableBody');

      if (filteredSantri.length === 0) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-10 text-slate-400">Tidak ada santri yang sesuai kriteria pencarian.</td></tr>`;
        return;
      }

      tbody.innerHTML = filteredSantri.map(s => {
        // Syahadah badge
        let syahadahBadge = '<span class="text-slate-400 text-xs">Belum Ada</span>';
        if (s.has_syahadah) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800 dark:bg-amber-950 dark:text-amber-200 border border-amber-300 dark:border-amber-700">Syahadah ${s.highest_syahadah.toUpperCase()}</span>`;
        } else if (s.total_juz_dicapai >= 5) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300">Siap Ujian 1</span>`;
        }

        // Fluency badge
        let flClass = 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400';
        if (s.fluency_label.includes('Sangat Lancar')) flClass = 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 border border-emerald-300';
        else if (s.fluency_label.includes('Mayoritas')) flClass = 'bg-teal-100 text-teal-800 dark:bg-teal-950 dark:text-teal-300';
        else if (s.fluency_label.includes('Perhatian')) flClass = 'bg-rose-100 text-rose-800 dark:bg-rose-950 dark:text-rose-300 border border-rose-300';

        // Percentage of 30 juz
        const pct = Math.round((s.total_juz_dicapai / 30) * 100);

        return `
          <tr class="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
            <td class="py-3 px-4 font-bold text-slate-900 dark:text-white">
              <div class="hover:text-emerald-600 transition">${s.nama}</div>
              <div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis} • NIK: ${s.nik ? s.nik.substring(0, 8) + '...' : '-'}</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <div class="font-medium text-slate-800 dark:text-slate-200">${s.kelas_name}</div>
              <div class="text-[10px] text-slate-400">${s.jenis_kelamin}</div>
            </td>
            <td class="py-3 px-4 text-xs">
              <div class="font-medium text-slate-700 dark:text-slate-300 max-w-[180px] truncate" title="${s.musyrif_nama}">
                ${s.musyrif_nama}
              </div>
            </td>
            <td class="py-3 px-4">
              <div class="flex items-center gap-2">
                <span class="font-bold text-emerald-600 dark:text-emerald-400 text-xs">${s.total_juz_dicapai} Juz</span>
                <span class="text-[10px] text-slate-400">(${pct}%)</span>
              </div>
              <div class="w-20 bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 mt-1 overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: ${pct}%"></div>
              </div>
            </td>
            <td class="py-3 px-4">
              <span class="font-bold text-teal-600 dark:text-teal-400 text-xs">${s.total_juz_lancar} Juz</span>
            </td>
            <td class="py-3 px-4">
              ${syahadahBadge}
            </td>
            <td class="py-3 px-4">
              <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold ${flClass}">
                ${s.fluency_label}
              </span>
            </td>
            <td class="py-3 px-4 text-center">
              <button onclick="event.stopPropagation(); openSantriModal(${s.id})" class="px-3 py-1 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm transition">
                Rapor 30 Juz
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    // 10. MODAL PROFIL SANTRI (RAPOR 30 JUZ)
    function openSantriModal(santriId) {
      const s = ALL_SANTRI.find(item => item.id === santriId);
      if (!s) return;

      document.getElementById('modal-avatar').textContent = s.nama.charAt(0);
      document.getElementById('modal-nama').textContent = s.nama;
      document.getElementById('modal-status').textContent = s.status;
      document.getElementById('modal-nis').textContent = `NIS: ${s.nis}`;
      document.getElementById('modal-kelas').textContent = s.kelas_name;
      document.getElementById('modal-halaqah').textContent = s.musyrif_nama;
      document.getElementById('modal-jk').textContent = s.jenis_kelamin;

      document.getElementById('modal-juz-dicapai').textContent = `${s.total_juz_dicapai} Juz`;
      document.getElementById('modal-juz-lancar').textContent = `${s.total_juz_lancar} Juz`;

      if (s.has_syahadah) {
        document.getElementById('modal-syahadah-highest').textContent = `Syahadah ${s.highest_syahadah.toUpperCase()}`;
        document.getElementById('modal-syahadah-count').textContent = `${s.syahadah_count} Sertifikasi Lulus`;
      } else {
        document.getElementById('modal-syahadah-highest').textContent = 'Belum Ada';
        document.getElementById('modal-syahadah-count').textContent = s.total_juz_dicapai >= 5 ? 'Siap Ujian 1' : 'Dalam Proses';
      }

      document.getElementById('modal-fluency-badge').textContent = s.fluency_label;
      document.getElementById('modal-tidak-lancar-count').textContent = `${s.total_tidak_lancar} Gagal Tes • ${s.sabtu_issues_count} Catatan`;

      // Target Progress
      document.getElementById('modal-target-title').textContent = s.syahadah_status_summary;
      document.getElementById('modal-target-pct').textContent = `${s.syahadah_progress_pct}%`;
      document.getElementById('modal-target-bar').style.width = `${s.syahadah_progress_pct}%`;
      document.getElementById('modal-target-desc').textContent = `Status Hafalan Terakhir: ${s.last_achievement ? `${s.last_achievement.type.toUpperCase()} di Juz ${s.last_achievement.juz || '-'}` : 'Belum tercatat'}`;

      // 30 Juz Grid
      const gridContainer = document.getElementById('modal-juz-grid');
      gridContainer.innerHTML = s.juz_grid.map(g => {
        let bg = 'bg-slate-100 text-slate-400 dark:bg-slate-800 dark:text-slate-600 border-slate-200 dark:border-slate-700';
        if (g.status === 'lancar') bg = 'bg-emerald-500 text-white font-bold border-emerald-600 shadow-sm';
        else if (g.status === 'belum_tes') bg = 'bg-amber-400 text-amber-950 font-bold border-amber-500';
        else if (g.status === 'tidak_lancar') bg = 'bg-rose-500 text-white font-bold border-rose-600';

        return `
          <div class="p-2 rounded-xl border text-center transition cursor-pointer hover:scale-105 ${bg}" title="Juz ${g.juz}: ${g.surah} - ${g.label}">
            <div class="text-[11px] font-black">Juz ${g.juz}</div>
            <div class="text-[9px] mt-0.5 truncate">${g.status === 'lancar' ? 'Lancar' : (g.status === 'belum_tes' ? 'Tuntas' : (g.status === 'tidak_lancar' ? 'Remidi' : '-'))}</div>
          </div>
        `;
      }).join('');

      // Syahadah History
      const sySection = document.getElementById('modal-syahadah-section');
      const syList = document.getElementById('modal-syahadah-list');
      if (s.syahadahs.length > 0) {
        sySection.classList.remove('hidden');
        syList.innerHTML = s.syahadahs.map(sy => `
          <div class="p-3 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 text-xs">
            <div class="flex items-center justify-between font-bold text-amber-900 dark:text-amber-200">
              <span>Syahadah ${sy.tingkat.toUpperCase()} (${sy.juz_cakupan_str})</span>
              <span class="px-2 py-0.5 rounded bg-amber-200 text-amber-900 font-bold">${sy.predikat} (${sy.kesalahan} salah)</span>
            </div>
            <div class="text-[11px] text-slate-500 mt-1">Penguji: ${sy.penguji} • Tanggal: ${sy.created_at}</div>
            <div class="text-[11px] text-slate-600 dark:text-slate-300 mt-1 italic">"${sy.catatan}"</div>
          </div>
        `).join('');
      } else {
        sySection.classList.add('hidden');
      }

      // Sabtu Issues
      const evSection = document.getElementById('modal-evaluasi-section');
      const evList = document.getElementById('modal-evaluasi-list');
      if (s.sabtu_issues.length > 0) {
        evSection.classList.remove('hidden');
        evList.innerHTML = s.sabtu_issues.slice(0, 5).map(iss => `
          <div class="p-2.5 rounded-lg bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/60 text-xs flex items-center justify-between">
            <div>
              <strong class="text-rose-800 dark:text-rose-300">Juz ${iss.juz || '-'}</strong>
              <span class="text-slate-500 ml-2">Halaman ${iss.startPage} s.d. ${iss.endPage}</span>
            </div>
            <span class="text-[10px] text-slate-400">${iss.tanggal}</span>
          </div>
        `).join('');
      } else {
        evSection.classList.add('hidden');
      }

      // Recommendation
      let rek = `Alhamdulillah, ananda ${s.nama} saat ini telah menuntaskan ${s.total_juz_dicapai} Juz. `;
      if (s.total_tidak_lancar > 0) {
        rek += `Sangat dianjurkan untuk memperkuat murajaah pada ${s.tidak_lancar_str} yang sebelumnya tercatat belum lancar, sebelum menambah lembaran ziyadah baru. `;
      }
      if (s.total_juz_dicapai >= 5 && !s.has_syahadah) {
        rek += `Ananda sudah siap secara kapasitas untuk mengambil Ujian Syahadah 1 (5 Juz). Mohon bimbingan orang tua di rumah untuk melatih murajaah sambung ayat. `;
      } else if (s.has_syahadah) {
        rek += `Pertahankan pencapaian mutqin Syahadah ${s.highest_syahadah} dengan konsisten tadarus 1 juz per hari ba'da Maghrib/Subuh.`;
      } else {
        rek += `Pertahankan kedisiplinan setoran ziyadah harian 0,5 halaman per hari bersama musyrif halaqah.`;
      }
      document.getElementById('modal-rekomendasi').textContent = rek;

      // Show modal
      const modal = document.getElementById('santriModal');
      const card = document.getElementById('santriModalCard');
      modal.classList.remove('hidden');
      setTimeout(() => {
        card.classList.remove('scale-95');
        card.classList.add('scale-100');
      }, 10);
      lucide.createIcons();
    }

    function closeSantriModal() {
      const modal = document.getElementById('santriModal');
      const card = document.getElementById('santriModalCard');
      card.classList.remove('scale-100');
      card.classList.add('scale-95');
      setTimeout(() => modal.classList.add('hidden'), 150);
    }

    // 11. EXPORT TO CSV
    function exportToCSV() {
      let csv = 'NIS,Nama,Kelas,Halaqah,Status,Gender,Total Juz Dicapai,Total Juz Lancar,Syahadah Tertinggi,Status Kelancaran\\n';
      ALL_SANTRI.forEach(s => {
        csv += `"${s.nis}","${s.nama}","${s.kelas_name}","${s.musyrif_nama}","${s.status}","${s.jenis_kelamin}",${s.total_juz_dicapai},${s.total_juz_lancar},"${s.highest_syahadah || '-'}","${s.fluency_label}"\\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `laporan_tahfidz_santri_${new Date().toISOString().slice(0,10)}.csv`;
      link.click();
    }

    // 12. INITIALIZATION ON DOM LOAD
    document.addEventListener('DOMContentLoaded', () => {
      initTheme();
      populateExecutiveHighlights();
      renderAllCharts();
      populateSyahadahReadyList();
      renderSyahadahTable();
      populateKelancaranTables();
      populateGroupingCards();
      initHalaqahFilterDropdown();
      renderSantriTable();
      lucide.createIcons();
    });
  </script>

</body>
</html>
"""

# Replace placeholder with actual JSON string
final_html = html_template.replace('DATA_JSON_PLACEHOLDER', json_data_str)

output_path = 'index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Generated {output_path} successfully! Size: {os.path.getsize(output_path) / 1024:.2f} KB")
