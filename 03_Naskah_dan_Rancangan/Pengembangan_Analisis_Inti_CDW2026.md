# Pengembangan Analisis Inti — CDW 2026

Rancangan sumber: `C:\Users\ACER\Downloads\BRAIN_STORM_INFOGRAPHIC (6).docx`. Dokumen sumber tidak diubah. Angka di bawah dihitung dari lima CSV CDW, bukan diambil sebagai fakta dari naskah sumber. Data fiktif/simulasi; tidak mewakili seluruh mahasiswa Indonesia.

[Notebook dengan analisis dan visual tambahan](../02_Analisis/Visualisasi_Infografis_CDW2026.ipynb) · [Katalog visual tambahan](../04_Visualisasi/output_visualisasi_cdw/analisis_lanjutan/Katalog_Analisis_Lanjutan_CDW2026.pdf)

## 1. Perubahan struktur yang disarankan

Bagian analisis saat ini hanya mempunyai dua pertanyaan analitis: perkembangan nilai dan hasil regresi. PETA sudah menjawab strategi, sehingga sebaiknya dipindahkan menjadi penghubung setelah analisis dan sebelum JEMBATAN.

Subbagian “Nilai Akhir Belum Menceritakan Seluruh Perkembangan” memuat tiga hasil yang berbeda. Pisahkan menjadi: posisi IPK terakhir, catatan kegiatan, dan perkembangan setelah memperhitungkan titik awal. Perbedaan target dan populasi analisis perlu tampak, agar koefisien −0,24 dan +0,08 tidak dibaca sebagai kontradiksi.

Benang merah yang diperluas:

**Titik awal berbeda → perkembangan nyata → kesenjangan capaian belum hilang → kebutuhan tidak cukup dibaca dari satu kategori → prediksi diuji beserta batasnya → pendampingan berdasarkan kebutuhan yang dikonfirmasi.**

## 2. Modul narasi dan visual

### A. Memulai Lebih Rendah, Bertumbuh Lebih Besar

**Isi infografis:**

Pada 3.603 mahasiswa dengan catatan semester 1 dan 4, rata-rata IPK kumulatif generasi pertama meningkat dari 2,68 menjadi 3,03. Kenaikannya +0,35 poin, dibanding +0,19 pada kelompok pembanding. Selisih rata-rata antarkelompok menyempit sekitar 34,8%, tetapi belum hilang.

**Pesan:** nilai terakhir tidak cukup untuk menggambarkan perjalanan akademik.

**Visual utama:** grafik dua garis semester 1–4, memakai mahasiswa yang sama pada setiap semester. Alternatif lebih ringkas: slope chart semester 1–4. Jangan memasang keduanya sekaligus pada poster.

[Lintasan empat semester](../04_Visualisasi/svg_plot_cdw2026/13_lintasan_semester_1_4.svg) · [Slope chart](../04_Visualisasi/svg_plot_cdw2026/04_slope_ipk_kohort_tetap.svg)

**Batas:** rata-rata IPK kumulatif, bukan IP tiap semester; kelompok dengan catatan lengkap bukan seluruh 5.000 mahasiswa. Ini bukan bukti efek dukungan tertentu atau gambaran mahasiswa tanpa catatan semester 4.

**Transisi:** “Kemajuan terlihat. Namun, apakah perbedaan capaian terakhir sudah menghilang?”

### B. IPK Terakhir Masih Berjarak

**Isi infografis:**

Setelah ekonomi, UKT, aktivitas bekerja, beasiswa, dukungan keluarga, tanggungan, jenis kelamin, fakultas, dan lama studi diperhitungkan, status generasi pertama masih berkaitan dengan IPK terakhir 0,24 poin lebih rendah. Rentang kepercayaan 95%: −0,27 sampai −0,22 poin.

**Visual:** forest plot koefisien OLS, atau potongan satu koefisien generasi pertama dengan garis CI 95%. Koefisien lain boleh dipindahkan ke notebook supaya poster tidak penuh.

[Forest plot IPK terakhir](../04_Visualisasi/svg_plot_cdw2026/06_forest_ipk_terkontrol.svg)

**Metode:** OLS, n=5.000, standard error HC3; R²=0,324. Hubungan observasional, bukan pengaruh sebab-akibat. Pengendalian variabel hanya mencakup kondisi yang tersedia.

### C. Kesenjangan Tidak Berhenti pada Nilai

**Isi infografis:**

