# API Dokumentasi: Santri Detail Endpoint

## Endpoint
```
GET http://localhost:4848/santri.php?nik=[NIK_SANTRI]
```

## Deskripsi
REST API endpoint yang menyediakan data lengkap dan mendalam tentang santri, termasuk pencapaian hafalan, kecepatan belajar, dan prediksi penyelesaian. Dapat diakses dari website manapun (CORS enabled).

## Parameter

| Parameter | Tipe | Wajib | Deskripsi |
|-----------|------|-------|-----------|
| `nik` | string | Ya | Nomor Induk Kependudukan santri (16 digit) |

## Response Structure

### Root Object
```json
{
  "success": true,
  "santri": {
    "nik": "string",
    "nama": "string",
    "namaPanggilan": "string",
    "jenisKelamin": "string",  // "Laki-laki" atau "Perempuan"
    "status": "string",
    "pencapaianJuz": {...},
    "pencapaianTerakhir": {...},
    "targetHafalan": number,
    "juziyah": [...],
    "syahadah": [...],
    "10LogTerakhir": [...],
    "kecepatan": {...},
    "prediksi": {...},
    "dataTambahan": {...},
    "rekomendasi": "string"
  }
}
```

### Field Details

#### 1. **pencapaianJuz**
Informasi juz yang telah dicapai santri menggunakan sistem sekuensial.

```json
{
  "juzYangDicapai": [30, 29, 1, 2, 3],      // Juz yang dicapai berdasarkan sekuens
  "juzYangLancar": [2],                      // Juz yang sudah berhasil dites (lancar)
  "juzYangTidakLancar": [30, 29, 1, 3]      // Juz yang sudah dicapai tapi belum dites
}
```

**Logika:**
- Menggunakan sistem sekuens juz: **[30, 29, 1, 2, 3, 4, ..., 28]**
- `juzYangDicapai`: Semua juz hingga posisi tertinggi yang dicapai dalam sekuens. Jika santri sudah mencapai juz 3, berarti otomatis sudah mencapai juz 30, 29, 1, 2, dan 3
- `juzYangLancar`: Distinct juz dari table `tes`
- `juzYangTidakLancar`: `juzYangDicapai` - `juzYangLancar` (juz yang sudah dicapai tapi belum dites)

#### 2. **pencapaianTerakhir**
Data pencapaian terakhir santri (khusus type `ziyadah`). Jika pencapaian terakhir bukan ziyadah, akan mencari ziyadah terakhir.

```json
{
  "tanggal": "2023-12-01 12:23:00",
  "juz": 3,
  "halaman": "1A",
  "kesalahan": 1
}
```

**Catatan:** Field ini `null` jika santri belum pernah mencapai ziyadah.

#### 3. **targetHafalan**
Target hafalan santri berdasarkan kelas (dihitung dari `tahun_masuk` dan settings kelas).

```json
"targetHafalan": 2  // Berarti targetnya Juz 2
```

**Logika:**
- Kelas 1 (`kelas1_year`): target = 3
- Kelas 2 (`kelas2_year`): target = 8
- Kelas 3 (`kelas3_year`): target = 13
- Tidak ada kelas: target = 0

#### 4. **juziyah**
Riwayat ujian juziyah santri (descending/terbaru dulu).

```json
[
  {
    "tanggal": "2023-12-01 12:23:00",
    "juz": 3,
    "kesalahan": 5
  },
  {
    "tanggal": "2023-11-01 12:23:00",
    "juz": 2,
    "kesalahan": 3
  }
]
```

#### 5. **syahadah**
Riwayat syahadah santri (descending/terbaru dulu).

```json
[
  {
    "tanggal": "2023-12-01 12:23:00",
    "tingkatan": "kedua",
    "kesalahan": 5
  },
  {
    "tanggal": "2023-11-01 12:23:00",
    "tingkatan": "pertama",
    "kesalahan": 3
  }
]
```

#### 6. **10LogTerakhir**
10 aktivitas terakhir santri (campuran semua type, descending).

