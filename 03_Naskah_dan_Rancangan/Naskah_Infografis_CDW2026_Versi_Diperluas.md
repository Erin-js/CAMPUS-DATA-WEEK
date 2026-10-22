# Rancangan Isi Infografis CDW 2026 — Versi Diperluas

Analisis inti diringkas menjadi enam subbagian. Bagian solusi memakai nama PIJAR dan dilengkapi usulan fitur serta analisis SWOT. Cakupan angka “1 dari 4”, jenis nilai, dan status solusi sebagai usulan prototipe tetap diperjelas. Dokumen acuan, notebook, dan aset visual tidak diubah dalam revisi naskah ini.

## Bagian I: Latar Belakang

### Sub-Judul: Kuliah dengan Latar Keluarga yang Berbeda

**Prelude:**

Mahasiswa generasi pertama kuliah adalah mahasiswa yang kedua orang tuanya belum pernah menempuh pendidikan tinggi.

Untuk memahami capaian mereka, IPK terakhir saja belum cukup. Kondisi ekonomi, aktivitas bekerja, dan perkembangan selama kuliah juga perlu diperhatikan.

**Data:** —

**Link:** —

**Visualisasi:** teks + ikon SDGs. Tanpa grafik data, mengikuti rancangan awal.

## Bagian II: Pembahasan

### Sub-Judul: Melihat Generasi Pertama Kuliah

**Prelude:**

38,5% mahasiswa merupakan generasi pertama kuliah. Sebanyak 1.924 dari 5.000 mahasiswa termasuk kelompok ini.

72,7% mahasiswa ekonomi rendah merupakan generasi pertama kuliah. Jumlahnya mencapai 808 dari 1.111 mahasiswa.

46,7% generasi pertama kuliah dari ekonomi rendah bekerja sambil kuliah. Sebanyak 377 dari 808 mahasiswa menjalani kedua aktivitas tersebut.

Pendidikan orang tua, ekonomi, dan aktivitas bekerja dapat hadir bersamaan dalam kehidupan seorang mahasiswa.

**Data:** tiga angka utama beserta jumlah mahasiswa dalam prelude.

**Link:** [Angka konteks](../04_Visualisasi/svg_plot_cdw2026/01_konteks_angka_besar.svg)

**Visualisasi:** teks + ikon; acuan plot `01_konteks_angka_besar`. Tiga kartu angka, masing-masing memuat persentase dan penyebutnya.

### Sub-Judul: Generasi Pertama Kuliah, Kondisi Ekonomi Berbeda

**Prelude:**

Sebanyak 42,0% mahasiswa generasi pertama kuliah berada pada ekonomi rendah, dibandingkan 9,9% pada kelompok bukan generasi pertama. Sebaliknya, proporsi ekonomi tinggi lebih kecil: 6,3% dibandingkan 36,1%. Perbedaan ini memberi konteks sebelum kita melihat capaian mahasiswa dalam kategori ekonomi yang sama.

**Data:**

| Kelompok mahasiswa | Jumlah | Ekonomi rendah | Ekonomi menengah | Ekonomi tinggi |
| --- | ---: | ---: | ---: | ---: |
| Generasi pertama kuliah | 1.924 | 42,0% | 51,7% | 6,3% |
| Bukan generasi pertama kuliah | 3.076 | 9,9% | 54,0% | 36,1% |

*Catatan kecil: persentase dihitung di dalam masing-masing kelompok, berbeda dari angka 72,7% yang dihitung dari seluruh mahasiswa ekonomi rendah.*

**Link:** [Komposisi ekonomi kedua kelompok](../04_Visualisasi/svg_plot_cdw2026/02_ekonomi_stacked_100.svg)

**Visualisasi:** horizontal stacked bar 100% `02_ekonomi_stacked_100`. Tampilkan komposisi ekonomi rendah, menengah, dan tinggi pada kedua kelompok beserta jumlah mahasiswanya.

### Sub-Judul: Ekonomi Sama, Capaian Berbeda