Pada ekonomi rendah, 36,0% generasi pertama mempunyai catatan prestasi/kegiatan, dibanding 56,8% kelompok pembanding. Selisih juga terlihat pada ekonomi menengah dan tinggi. Dalam model yang memperhitungkan sejumlah kondisi mahasiswa serta lama studi, odds memiliki catatan tersebut pada generasi pertama sekitar separuh kelompok pembanding: OR 0,50; CI 95% 0,43–0,58.

**Visual utama:** dumbbell tiga kategori ekonomi untuk memperlihatkan pola. Tambahkan OR sebagai angka kecil; forest plot logistik lengkap sebagai alternatif, bukan grafik tambahan wajib.

[Dumbbell kegiatan menurut ekonomi](../04_Visualisasi/svg_plot_cdw2026/11_dumbbell_prestasi_ekonomi.svg) · [Forest plot odds](../04_Visualisasi/svg_plot_cdw2026/07_forest_odds_prestasi.svg)

**Batas:** catatan mencakup peserta kegiatan, bukan hanya juara. OR bukan probabilitas dan tidak berarti peluang turun 50%. Ketiadaan catatan tidak membuktikan ketidakmampuan atau ketiadaan akses. Kelompok generasi pertama ekonomi tinggi hanya n=122.

**Transisi:** “Perbedaan capaian memang tercatat. Tetapi membaca kemampuan hanya dari posisi akhir juga melewatkan titik awal.”

### D. Saat Titik Awal Diperhitungkan, Gambarnya Berubah

**Isi infografis:**

Pada mahasiswa yang mempunyai catatan semester 1 dan 4, setelah nilai semester pertama, angkatan, serta sejumlah kondisi mahasiswa diperhitungkan, generasi pertama memiliki IP semester 4 sekitar 0,08 poin lebih tinggi. CI 95%: +0,06 sampai +0,11 poin.

**Visual:** forest plot model baseline-adjusted, terutama satu koefisien generasi pertama. Bisa menjadi callout di bawah grafik perkembangan pada modul A.

[Forest plot IP semester 4](../04_Visualisasi/svg_plot_cdw2026/08_forest_ip_semester4_baseline.svg)

**Metode:** OLS HC3, n=3.603, R²=0,464. Outcome adalah IP semester 4, bukan IPK terakhir. Model bukan eksperimen, bukan difference-in-differences, dan tidak membuktikan kelompok tertentu secara intrinsik lebih mampu. Penyesuaian baseline juga bukan bukti kausal atau jaminan bebas regresi menuju rata-rata.

### E. Kebutuhan Tidak Selalu Terlihat dari Kategori Ekonomi

**Isi infografis:**

Clustering merangkum tiga profil kondisi mahasiswa. Pada profil dengan kendala utama finansial, terdapat 1.648 mahasiswa: 58,6% merupakan generasi pertama. Namun, 57,4% justru berada pada kategori ekonomi menengah atau tinggi. Kategori ekonomi rendah saja belum mencakup seluruh mahasiswa yang mencatat kendala finansial.

**Visual utama untuk poster:** dua stacked bar sederhana: komposisi ekonomi dan generasi pertama pada profil finansial. **Alternatif mendalam:** heatmap tiga profil. Jangan menjadikan heatmap tujuh kolom sebagai satu-satunya cara pembaca memahami pesan.

[Komposisi profil finansial](../04_Visualisasi/svg_plot_cdw2026/22_cluster_kendala_finansial.svg) · [Heatmap profil kebutuhan](../04_Visualisasi/svg_plot_cdw2026/15_heatmap_profil_kebutuhan.svg)

| Profil deskriptif | Jumlah | Generasi pertama | IPK terakhir | Catatan kegiatan | Cuti/nonaktif/DO |
| --- | ---: | ---: | ---: | ---: | ---: |
| C1: bekerja, kendala utama nonfinansial | 663 | 42,8% | 3,05 | 46,3% | 10,4% |
| C2: kendala utama finansial, status bekerja beragam | 1.648 | 58,6% | 3,08 | 48,2% | 17,1% |
| C3: tidak bekerja, kendala utama nonfinansial | 2.689 | 25,1% | 3,31 | 66,3% | 5,3% |

**Pesan tambahan:** C2 bukan profil dengan IPK terendah, tetapi mempunyai proporsi status cuti/nonaktif/DO paling besar secara deskriptif. Nilai dan status akademik bukan ukuran yang sama. Ini tidak membuat C2 menjadi label risiko individual.