```json
[
  {
    "tipe": "Ziyadah",
    "tanggal": "2023-12-01 12:23:00",
    "juz": 3,
    "halaman": "1A",
    "kesalahan": 1
  },
  {
    "tipe": "Syahadah",
    "tanggal": "2023-12-01 12:23:00",
    "tingkatan": "pertama",
    "kesalahan": 5
  },
  {
    "tipe": "Juziyah",
    "tanggal": "2023-12-01 12:23:00",
    "juz": 3,
    "kesalahan": 5
  }
]
```

**Tipe yang mungkin:**
- `Ziyadah`: Hafalan baru
- `Juziyah`: Ujian juz
- `Syahadah`: Sertifikasi hafalan
- `Setengah juz`: Pencapaian setengah juz

#### 7. **kecepatan**
Analisis kecepatan santri dalam menambah hafalan (dalam hari).

```json
{
  "ziyadah": 1,      // Rata-rata hari per halaman ziyadah
  "juziyah": 34,     // Rata-rata hari per juziyah
  "syahadah": 0      // Rata-rata hari per syahadah
}
```

**Logika:**
- **Kecepatan dihitung berdasarkan selisih waktu antara record saat ini dengan record sebelumnya (tipe apapun)**
  - `ziyadah`: Selisih waktu antara record ziyadah saat ini dengan record pencapaian sebelumnya (bisa ziyadah, setengah juz, juziyah, atau syahadah)
  - `juziyah`: Selisih waktu antara record juziyah saat ini dengan record pencapaian sebelumnya
  - `syahadah`: Selisih waktu antara record syahadah saat ini dengan record pencapaian sebelumnya
- **Memerlukan minimal 2 record** untuk menghitung kecepatan. Jika hanya ada 1 atau 0 record, nilai akan `0`
- `ziyadah: 1` berarti setiap 1 hari ada pencapaian baru (hampir setiap hari)
- `ziyadah: 4` berarti setiap 4 hari ada pencapaian baru
- `juziyah: 34` berarti setiap 34 hari ada ujian juz
- `ziyadah: 0` atau `juziyah: 0` atau `syahadah: 0` berarti data belum cukup (kurang dari 2 record) untuk menghitung pola

#### 8. **prediksi**
Prediksi hari kalender (bukan hari aktif) yang dibutuhkan untuk menyelesaikan target hafalan.

```json
{
  "15Juz": 0,      // Sudah tercapai
  "30Juz": 808,    // 808 hari kalender untuk menyelesaikan 30 juz
  "catatan": null,  // Penjelasan jika data belum cukup
  "asumsi": "Perhitungan sudah memperhitungkan hari Ahad dan libur sekolah (2 bulan/tahun)"
}
```

**Logika:**
- **Memerlukan minimal 2 record ziyadah** untuk menghitung prediksi. Jika hanya ada 1 atau 0 record, nilai akan `null`
- **Sistem berbasis sekuens juz**: [30, 29, 1, 2, 3, 4, ..., 28]
  - **Target 15 Juz** = Posisi 15 dalam sekuens (mencapai juz 1-13, 29, 30)
  - **Target 30 Juz** = Posisi 30 dalam sekuens (mencapai semua juz 1-30)
- Jika santri **sudah mencapai atau melewati posisi target**, nilai akan `0` (sudah tercapai)
- **Rumus perhitungan**:
  1. Hitung juz yang tersisa: `remainingJuz = targetPosition - currentPosition`
  2. Hitung hari per juz: `daysPerJuz = 20 halaman × ziyadahSpeed`
  3. Hitung hari aktif: `activeDays = remainingJuz × daysPerJuz`
  4. Konversi ke hari kalender: `calendarDays = activeDays / 0.693`
- Setiap juz terdiri dari **20 halaman** (1A-10B = 20 halaman per juz)
- **Faktor penyesuaian hari tidak aktif:**
  - Hari Ahad: 52 hari per tahun (setiap minggu)
  - Libur sekolah: 60 hari per tahun (2 bulan)
  - Total hari tidak aktif: 112 hari per tahun
  - Rasio hari aktif: 253/365 ≈ 69.3%
  - **Rumus**: `hari_kalender = hari_aktif / 0.693`
