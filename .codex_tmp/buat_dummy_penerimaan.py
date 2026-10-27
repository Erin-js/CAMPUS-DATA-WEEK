import csv
import argparse
import hashlib
import json
import random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(r'C:\Users\ACER\OneDrive\Dokumen\COMPETITION\CAMPUS DATA WEEK')
parser = argparse.ArgumentParser(description='Membuat lima dataset dummy penerimaan yang konsisten.')
parser.add_argument('--source', type=Path, default=ROOT / '02_Analisis' / 'data')
parser.add_argument('--output', type=Path, default=ROOT / '02_Analisis' / 'data_dummy_penerimaan_34_wilayah')
args = parser.parse_args()
SOURCE = args.source.resolve()
OUTPUT = args.output.resolve()
SEED = 20261027
N_PEOPLE = 12000
SNAPSHOT = date(2025, 10, 1)
rng = random.Random(SEED)


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter=';'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, fields, rows):
    with path.open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)


source_hashes = {f.name: sha(f) for f in sorted(SOURCE.glob('*.csv'))}
profiles = read_csv(SOURCE / '1_profil_mahasiswa_umum.csv')
assert len({r['ID_Mahasiswa'] for r in profiles}) == len(profiles)
if OUTPUT.exists():
    raise SystemExit(f'Folder sudah ada; tidak ditimpa: {OUTPUT}')
OUTPUT.mkdir()
support = OUTPUT / '_pendukung'
support.mkdir()

# Preserve only category combinations and their empirical frequencies, not source people.
province_merge = {
    'Papua Selatan': 'Papua',
    'Papua Tengah': 'Papua',
    'Papua Pegunungan': 'Papua',
    'Papua Barat Daya': 'Papua Barat',
}
province_names = sorted({province_merge.get(r['Provinsi_Asal'], r['Provinsi_Asal']) for r in profiles})
assert len(province_names) == 34
province_codes = {name: f'W34-{i:02d}' for i, name in enumerate(province_names, 1)}
faculty_names = sorted({r['Fakultas'] for r in profiles})
faculty_codes = {name: f'FAK-{i:02d}' for i, name in enumerate(faculty_names, 1)}
program_pairs = sorted({(r['Program_Studi'], r['Fakultas']) for r in profiles})
assert len(program_pairs) == len({x[0] for x in program_pairs}) == 44
program_codes = {name: f'PRD-{i:03d}' for i, (name, _) in enumerate(program_pairs, 1)}
program_reference = [dict(Kode_Prodi=program_codes[name], Nama_Prodi=name,
    Kode_Fakultas=faculty_codes[faculty], Nama_Fakultas=faculty, Jenjang='S1')
    for name, faculty in program_pairs]
province_reference = [dict(Kode_Provinsi=province_codes[name], Nama_Provinsi=name)
    for name in province_names]
program_counts = Counter(r['Program_Studi'] for r in profiles)
program_population = [program_codes[name] for name, count in program_counts.items() for _ in range(count)]
# Dummy variation by program, drawn independently of gender and region.
program_adjustment = {code: rng.uniform(-0.065, 0.065) for code in program_codes.values()}
routes = ['SNBP', 'SNBT', 'Mandiri']
acceptance_base = {'SNBP': 0.25, 'SNBT': 0.34, 'Mandiri': 0.48}
registration_base = {'SNBP': 0.82, 'SNBT': 0.86, 'Mandiri': 0.76}
active_base = {0: 0.98, 1: 0.96, 2: 0.93, 3: 0.88, 4: 0.55, 5: 0.20, 6: 0.08}
route_month = {'SNBP': 4, 'SNBT': 6, 'Mandiri': 8}
applications, selections, active_students = [], [], []
people = {}
registered_people = set()
student_serial = 0

