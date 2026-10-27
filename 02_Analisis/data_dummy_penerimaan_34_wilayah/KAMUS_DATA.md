# Kamus data dummy

Struktur ini adalah rancangan simulasi berdasarkan percakapan, bukan skema resmi penyelenggara. Seluruh ID baru merupakan identitas dummy. Aturan generasi, sumber kategori, dan pemetaan wilayah dijelaskan pada README.md.

## 1_pendaftar_penerimaan.csv

Satu pendaftaran pada satu jalur dan tahun; orang bisa berulang.

| Kolom | Tipe | Keterangan |
|---|---|---|
| ID_Pendaftar | Teks | Identitas calon mahasiswa dummy; berulang bila orang yang sama mengikuti jalur berikutnya. |
| ID_Pendaftaran | Teks | Kunci unik pendaftaran, format DFT-DMY-#######. |
| Tahun_Penerimaan | Bilangan bulat | Tahun simulasi penerimaan, 2019-2025. |
| Jalur_Penerimaan | Kategori | SNBP / SNBT / Mandiri; label diseragamkan untuk latihan lintas tahun, bukan rekonstruksi nama historis jalur. |
| Jenis_Kelamin | Kategori | Laki-laki / Perempuan; distribusi mengacu kategori profil referensi. |
| Tanggal_Lahir | Tanggal ISO | Tanggal lahir sintetis, YYYY-MM-DD. |
| Usia_Saat_Daftar | Bilangan bulat | Usia pada 1 Agustus tahun penerimaan; usia dan tanggal lahir disimulasikan. |
| Kode_Wilayah_Asal | Teks | FK ke Kode_Provinsi pada tabel wilayah; W34-## adalah kode dummy. |
| Asal_Sekolah | Teks | Label sekolah sintetis SEKOLAH-DUMMY-..., bukan nama sekolah nyata. |
| Kode_Prodi_Pilihan_1 | Teks | FK ke tabel prodi; selalu diisi. |
| Kode_Prodi_Pilihan_2 | Teks | FK ke tabel prodi; berbeda dari pilihan 1; kosong berarti tidak memilih pilihan kedua. |
| Status_Pendaftaran | Kategori | Selesai; simulasi ini hanya mencakup pendaftaran lengkap. |

## 2_hasil_seleksi_daftar_ulang.csv

Satu hasil seleksi untuk setiap pendaftaran, termasuk yang tidak diterima.

| Kolom | Tipe | Keterangan |
|---|---|---|
| ID_Pendaftaran | Teks | PK sekaligus FK ke tabel pendaftar; satu hasil untuk setiap pendaftaran. |
| ID_Pendaftar | Teks | Identitas orang yang sama seperti tabel pendaftar. |
| Tahun_Penerimaan | Bilangan bulat | Sama dengan tahun pada pendaftaran terkait. |
| Jalur_Penerimaan | Kategori | Sama dengan jalur pada pendaftaran terkait. |
| Status_Seleksi | Kategori | Diterima / Tidak Diterima; tidak ada status menunggu. |
| Kode_Prodi_Diterima | Teks | Prodi pilihan 1 atau 2 jika diterima; kosong jika tidak diterima. |
| Status_Daftar_Ulang | Kategori | Sudah / Tidak Daftar Ulang / Tidak Berlaku. Tidak Berlaku khusus peserta tidak diterima. |
| Tanggal_Daftar_Ulang | Tanggal ISO | Tanggal sintetis; hanya terisi jika status Sudah. |
| NIM | Teks | NIM-DMY-YYYY-######; hanya diterbitkan untuk peserta yang sudah daftar ulang, termasuk yang tidak aktif pada snapshot. |

## 3_mahasiswa_aktif.csv

Satu mahasiswa aktif pada snapshot 1 Oktober 2025.

| Kolom | Tipe | Keterangan |
|---|---|---|
| NIM | Teks | Kunci unik mahasiswa pada satu snapshot; FK ke NIM tabel hasil seleksi. |
| ID_Pendaftar | Teks | Identitas calon mahasiswa sebelum menjadi mahasiswa. |
| ID_Pendaftaran | Teks | Pendaftaran yang menghasilkan registrasi mahasiswa ini. |
| Angkatan | Bilangan bulat | Tahun penerimaan pada pendaftaran terkait. |
| Tahun_Akademik | Teks | 2025/2026 untuk seluruh baris. |
| Semester_Pelaporan | Kategori | Ganjil untuk seluruh baris; bukan nomor semester tempuh. |
| Tanggal_Snapshot | Tanggal ISO | 2025-10-01; tanggal pengamatan simulasi. |
| Kode_Prodi | Teks | Sama dengan Kode_Prodi_Diterima; tidak disimulasikan perpindahan prodi. |
| Jenis_Kelamin | Kategori | Sama dengan data pendaftar terkait. |
| Kode_Wilayah_Asal | Teks | Sama dengan data pendaftar terkait; FK ke tabel wilayah. |
| Jalur_Masuk | Kategori | Jalur pendaftaran yang menghasilkan daftar ulang. |
| Status_Mahasiswa | Kategori | Aktif untuk seluruh baris; status lain tidak dimuat dalam tabel ini. |

## 4_ref_program_studi.csv

Satu program studi.

| Kolom | Tipe | Keterangan |
|---|---|---|
| Kode_Prodi | Teks | PK PRD-###; kode dummy, bukan kode resmi prodi. |
| Nama_Prodi | Teks | 44 nama prodi dari profil referensi. |
| Kode_Fakultas | Teks | FAK-##; kode dummy untuk 15 fakultas. |
| Nama_Fakultas | Teks | Pasangan prodi-fakultas dipertahankan dari profil referensi. |
| Jenjang | Kategori | S1 untuk semua prodi sebagai asumsi latihan; tidak tersedia pada profil referensi. |

## 5_ref_wilayah_34.csv

Satu kelompok provinsi dalam klasifikasi latihan 34 wilayah.

| Kolom | Tipe | Keterangan |
|---|---|---|
| Kode_Provinsi | Teks | PK W34-##; kode sintetis berurutan alfabetis, bukan kode BPS/Kemendagri. |
| Nama_Provinsi | Teks | 34 kelompok provinsi latihan setelah pemetaan kategori Papua; bukan referensi administratif resmi terkini. |

