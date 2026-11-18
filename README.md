# Laporan & Evaluasi Capaian Tahfidz Santri (Kelas 1, 2, & 3)

Aplikasi dashboard eksekutif dan laporan interaktif pencapaian tahfidz santri berbasis data SQLite (`everynight-in-my-dream.db`). Dirancang khusus agar **mudah dipahami oleh orang awam dan wali santri**, menggunakan **format tanggal lengkap bahasa Indonesia** (*contoh: Selasa, 30 Januari 2024*), memiliki **fitur filter rentang waktu interaktif**, tampilan **terang (Light Mode)** yang sejuk, serta **sangat optimal dibuka di layar ponsel pintar (HP/Smartphone)** maupun desktop.

> [!NOTE]
> **Cakupan Data**: Laporan ini secara ketat **hanya menampilkan data santri Kelas 1, Kelas 2, dan Kelas 3 (Total 44 santri)**. Angkatan senior terdahulu (2020–2023), alumni, serta **data evaluasi Sabtu (`laporansabtu`) dikecualikan**.

---

## 🌟 Fitur Unggulan

### 1. 📅 Filter Rentang Waktu Interaktif & Format Tanggal Bahasa Indonesia
- **Format Tanggal Bahasa Indonesia**:
  - Semua tanggal ditampilkan dalam format baku: `[Hari], [Tanggal] [Bulan] [Tahun]` (contoh: *Selasa, 30 Januari 2024*, *Minggu, 17 Mei 2026*, *Rabu, 18 November 2026*).
- **Filter Rentang Waktu (Date Range Picker)**:
  - Pengguna dapat memilih tanggal awal (*Dari Tanggal*) dan tanggal akhir (*Sampai Tanggal*) secara bebas.
  - **Tombol Pilihan Cepat (Presets)**:
    - **Semua Waktu**: Menampilkan seluruh riwayat akumulasi (16 Januari 2026 s/d 18 November 2026).
    - **🎯 Contoh Permintaan (1 Jul – 3 Okt 2026)**: Menampilkan aktivitas khusus pada kuartal 3 tahun 2026 (1.387 catatan setoran/ujian, 7 kelulusan syahadah, 72 tes lancar).
    - **Semester Ganjil 2026**: Rentang Juli 2026 s/d November 2026.
    - **Semester Genap 2026**: Rentang Januari 2026 s/d Juni 2026.
    - **30 Hari Terakhir**: Aktivitas 30 hari terakhir santri.
  - **Perhitungan Ulang Instan (Zero Reload)**:
    - Seluruh metrik KPI (santri menyetor, setoran juz, lulus syahadah, tes lancar, ujian juziyah) otomatis dihitung ulang dalam hitungan milidetik.
    - Ke-4 grafik visual (Chart.js) diperbarui secara dinamis mengikuti rentang waktu terpilih.
    - Tabel & kartu Syahadah hanya menampilkan santri yang mengambil ujian pada rentang waktu tersebut.
    - Modal rapor 30 juz menyorot juz yang disetor atau diuji pada rentang waktu terpilih dengan bingkai khusus (*ring highlight*).

### 2. 📱 Desain Mobile-First & Strictly Light Mode
- **Khusus Light Mode**: Menggunakan palet warna hijau zamrud (*emerald*) dan abu-abu lembut (*slate*) yang sejuk di mata, tanpa mode gelap.
- **Tampilan Ponsel Pintar (HP)**:
  - Mengubah tabel panjang menjadi kartu santri (*card view*) yang ringkas dan ramah sentuhan jempol saat dibuka di HP.
  - *Bottom Sheet Modal* untuk melihat rapor 30 juz santri secara penuh.
  - Tab navigasi geser horizontal (*horizontal swipeable tabs*) yang praktis di layar sempit.
  - Ukuran target sentuh (*touch target*) minimal 44px.

### 3. 📊 Ringkasan Eksekutif (Dashboard KPI)
- **6 Indikator Kunci Dinamis**:
  1. **Santri Terdaftar / Menyetor**: 44 santri terdaftar (42 aktif).
  2. **Kelulusan Syahadah**: 19 santri (22 sertifikat kelulusan 5-juz mutqin).
  3. **Akumulasi Setoran Juz**: 334 juz hafal (rata-rata 7,6 juz/santri).
  4. **Juz Teruji Mutqin / Lancar**: 96 juz lulus ujian kelancaran.
  5. **Ujian Juziyah Tuntas**: 150 ujian kelulusan 1-juz sekali duduk.
  6. **Total Catatan Aktivitas**: 3.670 catatan (3.449 setoran & 221 tes).
- **Grafik Interaktif (Chart.js)**:
  - Komparasi Capaian per Jenjang Kelas (Ula, Wustho, Ulya).
  - Proporsi Kelulusan Syahadah.
  - Peta Kendala Remidi Ujian Kelancaran 30 Juz Al-Qur'an.
  - Top 5 Santri Hafalan Terbanyak & Top 5 Santri Paling Mutqin.

