from pathlib import Path
import csv,json,collections,zipfile,html,hashlib
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
import pypdfium2 as pdfium
from pypdf import PdfReader

ROOT=Path.cwd();OUT=ROOT/'05_Latihan_Final/Hospital_Patient_Records';RAW=OUT/'data_asli';VIS=OUT/'visualisasi';VIS.mkdir(exist_ok=True)
AUD=json.loads((OUT/'hasil_pemeriksaan.json').read_text())
NAMES=['patients','encounters','procedures','payers','organizations']
DATA={n:list(csv.DictReader((RAW/f'{n}.csv').open(encoding='utf-8-sig',newline=''))) for n in NAMES}
SOURCE='https://mavenanalytics.io/challenges/maven-hospital-challenge'
DOWNLOAD='https://maven-datasets.s3.amazonaws.com/Hospital+Patient+Records/Hospital+Patient+Records.zip'
with zipfile.ZipFile(OUT/'Hospital_Patient_Records_original.zip') as z:
 for n in ['create_hospital_db.sql','hospital_analytics_questions.sql']:
  dst=OUT/'skrip_sumber'/n;dst.parent.mkdir(exist_ok=True);dst.write_bytes(z.read(n))
# Source scripts are preserved as files only; never executed.
grain={'patients':'Satu pasien sintetis','encounters':'Satu kunjungan / episode layanan','procedures':'Satu catatan tindakan / prosedur','payers':'Satu penanggung biaya, termasuk NO_INSURANCE','organizations':'Satu organisasi penyedia layanan'}
base={
'Id':'ID unik tabel; kunci utama.', 'START':'Waktu mulai layanan, format ISO 8601 UTC.','STOP':'Waktu selesai layanan, format ISO 8601 UTC.',
'PATIENT':'ID pasien; merujuk patients.Id.','ENCOUNTER':'ID kunjungan; merujuk encounters.Id.','PAYER':'ID penanggung biaya; merujuk payers.Id.','ORGANIZATION':'ID organisasi; merujuk organizations.Id.',
'ENCOUNTERCLASS':'Kategori layanan yang tercatat; enam kategori aktual.','CODE':'Kode layanan atau tindakan SNOMED-CT. Simpan sebagai teks.','DESCRIPTION':'Deskripsi kode layanan atau tindakan.',
'BASE_ENCOUNTER_COST':'Biaya dasar kunjungan, tidak termasuk rincian layanan tambahan (USD).','TOTAL_CLAIM_COST':'Total biaya kunjungan beserta rincian layanannya (USD).','PAYER_COVERAGE':'Nilai biaya yang tercatat ditanggung penjamin (USD).','REASONCODE':'Kode alasan / kondisi SNOMED-CT; dapat kosong.','REASONDESCRIPTION':'Deskripsi alasan / kondisi; dapat kosong.','BASE_COST':'Biaya item prosedur (USD).',
'BIRTHDATE':'Tanggal lahir pasien (YYYY-MM-DD).','DEATHDATE':'Tanggal kematian bila tercatat; kosong bukan nilai nol.','PREFIX':'Sapaan / gelar sebelum nama.','FIRST':'Nama depan sintetis.','LAST':'Nama keluarga sintetis.','SUFFIX':'Gelar / penanda setelah nama; opsional.','MAIDEN':'Nama sebelum menikah; opsional.','MARITAL':'Status pernikahan; M = menikah, S = lajang.','RACE':'Kategori ras yang tercatat.','ETHNICITY':'Kategori etnis yang tercatat.','GENDER':'Kode gender pada sumber; F = perempuan, M = laki-laki.','BIRTHPLACE':'Tempat lahir sintetis.',
'NAME':'Nama organisasi atau penanggung biaya.','ADDRESS':'Alamat yang tercatat.','CITY':'Kota pada alamat.','STATE':'Negara bagian pada alamat.','COUNTY':'Wilayah county pada alamat.','ZIP':'Kode pos; simpan sebagai teks agar nol di depan terjaga.','LAT':'Lintang lokasi.','LON':'Bujur lokasi.','STATE_HEADQUARTERED':'Negara bagian alamat kantor penanggung biaya.','PHONE':'Nomor telepon; simpan sebagai teks.'}
def dtype(n,k):
 if k in ['BASE_ENCOUNTER_COST','TOTAL_CLAIM_COST','PAYER_COVERAGE','BASE_COST','LAT','LON']:return 'Desimal'
 if k in ['START','STOP']:return 'Tanggal-waktu'
 if k in ['BIRTHDATE','DEATHDATE']:return 'Tanggal'
 return 'Teks / kategori'