for person_serial in range(1, N_PEOPLE + 1):
    sample = rng.choice(profiles)
    year = int(sample['Angkatan'])
    province = province_merge.get(sample['Provinsi_Asal'], sample['Provinsi_Asal'])
    region = province_codes[province]
    gender = sample['Jenis_Kelamin']
    # Source Usia is current age; do not misread it as age at admission.
    birth_year = year - rng.choices([17, 18, 19, 20, 21], [10, 60, 23, 6, 1])[0]
    birthday = date(birth_year, rng.randint(1, 12), rng.randint(1, 28))
    person_id = f'CAL-DMY-{person_serial:06d}'
    school = f'SEKOLAH-DUMMY-{region}-{rng.randint(1, 35):03d}'
    people[person_id] = (year, region, gender, birthday.isoformat(), school)
    route_start = rng.choices([0, 1, 2], [0.30, 0.45, 0.25])[0]
    for route_index in range(route_start, 3):
        route = routes[route_index]
        if route_index == route_start:
            first_program = program_codes[sample['Program_Studi']]
        else:
            first_program = rng.choice(program_population)
        second_program = rng.choice(program_population)
        while second_program == first_program:
            second_program = rng.choice(program_population)
        if rng.random() < 0.12:
            second_program = ''
        application_id = f'DFT-DMY-{len(applications)+1:07d}'
        age_at_admission = year - birthday.year - ((8, 1) < (birthday.month, birthday.day))
        app = dict(ID_Pendaftar=person_id, ID_Pendaftaran=application_id,
            Tahun_Penerimaan=year, Jalur_Penerimaan=route, Jenis_Kelamin=gender,
            Tanggal_Lahir=birthday.isoformat(), Usia_Saat_Daftar=age_at_admission,
            Kode_Wilayah_Asal=region, Asal_Sekolah=school,
            Kode_Prodi_Pilihan_1=first_program, Kode_Prodi_Pilihan_2=second_program,
            Status_Pendaftaran='Selesai')
        applications.append(app)
        year_adjustment = (year - 2022) * 0.006
        probability = acceptance_base[route] + program_adjustment[first_program] + year_adjustment
        admitted = rng.random() < probability
        program = (second_program if second_program and rng.random() < 0.18 else first_program) if admitted else ''
        registered = admitted and rng.random() < registration_base[route]
        registration_date = ''
        nim = ''
        if registered:
            student_serial += 1
            nim = f'NIM-DMY-{year}-{student_serial:06d}'
            registration_date = (date(year, route_month[route], 5) + timedelta(days=rng.randint(0, 20))).isoformat()
            registered_people.add(person_id)
        result = dict(ID_Pendaftaran=application_id, ID_Pendaftar=person_id,
            Tahun_Penerimaan=year, Jalur_Penerimaan=route,
            Status_Seleksi='Diterima' if admitted else 'Tidak Diterima',
            Kode_Prodi_Diterima=program,
            Status_Daftar_Ulang=('Sudah' if registered else 'Tidak Daftar Ulang') if admitted else 'Tidak Berlaku',
            Tanggal_Daftar_Ulang=registration_date, NIM=nim)
        selections.append(result)
        if registered:
            if rng.random() < active_base[2025-year]:
                active_students.append(dict(NIM=nim, ID_Pendaftar=person_id,
                    ID_Pendaftaran=application_id, Angkatan=year,
                    Tahun_Akademik='2025/2026', Semester_Pelaporan='Ganjil',
                    Tanggal_Snapshot=SNAPSHOT.isoformat(), Kode_Prodi=program,
                    Jenis_Kelamin=gender, Kode_Wilayah_Asal=region,
                    Jalur_Masuk=route, Status_Mahasiswa='Aktif'))
            break
        if rng.random() >= 0.45:
            break

