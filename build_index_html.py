# -*- coding: utf-8 -*-
import json
import os
import subprocess

# Automatically extract latest data from SQLite if needed
if os.path.exists('process_classes_123.py') and os.path.exists('everynight-in-my-dream.db'):
    if not os.path.exists('full_report_dataset.json') or os.path.getmtime('everynight-in-my-dream.db') > os.path.getmtime('full_report_dataset.json'):
        print("Mengekstrak data terbaru dari SQLite (Kelas 1, 2, & 3)...")
        subprocess.run(['python', 'process_classes_123.py'], check=True)

with open('full_report_dataset.json', encoding='utf-8') as f:
    dataset = json.load(f)

json_data_str = json.dumps(dataset, ensure_ascii=False)

html_content = """<!DOCTYPE html>
<html lang="id" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Laporan Capaian Tahfidz Santri Kelas 1, 2, & 3 | Dashboard Eksekutif</title>
  
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
    html, body {
      -webkit-tap-highlight-color: transparent;
      touch-action: manipulation;
    }
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    @media (min-width: 768px) {
      ::-webkit-scrollbar { width: 7px; height: 7px; }
      ::-webkit-scrollbar-track { background: #f8fafc; }
      ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
      ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
    }
    @media print {
      body { background: white !important; color: black !important; font-size: 11pt !important; }
      .no-print { display: none !important; }
      .print-break { page-break-before: always; }
      .shadow-sm, .shadow-md, .shadow-lg { box-shadow: none !important; border: 1px solid #e2e8f0 !important; }
    }
    .badge-mumtaz { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
    .badge-jayyid-jiddan { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-jayyid { background: #fefce8; color: #a16207; border: 1px solid #fef08a; }
  </style>
</head>

<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col font-sans">

  <!-- TOP HEADER & CONTEXT BAR -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40 shadow-xs">
    
    <!-- Top Micro Bar -->
    <div class="bg-emerald-900 text-emerald-100 text-[11px] py-1.5 px-3 sm:px-4 flex items-center justify-between no-print">
      <div class="flex items-center gap-2 truncate">
        <span class="inline-flex items-center px-1.5 py-0.2 rounded-full text-[10px] font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1 animate-pulse"></span>
          Santri Aktif (Kelas 1, 2, & 3)
        </span>
        <span class="hidden sm:inline text-emerald-200/60">•</span>
        <span class="truncate hidden sm:inline">Pesantren Tahfidzul Quran — Basis Data Terverifikasi</span>
      </div>
      <div class="flex items-center gap-3 shrink-0 text-emerald-200 text-[10px] sm:text-[11px]">
        <span id="topBarUpdateDate">Pembaruan: Rabu, 18 November 2026</span>
        <button onclick="window.print()" class="hover:text-white transition flex items-center gap-1 font-medium bg-emerald-800/80 hover:bg-emerald-700/80 px-2 py-0.5 rounded border border-emerald-700">
          <i data-lucide="printer" class="w-3 h-3"></i>
          <span class="hidden sm:inline">Cetak / PDF</span>
        </button>
      </div>
    </div>

    <!-- Main Header Bar -->
    <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14 sm:h-16 gap-2 sm:gap-4">
        
        <!-- Brand / Identity -->
        <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
          <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-teal-700 flex items-center justify-center text-white shadow-xs shrink-0 font-bold font-arabic text-base sm:text-lg">
            ق
          </div>
          <div class="truncate">
            <h1 class="text-sm sm:text-lg font-bold text-slate-900 leading-tight truncate flex items-center gap-1.5">
              <span>Laporan Capaian Tahfidz</span>
              <span class="text-[10px] sm:text-xs font-semibold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 border border-emerald-200 hidden xs:inline">
                Kelas 1, 2, & 3
              </span>
            </h1>
            <p class="text-[10px] sm:text-xs text-slate-500 truncate">
              Evaluasi Hafalan, Syahadah 5-Juz, & Mutqin Santri
            </p>
          </div>
        </div>

        <!-- Quick Header Actions -->
        <div class="flex items-center gap-1.5 sm:gap-2 shrink-0 no-print">
          <button onclick="exportToCSV()" class="px-2.5 sm:px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 transition flex items-center gap-1 shadow-2xs">
            <i data-lucide="download" class="w-3.5 h-3.5 text-emerald-700"></i>
            <span class="hidden md:inline">Ekspor</span> CSV
          </button>
        </div>

      </div>

      <!-- Navigation Tabs (Touch-friendly & Horizontal Scroll on Mobile) -->
      <nav class="flex space-x-1 sm:space-x-2 border-t border-slate-100 overflow-x-auto py-2 no-scrollbar no-print" id="mainTabs">
        <button onclick="switchTab('ringkasan')" id="tab-ringkasan" class="tab-btn active px-3 py-2 text-xs sm:text-sm font-semibold rounded-lg transition flex items-center gap-1.5 shrink-0 bg-emerald-50 text-emerald-800 border border-emerald-300">
          <i data-lucide="bar-chart-3" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-600"></i>
          <span>1. Ringkasan</span>
        </button>
        <button onclick="switchTab('syahadah')" id="tab-syahadah" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="award" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-amber-500"></i>
          <span>2. Syahadah</span>
        </button>
        <button onclick="switchTab('kelancaran')" id="tab-kelancaran" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="check-circle-2" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-teal-600"></i>
          <span>3. Kelancaran</span>
        </button>
        <button onclick="switchTab('grouping')" id="tab-grouping" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="users-2" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-blue-600"></i>
          <span>4. Kelas & Halaqah</span>
        </button>
        <button onclick="switchTab('santri')" id="tab-santri" class="tab-btn px-3 py-2 text-xs sm:text-sm font-medium rounded-lg transition flex items-center gap-1.5 shrink-0 text-slate-600 hover:text-slate-900 hover:bg-slate-100">
          <i data-lucide="list-filter" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-indigo-600"></i>
          <span>5. Direktori Santri</span>
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
    <!-- GLOBAL FILTER: RENTANG WAKTU (DATE RANGE FILTER) -->
    <!-- ========================================================================================= -->
    <section class="bg-white rounded-2xl sm:rounded-3xl border border-emerald-200/90 shadow-xs p-4 sm:p-5 no-print">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
        
        <!-- Title & Active Badge -->
        <div class="flex items-start sm:items-center gap-3">
          <div class="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 shadow-xs">
            <i data-lucide="calendar-range" class="w-5 h-5 text-emerald-700"></i>
          </div>
          <div>
            <div class="flex items-center gap-2 flex-wrap">
              <h2 class="text-sm sm:text-base font-extrabold text-slate-900 tracking-tight">
                Filter Rentang Waktu Laporan
              </h2>
              <span id="badgeActivePeriod" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                <span id="badgeActivePeriodText">Semua Waktu</span>
              </span>
            </div>
            <p class="text-xs text-slate-500 mt-0.5" id="dateFilterDescription">
              Menampilkan seluruh pencapaian sejak awal tahun ajaran. Pilih tanggal atau klik tombol pintas di bawah untuk memfilter rentang waktu tertentu.
            </p>
          </div>
        </div>

        <!-- Date Inputs & Actions -->
        <div class="flex flex-col sm:flex-row sm:items-end gap-2.5">
          <div class="flex items-center gap-2">
            <div class="flex-1 sm:w-40">
              <label for="filterStartDate" class="block text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                Dari Tanggal
              </label>
              <input type="date" id="filterStartDate" onchange="onDateInputChange()" class="w-full text-xs font-semibold px-3 py-2 bg-slate-50 hover:bg-white focus:bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-slate-800 cursor-pointer">
            </div>
            <span class="text-slate-400 font-bold self-end pb-2.5 text-xs">s/d</span>
            <div class="flex-1 sm:w-40">
              <label for="filterEndDate" class="block text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                Sampai Tanggal
              </label>
              <input type="date" id="filterEndDate" onchange="onDateInputChange()" class="w-full text-xs font-semibold px-3 py-2 bg-slate-50 hover:bg-white focus:bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition text-slate-800 cursor-pointer">
            </div>
          </div>

          <div class="flex items-center gap-1.5">
            <button onclick="applyDateRangeFilter()" class="flex-1 sm:flex-initial px-4 py-2 text-xs font-bold rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs transition flex items-center justify-center gap-1.5 shrink-0 active:scale-95">
              <i data-lucide="filter" class="w-3.5 h-3.5"></i>
              <span>Terapkan</span>
            </button>
            <button onclick="resetDateRangeFilter()" title="Kembalikan ke Semua Waktu" class="px-3 py-2 text-xs font-semibold rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center justify-center gap-1 shrink-0 active:scale-95">
              <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
              <span class="hidden sm:inline">Semua Waktu</span>
            </button>
          </div>
        </div>

      </div>

      <!-- Quick Preset Buttons -->
      <div class="mt-3.5 pt-3 border-t border-slate-100 flex flex-wrap items-center gap-1.5">
        <span class="text-[11px] font-bold text-slate-400 mr-1 flex items-center gap-1">
          <i data-lucide="sparkles" class="w-3 h-3 text-amber-500"></i> Pilihan Cepat:
        </span>
        <button type="button" onclick="setPresetRange('all')" id="preset-btn-all" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-bold bg-emerald-600 text-white shadow-2xs transition">
          Semua Waktu
        </button>
        <button type="button" onclick="setPresetRange('user_example')" id="preset-btn-user_example" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 transition flex items-center gap-1">
          <span>🎯 Contoh: 1 Jul – 3 Okt 2026</span>
        </button>
        <button type="button" onclick="setPresetRange('sem1_2026')" id="preset-btn-sem1_2026" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
          Semester Ganjil 2026
        </button>
        <button type="button" onclick="setPresetRange('sem2_2026')" id="preset-btn-sem2_2026" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
          Semester Genap 2026
        </button>
        <button type="button" onclick="setPresetRange('last_30d')" id="preset-btn-last_30d" class="preset-btn px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
          30 Hari Terakhir
        </button>
      </div>

      <!-- Active Period Notification Bar -->
      <div id="activePeriodAlertBar" class="mt-3 p-3 rounded-xl bg-emerald-50 border border-emerald-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
        <div class="flex items-start sm:items-center gap-2 text-emerald-950">
          <i data-lucide="info" class="w-4 h-4 text-emerald-700 shrink-0 mt-0.5 sm:mt-0"></i>
          <div>
            <span class="font-bold">Periode Aktif: </span>
            <span id="activePeriodSpanText" class="font-semibold text-emerald-900">Jumat, 16 Januari 2026 s/d Rabu, 18 November 2026</span>
            <span id="activePeriodStatsText" class="text-slate-600 ml-1">(Menampilkan seluruh riwayat santri)</span>
          </div>
        </div>
        <button id="btnResetInline" onclick="resetDateRangeFilter()" class="text-xs font-bold text-emerald-700 hover:text-emerald-900 underline self-start sm:self-auto shrink-0 hidden">
          Kembalikan ke Semua Waktu
        </button>
      </div>

    </section>

    <!-- ========================================================================================= -->
    <!-- TAB 1: RINGKASAN EKSEKUTIF -->
    <!-- ========================================================================================= -->
    <div id="content-ringkasan" class="tab-content space-y-6">

      <!-- Executive KPI Cards -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2.5 sm:gap-4">
        
        <!-- KPI 1: Santri -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Santri Terdaftar</span>
              <i data-lucide="users" class="w-4 h-4 text-emerald-600"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-slate-900" id="kpi-total-santri">44</div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-santri">
            <span class="text-emerald-700 font-semibold">42 Aktif</span> • 2 Non-aktif
          </div>
        </div>

        <!-- KPI 2: Syahadah -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Lulus Syahadah</span>
              <i data-lucide="award" class="w-4 h-4 text-amber-500"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-amber-900" id="kpi-total-syahadah">19</div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-syahadah">
            22 Sertifikat Kelulusan
          </div>
        </div>

        <!-- KPI 3: Total Hafalan -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Akumulasi Hafal</span>
              <i data-lucide="book-open" class="w-4 h-4 text-emerald-600"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-emerald-800" id="kpi-total-juz">334 <span class="text-xs font-normal text-slate-500">Juz</span></div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-juz">
            Rata-rata 7,6 Juz/Santri
          </div>
        </div>

        <!-- KPI 4: Mutqin / Lancar -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Teruji Mutqin</span>
              <i data-lucide="check-circle" class="w-4 h-4 text-teal-600"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-teal-800" id="kpi-total-lancar">96 <span class="text-xs font-normal text-slate-500">Juz</span></div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-lancar">
            Lolos Ujian Kelancaran
          </div>
        </div>

        <!-- KPI 5: Riwayat Catatan -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Total Aktivitas</span>
              <i data-lucide="file-text" class="w-4 h-4 text-blue-600"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-slate-800" id="kpi-total-pencapaian">3.670</div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-pencapaian">
            3.449 Setor • 221 Tes
          </div>
        </div>

        <!-- KPI 6: Laporan Sabtu -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Evaluasi Musyrif</span>
              <i data-lucide="clipboard-check" class="w-4 h-4 text-indigo-600"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-slate-800" id="kpi-total-sabtu">226</div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-sabtu">
            Laporan Evaluasi Sabtu
          </div>
        </div>

      </div>

      <!-- Panduan Awam Banner -->
      <div class="bg-gradient-to-r from-emerald-50 via-teal-50 to-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 border border-emerald-200 shadow-xs">
        <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div class="space-y-1 max-w-2xl">
            <div class="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-800 uppercase tracking-wider">
              <i data-lucide="sparkles" class="w-4 h-4 text-amber-500"></i>
              Panduan Cepat Membaca Laporan
            </div>
            <h3 class="text-base sm:text-lg font-bold text-slate-900">
              Bagaimana Tahapan & Standar Hafalan Santri di Pesantren?
            </h3>
            <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Santri memulai hafalan dari <strong>Juz 30</strong>, lalu <strong>Juz 29</strong>, kemudian Juz 1 s.d. 28. Setiap menyelesaikan 5 Juz (misal: Juz 30, 29, 1, 2, 3), santri diuji dalam ujian akbar <strong>Syahadah</strong> sekali duduk.
            </p>
          </div>
          <div class="flex items-center gap-2 self-stretch md:self-auto shrink-0">
            <button onclick="switchTab('panduan')" class="w-full md:w-auto px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-xs sm:text-sm font-semibold transition flex items-center justify-center gap-2 shadow-xs">
              <i data-lucide="book-open" class="w-4 h-4"></i>
              <span>Baca Panduan Lengkap</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Charts Section (Grid 2 Cols) -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        
        <!-- Chart 1: Per Jenjang Kelas -->
        <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h4 class="font-bold text-sm sm:text-base text-slate-900">Komparasi Capaian per Jenjang Kelas</h4>
              <p class="text-xs text-slate-500">Rata-rata hafalan (Juz) santri Kelas 1 (Ula), Kelas 2 (Wustho), & Kelas 3 (Ulya)</p>
            </div>
            <span class="p-2 bg-emerald-50 text-emerald-700 rounded-xl">
              <i data-lucide="bar-chart-2" class="w-4 h-4"></i>
            </span>
          </div>
          <div class="h-64 sm:h-72 w-full">
            <canvas id="chartClassComparison"></canvas>
          </div>
        </div>

        <!-- Chart 2: Status Syahadah -->
        <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs">
          <div class="flex items-center justify-between mb-4">
            <div>
              <h4 class="font-bold text-sm sm:text-base text-slate-900">Proporsi Kesiapan & Kelulusan Syahadah</h4>
              <p class="text-xs text-slate-500">Distribusi santri yang telah lulus, siap ujian (&ge;5 juz), dan sedang berproses</p>
            </div>
            <span class="p-2 bg-amber-50 text-amber-700 rounded-xl">
              <i data-lucide="pie-chart" class="w-4 h-4"></i>
            </span>
          </div>
          <div class="h-64 sm:h-72 w-full">
            <canvas id="chartSyahadahStatus"></canvas>
          </div>
        </div>

        <!-- Chart 3: Peta Kendala Juz -->
        <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs lg:col-span-2">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
            <div>
              <h4 class="font-bold text-sm sm:text-base text-slate-900">Peta Tingkat Kesulitan 30 Juz Al-Qur'an</h4>
              <p class="text-xs text-slate-500">Frekuensi catatan evaluasi Sabtu dan tes kelancaran yang belum lulus per juz</p>
            </div>
            <div class="flex items-center gap-3 text-xs">
              <span class="flex items-center gap-1.5 text-rose-600 font-medium">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Belum Lulus Tes
              </span>
              <span class="flex items-center gap-1.5 text-amber-600 font-medium">
                <span class="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Catatan Rapuh Sabtu
              </span>
            </div>
          </div>
          <div class="h-64 sm:h-80 w-full">
            <canvas id="chartJuzIssuesFull"></canvas>
          </div>
        </div>

      </div>

      <!-- Highlight Lists: Top Achievers, Top Lancar, & Juz Paling Menantang -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
        
        <!-- List 1: Top Capaian Hafalan -->
        <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <h4 class="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-1.5">
                <i data-lucide="crown" class="w-4 h-4 text-amber-500"></i>
                Top Capaian Hafalan
              </h4>
              <span class="text-[10px] font-semibold text-slate-400">Akumulasi</span>
            </div>
            <div class="space-y-2" id="list-top-achievers">
              <!-- Rendered via JS -->
            </div>
          </div>
          <button onclick="switchTab('santri')" class="mt-4 w-full py-2 text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 rounded-xl transition text-center">
            Lihat Semua Santri &rarr;
          </button>
        </div>

        <!-- List 2: Top Mutqin (Lancar Teruji) -->
        <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <h4 class="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-1.5">
                <i data-lucide="award" class="w-4 h-4 text-teal-600"></i>
                Top Mutqin (Lancar Teruji)
              </h4>
              <span class="text-[10px] font-semibold text-slate-400">Hasil Tes</span>
            </div>
            <div class="space-y-2" id="list-top-fluent">
              <!-- Rendered via JS -->
            </div>
          </div>
          <button onclick="switchTab('kelancaran')" class="mt-4 w-full py-2 text-xs font-semibold text-teal-700 bg-teal-50 hover:bg-teal-100 rounded-xl transition text-center">
            Detail Kelancaran &rarr;
          </button>
        </div>

        <!-- List 3: Juz Paling Menantang -->
        <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-3">
              <h4 class="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-1.5">
                <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-500"></i>
                Juz Paling Menantang
              </h4>
              <span class="text-[10px] font-semibold text-slate-400">Paling Sering Rapuh</span>
            </div>
            <div class="space-y-2" id="list-challenging-juz">
              <!-- Rendered via JS -->
            </div>
          </div>
          <div class="mt-4 text-[11px] text-slate-500 bg-slate-50 p-2.5 rounded-xl border border-slate-100">
            💡 Juz di atas paling banyak memerlukan pengulangan murajaah sebelum naik jenjang berikutnya.
          </div>
        </div>

      </div>

    </div>

    <!-- ========================================================================================= -->
    <!-- TAB 2: LAPORAN SYAHADAH -->
    <!-- ========================================================================================= -->
    <div id="content-syahadah" class="tab-content hidden space-y-6">

      <!-- Header & Penjelasan Awam Syahadah -->
      <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 border border-slate-200 shadow-xs space-y-3">
        <div class="flex items-center gap-2.5">
          <span class="p-2.5 bg-amber-100 text-amber-800 rounded-2xl">
            <i data-lucide="award" class="w-6 h-6"></i>
          </span>
          <div>
            <h3 class="text-base sm:text-lg font-bold text-slate-900">Ujian Syahadah (5 Juz Sekali Duduk)</h3>
            <p class="text-xs sm:text-sm text-slate-500">Sertifikasi kemutqinan resmi santri dengan standar maksimal 40 kesalahan per paket 5 juz.</p>
          </div>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-2 border-t border-slate-100 text-xs">
          <div class="p-2.5 rounded-xl bg-amber-50/70 border border-amber-200">
            <div class="font-bold text-amber-900">Syahadah 1 (5 Juz)</div>
            <div class="text-[11px] text-amber-800">Juz 30, 29, 1, 2, 3</div>
          </div>
          <div class="p-2.5 rounded-xl bg-amber-50/70 border border-amber-200">
            <div class="font-bold text-amber-900">Syahadah 2 (10 Juz)</div>
            <div class="text-[11px] text-amber-800">Juz 4, 5, 6, 7, 8</div>
          </div>
          <div class="p-2.5 rounded-xl bg-amber-50/70 border border-amber-200">
            <div class="font-bold text-amber-900">Syahadah 3 (15 Juz)</div>
            <div class="text-[11px] text-amber-800">Juz 9, 10, 11, 12, 13</div>
          </div>
          <div class="p-2.5 rounded-xl bg-amber-50/70 border border-amber-200">
            <div class="font-bold text-amber-900">Syahadah 4 (20 Juz)</div>
            <div class="text-[11px] text-amber-800">Juz 14, 15, 16, 17, 18</div>
          </div>
        </div>
      </div>

      <!-- Filter Buttons Subtab Syahadah -->
      <div class="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
        <button onclick="filterSyahadahTab('semua')" id="subtab-sy-semua" class="subtab-sy-btn active px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 text-white transition shrink-0">
          Semua Lulusan (22 Sertifikat)
        </button>
        <button onclick="filterSyahadahTab('pertama')" id="subtab-sy-pertama" class="subtab-sy-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition shrink-0">
          Syahadah 1 (12)
        </button>
        <button onclick="filterSyahadahTab('kedua')" id="subtab-sy-kedua" class="subtab-sy-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition shrink-0">
          Syahadah 2 (5)
        </button>
        <button onclick="filterSyahadahTab('ketiga')" id="subtab-sy-ketiga" class="subtab-sy-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition shrink-0">
          Syahadah 3 (3)
        </button>
        <button onclick="filterSyahadahTab('keempat')" id="subtab-sy-keempat" class="subtab-sy-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition shrink-0">
          Syahadah 4 (2)
        </button>
        <button onclick="filterSyahadahTab('belum_siap')" id="subtab-sy-belum-siap" class="subtab-sy-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-amber-100 hover:bg-amber-200 text-amber-900 transition shrink-0">
          Siap Ujian Syahadah (9)
        </button>
        <button onclick="filterSyahadahTab('belum_proses')" id="subtab-sy-belum-proses" class="subtab-sy-btn px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 transition shrink-0">
          Sedang Berproses (15)
        </button>
      </div>

      <!-- Container Tabel & Mobile Cards Syahadah -->
      <div class="bg-white rounded-2xl sm:rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
        
        <div class="p-4 border-b border-slate-200 flex items-center justify-between">
          <h4 class="font-bold text-xs sm:text-sm text-slate-900" id="syahadah-table-title">Daftar Santri Pemegang Sertifikasi Syahadah</h4>
          <span class="text-xs text-slate-500 font-semibold" id="syahadah-table-count">22 Catatan</span>
        </div>

        <!-- Mobile Card View for Syahadah -->
        <div class="sm:hidden divide-y divide-slate-100" id="syahadah-mobile-cards">
          <!-- Rendered via JS -->
        </div>

        <!-- Desktop Table for Syahadah -->
        <div class="hidden sm:block overflow-x-auto">
          <table class="w-full text-left text-xs sm:text-sm border-collapse">
            <thead class="bg-slate-50 text-slate-500 text-[11px] uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th class="py-3 px-4 font-semibold">Santri</th>
                <th class="py-3 px-4 font-semibold">Kelas & Halaqah</th>
                <th class="py-3 px-4 font-semibold">Tingkat</th>
                <th class="py-3 px-4 font-semibold">Juz Diuji</th>
                <th class="py-3 px-4 font-semibold">Predikat & Kesalahan</th>
                <th class="py-3 px-4 font-semibold">Penguji & Tanggal</th>
                <th class="py-3 px-4 font-semibold">Catatan Evaluasi</th>
                <th class="py-3 px-4 font-semibold text-center">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100" id="syahadah-table-body">
              <!-- Rendered via JS -->
            </tbody>
          </table>
        </div>

      </div>

      <!-- Section: Santri Siap Syahadah 1 -->
      <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs space-y-3">
        <div class="flex items-center justify-between">
          <div>
            <h4 class="font-bold text-sm text-slate-900 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              Santri Siap Mengikuti Ujian Syahadah 1 (Sudah Hafal &ge; 5 Juz)
            </h4>
            <p class="text-xs text-slate-500">Santri yang telah menyetorkan minimal 5 Juz pertama (30, 29, 1, 2, 3) dan siap dijadwalkan ujian Syahadah.</p>
          </div>
          <span class="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800">
            9 Santri
          </span>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5 pt-2" id="list-syahadah-ready">
          <!-- Rendered via JS -->
        </div>
      </div>

    </div>

    <!-- ========================================================================================= -->
    <!-- TAB 3: KELANCARAN & ANALISIS MUTQIN -->
    <!-- ========================================================================================= -->
    <div id="content-kelancaran" class="tab-content hidden space-y-6">

      <!-- Header & Intro -->
      <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 border border-slate-200 shadow-xs space-y-2">
        <div class="flex items-center gap-2.5">
          <span class="p-2.5 bg-teal-100 text-teal-800 rounded-2xl">
            <i data-lucide="check-circle-2" class="w-6 h-6"></i>
          </span>
          <div>
            <h3 class="text-base sm:text-lg font-bold text-slate-900">Status Kelancaran & Pengujian Mutqin</h3>
            <p class="text-xs sm:text-sm text-slate-500">Mengetahui siapa santri yang paling lancar (teruji mutqin) dan siapa yang membutuhkan bimbingan intensif / remidi.</p>
          </div>
        </div>
      </div>

      <!-- Dual Section: Paling Lancar vs Perlu Murajaah -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        
        <!-- Kolom Kiri: Santri Paling Lancar -->
        <div class="bg-white rounded-2xl sm:rounded-3xl border border-slate-200 shadow-xs overflow-hidden flex flex-col justify-between">
          <div>
            <div class="p-4 bg-emerald-50/50 border-b border-emerald-100 flex items-center justify-between">
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-emerald-950 flex items-center gap-1.5">
                  <i data-lucide="shield-check" class="w-4 h-4 text-emerald-600"></i>
                  Santri Teruji Mutqin / Lancar
                </h4>
                <p class="text-[11px] text-emerald-800">Santri dengan akumulasi juz lancar terbanyak</p>
              </div>
              <span class="text-xs font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full">Top Performer</span>
            </div>

            <!-- Mobile list -->
            <div class="sm:hidden divide-y divide-slate-100" id="list-fluent-mobile"></div>

            <!-- Desktop table -->
            <div class="hidden sm:block overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead class="bg-slate-50 text-slate-500 text-[10px] uppercase border-b border-slate-200">
                  <tr>
                    <th class="py-2 px-3">Nama</th>
                    <th class="py-2 px-3">Kelas</th>
                    <th class="py-2 px-3">Juz Lancar</th>
                    <th class="py-2 px-3">Rincian Juz</th>
                    <th class="py-2 px-3 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100" id="table-fluent-students"></tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Kolom Kanan: Butuh Perhatian / Remidi -->
        <div class="bg-white rounded-2xl sm:rounded-3xl border border-slate-200 shadow-xs overflow-hidden flex flex-col justify-between">
          <div>
            <div class="p-4 bg-rose-50/50 border-b border-rose-100 flex items-center justify-between">
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-rose-950 flex items-center gap-1.5">
                  <i data-lucide="alert-circle" class="w-4 h-4 text-rose-600"></i>
                  Santri Membutuhkan Bimbingan & Remidi
                </h4>
                <p class="text-[11px] text-rose-800">Santri yang memiliki catatan tes belum lancar atau catatan rapuh di evaluasi Sabtu</p>
              </div>
              <span class="text-xs font-bold text-rose-800 bg-rose-100 px-2 py-0.5 rounded-full">Perlu Murajaah</span>
            </div>

            <!-- Mobile list -->
            <div class="sm:hidden divide-y divide-slate-100" id="list-need-attention-mobile"></div>

            <!-- Desktop table -->
            <div class="hidden sm:block overflow-x-auto">
              <table class="w-full text-left text-xs border-collapse">
                <thead class="bg-slate-50 text-slate-500 text-[10px] uppercase border-b border-slate-200">
                  <tr>
                    <th class="py-2 px-3">Nama</th>
                    <th class="py-2 px-3">Kelas</th>
                    <th class="py-2 px-3">Juz Remidi</th>
                    <th class="py-2 px-3">Catatan Sabtu</th>
                    <th class="py-2 px-3 text-center">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100" id="table-need-attention-students"></tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ========================================================================================= -->
    <!-- TAB 4: PENGELOMPOKAN KELAS & HALAQAH -->
    <!-- ========================================================================================= -->
    <div id="content-grouping" class="tab-content hidden space-y-6">

      <!-- Pengelompokan Berdasarkan Jenjang Kelas (Khusus 1, 2, 3) -->
      <div class="space-y-3">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-base sm:text-lg font-bold text-slate-900">Perbandingan Berdasarkan Jenjang Kelas</h3>
            <p class="text-xs text-slate-500">Santri dikelompokkan ke dalam 3 jenjang pendidikan aktif</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4" id="cards-classes-grid">
          <!-- Rendered via JS -->
        </div>
      </div>

      <!-- Pengelompokan Berdasarkan Halaqah Musyrif (6 Halaqah) -->
      <div class="space-y-3 pt-4 border-t border-slate-200">
        <div>
          <h3 class="text-base sm:text-lg font-bold text-slate-900">Performa 6 Kelompok Halaqah Musyrif</h3>
          <p class="text-xs text-slate-500">Distribusi bimbingan harian santri di bawah masing-masing musyrif/asatidzah</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4" id="cards-halaqah-grid">
          <!-- Rendered via JS -->
        </div>
      </div>

    </div>

    <!-- ========================================================================================= -->
    <!-- TAB 5: DIREKTORI & RAPOR SANTRI INTERAKTIF -->
    <!-- ========================================================================================= -->
    <div id="content-santri" class="tab-content hidden space-y-4">

      <!-- Filter & Search Toolbar -->
      <div class="bg-white rounded-2xl sm:rounded-3xl p-3.5 sm:p-5 border border-slate-200 shadow-xs space-y-3">
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
          
          <!-- Search input -->
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Cari Santri</label>
            <div class="relative">
              <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Ketik nama / NIS santri..." class="w-full text-xs px-3 py-2 pl-8 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition">
              <i data-lucide="search" class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5"></i>
            </div>
          </div>

          <!-- Filter Kelas -->
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Kelas</label>
            <select id="filterKelas" onchange="applyFilters()" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 transition">
              <option value="semua">Semua Kelas (Kelas 1, 2, 3)</option>
              <option value="kelas_1">Kelas 1 (Ula)</option>
              <option value="kelas_2">Kelas 2 (Wustho)</option>
              <option value="kelas_3">Kelas 3 (Ulya)</option>
            </select>
          </div>

          <!-- Filter Halaqah -->
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Halaqah Musyrif</label>
            <select id="filterHalaqah" onchange="applyFilters()" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 transition">
              <option value="semua">Semua Halaqah</option>
            </select>
          </div>

          <!-- Filter Syahadah -->
          <div>
            <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Status Syahadah</label>
            <select id="filterSyahadah" onchange="applyFilters()" class="w-full text-xs px-3 py-2 border border-slate-200 rounded-xl bg-slate-50 focus:bg-white focus:ring-2 focus:ring-emerald-500 transition">
              <option value="semua">Semua Status</option>
              <option value="syahadah">Sudah Lulus Syahadah</option>
              <option value="siap">Siap Ujian 1 (&ge; 5 Juz)</option>
              <option value="belum">Belum Syahadah</option>
            </select>
          </div>

        </div>

        <div class="flex items-center justify-between pt-2 border-t border-slate-100 text-xs">
          <div class="text-slate-500">
            Ditemukan <strong class="text-slate-900" id="filterResultCount">44</strong> santri
          </div>
          <button onclick="resetFilters()" class="text-emerald-700 hover:text-emerald-900 font-semibold text-xs flex items-center gap-1">
            <i data-lucide="rotate-ccw" class="w-3 h-3"></i>
            Reset Filter
          </button>
        </div>

      </div>

      <!-- Mobile Card View -->
      <div class="sm:hidden space-y-2.5" id="santriMobileCards"></div>

      <!-- Desktop Table View -->
      <div class="hidden sm:block bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs sm:text-sm border-collapse" id="santriTable">
            <thead class="bg-slate-50 text-slate-500 text-[11px] uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th class="py-3 px-4 font-semibold cursor-pointer hover:text-slate-800" onclick="sortSantriTable('nama')">
                  Santri & NIS ↕
                </th>
                <th class="py-3 px-4 font-semibold cursor-pointer hover:text-slate-800" onclick="sortSantriTable('kelas')">
                  Kelas & Gender ↕
                </th>
                <th class="py-3 px-4 font-semibold cursor-pointer hover:text-slate-800" onclick="sortSantriTable('halaqah')">
                  Musyrif Halaqah ↕
                </th>
                <th class="py-3 px-4 font-semibold cursor-pointer hover:text-slate-800" onclick="sortSantriTable('juz_dicapai')">
                  Total Dicapai ↕
                </th>
                <th class="py-3 px-4 font-semibold cursor-pointer hover:text-slate-800" onclick="sortSantriTable('juz_lancar')">
                  Lancar (Mutqin) ↕
                </th>
                <th class="py-3 px-4 font-semibold">Syahadah</th>
                <th class="py-3 px-4 font-semibold">Status Kelancaran</th>
                <th class="py-3 px-4 font-semibold text-center">Rapor</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100" id="santriTableBody"></tbody>
          </table>
        </div>
      </div>

    </div>

    <!-- ========================================================================================= -->
    <!-- TAB 6: PANDUAN AWAM & GLOSARIUM TAHFIDZ -->
    <!-- ========================================================================================= -->
    <div id="content-panduan" class="tab-content hidden space-y-6">

      <!-- Panduan Alur Belajar -->
      <div class="bg-white rounded-2xl sm:rounded-3xl p-5 sm:p-7 border border-slate-200 shadow-xs space-y-4">
        <h3 class="text-base sm:text-lg font-bold text-slate-900 flex items-center gap-2">
          <i data-lucide="git-branch" class="w-5 h-5 text-emerald-600"></i>
          Alur & Metodologi Tahfidz Santri Pesantren
        </h3>
        <p class="text-xs sm:text-sm text-slate-600 leading-relaxed">
          Berikut adalah urutan tahapan yang dilalui santri mulai dari awal menyetorkan hafalan hingga menyandang predikat Mutqin:
        </p>

        <div class="grid grid-cols-1 md:grid-cols-5 gap-3 pt-2">
          
          <div class="p-3.5 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-1.5">
            <div class="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center">1</div>
            <h4 class="font-bold text-xs text-slate-900">Ziyadah Harian</h4>
            <p class="text-[11px] text-slate-600">Menyetor hafalan ayat/halaman baru setiap hari kepada musyrif halaqah.</p>
          </div>

          <div class="p-3.5 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-1.5">
            <div class="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center">2</div>
            <h4 class="font-bold text-xs text-slate-900">Setengah Juz</h4>
            <p class="text-[11px] text-slate-600">Setelah menyelesaikan 10 halaman (setengah juz), santri menyetor sekali duduk.</p>
          </div>

          <div class="p-3.5 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-1.5">
            <div class="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center">3</div>
            <h4 class="font-bold text-xs text-slate-900">Ujian Juziyah</h4>
            <p class="text-[11px] text-slate-600">Ujian 1 juz penuh sekali duduk dengan maksimal 15 kesalahan untuk dinyatakan lulus.</p>
          </div>

          <div class="p-3.5 rounded-2xl bg-emerald-50/60 border border-emerald-200 space-y-1.5">
            <div class="w-7 h-7 rounded-full bg-emerald-600 text-white font-bold text-xs flex items-center justify-center">4</div>
            <h4 class="font-bold text-xs text-slate-900">Tes Kelancaran</h4>
            <p class="text-[11px] text-slate-600">Ujian acak sambung ayat untuk menguji kemutqinan hafalan jangka panjang.</p>
          </div>

          <div class="p-3.5 rounded-2xl bg-amber-50 border border-amber-300 space-y-1.5">
            <div class="w-7 h-7 rounded-full bg-amber-600 text-white font-bold text-xs flex items-center justify-center">5</div>
            <h4 class="font-bold text-xs text-amber-950">Ujian Syahadah</h4>
            <p class="text-[11px] text-amber-900">Ujian akbar 5 juz sekali duduk di hadapan dewan penguji resmi tahfidz.</p>
          </div>

        </div>
      </div>

      <!-- Urutan Hafalan Khusus & Glosarium -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        
        <div class="bg-white rounded-2xl sm:rounded-3xl p-5 border border-slate-200 shadow-xs space-y-3">
          <h4 class="font-bold text-sm sm:text-base text-slate-900 flex items-center gap-2">
            <i data-lucide="book" class="w-4 h-4 text-emerald-600"></i>
            Mengapa Urutan Hafalan dari Juz 30 & 29?
          </h4>
          <p class="text-xs text-slate-600 leading-relaxed">
            Pesantren menerapkan tradisi menghafal dimulai dari <strong>Juz 30 (Juz 'Amma)</strong> lalu <strong>Juz 29</strong> sebelum masuk ke Juz 1 (Al-Baqarah). Hal ini karena surat-surat pendek di Juz 30 dan 29 paling sering dibaca saat salat lima waktu sehingga lebih cepat melekat, melatih kelenturan makhraj santri, dan menumbuhkan rasa percaya diri di tahun pertama (Kelas 1).
          </p>
        </div>

        <div class="bg-white rounded-2xl sm:rounded-3xl p-5 border border-slate-200 shadow-xs space-y-3">
          <h4 class="font-bold text-sm sm:text-base text-slate-900 flex items-center gap-2">
            <i data-lucide="help-circle" class="w-4 h-4 text-teal-600"></i>
            Arti Istilah Penting dalam Laporan
          </h4>
          <div class="space-y-2 text-xs text-slate-600">
            <div><strong class="text-slate-800">Ziyadah:</strong> Penambahan hafalan ayat baru.</div>
            <div><strong class="text-slate-800">Murajaah:</strong> Mengulang kembali hafalan yang sudah pernah disetor.</div>
            <div><strong class="text-slate-800">Mutqin:</strong> Hafalan yang sangat kuat, lancar tanpa tersendat, dan tajwidnya benar.</div>
            <div><strong class="text-slate-800">Syahadah:</strong> Sertifikasi hafalan 5 juz sekali duduk yang diuji langsung oleh penguji senior.</div>
          </div>
        </div>

      </div>

      <!-- Kriteria Nilai Resmi -->
      <div class="bg-white rounded-2xl sm:rounded-3xl p-5 border border-slate-200 shadow-xs space-y-3">
        <h4 class="font-bold text-sm sm:text-base text-slate-900">Standar Predikat Nilai Pesantren</h4>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-slate-50 text-slate-500 font-semibold border-b border-slate-200">
              <tr>
                <th class="py-2.5 px-3">Predikat</th>
                <th class="py-2.5 px-3">Arti / Keterangan</th>
                <th class="py-2.5 px-3">Batas Salah Syahadah (5 Juz)</th>
                <th class="py-2.5 px-3">Batas Salah Juziyah (1 Juz)</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr>
                <td class="py-2 px-3 font-bold text-emerald-700">Mumtaz</td>
                <td class="py-2 px-3">Istimewa / Sempurna</td>
                <td class="py-2 px-3">0 – 10 Kesalahan</td>
                <td class="py-2 px-3">0 – 5 Kesalahan</td>
              </tr>
              <tr>
                <td class="py-2 px-3 font-bold text-emerald-600">Jayyid Jiddan</td>
                <td class="py-2 px-3">Sangat Baik</td>
                <td class="py-2 px-3">11 – 20 Kesalahan</td>
                <td class="py-2 px-3">6 – 10 Kesalahan</td>
              </tr>
              <tr>
                <td class="py-2 px-3 font-bold text-amber-600">Jayyid</td>
                <td class="py-2 px-3">Baik</td>
                <td class="py-2 px-3">21 – 30 Kesalahan</td>
                <td class="py-2 px-3">11 – 15 Kesalahan</td>
              </tr>
              <tr>
                <td class="py-2 px-3 font-bold text-slate-600">Maqbul</td>
                <td class="py-2 px-3">Cukup</td>
                <td class="py-2 px-3">31 – 40 Kesalahan</td>
                <td class="py-2 px-3">16 – 20 Kesalahan</td>
              </tr>
              <tr>
                <td class="py-2 px-3 font-bold text-rose-600">Mardud</td>
                <td class="py-2 px-3">Mengulang / Belum Lulus</td>
                <td class="py-2 px-3">&gt; 40 Kesalahan</td>
                <td class="py-2 px-3">&gt; 20 Kesalahan</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>

  </main>

  <!-- ========================================================================================= -->
  <!-- MODAL: RAPOR & DETAIL SANTRI (30 JUZ TOUCH-FRIENDLY) -->
  <!-- ========================================================================================= -->
  <div id="santriModal" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs hidden flex items-end sm:items-center justify-center p-0 sm:p-4 no-print">
    <div class="bg-white w-full sm:max-w-3xl sm:rounded-3xl max-h-[92vh] flex flex-col shadow-2xl border-t sm:border border-slate-200 overflow-hidden transform transition-all duration-200" id="santriModalCard">
      
      <!-- Modal Header -->
      <div class="p-4 sm:p-5 bg-gradient-to-r from-emerald-800 to-teal-900 text-white flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-white/10 flex items-center justify-center text-white text-lg sm:text-xl font-bold font-arabic shrink-0" id="modal-avatar">
            س
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <h3 class="text-base sm:text-lg font-bold text-white truncate" id="modal-nama">Nama Santri</h3>
              <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-white/20 text-white shrink-0" id="modal-status">Aktif</span>
            </div>
            <p class="text-xs text-emerald-200 truncate mt-0.5">
              <span id="modal-nis">NIS: -</span> • <span id="modal-kelas">Kelas</span> • <span id="modal-halaqah">Musyrif</span>
            </p>
          </div>
        </div>
        <button onclick="closeSantriModal()" class="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition shrink-0">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>

      <!-- Modal Body (Scrollable) -->
      <div class="p-4 sm:p-6 overflow-y-auto space-y-5">
        
        <!-- 4 Quick Stats -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          <div class="bg-emerald-50/70 p-3 rounded-2xl border border-emerald-100">
            <div class="text-[10px] uppercase font-bold text-emerald-700">Total Hafal</div>
            <div class="text-lg font-black text-emerald-900 mt-0.5" id="modal-juz-dicapai">0 Juz</div>
            <div class="text-[10px] text-slate-500">Capaian Ziyadah</div>
          </div>

          <div class="bg-teal-50/70 p-3 rounded-2xl border border-teal-100">
            <div class="text-[10px] uppercase font-bold text-teal-700">Teruji Mutqin</div>
            <div class="text-lg font-black text-teal-900 mt-0.5" id="modal-juz-lancar">0 Juz</div>
            <div class="text-[10px] text-slate-500">Lolos Tes Kelancaran</div>
          </div>

          <div class="bg-amber-50/70 p-3 rounded-2xl border border-amber-100">
            <div class="text-[10px] uppercase font-bold text-amber-700">Syahadah</div>
            <div class="text-lg font-black text-amber-900 mt-0.5" id="modal-syahadah-highest">-</div>
            <div class="text-[10px] text-slate-500" id="modal-syahadah-count">0 Sertifikat</div>
          </div>

          <div class="bg-slate-50 p-3 rounded-2xl border border-slate-200">
            <div class="text-[10px] uppercase font-bold text-slate-500">Kelancaran</div>
            <div class="text-xs font-bold text-slate-800 mt-1 truncate" id="modal-fluency-badge">-</div>
            <div class="text-[10px] text-rose-600 font-medium" id="modal-tidak-lancar-count">0 Remidi</div>
          </div>
        </div>

        <!-- Target Berikutnya Progress -->
        <div class="bg-white p-3.5 rounded-2xl border border-slate-200 space-y-2">
          <div class="flex items-center justify-between text-xs">
            <span class="font-bold text-slate-800" id="modal-target-title">Target Syahadah 1 (5 Juz)</span>
            <span class="font-semibold text-emerald-700" id="modal-target-pct">0%</span>
          </div>
          <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
            <div class="bg-emerald-600 h-2 rounded-full transition-all duration-500" id="modal-target-bar" style="width: 0%"></div>
          </div>
          <p class="text-[11px] text-slate-500" id="modal-target-desc">Kurang 5 Juz untuk menuju ujian Syahadah 1.</p>
        </div>

        <!-- Visual 30-Juz Map Grid (Touch-friendly Tiles) -->
        <div class="space-y-2.5">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-1.5">
              <i data-lucide="layout-grid" class="w-4 h-4 text-emerald-600"></i>
              Peta Capaian 30 Juz Al-Qur'an
            </h4>
            <span class="text-[10px] text-slate-400">Klik kotak untuk detail surat</span>
          </div>

          <!-- Color Legend -->
          <div class="flex flex-wrap items-center gap-3 text-[10px] text-slate-600 pb-1">
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-emerald-500"></span> Mutqin / Lancar</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-amber-400"></span> Sudah Setor (Belum Tes)</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-rose-500"></span> Belum Lancar / Remidi</span>
            <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded bg-slate-100 border border-slate-200"></span> Belum Mulai</span>
          </div>

          <!-- 30-Juz Buttons Grid -->
          <div class="grid grid-cols-6 sm:grid-cols-10 gap-1.5" id="modal-juz-grid">
            <!-- Rendered via JS -->
          </div>

          <!-- Selected Juz Details -->
          <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between" id="selected-juz-box">
            <div class="flex items-center gap-2.5">
              <div class="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-800 font-bold text-xs flex items-center justify-center shrink-0" id="selected-juz-badge">
                30
              </div>
              <div>
                <div class="font-bold text-xs text-slate-900" id="selected-juz-title">Juz 30</div>
                <div class="text-[10px] text-slate-500" id="selected-juz-surah">An-Naba' 1 - An-Nas 6</div>
              </div>
            </div>
            <div class="text-[11px] font-bold text-emerald-700 shrink-0" id="selected-juz-status">
              Lancar / Mutqin
            </div>
          </div>
        </div>

        <!-- Syahadah History List -->
        <div class="space-y-2" id="modal-syahadah-section">
          <h4 class="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-1.5">
            <i data-lucide="award" class="w-4 h-4 text-amber-500"></i>
            Riwayat Ujian Syahadah Resmi
          </h4>
          <div class="space-y-2" id="modal-syahadah-list"></div>
        </div>

        <!-- Evaluasi Catatan Rapuh / Laporan Sabtu -->
        <div class="space-y-2" id="modal-evaluasi-section">
          <h4 class="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-1.5">
            <i data-lucide="clipboard-list" class="w-4 h-4 text-rose-500"></i>
            Catatan Perlu Perhatian / Murajaah Sabtu
          </h4>
          <div class="space-y-1.5" id="modal-evaluasi-list"></div>
        </div>

        <!-- Rekomendasi Musyrif -->
        <div class="p-3.5 rounded-2xl bg-emerald-50/70 border border-emerald-200 text-xs space-y-1">
          <div class="font-bold text-emerald-950 flex items-center gap-1.5">
            <i data-lucide="message-square" class="w-4 h-4 text-emerald-700"></i>
            Rekomendasi Musyrif untuk Wali Santri
          </div>
          <p class="text-slate-700 leading-relaxed text-[11px]" id="modal-rekomendasi">
            Santri memiliki komitmen yang baik dalam setoran harian.
          </p>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="p-3 sm:p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between shrink-0">
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
        <span class="font-semibold text-slate-700">Laporan Capaian Tahfidz Santri Kelas 1, 2, & 3</span>
      </div>
      <div class="text-[11px] text-slate-400" id="footerMetadata">
        Snapshot: <code class="font-mono text-emerald-700">everynight-in-my-dream.db</code> • 44 Santri
      </div>
    </div>
  </footer>

  <!-- EMBEDDED DATASET SCRIPT -->
  <script id="embedded-data" type="application/json">
DATA_JSON_PLACEHOLDER
  </script>

  <!-- JAVASCRIPT APPLICATION CODE -->
  <script>
    const INDO_DAYS = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'];
    const INDO_MONTHS = [
      'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
      'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ];

    function formatIndoDate(dateStr) {
      if (!dateStr || dateStr === '-' || dateStr === 'Belum Ada' || dateStr === 'null' || dateStr === 'undefined') return '-';
      if (typeof dateStr === 'string' && (dateStr.includes('Januari') || dateStr.includes('Februari') || dateStr.includes('Maret') || dateStr.includes('April') || dateStr.includes('Mei') || dateStr.includes('Juni') || dateStr.includes('Juli') || dateStr.includes('Agustus') || dateStr.includes('September') || dateStr.includes('Oktober') || dateStr.includes('November') || dateStr.includes('Desember'))) {
        return dateStr;
      }
      const cleanStr = String(dateStr).trim().split(' ')[0];
      const parts = cleanStr.split('-');
      if (parts.length === 3) {
        const y = parseInt(parts[0], 10);
        const m = parseInt(parts[1], 10) - 1;
        const d = parseInt(parts[2], 10);
        const dateObj = new Date(y, m, d);
        if (!isNaN(dateObj.getTime())) {
          const dayName = INDO_DAYS[dateObj.getDay()];
          const monthName = INDO_MONTHS[m];
          return `${dayName}, ${d} ${monthName} ${y}`;
        }
      }
      return dateStr;
    }

    const rawDataElem = document.getElementById('embedded-data');
    let DB = JSON.parse(rawDataElem.textContent);
    let ALL_SANTRI = DB.santri_list;
    let filteredSantri = [...ALL_SANTRI];
    let currentSort = { column: 'nama', asc: true };
    let currentModalSantri = null;

    let currentDateRange = {
      start: DB.metadata.min_date || '2026-01-16',
      end: DB.metadata.max_date || '2026-11-18',
      isCustom: false
    };
    let currentPeriodData = null;

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

    // Dynamic Period Computation
    function computePeriodData(startDate, endDate) {
      const isAllTime = (startDate <= DB.metadata.min_date && endDate >= DB.metadata.max_date);
      
      let totalPencapaian = 0;
      let totalTes = 0;
      let totalSabtu = 0;
      let totalSyahadahCerts = 0;
      let syahadahTierCounts = { 'pertama': 0, 'kedua': 0, 'ketiga': 0, 'keempat': 0 };
      let syahadahRecords = [];
      let santriActiveCount = 0;
      let totalJuzSetor = 0;
      let totalJuzLancar = 0;

      let juzStats = {};
      for (let j = 1; j <= 30; j++) {
        juzStats[j] = { juz: j, hafal_in_period: 0, tes_lancar_in_period: 0, tes_tl_in_period: 0, issues_in_period: 0 };
      }

      const periodSantriList = ALL_SANTRI.map(s => {
        const pInPeriod = (s.raw_achievements || []).filter(a => a.created_at >= startDate && a.created_at <= endDate);
        const tInPeriod = (s.raw_tests || []).filter(t => t.created_at >= startDate && t.created_at <= endDate);
        const sbInPeriod = (s.raw_sabtu || []).filter(sb => sb.created_at >= startDate && sb.created_at <= endDate);
        const syInPeriod = (s.syahadahs || []).filter(sy => sy.created_at >= startDate && sy.created_at <= endDate);
        const jzInPeriod = (s.juziyahs || []).filter(j => j.created_at >= startDate && j.created_at <= endDate);

        totalPencapaian += pInPeriod.length;
        totalTes += tInPeriod.length;
        totalSabtu += sbInPeriod.length;
        totalSyahadahCerts += syInPeriod.length;

        syInPeriod.forEach(sy => {
          syahadahTierCounts[sy.tingkat] = (syahadahTierCounts[sy.tingkat] || 0) + 1;
          syahadahRecords.push({
            santri: s,
            syahadah: sy
          });
        });

        const hasActivity = (pInPeriod.length > 0 || tInPeriod.length > 0 || sbInPeriod.length > 0);
        if (hasActivity) santriActiveCount++;

        const juzSetorInPeriod = Array.from(new Set(pInPeriod.filter(a => a.juz).map(a => a.juz)));
        const testLancarInPeriod = tInPeriod.filter(t => t.status === 'lancar');
        const testTlInPeriod = tInPeriod.filter(t => t.status === 'tidak_lancar');
        const juzLancarInPeriod = Array.from(new Set(testLancarInPeriod.map(t => t.juz)));
        const juzTlInPeriod = Array.from(new Set(testTlInPeriod.map(t => t.juz)));

        totalJuzSetor += juzSetorInPeriod.length;
        totalJuzLancar += juzLancarInPeriod.length;

        juzSetorInPeriod.forEach(j => { if (juzStats[j]) juzStats[j].hafal_in_period++; });
        juzLancarInPeriod.forEach(j => { if (juzStats[j]) juzStats[j].tes_lancar_in_period++; });
        juzTlInPeriod.forEach(j => { if (juzStats[j]) juzStats[j].tes_tl_in_period++; });

        let lastDateInPeriod = null;
        let lastDateIndo = '-';
        let allDates = [
          ...pInPeriod.map(x => x.created_at),
          ...tInPeriod.map(x => x.created_at),
          ...sbInPeriod.map(x => x.created_at)
        ].sort();
        if (allDates.length > 0) {
          lastDateInPeriod = allDates[allDates.length - 1];
          lastDateIndo = formatIndoDate(lastDateInPeriod);
        }

        return {
          ...s,
          pInPeriod,
          tInPeriod,
          sbInPeriod,
          period_has_activity: hasActivity,
          period_pencapaian_count: pInPeriod.length,
          period_tests_count: tInPeriod.length,
          period_sabtu_count: sbInPeriod.length,
          period_syahadahs: syInPeriod,
          period_juziyahs: jzInPeriod,
          period_juz_setor: juzSetorInPeriod,
          period_juz_setor_count: juzSetorInPeriod.length,
          period_juz_lancar: juzLancarInPeriod,
          period_juz_lancar_count: juzLancarInPeriod.length,
          period_juz_tidak_lancar: juzTlInPeriod,
          period_juz_tidak_lancar_count: juzTlInPeriod.length,
          period_last_date: lastDateInPeriod,
          period_last_date_indo: lastDateIndo
        };
      });

      return {
        startDate,
        endDate,
        startDateIndo: formatIndoDate(startDate),
        endDateIndo: formatIndoDate(endDate),
        isAllTime,
        periodSantriList,
        totalPencapaian,
        totalTes,
        totalSabtu,
        totalSyahadahCerts,
        syahadahTierCounts,
        syahadahRecords,
        santriActiveCount,
        totalJuzSetor,
        totalJuzLancar,
        juzStats
      };
    }

    function setPresetRange(key) {
      let start, end;
      if (key === 'all') {
        start = DB.metadata.min_date;
        end = DB.metadata.max_date;
      } else if (key === 'user_example') {
        start = '2026-07-01';
        end = '2026-10-03';
      } else if (key === 'sem1_2026') {
        start = '2026-07-01';
        end = DB.metadata.max_date;
      } else if (key === 'sem2_2026') {
        start = '2026-01-01';
        end = '2026-06-30';
      } else if (key === 'last_30d') {
        start = '2026-10-19';
        end = DB.metadata.max_date;
      }

      document.getElementById('filterStartDate').value = start;
      document.getElementById('filterEndDate').value = end;

      document.querySelectorAll('.preset-btn').forEach(b => {
        b.classList.remove('bg-emerald-600', 'text-white', 'shadow-2xs');
        b.classList.add('bg-slate-100', 'text-slate-700');
      });
      const activeBtn = document.getElementById('preset-btn-' + key);
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
        activeBtn.classList.add('bg-emerald-600', 'text-white', 'shadow-2xs');
      }

      applyDateRangeFilter();
    }

    function onDateInputChange() {
      document.querySelectorAll('.preset-btn').forEach(b => {
        b.classList.remove('bg-emerald-600', 'text-white', 'shadow-2xs');
        b.classList.add('bg-slate-100', 'text-slate-700');
      });
    }

    function applyDateRangeFilter() {
      let start = document.getElementById('filterStartDate').value;
      let end = document.getElementById('filterEndDate').value;

      if (!start) start = DB.metadata.min_date;
      if (!end) end = DB.metadata.max_date;
      if (start > end) {
        const tmp = start; start = end; end = tmp;
        document.getElementById('filterStartDate').value = start;
        document.getElementById('filterEndDate').value = end;
      }

      currentDateRange = { start, end, isCustom: !(start <= DB.metadata.min_date && end >= DB.metadata.max_date) };
      currentPeriodData = computePeriodData(start, end);

      const startIndo = formatIndoDate(start);
      const endIndo = formatIndoDate(end);

      const badgeText = document.getElementById('badgeActivePeriodText');
      const spanText = document.getElementById('activePeriodSpanText');
      const statsText = document.getElementById('activePeriodStatsText');
      const btnResetInline = document.getElementById('btnResetInline');

      if (currentDateRange.isCustom) {
        badgeText.textContent = `${startIndo} s/d ${endIndo}`;
        spanText.textContent = `${startIndo} s/d ${endIndo}`;
        statsText.textContent = `(${currentPeriodData.totalPencapaian} setoran, ${currentPeriodData.totalSyahadahCerts} kelulusan syahadah, ${currentPeriodData.totalJuzLancar} tes lancar)`;
        btnResetInline.classList.remove('hidden');
      } else {
        badgeText.textContent = 'Semua Waktu';
        spanText.textContent = `${startIndo} s/d ${endIndo}`;
        statsText.textContent = `(Menampilkan seluruh 44 santri & seluruh riwayat)`;
        btnResetInline.classList.add('hidden');
      }

      updateExecutiveHighlights(currentPeriodData);
      renderAllCharts(currentPeriodData);
      renderSyahadahTable();
      populateKelancaranTables();
      populateGroupingCards();
      applyFilters();
      lucide.createIcons();
    }

    function resetDateRangeFilter() {
      setPresetRange('all');
    }

    function updateExecutiveHighlights(data) {
      if (!data) return;

      if (data.isAllTime) {
        document.getElementById('kpi-total-santri').textContent = DB.summary.total_santri;
        document.getElementById('kpi-sub-santri').innerHTML = `<span class="text-emerald-700 font-semibold">${DB.summary.santri_aktif} Aktif</span> • ${DB.summary.santri_tidak_aktif} Non-aktif`;
        
        document.getElementById('kpi-total-syahadah').textContent = DB.summary.santri_dengan_syahadah;
        document.getElementById('kpi-sub-syahadah').textContent = `${DB.summary.total_sertifikat_syahadah} Sertifikat Kelulusan`;

        document.getElementById('kpi-total-juz').innerHTML = `${DB.summary.total_juz_dihafal} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-juz').textContent = `Rata-rata ${(DB.summary.total_juz_dihafal / DB.summary.total_santri).toFixed(1)} Juz/Santri`;

        document.getElementById('kpi-total-lancar').innerHTML = `${DB.summary.total_juz_lancar} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-lancar').textContent = 'Lolos Ujian Kelancaran';

        document.getElementById('kpi-total-pencapaian').textContent = (DB.summary.total_pencapaian_records + DB.summary.total_tes_records).toLocaleString('id-ID');
        document.getElementById('kpi-sub-pencapaian').textContent = `${DB.summary.total_pencapaian_records} Setor • ${DB.summary.total_tes_records} Tes`;

        document.getElementById('kpi-total-sabtu').textContent = DB.summary.total_laporansabtu_records;
        document.getElementById('kpi-sub-sabtu').textContent = 'Laporan Evaluasi Sabtu';
      } else {
        document.getElementById('kpi-total-santri').textContent = data.santriActiveCount;
        document.getElementById('kpi-sub-santri').innerHTML = `<span class="text-emerald-700 font-semibold">${data.santriActiveCount} Menyetor di Periode Ini</span>`;

        document.getElementById('kpi-total-syahadah').textContent = data.totalSyahadahCerts;
        document.getElementById('kpi-sub-syahadah').textContent = `${data.syahadahRecords.length} Ujian di Periode Ini`;

        document.getElementById('kpi-total-juz').innerHTML = `${data.totalJuzSetor} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-juz').textContent = `Disetor di Periode Ini`;

        document.getElementById('kpi-total-lancar').innerHTML = `${data.totalJuzLancar} <span class="text-xs font-normal text-slate-500">Juz</span>`;
        document.getElementById('kpi-sub-lancar').textContent = `Lolos Tes di Periode Ini`;

        document.getElementById('kpi-total-pencapaian').textContent = (data.totalPencapaian + data.totalTes).toLocaleString('id-ID');
        document.getElementById('kpi-sub-pencapaian').textContent = `${data.totalPencapaian} Setor • ${data.totalTes} Tes`;

        document.getElementById('kpi-total-sabtu').textContent = data.totalSabtu;
        document.getElementById('kpi-sub-sabtu').textContent = 'Laporan di Periode Ini';
      }

      // Top Achievers in Period
      const listSantri = data.periodSantriList || ALL_SANTRI;
      const topAchievers = [...listSantri].sort((a,b) => {
        if (!data.isAllTime) {
          return (b.period_juz_setor_count - a.period_juz_setor_count) || (b.total_juz_dicapai - a.total_juz_dicapai);
        }
        return b.total_juz_dicapai - a.total_juz_dicapai;
      }).slice(0, 5);

      document.getElementById('list-top-achievers').innerHTML = topAchievers.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 cursor-pointer transition border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-5 h-5 rounded-full bg-amber-100 text-amber-800 flex items-center justify-center text-[10px] font-bold shrink-0">${idx + 1}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
              <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-emerald-700 text-xs">${data.isAllTime ? s.total_juz_dicapai : s.period_juz_setor_count} Juz</div>
            <div class="text-[9px] text-slate-400">${data.isAllTime ? `${s.total_juz_lancar} lancar` : `${s.total_juz_dicapai} total`}</div>
          </div>
        </div>
      `).join('');

      // Top Fluent in Period
      const topFluent = [...listSantri].sort((a,b) => {
        if (!data.isAllTime) {
          return (b.period_juz_lancar_count - a.period_juz_lancar_count) || (b.total_juz_lancar - a.total_juz_lancar);
        }
        return b.total_juz_lancar - a.total_juz_lancar;
      }).slice(0, 5);

      document.getElementById('list-top-fluent').innerHTML = topFluent.map((s, idx) => `
        <div onclick="openSantriModal(${s.id})" class="flex items-center justify-between p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 cursor-pointer transition border border-slate-100">
          <div class="flex items-center gap-2.5 truncate">
            <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 flex items-center justify-center text-[10px] font-bold shrink-0">${idx + 1}</span>
            <div class="truncate">
              <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
              <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${s.musyrif_nama}</div>
            </div>
          </div>
          <div class="text-right shrink-0 ml-2">
            <div class="font-bold text-teal-700 text-xs">${data.isAllTime ? s.total_juz_lancar : s.period_juz_lancar_count} Juz</div>
            <div class="text-[9px] text-slate-400">${data.isAllTime ? `${s.total_juz_dicapai} dicapai` : `${s.total_juz_lancar} total`}</div>
          </div>
        </div>
      `).join('');

      // Top Challenging Juz
      const juzEntries = Object.values(data.juzStats || {}).map(j => ({
        ...j,
        surah: (DB.juz_stats.find(js => js.juz === j.juz) || {}).surah || `Juz ${j.juz}`,
        hafal_count: (DB.juz_stats.find(js => js.juz === j.juz) || {}).hafal_count || 0,
        total_issues: (j.tes_tl_in_period || 0) + (j.issues_in_period || 0)
      })).sort((a,b) => b.total_issues - a.total_issues).slice(0, 5);

      document.getElementById('list-challenging-juz').innerHTML = juzEntries.map(j => `
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
            <div class="text-[9px] text-slate-400">${j.tes_tl_in_period}x remidi</div>
          </div>
        </div>
      `).join('');
    }

    // Chart instances
    let chartInstanceClass = null;
    let chartInstanceSyahadah = null;
    let chartInstanceJuz = null;

    function renderAllCharts(data) {
      if (!data) data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const textColor = '#334155';
      const gridColor = '#f1f5f9';

      // 1. Chart Class Comparison
      const ctxClass = document.getElementById('chartClassComparison')?.getContext('2d');
      if (ctxClass) {
        if (chartInstanceClass) chartInstanceClass.destroy();
        
        const classNames = ['Kelas 1 (Ula)', 'Kelas 2 (Wustho)', 'Kelas 3 (Ulya)'];
        const classKeys = ['kelas_1', 'kelas_2', 'kelas_3'];
        
        let avgAchieved = [];
        let avgLancar = [];

        classKeys.forEach(k => {
          const listInClass = (data.periodSantriList || ALL_SANTRI).filter(s => s.kelas_id === k);
          const totalInClass = listInClass.length || 1;
          if (data.isAllTime) {
            const sumAch = listInClass.reduce((acc, s) => acc + s.total_juz_dicapai, 0);
            const sumLan = listInClass.reduce((acc, s) => acc + s.total_juz_lancar, 0);
            avgAchieved.push(+(sumAch / totalInClass).toFixed(1));
            avgLancar.push(+(sumLan / totalInClass).toFixed(1));
          } else {
            const sumAch = listInClass.reduce((acc, s) => acc + s.period_juz_setor_count, 0);
            const sumLan = listInClass.reduce((acc, s) => acc + s.period_juz_lancar_count, 0);
            avgAchieved.push(+(sumAch / totalInClass).toFixed(1));
            avgLancar.push(+(sumLan / totalInClass).toFixed(1));
          }
        });

        chartInstanceClass = new Chart(ctxClass, {
          type: 'bar',
          data: {
            labels: classNames,
            datasets: [
              {
                label: data.isAllTime ? 'Rata-rata Juz Dicapai' : 'Rata-rata Disetor Periode Ini',
                data: avgAchieved,
                backgroundColor: '#10b981',
                borderRadius: 4
              },
              {
                label: data.isAllTime ? 'Rata-rata Juz Lancar' : 'Rata-rata Lulus Tes Periode Ini',
                data: avgLancar,
                backgroundColor: '#0d9488',
                borderRadius: 4
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
              x: { ticks: { color: textColor, font: { size: 10 } }, grid: { display: false } },
              y: { ticks: { color: textColor, font: { size: 9 } }, grid: { color: gridColor }, beginAtZero: true }
            }
          }
        });
      }

      // 2. Chart Syahadah Status
      const ctxSyahadah = document.getElementById('chartSyahadahStatus')?.getContext('2d');
      if (ctxSyahadah) {
        if (chartInstanceSyahadah) chartInstanceSyahadah.destroy();
        
        let labels, values, bgColors;
        if (data.isAllTime) {
          labels = [
            'Lulus (' + DB.summary.santri_dengan_syahadah + ')',
            'Siap Ujian (' + DB.summary.ready_for_syahadah_count + ')',
            'Berproses (' + DB.summary.in_progress_non_syahadah_count + ')',
            'Awal / Non-aktif (' + DB.summary.unstarted_non_syahadah_count + ')'
          ];
          values = [
            DB.summary.santri_dengan_syahadah,
            DB.summary.ready_for_syahadah_count,
            DB.summary.in_progress_non_syahadah_count,
            DB.summary.unstarted_non_syahadah_count
          ];
          bgColors = ['#f59e0b', '#10b981', '#3b82f6', '#94a3b8'];
        } else {
          labels = [
            'Syahadah 1 (' + (data.syahadahTierCounts['pertama'] || 0) + ')',
            'Syahadah 2 (' + (data.syahadahTierCounts['kedua'] || 0) + ')',
            'Syahadah 3 (' + (data.syahadahTierCounts['ketiga'] || 0) + ')',
            'Syahadah 4 (' + (data.syahadahTierCounts['keempat'] || 0) + ')'
          ];
          values = [
            data.syahadahTierCounts['pertama'] || 0,
            data.syahadahTierCounts['kedua'] || 0,
            data.syahadahTierCounts['ketiga'] || 0,
            data.syahadahTierCounts['keempat'] || 0
          ];
          bgColors = ['#f59e0b', '#10b981', '#3b82f6', '#8b5cf6'];
        }

        chartInstanceSyahadah = new Chart(ctxSyahadah, {
          type: 'doughnut',
          data: {
            labels: labels,
            datasets: [{
              data: values,
              backgroundColor: bgColors,
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

      // 3. Chart Juz Issues
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

    let currentSyahadahFilter = 'semua';
    function filterSyahadahTab(filterKey) {
      currentSyahadahFilter = filterKey;
      document.querySelectorAll('.subtab-sy-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-emerald-600', 'text-white');
        btn.classList.add('bg-slate-100', 'text-slate-700');
      });
      const activeBtn = document.getElementById('subtab-sy-' + filterKey.replace('_', '-'));
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
        activeBtn.classList.add('active', 'bg-emerald-600', 'text-white');
      }
      renderSyahadahTable();
    }

    function renderSyahadahTable() {
      const tbody = document.getElementById('syahadah-table-body');
      const mobileCards = document.getElementById('syahadah-mobile-cards');
      const titleElem = document.getElementById('syahadah-table-title');
      const countElem = document.getElementById('syahadah-table-count');

      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      let records = [];

      if (currentSyahadahFilter === 'belum_siap') {
        titleElem.textContent = 'Santri Kelas 1-3 Belum Syahadah Namun Sudah Hafal >= 5 Juz (Siap Ujian)';
        const readySantri = listSantri.filter(s => !s.has_syahadah && s.total_juz_dicapai >= 5);
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
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs">Sudah menuntaskan batas 5 juz. Direkomendasikan segera diuji Syahadah 1.</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-100 hover:bg-slate-200">Rapor</button></td>
          </tr>
        `).join('');
        return;
      }

      if (currentSyahadahFilter === 'belum_proses') {
        titleElem.textContent = 'Santri Kelas 1-3 yang Sedang Berproses Menuju Syahadah 1 (1 - 4 Juz)';
        const inProgress = listSantri.filter(s => !s.has_syahadah && s.total_juz_dicapai > 0 && s.total_juz_dicapai < 5);
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

      listSantri.forEach(s => {
        const syList = data.isAllTime ? s.syahadahs : (s.period_syahadahs || []);
        syList.forEach(sy => {
          if (currentSyahadahFilter === 'semua' || sy.tingkat === currentSyahadahFilter) {
            records.push({ santri: s, syahadah: sy });
          }
        });
      });

      titleElem.textContent = data.isAllTime 
        ? 'Daftar Santri Kelas 1, 2, & 3 Pemegang Sertifikasi Syahadah'
        : `Daftar Ujian Syahadah pada Periode ${data.startDateIndo} s/d ${data.endDateIndo}`;
      countElem.textContent = `${records.length} Catatan`;

      if (records.length === 0) {
        mobileCards.innerHTML = `<div class="p-6 text-center text-xs text-slate-400">Tidak ada catatan syahadah pada rentang waktu atau filter ini.</div>`;
        tbody.innerHTML = `<tr><td colspan="8" class="text-center py-8 text-slate-400">Tidak ada catatan syahadah pada rentang waktu atau filter ini.</td></tr>`;
        return;
      }

      mobileCards.innerHTML = records.map(r => {
        const s = r.santri;
        const sy = r.syahadah;
        const dateFormatted = formatIndoDate(sy.created_at);
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
              <div class="text-[10px] text-slate-500 mt-0.5 font-medium">Penguji: ${sy.penguji} • <strong>${dateFormatted}</strong></div>
              ${sy.catatan ? `<div class="italic text-[10px] text-slate-500 mt-1">"${sy.catatan}"</div>` : ''}
            </div>
            <button onclick="openSantriModal(${s.id})" class="w-full py-1.5 rounded-lg bg-emerald-50 text-emerald-800 font-semibold text-xs border border-emerald-200">
              Lihat Rapor 30 Juz
            </button>
          </div>
        `;
      }).join('');

      tbody.innerHTML = records.map(r => {
        const s = r.santri;
        const sy = r.syahadah;
        const dateFormatted = formatIndoDate(sy.created_at);
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
            <td class="py-3 px-4 text-xs"><div class="font-medium text-slate-800">${sy.penguji}</div><div class="text-[11px] text-emerald-800 font-semibold mt-0.5">${dateFormatted}</div></td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs italic">"${sy.catatan}"</td>
            <td class="py-3 px-4 text-center"><button onclick="openSantriModal(${s.id})" class="px-2.5 py-1 text-xs font-semibold rounded bg-emerald-50 hover:bg-emerald-100 text-emerald-800 transition">Rapor</button></td>
          </tr>
        `;
      }).join('');
    }

    function populateKelancaranTables() {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      const fluent = [...listSantri].filter(s => {
        return data.isAllTime ? s.total_juz_lancar > 0 : s.period_juz_lancar_count > 0;
      }).sort((a,b) => {
        if (!data.isAllTime) return b.period_juz_lancar_count - a.period_juz_lancar_count;
        return b.total_juz_lancar - a.total_juz_lancar;
      });
      
      document.getElementById('list-fluent-mobile').innerHTML = fluent.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-3 bg-white hover:bg-slate-50 cursor-pointer transition flex items-center justify-between">
          <div class="truncate mr-2">
            <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
            <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${data.isAllTime ? s.lancar_juz_str : (s.period_juz_lancar.map(j => 'Juz ' + j).join(', ') || '-')}</div>
          </div>
          <span class="px-2 py-1 rounded text-xs font-bold bg-emerald-100 text-emerald-800 shrink-0">
            ${data.isAllTime ? s.total_juz_lancar : s.period_juz_lancar_count} Juz Lancar
          </span>
        </div>
      `).join('');

      document.getElementById('table-fluent-students').innerHTML = fluent.map(s => `
        <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
          <td class="py-2 px-3 font-bold text-slate-900">${s.nama}</td>
          <td class="py-2 px-3 text-[11px] text-slate-500">${s.kelas_name}</td>
          <td class="py-2 px-3 font-bold text-emerald-700">${data.isAllTime ? s.total_juz_lancar : s.period_juz_lancar_count} Juz</td>
          <td class="py-2 px-3 text-[11px] text-slate-600 truncate max-w-xs">${data.isAllTime ? s.lancar_juz_str : (s.period_juz_lancar.map(j => 'Juz ' + j).join(', ') || '-')}</td>
          <td class="py-2 px-3 text-center"><button class="px-2 py-0.5 text-[11px] font-semibold rounded bg-emerald-50 text-emerald-800">Lihat</button></td>
        </tr>
      `).join('');

      const needAttn = [...listSantri].filter(s => {
        if (!data.isAllTime) {
          return s.period_juz_tidak_lancar_count > 0 || s.period_sabtu_count > 0;
        }
        return s.total_tidak_lancar > 0 || s.sabtu_issues_count > 0;
      }).sort((a,b) => {
        if (!data.isAllTime) {
          return (b.period_juz_tidak_lancar_count + b.period_sabtu_count) - (a.period_juz_tidak_lancar_count + a.period_sabtu_count);
        }
        return (b.total_tidak_lancar + b.sabtu_issues_count) - (a.total_tidak_lancar + a.sabtu_issues_count);
      });
      
      document.getElementById('list-need-attention-mobile').innerHTML = needAttn.map(s => `
        <div onclick="openSantriModal(${s.id})" class="p-3 bg-white hover:bg-slate-50 cursor-pointer transition flex items-center justify-between">
          <div class="truncate mr-2">
            <div class="font-bold text-xs text-slate-900 truncate">${s.nama}</div>
            <div class="text-[10px] text-slate-400 truncate">${s.kelas_name} • ${data.isAllTime ? (s.total_tidak_lancar > 0 ? s.tidak_lancar_str : 'Laporan Sabtu rapuh') : (s.period_juz_tidak_lancar.map(j=>'Juz '+j).join(', ') || 'Catatan Sabtu')}</div>
          </div>
          <span class="px-2 py-1 rounded text-xs font-bold bg-rose-100 text-rose-800 shrink-0">
            ${data.isAllTime ? (s.total_tidak_lancar > 0 ? `${s.total_tidak_lancar} Juz Remidi` : `${s.sabtu_issues_count}x Catatan`) : `${s.period_juz_tidak_lancar_count} Remidi • ${s.period_sabtu_count} Catatan`}
          </span>
        </div>
      `).join('');

      document.getElementById('table-need-attention-students').innerHTML = needAttn.map(s => `
        <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
          <td class="py-2 px-3 font-bold text-slate-900">${s.nama}</td>
          <td class="py-2 px-3 text-[11px] text-slate-500">${s.kelas_name}</td>
          <td class="py-2 px-3 font-bold text-rose-700">${data.isAllTime ? (s.total_tidak_lancar > 0 ? s.tidak_lancar_str : 'Lolos Tes') : (s.period_juz_tidak_lancar.map(j=>'Juz '+j).join(', ') || '-')}</td>
          <td class="py-2 px-3 text-[11px] text-amber-700 font-medium">${data.isAllTime ? `${s.sabtu_issues_count} catatan` : `${s.period_sabtu_count} catatan`}</td>
          <td class="py-2 px-3 text-center"><button class="px-2 py-0.5 text-[11px] font-semibold rounded bg-rose-50 text-rose-800">Bimbing</button></td>
        </tr>
      `).join('');
    }

    function populateGroupingCards() {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      // Classes (Kelas 1, 2, 3)
      const classContainer = document.getElementById('cards-classes-grid');
      const classMeta = [
        { id: 'kelas_1', name: 'Kelas 1 (Ula)' },
        { id: 'kelas_2', name: 'Kelas 2 (Wustho)' },
        { id: 'kelas_3', name: 'Kelas 3 (Ulya)' }
      ];

      classContainer.innerHTML = classMeta.map(cm => {
        const c_students = listSantri.filter(s => s.kelas_id === cm.id);
        const tot = c_students.length;
        const act = data.isAllTime ? c_students.filter(s => s.status === 'Aktif').length : c_students.filter(s => s.period_has_activity).length;
        const sy = data.isAllTime ? c_students.filter(s => s.has_syahadah).length : c_students.reduce((acc, s) => acc + s.period_syahadahs.length, 0);
        const j_ach = data.isAllTime ? c_students.reduce((acc, s) => acc + s.total_juz_dicapai, 0) : c_students.reduce((acc, s) => acc + s.period_juz_setor_count, 0);
        const j_lan = data.isAllTime ? c_students.reduce((acc, s) => acc + s.total_juz_lancar, 0) : c_students.reduce((acc, s) => acc + s.period_juz_lancar_count, 0);

        return `
          <div onclick="filterByGroup('kelas', '${cm.id}')" class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs hover:border-emerald-500 cursor-pointer transition">
            <div class="flex items-center justify-between mb-2.5">
              <h4 class="font-bold text-slate-900 text-xs sm:text-sm truncate">${cm.name}</h4>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-600 shrink-0">${tot} Santri</span>
            </div>
            <div class="space-y-1.5 text-xs text-slate-500">
              <div class="flex justify-between"><span>${data.isAllTime ? 'Santri Aktif:' : 'Santri Menyetor:'}</span><strong class="text-slate-700">${act}</strong></div>
              <div class="flex justify-between"><span>${data.isAllTime ? 'Total Hafalan:' : 'Total Disetor:'}</span><strong class="text-emerald-700 font-bold">${j_ach} Juz</strong></div>
              <div class="flex justify-between"><span>${data.isAllTime ? 'Total Lancar:' : 'Lulus Tes Lancar:'}</span><strong class="text-teal-700 font-bold">${j_lan} Juz</strong></div>
              <div class="flex justify-between"><span>Lulus Syahadah:</span><strong class="text-amber-700 font-bold">${sy} ${data.isAllTime ? `(${Math.round(sy/tot*100)}%)` : 'Lulus'}</strong></div>
            </div>
          </div>
        `;
      }).join('');

      // Halaqah
      const halaqahContainer = document.getElementById('cards-halaqah-grid');
      const halaqahs = Object.values(DB.halaqah_summary);

      halaqahContainer.innerHTML = halaqahs.map(h => {
        const m_students = listSantri.filter(s => s.musyrif_nama === h.musyrif_nama);
        const tot = m_students.length;
        const act = data.isAllTime ? m_students.filter(s => s.status === 'Aktif').length : m_students.filter(s => s.period_has_activity).length;
        const j_ach = data.isAllTime ? m_students.reduce((acc, s) => acc + s.total_juz_dicapai, 0) : m_students.reduce((acc, s) => acc + s.period_juz_setor_count, 0);
        const sy = data.isAllTime ? m_students.filter(s => s.has_syahadah).length : m_students.reduce((acc, s) => acc + s.period_syahadahs.length, 0);

        return `
          <div onclick="filterByGroup('halaqah', '${h.musyrif_nama}')" class="bg-white rounded-2xl p-4 border border-slate-200 shadow-xs hover:border-teal-500 cursor-pointer transition">
            <div class="flex items-center justify-between mb-2.5">
              <h4 class="font-bold text-slate-900 text-xs sm:text-sm truncate mr-2" title="${h.musyrif_nama}">${h.musyrif_nama}</h4>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-teal-50 text-teal-800 shrink-0">${tot} Santri</span>
            </div>
            <div class="space-y-1.5 text-xs text-slate-500">
              <div class="flex justify-between"><span>${data.isAllTime ? 'Santri Aktif:' : 'Santri Menyetor:'}</span><strong class="text-slate-700">${act}</strong></div>
              <div class="flex justify-between"><span>${data.isAllTime ? 'Total Juz:' : 'Juz Disetor:'}</span><strong class="text-emerald-700 font-bold">${j_ach} Juz</strong></div>
              <div class="flex justify-between"><span>Lulus Syahadah:</span><strong class="text-amber-700 font-bold">${sy} Santri</strong></div>
            </div>
          </div>
        `;
      }).join('');
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

    function initHalaqahFilterDropdown() {
      const select = document.getElementById('filterHalaqah');
      const halaqahs = Object.keys(DB.halaqah_summary);
      halaqahs.forEach(h => {
        const opt = document.createElement('option');
        opt.value = h;
        opt.textContent = h;
        select.appendChild(opt);
      });
    }

    function applyFilters() {
      const search = document.getElementById('searchInput').value.toLowerCase().trim();
      const kFilter = document.getElementById('filterKelas').value;
      const hFilter = document.getElementById('filterHalaqah').value;
      const sFilter = document.getElementById('filterSyahadah').value;

      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;

      filteredSantri = listSantri.filter(s => {
        if (search) {
          const matchName = s.nama.toLowerCase().includes(search);
          const matchNis = s.nis.toLowerCase().includes(search);
          if (!matchName && !matchNis) return false;
        }

        if (kFilter !== 'semua' && s.kelas_id !== kFilter) return false;
        if (hFilter !== 'semua' && s.musyrif_nama !== hFilter) return false;

        if (sFilter === 'syahadah') {
          if (data.isAllTime) { if (!s.has_syahadah) return false; }
          else { if (s.period_syahadahs.length === 0) return false; }
        } else if (sFilter === 'siap') {
          if (s.has_syahadah || s.total_juz_dicapai < 5) return false;
        } else if (sFilter === 'belum') {
          if (s.has_syahadah) return false;
        }

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
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      filteredSantri.sort((a,b) => {
        let valA, valB;
        if (currentSort.column === 'nama') {
          valA = a.nama.toLowerCase(); valB = b.nama.toLowerCase();
        } else if (currentSort.column === 'kelas') {
          valA = a.kelas_name; valB = b.kelas_name;
        } else if (currentSort.column === 'halaqah') {
          valA = a.musyrif_nama; valB = b.musyrif_nama;
        } else if (currentSort.column === 'juz_dicapai') {
          valA = data.isAllTime ? a.total_juz_dicapai : a.period_juz_setor_count;
          valB = data.isAllTime ? b.total_juz_dicapai : b.period_juz_setor_count;
        } else if (currentSort.column === 'juz_lancar') {
          valA = data.isAllTime ? a.total_juz_lancar : a.period_juz_lancar_count;
          valB = data.isAllTime ? b.total_juz_lancar : b.period_juz_lancar_count;
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

      const isAllTime = (currentPeriodData && currentPeriodData.isAllTime) || !currentPeriodData;

      // Mobile Cards View
      mobileContainer.innerHTML = filteredSantri.map(s => {
        const pct = Math.round((s.total_juz_dicapai / 30) * 100);
        let badgeSy = '';
        if (s.has_syahadah) {
          badgeSy = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">Syahadah ${s.highest_syahadah.toUpperCase()}</span>`;
        } else if (s.total_juz_dicapai >= 5) {
          badgeSy = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">Siap Ujian 1</span>`;
        }

        const periodSetorInfo = isAllTime 
          ? `<strong class="text-emerald-700">${s.total_juz_dicapai} Juz</strong>`
          : `<strong class="text-emerald-700">${s.period_juz_setor_count} Juz di periode ini</strong> (${s.total_juz_dicapai} total)`;

        const periodLancarInfo = isAllTime
          ? `${s.total_juz_lancar} Juz Lancar`
          : `${s.period_juz_lancar_count} Lancar (${s.total_juz_lancar} total)`;

        const lastActivityFormatted = isAllTime 
          ? (s.last_ziyadah ? s.last_ziyadah.created_at_indo : '-')
          : (s.period_last_date_indo || '-');

        return `
          <div onclick="openSantriModal(${s.id})" class="bg-white rounded-2xl p-3.5 border border-slate-200 shadow-xs space-y-2.5 active:scale-[0.99] transition cursor-pointer">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-slate-900">${s.nama}</h4>
                <div class="text-[10px] text-slate-400">NIS: ${s.nis} • ${s.kelas_name}</div>
              </div>
              <div class="text-right">${badgeSy}</div>
            </div>

            <div>
              <div class="flex justify-between text-[11px] mb-1">
                <span class="text-slate-500">Capaian: ${periodSetorInfo}</span>
                <span class="text-teal-700 font-semibold">${periodLancarInfo}</span>
              </div>
              <div class="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                <div class="bg-emerald-500 h-1.5 rounded-full" style="width: ${pct}%"></div>
              </div>
            </div>

            <div class="flex items-center justify-between pt-1 border-t border-slate-100 text-[10px] text-slate-400">
              <span class="truncate max-w-[180px]">Musyrif: ${s.musyrif_nama}</span>
              <span class="font-semibold text-emerald-800">${lastActivityFormatted} &rarr;</span>
            </div>
          </div>
        `;
      }).join('');

      // Desktop Table View
      tableBody.innerHTML = filteredSantri.map(s => {
        const pct = Math.round((s.total_juz_dicapai / 30) * 100);
        let syahadahBadge = '<span class="text-slate-400 text-xs">-</span>';
        if (s.has_syahadah) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-xs font-bold bg-amber-100 text-amber-800 border border-amber-300">Syahadah ${s.highest_syahadah.toUpperCase()}</span>`;
        } else if (s.total_juz_dicapai >= 5) {
          syahadahBadge = `<span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-300">Siap Ujian 1</span>`;
        }

        const achDisplay = isAllTime 
          ? `<div class="flex items-center gap-1.5"><span class="font-bold text-emerald-700 text-xs">${s.total_juz_dicapai} Juz</span><span class="text-[10px] text-slate-400">(${pct}%)</span></div>`
          : `<div class="flex items-center gap-1.5"><span class="font-bold text-emerald-700 text-xs">${s.period_juz_setor_count} Juz</span><span class="text-[10px] text-slate-400">(${s.total_juz_dicapai} total)</span></div>`;

        const lanDisplay = isAllTime
          ? `${s.total_juz_lancar} Juz`
          : `${s.period_juz_lancar_count} Juz (${s.total_juz_lancar} total)`;

        return `
          <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="openSantriModal(${s.id})">
            <td class="py-3 px-4 font-bold text-slate-900">${s.nama}<div class="text-[10px] text-slate-400 font-normal">NIS: ${s.nis}</div></td>
            <td class="py-3 px-4 text-xs">${s.kelas_name}<div class="text-[10px] text-slate-400">${s.jenis_kelamin}</div></td>
            <td class="py-3 px-4 text-xs font-medium text-slate-700 truncate max-w-[180px]">${s.musyrif_nama}</td>
            <td class="py-3 px-4">
              ${achDisplay}
              <div class="w-16 bg-slate-100 rounded-full h-1 mt-1 overflow-hidden"><div class="bg-emerald-500 h-1 rounded-full" style="width: ${pct}%"></div></div>
            </td>
            <td class="py-3 px-4 font-bold text-teal-700 text-xs">${lanDisplay}</td>
            <td class="py-3 px-4">${syahadahBadge}</td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-slate-100 text-slate-700">${s.fluency_label}</span></td>
            <td class="py-3 px-4 text-center"><button class="px-3 py-1 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs">Rapor</button></td>
          </tr>
        `;
      }).join('');
    }

    function openSantriModal(santriId) {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = data.periodSantriList || ALL_SANTRI;
      const s = listSantri.find(item => item.id === santriId);
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
      
      const lastAchDate = s.last_achievement ? formatIndoDate(s.last_achievement.created_at) : '-';
      document.getElementById('modal-target-desc').textContent = `Setoran Terakhir: ${s.last_achievement ? `${s.last_achievement.type.toUpperCase()} di Juz ${s.last_achievement.juz || '-'} (${lastAchDate})` : 'Belum ada setoran'}`;

      const grid = document.getElementById('modal-juz-grid');
      grid.innerHTML = s.juz_grid.map(g => {
        let style = 'bg-slate-100 text-slate-400 border-slate-200';
        if (g.status === 'lancar') style = 'bg-emerald-500 text-white font-bold border-emerald-600 shadow-xs';
        else if (g.status === 'hafal_belum_tes') style = 'bg-amber-400 text-slate-900 font-bold border-amber-500';
        else if (g.status === 'tidak_lancar') style = 'bg-rose-500 text-white font-bold border-rose-600';

        const isSetorInPeriod = (s.period_juz_setor || []).includes(g.juz);
        const periodRing = isSetorInPeriod ? 'ring-2 ring-emerald-400 ring-offset-1' : '';

        return `
          <button onclick="selectJuzTile(${g.juz})" type="button" class="p-1.5 sm:p-2 rounded-xl border text-center transition active:scale-95 ${style} ${periodRing}">
            <div class="text-[10px] sm:text-xs font-black">J${g.juz}</div>
            <div class="text-[8px] sm:text-[9px] mt-0.5 truncate">${g.status === 'lancar' ? 'Lancar' : (g.status === 'hafal_belum_tes' ? 'Setor' : (g.status === 'tidak_lancar' ? 'Remidi' : '-'))}</div>
          </button>
        `;
      }).join('');

      selectJuzTile(s.achieved_juz_list.length > 0 ? s.achieved_juz_list[0] : 1);

      const sySection = document.getElementById('modal-syahadah-section');
      const syList = document.getElementById('modal-syahadah-list');
      if (s.syahadahs.length > 0) {
        sySection.classList.remove('hidden');
        syList.innerHTML = s.syahadahs.map(sy => {
          const formattedDate = formatIndoDate(sy.created_at);
          return `
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200 text-xs space-y-1">
              <div class="flex items-center justify-between font-bold text-amber-900">
                <span>Syahadah ${sy.tingkat.toUpperCase()} (${sy.juz_cakupan_str})</span>
                <span class="px-2 py-0.5 rounded bg-amber-200 text-amber-900">${sy.predikat} (${sy.kesalahan} salah)</span>
              </div>
              <div class="text-[11px] text-slate-600">Penguji: ${sy.penguji} • <strong class="text-emerald-800">${formattedDate}</strong></div>
              ${sy.catatan ? `<div class="italic text-[10px] text-slate-500">"${sy.catatan}"</div>` : ''}
            </div>
          `;
        }).join('');
      } else {
        sySection.classList.add('hidden');
      }

      const evSection = document.getElementById('modal-evaluasi-section');
      const evList = document.getElementById('modal-evaluasi-list');
      if (s.sabtu_issues.length > 0) {
        evSection.classList.remove('hidden');
        evList.innerHTML = s.sabtu_issues.slice(0, 4).map(iss => {
          const formattedDate = formatIndoDate(iss.tanggal);
          return `
            <div class="p-2 rounded-lg bg-rose-50 border border-rose-200 text-xs flex items-center justify-between">
              <div>
                <strong class="text-rose-800">Juz ${iss.juz || '-'}</strong>
                <span class="text-slate-500 ml-1.5 text-[11px]">Hal ${iss.startPage} s.d. ${iss.endPage}</span>
              </div>
              <span class="text-[11px] font-semibold text-slate-500">${formattedDate}</span>
            </div>
          `;
        }).join('');
      } else {
        evSection.classList.add('hidden');
      }

      let rek = `Alhamdulillah, ananda ${s.nama} (${s.kelas_name}) saat ini telah menyelesaikan ${s.total_juz_dicapai} Juz. `;
      if (s.total_tidak_lancar > 0) {
        rek += `Sangat dianjurkan untuk memperkuat murajaah pada ${s.tidak_lancar_str} yang sebelumnya tercatat remidi sebelum menambah ziyadah baru. `;
      }
      if (s.total_juz_dicapai >= 5 && !s.has_syahadah) {
        rek += `Ananda sudah siap secara kapasitas untuk mengambil Ujian Syahadah 1 (5 Juz). Mohon bimbingan orang tua di rumah untuk melatih murajaah sambung ayat. `;
      } else if (s.has_syahadah) {
        rek += `Pertahankan pencapaian mutqin Syahadah ${s.highest_syahadah} dengan konsisten tadarus 1 juz per hari.`;
      } else {
        rek += `Pertahankan kedisiplinan setoran harian bersama musyrif halaqah.`;
      }
      document.getElementById('modal-rekomendasi').textContent = rek;

      document.getElementById('santriModal').classList.remove('hidden');
      lucide.createIcons();
    }

    function selectJuzTile(juzNum) {
      if (!currentModalSantri) return;
      const g = currentModalSantri.juz_grid.find(item => item.juz === juzNum);
      if (!g) return;

      document.getElementById('selected-juz-badge').textContent = g.juz;
      document.getElementById('selected-juz-title').textContent = `Juz ${g.juz}`;
      document.getElementById('selected-juz-surah').textContent = `(${g.name})`;
      document.getElementById('selected-juz-status').textContent = g.label;

      const statusElem = document.getElementById('selected-juz-status');
      if (g.status === 'lancar') {
        statusElem.className = 'text-[11px] font-bold text-emerald-700 shrink-0';
      } else if (g.status === 'tidak_lancar') {
        statusElem.className = 'text-[11px] font-bold text-rose-700 shrink-0';
      } else if (g.status === 'hafal_belum_tes') {
        statusElem.className = 'text-[11px] font-bold text-amber-700 shrink-0';
      } else {
        statusElem.className = 'text-[11px] font-semibold text-slate-400 shrink-0';
      }
    }

    function closeSantriModal() {
      document.getElementById('santriModal').classList.add('hidden');
      currentModalSantri = null;
    }

    function exportToCSV() {
      const data = currentPeriodData || computePeriodData(currentDateRange.start, currentDateRange.end);
      const listSantri = filteredSantri;
      
      let csv = 'NIS,Nama,Kelas,Halaqah,Status,Gender,Total Juz Dicapai,Juz Disetor di Periode,Total Juz Lancar,Syahadah,Aktivitas Terakhir di Periode\n';
      listSantri.forEach(s => {
        csv += `"${s.nis}","${s.nama}","${s.kelas_name}","${s.musyrif_nama}","${s.status}","${s.jenis_kelamin}",${s.total_juz_dicapai},${s.period_juz_setor_count || 0},${s.total_juz_lancar},"${s.highest_syahadah || '-'}","${s.period_last_date_indo || '-'}"\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `laporan_tahfidz_kelas_123_${currentDateRange.start}_sd_${currentDateRange.end}.csv`;
      link.click();
    }

    document.addEventListener('DOMContentLoaded', () => {
      document.getElementById('filterStartDate').value = DB.metadata.min_date;
      document.getElementById('filterEndDate').value = DB.metadata.max_date;
      document.getElementById('topBarUpdateDate').textContent = `Pembaruan: ${formatIndoDate(DB.metadata.max_date)}`;
      document.getElementById('footerMetadata').innerHTML = `Snapshot: <code class="font-mono text-emerald-700">everynight-in-my-dream.db</code> • 44 Santri • Pembaruan: ${formatIndoDate(DB.metadata.max_date)}`;

      initHalaqahFilterDropdown();
      setPresetRange('all');
    });
  </script>

</body>
</html>
"""

final_html = html_content.replace('DATA_JSON_PLACEHOLDER', json_data_str)

output_path = 'index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Generated index.html successfully! Size: {os.path.getsize(output_path) / 1024:.2f} KB")