- `0` berarti sudah mencapai target tersebut
- `null` berarti data belum cukup untuk prediksi yang akurat
- Field `catatan` berisi penjelasan jika data belum cukup
- Field `asumsi` berisi penjelasan bahwa perhitungan sudah memperhitungkan Ahad dan libur sekolah

**Contoh ketika data belum cukup:**
```json
{
  "15Juz": null,
  "30Juz": null,
  "catatan": "Data belum cukup untuk prediksi. Minimal 2 record ziyadah diperlukan.",
  "asumsi": null
}
```

**Contoh ketika target sudah tercapai:**
```json
{
  "15Juz": 0,      // Sudah tercapai (siswa sudah di posisi 16+)
  "30Juz": 808,    // Masih perlu 808 hari kalender lagi (≈2.2 tahun)
  "catatan": null,
  "asumsi": "Perhitungan sudah memperhitungkan hari Ahad dan libur sekolah (2 bulan/tahun)"
}
```

**Catatan Penting:**
Prediksi ini menunjukkan **hari kalender**, bukan hanya hari aktif belajar. Misalnya, 808 hari kalender dengan kecepatan 2 hari per halaman (40 hari per juz) berarti santri butuh sekitar 2.2 tahun untuk menyelesaikan 14 juz tersisa (dengan memperhitungkan Ahad dan libur sekolah). Perhitungan ini berdasarkan kecepatan aktual santri dalam menyelesaikan halaman ziyadah.

#### 9. **dataTambahan**
Data tambahan untuk analisis lebih mendalam.

```json
{
  "totalPencapaian": 28,              // Total semua pencapaian
  "totalTes": 5,                       // Total tes yang sudah diikuti
  "rataRataKesalahan": 3.07,           // Rata-rata kesalahan per pencapaian
  "aktivitasPertama": "2026-01-18...", // Tanggal aktivitas pertama
  "aktivitasTerakhir": "2026-04-02...",// Tanggal aktivitas terakhir
  "hariBelajar": 77,                   // Jumlah hari sejak aktivitas pertama
  "musyrif": ["Ustadzah Marwa"],       // List nama musyrif yang membimbing
  "laporanSabtu": 3                    // Jumlah laporan sabtu yang ada
}
```

#### 10. **rekomendasi**
Rekomendasi personal untuk wali santri berdasarkan data lengkap santri, khusus untuk konteks pesantren.

```json
{
  "rekomendasi": "Masya Allah, Suhail hafalannya sangat cepat! Sebagai anak laki-laki, dia punya potensi jadi hafidz yang hebat. Dorong dia untuk nanti bisa mengajari adik-adik di pesantren."
}
```

**Logika:**
- **Sistem rekomendasi dinamis** yang menghasilkan satu rekomendasi unik untuk setiap santri
- **Dipilih dari pool 65+ rekomendasi** berdasarkan kondisi spesifik santri
- **Jenis kelamin dipertimbangkan** untuk rekomendasi yang lebih personal dan sesuai:
  - **Laki-laki**: Fokus pada olahraga, role model pria sholeh, hadiah praktis (koko, sarung), komunikasi langsung
  - **Perempuan**: Fokus pada skincare/mukena, role model wanita sholehah, hadiah fashion (jilbab), komunikasi emosional

- **Fokus pada konteks pesantren:**
  - **Saat penelponan**: Apa yang diucapkan, ditanyakan, dan dihindari saat menelepon santri
  - **Saat kunjungan bulanan**: Apa yang dibawa, dilakukan, dan dibicarakan
  - **Saat kunjungan Selasa malam (kajian)**: Aktivitas khusus seperti sholat bersama, bicara dengan musyrif
  - **Dukungan praktis**: Makanan bergizi, buku, Al-Quran, perlengkapan belajar
  - **Dukungan emosional**: Motivasi, pelukan, kata-kata penyemangat
  - **Komunikasi dengan musyrif**: Pertanyaan yang perlu diajukan
  