[Perbandingan capaian profil dengan CI 95%](../04_Visualisasi/svg_plot_cdw2026/16_capaian_menurut_cluster.svg)

**Metode dan kelayakan:**

- Hierarchical average linkage dengan jarak Gower untuk fitur campuran: ekonomi ordinal, bekerja, dukungan keluarga, tanggungan, kendala utama; bobot sama per fitur. IPK, prestasi, status akademik, dan generasi pertama tidak ikut membentuk cluster.
- K=2–6 diuji. K=3 dipilih di antara kandidat dengan anggota terkecil minimal 5% dan median ARI minimal 0,70. K=6 mempunyai silhouette lebih tinggi tetapi cluster terkecil hanya 2,94%; tidak lolos aturan kerja. K=5 mendekati skor K=3, jadi tiga profil bukan satu-satunya pengelompokan yang mungkin.
- Silhouette Gower K=3 sebesar 0,347 pada sampel 1.500 mahasiswa; median ARI=1,000 pada empat pengulangan subsampel 70%. Ini validasi internal yang terbatas, bukan validasi kampus lain.
- Kendala utama dan bekerja sangat menentukan pemisahan; tiga profil dapat dijelaskan hampir sebagai aturan sederhana. Jangan menjualnya sebagai identitas tersembunyi yang hanya bisa ditemukan AI.
- Spesifikasi awal memasukkan beasiswa dan memisahkan status beasiswa secara sempurna. Beasiswa kemudian dikeluarkan karena merupakan dukungan yang diterima, bukan kebutuhan itu sendiri. Perubahan spesifikasi ini dilakukan setelah diagnostik dan tetap eksploratif. ARI antara spesifikasi utama dan yang menambahkan beasiswa hanya 0,071: hasil sensitif terhadap pilihan fitur, meskipun stabil terhadap subsampel.
- Outcome dibandingkan setelah cluster terbentuk: Kruskal–Wallis untuk IPK dan chi-square untuk dua outcome biner, koreksi Holm atas tiga uji. Semua p terkoreksi <0,001, tetapi ukuran efek tetap perlu dilihat: epsilon² IPK=0,058; Cramér's V kegiatan=0,189 dan status akademik=0,180. Signifikansi tidak berarti pengaruh besar atau kausal.
- Capaian profil belum disesuaikan angkatan/lama studi. Status merupakan snapshot, bukan kejadian DO mendatang. Kendala tercatat bukan diagnosis kebutuhan yang telah dikonfirmasi.

[Validasi clustering](../04_Visualisasi/svg_plot_cdw2026/14_validasi_clustering_gower.svg)

### F. Nilai Berikutnya Bisa Diperkirakan—Tidak Dipastikan

**Isi infografis:**

Riwayat IP semester 1–3 dipakai untuk memperkirakan IP semester 4. Pada 1.213 mahasiswa angkatan 2024 yang tidak ikut memilih model, Ridge menghasilkan rata-rata kesalahan 0,229 poin. Memakai IP semester 3 saja menghasilkan kesalahan 0,272 poin. Pengurangan kesalahan sekitar 15,7% terhadap baseline tersebut, bukan “akurasi 84,3%”.

**Visual utama:** horizontal bar MAE tiga pendekatan. **Alternatif teknis:** scatter prediksi versus aktual, untuk melihat penyebaran kesalahan; bukan visual wajib poster.

[Perbandingan kesalahan prediksi](../04_Visualisasi/svg_plot_cdw2026/18_prediksi_ip_evaluasi_baseline.svg) · [Prediksi versus aktual](../04_Visualisasi/svg_plot_cdw2026/19_prediksi_vs_aktual_ip4.svg)

**Protokol:**

| Tahap | Angkatan | Jumlah | Fungsi |
| --- | --- | ---: | --- |
| Latih | 2019–2021 | 690 | Melatih kandidat awal |
| Validasi | 2022 | 670 | Memilih kandidat dan hyperparameter |
| Kalibrasi | 2023 | 1.030 | Membentuk interval; tidak melatih model |
| Uji | 2024 | 1.213 | Evaluasi akhir yang ditahan |

