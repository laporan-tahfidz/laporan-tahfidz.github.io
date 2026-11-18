const fs = require("fs");

const TOTAL_JUZ = 30;

const pageLabels = [];
for (let i = 1; i <= 10; i++) {
  pageLabels.push(`${i}A`);
  pageLabels.push(`${i}B`);
}

// Mapping dari juz + page_label ke ayat terakhir di halaman tersebut
// Berdasarkan perintah.txt yang sudah disesuaikan
const pageEndings = {
//   1: {
//     "1A": { surah: 2, ayah: 5 },
//     "1B": { surah: 2, ayah: 16 },
//     "2A": { surah: 2, ayah: 24 },
//     "2B": { surah: 2, ayah: 29 },
//     "3A": { surah: 2, ayah: 37 },
//     "3B": { surah: 2, ayah: 48 },
//     "4A": { surah: 2, ayah: 57 },
//     // Tambahkan halaman lainnya sesuai kebutuhan
//     // "4B": { surah: 2, ayah: XX },
//     // "5A": { surah: 2, ayah: XX },
//     // ... dan seterusnya
//   }
//   // Juz lainnya akan di-generate otomatis
};

async function fetchAllAyahs() {
  const axios = require("axios");
  const res = await axios.get("https://api.alquran.cloud/v1/quran/quran-uthmani");
  return res.data.data.surahs.flatMap(surah =>
    surah.ayahs.map(ayah => ({
      surah_number: surah.number,
      surah_name: surah.englishName,
      ayah: ayah.numberInSurah,
      juz: ayah.juz,
      globalIndex: ayah.number
    }))
  );
}

function getSurahName(surahNumber, allAyahs) {
  const surah = allAyahs.find(a => a.surah_number === surahNumber);
  return surah ? surah.surah_name : "";
}

function splitJuzIntoSlots(ayahs) {
  const result = [];

  for (let juz = 1; juz <= TOTAL_JUZ; juz++) {
    const juzAyahs = ayahs.filter(a => a.juz === juz);
    const hasMapping = pageEndings[juz];
    const totalPages = pageLabels.length;

    for (let i = 0; i < totalPages; i++) {
      const pageLabel = pageLabels[i];
      
      // Cek apakah ada mapping manual untuk halaman ini
      if (hasMapping && hasMapping[pageLabel]) {
        const ending = hasMapping[pageLabel];
        result.push({
          juz,
          page_label: pageLabel,
          surah_name: getSurahName(ending.surah, ayahs),
          surah_number: ending.surah,
          ayah: ending.ayah
        });
      } else {
        // Generate otomatis berdasarkan pembagian rata
        // Untuk halaman terakhir, ambil sampai akhir array
        const start = Math.floor((i * juzAyahs.length) / totalPages);
        const end = (i === totalPages - 1) 
          ? juzAyahs.length 
          : Math.floor(((i + 1) * juzAyahs.length) / totalPages);
        
        const chunk = juzAyahs.slice(start, end);

        if (chunk.length === 0) {
          // Jika chunk kosong (misalnya untuk halaman yang punya mapping), skip
          if (hasMapping && hasMapping[pageLabel]) {
            continue;
          }
          // Otherwise, use the last available ayah
          if (juzAyahs.length > 0) {
            const lastAyah = juzAyahs[juzAyahs.length - 1];
            result.push({
              juz,
              page_label: pageLabel,
              surah_name: lastAyah.surah_name,
              surah_number: lastAyah.surah_number,
              ayah: lastAyah.ayah
            });
          }
          continue;
        }

        const lastAyah = chunk[chunk.length - 1];

        result.push({
          juz,
          page_label: pageLabel,
          surah_name: lastAyah.surah_name,
          surah_number: lastAyah.surah_number,
          ayah: lastAyah.ayah
        });
      }
    }
  }

  return result;
}

async function main() {
  console.log("Fetching Quran data...");
  const ayahs = await fetchAllAyahs();

  console.log("Processing...");
  const result = splitJuzIntoSlots(ayahs);

  fs.writeFileSync(
    "quran-page-split-30juz.json",
    JSON.stringify(result, null, 2)
  );

  console.log("✅ Done! File saved: quran-page-split-30juz.json");
  console.log(`📊 Total entries: ${result.length}`);
}

main();