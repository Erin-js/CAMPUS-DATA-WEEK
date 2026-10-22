# Naskah dan arahan visual infografis CDW 2026

Tanggal verifikasi angka: 3 Oktober 2026.

Dokumen ini memuat naskah yang dapat disunting tim, arahan visual, dan lampiran pembuktian statistik. Angka deskriptif dicocokkan langsung dengan lima CSV. Dua model pada notebook direplikasi; analisis tambahan mempertimbangkan lama studi serta nilai awal dan angkatan. Analisis tambahan tersebut belum ditambahkan ke notebook sumber.

Rancangan acuan mencatat ketentuan bahwa narasi dan elemen visual utama harus dikerjakan tim sendiri. Perlakukan naskah berikut sebagai bahan penyuntingan tim sebelum digunakan dalam karya lomba.

---

## A. Naskah untuk halaman infografis

### Judul

**Sama-Sama Kuliah, Tak Sama Bebannya**

### Subjudul

Menelusuri irisan pendidikan keluarga, ekonomi, dan capaian mahasiswa untuk merancang dukungan berbasis data.

### Latar belakang — Membaca perjalanan di balik angka

**Ikon keluarga — Titik berangkat.** Mahasiswa generasi pertama berkuliah ketika kedua orang tuanya belum pernah menempuh pendidikan tinggi.

**Ikon dompet dan jam — Kondisi perjalanan.** Latar ekonomi dan aktivitas bekerja dapat menyertai kebutuhan dukungan yang berbeda selama kuliah.

**Ikon grafik dan piala — Capaian.** IPK dan catatan kegiatan memberi gambaran tentang perkembangan akademik serta capaian yang terekam.

Memahami perbedaan tersebut membantu kita membaca perjalanan mahasiswa dengan lebih utuh.

### Pembahasan — Kelompok besar, kondisi yang beririsan

**38,5% mahasiswa adalah generasi pertama.** Sebanyak 1.924 dari 5.000 mahasiswa berada pada kelompok ini.

**72,7% mahasiswa ekonomi rendah adalah generasi pertama.** Status generasi pertama dan ekonomi rendah banyak muncul pada mahasiswa yang sama: 808 dari 1.111 mahasiswa ekonomi rendah.

**46,7% generasi pertama dari ekonomi rendah bekerja sambil kuliah.** Hampir separuh kelompok ini menjalani kuliah bersama aktivitas kerja: 377 dari 808 mahasiswa.

Kondisi-kondisi tersebut beririsan. Perbandingan capaian perlu membaca kombinasi latar mahasiswa.

### Analisis 1 — Kenaikan lebih besar, selisih masih tersisa

Pada 3.603 mahasiswa yang memiliki catatan semester 1 dan 4, IPK kumulatif generasi pertama meningkat dari **2,68 menjadi 3,03**. Kelompok pembanding meningkat dari **3,16 menjadi 3,34**.

Kenaikannya **1,88 kali lebih besar**, sementara selisih IPK menyempit sekitar **35%**. Perkembangan yang lebih besar belum menutup perbedaan titik awal.

### Analisis 2 — Pada ekonomi rendah, pola berbeda saat kondisi beririsan

| Kelompok ekonomi rendah | n | IPK terakhir | Memiliki catatan prestasi/kegiatan | Status cuti atau nonaktif/DO |
| --- | ---: | ---: | ---: | ---: |
| Bukan generasi pertama, tidak bekerja | 204 | 3,29 | 60,8% | 7,4% |
| Bukan generasi pertama, bekerja | 99 | 3,18 | 48,5% | 14,1% |
| Generasi pertama, tidak bekerja | 431 | 3,03 | 42,5% | 15,3% |
| Generasi pertama, bekerja | 377 | 2,81 | 28,6% | 25,5% |

Pada kelompok generasi pertama yang bekerja, **sekitar 1 dari 4** berstatus cuti atau nonaktif/DO. Angka tersebut menunjukkan status yang tercatat, bukan ramalan DO.

Empat kelompok berbeda dibandingkan pada kategori ekonomi yang sama; urutannya bukan tahapan perjalanan satu mahasiswa.

### Analisis 3 — Selisih tetap terlihat setelah penyesuaian model

Setelah ekonomi, UKT, beasiswa, bekerja, dukungan keluarga, tanggungan, gender, fakultas, dan lama studi diperhitungkan, status generasi pertama masih berkaitan dengan:

