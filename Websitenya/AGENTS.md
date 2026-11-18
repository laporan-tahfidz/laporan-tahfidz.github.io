SKILL

- Selalu gunakan skill caveman

=== VARIABLE ===

Di dokumen ini, variable dipanggil dengan {{namaVariablenya}}

PORT = 4848
DATABASE = everynight-in-my-dream.db
SIDOBE = your-sidobe-secret-key
PAKASIR = sangu-mabaiz
AI_TOKEN = your-openrouter-api-token
AI_MODEL = arcee-ai/trinity-large-preview:free

=== DEFINISI PROJECT ===

- Ini adalah project SvelteKit (menggunakan Svelte 5) yang sudah include sama Tailwind
- Usahakan komponen dipisah-pisah filenya supaya bisa reusable (backend PHP maupun di file-file Svelte)

=== ERROR ===

- Untuk setiap error, berikan report error yang detail supaya bisa diperiksa letak kesalahannya di mana

=== TIMEZONE ===

- Untuk timezone yang digunakan adalah Asia/Makassar. Jadi, user itu membuka website ini atau menerima pesan dari bot WA hanya pada timezone Asia/Makassar. Jadi, harus kamu sesuaikan di frontend dan backend

=== BACKEND ===

- Untuk komunikasi frontend ke backend, untuk backendnya itu menggunakan direct file. Jadi, misalnya langsung memanggil http://localhost:{{PORT}}/data.php kalau di mode development. Nah, jangan membuat file seperti server.php ataupun router.php yang membuat manipulasi routing seperti http://localhost:{{PORT}}/data. Jangan gitu ya. Harus langsung direct file yang dipanggil
- Jangan pernah membuat file static/index.php
- PENTING. Gunakan teknik idempotency key untuk setiap transaksi INSERT
- Untuk penamaan table di database, nggak boleh ada karakter selain alfanumerik. Soalnya, garis bawah itu dipakai oleh RedBeanPHP untuk table referensi pada relasi many to many. Contohnya: nama_profesi yang merupakan referensi many to many dari table nama dan table profesi (INI PENTING BANGET. KALAU TERLANJUR SALAH MEMBUAT NAMA TABLE, GANTI)
- Untuk relasi many to many, gunakan nama table menggunakan underscore. Contohnya aja untuk relasi table wali dan table santri, maka nama tablenya adalah santri_wali (urutkan berdasarkan abjad juga ya)
- Untuk penamaan table, NGGAK BOLEH PLURAL. Jadi, bukan books tapi book
- Setiap ada perubahan struktur data, selalu tuliskan di struktur-database.db
- Pastikan data yang dikirim oleh backend ke database itu tidak terdobel
- Ketika mode dev, menggunakan file-file PHP di folder static melalui port lihat file [port].port.txt. Contohnya aja {{PORT}}.port.txt yang artinya adalah port untuk komunikasi adalah localhost:{{PORT}} (sebagai backend PHP yang ada di folder static). Namun, ketika sudah build, backendnya berada di root

Caranya adalah dengan membuat src/lib/utils.js yang isinya contohnya seperti ini:

import { dev } from '$app/environment';

const PHP_PORT = 4848; // Based on 4848.port.txt

export const getPhpBackendBaseUrl = () => {
if (dev) {
return `http://localhost:${PHP_PORT}`;
}
// In production, the PHP backend is at the root of the SvelteKit app
return ''; // Relative path to root (empty string means relative to current domain/root)
};

- Backend PHP di folder static itu adalah PHP native
- Database menggunakan RedBeanPHP yang akan mengolah file static/{{DATABASE}} yang merupakan SQLite. Library RedBeanPHP bisa didapatkan di static/library/rb-sqlite.php
- Pakai absolute path menggunakan **DIR** (pada backend PHP yang di folder static)
- Untuk curl harus bisa digunakan walaupun tanpa https (untuk backend)