**Prelude:**

Di dalam kelompok ekonomi rendah, perbedaan capaian terlihat ketika status generasi pertama kuliah dan aktivitas bekerja dipertimbangkan secara bersamaan.

Pada generasi pertama ekonomi rendah yang bekerja, sekitar 1 dari 4 berstatus cuti atau nonaktif/DO.

*Catatan kecil: angka ini menunjukkan status yang tercatat, bukan prediksi DO.*

**Data:**

| Kelompok mahasiswa ekonomi rendah | Jumlah | Rata-rata IPK terakhir | Ada catatan prestasi/kegiatan | Cuti atau nonaktif/DO |
| --- | ---: | ---: | ---: | ---: |
| Bukan generasi pertama, tidak bekerja | 204 | 3,29 | 60,8% | 7,4% |
| Bukan generasi pertama, bekerja | 99 | 3,18 | 48,5% | 14,1% |
| Generasi pertama, tidak bekerja | 431 | 3,03 | 42,5% | 15,3% |
| Generasi pertama, bekerja | 377 | 2,81 | 28,6% | 25,5% |

**Link:** [Matriks irisan ekonomi rendah](../04_Visualisasi/svg_plot_cdw2026/05_matriks_irisan_2x2.svg)

**Visualisasi:** box/tabel 2×2, mengikuti plot `05_matriks_irisan_2x2`. Empat kartu kelompok dengan posisi dan indikator yang konsisten.

## Bagian II: Analisis Inti

### 1. Sub-Judul: Dari Semester Awal, Kemajuan Mulai Terlihat

**Prelude:**

Pada 3.603 mahasiswa dengan catatan semester 1 dan 4, generasi pertama menunjukkan kenaikan IPK lebih besar. Mereka memulai lebih rendah, tetapi berkembang lebih banyak—meski selisih nilai belum hilang.

**Data:**

| Kelompok | IPK kumulatif semester 1 | IPK kumulatif semester 4 | Kenaikan IPK |
| --- | ---: | ---: | ---: |
| Generasi pertama kuliah | 2,68 | 3,03 | +0,35 |
| Bukan generasi pertama kuliah | 3,16 | 3,34 | +0,19 |

*Catatan kecil: mahasiswa yang dibandingkan sama pada kedua semester; generasi pertama n=1.345 dan pembanding n=2.258. Nilai merupakan rata-rata IPK kumulatif, bukan IP tiap semester.*

**Link:** [Lintasan semester 1–4](../04_Visualisasi/svg_plot_cdw2026/13_lintasan_semester_1_4.svg)

**Visualisasi:** line chart `13_lintasan_semester_1_4`. Alternatif ringkas: slope chart `04_slope_ipk_kohort_tetap`. Pilih satu; sorot kenaikan +0,35 dan +0,19.

### 2. Sub-Judul: Nilai Akhir Belum Menceritakan Seluruh Perkembangan

**Prelude:**

Setelah perbedaan kondisi mahasiswa diperhitungkan, generasi pertama kuliah masih memiliki IPK terakhir lebih rendah dan catatan kegiatan cenderung lebih jarang ditemukan. Namun, ketika nilai awal ikut diperhitungkan, IP semester 4 mereka sedikit lebih tinggi. Nilai akhir dan perkembangan dari semester awal perlu dilihat bersama.

**Isi tiga kartu untuk infografis:**

**IPK terakhir lebih rendah 0,24 poin**  
Perbedaan masih terlihat setelah kondisi mahasiswa dan lama studi diperhitungkan.

**Catatan prestasi/kegiatan cenderung lebih jarang ditemukan**  
Pola ini tetap terlihat setelah perbedaan kondisi mahasiswa diperhitungkan. Catatan mencakup peserta, finalis, dan juara.

**IP semester 4 lebih tinggi 0,08 poin**  
Hasil ini muncul setelah nilai semester pertama, angkatan, dan kondisi lain diperhitungkan.

