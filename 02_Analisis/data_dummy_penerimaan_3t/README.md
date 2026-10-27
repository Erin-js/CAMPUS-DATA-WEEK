# Data dummy penerimaan: revisi referensi wilayah 3T

Gunakan folder ini untuk latihan struktur sesuai gambar final. Folder data_dummy_penerimaan_34_wilayah adalah versi lama dan tidak mengikuti struktur final. Semua data hasil seleksi, registrasi, sekolah, kabupaten/kota, kode dan status 3T merupakan simulasi. Dataset ini bukan data resmi dan tidak untuk menetapkan kondisi wilayah nyata.

## Struktur sesuai gambar

| Berkas | Unit baris | Kunci | Jumlah baris |
|---|---|---|---:|
| 1_pendaftar_penerimaan.csv | Satu pendaftar | ID_Pendaftar | 12,000 |
| 2_hasil_seleksi_daftar_ulang.csv | Satu pendaftar yang diterima | ID_Pendaftar | 5,547 |
| 3_mahasiswa_aktif.csv | Satu mahasiswa yang sudah daftar ulang | ID_Mahasiswa | 4,601 |
| 4_ref_program_studi.csv | Satu prodi pada satu tahun | Kode_Prodi + Tahun_Penerimaan | 308 |
| 5_ref_wilayah_3t.csv | Satu kabupaten/kota | Kode_Wilayah | 304 |

## Arti ref_wilayah_3t

Tabel ini diasumsikan sebagai referensi kabupaten/kota beserta Status_3T, bukan daftar individu pendaftar. Hubungkan Kode_Wilayah_Asal pada pendaftar/mahasiswa dengan Kode_Wilayah referensi, kemudian bandingkan Status_3T = Ya dan Tidak. Kehadiran kedua kategori dipilih agar latihan perbandingan dapat dilakukan. Apakah tabel final memuat semua wilayah atau hanya wilayah 3T belum dapat dipastikan dari gambar; ikuti kamus final saat tersedia.

Terdapat 304 kabupaten/kota fiktif, delapan untuk setiap 38 kategori provinsi sumber. Dua dari delapan wilayah per provinsi diberi label Ya secara acak, sehingga 76 wilayah berlabel 3T dan 228 non-3T. Seluruh nama kabupaten/kota memuat kata Dummy; label 3T tidak berasal dari penetapan pemerintah. Tidak ada pengaruh 3T yang sengaja ditambahkan pada peluang seleksi atau registrasi. Perbedaan hasil antarlabel dalam dummy tidak boleh dianggap bukti ketimpangan nyata.

Nama 38 provinsi diambil dari 1_profil_mahasiswa_umum.csv. Pemetaan 34 wilayah lama dihentikan. Untuk orang yang sebelumnya masuk kelompok Papua/Papua Barat, kategori provinsi dipilih ulang dari kategori sumber yang dahulu digabung, mengikuti frekuensinya. Asal kabupaten/kota seluruh orang ditetapkan secara sintetis. Data ini mendukung latihan penggabungan dan clustering indikator wilayah; analisis peta lokasi nyata membutuhkan referensi geografis yang benar.

## Perubahan dari dummy sebelumnya

1. Tabel 1 sekarang tepat 12.000 pendaftar unik. ID_Pendaftaran dihapus. Untuk orang dengan beberapa jalur lama, dipilih pendaftaran yang berhasil daftar ulang; jika tidak ada, pendaftaran terakhir yang diterima; jika tidak ada, pendaftaran terakhir. Ini aturan konversi latihan, bukan mekanisme seleksi resmi. Jumlah jalur asal tidak lagi dapat dianalisis sebagai seluruh riwayat pendaftaran.
2. Tabel 2 hanya berisi 5,547 peserta diterima. Semua ID_Pendaftar unik; peserta tidak diterima tidak memiliki baris di tabel ini. Status_Daftar_Ulang membedakan Sudah dan Tidak Daftar Ulang.
3. Tabel 3 berisi seluruh 4,601 orang yang sudah daftar ulang, sesuai unit pada gambar. Kuncinya ID_Mahasiswa. Nama berkas tetap mahasiswa_aktif agar mengikuti acuan, tetapi tabel ini tidak boleh langsung dihitung sebagai seluruh mahasiswa berstatus aktif. Gunakan filter Status_Mahasiswa = Aktif untuk mendapatkan 3,996 orang aktif pada snapshot 1 Oktober 2025. Penyebab status lain tidak dapat disimpulkan dari ketidakhadiran pada tabel lama; rinciannya diisi sebagai asumsi latihan.
4. Tabel 4 kini memuat 44 prodi x 7 tahun = 308 baris. Kunci gabungannya Kode_Prodi + Tahun_Penerimaan. Nama dan fakultas disalin antarperiode; tidak ada klaim perubahan historis prodi. Jenjang S1 masih merupakan asumsi.
5. Tabel 5 diganti menjadi 5_ref_wilayah_3t.csv. Kunci Kode_Wilayah mewakili satu kabupaten/kota fiktif. Kode lama W34 tidak digunakan.