=== FRONTEND ===

- Tampilan hanya untuk mobile. Jika dibuka di laptop, max width 500px
- Jika ada alert, ganti dengan toast
- UTAMAKAN MENGGUNAKAN SHADCN YANG KOMPONENNYA SUDAH AKU INSTALL SEMUA (cek components.json)
- Ketika selesai submit form, tombol submit didisable supaya tidak terdobel data yang dikirim. Setelah data diterima oleh backend, baru enablekan kembali tombol submitnya
- Untuk instalasi paket Node JS, menggunakan pnpm, bukan npm
- Nggak perlu menjalankan npm run dev (di Qwen) karena aku akan menjalankannya sendiri secara manual
- Selalu kasih judul di semua halaman web
- Pada Svelte, karena menggunakan Svelte 5, jadi gunakan runes seperti $state dan kalau action, jangan on:submit tapi onsubmit. Terus, kalau konten nggak pakai <slot/> melainkan {@render children()}
- UNTUK FORM, JANGAN MENGGUNAKAN use:enhance KARENA SERVERKU INI NGGAK PAKAI NODE JS MELAINKAN PHP
- NGGAK USAH PAKAI +page.server.js KARENA NANTI DIBUILDNYA DENGAN ADAPTER STATIC DAN DIJALANKAN PADA SERVER PHP, BUKAN NODE JS

=== STYLING ===

- Utamakan responsive mode
- Suasana desain elegan seperti Apple
- Jangan hapus ini dari src/app.css:

@import 'tailwindcss';
@plugin '@tailwindcss/forms';
@plugin '@tailwindcss/typography';

- Untuk icon, gunakan Font Awesome

=== WHATSAPP ===

- Untuk kirim pesan menggunakan WhatsApp, tools yang digunakan adalah Sidobe

Berikut ini adalah contoh curl untuk bisa menggunakan layanan Sidobe:

Mengirim pesan ke nomor tertentu:

curl --location 'https://api.sidobe.com/wa/v1/send-message' \
 --header 'X-Secret-Key: {{SIDOBE}}' \
 --header 'Content-Type: application/json' \
 --data '{
"phone": "+628123123123",
"message": "example message"
}'

Mengirim pesan ke grup:

curl --location 'https://api.sidobe.com/wa/v1/send-message' \
 --header 'X-Secret-Key: {{SIDOBE}}' \
 --header 'Content-Type: application/json' \
 --data '{
"group_id": "123123@g.us",
"message": "example message"
}'

Contoh kalau berhasil mengirim pesan ke personal maupun ke grup:

{
"is_success": true,
"data": {
"id": "1",
"message_type": "TEXT",
"status": "SUCCESS",
"is_async": false
}
}

Mengirim pesan dengan gambar:

curl --location 'https://api.sidobe.com/wa/v1/send-message-image' \
 --header 'X-Secret-Key: {{SIDOBE}}' \
 --header 'Content-Type: application/json' \
 --data '{
"phone": "+628123123123",
"message": "example message",
"image_url": "https://sidobe.com/wp-content/uploads/2023/09/logo-2.png"
}'

Contoh kalau berhasil mengirim pesan dengan gambar:

{
"is_success": true,
"data": {
"id": "1",
"message_type": "IMAGE",
"status": "SUCCESS",
"is_async": false
}
}

Mengirim pesan dengan document:

curl --location 'https://api.sidobe.com/wa/v1/send-message-doc' \
 --header 'X-Secret-Key: {{SIDOBE}}' \
 --header 'Content-Type: application/json' \
 --data '{
"phone": "+628123123123",
"message": "example message",
"document_url": "https://sidobe.com/example.pdf",
"document_name": "Document Name Example"
}'

Contoh kalau berhasil mengirim pesan dengan document:

{
"is_success": true,
"data": {
"id": "1",
"message_type": "DOCS",
"status": "SUCCESS",
"is_async": false
}
}