- **IPK terakhir 0,24 poin lebih rendah**; interval kepercayaan 95%: −0,27 hingga −0,22.
- **Odds memiliki catatan prestasi/kegiatan sekitar separuh** kelompok pembanding; OR 0,50, interval kepercayaan 95%: 0,43–0,58.

Namun, pada model nilai semester 4 yang turut mempertimbangkan nilai semester 1 dan angkatan, generasi pertama memiliki **IP semester 4 sekitar 0,08 poin lebih tinggi**; interval kepercayaan 95%: +0,06 hingga +0,11.

Kondisi akhir dan perkembangan dari titik awal memberi dua gambaran yang saling melengkapi. Hasil model merupakan asosiasi, bukan bukti sebab-akibat.

### Jembatan strategi — Menentukan arah dengan PETA

Temuan ini mengarahkan perhatian pada kombinasi kebutuhan dan perkembangan mahasiswa. Gunakan **PETA** sebagai strategi:

**P — Petakan kebutuhan.** Baca kondisi ekonomi, aktivitas kerja, dukungan keluarga, dan kendala bersama-sama.

**E — Evaluasi perkembangan.** Bandingkan lintasan nilai dengan titik awal mahasiswa.

**T — Tautkan dukungan.** Hubungkan kebutuhan yang dikonfirmasi mahasiswa dengan layanan yang sesuai.

**A — Audit hasil.** Pantau siapa yang terjangkau dan perubahan setelah dukungan diberikan.

### Solusi — JEMBATAN: prototipe dari data menuju pendampingan

**JEMBATAN** adalah usulan aplikasi pendukung layanan mahasiswa yang dapat dibangun tim sains data.

**Peta kebutuhan.** Dashboard kelompok memperlihatkan irisan kondisi mahasiswa dan kebutuhan yang perlu ditinjau.

**Lintasan akademik.** Ringkasan perkembangan nilai membantu dosen pembimbing memulai percakapan pendampingan.

**Rujukan dukungan.** Mahasiswa menerima pilihan mentor, bantuan biaya, atau pendamping kegiatan yang tersedia dan sesuai kebutuhannya.

**Pemantauan tindak lanjut.** Layanan mencatat waktu respons, pendampingan yang diikuti, partisipasi kegiatan, dan perkembangan nilai untuk evaluasi pilot.

Target prototipe: kebutuhan lebih cepat dikenali dan rujukan lebih mudah ditindaklanjuti. Dampak akademiknya perlu diuji bersama kampus.

**Membaca titik awal. Memahami kondisi. Membuka jalan berkembang.**

### Footer

Sumber: lima dataset resmi CDW 2026, universitas anonim, Real World Fake Data. Unit analisis: mahasiswa. Lintasan IPK memakai kohort tetap semester 1 dan 4. Model menunjukkan asosiasi, bukan sebab-akibat. Catatan prestasi/kegiatan mencakup peserta, finalis, dan juara; ketiadaan catatan bukan ukuran kemampuan. Cuti dan nonaktif/DO adalah status yang tercatat, bukan prediksi kejadian. JEMBATAN merupakan usulan prototipe, belum dievaluasi dampaknya.

---

## B. Arahan visual dan alur baca

