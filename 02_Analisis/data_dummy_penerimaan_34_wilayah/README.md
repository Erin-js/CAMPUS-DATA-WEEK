# Data dummy penerimaan dan mahasiswa aktif

Seluruh catatan orang, identitas, pilihan prodi, hasil seleksi, registrasi, dan status aktif dalam folder ini merupakan simulasi untuk latihan analisis. Data ini bukan hasil penerimaan resmi dan tidak mengukur peluang lolos nyata.

## Isi folder

| Berkas | Jumlah baris | Arti satu baris |
|---|---:|---|
| 1_pendaftar_penerimaan.csv | 15,308 | Satu pendaftaran pada satu jalur dan tahun; orang bisa berulang. |
| 2_hasil_seleksi_daftar_ulang.csv | 15,308 | Satu hasil seleksi untuk setiap pendaftaran, termasuk yang tidak diterima. |
| 3_mahasiswa_aktif.csv | 3,996 | Satu mahasiswa aktif pada snapshot 1 Oktober 2025. |
| 4_ref_program_studi.csv | 44 | Satu program studi. |
| 5_ref_wilayah_34.csv | 34 | Satu kelompok provinsi dalam klasifikasi latihan 34 wilayah. |

Jumlah calon mahasiswa unik: 12,000. Pendaftaran diterima: 5,649; angka ini menghitung pendaftaran, bukan orang unik. Orang diterima unik: 5,547. Orang sudah daftar ulang: 4,601. Mahasiswa aktif: 3,996.

## Format dan cara membaca

- CSV memakai pemisah titik koma (;), pengodean UTF-8 dengan BOM, dan satu baris header.
- Tanggal menggunakan YYYY-MM-DD. Sel kosong berarti tidak berlaku atau tidak tersedia sesuai kamus; bukan nol.
- Semua kode identitas dan referensi harus dibaca sebagai teks. Semua kode baru bersifat dummy.
- Python/pandas: `pd.read_csv('1_pendaftar_penerimaan.csv', sep=';', encoding='utf-8-sig', dtype={'ID_Pendaftar': str, 'ID_Pendaftaran': str})`.
- Saat membuka di Excel, pilih pemisah titik koma jika kolom tidak langsung terpisah.

## Sumber acuan dan batas penggunaannya

Sumber kategori: ../data/1_profil_mahasiswa_umum.csv, berisi 5,000 baris. Nama 44 prodi, hubungan dengan 15 fakultas, serta kategori jenis kelamin, angkatan dan provinsi berasal dari tabel tersebut. Profil sumber diambil ulang secara acak untuk membentuk kombinasi kategori; ID dan baris orang sumber tidak disalin ke keluaran. Distribusi hasil mendekati referensi, tidak dipaksa identik.

Empat CSV sumber lainnya tidak dipakai sebagai fitur karena skema baru tidak memuat prestasi, generasi pertama kuliah, sosial ekonomi, atau riwayat IPK. Kelima berkas sumber diperiksa hash-nya sebelum dan sesudah pembuatan untuk memastikan tidak berubah.

## Asumsi simulasi