## Aturan penggabungan

- Mulai dari tabel 1 dan LEFT JOIN tabel 2 pada ID_Pendaftar agar semua pendaftar tetap dihitung.
- Dari tabel 2, LEFT JOIN tabel 3 pada ID_Mahasiswa. Alternatif: gabungkan tabel 1 langsung ke tabel 3 menggunakan ID_Pendaftar, yang juga unik di tabel 3.
- Dari tabel 1/2 ke referensi prodi, gunakan pasangan kode prodi terkait DAN Tahun_Penerimaan. Untuk tabel 3, padankan Angkatan dengan Tahun_Penerimaan pada referensi.
- Menggabungkan referensi prodi hanya berdasarkan Kode_Prodi akan memperbanyak setiap baris tujuh kali. Jangan melakukan itu.
- Hubungkan Kode_Wilayah_Asal dengan Kode_Wilayah untuk mendapatkan Nama_Provinsi, Nama_Kabupaten_Kota dan Status_3T.
- Jumlah baris tabel 1 = orang mendaftar; tabel 2 = orang diterima; tabel 3 = orang daftar ulang. Jumlah mahasiswa aktif memerlukan filter status.
- Menurut kontrak dummy ini, tidak ada baris hasil seleksi berarti Tidak Diterima karena seluruh hasil seleksi sudah final. Ini hanya asumsi dummy; pada data final, ketidakhadiran bisa bermakna lain dan wajib mengikuti kamus resmi.
- Untuk peluang diterima, penyebutnya pendaftar pada kelompok dan tahun yang sama. Untuk tingkat daftar ulang, penyebutnya peserta diterima. Rasio aktif pada snapshot lintas angkatan bukan ukuran putus kuliah.

## Latihan preprocessing dan nilai kosong

- 120 asal sekolah sengaja dikosongkan untuk latihan missing value. Arti: tidak tercatat, bukan tidak pernah sekolah.
- 60 nilai Jenis_Kelamin tabel 1 memiliki spasi awal/akhir. Lakukan trim sebelum agregasi dan pengecekan konsistensi.
- Pilihan prodi kedua kosong berarti tidak memilih pilihan kedua.
- Pada tabel 2, ID_Mahasiswa dan Tanggal_Daftar_Ulang kosong berarti tidak daftar ulang.
- Tidak ada duplikasi kunci atau FK putus yang sengaja ditambahkan. Data yang tampak bersih tetap perlu diperiksa.
- CSV menggunakan titik koma, UTF-8 dengan BOM, dan tanggal YYYY-MM-DD. Kode dibaca sebagai teks; sel kosong bukan nol.

## Dasar simulasi dan dokumentasi

Revisi menggunakan dummy lama sebagai masukan dan profil sumber sebagai referensi kategori. Identitas orang dummy dipertahankan. Label jalur SNBP, SNBT dan Mandiri diseragamkan lintas 2019-2025 hanya untuk latihan, bukan rekonstruksi sejarah jalur masuk. Sumber tidak memiliki hasil seleksi resmi; seluruh hasil dalam dummy lama maupun revisi adalah simulasi.

Seed revisi: 20261028. Asumsi probabilitas pembuatan dummy awal tersimpan pada README dan skrip generator versi lama. Empat CSV sumber prestasi, generasi pertama, ekonomi dan IPK tidak ditambahkan karena tidak masuk rancangan lima tabel ini. Berkas sumber dan dummy lama tidak diubah.

KAMUS_DATA.md menjelaskan seluruh kolom. _pendukung/hasil_pemeriksaan.json menyimpan hash, jumlah baris dan 25 pemeriksaan konsistensi. _pendukung/revisi_dummy_3t.py mereproduksi keluaran dari versi sebelumnya; gunakan --output ke folder baru. REVISI_DARI_GAMBAR.md membedakan isi yang dikonfirmasi gambar dengan asumsi latihan.