| Bagian | Visual | Data/elemen yang ditampilkan | Arahan desain |
| --- | --- | --- | --- |
| Judul dan latar belakang | Tiga ikon dengan teks pendek | Keluarga, dompet/jam, grafik/piala | Tanpa grafik data; latar sekitar 50–70 kata. Ikon membantu navigasi. |
| Konteks kelompok | Angka besar 38,5% | 1.924/5.000 mahasiswa | Cukup angka dan caption. Jangan menambah waffle 100 ikon bila ruang sempit. |
| Konteks ekonomi | Dua bar 100% sederhana | Generasi pertama: rendah 42,0%, menengah 51,7%, tinggi 6,3%; pembanding: 9,9%, 54,0%, 36,1% | 72,7% tampil sebagai callout dengan penyebut 1.111 mahasiswa ekonomi rendah. Pastikan penyebutnya berbeda dari isi bar. |
| Konteks bekerja | Dua bar pendek | Generasi pertama ekonomi rendah 46,7% (377/808); pembanding ekonomi rendah 32,7% (99/303) | Dua kategori mudah dibandingkan. Sumbu persentase mulai nol. |
| Analisis lintasan | Slope chart dua garis | Generasi pertama 2,68→3,03; pembanding 3,16→3,34; +0,35 vs +0,19 | Adaptasi grafik kohort tetap di notebook. Beri label IPK kumulatif, semester 1/4, n=1.345/2.258. Jika sumbu dipotong, tampilkan skala jelas. |
| Analisis irisan | Empat kartu dalam matriks 2×2 | Baris: generasi pertama/bukan; kolom: bekerja/tidak. Setiap kartu berisi n, IPK, % catatan prestasi/kegiatan, % status cuti/nonaktif | Sorot n=377. Jangan gunakan tangga yang tampak mengklaim penjumlahan efek. Tiga indikator berbeda satuan tidak memakai satu sumbu bersama. |
| Analisis model | Dua forest plot kecil dan satu callout | Koefisien IPK −0,242 (CI −0,267 s.d. −0,217), OR 0,497 (CI 0,429–0,576), callout IP semester 4 +0,083 | Forest pertama garis nol; forest kedua garis satu. Jangan gabungkan koefisien dan OR pada sumbu sama. Cantumkan 95% CI. |
| Jembatan strategi | Empat batu pijakan P–E–T–A | Kebutuhan → perkembangan → rujukan → evaluasi | Ini diagram strategi yang diusulkan, bukan grafik alur kausal dari data. |
| Solusi | Mockup aplikasi mini dan empat label fungsi | Peta kebutuhan, lintasan nilai, rujukan, tindak lanjut | Gunakan label “usulan prototipe”. Fokus mahasiswa dan layanan yang dihubungkan, tanpa jargon pemrograman. |

Proporsi ruang yang disarankan: judul/latar 15%, pembahasan 20%, analisis inti 40%, jembatan 8%, solusi 12%, footer 5%. Jika halaman terlalu padat, hapus callout tambahan dahulu; pertahankan ukuran teks.

Palet: jingga #E8710A untuk generasi pertama, biru #1B3A5F untuk pembanding, merah bata #A8402D untuk irisan kondisi yang disorot, hijau #2E8B57 untuk strategi/solusi, krem #FBF7EE untuk latar. Warna kelompok tetap konsisten.

Jika ingin menonjolkan prestasi lebih jauh, ganti grafik bar bekerja dengan dumbbell catatan prestasi/kegiatan menurut ekonomi: rendah 36,0% vs 56,8%; menengah 44,9% vs 64,7%; tinggi 59,0% vs 74,5%. Ini bukti perbedaan capaian tercatat, bukan pengukuran langsung akses kesempatan.

---

## C. Lampiran pembuktian statistik

### Pemeriksaan sumber

- Gabung profil, generasi pertama, ekonomi dengan ID_Mahasiswa dan relasi satu-ke-satu.
- Tabel prestasi memiliki 6.414 baris mentah dan tujuh duplikat identik; indikator mahasiswa tidak berubah karena deduplikasi.
- Semua catatan per mahasiswa diringkas sebelum penggabungan agar penyebut tetap 5.000.
- Capaian Peserta juga terdapat dalam tabel. Indikator umum diberi nama catatan prestasi/kegiatan, bukan kemenangan.
- Kohort semester 1/4 mencakup 3.603 mahasiswa, terdiri dari 1.345 generasi pertama dan 2.258 pembanding.

### Nilai asli untuk angka turunan

| Kelompok | IPK kumulatif semester 1 | IPK kumulatif semester 4 | Kenaikan |
| --- | ---: | ---: | ---: |
| Generasi pertama | 2,6845204461 | 3,0349144981 | 0,3503940520 |
| Pembanding | 3,1572276351 | 3,3433525244 | 0,1861248893 |

Rasio kenaikan 1,8825749388. Selisih awal 0,4727071890; selisih akhir 0,3084380262. Penyempitan 34,7507%. Semua angka turunan dihitung dari nilai asli, bukan angka grafik yang sudah dibulatkan.

Kenaikan lebih besar tidak membuktikan bahwa satu kelompok lebih tangguh atau mempunyai efek intervensi. Nilai awal yang rendah memberi ruang kenaikan lebih luas; IPK juga memiliki batas atas 4. Model nilai semester 4 dengan penyesuaian baseline merupakan pemeriksaan tambahan untuk isu ini.

