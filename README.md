# Laporan & Evaluasi Capaian Tahfidz Santri (Kelas 1, 2, & 3)

Aplikasi dashboard eksekutif dan laporan interaktif pencapaian tahfidz santri berbasis data SQLite (`everynight-in-my-dream.db`). Dirancang khusus agar **mudah dipahami oleh orang awam dan wali santri**, memiliki **tampilan terang (Light Mode)** yang bersih dan elegan, serta **sangat optimal dibuka di layar ponsel pintar (HP/Smartphone)** maupun desktop.

> [!NOTE]
> **Cakupan Data**: Laporan ini secara ketat **hanya menampilkan data santri Kelas 1, Kelas 2, dan Kelas 3 (Total 44 santri)**. Angkatan senior terdahulu (2020–2023) dan alumni tidak disertakan.

---

## 🌟 Fitur Unggulan

### 1. 📱 Desain Mobile-First & Strictly Light Mode
- **Khusus Light Mode**: Menggunakan palet warna hijau zamrud (*emerald*) dan abu-abu lembut (*slate*) yang sejuk di mata, tanpa mode gelap.
- **Tampilan Ponsel Pintar (HP)**:
  - Mengubah tabel panjang menjadi kartu santri (*card view*) yang ringkas dan ramah sentuhan jempol saat dibuka di HP.
  - *Bottom Sheet Modal* untuk melihat rapor 30 juz santri secara penuh.
  - Tab navigasi geser horizontal (*horizontal swipeable tabs*) yang praktis di layar sempit.
  - Tombol-tombol dengan ukuran target sentuh (*touch target*) minimal 44px.

### 2. 📊 Ringkasan Eksekutif (Dashboard KPI)
- **6 Indikator Kunci**:
  1. **Total Santri Terdaftar**: 44 santri (42 aktif, 2 non-aktif).
  2. **Kelulusan Syahadah**: 19 santri (22 sertifikat kelulusan).
  3. **Total Juz Hafal**: 334 juz terakumulasi.
  4. **Total Juz Mutqin / Lancar**: 96 juz telah teruji lancar.
  5. **Total Riwayat Evaluasi**: 3.449 catatan capaian ziyadah & 221 ujian juziyah.
  6. **Laporan Evaluasi Musyrif**: 226 lembar evaluasi pekanan.
- **Grafik Interaktif (Chart.js)**:
  - Komparasi Capaian per Jenjang Kelas (Ula, Wustho, Ulya).
  - Proporsi Kelulusan Syahadah.
  - Rasio Hafalan Lancar vs Belum Ujian Kelancaran.
  - 10 Santri dengan Capaian Hafalan Terbanyak.

### 3. 📜 Laporan Khusus Syahadah (Ujian Akbar 5-Juz Sekali Duduk)
- **Daftar Lulusan Syahadah**:
  - Daftar 19 santri peraih Syahadah 1 (5 Juz), Syahadah 2 (10 Juz), Syahadah 3 (15 Juz), hingga Syahadah 4 (20 Juz).
  - Rincian predikat resmi: **Mumtaz** (0-10 kesalahan), **Jayyid Jiddan** (11-20 kesalahan), **Jayyid** (21-30 kesalahan).
  - Catatan resmi langsung dari penguji tahfidz.
- **Analisis Siapa yang Belum Syahadah**:
  - **Kelompok Siap Ujian (9 santri)**: Santri yang hafalannya sudah mencapai &ge;5 juz namun belum mengambil ujian Syahadah resmi.
  - **Kelompok Sedang Berproses (15 santri)**: Santri yang sedang berproses menghafal 1–4 juz awal.
  - **Kelompok Belum Mulai (1 santri)**: Santri non-aktif.