def num(v):return f'{v:,}'.replace(',','.')
NAVY=colors.HexColor('#123047');TEAL=colors.HexColor('#007F82');GRAY=colors.HexColor('#617785');INK=colors.HexColor('#263B49');LIGHT=colors.HexColor('#EAF4F5');ORANGE=colors.HexColor('#D78735')

# Vector relationship diagram; keys and edges reflect the downloaded CSVs.
erdtmp=ROOT/'tmp/hospital_erd.pdf'
c=canvas.Canvas(str(erdtmp),pagesize=(1140,760));c.setFillColor(colors.white);c.rect(0,0,1140,760,fill=1,stroke=0)
c.setFillColor(NAVY);c.setFont('Helvetica-Bold',25);c.drawString(32,725,'Hospital Patient Records | Struktur relasi')
c.setFillColor(GRAY);c.setFont('Helvetica',12);c.drawString(32,702,'Lima tabel asli | 58 kolom | ID relasi diperiksa langsung pada CSV')
def box(x,y,w,h,name,lines):
 c.setStrokeColor(TEAL);c.setFillColor(colors.white);c.roundRect(x,y,w,h,8,fill=1,stroke=1)
 c.setFillColor(NAVY);c.roundRect(x,y+h-42,w,42,8,fill=1,stroke=0);c.rect(x,y+h-42,w,12,fill=1,stroke=0)
 c.setFillColor(colors.white);c.setFont('Helvetica-Bold',14);c.drawString(x+12,y+h-26,name)
 for i,line in enumerate(lines):c.setFillColor(INK);c.setFont('Helvetica',11);c.drawString(x+12,y+h-64-24*i,line)
def edge(points,lx,ly,label):
 c.setStrokeColor(TEAL);c.setLineWidth(1.6);p=c.beginPath();p.moveTo(*points[0])
 for q in points[1:]:p.lineTo(*q)
 c.drawPath(p);c.setFillColor(TEAL);c.setFont('Helvetica-Bold',11);c.drawString(lx,ly,label)
 # Directional arrow points to child table, with cardinalities given in labels.
 x,y=points[-1];px,py=points[-2];dx=x-px;dy=y-py;L=(dx*dx+dy*dy)**.5;ux,uy=dx/L,dy/L
 p=c.beginPath();p.moveTo(x,y);p.lineTo(x-8*ux+4*uy,y-8*uy-4*ux);p.lineTo(x-8*ux-4*uy,y-8*uy+4*ux);p.close();c.drawPath(p,fill=1,stroke=0)
box(30,440,265,235,'PATIENTS', ['974 baris | 20 kolom','PK  Id','BIRTHDATE, GENDER','RACE, ETHNICITY, MARITAL','CITY, ZIP, LAT, LON'])
box(30,135,265,190,'ORGANIZATIONS',['1 baris | 8 kolom','PK  Id','NAME, ADDRESS','CITY, STATE, ZIP'])
box(410,290,310,340,'ENCOUNTERS',['27.891 baris | 14 kolom','PK  Id','FK  PATIENT','FK  ORGANIZATION','FK  PAYER','START, STOP, ENCOUNTERCLASS','TOTAL_CLAIM_COST','PAYER_COVERAGE'])
box(820,490,270,185,'PAYERS',['10 baris | 7 kolom','PK  Id','NAME (termasuk NO_INSURANCE)','Alamat dan kontak'])
box(820,105,270,280,'PROCEDURES',['47.701 baris | 9 kolom','FK  ENCOUNTER','FK  PATIENT','START, STOP','CODE, DESCRIPTION','BASE_COST','Tidak ada kolom ID prosedur'])
edge([(295,550),(410,550)],310,563,'1 : N')
edge([(295,225),(355,225),(355,390),(410,390)],309,405,'1 : N')
edge([(820,555),(720,555)],748,568,'1 : N')
edge([(720,360),(770,360),(770,280),(820,280)],733,374,'1 : 0..N')
edge([(30,500),(15,500),(15,70),(955,70),(955,105)],425,79,'PATIENTS.Id -> PROCEDURES.PATIENT | 1 : 0..N')
c.setFillColor(GRAY);c.setFont('Helvetica',10);c.drawString(32,38,'PK = kunci utama; FK = kunci relasi logis. CSV tidak menerapkan constraint basis data secara otomatis.')
c.drawString(32,21,'Kolom di dalam kotak diringkas. Seluruh kolom dijelaskan dalam penjelasan_dataset.md dan PDF pendamping.')
c.save()
pdfium.PdfDocument(str(erdtmp))[0].render(scale=1.6).to_pil().save(VIS/'erd_hospital.png')

