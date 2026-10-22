# Rekomendasi Rancangan Infografis — Infographic Competition CDW 2026

Dokumen ini adalah **rancangan isi dan struktur**, bukan naskah final maupun desain visual jadi. Sesuai TM Infographic Competition CDW2026 (slide 8–9), elemen visual utama dan narasi infografis harus dibuat oleh tim sendiri; AI hanya boleh membantu memahami dataset dan mencari kemungkinan insight. Gunakan dokumen ini sebagai bahan diskusi tim, lalu tulis ulang naskah final dan eksekusi desainnya sendiri.

**Pengingat tenggat:** Guidebook mencantumkan batas unggah 25 September 2026, sedangkan TM mencantumkan 8 Oktober 2026. Dua tanggal ini berbeda — **konfirmasi tenggat yang berlaku di portal CDW atau grup resmi panitia sebelum menyusun jadwal kerja tim.**

Struktur cerita yang dipakai di sini: **Babak 1 Masalah (data ringan) → Babak 2 Statistik matang → Babak 3 Solusi.**

---

## 1. Judul & Subjudul

| Opsi | Judul | Subjudul | Catatan |
| --- | --- | --- | --- |
| **A — rekomendasi** | "Sama-Sama Kuliah, Tak Sama Bebannya" | "Generasi pertama kuliah mulai dari titik akademik lebih rendah, bekerja lebih banyak sambil kuliah, dan punya kesempatan berprestasi lebih sempit. Inilah yang data tunjukkan — dan apa yang bisa dilakukan kampus." | Judul langsung menyatakan masalah; subjudul menjanjikan solusi di akhir, sejalan dengan alur 3 babak. |
| B | "Naik Lebih Cepat, tetapi Berangkat Lebih Jauh" | "Mereka mengejar dengan kecepatan lebih tinggi — namun start mereka lebih jauh di belakang. Berikut dari mana jarak itu datang, dan ke mana jalan keluarnya." | Mempertahankan metafora rancangan lama; ujung subjudul diubah agar menjanjikan solusi, bukan menutup dengan pertanyaan reflektif seperti versi sebelumnya. |
| C | "Titik Berangkat yang Tidak Sama" | "Hampir 2 dari 5 mahasiswa memulai kuliah dari garis start yang berbeda. Ini jaraknya — dan ini yang bisa ditutup." | Paling blak-blakan sebagai pembuka masalah; cocok jika tim ingin kesan lebih tegas, kurang puitis. |

Rekomendasi: **Opsi A.** Judulnya sendiri sudah menyatakan masalah (sesuai arahan "awal menekankan masalah"), dan subjudulnya menutup dengan janji solusi tanpa bergantung pada metafora yang bisa disalahartikan sebagai ukuran data (lihat catatan soal metafora pendakian di `penjelasan_rancangan.md`).

---

## 2. Alur Cerita 3 Babak

| Babak | Panel | Fungsi | Fokus angka | Tinggi A3 (usulan) |
| --- | --- | --- | --- | ---: |
| **1. Masalah** | 0 — Hero | Judul, subjudul, ilustrasi minimal (tanpa data) | — | 8% |
| | 1 — Skala | Seberapa besar kelompok ini? | 38,5% (1.924/5.000) generasi pertama | 7% |
| | 2 — Irisan ekonomi | Dari kondisi apa mereka berangkat? | 72,7% mahasiswa ekonomi rendah adalah generasi pertama | 8% |
| | 3 — Beban waktu | Beban apa yang menyertai kuliah? | 46,7% generasi pertama-ekonomi rendah bekerja sambil kuliah | 8% |
| **2. Statistik matang** | 4 — Lintasan IPK | Puncak cerita 1: bagaimana perkembangan akademiknya? | 2,68→3,03 vs 3,16→3,34 (n=3.603); rasio kenaikan ±1,88× | 16% |
| | 5 — Beban bertumpuk | Puncak cerita 2: pola pada irisan kelompok | IPK 2,81 vs 3,29; prestasi 28,6% vs 60,8%; cuti/nonaktif 25,5% vs 7,4% (n=377 vs 204) | 14% |
| | 6 — Kesenjangan kesempatan | Apakah jaraknya hanya terlihat di IPK? | Selisih catatan prestasi 20,8 / 19,8 / 15,5 poin persentase per kategori ekonomi | 10% |
| | 7 — Validasi model | Apakah ekonomi saja cukup menjelaskan? | −0,25 poin IPK & 0,52× odds (generasi pertama); −0,17 poin & 0,60× odds (bekerja) | 6% |
| **3. Solusi** | 8 — Diagnosis | Menghubungkan 3 lapisan temuan | Titik awal, beban waktu, kesempatan | 8% |
| | 9 — Arah solusi | Apa yang bisa dilakukan? | 3 kartu aksi, dipetakan 1:1 ke 3 lapisan | 10% |
| | Footer | Sumber, metodologi, keterbatasan | — | 5% |