### 4. 🎯 Analisis Kelancaran & Peta Hambatan 30 Juz
- **Daftar Santri Paling Lancar (Top Mutqin)**.
- **Daftar Santri Butuh Penguatan (Perlu Murajaah / Remidi)**.
- **Peta Kendala 30 Juz**: Menganalisis juz mana saja yang paling menantang bagi santri (Juz 1, 2, 29, 3) disertai panduan cara mengatasinya.

### 5. 👥 Pengelompokan Kelas & Halaqah
- **Berdasarkan Jenjang Kelas**:
  - **Kelas 1 (Ula)**: Angkatan 2026 (11 santri, rata-rata 3,0 juz).
  - **Kelas 2 (Wustho)**: Angkatan 2025 (16 santri, rata-rata 6,3 juz, 8 peraih Syahadah).
  - **Kelas 3 (Ulya)**: Angkatan 2024 (17 santri, rata-rata 11,8 juz, 11 peraih Syahadah).
- **Berdasarkan Halaqah Musyrif**:
  - Mengelompokkan santri ke dalam 6 kelompok halaqah bimbingan musyrif (Ulya Ikhwan, Ula Ikhwan, Wustho Ikhwan, Ulya Akhwat, Wustho Akhwat, Ula Akhwat).

### 6. 🔍 Direktori & Rapor Santri Interaktif (Peta Visual 30 Juz)
- Pencarian instan berdasarkan nama atau NIS.
- Filter multi-dimensi (Kelas, Halaqah, Status Syahadah).
- Klik nama santri untuk membuka **Rapor 30 Juz Visual**:
  - Peta kisi warna-warni 30 Juz (Hijau = Lancar/Mutqin, Kuning = Selesai setor belum tes, Merah = Butuh remidi, Abu-abu = Belum mulai).
  - Riwayat ujian dan skor kesalahan.
  - Catatan evaluasi pekanan dan saran bimbingan musyrif untuk wali santri di rumah.

### 7. 📖 Panduan Awam & Glosarium
- Penjelasan sederhana mengenai alur menghafal (Ziyadah &rarr; Setengah Juz &rarr; Juziyah &rarr; Tes Kelancaran &rarr; Syahadah 5-Juz Sekali Duduk).
- Mengapa urutan hafalan dimulai dari Juz 30 & 29 baru ke Juz 1 s.d. 28.
- Kriteria nilai (Mumtaz, Jayyid Jiddan, Jayyid, Maqbul, Mardud).
- Tips praktis pendampingan orang tua di rumah.

---

## 🚀 Cara Membuka & Menggunakan

File `index.html` dibuat bersifat **mandiri (*single standalone HTML*)**. Anda tidak membutuhkan web server khusus:

1. **Buka di Komputer / Laptop**:
   Cukup klik ganda (*double click*) file [index.html](index.html) untuk langsung membukanya di peramban favorit Anda (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari, dll.).

2. **Buka di Ponsel Pintar (HP)**:
   - Kirimkan file `index.html` ke ponsel melalui WhatsApp / Telegram / Google Drive lalu buka menggunakan peramban HP.
   - Atau buka melalui GitHub Pages / local server.

3. **Menjalankan via Local Server (Opsional)**:
   ```bash
   python -m http.server 8000
   ```
   Lalu buka `http://localhost:8000` di browser.

4. **Ekspor Data & Cetak**:
   - Terdapat tombol **"Ekspor CSV"** untuk mengunduh rekap tabel santri ke Excel/Spreadsheet.
   - Terdapat tombol **"Cetak / PDF"** yang sudah diformat khusus tanpa tombol/elemen antarmuka yang mengganggu.

---

## 🛠️ Cara Memperbarui / Regenerasi Data

Jika ada penambahan data baru di `everynight-in-my-dream.db`:
```bash
python build_index_html.py
```
Skrip ini akan secara otomatis:
1. Memproses ulang data SQLite santri Kelas 1, 2, dan 3 (`process_classes_123.py`).
2. Menghasilkan dataset terstruktur `full_report_dataset.json`.
3. Memperbarui tampilan `index.html`.