mermaid='''erDiagram
    patients ||--o{ encounters : memiliki
    organizations ||--o{ encounters : melayani
    payers ||--o{ encounters : tercatat_pada
    encounters ||--o{ procedures : memuat
    patients ||--o{ procedures : menjalani
    patients {
        string Id PK
        date BIRTHDATE
        string GENDER
    }
    encounters {
        string Id PK
        string PATIENT FK
        string ORGANIZATION FK
        string PAYER FK
        datetime START
        datetime STOP
        decimal TOTAL_CLAIM_COST
        decimal PAYER_COVERAGE
    }
    procedures {
        string PATIENT FK
        string ENCOUNTER FK
        string CODE
        decimal BASE_COST
    }
    payers {
        string Id PK
        string NAME
    }
    organizations {
        string Id PK
        string NAME
    }
'''
(VIS/'erd_hospital.mmd').write_text(mermaid,encoding='utf-8')

# Two descriptive charts rendered with vector drawing primitives.
charttmp=ROOT/'tmp/hospital_overview.pdf'
c=canvas.Canvas(str(charttmp),pagesize=(1000,790));c.setFillColor(colors.white);c.rect(0,0,1000,790,fill=1,stroke=0)
c.setFillColor(NAVY);c.setFont('Helvetica-Bold',24);c.drawString(35,752,'Gambaran dataset | Data sintetis')
c.setFillColor(GRAY);c.setFont('Helvetica',11);c.drawString(35,730,'Dihitung dari CSV asli. Satuan utama: pasien, kunjungan, dan catatan prosedur.')
for i,(label,value) in enumerate([('Pasien',974),('Kunjungan',27891),('Catatan prosedur',47701),('Penanggung biaya',10)]):
 x=35+240*i;c.setFillColor(LIGHT);c.roundRect(x,635,220,70,6,fill=1,stroke=0);c.setFillColor(TEAL);c.setFont('Helvetica-Bold',22);c.drawString(x+14,670,num(value));c.setFont('Helvetica',11);c.setFillColor(INK);c.drawString(x+14,650,label)
c.setFillColor(NAVY);c.setFont('Helvetica-Bold',16);c.drawString(35,600,'Komposisi jenis kunjungan')
classes=sorted(AUD['encounter_classes'].items(),key=lambda kv:kv[1],reverse=True)
for i,(label,value) in enumerate(classes):
 y=561-i*32;c.setFillColor(INK);c.setFont('Helvetica',11);c.drawString(35,y,label)
 w=value/12537*610;c.setFillColor(TEAL);c.rect(155,y-4,w,18,fill=1,stroke=0)
 c.setFillColor(INK);c.drawString(155+w+9,y,f'{num(value)} | '+f'{value/27891*100:.1f}%'.replace('.',','))
c.setFillColor(GRAY);c.setFont('Helvetica',10);c.drawString(35,354,'Penyebut: 27.891 kunjungan. Label kelas mengikuti sumber; ambulatory dan outpatient dipertahankan terpisah.')
c.setFillColor(NAVY);c.setFont('Helvetica-Bold',16);c.drawString(35,320,'Jumlah kunjungan menurut tahun mulai')
for i,(yr,value) in enumerate(AUD['encounters_by_year'].items()):
 x=62+i*76;h=value/3885*190;c.setFillColor(ORANGE if yr=='2022' else TEAL);c.rect(x,90,44,h,fill=1,stroke=0)
 c.setFillColor(INK);c.setFont('Helvetica',9);c.drawCentredString(x+22,75,yr);c.drawCentredString(x+22,95+h,num(value))