Catatan perubahan dari rancangan lama ("Naik Lebih Cepat, tetapi Berangkat Lebih Jauh"): panel lintasan IPK yang dulu menjadi "puncak pertama" di bagian awal, di sini **dipindah ke Babak 2**, karena itu bukti analitis utama, bukan sekadar pembuka masalah. Babak 1 sengaja dibuat ringan — tiga angka tunggal untuk membangun tensi, tanpa chart kompleks dulu.

---

## 3. Detail Isi & Pilihan Visualisasi per Panel

### Babak 1 — Masalah (ringan data)

**Panel 1 — Skala.**
Visual: *waffle chart* 10×10 ikon, 38 ikon penuh + 1 ikon setengah warna jingga mewakili 38,5%.
Alasan: cara tercepat menunjukkan "ini bukan kelompok kecil" tanpa paragraf penjelasan.
Sumber: `3_generasi_pertama_kuliah.csv`.

**Panel 2 — Irisan ekonomi.**
Visual: dua *bar* horizontal 100% (komposisi ekonomi rendah/menengah/tinggi untuk generasi pertama vs bukan), dengan 72,7% sebagai angka fokus besar; 42,0% dan 9,9% tampil sebagai pembanding kecil.
Alasan: dua arah baca penyebut (42,0% vs 72,7%) tetap terlihat tanpa membingungkan, karena hanya satu angka dijadikan hero.
Sumber: tabel generasi pertama + status sosial ekonomi, digabung per `ID_Mahasiswa`.

**Panel 3 — Beban waktu.**
Visual: *lollipop chart* horizontal, 4 kelompok diurutkan dari persentase bekerja tertinggi ke terkecil.
Alasan: menonjolkan satu titik nilai (46,7%) tanpa bar tebal yang terasa berat di babak pembuka.
Sumber: tabel generasi pertama + status sosial ekonomi.

### Babak 2 — Statistik matang (inti pembuktian, porsi ruang terbesar)

**Panel 4 — Lintasan IPK.**
Visual: *slope chart* dua garis rata-rata IPK kumulatif dari semester 1 ke semester 4.
Alasan: panel terbesar karena memuat dua pesan sekaligus — titik awal lebih rendah DAN kenaikan lebih cepat. Kompleksitas pesan inilah yang membuatnya pantas menjadi bagian "statistik matang".
Wajib dicantumkan: n = 3.603 mahasiswa yang punya catatan di semester 1 dan 4; label "IPK kumulatif", bukan IP semester.
Sumber: tabel generasi pertama + riwayat IPK semester.

**Panel 5 — Beban bertumpuk.**
Visual: 4 kartu/anak tangga kecil (*small multiples*) untuk 4 kelompok ekonomi rendah (kombinasi generasi pertama × bekerja), masing-masing menampilkan rata-rata IPK, % memiliki catatan prestasi, % nasional/internasional, % cuti-nonaktif. Sorot kelompok generasi pertama-bekerja (n=377) dengan warna merah bata.
Catatan wajib: empat kelompok ini adalah perbandingan antar-kelompok berbeda, bukan satu kelompok yang diikuti sepanjang waktu; urutan visual tidak membuktikan beban bertambah secara kumulatif.
Sumber: tabel profil, prestasi, generasi pertama, status sosial ekonomi.

**Panel 6 — Kesenjangan kesempatan.**
Visual: *dumbbell chart*, satu baris per kategori ekonomi (rendah/menengah/tinggi), dua titik (generasi pertama vs bukan) dihubungkan garis selisih.
Alasan: dumbbell pas untuk "selisih dua kelompok yang berulang di beberapa kategori", lebih jelas dibanding bar berdampingan.
Catatan: selisih dinyatakan dalam poin persentase, bukan persentase kenaikan relatif; tidak mengukur akses kesempatan secara langsung, hanya catatan prestasi yang tercatat.
Sumber: tabel prestasi, generasi pertama, status sosial ekonomi.