schemas = {
    '1_pendaftar_penerimaan.csv': [
        ('ID_Pendaftar','Teks','Identitas calon mahasiswa dummy; berulang bila orang yang sama mengikuti jalur berikutnya.'),
        ('ID_Pendaftaran','Teks','Kunci unik pendaftaran, format DFT-DMY-#######.'),
        ('Tahun_Penerimaan','Bilangan bulat','Tahun simulasi penerimaan, 2019-2025.'),
        ('Jalur_Penerimaan','Kategori','SNBP / SNBT / Mandiri; label diseragamkan untuk latihan lintas tahun, bukan rekonstruksi nama historis jalur.'),
        ('Jenis_Kelamin','Kategori','Laki-laki / Perempuan; distribusi mengacu kategori profil referensi.'),
        ('Tanggal_Lahir','Tanggal ISO','Tanggal lahir sintetis, YYYY-MM-DD.'),
        ('Usia_Saat_Daftar','Bilangan bulat','Usia pada 1 Agustus tahun penerimaan; usia dan tanggal lahir disimulasikan.'),
        ('Kode_Wilayah_Asal','Teks','FK ke Kode_Provinsi pada tabel wilayah; W34-## adalah kode dummy.'),
        ('Asal_Sekolah','Teks','Label sekolah sintetis SEKOLAH-DUMMY-..., bukan nama sekolah nyata.'),
        ('Kode_Prodi_Pilihan_1','Teks','FK ke tabel prodi; selalu diisi.'),
        ('Kode_Prodi_Pilihan_2','Teks','FK ke tabel prodi; berbeda dari pilihan 1; kosong berarti tidak memilih pilihan kedua.'),
        ('Status_Pendaftaran','Kategori','Selesai; simulasi ini hanya mencakup pendaftaran lengkap.')],
    '2_hasil_seleksi_daftar_ulang.csv': [
        ('ID_Pendaftaran','Teks','PK sekaligus FK ke tabel pendaftar; satu hasil untuk setiap pendaftaran.'),
        ('ID_Pendaftar','Teks','Identitas orang yang sama seperti tabel pendaftar.'),
        ('Tahun_Penerimaan','Bilangan bulat','Sama dengan tahun pada pendaftaran terkait.'),
        ('Jalur_Penerimaan','Kategori','Sama dengan jalur pada pendaftaran terkait.'),
        ('Status_Seleksi','Kategori','Diterima / Tidak Diterima; tidak ada status menunggu.'),
        ('Kode_Prodi_Diterima','Teks','Prodi pilihan 1 atau 2 jika diterima; kosong jika tidak diterima.'),
        ('Status_Daftar_Ulang','Kategori','Sudah / Tidak Daftar Ulang / Tidak Berlaku. Tidak Berlaku khusus peserta tidak diterima.'),
        ('Tanggal_Daftar_Ulang','Tanggal ISO','Tanggal sintetis; hanya terisi jika status Sudah.'),
        ('NIM','Teks','NIM-DMY-YYYY-######; hanya diterbitkan untuk peserta yang sudah daftar ulang, termasuk yang tidak aktif pada snapshot.')],
    '3_mahasiswa_aktif.csv': [
        ('NIM','Teks','Kunci unik mahasiswa pada satu snapshot; FK ke NIM tabel hasil seleksi.'),
        ('ID_Pendaftar','Teks','Identitas calon mahasiswa sebelum menjadi mahasiswa.'),
        ('ID_Pendaftaran','Teks','Pendaftaran yang menghasilkan registrasi mahasiswa ini.'),
        ('Angkatan','Bilangan bulat','Tahun penerimaan pada pendaftaran terkait.'),
        ('Tahun_Akademik','Teks','2025/2026 untuk seluruh baris.'),
        ('Semester_Pelaporan','Kategori','Ganjil untuk seluruh baris; bukan nomor semester tempuh.'),
        ('Tanggal_Snapshot','Tanggal ISO','2025-10-01; tanggal pengamatan simulasi.'),
        ('Kode_Prodi','Teks','Sama dengan Kode_Prodi_Diterima; tidak disimulasikan perpindahan prodi.'),
        ('Jenis_Kelamin','Kategori','Sama dengan data pendaftar terkait.'),
        ('Kode_Wilayah_Asal','Teks','Sama dengan data pendaftar terkait; FK ke tabel wilayah.'),
        ('Jalur_Masuk','Kategori','Jalur pendaftaran yang menghasilkan daftar ulang.'),
        ('Status_Mahasiswa','Kategori','Aktif untuk seluruh baris; status lain tidak dimuat dalam tabel ini.')],
    '4_ref_program_studi.csv': [
        ('Kode_Prodi','Teks','PK PRD-###; kode dummy, bukan kode resmi prodi.'),
        ('Nama_Prodi','Teks','44 nama prodi dari profil referensi.'),
        ('Kode_Fakultas','Teks','FAK-##; kode dummy untuk 15 fakultas.'),
        ('Nama_Fakultas','Teks','Pasangan prodi-fakultas dipertahankan dari profil referensi.'),
        ('Jenjang','Kategori','S1 untuk semua prodi sebagai asumsi latihan; tidak tersedia pada profil referensi.')],
    '5_ref_wilayah_34.csv': [
        ('Kode_Provinsi','Teks','PK W34-##; kode sintetis berurutan alfabetis, bukan kode BPS/Kemendagri.'),
        ('Nama_Provinsi','Teks','34 kelompok provinsi latihan setelah pemetaan kategori Papua; bukan referensi administratif resmi terkini.')],
}
tables = dict(zip(schemas, [applications, selections, active_students, program_reference, province_reference]))
for name, rows in tables.items():
    write_csv(OUTPUT / name, [x[0] for x in schemas[name]], rows)

