# Kamus data dummy revisi 3T

Rancangan kolom merupakan asumsi latihan. Gambar acuan mengonfirmasi nama tabel, unit baris dan kunci, tetapi tidak memuat semua kolom atau definisi resmi status 3T.

## 1_pendaftar_penerimaan.csv

Unit: Satu pendaftar. Kunci: ID_Pendaftar. Jumlah baris: 12,000.

| Kolom | Tipe | Arti dan aturan |
|---|---|---|
| ID_Pendaftar | Teks | PK tabel 1 dan 2; FK tabel 3. Satu ID mewakili satu orang dalam latihan ini. |
| Tahun_Penerimaan | Bilangan bulat | 2019-2025; bagian kunci gabungan referensi prodi. |
| Jalur_Penerimaan | Kategori | SNBP / SNBT / Mandiri. Label simulasi diseragamkan lintas tahun, bukan nama historis resmi. |
| Jenis_Kelamin | Kategori | Laki-laki / Perempuan. Sebanyak 60 baris pendaftar memiliki spasi tepi untuk latihan trim. |
| Tanggal_Lahir | Tanggal | Tanggal lahir dummy; YYYY-MM-DD. |
| Usia_Saat_Daftar | Bilangan bulat | Usia pada 1 Agustus tahun penerimaan. |
| Kode_Wilayah_Asal | Teks | FK ke Kode_Wilayah tabel 5; tingkat kabupaten/kota, bukan provinsi. |
| Asal_Sekolah | Teks | Nama sekolah sintetis. Kosong pada 120 baris berarti tidak tercatat. |
| Kode_Prodi_Pilihan_1 | Teks | Pilihan pertama. Gabungkan dengan tabel 4 memakai kode ini DAN Tahun_Penerimaan. |
| Kode_Prodi_Pilihan_2 | Teks | Pilihan kedua; kosong berarti tidak memilih. Kunci join juga harus menyertakan Tahun_Penerimaan. |
| Status_Pendaftaran | Kategori | Selesai untuk semua baris; tidak ada pendaftaran belum lengkap pada simulasi. |

## 2_hasil_seleksi_daftar_ulang.csv

Unit: Satu pendaftar yang diterima. Kunci: ID_Pendaftar. Jumlah baris: 5,547.

| Kolom | Tipe | Arti dan aturan |
|---|---|---|
| ID_Pendaftar | Teks | PK tabel 1 dan 2; FK tabel 3. Satu ID mewakili satu orang dalam latihan ini. |
| Tahun_Penerimaan | Bilangan bulat | 2019-2025; bagian kunci gabungan referensi prodi. |
| Jalur_Penerimaan | Kategori | SNBP / SNBT / Mandiri. Label simulasi diseragamkan lintas tahun, bukan nama historis resmi. |
| Status_Seleksi | Kategori | Diterima untuk seluruh tabel 2. Ketidakhadiran di tabel 2 berarti tidak diterima hanya menurut kontrak dummy ini. |
| Kode_Prodi_Diterima | Teks | Salah satu prodi pilihan; FK bersama Tahun_Penerimaan ke tabel 4. |
| Status_Daftar_Ulang | Kategori | Sudah / Tidak Daftar Ulang; mencakup hasil registrasi peserta yang diterima. |
| Tanggal_Daftar_Ulang | Tanggal | Tanggal sintetis YYYY-MM-DD; kosong jika tidak daftar ulang. |
| ID_Mahasiswa | Teks | MHS-DMY-######. PK tabel 3, terisi di tabel 2 hanya jika sudah daftar ulang. |

## 3_mahasiswa_aktif.csv

Unit: Satu mahasiswa yang sudah daftar ulang. Kunci: ID_Mahasiswa. Jumlah baris: 4,601.

| Kolom | Tipe | Arti dan aturan |
|---|---|---|
| ID_Mahasiswa | Teks | MHS-DMY-######. PK tabel 3, terisi di tabel 2 hanya jika sudah daftar ulang. |
| ID_Pendaftar | Teks | PK tabel 1 dan 2; FK tabel 3. Satu ID mewakili satu orang dalam latihan ini. |
| Angkatan | Bilangan bulat | Tahun masuk; sama dengan Tahun_Penerimaan peserta terkait. Gunakan sebagai padanan tahun saat join referensi prodi. |
| Tahun_Akademik | Teks | 2025/2026 untuk seluruh tabel 3. |
| Semester_Pelaporan | Kategori | Ganjil untuk seluruh tabel 3; bukan semester ke berapa. |
| Tanggal_Snapshot | Tanggal | 2025-10-01; tanggal pengamatan status simulasi. |
| Kode_Prodi | Teks | Kode dummy PRD-###. Di tabel 4 hanya unik bersama Tahun_Penerimaan. Di tabel 3 gunakan bersama Angkatan. |
| Jenis_Kelamin | Kategori | Laki-laki / Perempuan. Sebanyak 60 baris pendaftar memiliki spasi tepi untuk latihan trim. |
| Kode_Wilayah_Asal | Teks | FK ke Kode_Wilayah tabel 5; tingkat kabupaten/kota, bukan provinsi. |
| Jalur_Masuk | Kategori | Jalur penerimaan saat peserta mendaftar ulang. |
| Status_Mahasiswa | Kategori | Aktif / Cuti / Lulus / Non-Aktif/DO. Status non-Aktif tambahan merupakan asumsi, bukan hasil observasi. |

## 4_ref_program_studi.csv

Unit: Satu prodi pada satu tahun. Kunci: Kode_Prodi + Tahun_Penerimaan. Jumlah baris: 308.

| Kolom | Tipe | Arti dan aturan |
|---|---|---|
| Kode_Prodi | Teks | Kode dummy PRD-###. Di tabel 4 hanya unik bersama Tahun_Penerimaan. Di tabel 3 gunakan bersama Angkatan. |
| Tahun_Penerimaan | Bilangan bulat | 2019-2025; bagian kunci gabungan referensi prodi. |
| Nama_Prodi | Teks | 44 kategori nama prodi berasal dari referensi lama. |
| Kode_Fakultas | Teks | FAK-##; kode sintetis. |
| Nama_Fakultas | Teks | Hubungan prodi dengan 15 fakultas dipertahankan dari sumber. |
| Jenjang | Kategori | S1 untuk seluruh prodi sebagai asumsi latihan, bukan verifikasi resmi. |

## 5_ref_wilayah_3t.csv

Unit: Satu kabupaten/kota. Kunci: Kode_Wilayah. Jumlah baris: 304.

| Kolom | Tipe | Arti dan aturan |
|---|---|---|
| Kode_Wilayah | Teks | PK DMY-WIL-####; kode sintetis kabupaten/kota, bukan kode BPS/Kemendagri. |
| Nama_Kabupaten_Kota | Teks | Nama kabupaten/kota fiktif berlabel Dummy. Tidak dapat dipasangkan langsung ke peta wilayah nyata. |
| Jenis_Wilayah | Kategori | Kabupaten / Kota; klasifikasi fiktif. |
| Kode_Provinsi | Teks | DMY-PRV-##; kode sintetis provinsi, bukan kode resmi. |
| Nama_Provinsi | Teks | 38 nama kategori provinsi dari profil sumber; kategori Papua tidak lagi digabung menjadi 34. |
| Status_3T | Kategori | Ya / Tidak; label dummy yang ditetapkan acak, tetap per wilayah. Bukan klasifikasi resmi 3T. |