### Model pada notebook, direplikasi

OLS: IPK terakhir ~ generasi pertama + bekerja + beasiswa + dukungan keluarga + tanggungan + kategori ekonomi + kategori UKT + gender + fakultas. Ekonomi, UKT, gender, dan fakultas memakai dummy kategori; standard error HC3.

Logistik binomial: indikator mahasiswa memiliki ≥1 catatan prestasi/kegiatan dengan kovariat yang sama. Interval OR menggunakan kovarians sandwich robust.

| Variabel | Koefisien IPK | CI 95% | OR catatan prestasi/kegiatan | CI 95% |
| --- | ---: | --- | ---: | --- |
| Generasi pertama | −0,2530 | −0,2802 s.d. −0,2258 | 0,5222 | 0,4555–0,5986 |
| Bekerja | −0,1664 | −0,1953 s.d. −0,1375 | 0,5958 | 0,5172–0,6864 |
| Beasiswa | +0,1838 | +0,1583 s.d. +0,2093 | 1,3596 | 1,1873–1,5569 |

R² OLS = 0,2284. Ini bukan akurasi 22,8% dan bukan ukuran kelayakan keputusan individual.

### Analisis tambahan 1: mempertimbangkan lama studi

Model di atas ditambah kategori Masa_Studi_Semester. Alasannya, nilai terakhir dan peluang mengumpulkan catatan prestasi dapat berbeda menurut lamanya mahasiswa berada di kampus.

| Variabel | Koefisien IPK | CI 95% | OR catatan prestasi/kegiatan | CI 95% |
| --- | ---: | --- | ---: | --- |
| Generasi pertama | −0,2421 | −0,2674 s.d. −0,2169 | 0,4969 | 0,4288–0,5759 |
| Bekerja | −0,1431 | −0,1699 s.d. −0,1163 | 0,5956 | 0,5115–0,6935 |
| Beasiswa | +0,1741 | +0,1498 s.d. +0,1983 | 1,3771 | 1,1922–1,5906 |

n=5.000. R² OLS = 0,3239. Selisih generasi pertama tetap terlihat. Lama studi juga dapat terkait dengan status akademik, sehingga pemeriksaan ini bukan penyelesaian semua bias atau model kausal.

### Analisis tambahan 2: nilai awal dan semester 4

Model baseline/ANCOVA: IP_Semester pada semester 4 ~ generasi pertama + bekerja + beasiswa + dukungan keluarga + tanggungan + kategori ekonomi + kategori UKT + gender + fakultas + IP semester 1 + kategori angkatan.

IP semester 1 sama dengan IPK kumulatif semester 1. Outcome memakai IP semester 4, bukan IPK kumulatif, agar nilai semester 1 tidak menjadi komponen matematis langsung dari outcome.

- n=3.603; R²=0,4637; standard error HC3.
- Generasi pertama: +0,08344 poin; CI 95% +0,05593 s.d. +0,11096; p sekitar 2,79×10^-9.
- Bekerja: −0,04903 poin; CI 95% −0,07699 s.d. −0,02106.

Interpretasi: pada kovariat dan nilai awal yang disesuaikan model, IP semester 4 generasi pertama rata-rata lebih tinggi. Ini pertanyaan berbeda dari perbandingan IPK terakhir; hasilnya tidak saling membatalkan. Tidak diketahui sejak kapan mahasiswa bekerja, menerima beasiswa, atau mengikuti pendampingan.

### Statistik yang tidak layak dijadikan klaim

- OR 0,50 bukan probabilitas 50%, bukan penurunan peluang 50%, dan bukan risiko DO.
- Cuti/nonaktif adalah status saat data dicatat, bukan kejadian prospektif.
- Catatan kegiatan tidak mengukur biaya lomba, penolakan pendaftaran, waktu belajar, atau bakat.
- Kategori UKT adalah kelompok biaya, bukan nilai rupiah persis atau ukuran semua biaya kuliah.
- Model beasiswa belum mengatasi seleksi penerima; hubungan positif tidak membuktikan manfaat beasiswa.
- Nilai-p pada data simulasi mendeskripsikan pola statistik dataset; tidak menjadi bukti tentang seluruh mahasiswa Indonesia.

