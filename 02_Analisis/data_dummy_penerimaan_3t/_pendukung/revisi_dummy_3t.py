import argparse
import ast
import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(r'C:\Users\ACER\OneDrive\Dokumen\COMPETITION\CAMPUS DATA WEEK')
parser = argparse.ArgumentParser(description='Merevisi dummy ke lima tabel sesuai deskripsi final.')
parser.add_argument('--previous', type=Path, default=ROOT/'02_Analisis/data_dummy_penerimaan_34_wilayah')
parser.add_argument('--source', type=Path, default=ROOT/'02_Analisis/data')
parser.add_argument('--output', type=Path, default=ROOT/'02_Analisis/data_dummy_penerimaan_3t')
parser.add_argument('--resume-incomplete', action='store_true', help='Melanjutkan keluaran parsial yang belum memiliki README')
parser.add_argument('--refresh-generated', action='store_true', help='Membangun ulang keluaran generator jika hash CSV belum diubah')
args = parser.parse_args()
previous, source, output = args.previous.resolve(), args.source.resolve(), args.output.resolve()
rng = random.Random(20261028)


def load(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


source_hash = {str(f): digest(f) for p in [source, previous] for f in p.rglob('*') if f.is_file()}
if output.exists():
    expected_partial={'1_pendaftar_penerimaan.csv','2_hasil_seleksi_daftar_ulang.csv','3_mahasiswa_aktif.csv','4_ref_program_studi.csv','5_ref_wilayah_3t.csv','_pendukung/hasil_pemeriksaan.json'}
    actual_partial={f.relative_to(output).as_posix() for f in output.rglob('*') if f.is_file()}
    complete_files=expected_partial|{'README.md','KAMUS_DATA.md','REVISI_DARI_GAMBAR.md','_pendukung/revisi_dummy_3t.py'}
    safe_refresh=False
    if args.refresh_generated and actual_partial==complete_files:
        old_report=json.loads((output/'_pendukung/hasil_pemeriksaan.json').read_text(encoding='utf-8'))
        safe_refresh=all(digest(output/name)==value for name,value in old_report['sha256_output'].items())
    if not safe_refresh and (not args.resume_incomplete or actual_partial!=expected_partial):
        raise SystemExit(f'Folder keluaran sudah ada; tidak ditimpa: {output}')
old_apps = load(previous/'1_pendaftar_penerimaan.csv')
old_results = {r['ID_Pendaftaran']:r for r in load(previous/'2_hasil_seleksi_daftar_ulang.csv')}
old_active = {r['NIM'] for r in load(previous/'3_mahasiswa_aktif.csv')}
old_programs = load(previous/'4_ref_program_studi.csv')
old_provinces = {r['Kode_Provinsi']:r['Nama_Provinsi'] for r in load(previous/'5_ref_wilayah_34.csv')}
profiles = load(source/'1_profil_mahasiswa_umum.csv')
province_frequency = Counter(r['Provinsi_Asal'] for r in profiles)
merge = {'Papua Selatan':'Papua','Papua Tengah':'Papua','Papua Pegunungan':'Papua','Papua Barat Daya':'Papua Barat'}
province_groups = defaultdict(list)
for name, count in province_frequency.items():
    province_groups[merge.get(name, name)].extend([name]*count)

# 8 fictional districts per source province; 2 of each 8 receive a dummy 3T label.
regions, regions_by_province = [], defaultdict(list)
for pindex, province in enumerate(sorted(province_frequency), 1):
    dummy_3t_positions = set(rng.sample(range(1, 9), 2))
    for district in range(1, 9):
        kind = 'Kabupaten' if district <= 6 else 'Kota'
        region = dict(Kode_Wilayah=f'DMY-WIL-{pindex:02d}{district:02d}',
            Nama_Kabupaten_Kota=f'{kind} Dummy {district:02d} - {province}',
            Jenis_Wilayah=kind, Kode_Provinsi=f'DMY-PRV-{pindex:02d}',
            Nama_Provinsi=province, Status_3T='Ya' if district in dummy_3t_positions else 'Tidak')
        regions.append(region)
        regions_by_province[province].append(region)

apps_by_person = defaultdict(list)
for app in old_apps:
    apps_by_person[app['ID_Pendaftar']].append(app)
selected_apps, admitted_rows, student_rows = [], [], []
conversion = Counter()
for person, attempts in sorted(apps_by_person.items()):
    registered_attempts = [r for r in attempts if old_results[r['ID_Pendaftaran']]['Status_Daftar_Ulang']=='Sudah']
    admitted_attempts = [r for r in attempts if old_results[r['ID_Pendaftaran']]['Status_Seleksi']=='Diterima']
    chosen = (registered_attempts or admitted_attempts or attempts)[-1]
    conversion['pendaftar_dengan_jalur_berulang_diringkas'] += len(attempts)>1
    result = old_results[chosen['ID_Pendaftaran']]
    old_province = old_provinces[chosen['Kode_Wilayah_Asal']]
    province = rng.choice(province_groups[old_province])
    region = rng.choice(regions_by_province[province])
    entry = {k:chosen[k] for k in ['ID_Pendaftar','Tahun_Penerimaan','Jalur_Penerimaan','Jenis_Kelamin','Tanggal_Lahir','Usia_Saat_Daftar']}
    entry.update(Kode_Wilayah_Asal=region['Kode_Wilayah'],
        Asal_Sekolah=f"SEKOLAH-DUMMY-{region['Kode_Wilayah']}-{rng.randint(1,20):02d}",
        Kode_Prodi_Pilihan_1=chosen['Kode_Prodi_Pilihan_1'],
        Kode_Prodi_Pilihan_2=chosen['Kode_Prodi_Pilihan_2'], Status_Pendaftaran='Selesai')
    selected_apps.append(entry)
    if result['Status_Seleksi'] != 'Diterima':
        continue
    registered = result['Status_Daftar_Ulang']=='Sudah'
    student_id = f'MHS-DMY-{len(student_rows)+1:06d}' if registered else ''
    admitted = dict(ID_Pendaftar=person, Tahun_Penerimaan=entry['Tahun_Penerimaan'],
        Jalur_Penerimaan=entry['Jalur_Penerimaan'], Status_Seleksi='Diterima',
        Kode_Prodi_Diterima=result['Kode_Prodi_Diterima'],
        Status_Daftar_Ulang='Sudah' if registered else 'Tidak Daftar Ulang',
        Tanggal_Daftar_Ulang=result['Tanggal_Daftar_Ulang'], ID_Mahasiswa=student_id)
    admitted_rows.append(admitted)
    if registered:
        if result['NIM'] in old_active:
            status='Aktif'
        elif int(entry['Tahun_Penerimaan'])<=2021:
            status=rng.choices(['Cuti','Lulus','Non-Aktif/DO'],[0.25,0.60,0.15])[0]
        else:
            status=rng.choices(['Cuti','Non-Aktif/DO'],[0.65,0.35])[0]
        student_rows.append(dict(ID_Mahasiswa=student_id, ID_Pendaftar=person,
            Angkatan=entry['Tahun_Penerimaan'], Tahun_Akademik='2025/2026',
            Semester_Pelaporan='Ganjil', Tanggal_Snapshot='2025-10-01',
            Kode_Prodi=result['Kode_Prodi_Diterima'], Jenis_Kelamin=entry['Jenis_Kelamin'],
            Kode_Wilayah_Asal=region['Kode_Wilayah'], Jalur_Masuk=entry['Jalur_Penerimaan'],
            Status_Mahasiswa=status))

years = sorted({int(r['Tahun_Penerimaan']) for r in selected_apps})
programs = [dict(Kode_Prodi=r['Kode_Prodi'], Tahun_Penerimaan=str(year),
    Nama_Prodi=r['Nama_Prodi'], Kode_Fakultas=r['Kode_Fakultas'],
    Nama_Fakultas=r['Nama_Fakultas'], Jenjang=r['Jenjang']) for r in old_programs for year in years]

# Small, documented preprocessing exercise; never corrupt the keys or outcomes.
missing_school_ids = set(rng.sample([r['ID_Pendaftar'] for r in selected_apps],120))
spaced_gender_ids = set(rng.sample([r['ID_Pendaftar'] for r in selected_apps],60))
for row in selected_apps:
    if row['ID_Pendaftar'] in missing_school_ids:
        row['Asal_Sekolah']=''
    if row['ID_Pendaftar'] in spaced_gender_ids:
        row['Jenis_Kelamin']=' '+row['Jenis_Kelamin']+' '

tables = {
    '1_pendaftar_penerimaan.csv': selected_apps,
    '2_hasil_seleksi_daftar_ulang.csv': admitted_rows,
    '3_mahasiswa_aktif.csv': student_rows,
    '4_ref_program_studi.csv': programs,
    '5_ref_wilayah_3t.csv': regions,
}
output.mkdir(exist_ok=args.resume_incomplete or args.refresh_generated)
support = output/'_pendukung'
support.mkdir(exist_ok=args.resume_incomplete or args.refresh_generated)
for name, rows in tables.items():
    with (output/name).open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

# Reopen all saved tables and verify grain, coverage and foreign keys.
saved={name:load(output/name) for name in tables}
a,b,c,d,e=saved.values()
ai={r['ID_Pendaftar']:r for r in a}
bi={r['ID_Pendaftar']:r for r in b}
ci={r['ID_Mahasiswa']:r for r in c}
di={(r['Kode_Prodi'],r['Tahun_Penerimaan']):r for r in d}
ei={r['Kode_Wilayah']:r for r in e}
registered=[r for r in b if r['Status_Daftar_Ulang']=='Sudah']
checks=[]


def check(label, good):
    checks.append(dict(pemeriksaan=label,lulus=bool(good)))


check('Tabel 1: tepat satu baris per pendaftar',len(a)==len(ai)==12000)
check('Tabel 2: kunci ID_Pendaftar unik dan hanya peserta diterima',len(b)==len(bi) and all(r['Status_Seleksi']=='Diterima' for r in b))
check('Tabel 2 adalah subset ketat tabel 1',set(bi)<set(ai))
check('Tabel 3: kunci ID_Mahasiswa dan ID_Pendaftar unik',len(c)==len(ci)==len({r['ID_Pendaftar'] for r in c}))
check('Cakupan tabel 3 persis seluruh orang yang sudah daftar ulang',{r['ID_Pendaftar'] for r in c}=={r['ID_Pendaftar'] for r in registered})
check('Tabel 3 subset ketat tabel 2',{r['ID_Pendaftar'] for r in c}<set(bi))
check('ID_Mahasiswa tabel 2 cocok dengan tabel 3',all(r['ID_Mahasiswa'] in ci and ci[r['ID_Mahasiswa']]['ID_Pendaftar']==r['ID_Pendaftar'] for r in registered))
check('Peserta belum daftar ulang tidak memiliki ID_Mahasiswa atau tanggal',all(not r['ID_Mahasiswa'] and not r['Tanggal_Daftar_Ulang'] for r in b if r['Status_Daftar_Ulang']!='Sudah'))
check('Tahun dan jalur konsisten dari tabel 1 ke 2',all(all(r[k]==ai[r['ID_Pendaftar']][k] for k in ['Tahun_Penerimaan','Jalur_Penerimaan']) for r in b))
check('Tabel 4: kunci gabungan unik, 44 prodi x 7 tahun',len(d)==len(di)==308 and len({r['Kode_Prodi'] for r in d})==44)
check('Pilihan prodi valid pada tahun penerimaan terkait',all((r['Kode_Prodi_Pilihan_1'],r['Tahun_Penerimaan']) in di and (not r['Kode_Prodi_Pilihan_2'] or (r['Kode_Prodi_Pilihan_2'],r['Tahun_Penerimaan']) in di) for r in a))
check('Prodi diterima valid dan termasuk pilihan',all((r['Kode_Prodi_Diterima'],r['Tahun_Penerimaan']) in di and r['Kode_Prodi_Diterima'] in [ai[r['ID_Pendaftar']]['Kode_Prodi_Pilihan_1'],ai[r['ID_Pendaftar']]['Kode_Prodi_Pilihan_2']] for r in b))
check('Mahasiswa: prodi angkatan jalur sesuai hasil seleksi',all(r['Kode_Prodi']==bi[r['ID_Pendaftar']]['Kode_Prodi_Diterima'] and r['Angkatan']==bi[r['ID_Pendaftar']]['Tahun_Penerimaan'] and r['Jalur_Masuk']==bi[r['ID_Pendaftar']]['Jalur_Penerimaan'] for r in c))
check('Tabel 5: 304 kabupaten/kota sintetis dengan kunci wilayah unik',len(e)==len(ei)==304 and len({r['Nama_Provinsi'] for r in e})==38)
check('Seluruh FK wilayah valid',all(r['Kode_Wilayah_Asal'] in ei for r in a+c))
check('Wilayah dan gender mahasiswa konsisten setelah trim',all(r['Kode_Wilayah_Asal']==ai[r['ID_Pendaftar']]['Kode_Wilayah_Asal'] and r['Jenis_Kelamin'].strip()==ai[r['ID_Pendaftar']]['Jenis_Kelamin'].strip() for r in c))
check('Kedua status 3T tersedia dan tidak ada status kosong',set(r['Status_3T'] for r in e)=={'Ya','Tidak'} and all(r['Status_3T'] for r in e))
check('Wilayah pendaftar subset referensi; referensi tanpa pendaftar dibolehkan',{r['Kode_Wilayah_Asal'] for r in a}<=set(ei))
check('Registrasi memiliki tanggal yang sesuai tahun dan sebelum snapshot',all(date.fromisoformat(r['Tanggal_Daftar_Ulang']).year==int(r['Tahun_Penerimaan']) and date.fromisoformat(r['Tanggal_Daftar_Ulang'])<=date(2025,10,1) for r in registered))
check('Jumlah mahasiswa berstatus Aktif dipertahankan dari dummy lama',sum(r['Status_Mahasiswa']=='Aktif' for r in c)==len(old_active))
check('Status Lulus hanya untuk angkatan yang telah menempuh minimal empat tahun',all(int(r['Angkatan'])<=2021 for r in c if r['Status_Mahasiswa']=='Lulus'))
check('Latihan missing value tepat 120 asal sekolah kosong',sum(not r['Asal_Sekolah'] for r in a)==120)
check('Latihan whitespace tepat 60 gender dengan spasi tepi',sum(r['Jenis_Kelamin']!=r['Jenis_Kelamin'].strip() for r in a)==60)
check('CSV BOM UTF-8 dan lebar baris konsisten',all((output/name).read_bytes().startswith(b'\xef\xbb\xbf') and all(None not in row and all(v is not None for v in row.values()) for row in rows) for name,rows in saved.items()))
check('Sumber dan dummy sebelumnya tidak berubah',all(digest(Path(path))==value for path,value in source_hash.items()))
summary=dict(versi='revisi_3t_sesuai_deskripsi_gambar',seed=20261028,
    jumlah_baris={name:len(rows) for name,rows in saved.items()},
    jumlah_pendaftar_unik=len(ai),jumlah_diterima=len(b),jumlah_daftar_ulang=len(c),
    status_mahasiswa=dict(Counter(r['Status_Mahasiswa'] for r in c)),
    status_3t_referensi=dict(Counter(r['Status_3T'] for r in e)),
    status_3t_pendaftar=dict(Counter(ei[r['Kode_Wilayah_Asal']]['Status_3T'] for r in a)),
    wilayah_referensi_tanpa_pendaftar=sorted(set(ei)-{r['Kode_Wilayah_Asal'] for r in a}),
    jumlah_pemeriksaan=len(checks),semua_lulus=all(r['lulus'] for r in checks),
    pemeriksaan=checks,perubahan=dict(conversion),sha256_sumber=source_hash,
    sha256_output={name:digest(output/name) for name in saved},
    catatan='Semua label 3T, kabupaten/kota, dan kode wilayah adalah simulasi. Tidak ada penetapan resmi 3T.')
(support/'hasil_pemeriksaan.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
assert summary['semua_lulus'],[r for r in checks if not r['lulus']]

definitions={
 'ID_Pendaftar':('Teks','PK tabel 1 dan 2; FK tabel 3. Satu ID mewakili satu orang dalam latihan ini.'),
 'Tahun_Penerimaan':('Bilangan bulat','2019-2025; bagian kunci gabungan referensi prodi.'),
 'Jalur_Penerimaan':('Kategori','SNBP / SNBT / Mandiri. Label simulasi diseragamkan lintas tahun, bukan nama historis resmi.'),
 'Jenis_Kelamin':('Kategori','Laki-laki / Perempuan. Sebanyak 60 baris pendaftar memiliki spasi tepi untuk latihan trim.'),
 'Tanggal_Lahir':('Tanggal','Tanggal lahir dummy; YYYY-MM-DD.'),
 'Usia_Saat_Daftar':('Bilangan bulat','Usia pada 1 Agustus tahun penerimaan.'),
 'Kode_Wilayah_Asal':('Teks','FK ke Kode_Wilayah tabel 5; tingkat kabupaten/kota, bukan provinsi.'),
 'Asal_Sekolah':('Teks','Nama sekolah sintetis. Kosong pada 120 baris berarti tidak tercatat.'),
 'Kode_Prodi_Pilihan_1':('Teks','Pilihan pertama. Gabungkan dengan tabel 4 memakai kode ini DAN Tahun_Penerimaan.'),
 'Kode_Prodi_Pilihan_2':('Teks','Pilihan kedua; kosong berarti tidak memilih. Kunci join juga harus menyertakan Tahun_Penerimaan.'),
 'Status_Pendaftaran':('Kategori','Selesai untuk semua baris; tidak ada pendaftaran belum lengkap pada simulasi.'),
 'Status_Seleksi':('Kategori','Diterima untuk seluruh tabel 2. Ketidakhadiran di tabel 2 berarti tidak diterima hanya menurut kontrak dummy ini.'),
 'Kode_Prodi_Diterima':('Teks','Salah satu prodi pilihan; FK bersama Tahun_Penerimaan ke tabel 4.'),
 'Status_Daftar_Ulang':('Kategori','Sudah / Tidak Daftar Ulang; mencakup hasil registrasi peserta yang diterima.'),
 'Tanggal_Daftar_Ulang':('Tanggal','Tanggal sintetis YYYY-MM-DD; kosong jika tidak daftar ulang.'),
 'ID_Mahasiswa':('Teks','MHS-DMY-######. PK tabel 3, terisi di tabel 2 hanya jika sudah daftar ulang.'),
 'Angkatan':('Bilangan bulat','Tahun masuk; sama dengan Tahun_Penerimaan peserta terkait. Gunakan sebagai padanan tahun saat join referensi prodi.'),
 'Tahun_Akademik':('Teks','2025/2026 untuk seluruh tabel 3.'),
 'Semester_Pelaporan':('Kategori','Ganjil untuk seluruh tabel 3; bukan semester ke berapa.'),
 'Tanggal_Snapshot':('Tanggal','2025-10-01; tanggal pengamatan status simulasi.'),
 'Kode_Prodi':('Teks','Kode dummy PRD-###. Di tabel 4 hanya unik bersama Tahun_Penerimaan. Di tabel 3 gunakan bersama Angkatan.'),
 'Jalur_Masuk':('Kategori','Jalur penerimaan saat peserta mendaftar ulang.'),
 'Status_Mahasiswa':('Kategori','Aktif / Cuti / Lulus / Non-Aktif/DO. Status non-Aktif tambahan merupakan asumsi, bukan hasil observasi.'),
 'Nama_Prodi':('Teks','44 kategori nama prodi berasal dari referensi lama.'),
 'Kode_Fakultas':('Teks','FAK-##; kode sintetis.'),
 'Nama_Fakultas':('Teks','Hubungan prodi dengan 15 fakultas dipertahankan dari sumber.'),
 'Jenjang':('Kategori','S1 untuk seluruh prodi sebagai asumsi latihan, bukan verifikasi resmi.'),
 'Kode_Wilayah':('Teks','PK DMY-WIL-####; kode sintetis kabupaten/kota, bukan kode BPS/Kemendagri.'),
 'Nama_Kabupaten_Kota':('Teks','Nama kabupaten/kota fiktif berlabel Dummy. Tidak dapat dipasangkan langsung ke peta wilayah nyata.'),
 'Jenis_Wilayah':('Kategori','Kabupaten / Kota; klasifikasi fiktif.'),
 'Kode_Provinsi':('Teks','DMY-PRV-##; kode sintetis provinsi, bukan kode resmi.'),
 'Nama_Provinsi':('Teks','38 nama kategori provinsi dari profil sumber; kategori Papua tidak lagi digabung menjadi 34.'),
 'Status_3T':('Kategori','Ya / Tidak; label dummy yang ditetapkan acak, tetap per wilayah. Bukan klasifikasi resmi 3T.'),
}
grains=[('Satu pendaftar','ID_Pendaftar'),('Satu pendaftar yang diterima','ID_Pendaftar'),
    ('Satu mahasiswa yang sudah daftar ulang','ID_Mahasiswa'),
    ('Satu prodi pada satu tahun','Kode_Prodi + Tahun_Penerimaan'),('Satu kabupaten/kota','Kode_Wilayah')]
dictionary='# Kamus data dummy revisi 3T\n\nRancangan kolom merupakan asumsi latihan. Gambar acuan mengonfirmasi nama tabel, unit baris dan kunci, tetapi tidak memuat semua kolom atau definisi resmi status 3T.\n\n'
for (name,rows),(grain,key) in zip(saved.items(),grains):
    dictionary+=f'## {name}\n\nUnit: {grain}. Kunci: {key}. Jumlah baris: {len(rows):,}.\n\n| Kolom | Tipe | Arti dan aturan |\n|---|---|---|\n'
    for field in rows[0]:
        dtype,description=definitions[field]
        dictionary+=f'| {field} | {dtype} | {description} |\n'
    dictionary+='\n'
(output/'KAMUS_DATA.md').write_text(dictionary,encoding='utf-8')
readme=f'''# Data dummy penerimaan: revisi referensi wilayah 3T

Gunakan folder ini untuk latihan struktur sesuai gambar final. Folder data_dummy_penerimaan_34_wilayah adalah versi lama dan tidak mengikuti struktur final. Semua data hasil seleksi, registrasi, sekolah, kabupaten/kota, kode dan status 3T merupakan simulasi. Dataset ini bukan data resmi dan tidak untuk menetapkan kondisi wilayah nyata.

## Struktur sesuai gambar

| Berkas | Unit baris | Kunci | Jumlah baris |
|---|---|---|---:|
'''
for (name,rows),(grain,key) in zip(saved.items(),grains):
    readme+=f'| {name} | {grain} | {key} | {len(rows):,} |\n'
readme+=f'''
## Arti ref_wilayah_3t

Tabel ini diasumsikan sebagai referensi kabupaten/kota beserta Status_3T, bukan daftar individu pendaftar. Hubungkan Kode_Wilayah_Asal pada pendaftar/mahasiswa dengan Kode_Wilayah referensi, kemudian bandingkan Status_3T = Ya dan Tidak. Kehadiran kedua kategori dipilih agar latihan perbandingan dapat dilakukan. Apakah tabel final memuat semua wilayah atau hanya wilayah 3T belum dapat dipastikan dari gambar; ikuti kamus final saat tersedia.

Terdapat 304 kabupaten/kota fiktif, delapan untuk setiap 38 kategori provinsi sumber. Dua dari delapan wilayah per provinsi diberi label Ya secara acak, sehingga 76 wilayah berlabel 3T dan 228 non-3T. Seluruh nama kabupaten/kota memuat kata Dummy; label 3T tidak berasal dari penetapan pemerintah. Tidak ada pengaruh 3T yang sengaja ditambahkan pada peluang seleksi atau registrasi. Perbedaan hasil antarlabel dalam dummy tidak boleh dianggap bukti ketimpangan nyata.

Nama 38 provinsi diambil dari 1_profil_mahasiswa_umum.csv. Pemetaan 34 wilayah lama dihentikan. Untuk orang yang sebelumnya masuk kelompok Papua/Papua Barat, kategori provinsi dipilih ulang dari kategori sumber yang dahulu digabung, mengikuti frekuensinya. Asal kabupaten/kota seluruh orang ditetapkan secara sintetis. Data ini mendukung latihan penggabungan dan clustering indikator wilayah; analisis peta lokasi nyata membutuhkan referensi geografis yang benar.

## Perubahan dari dummy sebelumnya

1. Tabel 1 sekarang tepat 12.000 pendaftar unik. ID_Pendaftaran dihapus. Untuk orang dengan beberapa jalur lama, dipilih pendaftaran yang berhasil daftar ulang; jika tidak ada, pendaftaran terakhir yang diterima; jika tidak ada, pendaftaran terakhir. Ini aturan konversi latihan, bukan mekanisme seleksi resmi. Jumlah jalur asal tidak lagi dapat dianalisis sebagai seluruh riwayat pendaftaran.
2. Tabel 2 hanya berisi {len(b):,} peserta diterima. Semua ID_Pendaftar unik; peserta tidak diterima tidak memiliki baris di tabel ini. Status_Daftar_Ulang membedakan Sudah dan Tidak Daftar Ulang.
3. Tabel 3 berisi seluruh {len(c):,} orang yang sudah daftar ulang, sesuai unit pada gambar. Kuncinya ID_Mahasiswa. Nama berkas tetap mahasiswa_aktif agar mengikuti acuan, tetapi tabel ini tidak boleh langsung dihitung sebagai seluruh mahasiswa berstatus aktif. Gunakan filter Status_Mahasiswa = Aktif untuk mendapatkan {len(old_active):,} orang aktif pada snapshot 1 Oktober 2025. Penyebab status lain tidak dapat disimpulkan dari ketidakhadiran pada tabel lama; rinciannya diisi sebagai asumsi latihan.
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

KAMUS_DATA.md menjelaskan seluruh kolom. _pendukung/hasil_pemeriksaan.json menyimpan hash, jumlah baris dan {len(checks)} pemeriksaan konsistensi. _pendukung/revisi_dummy_3t.py mereproduksi keluaran dari versi sebelumnya; gunakan --output ke folder baru. REVISI_DARI_GAMBAR.md membedakan isi yang dikonfirmasi gambar dengan asumsi latihan.
'''
(output/'README.md').write_text(readme,encoding='utf-8')
notes='''# Dasar revisi dari gambar

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
'''
(output/'REVISI_DARI_GAMBAR.md').write_text(notes,encoding='utf-8')
code=Path(__file__).read_text(encoding='utf-8')
ast.parse(code)
(support/'revisi_dummy_3t.py').write_text(code,encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k in ['jumlah_baris','jumlah_pendaftar_unik','jumlah_diterima','jumlah_daftar_ulang','status_mahasiswa','status_3t_referensi','jumlah_pemeriksaan','semua_lulus']},ensure_ascii=False,indent=2))
print('OUTPUT',output)