- **Faktor yang dipertimbangkan:**
  - **Jenis kelamin** (laki-laki vs perempuan) - rekomendasi berbeda
  - Kecepatan ziyadah (fast: 1-2 hari, moderate: 3-5 hari, slow: 6+ hari)
  - Jumlah juz yang dicapai (milestones: 5, 10, 15, 20, 25+ juz)
  - Jumlah juz yang lancar vs tidak lancar
  - Kecepatan juziyah dan syahadah
  - Rata-rata kesalahan (high: >5, medium: 3-5, low: <2)
  - Prediksi hari ke 15 juz dan 30 juz
  - Durasi belajar (new: <30 hari, adapting: 30-180 hari, established: 180-365 hari, veteran: 365+ hari)
  - Target kelas (3, 8, atau 13 juz)
  - Status ujian juziyah dan syahadah

- **Rekomendasi bersifat personal** menggunakan nama panggilan santri dan jenis kelamin
- **TIDAK mencakup:** Mengikuti lomba tahfidz (santri fokus pada hafalan, bukan kompetisi)
- **Setelah data santri berubah, rekomendasi juga berubah** karena hash signature berubah

**Contoh Rekomendasi Berdasarkan Jenis Kelamin & Situasi:**

**Untuk Santri LAKI-LAKI:**

*Fast Progress (1-2 hari/page):*
```
"Masya Allah, Suhail hafalannya sangat cepat! Sebagai anak laki-laki, dia punya potensi jadi hafidz yang hebat. Dorong dia untuk nanti bisa mengajari adik-adik di pesantren."
```

*High Achievement (15+ juz):*
```
"Suhail sudah mencapai 15+ juz. Sebagai anak laki-laki, ini modal besar untuk jadi imam dan pemimpin masa depan. Saat kunjungan, tekankan tanggung jawabnya untuk menjaga dan mengamalkan Al-Quran."
```

*General Male:*
```
"Saat kunjungan, bawakan Suhail olahraga ringan seperti bola atau resistance band. Anak laki-laki butuh aktivitas fisik untuk menjaga stamina hafalan. Ingatkan untuk tidak terlalu banyak main game."
```

```
"Saat menelepon Suhail, hindari bertanya terlalu detail tentang perasaan. Anak laki-laki lebih nyaman dengan pertanyaan langsung seperti 'Hafalan sudah berapa?' atau 'Butuh apa nggak?'"
```

**Untuk Santri PEREMPUAN:**

*Fast Progress (1-2 hari/page):*
```
"Masya Allah, Aiko hafalannya sangat cepat! Sebagai anak perempuan, ini bekal luar biasa untuk jadi ibu yang mendidik generasi penghafal Al-Quran masa depan."
```

*High Achievement (15+ juz):*
```
"Aiko sudah mencapai 15+ juz. Sebagai anak perempuan, ini modal besar untuk jadi ibu yang mendidik anak-anak penghafal Al-Quran. Saat kunjungan, tekankan keutamaan wanita penghafal Al-Quran."
```

*General Female:*
```
"Saat kunjungan, bawakan Aiko skincare halal atau mukena cantik. Anak perempuan senang dengan hadiah yang membuat dia merasa diperhatikan dan cantik."
```

```
"Saat menelepon Aiko, lebih peka terhadap perubahan suaranya. Jika terdengar sedih atau lelah, berikan kata-kata lembut. Anak perempuan lebih sensitif secara emosional."
```

**Saat Penelponan (General):**
```
"Telepon Aiko secara rutin, minimal seminggu sekali. Tanyakan tentang teman sekamar, kegiatan harian, dan makanan di pesantren. Ini menunjukkan Anda peduli pada kebahagiaannya, bukan hanya hafalan."
```

```
"Saat telepon Suhail, hindari pertanyaan yang membuat stres seperti 'Kenapa hafalan lambat?' atau 'Kok belum naik juz?' Ganti dengan 'Ada yang bisa Ayah/Bunda bantu?' atau 'Semangat ya, Nak!'"
```

**Saat Kunjungan Bulanan (General):**
```
"Saat kunjungan bulan depan, bawakan makanan bergizi seperti kurma, madu, susu, atau kacang. Hindari makanan cepat saji. Suhail butuh gizi baik untuk konsentrasi hafalan di pesantren."
```