---

## D. Pilihan analisis lanjutan

### Pilihan utama untuk cerita ini

Gunakan kohort tetap + analisis irisan + regresi dengan penyesuaian lama studi + model semester 4 dengan baseline. Keempatnya sudah dihitung/ditelusuri pada pekerjaan ini dan langsung menjawab benang merah cerita.

### Clustering sebagai pengayaan opsional

Jika ingin menambah tipologi kebutuhan, lakukan clustering variabel kondisi, bukan mencampur outcome lalu menjadikan rendahnya outcome sebagai penemuan baru. Fitur awal dapat mencakup ekonomi, UKT, generasi pertama, bekerja, beasiswa, persepsi dukungan keluarga, dan kendala. Pertimbangkan redundansi ekonomi–UKT sebelum memberi bobot.

Karena data campuran kategorik/ordinal, gunakan k-prototypes atau jarak Gower dengan metode pengelompokan yang sesuai. Bandingkan jumlah cluster menggunakan kualitas pemisahan pada ruang fitur asli, ukuran cluster, dan stabilitas pada beberapa pengulangan/subsampel. Setelah cluster terbentuk, bandingkan IPK dan catatan kegiatan, dengan penyesuaian angkatan/lama studi bila perlu.

Visual pilihan: heatmap profil cluster plus n tiap cluster. Label tipologi mengikuti hasil aktual, misalnya “bekerja dan dukungan rendah” hanya jika profil data mendukung. Belum ada hasil clustering terverifikasi; jangan menulis jumlah cluster atau nama tipologi sebagai temuan final saat ini.

### Forecasting dan peringatan dini

Forecasting agregat tidak menjadi pilihan utama karena semester bukan deret waktu kalender universitas, jumlah mahasiswa berubah, dan riwayat masing-masing pendek. Model notebook dengan ROC-AUC 0,804 memisahkan catatan prestasi yang sudah terjadi; itu bukan model deteksi DO atau prediksi prestasi masa depan.

Model peringatan dini baru memerlukan outcome semester berikutnya, waktu pengukuran semua fitur, pemisahan latih/uji menurut waktu serta mahasiswa, dan validasi kalibrasi/ketepatan per kelompok. Sebelum data tersebut tersedia, modul prototipe memakai pemantauan lintasan dan aturan yang dapat ditinjau manusia.

---

## E. Spesifikasi prototipe mahasiswa sains data

**Nama:** JEMBATAN. **Tujuan:** membantu mahasiswa dan layanan kampus menemukan serta menindaklanjuti dukungan yang sesuai. **Batas MVP:** satu aplikasi demonstrasi dengan data fiktif yang tersedia.

1. Integrasi lima tabel dan dashboard kebutuhan kelompok, dengan ukuran sampel dan filter ekonomi/generasi pertama/bekerja.
2. Lintasan IP per mahasiswa untuk pengguna berwenang; layar publik hanya agregat. Perkembangan nilai adalah bahan percakapan, bukan keputusan otomatis.
3. Direktori layanan yang diisi/verifikasi pengelola. Status sosial-ekonomi tidak otomatis menentukan penerima beasiswa atau menghalangi akses layanan.
4. Form konfirmasi kebutuhan mahasiswa, saran rujukan yang bisa dipilih, dan log tindak lanjut.
5. Dashboard evaluasi waktu respons, rujukan yang diikuti, keterlibatan kegiatan, dan perkembangan nilai. Metrik layanan baru memerlukan data pilot dan tidak diklaim sudah tersedia pada lima CSV.

Pengujian prototipe: rekonsiliasi angka sumber, uji alur rujukan, dan penilaian kegunaan bersama pengguna. Pengujian dampak: pilot layanan dengan baseline dan kelompok pembanding yang layak; laporkan siapa yang tidak terjangkau. Prototipe tidak dapat menjanjikan kenaikan IPK atau penurunan DO sebelum diuji.

Sumber kerja: Rekomendasi_Rancangan_Infografis_CDW2026.md, Eksplorasi_Insight_Mahasiswa_CDW2026.ipynb, serta 1_profil_mahasiswa_umum.csv, 2_prestasi_mahasiswa.csv, 3_generasi_pertama_kuliah.csv, 4_status_sosial_ekonomi.csv, 5_riwayat_ipk_semester.csv.