Lima alpha Ridge dan tiga konfigurasi Random Forest diuji pada validasi. Ridge alpha=0,01 terpilih; dilatih ulang pada latih+validasi (n=1.360). Nilai validasi antarbeberapa alpha sangat berdekatan, sehingga alpha tersebut bukan parameter universal. Target uji tidak ikut memilih model atau interval. Hasil uji: MAE=0,229; RMSE=0,290; R²=0,581. Pengurangan MAE versus IP3 adalah 0,043 poin, CI bootstrap berpasangan 95% 0,033–0,052; 1.000 pengulangan.

**Mengapa bukan ARIMA/Prophet:** riwayat pendek, panjang pengamatan berbeda, dan data terdiri atas perjalanan banyak mahasiswa, bukan satu deret waktu panjang dengan tanggal observasi yang memadai. Prediksi satu langkah berbasis riwayat lebih sesuai dengan struktur ini. Angkatan bukan tanggal pengamatan; evaluasi ini retrospektif lintas angkatan, bukan bukti kinerja forecasting masa depan.

### G. Model Juga Perlu Diaudit

**Isi infografis:**

Prediksi mempunyai ketidakpastian. Interval dengan target cakupan 90% mencakup 91,1% nilai aktual pada angkatan uji. Kesalahan rata-rata juga berbeda: 0,249 poin pada generasi pertama dan 0,217 pada kelompok pembanding. Model yang berguna secara keseluruhan belum tentu sama baiknya bagi setiap kelompok.

**Visual:** dot-and-whisker untuk contoh interval; bar MAE per kelompok untuk audit. Gabungkan sebagai catatan ringkas pada modul F bila ruang terbatas.

[Interval prediksi](../04_Visualisasi/svg_plot_cdw2026/20_interval_prediksi_ip4.svg) · [Audit kelompok](../04_Visualisasi/svg_plot_cdw2026/21_audit_prediksi_per_kelompok.svg)