# Verify the saved CSVs, not only the in-memory objects.
saved = {name: read_csv(OUTPUT / name) for name in schemas}
apps, results, active, prodi, wilayah = saved.values()
apps_by_id = {r['ID_Pendaftaran']: r for r in apps}
results_by_id = {r['ID_Pendaftaran']: r for r in results}
valid_prodi = {r['Kode_Prodi'] for r in prodi}
valid_wilayah = {r['Kode_Provinsi'] for r in wilayah}
registered = [r for r in results if r['Status_Daftar_Ulang'] == 'Sudah']
accepted = [r for r in results if r['Status_Seleksi'] == 'Diterima']
checks = []


def check(name, condition):
    checks.append({'pemeriksaan': name, 'lulus': bool(condition)})


check('12.000 calon mahasiswa unik', len({r['ID_Pendaftar'] for r in apps}) == N_PEOPLE)
check('Kunci pendaftaran dan hasil unik; cakupan identik', len(apps_by_id) == len(apps) == len(results_by_id) == len(results) and apps_by_id.keys() == results_by_id.keys())
check('44 kode prodi dan 34 kode wilayah unik', len(prodi) == len(valid_prodi) == 44 and len(wilayah) == len(valid_wilayah) == 34)
check('Semua FK wilayah dan pilihan prodi valid', all(r['Kode_Wilayah_Asal'] in valid_wilayah and r['Kode_Prodi_Pilihan_1'] in valid_prodi and (not r['Kode_Prodi_Pilihan_2'] or r['Kode_Prodi_Pilihan_2'] in valid_prodi) for r in apps))
check('Pilihan 1 dan 2 tidak sama', all(r['Kode_Prodi_Pilihan_1'] != r['Kode_Prodi_Pilihan_2'] for r in apps))
check('Identitas tahun dan jalur konsisten antartabel', all(all(r[k] == apps_by_id[r['ID_Pendaftaran']][k] for k in ['ID_Pendaftar','Tahun_Penerimaan','Jalur_Penerimaan']) for r in results))
check('Prodi diterima termasuk pilihan pendaftar', all(r['Kode_Prodi_Diterima'] in [apps_by_id[r['ID_Pendaftaran']]['Kode_Prodi_Pilihan_1'], apps_by_id[r['ID_Pendaftaran']]['Kode_Prodi_Pilihan_2']] and r['Kode_Prodi_Diterima'] in valid_prodi for r in accepted))
check('Peserta tidak diterima tidak memiliki prodi diterima NIM atau tanggal registrasi', all(not r['Kode_Prodi_Diterima'] and not r['NIM'] and not r['Tanggal_Daftar_Ulang'] and r['Status_Daftar_Ulang'] == 'Tidak Berlaku' for r in results if r['Status_Seleksi'] == 'Tidak Diterima'))
check('NIM dan tanggal hanya terisi jika sudah daftar ulang', all(bool(r['NIM']) == bool(r['Tanggal_Daftar_Ulang']) == (r['Status_Daftar_Ulang'] == 'Sudah') for r in results))
check('Daftar ulang hanya untuk peserta diterima', all(r['Status_Seleksi'] == 'Diterima' for r in registered))
check('Satu orang paling banyak satu daftar ulang dan NIM', len({r['NIM'] for r in registered}) == len({r['ID_Pendaftar'] for r in registered}) == len(registered))
check('NIM dan identitas mahasiswa aktif unik', len(active) == len({r['NIM'] for r in active}) == len({r['ID_Pendaftar'] for r in active}))
check('Mahasiswa aktif berasal dari registrasi yang sesuai', all(results_by_id[r['ID_Pendaftaran']]['Status_Daftar_Ulang'] == 'Sudah' and all(r[a] == results_by_id[r['ID_Pendaftaran']][b] for a,b in [('NIM','NIM'),('ID_Pendaftar','ID_Pendaftar'),('Angkatan','Tahun_Penerimaan'),('Jalur_Masuk','Jalur_Penerimaan'),('Kode_Prodi','Kode_Prodi_Diterima')]) for r in active))
check('Demografi dan wilayah mahasiswa aktif konsisten', all(all(r[k] == apps_by_id[r['ID_Pendaftaran']][k] for k in ['Jenis_Kelamin','Kode_Wilayah_Asal']) for r in active))
check('Semua mahasiswa aktif berada pada snapshot yang sama', all(r['Tahun_Akademik'] == '2025/2026' and r['Semester_Pelaporan'] == 'Ganjil' and r['Tanggal_Snapshot'] == SNAPSHOT.isoformat() and r['Status_Mahasiswa'] == 'Aktif' for r in active))
check('Tanggal registrasi tidak melampaui snapshot dan tahun sesuai', all(date.fromisoformat(r['Tanggal_Daftar_Ulang']) <= SNAPSHOT and date.fromisoformat(r['Tanggal_Daftar_Ulang']).year == int(r['Tahun_Penerimaan']) for r in registered))
check('Tanggal lahir dan usia konsisten', all(int(r['Usia_Saat_Daftar']) == int(r['Tahun_Penerimaan']) - date.fromisoformat(r['Tanggal_Lahir']).year - ((8, 1) < (date.fromisoformat(r['Tanggal_Lahir']).month, date.fromisoformat(r['Tanggal_Lahir']).day)) for r in apps))
check('Profil orang konsisten pada pendaftaran berulang', all(len({tuple(r[k] for k in ['Tahun_Penerimaan','Jenis_Kelamin','Tanggal_Lahir','Kode_Wilayah_Asal','Asal_Sekolah']) for r in apps if r['ID_Pendaftar'] == pid}) == 1 for pid, n in Counter(r['ID_Pendaftar'] for r in apps).items() if n > 1))
check('Semua berkas CSV memiliki BOM UTF-8 dan lebar baris konsisten', all((OUTPUT/name).read_bytes().startswith(b'\xef\xbb\xbf') and all(None not in r and all(v is not None for v in r.values()) for r in rows) for name, rows in saved.items()))
check('Referensi sumber tidak berubah', source_hashes == {f.name: sha(f) for f in sorted(SOURCE.glob('*.csv'))})
summary = {
    'jenis_data': 'DUMMY / SINTETIS, bukan hasil penerimaan nyata',
    'seed': SEED, 'snapshot': SNAPSHOT.isoformat(),
    'jumlah_baris': {name: len(rows) for name, rows in saved.items()},
    'calon_mahasiswa_unik': N_PEOPLE,
    'pendaftaran_diterima': len(accepted), 'orang_diterima_unik': len({r['ID_Pendaftar'] for r in accepted}),
    'orang_sudah_daftar_ulang': len(registered), 'mahasiswa_aktif': len(active),
    'jumlah_pemeriksaan': len(checks), 'semua_lulus': all(c['lulus'] for c in checks),
    'pemeriksaan': checks,
    'sha256_sumber': source_hashes,
    'sha256_output_csv': {name: sha(OUTPUT/name) for name in schemas},
    'ringkasan_per_tahun': [dict(tahun=year,
        orang_mendaftar=len({r['ID_Pendaftar'] for r in apps if r['Tahun_Penerimaan']==str(year)}),
        pendaftaran=sum(r['Tahun_Penerimaan']==str(year) for r in apps),
        pendaftaran_diterima=sum(r['Tahun_Penerimaan']==str(year) for r in accepted),
        daftar_ulang=sum(r['Tahun_Penerimaan']==str(year) for r in registered),
        aktif=sum(r['Angkatan']==str(year) for r in active)) for year in range(2019,2026)],
}
(support / 'hasil_pemeriksaan.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
assert summary['semua_lulus'], [c for c in checks if not c['lulus']]

readme = f'''# Data dummy penerimaan dan mahasiswa aktif

Seluruh catatan orang, identitas, pilihan prodi, hasil seleksi, registrasi, dan status aktif dalam folder ini merupakan simulasi untuk latihan analisis. Data ini bukan hasil penerimaan resmi dan tidak mengukur peluang lolos nyata.

## Isi folder

| Berkas | Jumlah baris | Arti satu baris |
|---|---:|---|
'''
grains = ['Satu pendaftaran pada satu jalur dan tahun; orang bisa berulang.', 'Satu hasil seleksi untuk setiap pendaftaran, termasuk yang tidak diterima.', 'Satu mahasiswa aktif pada snapshot 1 Oktober 2025.', 'Satu program studi.', 'Satu kelompok provinsi dalam klasifikasi latihan 34 wilayah.']
for (name, rows), grain in zip(tables.items(), grains):
    readme += f'| {name} | {len(rows):,} | {grain} |\n'
readme += f'''
Jumlah calon mahasiswa unik: {N_PEOPLE:,}. Pendaftaran diterima: {len(accepted):,}; angka ini menghitung pendaftaran, bukan orang unik. Orang diterima unik: {summary['orang_diterima_unik']:,}. Orang sudah daftar ulang: {len(registered):,}. Mahasiswa aktif: {len(active):,}.

## Format dan cara membaca

- CSV memakai pemisah titik koma (;), pengodean UTF-8 dengan BOM, dan satu baris header.
- Tanggal menggunakan YYYY-MM-DD. Sel kosong berarti tidak berlaku atau tidak tersedia sesuai kamus; bukan nol.
- Semua kode identitas dan referensi harus dibaca sebagai teks. Semua kode baru bersifat dummy.
- Python/pandas: `pd.read_csv('1_pendaftar_penerimaan.csv', sep=';', encoding='utf-8-sig', dtype={{'ID_Pendaftar': str, 'ID_Pendaftaran': str}})`.
- Saat membuka di Excel, pilih pemisah titik koma jika kolom tidak langsung terpisah.

## Sumber acuan dan batas penggunaannya

Sumber kategori: ../data/1_profil_mahasiswa_umum.csv, berisi {len(profiles):,} baris. Nama 44 prodi, hubungan dengan 15 fakultas, serta kategori jenis kelamin, angkatan dan provinsi berasal dari tabel tersebut. Profil sumber diambil ulang secara acak untuk membentuk kombinasi kategori; ID dan baris orang sumber tidak disalin ke keluaran. Distribusi hasil mendekati referensi, tidak dipaksa identik.

Empat CSV sumber lainnya tidak dipakai sebagai fitur karena skema baru tidak memuat prestasi, generasi pertama kuliah, sosial ekonomi, atau riwayat IPK. Kelima berkas sumber diperiksa hash-nya sebelum dan sesudah pembuatan untuk memastikan tidak berubah.

## Asumsi simulasi

1. Ada {N_PEOPLE:,} orang sintetis, tahun penerimaan 2019-2025. Satu orang hanya berada dalam satu tahun penerimaan dan dapat mengikuti paling banyak tiga jalur berurutan: SNBP, SNBT, Mandiri. Peluang jalur awal adalah 30%, 45%, 25%.
2. Nama jalur tersebut hanya label seragam untuk latihan lintas tahun; tidak dimaksudkan sebagai nama historis resmi untuk setiap tahun. Seluruh pendaftaran berstatus Selesai; tidak ada berkas belum lengkap atau hasil tertunda.
3. Peluang simulasi diterima dasar adalah SNBP 25%, SNBT 34%, Mandiri 48%, ditambah variasi acak tetap per prodi antara -6,5 dan +6,5 poin persentase serta variasi tahun sebesar (tahun-2022) x 0,6 poin persentase. Angka-angka ini dipilih untuk membentuk data latihan dan tidak diestimasi dari sumber.
4. Dari peserta diterima, peluang simulasi daftar ulang adalah SNBP 82%, SNBT 86%, Mandiri 76%. Jika belum daftar ulang atau tidak diterima, peluang melanjutkan ke jalur berikutnya adalah 45%. Setelah daftar ulang, orang tidak mengikuti jalur selanjutnya. Satu orang paling banyak memiliki satu NIM.
5. Sekitar 12% pendaftaran tidak memiliki pilihan kedua. Jika diterima dan memiliki pilihan kedua, peluang prodi diterima dialihkan ke pilihan kedua adalah 18%. Proses ini tidak meniru sistem pemeringkatan, kuota, atau mekanisme seleksi resmi.
6. Mahasiswa aktif adalah subset orang yang sudah daftar ulang, diamati pada 1 Oktober 2025, tahun akademik 2025/2026 Ganjil. Peluang aktif menurut selisih tahun 2025-angkatan adalah 98%, 96%, 93%, 88%, 55%, 20%, 8% untuk selisih 0 hingga 6 tahun. Pola ini merupakan asumsi simulasi, bukan tingkat retensi hasil observasi.
7. Tidak muncul di tabel aktif hanya berarti tidak aktif pada snapshot simulasi. Penyebabnya tidak tersedia; jangan otomatis menyimpulkan putus kuliah atau gagal registrasi.
8. Semua prodi diberi jenjang S1 sebagai asumsi latihan karena kolom jenjang tidak ada pada sumber. Prodi mahasiswa aktif sama dengan prodi diterima; perpindahan prodi tidak disimulasikan.
9. Tanggal lahir, sekolah, dan tanggal registrasi disimulasikan. Usia dihitung pada 1 Agustus tahun penerimaan. Tanggal registrasi tidak mewakili jadwal resmi.
10. Seed acak tetap: {SEED}. Hasil dapat direproduksi menggunakan skrip pendukung dengan versi Python yang sama.

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

KAMUS_DATA.md menjelaskan seluruh kolom, tipe, kunci dan arti nilai kosong. _pendukung/hasil_pemeriksaan.json menyimpan jumlah baris, ringkasan per tahun, hash sumber/keluaran, dan {len(checks)} pemeriksaan konsistensi yang semuanya lulus. Skrip _pendukung/buat_dummy_penerimaan.py disertakan agar simulasi dapat ditinjau; jalankan dengan `--output` menuju folder baru jika ingin mengulang.
'''
(OUTPUT / 'README.md').write_text(readme, encoding='utf-8')
dictionary = '# Kamus data dummy\n\nStruktur ini adalah rancangan simulasi berdasarkan percakapan, bukan skema resmi penyelenggara. Seluruh ID baru merupakan identitas dummy. Aturan generasi, sumber kategori, dan pemetaan wilayah dijelaskan pada README.md.\n\n'
for (name, fields), grain in zip(schemas.items(), grains):
    dictionary += f'## {name}\n\n{grain}\n\n| Kolom | Tipe | Keterangan |\n|---|---|---|\n'
    for field, dtype, desc in fields:
        dictionary += f'| {field} | {dtype} | {desc} |\n'
    dictionary += '\n'
(OUTPUT / 'KAMUS_DATA.md').write_text(dictionary, encoding='utf-8')
# Keep an identical, independently runnable generator with source/output options.
(support / 'buat_dummy_penerimaan.py').write_text(Path(__file__).read_text(encoding='utf-8'), encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k in ['jumlah_baris','calon_mahasiswa_unik','pendaftaran_diterima','orang_diterima_unik','orang_sudah_daftar_ulang','mahasiswa_aktif','jumlah_pemeriksaan','semua_lulus']}, ensure_ascii=False, indent=2))
print('OUTPUT', OUTPUT)
