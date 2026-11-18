# Panduan Agen AI & Spesifikasi Repositori (AGENTS.md)

Dokumen ini memuat aturan baku, standar teknis, dan konvensi pengembangan yang **wajib dipatuhi oleh setiap Agen AI** yang bekerja pada repositori ini.

---

## 1. Aturan Wajib: Cache Busting dengan Hash ULID

> **ATURAN MUTLAK**:
> Setiap kali AI mengolah, membuat, atau memperbarui file **JavaScript (.js)** maupun **CSS (.css)**, di file **HTML** yang memanggil file-file tersebut, **WAJIB** menggunakan query parameter berupa **hash ULID** (*Universally Unique Lexicographically Sortable Identifier*).

### Contoh Pemanggilan
```html
<!-- Pemanggilan stylesheet CSS dengan hash ULID -->
<link rel="stylesheet" href="style.css?01M7PG92011DTMR1FNKXQQKQKA">

<!-- Pemanggilan file JavaScript aplikasi dengan hash ULID -->
<script src="app.js?01M7PG92015YWWVVYDJVWGSTYY"></script>
```

### Spesifikasi Teknis ULID
- **Panjang**: Tepat 26 karakter alfanumerik.
- **Encoding**: Crockford's Base32 (`0123456789ABCDEFGHJKMNPQRSTVWXYZ`), tidak memakai karakter ambigu `I`, `L`, `O`, dan `U`.
- **Komposisi**:
  - **10 karakter pertama (48 bit)**: UNIX epoch timestamp dalam milidetik (membuatnya berurutan secara waktu / *lexicographically sortable*).
  - **16 karakter terakhir (80 bit)**: Entropi acak kriptografis (*cryptographically secure randomness*).
- **Karakteristik**: Menghindari stale cache pada browser pengguna saat aset web diperbarui, sekaligus memungkinkan pelacakan versi file secara kronologis.

### Implementasi Generator ULID

#### Dalam Python (`build_index_html.py` atau script generator lainnya)
```python
import os
import time

CROCKFORD_BASE32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

def generate_ulid(timestamp_ms=None):
    """Menghasilkan 26 karakter standar Crockford Base32 ULID."""
    if timestamp_ms is None:
        timestamp_ms = int(time.time() * 1000)
    
    # 48-bit timestamp -> 10 karakter Base32
    time_chars = [''] * 10
    t = timestamp_ms
    for i in range(9, -1, -1):
        time_chars[i] = CROCKFORD_BASE32[t & 0x1F]
        t >>= 5
        
    # 80-bit secure randomness -> 16 karakter Base32
    rand_bytes = os.urandom(10)
    rand_val = int.from_bytes(rand_bytes, byteorder='big')
    rand_chars = [''] * 16
    for i in range(15, -1, -1):
        rand_chars[i] = CROCKFORD_BASE32[rand_val & 0x1F]
        rand_val >>= 5
        
    return ''.join(time_chars) + ''.join(rand_chars)
```

#### Dalam JavaScript / Node.js
```javascript
const CROCKFORD_BASE32 = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';

function generateULID(timestampMs = Date.now()) {
  let timeChars = '';
  let t = timestampMs;
  for (let i = 9; i >= 0; i--) {
    timeChars = CROCKFORD_BASE32[t % 32] + timeChars;
    t = Math.floor(t / 32);
  }

  let randChars = '';
  const cryptoObj = typeof crypto !== 'undefined' ? crypto : require('crypto');
  const bytes = typeof cryptoObj.getRandomValues === 'function'
    ? cryptoObj.getRandomValues(new Uint8Array(10))
    : cryptoObj.randomBytes(10);

  let randVal = BigInt(0);
  for (let i = 0; i < 10; i++) {
    randVal = (randVal << BigInt(8)) | BigInt(bytes[i]);
  }
  for (let i = 0; i < 16; i++) {
    const rem = Number(randVal & BigInt(0x1F));
    randChars = CROCKFORD_BASE32[rem] + randChars;
    randVal >>= BigInt(5);
  }

  return timeChars + randChars;
}
```

---

## 2. Aturan Bisnis & Batasan Data Proyek