**Panel 7 — Validasi model.**
Visual: 4 *tile* angka ringkas (bukan tabel regresi panjang): −0,25 poin IPK & 0,52× odds memiliki catatan prestasi (generasi pertama); −0,17 poin IPK & 0,60× odds (bekerja sambil kuliah), setelah mengontrol kategori ekonomi, UKT, dukungan keluarga, tanggungan, jenis kelamin, dan fakultas.
Caption wajib: **"Asosiasi model, bukan estimasi sebab-akibat."** Odds ratio bukan probabilitas langsung.
Sumber: hasil model pada notebook eksplorasi (OLS untuk IPK, regresi logistik untuk catatan prestasi).

### Babak 3 — Solusi

**Panel 8 — Diagnosis.**
Ringkas 3 lapisan temuan dalam satu-dua kalimat per lapisan: titik awal akademik, beban waktu, kesenjangan kesempatan. Menyambung langsung ke panel 9.

**Panel 9 — Arah solusi.**
Visual: 3 kartu ikon sejajar (bukan chart data), masing-masing dipetakan langsung ke satu lapisan masalah.

| Temuan | Arah solusi (hedged, bukan janji hasil) | Aktor realistis |
| --- | --- | --- |
| Titik awal akademik rendah | Program transisi/pendampingan intensif semester awal + peringatan dini akademik | Fakultas/prodi, dosen pembimbing akademik |
| Beban waktu (kerja sambil kuliah) | Opsi kerja-studi relevan di kampus, dana darurat, penjadwalan kuliah fleksibel | Unit kemahasiswaan, unit keuangan/beasiswa |
| Kesenjangan kesempatan berprestasi | Jalur partisipasi lomba/kegiatan berbiaya terjangkau + pendampingan submission | Pengelola kegiatan kemahasiswaan |

Gunakan bahasa seperti "arah yang perlu diuji", bukan klaim dampak terukur ("solusi ini akan menaikkan IPK sebesar X"). Dataset ini deskriptif/asosiatif, bukan bukti kausal — konsisten dengan batasan interpretasi yang sudah dipegang di seluruh panel sebelumnya.

**Footer.**
Sumber lima tabel data, catatan data fiktif (*Real World Fake Data*), batas sampel kecil (misalnya n=99 pada salah satu kelompok di panel 5), dan label "universitas anonim" — wajib ada sesuai TM slide 4–5.

---

## 4. Pewarnaan

Lanjutkan palet yang sudah dipakai di rancangan sebelumnya:

| Warna | Kode | Arti |
| --- | --- | --- |
| Jingga | `#E8710A` | Generasi pertama |
| Biru tua | `#1B3A5F` | Bukan generasi pertama |
| Merah bata | `#A8402D` | Sorotan beban bertumpuk / cuti-nonaktif |
| Hijau | `#2E8B57` | Peningkatan IPK (Babak 2) **dan** zona solusi (Babak 3) |
| Krem / putih | `#FBF7EE` | Latar halaman/panel |
| Abu muda | `#E6E6E3` | Elemen netral, ikon pembanding waffle |

Penambahan makna: geser aksen ke **hijau** di seluruh Babak 3 sebagai sinyal visual "sekarang kita bicara ke depan/perbaikan" — membantu pembaca merasakan transisi dari diagnosis ke solusi tanpa teks penanda tambahan.

---

## 5. Yang Perlu Dicek Tim Sebelum Desain Final

1. Jalankan ulang notebook `Eksplorasi_Insight_Mahasiswa_CDW2026.ipynb` untuk memastikan angka panel 5–7 (tabel interseksional, dumbbell, koefisien model) — beberapa output notebook berupa tabel `Styler` yang tidak tersimpan sebagai teks, sehingga perlu dibuka ulang di Jupyter.
2. Konfirmasi tenggat pengumpulan yang berlaku di portal CDW resmi.
3. Pastikan definisi gabungan "cuti/nonaktif" pada panel 5 sudah disepakati tim.
4. Hitung ulang angka turunan (rasio kenaikan, selisih, penyempitan) dari nilai asli dengan aturan pembulatan konsisten — jangan merekonstruksi dari angka yang sudah dibulatkan.
5. Naskah final dan elemen visual utama harus ditulis/dibuat tim sendiri sesuai batasan AI pada TM slide 8–9; jangan menyalin mentah hasil AI ke karya akhir.
6. Jangan mencantumkan nama universitas mana pun; gunakan label "universitas anonim" bila konteks diperlukan.

---

*Sumber acuan: `penjelasan_lomba_cdw.md`, `penjelasan_rancangan.md`, dan `Eksplorasi_Insight_Mahasiswa_CDW2026.ipynb`.*