**Saat Kunjungan Selasa Malam (Kajian):**
```
"Saat kunjungan Selasa malam, luangkan waktu untuk sholat bersama Aiko di masjid pesantren. Ini menunjukkan dukungan spiritual dan memperkuat ikatan. Afterwards, tanya tentang hafalan dengan santai."
```

**Dukungan Emosional:**
```
"Perhatikan aspek emosional Suhail. Saat kunjungan atau telepon, tanyakan tentang perasaan, persahabatan, dan kebahagiaan di pesantren. Anak yang bahagia akan lebih mudah menghafal."
```

```
"Saat kunjungan, peluk Aiko dan katakan 'Ayah/Bunda sayang kamu, bangga sama perjuangan kamu menghafal Al-Quran.' Ini akan membuatnya sangat termotivasi."
```

**Santri Baru (< 30 hari):**
```
"Ifroyim masih baru di pesantren. Saat kunjungan pertama, jangan terlalu banyak tanya hafalan. Tanyakan tentang kenyamanan, teman sekamar, makanan, dan ustadz. Bawakan barang yang dia butuhkan."
```

**Santri dengan Kesalahan Tinggi:**
```
"Kesalahan Siti Sofia cukup tinggi (rata-rata 3.5). Saat kunjungan, belikan buku tajwid praktis dan minta dia praktekkan bacaannya di depan Anda. Ingatkan untuk tadarus dengan teman yang bacaannya bagus."
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Parameter ?nik=[nik] harus diisi"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Santri dengan NIK tersebut tidak ditemukan"
}
```

### 405 Method Not Allowed
```json
{
  "success": false,
  "message": "Method not allowed"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "Terjadi kesalahan: [detail error]"
}
```

## Contoh Penggunaan

### JavaScript (Fetch API)
```javascript
const response = await fetch('http://localhost:4848/santri.php?nik=6472056809110001');
const data = await response.json();

if (data.success) {
  console.log('Nama:', data.santri.nama);
  console.log('Juz lancar:', data.santri.pencapaianJuz.juzYangLancar);
  console.log('Prediksi 30 juz:', data.santri.prediksi['30Juz'], 'hari');
}
```

### PHP
```php
$nik = '6472056809110001';
$url = "http://localhost:4848/santri.php?nik=$nik";
$response = file_get_contents($url);
$data = json_decode($response, true);

if ($data['success']) {
    echo "Nama: " . $data['santri']['nama'];
    echo "Target: Juz " . $data['santri']['targetHafalan'];
}
```

### cURL
```bash
curl "http://localhost:4848/santri.php?nik=6472056809110001"
```

## Catatan Penting

1. **CORS Enabled**: Endpoint ini bisa diakses dari domain manapun
2. **GET Method**: Menggunakan GET (bukan POST) untuk kemudahan akses
3. **Read Only**: Endpoint ini hanya untuk membaca data, tidak mengubah
4. **Timezone**: Semua waktu menggunakan Asia/Makassar (WITA, UTC+8)
5. **Tipe Pencapaian**:
   - `ziyadah`: Hafalan baru per halaman
   - `juziyah`: Ujian juz
   - `syahadah`: Sertifikasi hafalan Al-Quran
   - `setengah_juz`: Pencapaian setengah juz

## Sumber Data

| Data | Table | Field |
|------|-------|-------|
| Info Santri | `santri` | Semua field |
| Pencapaian Juz | `pencapaian` | juz (distinct) |
| Juz Lancar | `tes` | juz (distinct) |
| Juziyah | `pencapaian` | type = 'juziyah' |
| Syahadah | `pencapaian` | type = 'syahadah' |
| Kecepatan | `pencapaian` | Dihitung dari created_at |
| Target | `settings` + `santri.tahun_masuk` | kelas configuration |
| Musyrif | `musyrif` + `musyrfst` | Join table |

## Update & Maintenance

- File: `static/santri.php`
- Database: `static/everynight-in-my-dream.db`
- Library: RedBeanPHP (`static/library/rb-sqlite.php`)
- Functions: `static/functions.php`, `static/functions-settings.php`
