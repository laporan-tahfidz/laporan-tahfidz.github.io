# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

SvelteKit (Svelte 5, adapter-static, fallback 404.html) + Tailwind CSS v4 + shadcn-svelte UI components. Backend: PHP native di folder `static/` + SQLite via RedBeanPHP. Mobile-first (maks. width 500px di desktop). Build mode dev: PHP di localhost:4848; build: backend di root. [Dikonfirmasi: "sebagaimana yang sudah ada aja" = lanjutkan stack incumbent.]

## Users

- **Musyrif / musyrifah** (primary): pengampu tahfidz santri. Pekerjaan utama: menyimak setoran hafalan santri.
- Santri: subjek pencatatan, akses data sendiri (StudentSidebar ada).
- Koordinator tahfidz: memantau santri yang perlu perhatian khusus.

## Product Purpose

Sistem pencatatan pencapaian tahfidz santri (ziyadah, setengah juz, juziyah, syahadah) untuk pesantren. Sukses berarti setiap setoran hafalan tercatat benar, tidak ganda, dan santri yang butuh perhatian terpantau tepat waktu (laporan Sabtu, pengingat WhatsApp).

## Positioning

Pencatatan tahfidz terikat alur nyata penyimakan: setiap pencapaian punya aturan hitung target (0.5 halaman/hari dari Senin), logika "perlu perhatian" terstruktur per peran (musyrif vs koordinator, ambang hari berbeda), dan nilai syahadah/juziyah mengikuti skala mutu pesantren (Mumtaz..Mardud).

## Operating Context

- Timezone **Asia/Makassar** — berlaku di frontend dan backend.
- Akses via HP (mobile-first); notifikasi & laporan via grup WhatsApp.
- Santri masuk dari sistem eksternal (API SANTRI, mapping NIK).
- Syahadah/juziyah bisa masuk via **webhook** eksternal (id_guru, nik_santri, nilai).

## Capabilities and Constraints

- Tabel DB: idempotency, otp, token, santri, musyrif, musyrfst (relasi many-to-many), pencapaian, tes, settings, laporansabtu, webhooksyahadah, webhookjuziyah. Nama tabel tanpa plural; relasi many-to-many pakai underscore urut abjad. [Evidence: `struktur-database.txt`, `struktur-database.db`]
- Idempotency key wajib tiap INSERT.
- Anggota santri-musyrif direlasikan lewat tabel **musyrfst** (catatan: nama jenisnya tak konsisten konvensi underscore — pertahankan demi data yang sudah ada).
- Login via OTP + token (tabel otp, token; OtpVerificationModal).
- Integrasi: Sidobe (WA), Pakasir (payment), OpenRouter AI (undian? belum jelas), cron `perhatian.php` ke grup WA.
- Upload gambar: alur temp → image; hapus/ganti gambar ikut hapus record. [Ada folder image/temp? belum diverifikasi]
- Redirect pakasir tanpa new tab. Webhook pakasir: amount + order_id dicek ke DB.
- Tidak ada API eksplisit "halaman apa yang harus diverifikasi" — target 0.5 hlm/hari & ambang hari sudah terdokumentasi di logika perhatian.

## Brand Commitments

[Tidak ada identitas brand/logo/nama resmi yang dinyatakan user. Jangan mengarang nama, tagline, atau klaim.]

## Evidence on Hand

- `struktur-database.txt` / `.db` — skema & logika perhatian terdokumentasi.
- `API-SANTRI-DOCUMENTATION.md` — sumber data santri eksternal.
- `list-grup-wa.txt`, `murajaah.txt`, `nomor-halaman.txt`, `quran-page-split-30juz.json` — data operasional nyata.
- `src/lib/components/` — komponen bento perhatian (CoordinatorAttentionBento, MusyrifAttentionBento, dll) membuktikan dashboard pemantauan pernah dibangun.
- Tidak ada screenshot/golden visual tersimpan. Tidak ada testimoni/press.

## Product Principles

1. Data setoran harus akurat, tidak dobel, dan bisa dilacak (idempotency + audit timestamp).
2. Semua waktu dihitung Asia/Makassar tanpa pengecualian.
3. Aturan penilaian & ambang perhatian pesantren adalah truth, bukan tafsir aplikasi.
4. Pencatatan cepat dari HP, sisanya otomatis (WA/cron) di belakang.
5. Santri tetap bisa melihat progres/riwayatnya sendiri.

## Accessibility & Inclusion

[Belum ada kebutuhan aksesibilitas spesifik yang dinyatakan. Mobile-first sudah dipaksa oleh konteks penggunaan.]