c.setStrokeColor(GRAY);c.line(50,90,965,90);c.setFillColor(GRAY);c.setFont('Helvetica',10)
c.drawString(35,45,'2022 hanya mencakup kunjungan hingga 5 Februari; jangan dibandingkan sebagai satu tahun penuh.')
c.drawString(35,27,'Periode START aktual: 2 Januari 2011 - 5 Februari 2022. Data tidak menunjukkan kondisi rumah sakit nyata.')
c.save();pdfium.PdfDocument(str(charttmp))[0].render(scale=1.6).to_pil().save(VIS/'gambaran_dataset.png')

intro='''Dataset ini merupakan data pasien sintetis berbasis Synthea yang disediakan untuk Maven Hospital Challenge. Data bukan rekam medis pasien nyata dan tidak dapat dipakai untuk menyimpulkan kinerja aktual Massachusetts General Hospital. Berkas diunduh dari tautan arsip publik resmi Maven pada 22 Oktober 2026.'''
rules=[
('Pilih unit analisis sebelum menggabungkan tabel.','Gunakan patients untuk menghitung orang, encounters untuk kunjungan, dan procedures untuk catatan tindakan. Jumlah baris hasil join bukan otomatis jumlah pasien.'),
('Hindari penggandaan biaya.','Satu kunjungan dapat memiliki banyak prosedur. Menjumlahkan TOTAL_CLAIM_COST setelah join langsung ke procedures akan menggandakan biaya kunjungan. Ringkas prosedur per ENCOUNTER sebelum join atau hitung biaya di tabel encounters.'),
('Hubungkan prosedur melalui ENCOUNTER.','Untuk mengaitkan tindakan dengan kunjungan, gunakan procedures.ENCOUNTER = encounters.Id. Join hanya melalui PATIENT akan memasangkan tindakan dengan kunjungan lain milik pasien yang sama.'),
('Jangan menjumlahkan komponen biaya yang bertumpang tindih.','TOTAL_CLAIM_COST sudah mencakup item layanan. BASE_ENCOUNTER_COST dan BASE_COST prosedur memiliki cakupan berbeda; jangan menambahkan semuanya sebagai total baru.'),
('Bedakan cakupan penjamin dari pengeluaran pasien.','PAYER_COVERAGE adalah nilai cakupan yang tercatat. Selisih TOTAL_CLAIM_COST - PAYER_COVERAGE boleh disebut biaya yang tidak tercakup pada catatan ini, bukan otomatis pembayaran tunai pasien atau utang yang sudah tertagih.'),
('Kunjungan berulang bukan otomatis readmisi klinis.','Tetapkan definisi episode, jenis rawat inap, urutan keluar-masuk, serta jendela waktu bila ingin menghitung readmisi. Jangan menyebut semua pasien dengan beberapa kunjungan sebagai pasien readmisi.'),
('Gunakan tanggal yang relevan.','Usia sebaiknya dihitung pada START kunjungan, bukan menggunakan usia saat ini. Durasi = STOP - START; hitung untuk kelas layanan yang sesuai. Data 2022 berhenti pada 5 Februari.'),
('Pertahankan nilai kosong sesuai maknanya.','DEATHDATE kosong berarti tanggal kematian tidak tercatat. SUFFIX dan MAIDEN bersifat opsional; REASONCODE tidak selalu tersedia. Jangan mengganti semua nilai kosong dengan nol atau menghapus semua baris yang tidak lengkap.'),
]
questions=[('Profil pemanfaatan layanan','Distribusi jenis kunjungan menurut usia saat kunjungan atau gender; penyebut harus jelas.','Batang berkelompok / 100%'),('Konsentrasi kunjungan','Jumlah kunjungan per pasien; median, kuartil, dan porsi kunjungan dari kelompok frekuensi tinggi.','Histogram / kurva kumulatif'),('Cakupan pembiayaan','SUM(PAYER_COVERAGE) / SUM(TOTAL_CLAIM_COST) menurut kelas layanan atau penjamin.','Batang persentase'),('Perubahan aktivitas layanan','Jumlah kunjungan per tahun atau bulan mulai; bandingkan periode yang setara.','Garis / batang'),('Durasi dan biaya layanan','Median durasi serta biaya menurut ENCOUNTERCLASS; pisahkan rawat inap.','Boxplot / batang median')]
md='# Penjelasan Dataset Hospital Patient Records\n\n'+intro+'\n\n## 1. Sumber dan berkas\n\n'
md+=f'- Halaman challenge: {SOURCE}\n- Halaman dataset: https://mavenanalytics.io/data-playground/hospital-patient-records\n- Arsip unduhan resmi: {DOWNLOAD}\n- Lisensi pada halaman Maven: Public Domain. Atribusi sumber tetap disarankan.\n- CSV asli dipertahankan dalam `data_asli/`; skrip SQL sumber disimpan terpisah dan tidak dijalankan.\n- Rujukan Synthea dari `citation.txt`: https://doi.org/10.1093/jamia/ocx079.\n\n'
md+='## 2. Inventaris dan unit analisis\n\n| Tabel | Satu baris mewakili | Baris | Kolom | Kunci utama |\n| --- | --- | ---: | ---: | --- |\n'
for n in NAMES:md+=f'| `{n}.csv` | {grain[n]} | {num(AUD[n]["rows"])} | {len(AUD[n]["columns"])} | '+('`Id`' if n!='procedures' else 'Tidak ada ID eksplisit')+' |\n'
md+='\nTotal: **76.577 baris lintas lima tabel dan 58 kolom**. Penjumlahan baris lintas tabel bukan jumlah pasien atau kejadian unik. `data_dictionary.csv` merupakan dokumentasi pendamping, bukan tabel analisis keenam.\n\n'
md+='**Perbedaan dokumentasi:** kamus bawaan menyebut `Middle` dan `FIPS County Code` pada patients, tetapi keduanya tidak ada di CSV aktual. Nama kolom dokumentasi juga memakai kapitalisasi berbeda. Penjelasan ini mengikuti nama dan jumlah kolom CSV yang diunduh, bukan angka ringkasan pada situs.\n\n'
md+='## 3. Relasi antartabel\n\n![ERD](visualisasi/erd_hospital.png)\n\n```mermaid\n'+mermaid+'```\n\n'
md+='| Relasi | Makna | ID anak tanpa induk |\n| --- | --- | ---: |\n'
for r in AUD['relations']:md+=f'| `{r["child"]}.{r["key"]}` → `{r["parent"]}.Id` | Banyak baris anak dapat merujuk satu induk | {r["orphans"]} |\n'
md+='\nEmpat tabel memiliki `Id` unik dan tidak kosong: patients, encounters, payers, organizations. Procedures tidak memiliki ID eksplisit; jangan menganggap `CODE` atau pasangan PATIENT-ENCOUNTER sebagai kunci unik. Diagram menunjukkan relasi logis dari CSV, bukan constraint yang sedang dijalankan pada basis data.\n\nPada salinan ini, seluruh 974 pasien memiliki kunjungan. Sebanyak **793 pasien** dan **14.670 kunjungan** mempunyai catatan prosedur. Terdapat **181 pasien** dan **13.221 kunjungan** tanpa baris prosedur; pertahankan mereka dengan left join jika analisis membutuhkan seluruh populasi. Seluruh pasangan PATIENT pada prosedur konsisten dengan PATIENT kunjungannya.\n\n'
md+='## 4. Kamus seluruh kolom aktual\n\nTipe di bawah merupakan tipe analitis yang disarankan. CSV sendiri menyimpan teks. ID, kode SNOMED-CT, nomor telepon, dan ZIP sebaiknya dipertahankan sebagai teks.\n\n'
for n in NAMES:
 md+=f'### {n}.csv\n\n{grain[n]}.\n\n| Kolom asli | Tipe analitis | Penjelasan | Sel kosong |\n| --- | --- | --- | ---: |\n'
 for k in AUD[n]['columns']:md+=f'| `{k}` | {dtype(n,k)} | {base[k]} | {num(AUD[n]["missing"][k])} |\n'
 md+='\n'