**Makna utama:** IPK terakhir yang lebih rendah belum menceritakan seluruh perkembangan generasi pertama kuliah.

**Data pendukung, bukan teks utama poster:**

| Perbandingan dengan mahasiswa bukan generasi pertama | Perkiraan model | Rentang ketidakpastian (CI 95%) | Jumlah mahasiswa |
| --- | ---: | --- | ---: |
| Selisih IPK terakhir, setelah penyesuaian kondisi dan lama studi | −0,24 poin | −0,27 sampai −0,22 | 5.000 |
| Perbandingan odds memiliki catatan prestasi/kegiatan, setelah penyesuaian kondisi dan lama studi | OR 0,50 | 0,43–0,58 | 5.000 |
| Selisih IP semester 4, setelah nilai semester pertama, angkatan, dan kondisi lain diperhitungkan | +0,08 poin | +0,06 sampai +0,11 | 3.603 |

**Panduan istilah jika angka statistik ditampilkan:**

- **Odds** membandingkan kemungkinan memiliki catatan kegiatan dengan kemungkinan tidak memilikinya. **OR** membandingkan odds tersebut antara dua kelompok. OR 0,50 berarti odds pada generasi pertama sekitar separuh kelompok pembanding, bukan berarti persentase mahasiswa yang memiliki catatan kegiatan turun 50%.
- **CI 95%** adalah rentang ketidakpastian perkiraan model. Misalnya, selisih IPK diperkirakan −0,24 poin, dengan rentang −0,27 sampai −0,22. Rentang ini bukan nilai IPK setiap mahasiswa.

*Catatan kecil untuk poster: IPK adalah nilai kumulatif, sedangkan IP semester 4 adalah nilai satu semester. Ketiga hasil menggunakan perbandingan yang berbeda dan menunjukkan hubungan, bukan sebab-akibat. Tidak adanya catatan kegiatan belum tentu berarti mahasiswa tidak aktif.*

**Link:** [Notebook visualisasi](../02_Analisis/Visualisasi_Infografis_CDW2026.ipynb)

**Visualisasi:** tiga kartu dengan bahasa sehari-hari sesuai teks di atas. Sorot **−0,24 poin IPK terakhir**, **catatan kegiatan cenderung lebih jarang ditemukan**, dan **+0,08 poin IP semester 4**. Gunakan angka dari `06_forest_ipk_terkontrol`, `07_forest_odds_prestasi`, dan `08_forest_ip_semester4_baseline`. OR dan CI disimpan sebagai data pendukung; jika tetap ditampilkan, tempatkan panduan istilah singkat sebelum visual. Jangan mengubah OR 0,50 menjadi headline “peluang turun 50%”.

### 3. Sub-Judul: Menerima Beasiswa, Tetap Menjalani Dua Peran

**Prelude:**

Di antara generasi pertama ekonomi rendah penerima beasiswa, lebih dari 4 dari 10 tetap bekerja sambil kuliah. Bantuan tercatat, tetapi dua peran masih berjalan. Status beasiswa saja belum menceritakan seluruh kebutuhan mereka.

**Data:**

| Generasi pertama ekonomi rendah | Jumlah mahasiswa | Bekerja sambil kuliah | Proporsi bekerja |
| --- | ---: | ---: | ---: |
| Menerima beasiswa | 528 | 224 | 42,4% |
| Tidak menerima beasiswa | 280 | 153 | 54,6% |

*Catatan kecil: bukan uji efektivitas beasiswa. Besaran bantuan, jam kerja, alasan bekerja, dan waktu penerimaan tidak diketahui.*

**Link:** [Beasiswa dan aktivitas bekerja](../04_Visualisasi/svg_plot_cdw2026/12_beasiswa_dan_bekerja.svg)

**Visualisasi:** horizontal bar chart `12_beasiswa_dan_bekerja`. Sorot 42,4%, dengan jumlah 224 dari 528 mahasiswa. Hindari panah yang menyiratkan beasiswa menyebabkan penurunan bekerja.

