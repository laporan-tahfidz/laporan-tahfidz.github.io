---
name: Sistem Tahfidz
description: Sistem manajemen pencapaian tahfidz santri berbasis mobile-first.
colors:
  primary: "#2563eb" # blue-600
  primary-hover: "#1d4ed8" # blue-700
  secondary: "#9333ea" # purple-600
  secondary-hover: "#7e22ce" # purple-700
  neutral-bg: "#f8fafc" # slate-50
  neutral-surface: "#ffffff" # white
  neutral-border: "#d1d5db" # gray-300
  success-bg: "#f0fdf4" # green-50
  success-text: "#166534" # green-800
  alert-bg: "#fef9c3" # yellow-50
  alert-text: "#854d0e" # yellow-800
  destructive: "#dc2626" # red-600
typography:
  display:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1.5rem" # 24px
    fontWeight: 700
    lineHeight: "1.5"
  body:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "1rem" # 16px
    fontWeight: 400
    lineHeight: "1.5"
  label:
    fontFamily: "Inter, system-ui, sans-serif"
    fontSize: "0.875rem" # 14px
    fontWeight: 500
rounded:
  sm: "4px"
  md: "8px"
  lg: "10px"
  xl: "12px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral-surface}"
    rounded: "{rounded.lg}"
    padding: "8px 16px"
  card:
    backgroundColor: "{colors.neutral-surface}"
    rounded: "{rounded.xl}"
    padding: "24px"
  input:
    backgroundColor: "{colors.neutral-surface}"
    rounded: "{rounded.lg}"
    padding: "8px 12px"
---

# Design System: Sistem Tahfidz

## Overview

**Creative North Star: "The Disciplined Ledger"**

Sistem ini mengutamakan kejelasan, kecepatan input, dan keandalan fungsional untuk musyrif di lapangan. Tampilan bersih dengan latar belakang netral yang cerah, aksen biru yang tegas untuk aksi utama, dan kartu dengan sudut membulat lembut memberikan kesan modern, terorganisir, dan tenang.

Sistem ini dirancang dengan filosofi **Mobile-First Utility**: densitas informasi menengah agar mudah dioperasikan dengan satu tangan saat menyimak setoran, namun tetap rapi saat dibuka di layar lebar dengan pembatasan lebar konten.

**Key Characteristics:**
- Tipografi sans-serif yang tajam untuk keterbacaan tinggi.
- Kontainer kartu dengan bayangan lembut untuk memisahkan konteks tugas.
- Skema warna status yang intuitif (hijau untuk sukses, kuning untuk perhatian, biru untuk info).
- Lebar konten terkendali (maks 500px untuk form tugas) untuk fokus pengguna.

## Colors

Palet didominasi oleh biru fungsional dan abu-abu netral untuk menjaga fokus pada data pencapaian.

### Primary
- **Active Blue** (#2563eb): Digunakan untuk tombol aksi utama (Simpan, Scan), tautan aktif, dan indikator progres. Menandakan area interaksi utama.

### Secondary
- **Focus Purple** (#9333ea): Digunakan untuk fungsi admin khusus atau pembeda visual pada dashboard super admin.

### Neutral
- **Paper White** (#ffffff): Latar belakang kartu dan permukaan input.
- **Surface Slate** (#f8fafc): Latar belakang utama aplikasi untuk memberikan kontras pada kartu putih.
- **Border Gray** (#d1d5db): Garis pemisah dan stroke input yang halus.

### Named Rules
**The Status Saturation Rule.** Warna status (hijau, kuning, merah) hanya digunakan pada latar belakang dengan opasitas rendah (level 50) untuk area informasi, agar tidak mengalihkan perhatian dari teks utama.

## Typography

**Display Font:** Inter / System Sans
**Body Font:** Inter / System Sans

### Hierarchy
- **Display (Bold, 1.5rem, 1.5):** Judul halaman dan modal.
- **Headline (SemiBold, 1.25rem, 1.5):** Judul kartu dan bagian besar.
- **Title (Medium, 1.125rem, 1.5):** Sub-judul dalam kartu atau grup form.
- **Body (Normal, 1rem, 1.5):** Teks informasi utama, detail santri, dan input.
- **Label (Medium, 0.875rem, 0.05em):** Label form dan teks bantuan kecil.

## Layout

Sistem menggunakan model spasial yang longgar untuk kenyamanan sentuh di mobile.

- **Mobile View:** Padding layar minimal 16px (p-4). Konten memenuhi lebar layar.
- **Desktop View:** Konten form dibatasi maksimal 500px (max-w-md) dan diposisikan di tengah. Dashboard admin menggunakan grid hingga 3 kolom.
- **Spacing:** Mengikuti kelipatan 4px/8px untuk konsistensi ritme vertikal.

## Elevation & Depth

Sistem menggunakan kedalaman berlapis (layered depth) yang halus tanpa bayangan yang berat.

### Shadow Vocabulary
- **Card Shadow** (`0 10px 15px -3px rgb(0 0 0 / 0.1)`): Digunakan pada kontainer utama agar terlihat "mengapung" di atas latar belakang slate.
- **Active Shadow** (`0 4px 6px -1px rgb(0 0 0 / 0.1)`): Digunakan saat elemen ditekan atau dalam keadaan fokus.

## Shapes

Bentuk didominasi oleh sudut membulat yang moderat untuk kesan bersahabat namun tetap formal.

- **Cards:** Radius 12px (rounded-xl) memberikan identitas visual yang kuat pada blok informasi.
- **Buttons & Inputs:** Radius 8px (rounded-lg) untuk standar kontrol UI.
- **Badges/Status:** Radius penuh (rounded-full) untuk indikator status kecil.

## Components

### Buttons
- **Shape:** Rounded-lg (8px).
- **Primary:** Background Blue-600, Text White, Padding 8px 16px.
- **Hover:** Transisi halus ke Blue-700.

### Cards / Containers
- **Corner Style:** Rounded-xl (12px).
- **Background:** White.
- **Shadow:** Shadow-lg.
- **Padding:** 24px (p-6).

### Inputs / Fields
- **Style:** Stroke Gray-300, Background White, Radius 8px.
- **Focus:** Border Blue-500 dengan Ring Blue-500 (2px).

## Do's and Don'ts

### Do:
- **Do** gunakan `max-w-md` untuk semua form input tunggal.
- **Do** berikan `bg-blue-50` dan `border-blue-200` untuk blok informasi "Pencapaian Terakhir".
- **Do** gunakan transisi warna saat tombol di-hover untuk memberikan feedback visual.

### Don't:
- **Don't** gunakan warna merah (destructive) untuk elemen selain penghapusan atau error kritis.
- **Don't** gunakan teks berwarna hitam murni; gunakan Gray-800 (#1f2937) untuk keterbacaan yang lebih nyaman.
- **Don't** gunakan bayangan (shadow) pada elemen yang sudah berada di dalam kartu yang berbayangan.