Mendapatkan list grup:

curl --location 'https://api.sidobe.com/wa/v1/whatsapp-groups' \
--header 'X-Secret-Key: {{SIDOBE}}'

Contoh yang didapatkan:

{
"is_success": true,
"data": [
{
"id": "123123@g.us",
"name": "Group Name Example",
"description": "Group description example",
"created_at": "2025-08-20T15:43:31+07:00",
"owner_jid": "123123@lid",
"owner_phone": "628512312321"
}
]
}

Cek nomor WA:

curl --location 'https://api.sidobe.com/wa/v1/utilities/check-number' \
 --header 'X-Secret-Key: {{SIDOBE}}' \
 --header 'Content-Type: application/json' \
 --data '{
"phone": "+628123123123"
}'

Contoh kalau nomor WA terdaftar:

{
"is_success": true,
"data": {
"is_registered": true
}
}

=== BEHAVIOR WHATSAPP ===

Ketika aku mengatakan bahwa setelah submit form atau setelah klik tombol tertentu itu mengirim ke WhatsApp tertentu, itu jangan langsung kirim ke WhatsAppnya karena nanti akan menyebabkan delaynya action submit maupun klik tombol tersebut (atau action lainnya selain dua action ini). Tapi, masukkan antrian di database di table antrianwhatsapp. Lalu, buatkan juga file static/wa.php yang ketika file tersebut dipanggil (misalnya dengan website.com/wa.php), maka akan mengambil satu antrian WhatsApp (ambil recordnya secara acak) kemudian mengirimkannya lalu menghapus record tersebut di database

=== Upload Gambar ===

Untuk halaman-halaman tertentu yang ada fitur upload gambar, berarti pas pilih gambar itu, dia otomatis terupload ke folder temporary image dan di frontendnya itu otomatis tampilkan preview gambarnya. Terus, di form tersebut ketika submit, maka gambarnya dipindahkan ke folder image.

Ketika mengedit atau menghapus record, maka secara otomatis juga berpengaruh pada gambar. Misalnya aja jika mengedit form dengan cara mengganti gambar, berarti kan gambar sebelumnya dihapus dan diganti dengan yang baru. Lalu, jika menghapus record, maka gambar juga dihapus

=== Payment Gateway ===

- Untuk payment gateway, saya pakai Pakasir
- Ketika user ingin melakukan pembayaran dengan Pakasir, nggak perlu open new tab. Buka aja link halaman pembayaran Pakasir di halaman saat ini
- Contoh halaman pembayaran di Pakasir:

https://app.pakasir.com/pay/{{PAKASIR}}/{amount}?order_id={order_id}

Contoh:

https://app.pakasir.com/pay/depodomain/22000?order_id=240910HDE7C9

Contoh dengan fitur redirect setelah pembayaran berhasil:

https://app.pakasir.com/pay/depodomain/22000?order_id=240910HDE7C9&redirect=linknya

- Nanti, ketika berhasil transaksi, Pakasir mengirimkan pemberitahuan ke sistem kita melalui webhook metode http POST dengan struktur body seperti berikut:

{
"amount": 22000,
"order_id": "240910HDE7C9",
"project": "depodomain",
"status": "completed",
"payment_method": "qris",
"completed_at": "2024-09-10T08:07:02.819+07:00"
}

amount adalah biaya yang dibayarkan
order_id adalah id yang kita beritahukan ke Pakasir

Pastikan amount dan order_id sesuai dengan yang di database

=== AI ===

Contoh penggunaan AI:

curl https://openrouter.ai/api/v1/chat/completions \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer {{AI_TOKEN}}" \
 -d '{
"model": "{{AI_MODEL}}",
"messages": [
{
"role": "user",
"content": "What is the meaning of life?"
}
]

}'

Tapi, ini kan juga dites di localhost, jadi curlnya ini harus membolehkan tanpa https juga