### 4. 📜 Laporan Khusus Syahadah (Ujian Akbar 5-Juz Sekali Duduk)
- **Daftar Lulusan Syahadah**:
  - Daftar peraih Syahadah 1 (5 Juz), Syahadah 2 (10 Juz), Syahadah 3 (15 Juz), hingga Syahadah 4 (20 Juz).
  - Rincian predikat resmi: **Mumtaz** (0-10 kesalahan), **Jayyid Jiddan** (11-20 kesalahan), **Jayyid** (21-30 kesalahan).
  - Nama penguji, tanggal ujian resmi (format bahasa Indonesia), dan catatan dewan penguji.
- **Analisis Kesiapan Ujian**:
  - **Kelompok Siap Ujian (9 santri)**: Santri yang hafalannya sudah mencapai &ge;5 juz namun belum mengambil ujian Syahadah resmi.
  - **Kelompok Sedang Berproses (15 santri)**: Santri yang sedang berproses menghafal 1–4 juz awal.

### 5. 🎯 Analisis Kelancaran & Peta Hambatan 30 Juz
- **Daftar Santri Paling Lancar (Top Mutqin)**.
- **Daftar Santri Membutuhkan Bimbingan & Remidi**: Menampilkan santri yang belum lulus tes kelancaran.
- **Peta Kendala 30 Juz**: Menganalisis juz mana saja yang paling banyak memerlukan remidi tes kelancaran (Juz 1, 2, 29, 4, 3, 30).

### 6. 👥 Pengelompokan Kelas & Halaqah
- **Berdasarkan Jenjang Kelas**:
  - **Kelas 1 (Ula)**: Angkatan 2026 (11 santri, rata-rata 3,0 juz).
  - **Kelas 2 (Wustho)**: Angkatan 2025 (16 santri, rata-rata 6,3 juz, 8 peraih Syahadah).
  - **Kelas 3 (Ulya)**: Angkatan 2024 (17 santri, rata-rata 11,8 juz, 11 peraih Syahadah).
- **Berdasarkan Halaqah Musyrif**:
  - Mengelompokkan santri ke dalam 6 kelompok halaqah bimbingan musyrif (Ulya Ikhwan, Ula Ikhwan, Wustho Ikhwan, Ulya Akhwat, Wustho Akhwat, Ula Akhwat).

### 7. 🔍 Direktori & Rapor Santri Interaktif (Peta Visual 30 Juz)
- Pencarian instan (Nama, NIS).
- Filter multi-dimensi (Kelas, Halaqah, Status Syahadah).
- **Modal Interaktif 30 Juz Visual Grid**:
  - Peta kisi 30 Juz (Hijau = Lancar/Mutqin, Kuning = Selesai setor belum tes, Merah = Butuh remidi, Abu-abu = Belum mulai).
  - Sorotan khusus (*highlight ring*) untuk juz yang disetor pada rentang waktu terpilih.
  - Riwayat ujian Syahadah dan ujian Juziyah lengkap dengan tanggal format bahasa Indonesia.
  - Rekomendasi personal musyrif untuk orang tua / wali santri di rumah.

### 8. 📖 Panduan Awam & Glosarium
- Penjelasan alur belajar (Ziyadah &rarr; Setengah Juz &rarr; Juziyah &rarr; Tes Kelancaran &rarr; Syahadah 5-Juz).
- Alasan urutan hafalan dimulai dari Juz 30 & 29 baru ke Juz 1 s.d. 28.
- Tabel standar nilai predikat (Mumtaz s.d. Mardud).
- Tips pendampingan murajaah anak di rumah.

---

## 🚀 Cara Membuka & Menggunakan

File `index.html` bersifat **mandiri (*single standalone HTML*)**:

1. **Buka di Komputer / Laptop**:
   Cukup klik ganda (*double click*) file [index.html](index.html) untuk langsung membukanya di browser favorit Anda (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari, dll.).

2. **Buka di Ponsel Pintar (HP)**:
   - Kirimkan file `index.html` ke ponsel melalui WhatsApp / Telegram / Google Drive lalu buka dengan peramban bawaan ponsel.
   - Atau buka melalui GitHub Pages / hosting web.

3. **Menjalankan via Local Server (Opsional)**:
   ```bash
   python -m http.server 8000
   ```
   Lalu buka `http://localhost:8000` di peramban.

4. **Ekspor Data & Cetak**:
   - Tombol **"Ekspor CSV"** mengunduh rekap santri sesuai rentang tanggal yang sedang aktif.
   - Tombol **"Cetak / PDF"** memformat tampilan bersih khusus pencetakan dokumen fisik atau arsip PDF.

---

## 🛠️ Cara Memperbarui / Regenerasi Data

Jika ada pembaruan data di database SQLite `everynight-in-my-dream.db`:
```bash
python build_index_html.py
```
Skrip ini akan secara otomatis:
1. Membaca data terbaru untuk santri Kelas 1, 2, dan 3 (`process_classes_123.py`) tanpa menyertakan evaluasi Sabtu.
2. Menghasilkan dataset terstruktur `full_report_dataset.json` lengkap dengan tanggal bahasa Indonesia dan rekaman aktivitas mentah.
3. Memperbarui `index.html`.