md+='## 5. Hasil pemeriksaan kualitas\n\n'
md+='- Tidak ditemukan baris identik pada masing-masing dari lima tabel.\n- Tidak ditemukan ID kosong atau ID berulang pada empat tabel yang memiliki Id.\n- Tidak ditemukan ID relasi yang tidak memiliki induk pada lima hubungan yang diperiksa.\n- Tidak ditemukan STOP lebih awal dari START pada encounters dan procedures.\n- Tidak ditemukan perbedaan ID pasien antara baris prosedur dan kunjungan yang dirujuknya.\n- Terdapat nilai kosong pada beberapa kolom; jumlah per kolom ada pada kamus di atas dan hasil_pemeriksaan.json. Pemeriksaan ini belum merupakan audit klinis lengkap atau jaminan bahwa setiap catatan valid.\n\n'
md+='**Makna kosong yang penting:** kolom alasan kunjungan kosong pada 19.541 dari 27.891 kunjungan; kolom alasan prosedur kosong pada 36.945 dari 47.701 prosedur. Nilai tersebut tidak boleh diartikan sebagai tidak ada penyakit. Atribut kontak payer yang kosong berada pada kategori NO_INSURANCE; kategori ini adalah label eksplisit, bukan nilai kosong PAYER.\n\n'
md+='## 6. Aturan penggabungan dan interpretasi\n\n'
for title,body in rules:md+=f'### {title}\n\n{body}\n\n'
md+='## 7. Visualisasi awal\n\n![Gambaran data](visualisasi/gambaran_dataset.png)\n\nVisual dihitung dari tabel encounters tanpa menggandakan baris melalui join. Komposisi menggunakan penyebut 27.891 kunjungan; tren memakai tahun START. Kategori ambulatory dan outpatient dipertahankan sebagai dua label sumber yang berbeda. Tahun 2022 hanya periode parsial.\n\n'
md+='## 8. Arah eksplorasi infografis\n\nPertanyaan berikut merupakan rekomendasi analisis, bukan hubungan sebab-akibat yang telah dibuktikan.\n\n| Fokus | Ukuran | Visual |\n| --- | --- | --- |\n'
for row in questions:md+='| '+' | '.join(row)+' |\n'
md+='\n## 9. Ringkasan angka dasar\n\n'
md+=f'- Periode START kunjungan: `{AUD["period"][0]}` hingga `{AUD["period"][1]}`.\n- Total TOTAL_CLAIM_COST: USD {AUD["money"]["TOTAL_CLAIM_COST"]:,.2f}.\n- Total PAYER_COVERAGE: USD {AUD["money"]["PAYER_COVERAGE"]:,.2f}.\n- Rasio cakupan tertimbang: {AUD["money"]["PAYER_COVERAGE"]/AUD["money"]["TOTAL_CLAIM_COST"]*100:.2f}%. Ini rasio jumlah biaya, bukan persentase pasien terlindungi atau rata-rata persentase per kunjungan.\n\n'
md+='## 10. Isi folder\n\n- `data_asli/`: lima CSV analisis, kamus sumber, dan citation.txt.\n- `Hospital_Patient_Records_original.zip`: arsip unduhan tanpa perubahan.\n- `skrip_sumber/`: dua skrip SQL bawaan, disimpan tanpa dijalankan.\n- `visualisasi/erd_hospital.png`: diagram relasi.\n- `visualisasi/erd_hospital.mmd`: sumber diagram yang dapat diedit.\n- `visualisasi/gambaran_dataset.png`: grafik ringkasan awal.\n- `hasil_pemeriksaan.json`: jumlah baris, kosong, validasi relasi, dan hash CSV.\n- `penjelasan_struktur_dataset.pdf`: penjelasan dan visual siap dibaca.\n'
(OUT/'penjelasan_dataset.md').write_text(md,encoding='utf-8')

