# -*- coding: utf-8 -*-
import json
import os
import subprocess
import time

CROCKFORD_BASE32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'

def generate_ulid(timestamp_ms=None):
    """Generate standard 26-char Crockford Base32 ULID"""
    if timestamp_ms is None:
        timestamp_ms = int(time.time() * 1000)
    time_chars = [''] * 10
    t = timestamp_ms
    for i in range(9, -1, -1):
        time_chars[i] = CROCKFORD_BASE32[t & 0x1F]
        t >>= 5
    rand_bytes = os.urandom(10)
    rand_val = int.from_bytes(rand_bytes, byteorder='big')
    rand_chars = [''] * 16
    for i in range(15, -1, -1):
        rand_chars[i] = CROCKFORD_BASE32[rand_val & 0x1F]
        rand_val >>= 5
    return ''.join(time_chars) + ''.join(rand_chars)

# Automatically extract latest data from SQLite if needed
if os.path.exists('process_classes_123.py') and os.path.exists('everynight-in-my-dream.db'):
    if not os.path.exists('full_report_dataset.json') or os.path.getmtime('everynight-in-my-dream.db') > os.path.getmtime('full_report_dataset.json'):
        print('Mengekstrak data terbaru dari SQLite (Kelas 1, 2, & 3)...')
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

  <!-- Custom Stylesheet with ULID Cache Busting -->
  <link rel="stylesheet" href="style.css?CSS_ULID_PLACEHOLDER">
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
              Evaluasi Hafalan, Ujian Juziyah, Syahadah 5-Juz, & Mutqin Santri
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
              Menampilkan pencapaian santri dalam periode yang Anda pilih. Pilih tanggal atau klik tombol pintas di bawah.
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

      <!-- Executive KPI Cards (6 Tahfidz Metrics - Evaluasi Sabtu Excluded) -->
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
            22 Sertifikat (5-Juz Mutqin)
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

        <!-- KPI 5: Ujian Juziyah Tuntas -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Ujian Juziyah</span>
              <i data-lucide="bookmark-check" class="w-4 h-4 text-indigo-600"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-indigo-900" id="kpi-total-juziyah">150</div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-juziyah">
            Ujian 1-Juz Sekali Duduk
          </div>
        </div>

        <!-- KPI 6: Total Aktivitas Setoran & Ujian -->
        <div class="bg-white rounded-2xl p-3.5 sm:p-4 border border-slate-200 shadow-xs flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between text-slate-400 mb-1.5">
              <span class="text-[11px] font-semibold text-slate-500">Total Setor & Tes</span>
              <i data-lucide="file-text" class="w-4 h-4 text-blue-600"></i>
            </div>
            <div class="text-xl sm:text-2xl font-black text-slate-800" id="kpi-total-pencapaian">3.670</div>
          </div>
          <div class="mt-2 text-[10px] sm:text-[11px] text-slate-500 font-medium border-t border-slate-100 pt-1.5" id="kpi-sub-pencapaian">
            3.449 Setor • 221 Tes
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

        <!-- Chart 3: Peta Kendala Ujian Kelancaran -->
        <div class="bg-white rounded-2xl sm:rounded-3xl p-4 sm:p-5 border border-slate-200 shadow-xs lg:col-span-2">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
            <div>
              <h4 class="font-bold text-sm sm:text-base text-slate-900">Peta Tingkat Kesulitan 30 Juz Al-Qur'an (Remidi Ujian Kelancaran)</h4>
              <p class="text-xs text-slate-500">Jumlah frekuensi tes kelancaran yang belum lulus / perlu remidi per juz</p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="flex items-center gap-1.5 text-rose-600 font-medium">
                <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Jumlah Remidi Tes Kelancaran
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
              <span class="text-[10px] font-semibold text-slate-400">Paling Banyak Remidi</span>
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
            <p class="text-xs sm:text-sm text-slate-500">Mengetahui siapa santri yang paling lancar (teruji mutqin) dan siapa yang sedang dalam proses remidi ujian kelancaran.</p>
          </div>
        </div>
      </div>

      <!-- Dual Section: Paling Lancar vs Perlu Remidi -->
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

        <!-- Kolom Kanan: Butuh Perhatian / Remidi Ujian -->
        <div class="bg-white rounded-2xl sm:rounded-3xl border border-slate-200 shadow-xs overflow-hidden flex flex-col justify-between">
          <div>
            <div class="p-4 bg-rose-50/50 border-b border-rose-100 flex items-center justify-between">
              <div>
                <h4 class="font-bold text-xs sm:text-sm text-rose-950 flex items-center gap-1.5">
                  <i data-lucide="alert-circle" class="w-4 h-4 text-rose-600"></i>
                  Santri Membutuhkan Bimbingan & Remidi
                </h4>
                <p class="text-[11px] text-rose-800">Santri yang memiliki catatan tes kelancaran yang belum lulus</p>
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
                    <th class="py-2 px-3">Juz Belum Lulus</th>
                    <th class="py-2 px-3">Status Remidi</th>
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
            <div><strong class="text-slate-800">Juziyah:</strong> Ujian kelulusan 1 juz lengkap sekali duduk.</div>
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
            <div class="text-[10px] uppercase font-bold text-slate-500">Ujian Juziyah</div>
            <div class="text-lg font-black text-slate-800 mt-0.5" id="modal-juziyah-count">0 Juziyah</div>
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

        <!-- Juziyah History List -->
        <div class="space-y-2" id="modal-juziyah-section">
          <h4 class="font-bold text-xs sm:text-sm text-slate-900 flex items-center gap-1.5">
            <i data-lucide="bookmark-check" class="w-4 h-4 text-indigo-600"></i>
            Riwayat Ujian Juziyah (1-Juz Sekali Duduk)
          </h4>
          <div class="space-y-1.5" id="modal-juziyah-list"></div>
        </div>

        <!-- Rekomendasi Musyrif -->
        <div class="p-3.5 rounded-2xl bg-emerald-50/70 border border-emerald-200 text-xs space-y-1">
          <div class="font-bold text-emerald-950 flex items-center gap-1.5">
            <i data-lucide="message-square" class="w-4 h-4 text-emerald-700"></i>
            Rekomendasi Bimbingan untuk Santri & Wali
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

  <!-- Application Logic with ULID Cache Busting -->
  <script src="app.js?JS_ULID_PLACEHOLDER"></script>
</body>
</html>
"""

css_ulid = generate_ulid()
js_ulid = generate_ulid()
print(f"Generated ULID for CSS: {css_ulid}")
print(f"Generated ULID for JS:  {js_ulid}")

final_html = html_content.replace('DATA_JSON_PLACEHOLDER', json_data_str)
final_html = final_html.replace('CSS_ULID_PLACEHOLDER', css_ulid)
final_html = final_html.replace('JS_ULID_PLACEHOLDER', js_ulid)

output_path = 'index.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Generated index.html successfully! Size: {os.path.getsize(output_path) / 1024:.2f} KB")
