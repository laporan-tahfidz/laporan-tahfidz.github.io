import json
import os

with open('full_report_dataset.json', encoding='utf-8') as f:
    dataset = json.load(f)

json_data_str = json.dumps(dataset, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Laporan & Evaluasi Capaian Tahfidz Santri | Dashboard Eksekutif</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Amiri:wght@400;700&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
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
    /* Mobile-first smooth scrolling & touch optimization */
    html, body {
      -webkit-tap-highlight-color: transparent;
      touch-action: manipulation;
    }
    
    /* Hide scrollbars for clean mobile swiping */
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    
    /* Custom Scrollbar for desktop */
    @media (min-width: 768px) {
      ::-webkit-scrollbar { width: 7px; height: 7px; }
      ::-webkit-scrollbar-track { background: #f8fafc; }
      ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
      ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    }
    
    /* Print Styles */
    @media print {
      body { background: white !important; color: black !important; font-size: 11pt !important; }
      .no-print { display: none !important; }
      .print-break { page-break-before: always; }
      .shadow-sm, .shadow-md, .shadow-lg { box-shadow: none !important; border: 1px solid #e2e8f0 !important; }
    }
    
    /* Badges */
    .badge-mumtaz { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
    .badge-jayyid-jiddan { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-jayyid { background: #fefce8; color: #a16207; border: 1px solid #fef08a; }
    .badge-maqbul { background: #fff7ed; color: #c2410c; border: 1px solid #ffedd5; }
    .badge-mardud { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
  </style>
</head>

<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col font-sans">

  <!-- TOP HEADER & CONTEXT BAR -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
    
    <!-- Top Micro Bar (Hidden on very small screens, visible from sm) -->
    <div class="bg-emerald-900 text-emerald-100 text-[11px] py-1.5 px-3 sm:px-4 flex items-center justify-between no-print">
      <div class="flex items-center gap-2 truncate">
        <span class="inline-flex items-center px-1.5 py-0.2 rounded-full text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1 animate-pulse"></span>
          Snapshot DB
        </span>
        <span class="truncate">Basis Data: <strong class="text-emerald-200">everynight-in-my-dream.db</strong></span>
      </div>
      <div class="hidden sm:flex items-center gap-3 text-emerald-200 text-[11px]">
        <span>WITA (Asia/Makassar)</span>
        <span>•</span>
        <span>115 Santri Total</span>
      </div>
    </div>

    <!-- Main Navigation Bar -->
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16 sm:h-20">
        
        <!-- Brand / Identity -->
        <div class="flex items-center gap-2.5 sm:gap-3.5 min-w-0">
          <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-600/20 shrink-0">
            <i data-lucide="book-open" class="w-5 h-5 sm:w-6 sm:h-6"></i>
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-1.5 sm:gap-2">
              <h1 class="text-base sm:text-2xl font-bold tracking-tight text-slate-900 truncate">Laporan Capaian Tahfidz</h1>
              <span class="hidden sm:inline-block bg-emerald-100 text-emerald-800 text-[11px] font-semibold px-2 py-0.5 rounded-full border border-emerald-300">
                Lengkap & Detail
              </span>
            </div>
            <p class="text-[11px] sm:text-xs text-slate-500 truncate">
              Pesantren Tahfidzul Quran • Evaluasi Syahadah & Kelancaran
            </p>
          </div>
        </div>

        <!-- Quick Header Actions -->
        <div class="flex items-center gap-1.5 sm:gap-2 shrink-0 no-print">
          <button onclick="switchTab('santri')" title="Cari Santri" class="p-2 sm:px-3 sm:py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition">
            <i data-lucide="search" class="w-4 h-4 text-slate-500"></i>
            <span class="hidden sm:inline">Cari Santri</span>
          </button>
          <button onclick="exportToCSV()" title="Unduh CSV" class="p-2 sm:px-3 sm:py-2 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition">
            <i data-lucide="download" class="w-4 h-4 text-slate-500"></i>
            <span class="hidden sm:inline">CSV</span>
          </button>
          <button onclick="window.print()" title="Cetak / Simpan PDF" class="px-3 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold flex items-center gap-1.5 shadow-sm transition">
            <i data-lucide="printer" class="w-4 h-4"></i>
            <span class="hidden sm:inline">Cetak</span>
          </button>
        </div>

      </div>

      <!-- HORIZONTAL SCROLLING TABS (Optimized for Mobile Touch) -->
      <nav class="flex space-x-1 sm:space-x-2 border-t border-slate-100 overflow-x-auto py-2 no-scrollbar no-print" id="mainTabs">
        <button onclick="switchTab('ringkasan')" id="tab-ringkasan" class="tab-btn active px-3 py-2 text-xs sm:text-sm font-semibold rounded-lg transition flex items-center gap-1.5 shrink-0 bg-emerald-50 text-emerald-800 border border-emerald-300">
          <i data-lucide="bar-chart-3" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-600"></i>
          <span>1. Ringkasan</span>
        </button>
        <button onclick="switchTab('syahadah')" id="tab-syahadah" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="award" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-amber-500"></i>
          <span>2. Syahadah</span>
          <span class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">26</span>
        </button>
        <button onclick="switchTab('kelancaran')" id="tab-kelancaran" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="check-check" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-teal-600"></i>
          <span>3. Kelancaran</span>
        </button>
        <button onclick="switchTab('grouping')" id="tab-grouping" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="layers" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-indigo-600"></i>
          <span>4. Kelas & Halaqah</span>
        </button>
        <button onclick="switchTab('santri')" id="tab-santri" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="users" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-600"></i>
          <span>5. Direktori Santri</span>
          <span class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-slate-200 text-slate-700">115</span>
        </button>
        <button onclick="switchTab('panduan')" id="tab-panduan" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="help-circle" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-slate-500"></i>
          <span>6. Panduan Awam</span>
        </button>
      </nav>

    </div>
  </header>

  <!-- MAIN CONTENT CONTAINER -->
  <main class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-6 flex-1 w-full space-y-6">

    <!-- ========================================================================================= -->
    <!-- TAB 1: RINGKASAN EKSEKUTIF (MOBILE OPTIMIZED) -->
    <!-- ========================================================================================= -->
    <section id="content-ringkasan" class="tab-content space-y-5 sm:space-y-6">

      <!-- Layman Explanatory Welcome Banner (Mobile Clean) -->
      <div class="rounded-2xl bg-gradient-to-r from-emerald-800 via-teal-800 to-slate-900 text-white p-5 sm:p-7 shadow-md relative overflow-hidden">
        <div class="relative z-10 max-w-3xl">
          <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-400/20 text-emerald-200 border border-emerald-400/30 mb-2.5">
            <i data-lucide="sparkles" class="w-3 h-3 text-emerald-300"></i>
            <span>Ringkasan untuk Orang Awam & Wali Santri</span>
          </div>
          <h2 class="text-xl sm:text-3xl font-extrabold tracking-tight leading-snug">
            Kilas Kinerja & Capaian Tahfidz Santri
          </h2>
          <p class="mt-2 text-slate-200 text-xs sm:text-sm leading-relaxed">
            Laporan ini menyajikan ringkasan lengkap perkembangan hafalan santri di pesantren kita: 
            mulai dari setoran harian (<span class="text-emerald-300 font-semibold">Ziyadah</span>), 
            ujian kelulusan 1 juz utuh (<span class="text-emerald-300 font-semibold">Juziyah</span>), 
            hingga ujian akbar mutqin per 5 juz (<span class="text-emerald-300 font-semibold">Syahadah</span>). 
            Disusun dengan bahasa yang mudah dipahami oleh orang tua santri dan masyarakat luas.
          </p>
          <div class="mt-4 flex flex-wrap gap-2 sm:gap-3">
            <button onclick="switchTab('syahadah')" class="px-3.5 py-2 bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-semibold rounded-lg shadow-xs transition flex items-center gap-1.5">
              <i data-lucide="award" class="w-3.5 h-3.5"></i>
              Lihat 26 Lulusan Syahadah
            </button>
            <button onclick="switchTab('kelancaran')" class="px-3.5 py-2 bg-white/10 hover:bg-white/20 text-white text-xs font-semibold rounded-lg backdrop-blur-sm border border-white/20 transition flex items-center gap-1.5">
              <i data-lucide="check-check" class="w-3.5 h-3.5"></i>
              Analisis Kelancaran
            </button>
            <button onclick="switchTab('panduan')" class="px-3.5 py-2 bg-slate-800/80 hover:bg-slate-800 text-emerald-300 text-xs font-semibold rounded-lg transition flex items-center gap-1.5">
              <i data-lucide="book-open" class="w-3.5 h-3.5"></i>
              Panduan Istilah
            </button>
          </div>
        </div>
      </div>

      <!-- 6 METRIC CARDS (2 Cols on Mobile, 3 on Tablet, 6 on Desktop) -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2.5 sm:gap-4">
        
        <!-- Total Santri -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between">
            <span class="text-[11px] sm:text-xs font-medium text-slate-500">Total Santri</span>
            <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <i data-lucide="users" class="w-3.5 h-3.5 sm:w-4 sm:h-4"></i>
            </div>
          </div>
          <div class="mt-2">
            <span class="text-xl sm:text-2xl font-bold text-slate-900">115</span>
            <span class="text-[10px] sm:text-xs text-slate-400 ml-0.5">santri</span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-emerald-600 font-medium mt-1 truncate">
            ● 97 Santri Aktif
          </p>
        </div>

        <!-- Lulus Syahadah -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between">
            <span class="text-[11px] sm:text-xs font-medium text-slate-500">Lulus Syahadah</span>
            <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
              <i data-lucide="award" class="w-3.5 h-3.5 sm:w-4 sm:h-4"></i>
            </div>
          </div>
          <div class="mt-2">
            <span class="text-xl sm:text-2xl font-bold text-amber-600">26</span>
            <span class="text-[10px] sm:text-xs text-slate-400 ml-0.5">santri</span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-amber-700 font-medium mt-1 truncate">
            29 Sertifikat diraih
          </p>
        </div>

        <!-- Juz Dihafal -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between">
            <span class="text-[11px] sm:text-xs font-medium text-slate-500">Juz Selesai</span>
            <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <i data-lucide="book-open-check" class="w-3.5 h-3.5 sm:w-4 sm:h-4"></i>
            </div>
          </div>
          <div class="mt-2">
            <span class="text-xl sm:text-2xl font-bold text-emerald-600">540</span>
            <span class="text-[10px] sm:text-xs text-slate-400 ml-0.5">juz</span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-slate-500 mt-1 truncate">
            Total seluruh santri
          </p>
        </div>

        <!-- Teruji Lancar (Mutqin) -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between">
            <span class="text-[11px] sm:text-xs font-medium text-slate-500">Teruji Mutqin</span>
            <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
              <i data-lucide="check-circle" class="w-3.5 h-3.5 sm:w-4 sm:h-4"></i>
            </div>
          </div>
          <div class="mt-2">
            <span class="text-xl sm:text-2xl font-bold text-teal-600">96</span>
            <span class="text-[10px] sm:text-xs text-slate-400 ml-0.5">juz</span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-teal-700 font-medium mt-1 truncate">
            Lolos Uji Tes 1 Juz
          </p>
        </div>

        <!-- Riwayat Setoran -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between">
            <span class="text-[11px] sm:text-xs font-medium text-slate-500">Total Setoran</span>
            <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
              <i data-lucide="activity" class="w-3.5 h-3.5 sm:w-4 sm:h-4"></i>
            </div>
          </div>
          <div class="mt-2">
            <span class="text-xl sm:text-2xl font-bold text-purple-600">4.228</span>
            <span class="text-[10px] sm:text-xs text-slate-400 ml-0.5">kali</span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-slate-500 mt-1 truncate">
            Ziyadah & ujian disimak
          </p>
        </div>

        <!-- Evaluasi Sabtu -->
        <div class="bg-white rounded-xl p-3 sm:p-4 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between">
            <span class="text-[11px] sm:text-xs font-medium text-slate-500">Evaluasi Sabtu</span>
            <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-rose-50 text-rose-600 flex items-center justify-center">
              <i data-lucide="clipboard-list" class="w-3.5 h-3.5 sm:w-4 sm:h-4"></i>
            </div>
          </div>
          <div class="mt-2">
            <span class="text-xl sm:text-2xl font-bold text-rose-600">364</span>
            <span class="text-[10px] sm:text-xs text-slate-400 ml-0.5">laporan</span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-slate-500 mt-1 truncate">
            Titik rapuh hafalan
          </p>
        </div>

      </div>

      <!-- CHARTS ROW (Responsive Stack on Mobile) -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        
        <!-- Chart 1: Perbandingan per Kelas -->
        <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h3 class="font-bold text-slate-900 text-sm sm:text-base">Capaian & Kelancaran Rata-Rata per Kelas</h3>
              <p class="text-[11px] sm:text-xs text-slate-500">Perbandingan juz yang sudah dihafal vs yang sudah teruji mutqin</p>
            </div>
            <span class="px-2 py-0.5 bg-slate-100 text-slate-700 text-[10px] sm:text-xs font-semibold rounded-md">
              Per Jenjang
            </span>
          </div>
          <div class="relative h-56 sm:h-64">
            <canvas id="chartKelasComparison"></canvas>
          </div>
          <div class="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span><strong class="text-emerald-700">Kelas 3 (Ulya)</strong> memimpin (rata-rata 11,8 Juz).</span>
            <button onclick="switchTab('grouping')" class="text-emerald-700 hover:underline font-semibold">Detail &rarr;</button>
          </div>
        </div>

        <!-- Chart 2: Komposisi Status Syahadah -->
        <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h3 class="font-bold text-slate-900 text-sm sm:text-base">Kesiapan & Kelulusan Ujian Syahadah</h3>
              <p class="text-[11px] sm:text-xs text-slate-500">Status 115 santri terhadap ujian akbar kelipatan 5 juz</p>
            </div>
            <span class="px-2 py-0.5 bg-amber-50 text-amber-800 text-[10px] sm:text-xs font-semibold rounded-md">
              Status Syahadah
            </span>
          </div>
          <div class="relative h-56 sm:h-64 flex items-center justify-center">
            <canvas id="chartSyahadahStatus"></canvas>
          </div>
          <div class="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span><strong class="text-amber-700">20 Santri</strong> sudah hafal &ge;5 juz & siap ujian!</span>
            <button onclick="switchTab('syahadah')" class="text-amber-700 hover:underline font-semibold">Detail &rarr;</button>
          </div>
        </div>

      </div>

      <!-- TOP HIGHLIGHTS (Mobile-Friendly Stacked Lists) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <!-- Top 5 Santri Hafalan Tertinggi -->
        <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-900 text-xs sm:text-sm flex items-center gap-1.5">
              <i data-lucide="crown" class="w-4 h-4 text-amber-500"></i>
              Top Santri Paling Maju
            </h3>
            <span class="text-[10px] text-slate-400">Total Juz</span>
          </div>
          <div class="space-y-2" id="list-top-achievers">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- Top 5 Santri Paling Mutqin -->
        <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-900 text-xs sm:text-sm flex items-center gap-1.5">
              <i data-lucide="award" class="w-4 h-4 text-emerald-500"></i>
              Top Santri Paling Mutqin
            </h3>
            <span class="text-[10px] text-slate-400">Juz Teruji</span>
          </div>
          <div class="space-y-2" id="list-top-fluent">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- 5 Juz Paling Menantang -->
        <div class="bg-white p-4 sm:p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between mb-3">
            <h3 class="font-bold text-slate-900 text-xs sm:text-sm flex items-center gap-1.5">
              <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-500"></i>
              Juz Paling Menantang
            </h3>
            <span class="text-[10px] text-slate-400">Frekuensi Kendala</span>
          </div>
          <div class="space-y-2" id="list-challenging-juz">
            <!-- Dynamically populated -->
          </div>
        </div>

      </div>

      <!-- RECOMMENDATION BANNER -->
      <div class="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 sm:p-6 shadow-xs">
        <h3 class="font-bold text-emerald-900 text-sm sm:text-base flex items-center gap-2">
          <i data-lucide="compass" class="w-4 h-4 sm:w-5 sm:h-5 text-emerald-700"></i>
          Rekomendasi Pembinaan Tahfidz
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4 mt-3 text-xs text-emerald-950">
          <div class="bg-white p-3.5 rounded-xl border border-emerald-200">
            <strong class="text-slate-900 block mb-1">1. Jadwalkan 20 Calon Syahadah</strong>
            <p class="text-slate-600 text-[11px] leading-relaxed">
              Ada 20 santri yang sudah tuntas 5 hingga 15 juz (M. Alvin, Wildan Akhram, dll) namun belum mengambil Syahadah 1. Diperlukan pekan khusus ujian syahadah.
            </p>
          </div>
          <div class="bg-white p-3.5 rounded-xl border border-emerald-200">
            <strong class="text-slate-900 block mb-1">2. Takhassus Juz 1 & 2</strong>
            <p class="text-slate-600 text-[11px] leading-relaxed">
              Juz 1 dan 2 tercatat 321 kali rapuh di evaluasi Sabtu karena panjang ayat dan kemiripan lafadz (*mutasyabihat*). Butuh penguatan talaqqi intensif.
            </p>
          </div>
          <div class="bg-white p-3.5 rounded-xl border border-emerald-200">
            <strong class="text-slate-900 block mb-1">3. Pendampingan Kelas 1 (Ula)</strong>
            <p class="text-slate-600 text-[11px] leading-relaxed">
              Santri Kelas 1 stabil dengan rata-rata 3 juz (Juz 30 & 29). Target berikutnya menuntaskan Juz 1, 2, dan 3 agar siap menyusul Syahadah 1 bersama.
            </p>
          </div>
        </div>
      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 2: LAPORAN SYAHADAH -->
    <!-- ========================================================================================= -->
    <section id="content-syahadah" class="tab-content hidden space-y-5 sm:space-y-6">
      
      <!-- Syahadah Header Box -->
      <div class="bg-white rounded-2xl p-4 sm:p-6 border border-slate-200 shadow-xs">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-amber-100 text-amber-800 border border-amber-300 mb-1.5">
              <i data-lucide="award" class="w-3.5 h-3.5 text-amber-600"></i>
              Ujian Akbar Mutqin 5-Juz
            </div>
            <h2 class="text-lg sm:text-2xl font-bold text-slate-900">Laporan Khusus Syahadah Santri</h2>
            <p class="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
              Syahadah adalah ujian puncak kelayakan mutqin yang disimak langsung per 5 juz berturut-turut tanpa melihat mushaf.
            </p>
          </div>
          <!-- Mini summary pills -->
          <div class="grid grid-cols-3 gap-2 bg-slate-50 p-2.5 rounded-xl border border-slate-200 text-center shrink-0">
            <div class="px-1.5">
              <div class="text-[10px] text-slate-400">Lulus Syahadah</div>
              <div class="text-base sm:text-lg font-bold text-amber-600">26 Santri</div>
            </div>
            <div class="px-1.5 border-x border-slate-200">
              <div class="text-[10px] text-slate-400">Total Event</div>
              <div class="text-base sm:text-lg font-bold text-emerald-600">29 Kali</div>
            </div>
            <div class="px-1.5">
              <div class="text-[10px] text-slate-400">Belum Syahadah</div>
              <div class="text-base sm:text-lg font-bold text-slate-600">89 Santri</div>
            </div>
          </div>
        </div>

        <!-- 4 Tiers of Syahadah Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3 mt-4 pt-4 border-t border-slate-100">
          <div class="p-3 rounded-xl bg-amber-50 border border-amber-200">
            <div class="text-xs text-amber-900 font-semibold">Syahadah 1 (5 Juz)</div>
            <div class="text-xl sm:text-2xl font-black text-amber-700 mt-0.5">12 <span class="text-xs font-normal text-amber-600">Santri</span></div>
            <div class="text-[10px] text-amber-700/80 mt-0.5 truncate">Juz 30, 29, 1, 2, 3</div>
          </div>
          <div class="p-3 rounded-xl bg-teal-50 border border-teal-200">
            <div class="text-xs text-teal-900 font-semibold">Syahadah 2 (10 Juz)</div>
            <div class="text-xl sm:text-2xl font-black text-teal-700 mt-0.5">10 <span class="text-xs font-normal text-teal-600">Santri</span></div>
            <div class="text-[10px] text-teal-700/80 mt-0.5 truncate">Juz 4, 5, 6, 7, 8</div>
          </div>
          <div class="p-3 rounded-xl bg-blue-50 border border-blue-200">
            <div class="text-xs text-blue-900 font-semibold">Syahadah 3 (15 Juz)</div>
            <div class="text-xl sm:text-2xl font-black text-blue-700 mt-0.5">4 <span class="text-xs font-normal text-blue-600">Santri</span></div>
            <div class="text-[10px] text-blue-700/80 mt-0.5 truncate">Juz 9, 10, 11, 12, 13</div>
          </div>
          <div class="p-3 rounded-xl bg-purple-50 border border-purple-200">
            <div class="text-xs text-purple-900 font-semibold">Syahadah 4 (20 Juz)</div>
            <div class="text-xl sm:text-2xl font-black text-purple-700 mt-0.5">3 <span class="text-xs font-normal text-purple-600">Santri</span></div>
            <div class="text-[10px] text-purple-700/80 mt-0.5 truncate">Juz 14, 15, 16, 17, 18</div>
          </div>
        </div>

      </div>

      <!-- SYAHADAH SUB-TABS (Horizontal Swipe on Mobile) -->
      <div class="flex items-center gap-1.5 sm:gap-2 overflow-x-auto no-scrollbar pb-1 no-print">
        <button onclick="filterSyahadahTab('semua')" id="subtab-sy-semua" class="subtab-btn active px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-600 text-white shrink-0 transition">
          Semua Lulusan (29)
        </button>
        <button onclick="filterSyahadahTab('keempat')" id="subtab-sy-keempat" class="subtab-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100 shrink-0 transition">
          Syahadah 4 (20 Juz) • 3
        </button>
        <button onclick="filterSyahadahTab('ketiga')" id="subtab-sy-ketiga" class="subtab-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100 shrink-0 transition">
          Syahadah 3 (15 Juz) • 4
        </button>
        <button onclick="filterSyahadahTab('kedua')" id="subtab-sy-kedua" class="subtab-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100 shrink-0 transition">
          Syahadah 2 (10 Juz) • 10
        </button>
        <button onclick="filterSyahadahTab('pertama')" id="subtab-sy-pertama" class="subtab-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-100 shrink-0 transition">
          Syahadah 1 (5 Juz) • 12
        </button>
        <button onclick="filterSyahadahTab('belum_siap')" id="subtab-sy-belum-siap" class="subtab-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-amber-800 bg-amber-50 hover:bg-amber-100 shrink-0 transition">
          Belum: Siap Ujian (&ge;5 Juz) • 20
        </button>
        <button onclick="filterSyahadahTab('belum_proses')" id="subtab-sy-belum-proses" class="subtab-btn px-3 py-1.5 rounded-lg text-xs font-semibold text-blue-800 bg-blue-50 hover:bg-blue-100 shrink-0 transition">
          Belum: Berproses (1-4 Juz) • 17
        </button>
      </div>

      <!-- SYAHADAH LIST (Mobile Card View + Desktop Table View) -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="p-3.5 sm:p-4 border-b border-slate-200 bg-slate-50/70 flex items-center justify-between">
          <div>
            <h3 class="font-bold text-slate-900 text-xs sm:text-sm" id="syahadah-table-title">Daftar Pemegang Sertifikasi Syahadah</h3>
            <p class="text-[10px] sm:text-xs text-slate-500" id="syahadah-table-subtitle">Data ujian akbar resmi kelipatan 5 juz yang telah diselesaikan</p>
          </div>
          <span class="text-[11px] font-semibold text-slate-600" id="syahadah-table-count">29 Catatan</span>
        </div>

        <!-- Mobile Card Container (visible on sm:hidden) -->
        <div class="sm:hidden divide-y divide-slate-100" id="syahadah-mobile-cards">
          <!-- Populated by JS -->
        </div>

        <!-- Desktop Table (visible on sm:table) -->
        <div class="hidden sm:block overflow-x-auto">
          <table class="w-full text-left text-xs sm:text-sm">
            <thead class="bg-slate-100 text-slate-600 uppercase text-[11px] font-bold">
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
            <tbody class="divide-y divide-slate-100" id="syahadah-table-body">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- PRIORITAS UJIAN & DISTRIBUSI BELUM SYAHADAH -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        
        <!-- Kolom Siap Ujian (>=5 Juz) -->
        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-amber-200 shadow-xs">
          <div class="flex items-center gap-2 mb-2.5">
            <div class="w-7 h-7 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center font-bold">
              <i data-lucide="bell-ring" class="w-4 h-4"></i>
            </div>
            <div>
              <h3 class="font-bold text-slate-900 text-sm">Prioritas: Hafalan Sudah &ge;5 Juz</h3>
              <p class="text-[11px] text-slate-500">Santri yang telah memenuhi syarat kuantitas untuk Syahadah 1</p>
            </div>
          </div>
          <p class="text-[11px] text-slate-600 mb-3 bg-amber-50 p-2.5 rounded-xl border border-amber-200 leading-relaxed">
            Santri di bawah ini telah menuntaskan 5 hingga 15 juz, namun belum tercatat mengambil ujian resmi Syahadah. 
            Direkomendasikan agar musyrif segera mengagendakan simulasi dan ujian syahadah.
          </p>
          <div class="space-y-2 max-h-80 overflow-y-auto pr-1" id="list-syahadah-ready">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- Kolom Analisis Belum Syahadah per Jenjang -->
        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs space-y-3">
          <div class="flex items-center gap-2 mb-1">
            <div class="w-7 h-7 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold">
              <i data-lucide="pie-chart" class="w-4 h-4"></i>
            </div>
            <div>
              <h3 class="font-bold text-slate-900 text-sm">Distribusi Belum Syahadah per Kelas</h3>
              <p class="text-[11px] text-slate-500">Kondisi dan alasan wajar santri di tiap jenjang</p>
            </div>
          </div>

          <div class="space-y-2.5 text-xs">
            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
              <div class="flex justify-between font-bold text-slate-900">
                <span>Kelas 1 (Ula - Angkatan 2026)</span>
                <span class="text-slate-500">11 dari 11 Belum (100%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px] leading-relaxed">
                <strong>Alasan wajar:</strong> Santri baru tahun pertama. Rata-rata capaian 3 Juz (Juz 30 & 29). Target Syahadah 1 di semester genap setelah menuntaskan Juz 1, 2, dan 3.
              </p>
            </div>

            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
              <div class="flex justify-between font-bold text-slate-900">
                <span>Kelas 2 (Wustho - Angkatan 2025)</span>
                <span class="text-amber-700">8 dari 16 Belum (50%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px] leading-relaxed">
                <strong>Kondisi:</strong> 4 santri sudah mencapai 5 juz dan siap ujian (Ammar Maududi, Aina Talita, Erina Liyana, Nur Humaira). 4 santri lainnya sedang menyelesaikan Juz 2 dan 3.
              </p>
            </div>

            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
              <div class="flex justify-between font-bold text-slate-900">
                <span>Kelas 3 (Ulya - Angkatan 2024)</span>
                <span class="text-emerald-700">6 dari 17 Belum (35%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px] leading-relaxed">
                <strong>Kondisi:</strong> 5 santri sudah mencapai 10-15 juz (M. Alvin [15 juz], M. Rizky [10 juz], Yusuf Kamil [10 juz], Sabila Farrah [10 juz], Khalid Fayyadh [5 juz]). Sangat siap diuji!
              </p>
            </div>

            <div class="p-2.5 rounded-xl bg-slate-50 border border-slate-200">
              <div class="flex justify-between font-bold text-slate-900">
                <span>Angkatan 2023 (Senior)</span>
                <span class="text-purple-700">13 dari 20 Belum (65%)</span>
              </div>
              <p class="text-slate-500 mt-1 text-[11px] leading-relaxed">
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
    <section id="content-kelancaran" class="tab-content hidden space-y-5 sm:space-y-6">
      
      <!-- Kelancaran Header Box -->
      <div class="bg-white rounded-2xl p-4 sm:p-6 border border-slate-200 shadow-xs">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-teal-100 text-teal-800 border border-teal-300 mb-1.5">
              <i data-lucide="check-check" class="w-3.5 h-3.5 text-teal-600"></i>
              Uji Mutqin & Laporan Evaluasi Sabtu
            </div>
            <h2 class="text-lg sm:text-2xl font-bold text-slate-900">Analisis Kelancaran Hafalan Santri</h2>
            <p class="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
              Kelancaran hafalan dinilai melalui <strong>Ujian Tes 1 Juz Utuh</strong> (kelulusan mutqin) dan <strong>Laporan Evaluasi Sabtu</strong> (pendeteksian titik rapuh hafalan).
            </p>
          </div>
          <!-- Pills -->
          <div class="grid grid-cols-3 gap-2 bg-slate-50 p-2.5 rounded-xl border border-slate-200 text-center shrink-0">
            <div class="px-1.5">
              <div class="text-[10px] text-slate-400">Total Uji Tes</div>
              <div class="text-base sm:text-lg font-bold text-slate-800">221 Kali</div>
            </div>
            <div class="px-1.5 border-x border-slate-200">
              <div class="text-[10px] text-slate-400">Lulus Lancar</div>
              <div class="text-base sm:text-lg font-bold text-emerald-600">116 Juz</div>
            </div>
            <div class="px-1.5">
              <div class="text-[10px] text-slate-400">Perlu Remidi</div>
              <div class="text-base sm:text-lg font-bold text-rose-600">105 Ujian</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2 TABLES: SIAPA SAJA YANG LANCAR vs TIDAK LANCAR (Mobile Friendly Cards) -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        
        <!-- Table 1: Santri Teruji Lancar -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 sm:p-4 border-b border-slate-200 bg-emerald-50/60 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <h3 class="font-bold text-slate-900 text-xs sm:text-sm">Santri dengan Hafalan Lancar Terbanyak</h3>
            </div>
            <span class="text-[11px] text-emerald-800 font-semibold">Tuntas Uji Musyrif</span>
          </div>

          <!-- Mobile list (sm:hidden) -->
          <div class="sm:hidden divide-y divide-slate-100 max-h-96 overflow-y-auto" id="list-fluent-mobile">
            <!-- Populated by JS -->
          </div>

          <!-- Desktop Table (hidden sm:block) -->
          <div class="hidden sm:block p-3 overflow-x-auto max-h-96 overflow-y-auto">
            <table class="w-full text-left text-xs">
              <thead class="text-slate-500 uppercase text-[10px] font-bold border-b border-slate-100">
                <tr>
                  <th class="py-2 px-3">Santri</th>
                  <th class="py-2 px-3">Kelas</th>
                  <th class="py-2 px-3">Juz Lancar</th>
                  <th class="py-2 px-3">Daftar Juz Mutqin</th>
                  <th class="py-2 px-3 text-center">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100" id="table-fluent-students">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>

        <!-- Table 2: Santri Memerlukan Bimbingan / Remidi -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
          <div class="p-3.5 sm:p-4 border-b border-slate-200 bg-rose-50/60 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              <h3 class="font-bold text-slate-900 text-xs sm:text-sm">Santri Memerlukan Bimbingan Remidi</h3>
            </div>
            <span class="text-[11px] text-rose-800 font-semibold">Prioritas Murajaah</span>
          </div>

          <!-- Mobile list (sm:hidden) -->
          <div class="sm:hidden divide-y divide-slate-100 max-h-96 overflow-y-auto" id="list-need-attention-mobile">
            <!-- Populated by JS -->
          </div>

          <!-- Desktop Table (hidden sm:block) -->
          <div class="hidden sm:block p-3 overflow-x-auto max-h-96 overflow-y-auto">
            <table class="w-full text-left text-xs">
              <thead class="text-slate-500 uppercase text-[10px] font-bold border-b border-slate-100">
                <tr>
                  <th class="py-2 px-3">Santri</th>
                  <th class="py-2 px-3">Kelas</th>
                  <th class="py-2 px-3">Juz Belum Lulus</th>
                  <th class="py-2 px-3">Catatan Rapuh</th>
                  <th class="py-2 px-3 text-center">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100" id="table-need-attention-students">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ANALISIS KENDALA PER JUZ AL-QURAN -->
      <div class="bg-white rounded-2xl p-4 sm:p-6 border border-slate-200 shadow-xs">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h3 class="font-bold text-slate-900 text-sm sm:text-base">Peta Kesulitan 30 Juz Al-Quran</h3>
            <p class="text-[11px] sm:text-xs text-slate-500">Frekuensi tidak lulus tes & catatan rapuh di Laporan Sabtu</p>
          </div>
          <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-rose-100 text-rose-800 text-[11px] font-medium self-start sm:self-auto">
            ● Paling Menantang: Juz 2, 1, 29, 3
          </span>
        </div>

        <div class="relative h-60 sm:h-72">
          <canvas id="chartJuzIssuesFull"></canvas>
        </div>

        <!-- Explanations -->
        <div class="mt-4 pt-4 border-t border-slate-100 grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-600">
          <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
            <strong class="text-slate-900 block mb-0.5">Juz 2 Paling Menantang (165x)</strong>
            <p class="text-[11px] leading-relaxed">
              Memuat banyak ayat hukum yang padat di Surah Al-Baqarah dan kemiripan ujung ayat (*mutasyabihat*). Butuh bimbingan makna ayat.
            </p>
          </div>
          <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
            <strong class="text-slate-900 block mb-0.5">Juz 1 Gerbang Transisi (156x)</strong>
            <p class="text-[11px] leading-relaxed">
              Transisi dari surah pendek (Juz 30 & 29) ke surah panjang pertama membutuhkan adaptasi nafas dan konsentrasi tinggi.
            </p>
          </div>
          <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
            <strong class="text-slate-900 block mb-0.5">Juz 29 Irama Rapat (138x)</strong>
            <p class="text-[11px] leading-relaxed">
              Memuat 11 surah (Al-Mulk s.d. Al-Mursalat). Jika jarang dimurajaah, awalan ayat di Al-Qalam dan Al-Ma'arij mudah tertukar.
            </p>
          </div>
        </div>

      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 4: GROUPING KELAS & HALAQAH -->
    <!-- ========================================================================================= -->
    <section id="content-grouping" class="tab-content hidden space-y-5 sm:space-y-6">
      
      <!-- Grouping Header -->
      <div class="bg-white rounded-2xl p-4 sm:p-6 border border-slate-200 shadow-xs">
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300 mb-1.5">
          <i data-lucide="layers" class="w-3.5 h-3.5 text-emerald-600"></i>
          Struktur Pembinaan Pesantren
        </div>
        <h2 class="text-lg sm:text-2xl font-bold text-slate-900">Grouping per Jenjang Kelas & Halaqah Musyrif</h2>
        <p class="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
          Setiap santri dibina dalam jenjang kelas berjenjang (Ula, Wustho, Ulya) dan dibimbing personal di kelompok halaqah oleh musyrif/musyrifah.
        </p>
      </div>

      <!-- ANALISIS PER JENJANG KELAS -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <h3 class="text-sm sm:text-base font-bold text-slate-900 flex items-center gap-1.5">
            <i data-lucide="graduation-cap" class="w-4 h-4 text-emerald-600"></i>
            Analisis Capaian per Jenjang Kelas
          </h3>
          <span class="text-[11px] text-slate-400">Klik kartu untuk filter santri</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4" id="cards-classes-grid">
          <!-- Dynamically populated -->
        </div>
      </div>

      <!-- ANALISIS PER HALAQAH MUSYRIF -->
      <div class="space-y-3 pt-2">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm sm:text-base font-bold text-slate-900 flex items-center gap-1.5">
              <i data-lucide="users" class="w-4 h-4 text-teal-600"></i>
              Analisis Capaian per Halaqah Musyrif
            </h3>
            <p class="text-[11px] text-slate-400">6 Halaqah aktif pengampu harian para santri</p>
          </div>
          <span class="text-[11px] text-slate-400">Rasio kelulusan & rata-rata juz</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4" id="cards-halaqah-grid">
          <!-- Dynamically populated -->
        </div>
      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 5: DIREKTORI & DETAIL SANTRI (MOBILE TOUCH OPTIMIZED) -->
    <!-- ========================================================================================= -->
    <section id="content-santri" class="tab-content hidden space-y-4 sm:space-y-6">
      
      <!-- Filter & Search Controls -->
      <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs space-y-3">
        <div class="flex items-center justify-between gap-2">
          <div>
            <h2 class="text-sm sm:text-lg font-bold text-slate-900 flex items-center gap-1.5">
              <i data-lucide="search" class="w-4 h-4 text-emerald-600"></i>
              Direktori & Profil Santri
            </h2>
            <p class="text-[11px] text-slate-500">Cari nama santri dan filter berdasarkan kriteria</p>
          </div>
          <button onclick="resetFilters()" class="text-xs font-semibold text-rose-600 hover:underline flex items-center gap-1">
            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
            <span>Reset</span>
          </button>
        </div>

        <!-- Filter Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
          
          <!-- Search box -->
          <div class="lg:col-span-2 relative">
            <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Ketik nama / NIS santri..."
              class="w-full pl-9 pr-3 py-2 text-xs rounded-lg border border-slate-200 bg-slate-50 text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500">
            <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-2.5"></i>
          </div>

          <!-- Filter Kelas -->
          <div>
            <select id="filterKelas" onchange="applyFilters()"
              class="w-full py-2 px-2.5 text-xs rounded-lg border border-slate-200 bg-slate-50 text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500">
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
            <select id="filterHalaqah" onchange="applyFilters()"
              class="w-full py-2 px-2.5 text-xs rounded-lg border border-slate-200 bg-slate-50 text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="semua">Semua Halaqah</option>
              <!-- Populated by JS -->
            </select>
          </div>

          <!-- Filter Syahadah -->
          <div>
            <select id="filterSyahadah" onchange="applyFilters()"
              class="w-full py-2 px-2.5 text-xs rounded-lg border border-slate-200 bg-slate-50 text-slate-900 focus:outline-none focus:ring-2 focus:ring-emerald-500">
              <option value="semua">Status Syahadah</option>
              <option value="sudah_syahadah">Lulus Syahadah</option>
              <option value="siap_syahadah">Siap Ujian (&ge;5 Juz)</option>
              <option value="berproses">Berproses (1-4 Juz)</option>
              <option value="belum_syahadah">Belum Syahadah</option>
            </select>
          </div>

        </div>

        <div class="flex items-center justify-between text-[11px] text-slate-500 pt-1 border-t border-slate-100">
          <span>Menampilkan <strong id="filterResultCount" class="text-slate-900">115</strong> santri</span>
          <span class="text-slate-400">Klik santri untuk melihat Rapor 30 Juz</span>
        </div>
      </div>

      <!-- SANTRI DIRECTORY: CARD VIEW ON MOBILE (sm:hidden) -->
      <div class="sm:hidden space-y-2.5" id="santriMobileCards">
        <!-- Populated by JS -->
      </div>

      <!-- SANTRI DIRECTORY: TABLE VIEW ON DESKTOP (hidden sm:block) -->
      <div class="hidden sm:block bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs sm:text-sm">
            <thead class="bg-slate-100 text-slate-600 uppercase text-[11px] font-bold tracking-wider cursor-pointer select-none">
              <tr>
                <th class="py-3 px-4" onclick="sortSantriTable('nama')">
                  <div class="flex items-center gap-1">Santri <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i></div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('kelas')">
                  <div class="flex items-center gap-1">Kelas <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i></div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('halaqah')">
                  <div class="flex items-center gap-1">Halaqah <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i></div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('juz_dicapai')">
                  <div class="flex items-center gap-1">Juz Selesai <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i></div>
                </th>
                <th class="py-3 px-4" onclick="sortSantriTable('juz_lancar')">
                  <div class="flex items-center gap-1">Juz Lancar <i data-lucide="arrow-up-down" class="w-3 h-3 text-slate-400"></i></div>
                </th>
                <th class="py-3 px-4">Syahadah</th>
                <th class="py-3 px-4">Kelancaran</th>
                <th class="py-3 px-4 text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100" id="santriTableBody">
              <!-- Dynamically populated -->
            </tbody>
          </table>
        </div>
      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 6: PANDUAN AWAM & GLOSARIUM -->
    <!-- ========================================================================================= -->
    <section id="content-panduan" class="tab-content hidden space-y-5 sm:space-y-6">
      
      <div class="bg-white rounded-2xl p-4 sm:p-6 border border-slate-200 shadow-xs">
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800 border border-emerald-300 mb-1.5">
          <i data-lucide="book-marked" class="w-3.5 h-3.5 text-emerald-600"></i>
          Panduan Sederhana untuk Wali Santri & Masyarakat
        </div>
        <h2 class="text-lg sm:text-2xl font-bold text-slate-900">Memahami Sistem & Istilah Tahfidz</h2>
        <p class="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
          Panduan praktis agar para orang tua dan orang awam memahami alur belajar, arti istilah, dan cara membaca laporan ini.
        </p>
      </div>

      <!-- ALUR BELAJAR FLOWCHART -->
      <div class="bg-white rounded-2xl p-4 sm:p-6 border border-slate-200 shadow-xs">
        <h3 class="text-sm sm:text-base font-bold text-slate-900 mb-3 flex items-center gap-1.5">
          <i data-lucide="git-branch" class="w-4 h-4 text-emerald-600"></i>
          Alur Perjalanan Menghafal Al-Quran di Pesantren
        </h3>

        <div class="grid grid-cols-1 sm:grid-cols-5 gap-2.5 text-xs">
          
          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <div class="w-6 h-6 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center text-xs mb-1.5">1</div>
            <strong class="text-slate-900 block text-xs mb-0.5">Ziyadah Harian</strong>
            <p class="text-slate-500 text-[11px] leading-relaxed">
              Menyetorkan hafalan baru per halaman (1A s.d. 10B). Target: 0,5 - 1 halaman per hari.
            </p>
          </div>

          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <div class="w-6 h-6 rounded-full bg-teal-600 text-white font-bold flex items-center justify-center text-xs mb-1.5">2</div>
            <strong class="text-slate-900 block text-xs mb-0.5">Setengah Juz</strong>
            <p class="text-slate-500 text-[11px] leading-relaxed">
              Setelah 10 halaman tuntas, santri menyetorkan 10 halaman sekaligus dalam sekali duduk.
            </p>
          </div>

          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <div class="w-6 h-6 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-xs mb-1.5">3</div>
            <strong class="text-slate-900 block text-xs mb-0.5">Ujian Juziyah (1 Juz)</strong>
            <p class="text-slate-500 text-[11px] leading-relaxed">
              Ujian formal 1 juz utuh (20 halaman) dari awal sampai akhir juz di hadapan musyrif.
            </p>
          </div>

          <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <div class="w-6 h-6 rounded-full bg-purple-600 text-white font-bold flex items-center justify-center text-xs mb-1.5">4</div>
            <strong class="text-slate-900 block text-xs mb-0.5">Ujian Kelancaran</strong>
            <p class="text-slate-500 text-[11px] leading-relaxed">
              Tes sambung ayat acak untuk memastikan hafalan mutqin (status: Lancar vs Remidi).
            </p>
          </div>

          <div class="p-3.5 rounded-xl bg-amber-50 border border-amber-300">
            <div class="w-6 h-6 rounded-full bg-amber-500 text-white font-bold flex items-center justify-center text-xs mb-1.5">5</div>
            <strong class="text-amber-900 block text-xs mb-0.5">Ujian Syahadah</strong>
            <p class="text-amber-800 text-[11px] leading-relaxed">
              Ujian puncak 5 juz berturut-turut dalam sekali duduk tanpa mushaf berpredikat resmi.
            </p>
          </div>

        </div>
      </div>

      <!-- GLOSARIUM KATA / STANDAR NILAI -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        
        <!-- Istilah penting -->
        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs space-y-3">
          <h3 class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
            <i data-lucide="book" class="w-4 h-4 text-emerald-600"></i>
            Kamus Istilah Penting
          </h3>

          <div class="space-y-2.5 text-xs">
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
              <strong class="text-emerald-700">Ziyadah:</strong>
              <p class="text-slate-600 mt-0.5 text-[11px]">Setoran hafalan baru per lembar dari santri kepada musyrif.</p>
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
              <strong class="text-emerald-700">Murajaah:</strong>
              <p class="text-slate-600 mt-0.5 text-[11px]">Mengulang kembali hafalan yang sudah disetorkan agar tidak lupa.</p>
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
              <strong class="text-emerald-700">Mutqin:</strong>
              <p class="text-slate-600 mt-0.5 text-[11px]">Hafalan yang sangat kokoh, lancar di luar kepala, dan fasih tajwidnya.</p>
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
              <strong class="text-emerald-700">Syahadah:</strong>
              <p class="text-slate-600 mt-0.5 text-[11px]">Sertifikasi ujian akbar per 5 juz (Syahadah 1 = 5 Juz, 2 = 10 Juz, dst).</p>
            </div>
            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
              <strong class="text-emerald-700">Urutan 30, 29, 1 s.d. 28:</strong>
              <p class="text-slate-600 mt-0.5 text-[11px]">Kurikulum mendahulukan Juz 30 dan 29 karena sering dibaca dalam shalat harian.</p>
            </div>
          </div>
        </div>

        <!-- Standar Nilai -->
        <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-xs space-y-3">
          <h3 class="font-bold text-slate-900 text-sm flex items-center gap-1.5">
            <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-600"></i>
            Standar Predikat Nilai Pesantren
          </h3>

          <div class="space-y-2 text-xs">
            <div class="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200">
              <div class="flex justify-between font-bold text-emerald-800">
                <span>Mumtaz (ممتاز) - Istimewa</span>
                <span>0 - 10 Kesalahan</span>
              </div>
              <p class="text-emerald-700 text-[10px] mt-0.5">Sangat sempurna, makhraj dan mad sangat teliti.</p>
            </div>
            <div class="p-2.5 rounded-lg bg-blue-50 border border-blue-200">
              <div class="flex justify-between font-bold text-blue-800">
                <span>Jayyid Jiddan (جيد جداً) - Sangat Baik</span>
                <span>11 - 20 Kesalahan</span>
              </div>
              <p class="text-blue-700 text-[10px] mt-0.5">Hafalan lancar dan kokoh dengan sedikit koreksi minor.</p>
            </div>
            <div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200">
              <div class="flex justify-between font-bold text-amber-800">
                <span>Jayyid (جيد) - Baik</span>
                <span>21 - 30 Kesalahan</span>
              </div>
              <p class="text-amber-700 text-[10px] mt-0.5">Lulus standar, perlu pengulangan mandiri di beberapa halaman.</p>
            </div>
            <div class="p-2.5 rounded-lg bg-orange-50 border border-orange-200">
              <div class="flex justify-between font-bold text-orange-800">
                <span>Maqbul (مقبول) - Cukup</span>
                <span>31 - 40 Kesalahan</span>
              </div>
              <p class="text-orange-700 text-[10px] mt-0.5">Lulus bersyarat dengan kewajiban murajaah intensif.</p>
            </div>
            <div class="p-2.5 rounded-lg bg-rose-50 border border-rose-200">
              <div class="flex justify-between font-bold text-rose-800">
                <span>Mardud (مردود) - Remidi</span>
                <span>> 40 Kesalahan</span>
              </div>
              <p class="text-rose-700 text-[10px] mt-0.5">Belum memenuhi standar minimal, wajib mengulang ujian.</p>
            </div>
          </div>
        </div>

      </div>

    </section>

  </main>

  <!-- ========================================================================================= -->
  <!-- MODAL: RAPOR & DETAIL SANTRI (30 JUZ VISUAL GRID - TOUCH FRIENDLY) -->
  <!-- ========================================================================================= -->
  <div id="santriModal" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs hidden flex items-end sm:items-center justify-center p-0 sm:p-4 no-print">
    <div class="bg-white w-full sm:max-w-3xl sm:rounded-3xl max-h-[92vh] flex flex-col shadow-2xl border-t sm:border border-slate-200 overflow-hidden transform transition-all duration-200" id="santriModalCard">
      
      <!-- Modal Header (Sticky on top) -->
      <div class="p-4 sm:p-5 bg-gradient-to-r from-emerald-800 to-teal-900 text-white flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-white/10 flex items-center justify-center text-white text-lg sm:text-xl font-bold font-arabic shrink-0" id="modal-avatar">
            س
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <h3 class="text-base sm:text-lg font-bold text-white truncate" id="modal-nama">Nama Santri</h3>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-white/20 text-white shrink-0" id="modal-status">Aktif</span>
            </div>
            <div class="flex flex-wrap items-center gap-1.5 text-[11px] text-emerald-200 mt-0.5 truncate">
              <span id="modal-nis">NIS: -</span>
              <span>•</span>
              <span id="modal-kelas">Kelas</span>
              <span>•</span>
              <span id="modal-halaqah" class="truncate">Halaqah</span>
            </div>
          </div>
        </div>
        <button onclick="closeSantriModal()" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center shrink-0 transition">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <!-- Modal Body (Scrollable with touch) -->
      <div class="p-4 sm:p-6 overflow-y-auto space-y-4 sm:space-y-5 text-slate-800 flex-1">
        
        <!-- 4 Summary Stats Mini-Cards (2x2 on mobile) -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3">
          <div class="p-2.5 sm:p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span class="text-[10px] sm:text-xs text-slate-500">Juz Dicapai</span>
            <div class="text-base sm:text-xl font-bold text-emerald-700 mt-0.5" id="modal-juz-dicapai">0 Juz</div>
            <span class="text-[9px] sm:text-[10px] text-slate-400">Ziyadah tuntas</span>
          </div>
          <div class="p-2.5 sm:p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span class="text-[10px] sm:text-xs text-slate-500">Juz Lancar</span>
            <div class="text-base sm:text-xl font-bold text-teal-700 mt-0.5" id="modal-juz-lancar">0 Juz</div>
            <span class="text-[9px] sm:text-[10px] text-slate-400">Mutqin teruji</span>
          </div>
          <div class="p-2.5 sm:p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span class="text-[10px] sm:text-xs text-slate-500">Syahadah</span>
            <div class="text-base sm:text-xl font-bold text-amber-600 mt-0.5" id="modal-syahadah-highest">-</div>
            <span class="text-[9px] sm:text-[10px] text-slate-400" id="modal-syahadah-count">0 Sertifikat</span>
          </div>
          <div class="p-2.5 sm:p-3 rounded-xl bg-slate-50 border border-slate-200">
            <span class="text-[10px] sm:text-xs text-slate-500">Kelancaran</span>
            <div class="text-[11px] sm:text-xs font-bold text-slate-800 mt-1 truncate" id="modal-fluency-badge">-</div>
            <span class="text-[9px] sm:text-[10px] text-slate-400" id="modal-tidak-lancar-count">0 Kendala</span>
          </div>
        </div>

        <!-- Target Progress -->
        <div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200">
          <div class="flex items-center justify-between text-xs font-semibold text-emerald-900 mb-1.5">
            <span id="modal-target-title" class="truncate pr-2">Target Syahadah</span>
            <span id="modal-target-pct">0%</span>
          </div>
          <div class="w-full bg-emerald-200 rounded-full h-2 overflow-hidden">
            <div id="modal-target-bar" class="bg-emerald-600 h-2 rounded-full transition-all duration-500" style="width: 0%"></div>
          </div>
          <p class="text-[11px] text-emerald-800 mt-1.5 truncate" id="modal-target-desc">-</p>
        </div>

        <!-- 30-JUZ VISUAL INTERACTIVE GRID -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-slate-900 text-xs sm:text-sm flex items-center gap-1.5">
              <i data-lucide="layout-grid" class="w-3.5 h-3.5 text-emerald-600"></i>
              Peta Visual 30 Juz
            </h4>
            <div class="flex items-center gap-2 text-[9px] sm:text-[10px]">
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-emerald-500"></span>Lancar</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-amber-400"></span>Belum Tes</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-rose-500"></span>Remidi</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded bg-slate-200"></span>Belum</span>
            </div>
          </div>

          <!-- 30 Tiles Grid (5x6 on mobile) -->
          <div class="grid grid-cols-5 sm:grid-cols-6 md:grid-cols-10 gap-1.5" id="modal-juz-grid">
            <!-- Populated by JS -->
          </div>

          <!-- Selected Juz Tap Feedback (Essential for Mobile touch!) -->
          <div id="modal-juz-selected-info" class="p-2.5 rounded-xl bg-slate-50 border border-slate-200 text-xs flex items-center justify-between">
            <div class="flex items-center gap-2 truncate">
              <span class="w-6 h-6 rounded-md bg-emerald-600 text-white font-bold flex items-center justify-center text-[11px] shrink-0" id="selected-juz-badge">1</span>
              <div class="truncate">
                <strong id="selected-juz-title">Juz 1</strong>
                <span class="text-slate-500 text-[11px] ml-1 truncate" id="selected-juz-surah">-</span>
              </div>
            </div>
            <span class="text-[11px] font-semibold text-emerald-700 shrink-0" id="selected-juz-status">Lancar</span>
          </div>
        </div>

        <!-- RIWAYAT SYAHADAH -->
        <div id="modal-syahadah-section">
          <h4 class="font-bold text-slate-900 text-xs sm:text-sm mb-2 flex items-center gap-1.5">
            <i data-lucide="award" class="w-3.5 h-3.5 text-amber-500"></i>
            Riwayat Ujian Syahadah
          </h4>
          <div class="space-y-1.5" id="modal-syahadah-list"></div>
        </div>

        <!-- CATATAN SABTU -->
        <div id="modal-evaluasi-section">
          <h4 class="font-bold text-slate-900 text-xs sm:text-sm mb-2 flex items-center gap-1.5">
            <i data-lucide="alert-circle" class="w-3.5 h-3.5 text-rose-500"></i>
            Catatan Halaman Rapuh (Evaluasi Sabtu)
          </h4>
          <div class="space-y-1.5" id="modal-evaluasi-list"></div>
        </div>

        <!-- REKOMENDASI MUSYRIF -->
        <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
          <h4 class="font-bold text-slate-900 text-xs mb-1 flex items-center gap-1">
            <i data-lucide="info" class="w-3.5 h-3.5 text-emerald-600"></i>
            Rekomendasi Musyrif
          </h4>
          <p class="text-xs text-slate-600 leading-relaxed" id="modal-rekomendasi">-</p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-3 sm:p-4 border-t border-slate-200 bg-slate-50 flex items-center justify-between shrink-0">
        <span class="text-[11px] text-slate-400">Pesantren Tahfidzul Quran</span>
        <button onclick="closeSantriModal()" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-semibold rounded-lg transition">
          Tutup Rapor
        </button>
      </div>

    </div>
  </div>

  <!-- FOOTER -->
  <footer class="bg-white border-t border-slate-200 py-5 text-center text-xs text-slate-500 no-print">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
      <div class="flex items-center gap-1.5">
        <div class="w-5 h-5 rounded bg-emerald-600 text-white font-bold text-[10px] flex items-center justify-center">TQ</div>
        <span class="font-semibold text-slate-700">Laporan Capaian Tahfidz Santri</span>
      </div>
      <div class="text-[11px] text-slate-400">
        Snapshot: <code class="font-mono text-emerald-700">everynight-in-my-dream.db</code> • 115 Santri
      </div>
    </div>
  </footer>

  <!-- EMBEDDED DATASET SCRIPT -->
  <script id="embedded-data" type="application/json">
DATA_JSON_PLACEHOLDER
  </script>

  <!-- JAVASCRIPT APPLICATION CODE (CLEAN & TOUCH FRIENDLY) -->
  <script>
    // 1. DATA INITIALIZATION
    const rawDataElem = document.getElementById('embedded-data');
    let DB = JSON.parse(rawDataElem.textContent);
    let ALL_SANTRI = DB.santri_list;
    let filteredSantri = [...ALL_SANTRI];
    let currentSort = { column: 'nama', asc: true };
    let currentModalSantri = null;

    // 2. TAB SWITCHING
    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-emerald-50', 'text-emerald-800', 'border', 'border-emerald-300');
        btn.classList.add('text-slate-600');
      });
      document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));

      const activeBtn = document.getElementById('tab-' + tabId);
      const activeContent = document.getElementById('content-' + tabId);
      if (activeBtn && activeContent) {
        activeBtn.classList.add('active', 'bg-emerald-50', 'text-emerald-800', 'border', 'border-emerald-300');
        activeBtn.classList.remove('text-slate-600');
        activeContent.classList.remove('hidden');
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
      lucide.createIcons();
    }

    // 3. EXECUTIVE SUMMARY HIGHLIGHTS
    function populateExecutiveHighlights() {
      // Top 5 Achievers
      const topAchievers = [...ALL_SANTRI].sort((a,b) => b.total_juz_dicapai - a.total_juz_dicapai).slice(0, 5);
      const topAchElem = document.getElementById('list-top-achievers');
      topAchElem.innerHTML = topAchievers.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 cursor-pointer transition border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-5 h-5 rounded-full bg-amber-100 text-amber-800 flex items-center justify-center text-[10px] font-bold shrink-0">${idx + 1}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
              <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-emerald-700 text-xs">${s.total_juz_dicapai} Juz</div>
            <div class="text-[9px] text-slate-400">${s.total_juz_lancar} lancar</div>
          </div>
        </div>
      `).join('');

      // Top 5 Fluent
      const topFluent = [...ALL_SANTRI].sort((a,b) => (b.total_juz_lancar - a.total_juz_lancar) || (b.total_juz_dicapai - a.total_juz_dicapai)).slice(0, 5);
      const topFluElem = document.getElementById('list-top-fluent');
      topFluElem.innerHTML = topFluent.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 cursor-pointer transition border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center text-[10px] font-bold shrink-0">${idx + 1}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
              <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-teal-700 text-xs">${s.total_juz_lancar} Juz</div>
            <div class="text-[9px] text-slate-400">${s.total_juz_dicapai} dicapai</div>
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
        <div class="flex items-center justify-between p-2 rounded-xl bg-slate-50 border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-6 h-6 rounded-lg bg-rose-100 text-rose-800 flex items-center justify-center text-[10px] font-bold shrink-0">Juz ${j.juz}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${j.surah}</div>
              <div class="text-[10px] text-slate-400">${j.hafal_count} santri hafal</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-rose-600 text-xs">${j.total_issues}x Kendala</div>
            <div class="text-[9px] text-slate-400">${j.tes_tidak_lancar}x remidi</div>
          </div>
        </div>
      `).join('');
    }

    // 4. RENDER CHARTS
    let chartInstanceKelas = null;
    let chartInstanceSyahadah = null;
    let chartInstanceJuz = null;

    function renderAllCharts() {
      const textColor = '#475569';
      const gridColor = '#e2e8f0';

      // 1. Chart Kelas Comparison
      const ctxKelas = document.getElementById('chartKelasComparison')?.getContext('2d');
      if (ctxKelas) {
        if (chartInstanceKelas) chartInstanceKelas.destroy();
        const classes = Object.values(DB.classes_summary).filter(c => c.total_santri > 0);
        chartInstanceKelas = new Chart(ctxKelas, {
          type: 'bar',
          data: {
            labels: classes.map(c => c.name.replace(/\\s*\\(.*?\\)/, '')),
            datasets: [
              {
                label: 'Rata-rata Juz Dicapai',
                data: classes.map(c => c.avg_juz_dicapai),
                backgroundColor: '#10b981',
                borderRadius: 5
              },
              {
                label: 'Rata-rata Juz Lancar',
                data: classes.map(c => c.avg_juz_lancar),
                backgroundColor: '#14b8a6',
                borderRadius: 5
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: textColor, font: { size: 10, family: 'Plus Jakarta Sans' } } }
            },
            scales: {
              x: { ticks: { color: textColor, font: { size: 9 } }, grid: { display: false } },
              y: { ticks: { color: textColor, font: { size: 9 } }, grid: { color: gridColor }, beginAtZero: true }
            }
          }
        });
      }

      // 2. Chart Syahadah Status
      const ctxSyahadah = document.getElementById('chartSyahadahStatus')?.getContext('2d');
      if (ctxSyahadah) {
        if (chartInstanceSyahadah) chartInstanceSyahadah.destroy();
        chartInstanceSyahadah = new Chart(ctxSyahadah, {
          type: 'doughnut',
          data: {
            labels: [
              'Lulus (' + DB.summary.santri_dengan_syahadah + ')',
              'Siap Ujian (' + DB.summary.ready_for_syahadah_count + ')',
              'Berproses (' + DB.summary.in_progress_non_syahadah_count + ')',
              'Awal (' + DB.summary.unstarted_non_syahadah_count + ')'
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
              legend: { position: 'bottom', labels: { color: textColor, font: { size: 9 } } }
            },
            cutout: '65%'
          }
        });
      }

      // 3. Chart Juz Issues (Kelancaran)
      const ctxJuz = document.getElementById('chartJuzIssuesFull')?.getContext('2d');
      if (ctxJuz) {
        if (chartInstanceJuz) chartInstanceJuz.destroy();
        const sortedJuz = [...DB.juz_stats].sort((a,b) => (b.tes_tidak_lancar + b.sabtu_issues) - (a.tes_tidak_lancar + a.sabtu_issues));
        chartInstanceJuz = new Chart(ctxJuz, {
          type: 'bar',
          data: {
            labels: sortedJuz.map(j => 'J' + j.juz),
            datasets: [
              {
                label: 'Gagal Tes',
                data: sortedJuz.map(j => j.tes_tidak_lancar),
                backgroundColor: '#ef4444',
                borderRadius: 3
              },
              {
                label: 'Catatan Rapuh',
                data: sortedJuz.map(j => j.sabtu_issues),
                backgroundColor: '#f97316',
                borderRadius: 3
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { labels: { color: textColor, font: { size: 10 } } }
            },
            scales: {
              x: { stacked: true, ticks: { color: textColor, font: { size: 8 } }, grid: { display: false } },
              y: { stacked: true, ticks: { color: textColor, font: { size: 9 } }, grid: { color: gridColor }, beginAtZero: true }
            }
          }
        });
      }
    }

    // 5. SYAHADAH DATA & FILTERING (Mobile Cards + Desktop Table)
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
      const mobileCards = document.getElementById('syahadah-mobile-cards');
      const titleElem = document.getElementById('syahadah-table-title');
      const countElem = document.getElementById('syahadah-table-count');

      let records = [];

      // Case: Siap Ujian (>= 5 juz)
      if (currentSyahadahFilter === 'belum_siap') {
        titleElem.textContent = 'Santri Belum Syahadah Namun Sudah Hafal >= 5 Juz (Siap Ujian)';
        const readySantri = ALL_SANTRI.filter(s => !s.has_syahadah && s.total_juz_dicapai >= 5);
        countElem.textContent = `${readySantri.length} Santri`;

        mobileCards.innerHTML = readySantri.map(s => `
          <div class="p-3 bg-white hover:bg-slate-50 transition space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-slate-900">${s.nama}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">Siap Ujian 1</span>
            </div>
            <div class="text-[11px] text-slate-500">${s.kelas_name} • ${s.musyrif_nama}</div>
            <div class="text-xs text-emerald-700 font-semibold">${s.total_juz_dicapai} Juz Dicapai (${s.achieved_juz_str})</div>
            <button onclick="openSantriModal(${s.id})" class="w-full py-1.5 rounded-lg bg-emerald-50 text-emerald-700 font-semibold text-xs border border-emerald-200">
              Lihat Rapor 30 Juz
            </button>
          </div>
        `).join('');

        tbody.innerHTML = readySantri.map(s => `
          <tr class="hover:bg-slate-50 transition">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.musyrif_nama}</div></td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800">Siap Syahadah 1</span></td>
            <td class="py-3 px-4 text-xs font-bold text-emerald-700">${s.total_juz_dicapai} Juz<div class="text-[10px] text-slate-400 font-normal">${s.achieved_juz_str}</div></td>
            <td class="py-3 px-4 text-xs text-amber-700 font-medium">${s.juziyah_count} Juziyah Tuntas</td>
            <td class="py-3 px-4 text-xs text-slate-500">Belum Ujian</td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs">Sudah melampaui batas 5 juz. Direkomendasikan segera diuji Syahadah 1.</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-100 hover:bg-slate-200">Rapor</button></td>
          </tr>
        `).join('');
        return;
      }

      // Case: Berproses (1-4 juz)
      if (currentSyahadahFilter === 'belum_proses') {
        titleElem.textContent = 'Santri yang Sedang Berproses Menuju Syahadah 1 (1 - 4 Juz)';
        const inProgress = ALL_SANTRI.filter(s => !s.has_syahadah && s.total_juz_dicapai > 0 && s.total_juz_dicapai < 5);
        countElem.textContent = `${inProgress.length} Santri`;

        mobileCards.innerHTML = inProgress.map(s => {
          const needed = 5 - s.total_juz_dicapai;
          return `
          <div class="p-3 bg-white hover:bg-slate-50 transition space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-slate-900">${s.nama}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-medium bg-blue-50 text-blue-800">Kurang ${needed} Juz</span>
            </div>
            <div class="text-[11px] text-slate-500">${s.kelas_name} • ${s.musyrif_nama}</div>
            <div class="text-xs text-blue-700 font-semibold">${s.total_juz_dicapai} dari 5 Juz (${s.achieved_juz_str})</div>
            <button onclick="openSantriModal(${s.id})" class="w-full py-1.5 rounded-lg bg-slate-100 text-slate-700 font-semibold text-xs border border-slate-200">
              Lihat Rapor
            </button>
          </div>
        `;}).join('');

        tbody.innerHTML = inProgress.map(s => `
          <tr class="hover:bg-slate-50 transition">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.musyrif_nama}</div></td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">Menuju Syahadah 1</span></td>
            <td class="py-3 px-4 text-xs font-bold text-blue-700">${s.total_juz_dicapai} / 5 Juz<div class="text-[10px] text-slate-400 font-normal">${s.achieved_juz_str}</div></td>
            <td class="py-3 px-4 text-xs text-emerald-700 font-bold">${s.total_juz_lancar} Juz Lancar</td>
            <td class="py-3 px-4 text-xs text-slate-500">Ziyadah Aktif</td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs">Kurang ${5 - s.total_juz_dicapai} juz untuk mencapai target Syahadah 1.</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-100 hover:bg-slate-200">Rapor</button></td>
          </tr>
        `).join('');
        return;
      }

      // Default: Actual Syahadah Holders
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
      countElem.textContent = `${records.length} Catatan`;

      if (records.length === 0) {
        mobileCards.innerHTML = `<div class="p-6 text-center text-xs text-slate-400">Tidak ada catatan syahadah untuk filter ini.</div>`;
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-400">Tidak ada catatan syahadah untuk filter ini.</td></tr>`;
        return;
      }

      // Render Mobile Cards
      mobileCards.innerHTML = records.map(r => {
        const s = r.santri;
        const sy = r.syahadah;
        return `
          <div class="p-3 bg-white hover:bg-slate-50 transition space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-slate-900">${s.nama}</span>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300">
                Syahadah ${sy.tingkat.toUpperCase()}
              </span>
            </div>
            <div class="flex items-center justify-between text-[11px]">
              <span class="text-slate-500">${s.kelas_name} • ${s.musyrif_nama}</span>
              <span class="font-bold text-emerald-800">${sy.predikat} (${sy.kesalahan} salah)</span>
            </div>
            <div class="text-[11px] text-slate-600 bg-slate-50 p-2 rounded-lg border border-slate-100">
              <div><strong>Cakupan:</strong> ${sy.juz_cakupan_str}</div>
              <div class="text-[10px] text-slate-400 mt-0.5">Penguji: ${sy.penguji} (${sy.created_at})</div>
              ${sy.catatan ? `<div class="italic text-[10px] text-slate-500 mt-1">"${sy.catatan}"</div>` : ''}
            </div>
            <button onclick="openSantriModal(${s.id})" class="w-full py-1.5 rounded-lg bg-emerald-50 text-emerald-800 font-semibold text-xs border border-emerald-200">
              Lihat Rapor 30 Juz
            </button>
          </div>
        `;
      }).join('');

      // Render Desktop Table
      tbody.innerHTML = records.map(r => {
        const s = r.santri;
        const sy = r.syahadah;
        let badgeClass = 'badge-mumtaz';
        if (sy.predikat.includes('Jayyid Jiddan')) badgeClass = 'badge-jayyid-jiddan';
        else if (sy.predikat.includes('Jayyid')) badgeClass = 'badge-jayyid';

        return `
          <tr class="hover:bg-slate-50 transition">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.musyrif_nama}</div></td>
            <td class="py-3 px-4"><span class="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-50 text-amber-800 border border-amber-300">Syahadah ${sy.tingkat.toUpperCase()}</span></td>
            <td class="py-3 px-4 text-xs font-medium text-slate-700">${sy.juz_cakupan_str}</td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded text-xs font-bold ${badgeClass}">${sy.predikat}</span><div class="text-[10px] text-slate-500 mt-0.5">${sy.kesalahan} kesalahan</div></td>
            <td class="py-3 px-4 text-xs"><div class="font-medium text-slate-800">${sy.penguji}</div><div class="text-[10px] text-slate-400">${sy.created_at}</div></td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs italic">"${sy.catatan}"</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-emerald-50 hover:bg-emerald-100 text-emerald-800 transition">Rapor</button></td>
          </tr>
        `;
      }).join('');
    }

    function populateSyahadahReadyList() {
      const readySantri = ALL_SANTRI.filter(s => !s.has_syahadah && s.total_juz_dicapai >= 5).sort((a,b) => b.total_juz_dicapai - a.total_juz_dicapai);
      const container = document.getElementById('list-syahadah-ready');
      container.innerHTML = readySantri.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-2 rounded-xl bg-slate-50 hover:bg-amber-50 cursor-pointer transition border border-slate-200 flex items-center justify-between">
          <div class="truncate mr-2">
            <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
            <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.musyrif_nama}</div>
          </div>
          <span class="px-2 py-0.5 rounded text-[11px] font-bold bg-amber-100 text-amber-800 shrink-0">
            ${s.total_juz_dicapai} Juz
          </span>
        </div>
      `).join('');
    }

    // 6. KELANCARAN TABLES & MOBILE LISTS
    function populateKelancaranTables() {
      // Fluent
      const fluent = [...ALL_SANTRI].filter(s => s.total_juz_lancar > 0).sort((a,b) => b.total_juz_lancar - a.total_juz_lancar);
      
      document.getElementById('list-fluent-mobile').innerHTML = fluent.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-3 bg-white hover:bg-slate-50 cursor-pointer transition flex items-center justify-between">
          <div class="truncate mr-2">
            <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
            <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.lancar_juz_str}</div>
          </div>
          <span class="px-2 py-1 rounded text-xs font-bold bg-emerald-100 text-emerald-800 shrink-0">
            ${s.total_juz_lancar} Juz Lancar
          </span>
        </div>
      `).join('');

      document.getElementById('table-fluent-students').innerHTML = fluent.map(s => `
        <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
          <td class="py-2 px-3 font-bold text-slate-900">${s.nama}</td>
          <td class="py-2 px-3 text-[11px] text-slate-500">${s.kelas_name}</td>
          <td class="py-2 px-3 font-bold text-emerald-700">${s.total_juz_lancar} Juz</td>
          <td class="py-2 px-3 text-[11px] text-slate-600 truncate max-w-xs">${s.lancar_juz_str}</td>
          <td class="py-2 px-3 text-center"><button class="px-2 py-0.5 text-[11px] font-semibold rounded bg-emerald-50 text-emerald-800">Lihat</button></td>
        </tr>
      `).join('');

      // Need Attention
      const needAttn = [...ALL_SANTRI].filter(s => s.total_tidak_lancar > 0 || s.sabtu_issues_count > 0).sort((a,b) => (b.total_tidak_lancar + b.sabtu_issues_count) - (a.total_tidak_lancar + a.sabtu_issues_count));
      
      document.getElementById('list-need-attention-mobile').innerHTML = needAttn.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-3 bg-white hover:bg-slate-50 cursor-pointer transition flex items-center justify-between">
          <div class="truncate mr-2">
            <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
            <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.total_tidak_lancar > 0 ? s.tidak_lancar_str : 'Laporan Sabtu rapuh'}</div>
          </div>
          <span class="px-2 py-1 rounded text-xs font-bold bg-rose-100 text-rose-800 shrink-0">
            ${s.total_tidak_lancar > 0 ? `${s.total_tidak_lancar} Juz Remidi` : `${s.sabtu_issues_count}x Catatan`}
          </span>
        </div>
      `).join('');

      document.getElementById('table-need-attention-students').innerHTML = needAttn.map(s => `
        <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
          <td class="py-2 px-3 font-bold text-slate-900">${s.nama}</td>
          <td class="py-2 px-3 text-[11px] text-slate-500">${s.kelas_name}</td>
          <td class="py-2 px-3 font-bold text-rose-700">${s.total_tidak_lancar > 0 ? s.tidak_lancar_str : 'Lolos Tes'}</td>
          <td class="py-2 px-3 text-[11px] text-amber-700 font-medium">${s.sabtu_issues_count} catatan</td>
          <td class="py-2 px-3 text-center"><button class="px-2 py-0.5 text-[11px] font-semibold rounded bg-rose-50 text-rose-800">Bimbing</button></td>
        </tr>
      `).join('');
    }

    // 7. GROUPING CARDS
    function populateGroupingCards() {
      // Classes
      const classContainer = document.getElementById('cards-classes-grid');
      const classes = Object.values(DB.classes_summary).filter(c => c.total_santri > 0);
      classContainer.innerHTML = classes.map(c => `
        <div onclick="filterByGroup('kelas', '${c.id}')" class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs hover:border-emerald-500 cursor-pointer transition">
          <div class="flex items-center justify-between mb-2.5">
            <h4 class="font-bold text-slate-900 text-xs sm:text-sm truncate">${c.name}</h4>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-600 shrink-0">${c.total_santri} Santri</span>
          </div>
          <div class="space-y-1.5 text-xs text-slate-500">
            <div class="flex justify-between"><span>Aktif:</span><strong class="text-slate-700">${c.aktif}</strong></div>
            <div class="flex justify-between"><span>Rata-rata Hafal:</span><strong class="text-emerald-700 font-bold">${c.avg_juz_dicapai} Juz</strong></div>
            <div class="flex justify-between"><span>Rata-rata Lancar:</span><strong class="text-teal-700 font-bold">${c.avg_juz_lancar} Juz</strong></div>
            <div class="flex justify-between"><span>Lulus Syahadah:</span><strong class="text-amber-700 font-bold">${c.syahadah_holders} (${c.syahadah_pct}%)</strong></div>
          </div>
        </div>
      `).join('');

      // Halaqah
      const halaqahContainer = document.getElementById('cards-halaqah-grid');
      const halaqahs = Object.values(DB.halaqah_summary);
      halaqahContainer.innerHTML = halaqahs.map(h => `
        <div onclick="filterByGroup('halaqah', '${h.musyrif_nama}')" class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs hover:border-teal-500 cursor-pointer transition">
          <div class="flex items-center justify-between mb-2.5">
            <h4 class="font-bold text-slate-900 text-xs sm:text-sm truncate mr-2" title="${h.musyrif_nama}">${h.musyrif_nama}</h4>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-50 text-teal-800 shrink-0">${h.total_santri} Santri</span>
          </div>
          <div class="space-y-1.5 text-xs text-slate-500">
            <div class="flex justify-between"><span>Santri Aktif:</span><strong class="text-slate-700">${h.aktif}</strong></div>
            <div class="flex justify-between"><span>Total Juz:</span><strong class="text-emerald-700 font-bold">${h.total_juz_dicapai} Juz</strong></div>
            <div class="flex justify-between"><span>Rata-rata/Santri:</span><strong class="text-slate-700">${h.avg_juz_dicapai} Juz</strong></div>
            <div class="flex justify-between"><span>Lulus Syahadah:</span><strong class="text-amber-700 font-bold">${h.syahadah_holders} (${h.syahadah_pct}%)</strong></div>
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

    // 8. SANTRI DIRECTORY (MOBILE CARDS + DESKTOP TABLE)
    function initHalaqahFilterDropdown() {
      const select = document.getElementById('filterHalaqah');
      const names = Object.keys(DB.halaqah_summary);
      select.innerHTML = '<option value="semua">Semua Halaqah</option>' + 
        names.map(name => `<option value="${name}">${name}</option>`).join('');
    }

    function applyFilters() {
      const q = document.getElementById('searchInput').value.toLowerCase().trim();
      const k = document.getElementById('filterKelas').value;
      const h = document.getElementById('filterHalaqah').value;
      const sy = document.getElementById('filterSyahadah').value;

      filteredSantri = ALL_SANTRI.filter(s => {
        if (q) {
          const matchName = s.nama.toLowerCase().includes(q);
          const matchNis = s.nis.toLowerCase().includes(q);
          const matchNik = s.nik.toLowerCase().includes(q);
          if (!matchName && !matchNis && !matchNik) return false;
        }

        if (k !== 'semua') {
          if (k === 'alumni') {
            if (!s.kelas_name.includes('Alumni')) return false;
          } else {
            if (s.kelas_id !== k) return false;
          }
        }

        if (h !== 'semua' && s.musyrif_nama !== h) return false;

        if (sy === 'sudah_syahadah' && !s.has_syahadah) return false;
        if (sy === 'siap_syahadah' && (s.has_syahadah || s.total_juz_dicapai < 5)) return false;
        if (sy === 'berproses' && (s.has_syahadah || s.total_juz_dicapai === 0 || s.total_juz_dicapai >= 5)) return false;
        if (sy === 'belum_syahadah' && s.has_syahadah) return false;

        return true;
      });

      sortFilteredSantri();
      renderSantriViews();
    }

    function resetFilters() {
      document.getElementById('searchInput').value = '';
      document.getElementById('filterKelas').value = 'semua';
      document.getElementById('filterHalaqah').value = 'semua';
      document.getElementById('filterSyahadah').value = 'semua';
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
      renderSantriViews();
    }

    function sortFilteredSantri() {
      filteredSantri.sort((a,b) => {
        let valA, valB;
        if (currentSort.column === 'nama') {
          valA = a.nama.toLowerCase(); valB = b.nama.toLowerCase();
        } else if (currentSort.column === 'kelas') {
          valA = a.kelas_name; valB = b.kelas_name;
        } else if (currentSort.column === 'halaqah') {
          valA = a.musyrif_nama; valB = b.musyrif_nama;
        } else if (currentSort.column === 'juz_dicapai') {
          valA = a.total_juz_dicapai; valB = b.total_juz_dicapai;
        } else if (currentSort.column === 'juz_lancar') {
          valA = a.total_juz_lancar; valB = b.total_juz_lancar;
        }
        if (valA < valB) return currentSort.asc ? -1 : 1;
        if (valA > valB) return currentSort.asc ? 1 : -1;
        return 0;
      });
    }

    function renderSantriViews() {
      document.getElementById('filterResultCount').textContent = filteredSantri.length;
      const mobileContainer = document.getElementById('santriMobileCards');
      const tableBody = document.getElementById('santriTableBody');

      if (filteredSantri.length === 0) {
        mobileContainer.innerHTML = `<div class="p-8 text-center text-xs text-slate-400 bg-white rounded-2xl border border-slate-200">Tidak ada santri yang sesuai kriteria pencarian.</div>`;
        tableBody.innerHTML = `<tr><td colspan="8" class="text-center py-10 text-slate-400">Tidak ada santri yang sesuai kriteria pencarian.</td></tr>`;
        return;
      }

      // 1. Mobile Cards View
      mobileContainer.innerHTML = filteredSantri.map(s => {
        const pct = Math.round((s.total_juz_dicapai / 30) * 100);
        let badgeSy = '';
        if (s.has_syahadah) {
          badgeSy = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">Syahadah ${s.highest_syahadah.toUpperCase()}</span>`;
        } else if (s.total_juz_dicapai >= 5) {
          badgeSy = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">Siap Ujian 1</span>`;
        }

        return `
          <div onclick="openSantriModal(${s.id})" class="bg-white rounded-2xl p-3.5 border border-slate-200 shadow-xs space-y-2.5 active:scale-[0.99] transition cursor-pointer">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-slate-900">${s.nama}</h4>
                <div class="text-[10px] text-slate-400">NIS: ${s.nis} • ${s.kelas_name}</div>
              </div>
              <div class="text-right">
                ${badgeSy}
              </div>
            </div>

            <!-- Progress Bar -->
            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-500">Capaian: <strong class="text-emerald-700">${s.total_juz_dicapai} Juz</strong></span>
                <span class="text-teal-700 font-semibold">${s.total_juz_lancar} Juz Lancar</span>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: ${pct}%"></div>
              </div>
            </div>

            <div class="flex items-center justify-between pt-1 border-t border-slate-100 text-[10px] text-slate-400">
              <span class="truncate max-w-[200px]">${s.musyrif_nama}</span>
              <span class="font-semibold text-emerald-700">Buka Rapor &rarr;</span>
            </div>
          </div>
        `;
      }).join('');

      // 2. Desktop Table View
      tableBody.innerHTML = filteredSantri.map(s => {
        const pct = Math.round((s.total_juz_dicapai / 30) * 100);
        let syahadahBadge = '<span class="text-slate-400 text-xs">-</span>';
        if (s.has_syahadah) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300">Syahadah ${s.highest_syahadah.toUpperCase()}</span>`;
        } else if (s.total_juz_dicapai >= 5) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-300">Siap Ujian 1</span>`;
        }

        return `
          <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.jenis_kelamin}</div></td>
            <td class="py-3 px-4 text-xs font-medium text-slate-700 truncate max-w-[180px]">${s.musyrif_nama}</td>
            <td class="py-3 px-4">
              <div class="flex items-center gap-1.5"><span class="font-bold text-emerald-700 text-xs">${s.total_juz_dicapai} Juz</span><span class="text-[10px] text-slate-400">(${pct}%)</span></div>
              <div class="w-16 bg-slate-100 rounded-full h-1 mt-1 overflow-hidden"><div class="bg-emerald-500 h-1 rounded-full" style="width: ${pct}%"></div></div>
            </td>
            <td class="py-3 px-4 font-bold text-teal-700 text-xs">${s.total_juz_lancar} Juz</td>
            <td class="py-3 px-4">${syahadahBadge}</td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700">${s.fluency_label}</span></td>
            <td class="py-3 px-4 text-center"><button class="px-3 py-1 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs">Rapor</button></td>
          </tr>
        `;
      }).join('');
    }

    // 9. MODAL INTERAKTIF 30 JUZ
    function openSantriModal(santriId) {
      const s = ALL_SANTRI.find(item => item.id === santriId);
      if (!s) return;
      currentModalSantri = s;

      document.getElementById('modal-avatar').textContent = s.nama.charAt(0);
      document.getElementById('modal-nama').textContent = s.nama;
      document.getElementById('modal-status').textContent = s.status;
      document.getElementById('modal-nis').textContent = `NIS: ${s.nis}`;
      document.getElementById('modal-kelas').textContent = s.kelas_name;
      document.getElementById('modal-halaqah').textContent = s.musyrif_nama;

      document.getElementById('modal-juz-dicapai').textContent = `${s.total_juz_dicapai} Juz`;
      document.getElementById('modal-juz-lancar').textContent = `${s.total_juz_lancar} Juz`;

      if (s.has_syahadah) {
        document.getElementById('modal-syahadah-highest').textContent = `Syahadah ${s.highest_syahadah.toUpperCase()}`;
        document.getElementById('modal-syahadah-count').textContent = `${s.syahadah_count} Sertifikat Lulus`;
      } else {
        document.getElementById('modal-syahadah-highest').textContent = 'Belum Ada';
        document.getElementById('modal-syahadah-count').textContent = s.total_juz_dicapai >= 5 ? 'Siap Ujian 1' : 'Dalam Proses';
      }

      document.getElementById('modal-fluency-badge').textContent = s.fluency_label;
      document.getElementById('modal-tidak-lancar-count').textContent = `${s.total_tidak_lancar} Remidi • ${s.sabtu_issues_count} Rapuh`;

      document.getElementById('modal-target-title').textContent = s.syahadah_status_summary;
      document.getElementById('modal-target-pct').textContent = `${s.syahadah_progress_pct}%`;
      document.getElementById('modal-target-bar').style.width = `${s.syahadah_progress_pct}%`;
      document.getElementById('modal-target-desc').textContent = `Status Terakhir: ${s.last_achievement ? `${s.last_achievement.type.toUpperCase()} di Juz ${s.last_achievement.juz || '-'}` : 'Belum ada setoran'}`;

      // 30 Juz Grid (Touchable Tiles)
      const grid = document.getElementById('modal-juz-grid');
      grid.innerHTML = s.juz_grid.map(g => {
        let style = 'bg-slate-100 text-slate-400 border-slate-200';
        if (g.status === 'lancar') style = 'bg-emerald-500 text-white font-bold border-emerald-600 shadow-xs';
        else if (g.status === 'belum_tes') style = 'bg-amber-400 text-amber-950 font-bold border-amber-500';
        else if (g.status === 'tidak_lancar') style = 'bg-rose-500 text-white font-bold border-rose-600';

        return `
          <button onclick="selectJuzTile(${g.juz})" type="button" class="p-1.5 sm:p-2 rounded-xl border text-center transition active:scale-95 ${style}">
            <div class="text-[10px] sm:text-xs font-black">J${g.juz}</div>
            <div class="text-[8px] sm:text-[9px] mt-0.5 truncate">${g.status === 'lancar' ? 'Lancar' : (g.status === 'belum_tes' ? 'Tuntas' : (g.status === 'tidak_lancar' ? 'Remidi' : '-'))}</div>
          </button>
        `;
      }).join('');

      // Select first active juz or Juz 1
      selectJuzTile(s.achieved_juz_list.length > 0 ? s.achieved_juz_list[0] : 1);

      // Syahadah History
      const sySection = document.getElementById('modal-syahadah-section');
      const syList = document.getElementById('modal-syahadah-list');
      if (s.syahadahs.length > 0) {
        sySection.classList.remove('hidden');
        syList.innerHTML = s.syahadahs.map(sy => `
          <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-xs space-y-1">
            <div class="flex items-center justify-between font-bold text-amber-900">
              <span>Syahadah ${sy.tingkat.toUpperCase()} (${sy.juz_cakupan_str})</span>
              <span class="px-2 py-0.5 rounded bg-amber-200 text-amber-900">${sy.predikat} (${sy.kesalahan} salah)</span>
            </div>
            <div class="text-[10px] text-slate-500">Penguji: ${sy.penguji} • ${sy.created_at}</div>
            ${sy.catatan ? `<div class="italic text-[10px] text-slate-600">"${sy.catatan}"</div>` : ''}
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
        evList.innerHTML = s.sabtu_issues.slice(0, 4).map(iss => `
          <div class="p-2 rounded-lg bg-rose-50 border border-rose-200 text-xs flex items-center justify-between">
            <div>
              <strong class="text-rose-800">Juz ${iss.juz || '-'}</strong>
              <span class="text-slate-500 ml-1.5 text-[11px]">Hal ${iss.startPage} s.d. ${iss.endPage}</span>
            </div>
            <span class="text-[10px] text-slate-400">${iss.tanggal}</span>
          </div>
        `).join('');
      } else {
        evSection.classList.add('hidden');
      }

      // Recommendation
      let rek = `Alhamdulillah, ananda ${s.nama} saat ini telah menyelesaikan ${s.total_juz_dicapai} Juz. `;
      if (s.total_tidak_lancar > 0) {
        rek += `Sangat dianjurkan untuk memperkuat murajaah pada ${s.tidak_lancar_str} yang sebelumnya tercatat remidi sebelum menambah ziyadah baru. `;
      }
      if (s.total_juz_dicapai >= 5 && !s.has_syahadah) {
        rek += `Ananda sudah siap secara kapasitas untuk mengambil Ujian Syahadah 1 (5 Juz). Mohon bantuan orang tua di rumah untuk menyimak murajaah sambung ayat. `;
      } else if (s.has_syahadah) {
        rek += `Pertahankan pencapaian mutqin Syahadah ${s.highest_syahadah} dengan konsisten tadarus 1 juz per hari.`;
      } else {
        rek += `Pertahankan kedisiplinan setoran harian bersama musyrif halaqah.`;
      }
      document.getElementById('modal-rekomendasi').textContent = rek;

      // Show modal
      document.getElementById('santriModal').classList.remove('hidden');
      lucide.createIcons();
    }

    function selectJuzTile(juzNum) {
      if (!currentModalSantri) return;
      const g = currentModalSantri.juz_grid.find(item => item.juz === juzNum);
      if (!g) return;

      document.getElementById('selected-juz-badge').textContent = g.juz;
      document.getElementById('selected-juz-title').textContent = `Juz ${g.juz}`;
      document.getElementById('selected-juz-surah').textContent = `(${g.surah})`;
      document.getElementById('selected-juz-status').textContent = g.label;

      const statusElem = document.getElementById('selected-juz-status');
      if (g.status === 'lancar') {
        statusElem.className = 'text-[11px] font-bold text-emerald-700 shrink-0';
      } else if (g.status === 'tidak_lancar') {
        statusElem.className = 'text-[11px] font-bold text-rose-700 shrink-0';
      } else if (g.status === 'belum_tes') {
        statusElem.className = 'text-[11px] font-bold text-amber-700 shrink-0';
      } else {
        statusElem.className = 'text-[11px] font-semibold text-slate-400 shrink-0';
      }
    }

    function closeSantriModal() {
      document.getElementById('santriModal').classList.add('hidden');
      currentModalSantri = null;
    }

    // 10. EXPORT TO CSV
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

    // 11. INITIALIZATION ON LOAD
    document.addEventListener('DOMContentLoaded', () => {
      populateExecutiveHighlights();
      renderAllCharts();
      populateSyahadahReadyList();
      renderSyahadahTable();
      populateKelancaranTables();
      populateGroupingCards();
      initHalaqahFilterDropdown();
      renderSantriViews();
      lucide.createIcons();
    });
  </script>

</body>
</html>
"""

final_html = html_content.replace('DATA_JSON_PLACEHOLDER', json_data_str)

output_path = 'index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Generated mobile-optimized index.html successfully! Size: {os.path.getsize(output_path) / 1024:.2f} KB")