styles=getSampleStyleSheet()
for name,size,lead,color in [('TitleH',24,29,NAVY),('HeadH',13,17,TEAL),('BodyH',10,15,INK),('CellH',8.4,11.4,INK),('SmallH',8,11,GRAY)]:
 styles.add(ParagraphStyle(name=name,fontName='Helvetica-Bold' if name in ['TitleH','HeadH'] else 'Helvetica',fontSize=size,leading=lead,textColor=color,spaceAfter=8))
def P(s,sty='BodyH'):return Paragraph(s,styles[sty])
def T(rows,widths):
 t=Table([[P(html.escape(str(v)),'CellH') for v in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,1),(-1,-1),.35,colors.HexColor('#D5E2E7')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]));return t
def foot(c,d):
 c.setStrokeColor(colors.HexColor('#D5E2E7'));c.line(44,42,551,42);c.setFillColor(GRAY);c.setFont('Helvetica',8);c.drawString(44,28,'HOSPITAL PATIENT RECORDS | Data sintetis | 22 Oktober 2026');c.drawRightString(551,28,str(d.page))
story=[P('Hospital Patient Records','TitleH'),P('Struktur, relasi, dan panduan eksplorasi infografis','HeadH'),P(intro),
 T([['Tabel','Unit per baris','Baris','Kolom']]+[[n,grain[n],num(AUD[n]['rows']),len(AUD[n]['columns'])] for n in NAMES],[95,260,75,75]),Spacer(1,12),
 P('Apa yang perlu diketahui sejak awal','HeadH'),P('<b>Lima tabel, 58 kolom.</b> Total baris lintas tabel adalah 76.577; angka ini bukan jumlah pasien. Periode mulai kunjungan aktual adalah 2 Januari 2011 hingga 5 Februari 2022.'),
 P('Kamus sumber mencantumkan Middle dan FIPS County Code pada patients, tetapi kedua kolom tidak terdapat pada CSV aktual. Dokumentasi ini mengikuti berkas yang diunduh.'),
 P('Lima hubungan antar-ID telah diperiksa: tidak ditemukan ID anak tanpa induk. Tidak ada baris identik pada lima tabel. Nilai kosong tetap ada pada atribut tertentu dan dibahas menurut maknanya.'),
 P(f'<link href="{SOURCE}" color="#007F82">Halaman resmi Maven Hospital Challenge</link><br/><link href="{DOWNLOAD}" color="#007F82">Tautan unduhan arsip resmi Maven</link>','SmallH'),PageBreak(),
 P('Peta relasi lima tabel','TitleH'),Image(str(VIS/'erd_hospital.png'),width=505,height=337),
 P('Cara membaca relasi','HeadH'),P('patients, organizations, dan payers terhubung ke encounters. Setiap kunjungan dapat memiliki nol atau banyak catatan procedures. procedures juga menyimpan PATIENT yang merujuk langsung ke patients.'),
 P('<b>793 pasien</b> dan <b>14.670 kunjungan</b> mempunyai catatan prosedur. Sebanyak 181 pasien dan 13.221 kunjungan tidak memiliki baris prosedur. Gunakan left join bila seluruh pasien atau kunjungan harus dipertahankan.'),
 P('Id unik tersedia pada empat tabel induk. Procedures tidak memiliki kolom ID prosedur eksplisit; CODE bukan kunci unik. PK dan FK pada diagram adalah kunci logis yang diperiksa pada CSV.'),
 P('Penggabungan prosedur dengan kunjungan memakai ENCOUNTER = Id. Join hanya melalui PATIENT dapat memasangkan satu prosedur dengan kunjungan lain milik pasien yang sama.'),PageBreak()]