### 4. Sub-Judul: Generasi Pertama, Beragam Kebutuhan

**Prelude:**

Clustering merangkum tiga profil kondisi mahasiswa; proporsi generasi pertama terbesar ada pada profil finansial. Namun, lebih dari separuh anggota profil itu bukan dari ekonomi rendah. Kebutuhan tidak selalu mengikuti label ekonomi.

**Data:**

| Profil dari clustering 5.000 mahasiswa | Jumlah | Generasi pertama | Bekerja | Rata-rata dukungan keluarga, skala 1–5 |
| --- | ---: | ---: | ---: | ---: |
| C1: bekerja; kendala utama selain finansial | 663 | 42,8% | 100,0% | 3,3 |
| C2: kendala utama finansial; status bekerja beragam | 1.648 | 58,6% | 34,3% | 2,9 |
| C3: tidak bekerja; kendala utama selain finansial | 2.689 | 25,1% | 0,0% | 3,6 |

Sorotan C2: **966 dari 1.648 mahasiswa merupakan generasi pertama (58,6%)**. Pada seluruh anggota C2, **946 mahasiswa berada pada ekonomi menengah atau tinggi (57,4%)**.

Metode: hierarchical average linkage dengan jarak Gower; fitur ekonomi, bekerja, dukungan keluarga, tanggungan, dan kendala utama. Validasi internal: silhouette 0,347; median ARI 1,000 pada empat subsampel 70%.

*Catatan kecil: generasi pertama, beasiswa, IPK, prestasi, dan status akademik tidak membentuk cluster. Profil bersifat eksploratif dan sensitif terhadap pilihan fitur, bukan label risiko. Komposisi ekonomi C2 mencakup seluruh anggotanya, bukan hanya generasi pertama. Kendala utama selain finansial bukan berarti bebas kesulitan finansial.*

**Link:** [Profil kebutuhan mahasiswa](../04_Visualisasi/svg_plot_cdw2026/15_heatmap_profil_kebutuhan.svg) · [Komposisi profil finansial](../04_Visualisasi/svg_plot_cdw2026/22_cluster_kendala_finansial.svg)

**Visualisasi:** tiga kartu profil, memakai data `15_heatmap_profil_kebutuhan`, dengan sorotan **58,6% generasi pertama pada C2**. Tambahkan satu callout **“57,4% anggota C2 bukan kategori ekonomi rendah”**, mengambil angka dari `22_cluster_kendala_finansial`. Tidak perlu memasang heatmap dan stacked bar penuh sekaligus; validasi `14_validasi_clustering_gower` tetap di notebook.

### 5. Sub-Judul: Prediksi Membantu, Bukan Menentukan

**Prelude:**

Riwayat nilai membantu memperkirakan IP semester berikutnya, tetapi kesalahannya lebih besar pada generasi pertama. Prediksi perlu dibaca bersama ketidakpastiannya—sebagai bahan percakapan dengan pembimbing, bukan stempel kemampuan mahasiswa.

**Data:**

| Pendekatan pada angkatan uji 2024, n=1.213 | Rata-rata kesalahan absolut / MAE |
| --- | ---: |
| Menggunakan IP semester 3 sebagai prediksi | 0,272 poin |
| Menggunakan rata-rata IP semester 1–3 | 0,280 poin |
| Ridge, dipilih melalui validasi | 0,229 poin |

Pengurangan MAE terhadap baseline IP semester 3: **15,7%**, atau **0,043 poin**; CI bootstrap 95% **0,033–0,052 poin**.

Audit kesalahan: generasi pertama **0,249 poin (n=448)**; pembanding **0,217 poin (n=765)**. Interval dengan target cakupan 90% memuat **91,1% nilai aktual** pada seluruh angkatan uji.

*Catatan kecil: fitur hanya IP 1–3. Model dipilih pada validasi 2022, dilatih ulang pada 2019–2022, dikalibrasi pada 2023, dan diuji pada 2024. Ini pengujian retrospektif, bukan prediksi DO. Perbedaan MAE bersifat deskriptif; cakupan interval bukan jaminan per individu atau angkatan berikutnya.*

