# Dasar revisi dari gambar

## Dikonfirmasi oleh gambar pengguna

- 1_pendaftar_penerimaan: satu pendaftar, kunci ID_Pendaftar.
- 2_hasil_seleksi_daftar_ulang: satu pendaftar diterima, kunci ID_Pendaftar.
- 3_mahasiswa_aktif: satu mahasiswa yang daftar ulang, kunci ID_Mahasiswa.
- 4_ref_program_studi: satu prodi pada satu tahun, kunci Kode_Prodi + Tahun_Penerimaan.
- 5_ref_wilayah_3t: satu kabupaten/kota, kunci Kode_Wilayah.
- Tidak semua pendaftar muncul pada tabel 2 dan 3. CSV titik koma dan UTF-8 BOM, tanggal ISO, nilai kosong tidak otomatis nol.

## Asumsi yang belum dikonfirmasi kamus final

- Ref wilayah memuat seluruh wilayah beserta Status_3T Ya/Tidak; bisa saja tabel resmi hanya memuat wilayah 3T.
- Semua kolom selain kunci dan nama tabel dirancang untuk latihan, bukan hasil pembacaan kamus final.
- Status 3T bersifat tetap pada seluruh tahun simulasi. Ini penyederhanaan, bukan verifikasi status administratif tiap tahun.
- Kabupaten/kota dan kode wilayah fiktif. Sebaran 3T ditetapkan acak dengan jumlah sama per provinsi; tidak mencerminkan sebaran nyata.
- Semua orang sudah memiliki hasil seleksi final. Ketiadaan pada tabel 2 berarti tidak diterima hanya dalam dummy ini.
- Penafsiran tabel 3 mengikuti unit baris pada gambar, yaitu sudah daftar ulang, walaupun nama berkas memakai mahasiswa_aktif. Seluruh orang yang daftar ulang dicantumkan; status snapshot menjadi kolom terpisah. Jika kamus final menyatakan hanya mahasiswa berstatus aktif, filter ini harus disesuaikan.

Kamus Data Final tetap menjadi rujukan penentu ketika dirilis.