for n in NAMES:
 story += [P(f'Kamus tabel: {n}','TitleH'),P(f'{grain[n]}. {num(AUD[n]["rows"])} baris dan {len(AUD[n]["columns"])} kolom. Tipe di bawah adalah tipe analitis yang disarankan.','SmallH')]
 rows=[['Kolom asli','Tipe','Makna','Kosong']]+[[k,dtype(n,k),base[k],num(AUD[n]['missing'][k])] for k in AUD[n]['columns']]
 story += [T(rows,[112,78,270,45]),Spacer(1,10)]
 if n=='patients':story+=[P('DEATHDATE, SUFFIX, dan MAIDEN dapat kosong sesuai konteks. Jangan menghapus seluruh pasien hanya karena kolom opsional tidak terisi. ZIP sebaiknya disimpan sebagai teks.','SmallH')]
 if n=='encounters':story+=[P('TOTAL_CLAIM_COST sudah mencakup item layanan. REASONCODE kosong berarti alasan spesifik tidak tercatat pada kolom ini, bukan tidak ada kondisi kesehatan.','SmallH')]
 if n=='procedures':story+=[P('Satu kunjungan dapat memiliki banyak baris. Tidak semua kunjungan mempunyai prosedur. PATIENT seluruh prosedur konsisten dengan pasien pada ENCOUNTER yang dirujuk.','SmallH')]
 if n=='payers':story+=[P('Terdapat kategori NO_INSURANCE. Kontaknya kosong, tetapi ID-nya tetap terisi dan valid. Kategori ini jangan dianggap sebagai foreign key yang hilang.','SmallH')]
 if n=='organizations':story+=[P('Hanya satu organisasi tercatat, sehingga dataset ini tidak mendukung perbandingan kinerja antar-rumah sakit.','SmallH')]
 story+=[PageBreak()]