**Link:** [Evaluasi prediksi IP](../04_Visualisasi/svg_plot_cdw2026/18_prediksi_ip_evaluasi_baseline.svg) · [Audit kelompok](../04_Visualisasi/svg_plot_cdw2026/21_audit_prediksi_per_kelompok.svg)

**Visualisasi:** bar MAE `18_prediksi_ip_evaluasi_baseline` sebagai grafik utama, dengan keterangan “lebih kecil berarti kesalahan lebih kecil”. Audit generasi pertama dan pembanding ditampilkan sebagai dua angka kecil dari `21_audit_prediksi_per_kelompok`; cakupan 91,1% menjadi catatan. Scatter `19_prediksi_vs_aktual_ip4` dan interval `20_interval_prediksi_ip4` tetap sebagai detail notebook.

### 6. Sub-Judul: Pendampingan yang Memahami Kondisi Mahasiswa

**Prelude:**

Perkembangan, kondisi, dan batas prediksi perlu dibaca bersama. Temuan ini menjadi dasar usulan PIJAR: memakai data sebagai awal percakapan, lalu menghubungkan kebutuhan yang dikonfirmasi mahasiswa dengan dukungan melalui PETA.

**Data:** —; PETA adalah kerangka strategi yang diusulkan, bukan hasil evaluasi program.

| PETA | Arah pendampingan |
| --- | --- |
| Petakan kebutuhan | Baca ekonomi, bekerja, dan dukungan keluarga bersama-sama. |
| Evaluasi perkembangan | Perhatikan perubahan nilai sejak semester awal. |
| Tautkan dukungan | Hubungkan kebutuhan yang dikonfirmasi dengan layanan tersedia. |
| Audit hasil | Pantau akses layanan, tindak lanjut, dan kesalahan prediksi antarkelompok. |

**Link:** [Strategi PETA](../04_Visualisasi/svg_plot_cdw2026/09_strategi_peta.svg)

**Visualisasi:** logo/ikon + empat langkah `09_strategi_peta`. Jadikan jembatan dari analisis menuju solusi, bukan grafik statistik tambahan.

## Bagian III: Solusi

### Sub-Judul: PIJAR — Kenali Kebutuhan, Dampingi Perjalanan

**Prelude:**

PIJAR diusulkan sebagai prototipe pendampingan mahasiswa generasi pertama kuliah. Seperti pijar yang menerangi langkah, data membantu memahami kebutuhan dan perkembangan—agar mahasiswa tidak harus mencari arah sendirian.

Mahasiswa perlu dipahami berdasarkan perjalanan, tantangan, dan kemajuan akademiknya.

**Data:** —; usulan prototipe, belum merupakan aplikasi operasional atau intervensi yang terbukti efektif.

**Link:** [Acuan mockup PIJAR — aset masih memakai nama lama](../04_Visualisasi/svg_plot_cdw2026/10_mockup_jembatan.svg)

**Visualisasi:** gunakan tata letak mockup `10_mockup_jembatan` sebagai acuan, lalu ganti identitas yang terlihat menjadi **PIJAR** saat mendesain infografis. Beri label “Usulan Prototipe”. Empat fungsi utamanya dijabarkan di bawah. Clustering dan prediksi tidak digunakan sebagai skor kelayakan bantuan atau vonis individu.

### Sub-Judul: Empat Fitur, Satu Perjalanan Pendampingan

**Prelude:**

Pendampingan tidak berhenti saat kebutuhan ditemukan. PIJAR dirancang agar mahasiswa dapat menceritakan kondisinya, membaca perkembangan, menemukan dukungan, dan mengetahui tindak lanjutnya—dengan keputusan tetap dibicarakan bersama pendamping.

**Data:** —; rancangan fitur, belum diimplementasikan atau diuji kepada pengguna.