1. **Skop Santri (Kelas 1, 2, & 3 Saja)**:
   - Data yang diproses dan ditampilkan **hanya untuk santri aktif/terdaftar di Kelas 1, 2, dan 3** (total 44 santri: 11 Kelas 1, 16 Kelas 2, 17 Kelas 3).
   - Alumni dan jenjang kelas lainnya **dilarang disertakan**.
2. **Pengecualian Evaluasi Sabtu**:
   - Data evaluasi Sabtu (`laporansabtu`) **dikecualikan** dari perhitungan mutqin, ziyadah, dan capaian harian santri.
3. **Format Tanggal Bahasa Indonesia Baku**:
   - Seluruh penanggalan yang ditampilkan ke pengguna harus diformat ke Bahasa Indonesia lengkap:
     - Pola: `Hari, DD Bulan YYYY` (Contoh: `Selasa, 30 Januari 2024`).
     - Tidak boleh menampilkan format mentah seperti `2026-05-17` pada antarmuka pengguna.
4. **Tema Tampilan Wajib Terang (Strict Light Mode)**:
   - Antarmuka dashboard dirancang dengan nuansa profesional, bersih, dan hangat (*emerald/teal palette* dengan latar belakang `bg-slate-50` / `bg-white`).
   - **DILARANG mengaktifkan atau menambahkan Dark Mode**.
5. **Optimasi Khusus Layar Smartphone (Mobile-First HP)**:
   - Antarmuka harus sangat nyaman digunakan lewat HP/smartphone:
     - Tap target minimal 44px untuk elemen interaktif.
     - Horizontal card scrolling untuk ringkasan cepat.
     - Sticky top bar ringkas dan date picker responsif.
     - Modal detail santri responsif dengan grid 30 juz yang mudah disentuh di layar sentuh.
6. **Filter Rentang Waktu Dinamis**:
   - Pengguna dapat memilih tanggal awal (`Start Date`) dan tanggal akhir (`End Date`) atau menggunakan preset (*Semua*, *Semester Ini*, *3 Bulan Terakhir*, *Bulan Ini*, *Hari Ini*).
   - Seluruh kartu metrik, chart, dan tabel data santri akan menghitung ulang jumlah setoran, juz yang dicapai, dan aktivitas dalam rentang waktu yang dipilih secara instan.

---

## 3. Struktur & Alur Kerja File

- `everynight-in-my-dream.db`: Database SQLite sumber utama laporan.
- `process_classes_123.py`: Script ekstraksi dan normalisasi data dari SQLite ke format JSON dataset lengkap (`full_report_dataset.json`).
- `full_report_dataset.json`: Snapshot data yang memuat metadata, agregat kelas, halaqah, statistik juz, dan profil 44 santri.
- `style.css`: File styling kustom (scrollbar, cetak, badge) yang di-link di `index.html` dengan hash ULID.
- `app.js`: File logika interaktif frontend (filter tanggal, kalkulasi metrik, inisialisasi Chart.js, modal santri, export CSV). Di-link di `index.html` dengan hash ULID.
- `build_index_html.py`: Script otomasi build yang:
  1. Menghasilkan hash ULID baru untuk CSS dan JS.
  2. Menyematkan payload data ke `<script id="embedded-data" type="application/json">`.
  3. Memperbarui link `style.css?<ulid>` dan `app.js?<ulid>` di `index.html`.
- `index.html`: File HTML dashboard mandiri yang dapat dibuka langsung secara offline via file browser maupun di-host via server web (GitHub Pages/Vercel/dll).

---

## 4. Prosedur Saat Mengubah Kode

Setiap kali Anda (Agen AI) melakukan perubahan pada `app.js` atau `style.css`:
1. Uji sintaks JavaScript terlebih dahulu:
   ```bash
   node -c app.js
   ```
2. Jalankan script build untuk memperbarui hash ULID dan meregenerasi `index.html`:
   ```bash
   python build_index_html.py
   ```
3. Pastikan `index.html` telah memanggil file terkait dengan query ULID terbaru:
   ```html
   <link rel="stylesheet" href="style.css?01...">
   <script src="app.js?01..."></script>
   ```
4. Commit dan push perubahan ke repositori remote Git jika diminta:
   ```bash
   git add AGENTS.md app.js style.css build_index_html.py index.html
   git commit -m "feat/fix: deskripsi perubahan"
   git push origin main
   ```
