# Laporan & Evaluasi Capaian Tahfidz Santri

Aplikasi dashboard eksekutif dan laporan komprehensif pencapaian tahfidz santri berbasis data SQLite (`everynight-in-my-dream.db`). Dirancang agar mudah dipahami oleh siapa saja, mulai dari pimpinan pesantren, asatidzah/musyrif, orang tua / wali santri, hingga masyarakat umum.

---

## 🌟 Fitur Utama

1. **Ringkasan Eksekutif (Dashboard KPI)**:
   - 6 Metrik Kunci: Total Santri (115 total, 97 aktif), Total Lulus Syahadah (26 santri, 29 sertifikat), Akumulasi Juz Dihafal (540 juz), Juz Teruji Mutqin/Lancar (96 juz), Total Catatan Ziyadah & Ujian (4.228 riwayat), dan Laporan Evaluasi Sabtu (364 catatan).
   - Penjelasan awam ramah wali santri ("Bagaimana cara membaca laporan ini?").
   - 4 Visual Chart interaktif: Komparasi antar kelas, Proporsi Syahadah, Rasio Kelancaran, dan Top Performers.

2. **Laporan Syahadah (Ujian Akbar 5-Juz Mutqin)**:
   - Rincian 26 Santri pemegang Syahadah (Syahadah 1 [5 Juz], Syahadah 2 [10 Juz], Syahadah 3 [15 Juz], Syahadah 4 [20 Juz]).
   - Predikat nilai resmi pesantren: Mumtaz (0-10 salah), Jayyid Jiddan (11-20 salah), Jayyid (21-30 salah), Maqbul (31-40 salah), Mardud (>40 salah).
   - Catatan evaluasi langsung dari penguji tahfidz.
   - **Analisis Siapa yang Belum Syahadah**:
     - Kelompok Siap Ujian (20 santri yang sudah hafal &ge;5 juz namun belum mengambil ujian resmi).
     - Kelompok Sedang Berproses (17 santri yang sudah hafal 1-4 juz).
     - Distribusi per jenjang kelas.

3. **Status Kelancaran (Mutqin vs Perlu Murajaah)**:
   - Siapa saja santri paling lancar (Top Mutqin).
   - Siapa saja santri yang membutuhkan penguatan/remidi (gagal tes kelancaran atau catatan rapuh di evaluasi Sabtu).
   - Peta analisis kendala pada 30 Juz Al-Quran (Juz 1, 2, 29, 3, 30 paling sering mengalami kebuntuan) beserta penjelasan metodologis penyebab kesulitannya.

4. **Grouping Berdasarkan Kelas & Halaqah**:
   - **Per Jenjang Kelas**: Kelas 1 (Ula), Kelas 2 (Wustho), Kelas 3 (Ulya), Angkatan 2023 (Senior), dan Alumni (2020-2022).
   - **Per Halaqah Musyrif**: 6 Halaqah aktif (Ulya Ikhwan, Ula Ikhwan, Whusto Ikhwan, Ulya Akhwat, Wustho Akhwat, Ula Akhwat).
   - Metrik per kelompok: total santri, rasio aktif, rata-rata juz dicapai, rata-rata juz lancar, persentase kelulusan syahadah.

5. **Direktori & Profil Santri Interaktif (Rapor 30 Juz)**:
   - Pencarian real-time (Nama, NIS, NIK).
   - Multi-filter: Kelas, Halaqah, Status Syahadah, Kelancaran.
   - Sorting tabel pada seluruh kolom.
   - **Modal Interaktif 30 Juz Visual Grid**:
     - Peta 30 kotak juz dengan kode warna (Hijau = Lancar, Kuning = Sudah hafal belum tes, Merah = Perlu remidi, Abu-abu = Belum mulai).
     - Riwayat ujian Syahadah, ujian Juziyah, dan catatan evaluasi Sabtu.
     - Rekomendasi musyrif personal untuk santri dan wali santri.

6. **Panduan Awam & Glosarium Tahfidz**:
   - Bagan alur tahapan belajar (Ziyadah &rarr; Setengah Juz &rarr; Juziyah &rarr; Ujian Kelancaran &rarr; Syahadah).
   - Arti istilah: Ziyadah, Murajaah, Mutqin, Syahadah, dan urutan hafalan khas pesantren (30, 29, 1 s.d. 28).
   - Standar nilai predikat pesantren (Mumtaz s.d. Mardud).
   - Pesan dan tips pendampingan untuk ayah/bunda wali santri di rumah.

7. **Fitur Tambahan**:
   - Mode Gelap / Terang (Dark / Light Mode Toggle).
   - Ekspor data santri ke format CSV.
   - Tampilan ramah cetak (`window.print()` / Simpan PDF).
   - Bekerja 100% mandiri (*single standalone HTML*), dapat dibuka langsung di browser mana pun tanpa butuh web server.

---

## 🚀 Cara Menjalankan

Cukup buka file `index.html` langsung di browser favorit Anda (Google Chrome, Microsoft Edge, Mozilla Firefox, dll.) dengan klik ganda (*double click*).

Jika ingin menjalankan melalui local server:
```bash
python -m http.server 8000
```
Lalu buka `http://localhost:8000` di browser.

---

## 🛠️ Regenerasi Data

Jika database `everynight-in-my-dream.db` mengalami pembaruan, jalankan perintah:
```bash
python build_index_html.py
```
Perintah ini akan membaca ulang database SQLite, menyusun kembali ringkasan statistik, dan memperbarui `index.html`.