| Fitur | Isi yang diusulkan | Manfaat yang dituju |
| --- | --- | --- |
| **Ceritakan Kondisimu** | Ringkasan ekonomi, beasiswa, aktivitas bekerja, dan dukungan keluarga; mahasiswa dapat mengonfirmasi atau memperbarui informasi. Profil clustering hanya membantu membuka percakapan. | Kebutuhan dibaca bersama, bukan ditebak dari satu label ekonomi. |
| **Lihat Perjalananmu** | Riwayat IP tiap semester dan IPK kumulatif dengan label berbeda; prediksi IP berikutnya ditampilkan terpisah dari nilai aktual, beserta ketidakpastian jika metode yang sesuai tersedia. | Kemajuan terlihat tanpa mengubah prediksi menjadi penilaian kemampuan. |
| **Temukan Dukunganmu** | Direktori layanan kampus: konsultasi bantuan biaya, pendampingan akademik, konseling, atau peluang kegiatan. Rujukan dibuat setelah kebutuhan dikonfirmasi mahasiswa dan layanan diperiksa ketersediaannya. | Mahasiswa lebih mudah mengetahui pintu bantuan yang relevan. |
| **Lanjutkan Langkahmu** | Status rujukan—diajukan, dijadwalkan, selesai, atau perlu tindak lanjut—disertai pengingat dan umpan balik mahasiswa. Pendamping memantau akses layanan secara agregat. | Rujukan tidak berhenti sebagai rekomendasi di layar. |

*Catatan kecil: persetujuan mahasiswa, pembatasan akses berdasarkan peran, dan kesempatan mengoreksi data menjadi rancangan lintas fitur. Informasi sensitif tidak ditampilkan pada ringkasan publik. Kelayakan bantuan mengikuti prosedur layanan terkait, bukan hasil cluster atau prediksi.*

**Link:** acuan empat fungsi pada [mockup yang tersedia](../04_Visualisasi/svg_plot_cdw2026/10_mockup_jembatan.svg); kartu rincian fitur belum dibuat di notebook.

**Visualisasi:** empat kartu fitur dengan ikon **percakapan → lintasan nilai → penunjuk arah → checklist**. Hubungkan dengan alur **“Konfirmasi kebutuhan → sepakati rujukan → pantau tindak lanjut”**. Gunakan nama fitur sebagai judul kartu dan satu kalimat manfaat; tabel di atas menjadi bank isi, bukan seluruhnya dipasang pada poster.

### Sub-Judul: Membaca Potensi, Menjaga Batas

**Prelude:**

PIJAR menawarkan pendampingan yang lebih utuh, tetapi aplikasi saja tidak menghilangkan hambatan. SWOT memetakan potensi dan batasnya: dukungan harus tersedia, data perlu dijaga, dan manfaatnya masih harus dibuktikan.

**Data:** —; SWOT kualitatif atas rancangan prototipe. Kekuatan dan peluang merupakan potensi, bukan hasil evaluasi efektivitas.

| Aspek SWOT | Analisis PIJAR | Implikasi untuk pengembangan |
| --- | --- | --- |
| **Strengths — Kekuatan** | Menghubungkan kondisi ekonomi, perjalanan akademik, rujukan, dan tindak lanjut dalam satu alur. Kebutuhan dikonfirmasi mahasiswa, bukan ditentukan model. | Pertahankan alur yang mudah dipahami dan menempatkan mahasiswa sebagai mitra pendampingan. |
| **Weaknesses — Kelemahan** | Model masih berbasis data simulasi; integrasi layanan dan manfaat pendampingan belum diuji. Riwayat nilai tidak menjelaskan seluruh alasan kesulitan mahasiswa. | Mulai dari fitur inti dan percakapan pendamping; validasi data serta model sebelum penggunaan nyata. |
| **Opportunities — Peluang** | Dapat menjadi penghubung layanan kampus yang tersedia dan membuka ruang kolaborasi mahasiswa sains data dengan dosen wali serta unit kemahasiswaan. | Uji coba pada lingkup kecil bersama pengguna dan pengelola layanan; pastikan jalur rujukan benar-benar aktif. |
| **Threats — Ancaman** | Kebocoran informasi sensitif, stigmatisasi generasi pertama, dan prediksi yang diperlakukan sebagai vonis. Antrean layanan atau akses digital terbatas dapat membuat rujukan tidak terjangkau. | Batasi akses data, audit kesalahan antarkelompok, sediakan jalur pendampingan non-digital, dan pantau kapasitas layanan. |