story += [P('Visualisasi awal','TitleH'),Image(str(VIS/'gambaran_dataset.png'),width=505,height=399),
 P('Grafik dihitung dari encounters asli. Tidak ada penggandaan baris melalui join. Kategori ambulatory dan outpatient dipertahankan terpisah sesuai label sumber.','SmallH'),
 P('Tahun 2022 hanya hingga 5 Februari. Penurunan jumlah pada batang terakhir tidak dapat dibaca sebagai penurunan tahunan penuh. Seluruh catatan bersifat sintetis.','BodyH'),PageBreak(),
 P('Aturan analisis','TitleH')]
for title,body in rules:story += [P(title,'HeadH'),P(body)]
story += [PageBreak(),P('Arah eksplorasi dan verifikasi','TitleH'),T([['Fokus','Ukuran yang dapat dihitung','Visual']]+questions,[110,290,105]),Spacer(1,10),
 P('Hasil pemeriksaan berkas','HeadH'),P('ID pada empat tabel yang memiliki Id unik dan terisi. Lima relasi tanpa ID anak yang kehilangan induk. Tidak ditemukan baris identik atau durasi negatif pada kunjungan dan prosedur. Pemeriksaan ini bukan audit klinis lengkap.'),
 P('Total biaya kunjungan tercatat USD 101.514.375,52; cakupan penjamin USD 31.097.506,99. Rasio jumlah cakupan terhadap jumlah biaya adalah 30,63%, bukan persentase pasien yang ditanggung.'),
 P('Sumber dan atribusi','HeadH'),P('Maven Hospital Challenge / Hospital Patient Records; sumber data sintetis: Synthea / SyntheticMass. Halaman Maven mencantumkan Public Domain. CSV asli, kamus, dan arsip unduhan disimpan tanpa perubahan.','SmallH'),
 P('<link href="https://doi.org/10.1093/jamia/ocx079" color="#007F82">Walonoski et al. (2018). Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record.</link>','SmallH'),
 P('Dokumentasi lengkap: penjelasan_dataset.md. Angka pemeriksaan per kolom dan hash berkas: hasil_pemeriksaan.json.','SmallH')]
pdf=OUT/'penjelasan_struktur_dataset.pdf'
SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=42,bottomMargin=55,title='Hospital Patient Records - Struktur Dataset',author='Dokumentasi latihan final CDW').build(story,onFirstPage=foot,onLaterPages=foot)
qa=ROOT/'tmp/pdfs/hospital';qa.mkdir(parents=True,exist_ok=True);doc=pdfium.PdfDocument(str(pdf))
for i in range(len(doc)):doc[i].render(scale=1.15).to_pil().save(qa/f'page-{i+1}.png')
reader=PdfReader(pdf);texts=[p.extract_text() for p in reader.pages]
assert all(len(t)>100 for t in texts)
assert len([k for n in NAMES for k in AUD[n]['columns']])==58
assert sum(AUD[n]['rows'] for n in NAMES)==76577
print(json.dumps({'pages':len(doc),'characters_by_page':[len(t) for t in texts],'output':str(OUT)},indent=2))