1. Ada 12,000 orang sintetis, tahun penerimaan 2019-2025. Satu orang hanya berada dalam satu tahun penerimaan dan dapat mengikuti paling banyak tiga jalur berurutan: SNBP, SNBT, Mandiri. Peluang jalur awal adalah 30%, 45%, 25%.
2. Nama jalur tersebut hanya label seragam untuk latihan lintas tahun; tidak dimaksudkan sebagai nama historis resmi untuk setiap tahun. Seluruh pendaftaran berstatus Selesai; tidak ada berkas belum lengkap atau hasil tertunda.
3. Peluang simulasi diterima dasar adalah SNBP 25%, SNBT 34%, Mandiri 48%, ditambah variasi acak tetap per prodi antara -6,5 dan +6,5 poin persentase serta variasi tahun sebesar (tahun-2022) x 0,6 poin persentase. Angka-angka ini dipilih untuk membentuk data latihan dan tidak diestimasi dari sumber.
4. Dari peserta diterima, peluang simulasi daftar ulang adalah SNBP 82%, SNBT 86%, Mandiri 76%. Jika belum daftar ulang atau tidak diterima, peluang melanjutkan ke jalur berikutnya adalah 45%. Setelah daftar ulang, orang tidak mengikuti jalur selanjutnya. Satu orang paling banyak memiliki satu NIM.
5. Sekitar 12% pendaftaran tidak memiliki pilihan kedua. Jika diterima dan memiliki pilihan kedua, peluang prodi diterima dialihkan ke pilihan kedua adalah 18%. Proses ini tidak meniru sistem pemeringkatan, kuota, atau mekanisme seleksi resmi.
6. Mahasiswa aktif adalah subset orang yang sudah daftar ulang, diamati pada 1 Oktober 2025, tahun akademik 2025/2026 Ganjil. Peluang aktif menurut selisih tahun 2025-angkatan adalah 98%, 96%, 93%, 88%, 55%, 20%, 8% untuk selisih 0 hingga 6 tahun. Pola ini merupakan asumsi simulasi, bukan tingkat retensi hasil observasi.
7. Tidak muncul di tabel aktif hanya berarti tidak aktif pada snapshot simulasi. Penyebabnya tidak tersedia; jangan otomatis menyimpulkan putus kuliah atau gagal registrasi.
8. Semua prodi diberi jenjang S1 sebagai asumsi latihan karena kolom jenjang tidak ada pada sumber. Prodi mahasiswa aktif sama dengan prodi diterima; perpindahan prodi tidak disimulasikan.
9. Tanggal lahir, sekolah, dan tanggal registrasi disimulasikan. Usia dihitung pada 1 Agustus tahun penerimaan. Tanggal registrasi tidak mewakili jadwal resmi.
10. Seed acak tetap: 20261027. Hasil dapat direproduksi menggunakan skrip pendukung dengan versi Python yang sama.

## Pemetaan 38 kategori provinsi menjadi 34

Nama tabel Ref wilayah 34 ditafsirkan sebagai referensi tingkat provinsi, bukan kabupaten/kota. Sumber memiliki 38 kategori provinsi. Untuk kebutuhan latihan ini:

| Kategori asal referensi | Kelompok dalam dummy |
|---|---|
| Papua Selatan | Papua |
| Papua Tengah | Papua |
| Papua Pegunungan | Papua |
| Papua Barat Daya | Papua Barat |

Kategori lainnya dipertahankan, sehingga terdapat 34 kelompok. Ini hanya pengelompokan latihan berbasis nama kategori, bukan konversi batas wilayah administratif resmi pada tahun tertentu. Kode W34-01 sampai W34-34 dibuat menurut urutan alfabetis, bukan kode BPS atau Kemendagri. Untuk analisis wilayah resmi, ganti dengan referensi dan pemetaan yang sah.

## Hubungan tabel dan penghitungan

- Pendaftar ke hasil seleksi: gabungkan dengan ID_Pendaftaran, hubungan satu-ke-satu. Kedua tabel memuat cakupan pendaftaran yang sama.
- Pendaftar ke orang: ID_Pendaftar berulang lintas jalur. Hitung ID_Pendaftar unik untuk jumlah orang; hitung ID_Pendaftaran untuk jumlah pendaftaran. Jumlah pendaftar per jalur tidak boleh dijumlahkan sebagai orang unik seluruh jalur.
- Hasil seleksi ke mahasiswa aktif: gunakan NIM atau ID_Pendaftaran. Orang yang sudah registrasi tetapi tidak aktif tetap memiliki NIM pada tabel hasil seleksi.
- Kode_Prodi_Pilihan_1, Kode_Prodi_Pilihan_2, Kode_Prodi_Diterima dan Kode_Prodi mengacu pada Kode_Prodi tabel referensi. Artinya berbeda; pilih yang sesuai pertanyaan analisis.
- Kode_Wilayah_Asal mengacu pada Kode_Provinsi tabel wilayah.
- Untuk alur berbasis orang, gunakan orang mendaftar unik, orang diterima unik, orang daftar ulang unik, kemudian orang aktif pada angkatan yang sama. Jangan mencampurkan hitungan pendaftaran dengan hitungan orang.
- Untuk melihat cakupan lengkap hingga aktif, gunakan penggabungan kiri dari pendaftaran. Penggabungan dalam ke tabel aktif hanya mempertahankan mahasiswa aktif.

## Dokumentasi dan pemeriksaan

KAMUS_DATA.md menjelaskan seluruh kolom, tipe, kunci dan arti nilai kosong. _pendukung/hasil_pemeriksaan.json menyimpan jumlah baris, ringkasan per tahun, hash sumber/keluaran, dan 20 pemeriksaan konsistensi yang semuanya lulus. Skrip _pendukung/buat_dummy_penerimaan.py disertakan agar simulasi dapat ditinjau; jalankan dengan `--output` menuju folder baru jika ingin mengulang.