**Link:** —; analisis SWOT disusun untuk rancangan PIJAR, bukan keluaran pemodelan notebook.

**Visualisasi:** matriks SWOT 2×2 dengan empat ikon: **mata rantai** (kekuatan), **alat perbaikan** (kelemahan), **pintu terbuka** (peluang), dan **perisai** (ancaman). Isi ringkas tiap kotak: **“Kebutuhan hingga tindak lanjut terhubung”**, **“Data simulasi; manfaat belum teruji”**, **“Kolaborasi dengan layanan kampus”**, dan **“Privasi, stigma, serta keterjangkauan layanan”**. Tidak perlu radar chart atau skor numerik karena SWOT belum diukur.

**Penutup solusi:** Mulai dari uji coba kecil: apakah mahasiswa memahami fitur, rujukan dapat diakses, dan tindak lanjut benar-benar terjadi? Pantau keberhasilan mengakses layanan, waktu tunggu, serta umpan balik—bukan hanya akurasi prediksi. Kenaikan IPK saja belum membuktikan dampak PIJAR tanpa evaluasi pembanding yang memadai.

## Catatan sumber untuk footer

Sumber: lima CSV CDW 2026, diolah dalam `Visualisasi_Infografis_CDW2026.ipynb`. Data fiktif/simulasi; bukan gambaran seluruh mahasiswa Indonesia. Hasil bersifat observasional atau eksploratif dan tidak menunjukkan sebab-akibat. Catatan kegiatan mencakup peserta, bukan hanya juara; cuti/nonaktif/DO adalah status yang tercatat, bukan prediksi.

## Catatan penyusunan, bukan teks utama infografis

- Analisis inti berisi enam subbagian. Untuk satu poster, gunakan satu visual dominan per subbagian; bagian solusi cukup satu mockup, empat kartu fitur ringkas, dan matriks SWOT kecil. Tabel fitur dan SWOT merupakan bank isi untuk memilih teks yang sesuai ruang.
- Nama solusi dalam naskah adalah PIJAR. Aset `10_mockup_jembatan` masih memakai nama lama; identitas visual perlu diganti saat penyusunan infografis. Revisi ini tidak mengubah notebook atau berkas SVG tersebut.
- Angka IPK, OR, dan IP semester 4 pada subbagian 2 memiliki target dan kelompok analisis berbeda; jangan dibaca sebagai hasil yang saling membatalkan.
- Validasi clustering sensitif terhadap pilihan fitur. Spesifikasi awal dengan beasiswa menghasilkan pemisahan status beasiswa; spesifikasi kebutuhan utama kemudian mengeluarkan beasiswa, perubahan eksploratif setelah diagnostik. ARI antara spesifikasi utama dan yang menambahkan beasiswa hanya 0,071. Kendala utama dan bekerja sangat menentukan profil, sehingga jangan menyebutnya tipe mahasiswa tersembunyi atau diagnosis otomatis.
- Tidak ditambahkan headline “beban bekerja terbukti berlipat pada generasi pertama”: uji interaksi IPK dan logistik belum mendukungnya. Rincian ada pada plot `17_interaksi_bekerja_generasi_pertama`.
- Bukti pemodelan tersimpan dalam notebook dan [pengembangan analisis](Pengembangan_Analisis_Inti_CDW2026.md). Semua angka tambahan ditinjau terhadap tabel hasil yang sudah diekspor; tidak dilakukan pemodelan ulang untuk naskah ini.