**Metode:** split-conformal menggunakan residual kalibrasi terpisah; q=0,485 poin sebelum pemotongan ke rentang IP 0–4. Sampel 30 interval dipilih acak, bukan contoh terbaik. Cakupan aktual generasi pertama 89,7% (n=448) dan pembanding 91,9% (n=765). Pergeseran antarkohort membatasi jaminan cakupan; bukan kepastian per individu. Dasar metode: [Angelopoulos & Bates](https://arxiv.org/abs/2107.07511).

**Batas:** model hanya menggunakan IP 1–3; ekonomi dan generasi pertama dipakai untuk audit snapshot. Tidak ada prediksi DO, klasifikasi “mahasiswa bermasalah”, atau validasi kesetaraan model. Perbedaan MAE audit masih deskriptif, bukan uji formal diskriminasi.

### H. Alternatif Pendukung: Bantuan Finansial Tidak Menceritakan Semua Kebutuhan

**Isi infografis:**

Di antara generasi pertama ekonomi rendah yang menerima beasiswa, 42,4% tetap bekerja sambil kuliah (224 dari 528). Pada yang tidak menerima beasiswa, proporsinya 54,6% (153 dari 280). Status beasiswa tidak dapat menggantikan pembacaan kebutuhan waktu, dukungan, dan perjalanan akademik.

[Beasiswa dan bekerja](../04_Visualisasi/svg_plot_cdw2026/12_beasiswa_dan_bekerja.svg)

**Batas:** bukan evaluasi efektivitas beasiswa. Besaran bantuan, jam kerja, motivasi bekerja, dan waktu penerimaan tidak diketahui.

## 3. Uji tambahan yang perlu dijaga interpretasinya

Uji interaksi generasi pertama × bekerja ditambahkan pada OLS IPK terakhir dan regresi logistik catatan kegiatan, dengan penyesuaian kondisi serta lama studi. Grafik menunjukkan rata-rata prediksi terstandar pada distribusi kovariat ekonomi rendah yang sama (n=1.111), bukan rata-rata mentah dari empat kelompok dan bukan efek intervensi.

Hasil interaksi OLS: −0,028 poin, CI 95% −0,080 sampai +0,024; p Holm=0,588. Interaksi logistik: OR 0,954, CI 0,709–1,284; p Holm=0,758. Data belum memberi bukti statistik yang cukup bahwa hubungan bekerja berbeda menurut generasi pertama pada skala model yang diuji. Ini bukan bukti kedua pola pasti identik. Interaksi logistik diuji pada skala log-odds, bukan selisih probabilitas.

[Visual uji interaksi](../04_Visualisasi/svg_plot_cdw2026/17_interaksi_bekerja_generasi_pertama.svg)

Jangan mengganti hasil tersebut dengan klaim “beban bekerja terbukti berlipat pada generasi pertama”. Empat kelompok deskriptif tetap relevan, tetapi label “beban berlipat” membutuhkan bukti berbeda.

## 4. Susunan poster yang paling disarankan

Untuk satu halaman, gunakan lima panel analisis, bukan seluruh sembilan visual tambahan:

1. **Perkembangan:** modul A; hasil D sebagai callout +0,08 dengan label outcome IP semester 4 yang jelas.
2. **Kesenjangan capaian:** modul B dan C, dua hasil terpisah dalam satu area; prioritaskan dumbbell dan dua angka model ringkas.
3. **Profil kebutuhan:** modul E, tiga kartu profil atau heatmap yang disederhanakan; tonjolkan 58,6% generasi pertama pada C2.
4. **Kategori ekonomi bukan seluruh cerita:** pecahan modul E; stacked bar C2 dan callout 57,4% menengah/tinggi. Bila sempit, gabungkan dengan panel 3.
5. **Prediksi yang diuji, bukan vonis:** modul F; cakupan 91,1% dan audit MAE modul G sebagai catatan. Ini penghubung ke prototype, bukan solusi yang sudah terbukti efektif.

Modul H dan visual interaksi menjadi alternatif bila ingin menonjolkan bekerja/beasiswa. Grafik validasi clustering, scatter prediksi, rincian CI, dan semua uji dapat ditautkan melalui QR ke notebook. Jangan menumpuk tiga forest plot, heatmap, scatter, dan interval pada poster yang sama. Nomor file adalah urutan aset, bukan urutan baca wajib.

Sebagai usulan desain, bukan perubahan aturan lomba: header 10%, latar 8%, pembahasan 15%, analisis 42%, strategi 8%, solusi 12%, penutup/sumber 5%. Jika ketentuan lomba menetapkan pembagian tertentu, ikuti ketentuan tersebut. Latar belakang tetap ikon+teks; modeling mulai muncul setelah konteks pembaca terbentuk.

## 5. Bridging menuju PETA dan JEMBATAN

**Judul:** Dari Angka Menuju Pendampingan—Bukan Pelabelan.

**Naskah siap pakai:**

Perkembangan akademik perlu dibaca bersama kondisi mahasiswa. Kategori ekonomi belum merangkum seluruh kebutuhan, dan prediksi nilai tetap memiliki ketidakpastian. Karena itu, data sebaiknya menjadi awal percakapan, bukan dasar vonis. JEMBATAN mengusulkan pendampingan melalui PETA: petakan kebutuhan, evaluasi perkembangan, tautkan dukungan, dan audit hasil.

**Konsekuensi bagi prototipe:** clustering sebagai ringkasan kelompok layanan, bukan skor kelayakan bantuan; riwayat dan interval sebagai bahan diskusi pembimbing, bukan ambang hukuman; rujukan setelah konfirmasi mahasiswa; audit kesalahan, akses layanan, dan tindak lanjut. Jangan menggunakan status generasi pertama untuk menolak bantuan, mengurangi kesempatan, atau melabeli individu.

**Visual strategi:** gunakan flow PETA yang sudah ada, lalu mockup JEMBATAN. PETA bukan subbagian analisis statistik.

[PETA](../04_Visualisasi/svg_plot_cdw2026/09_strategi_peta.svg) · [Mockup JEMBATAN](../04_Visualisasi/svg_plot_cdw2026/10_mockup_jembatan.svg)

## 6. Status implementasi

Notebook visualisasi ditambah bagian 13–17: dua spesifikasi clustering, validasi pemisahan/stabilitas/sensitivitas, uji outcome dengan koreksi Holm, interaksi, seleksi model prediksi, holdout lintas angkatan, bootstrap perbaikan MAE, interval split-conformal, dan audit kelompok. Sembilan visual baru diekspor ke SVG, PNG, PNG transparan, dan PDF. Visual lama tetap ada; preview A3 lama tidak otomatis menjadi layout baru. CSV yang diekspor berupa agregat, tanpa ID mahasiswa. Notebook eksplorasi asli tidak diubah.

Semua hasil merupakan analisis eksploratif pada data simulasi. Penggunaan nyata membutuhkan data bertanggal, konfirmasi definisi variabel, persetujuan pemrosesan data, validasi prospektif, serta pembimbing yang bertanggung jawab atas tindak lanjut.
