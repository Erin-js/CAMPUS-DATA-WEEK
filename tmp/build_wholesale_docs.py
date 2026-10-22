from pathlib import Path
import json, csv, html
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Flowable
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT = Path.cwd()
OUT = ROOT / '05_Latihan_Final' / 'Wholesale_Customers'
meta = json.loads((OUT / 'hasil_pemeriksaan.json').read_text())
source = 'https://archive.ics.uci.edu/dataset/292/wholesale+customers'
doi = 'https://doi.org/10.24432/C5030X'
fields = [
 ('Channel','Kategori berkode','Jenis pelanggan: 1 = Horeca (hotel, restoran, kafe); 2 = Retail.','1-2'),
 ('Region','Kategori berkode','Wilayah pelanggan: 1 = Lisbon; 2 = Oporto; 3 = wilayah lain.','1-3'),
 ('Fresh','Numerik','Pengeluaran tahunan untuk produk segar, dalam m.u.','3-112.151'),
 ('Milk','Numerik','Pengeluaran tahunan untuk produk susu, dalam m.u.','55-73.498'),
 ('Grocery','Numerik','Pengeluaran tahunan untuk kebutuhan bahan pangan / grocery, dalam m.u.','3-92.780'),
 ('Frozen','Numerik','Pengeluaran tahunan untuk produk beku, dalam m.u.','25-60.869'),
 ('Detergents_Paper','Numerik','Pengeluaran tahunan untuk deterjen dan produk kertas, dalam m.u.','3-40.827'),
 ('Delicassen','Numerik','Pengeluaran tahunan untuk produk delicatessen / makanan khusus, dalam m.u.','3-47.943'),
]
md = '''# Penjelasan Dataset Wholesale Customers

## 1. Gambaran dan sumber

Dataset ini memuat profil jenis pelanggan, wilayah, dan pengeluaran tahunan pelanggan sebuah distributor grosir. Satu baris mewakili satu pelanggan; enam kolom pengeluaran merangkum belanja per kategori produk, bukan transaksi individual. Dataset cocok untuk latihan infografis bisnis mengenai perbedaan pola belanja dan komposisi pengeluaran.

- Sumber resmi: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/292/wholesale+customers).
- Pembuat yang dicantumkan UCI: Margarida Cardoso.
- DOI: https://doi.org/10.24432/C5030X.
- Lisensi: CC BY 4.0; cantumkan atribusi saat menggunakan atau mengadaptasi data.
- Tanggal unduh dan pemeriksaan: 22 Oktober 2026.
- Berkas asli: `Wholesale customers data.csv`; arsip unduhan: `wholesale_customers_original.zip`.

Tahun pengamatan belanja dan mata uang spesifik tidak dijelaskan pada halaman sumber yang diperiksa. Tanggal publikasi / donasi bukan tahun pengamatan. Nilai pengeluaran dinyatakan dalam *monetary units* (m.u.); jangan menggantinya dengan rupiah atau euro tanpa sumber tambahan.

## 2. Struktur dan unit analisis

| Aspek | Hasil pemeriksaan berkas |
| --- | --- |
| Tabel | Satu tabel datar |
| Jumlah baris | 440 pelanggan |
| Jumlah kolom | 8 |
| Pemisah CSV | Koma (`,`) |
| Header | Ada pada baris pertama |
| Representasi nilai | Seluruh nilai dapat dibaca sebagai bilangan bulat |
| Variabel kategori | `Channel`, `Region`; angka merupakan kode kategori |
| Variabel pengeluaran | Enam kolom numerik dalam m.u. |
| Primary key / ID pelanggan | Tidak tersedia secara eksplisit |
| Foreign key | Tidak tersedia |
| Relasi antartabel | Tidak ada pada dataset yang diunduh |

**Jumlah delapan kolom mengikuti CSV aktual.** Angka tujuh fitur pada ringkasan UCI mengikuti pembagian peran variabel di repositori, bukan jumlah seluruh kolom berkas.

## 3. Kamus data

| Kolom asli | Jenis analitis | Makna | Minimum-maksimum aktual |
| --- | --- | --- | --- |
'''
for name,typ,desc,rng in fields:
    md += f'| `{name}` | {typ} | {desc} | {rng} |\n'
md += '''
Rentang pada dua kolom pertama merupakan rentang kode, bukan besaran kuantitatif. Enam kolom lainnya memiliki skala pengeluaran. Nama `Delicassen` mengikuti ejaan asli CSV agar pemanggilan kolom tidak keliru.

### Pemetaan kategori dan jumlah pelanggan

| Kolom | Kode | Label | Jumlah | Proporsi |
| --- | --- | --- | ---: | ---: |
| Channel | 1 | Horeca: hotel, restoran, kafe | 298 | 67,7% |
| Channel | 2 | Retail | 142 | 32,3% |
| Region | 1 | Lisbon | 77 | 17,5% |
| Region | 2 | Oporto | 47 | 10,7% |
| Region | 3 | Wilayah lain | 316 | 71,8% |

Penyebut setiap proporsi adalah 440 pelanggan. Setiap pelanggan memiliki satu kode Channel dan satu kode Region. Proporsi dibulatkan satu angka desimal. Pemetaan label mengikuti kategori sumber dan dicocokkan dengan frekuensi resmi UCI.

## 4. Diagram struktur data dan status ERD

Dataset asli tidak menyediakan beberapa tabel, primary key, atau foreign key. Karena itu, tidak ada relasi antartabel yang dapat digambar sebagai ERD relasional. Diagram berikut adalah representasi satu entitas / tabel, tanpa menambahkan hubungan yang tidak tersedia.

```mermaid
erDiagram
    WHOLESALE_CUSTOMERS {
        int Channel "Kategori: Horeca atau Retail"
        int Region "Kategori: Lisbon, Oporto, atau lainnya"
        int Fresh "Pengeluaran tahunan, m.u."
        int Milk "Pengeluaran tahunan, m.u."
        int Grocery "Pengeluaran tahunan, m.u."
        int Frozen "Pengeluaran tahunan, m.u."
        int Detergents_Paper "Pengeluaran tahunan, m.u."
        int Delicassen "Pengeluaran tahunan, m.u."
    }
```

`Channel` dan `Region` bukan ID unik. Penamaan tabel `WHOLESALE_CUSTOMERS` pada diagram adalah label dokumentasi, bukan nama tabel basis data yang disediakan sumber. Jika kelak diimpor ke basis data, ID baris dapat ditambahkan sebagai kunci teknis; ID tambahan tersebut bukan identitas pelanggan dari sumber. Dataset yang diunduh tetap dipertahankan tanpa perubahan.

## 5. Hasil pemeriksaan kualitas

- Terdapat 440 baris dengan delapan kolom yang konsisten.
- Tidak ditemukan sel kosong atau penanda umum nilai hilang (`NA`, `NaN`, `null`, `?`).
- Tidak ditemukan baris identik pada seluruh delapan kolom.
- Semua nilai dapat dibaca sebagai bilangan bulat. Enam kolom pengeluaran bernilai positif.
- Kode Channel hanya 1 dan 2; kode Region hanya 1, 2, dan 3.

Hasil tersebut cukup untuk memulai analisis deskriptif tanpa imputasi atau penghapusan duplikat. Pemeriksaan struktur ini tidak membuktikan kebenaran seluruh catatan dunia nyata. Karena tidak ada ID eksplisit, ketiadaan baris identik juga tidak memverifikasi keunikan identitas pelanggan secara independen. Nilai pengeluaran tinggi tidak otomatis salah dan tidak perlu dihapus tanpa alasan.

## 6. Cara membaca data untuk infografis

### Pisahkan ukuran kelompok dan perilaku belanja

Jumlah pelanggan Horeca lebih besar daripada Retail. Karena itu, total pengeluaran kelompok dapat lebih besar hanya karena jumlah pelanggannya lebih banyak. Jika ingin membahas pola pelanggan, bandingkan median atau rerata pengeluaran per pelanggan dan cantumkan ukuran kelompok. Gunakan total jika pertanyaannya mengenai kontribusi nilai belanja kelompok dalam dataset.

### Tentukan makna komposisi

Total belanja enam kategori per pelanggan dapat dihitung sebagai `Fresh + Milk + Grocery + Frozen + Detergents_Paper + Delicassen`. Sebut sebagai total **enam kategori yang tercatat**, karena dataset tidak memastikan semua jenis belanja pelanggan tercakup. Kolom total ini merupakan hasil perhitungan, bukan kolom asli.

Proporsi kategori dari total belanja kelompok berbeda dari rata-rata proporsi per pelanggan. Ukuran pertama memberi bobot lebih besar kepada pelanggan dengan pengeluaran besar. Pilih ukuran sesuai pertanyaan dan tuliskan definisinya.

### Hindari klaim yang melampaui data

- Gunakan istilah pengeluaran atau nilai belanja, bukan laba, margin, atau jumlah barang.
- Data tidak memuat tanggal transaksi, sehingga tidak mendukung analisis tren bulanan atau musiman.
- Dataset ini tidak cukup untuk menyimpulkan bahwa wilayah atau jenis pelanggan menyebabkan perbedaan pengeluaran.
- Temuan berlaku pada 440 pelanggan dalam dataset; jangan menggeneralisasikannya menjadi seluruh pasar tanpa dasar pengambilan sampel.
- Membandingkan median dan rerata membantu membaca distribusi yang mungkin dipengaruhi pengeluaran sangat tinggi. Pencilan perlu ditinjau, bukan otomatis dibuang.

## 7. Pilihan arah eksplorasi dan visualisasi

Berikut pertanyaan latihan, bukan temuan yang sudah dibuktikan.

| Pertanyaan | Ukuran yang dapat dihitung | Visual yang disarankan |
| --- | --- | --- |
| Bagaimana pola belanja Horeca dan Retail berbeda? | Median per kategori dan ukuran kelompok | Grafik batang berkelompok atau small multiples |
| Bagaimana komposisi belanja tiap jenis pelanggan? | Pangsa enam kategori dari total pengeluaran kelompok | Batang bertumpuk 100% |
| Seberapa beragam pengeluaran pelanggan? | Median, kuartil, rentang distribusi | Boxplot per kategori / Channel |
| Apakah pola belanja berbeda antarwilayah? | Median per kategori menurut Region | Heatmap dengan skala dan satuan jelas |

Untuk simulasi lima jam, pilih satu pertanyaan utama dan dua sampai tiga bukti pendukung. Pengelompokan, penghitungan median, serta pemberian label kategori merupakan bagian analisis; tidak memerlukan normalisasi atau standardisasi data untuk sekadar membuat grafik deskriptif.

## 8. Contoh satu baris

Baris pertama berisi `Channel=2`, `Region=3`, `Fresh=12669`, `Milk=9656`, `Grocery=7561`, `Frozen=214`, `Detergents_Paper=2674`, dan `Delicassen=1338`. Artinya, pelanggan tersebut termasuk Retail di wilayah lain, dengan pengeluaran tahunan produk segar 12.669 m.u. Baris ini bukan catatan satu transaksi.

## 9. Berkas pendamping dan atribusi

- [CSV asli](Wholesale%20customers%20data.csv)
- [Arsip asli](wholesale_customers_original.zip)
- [PDF struktur data](penjelasan_struktur_data.pdf)
- [Hasil pemeriksaan terstruktur](hasil_pemeriksaan.json)
- [Diagram struktur PNG](diagram_struktur_data.png)

Contoh atribusi: Cardoso, M. (2013). *Wholesale customers* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5030X. Lisensi CC BY 4.0. Tahun 2013 mengikuti sitasi yang disediakan UCI, bukan klaim tahun pengamatan.
'''
(OUT/'penjelasan_dataset.md').write_text(md,encoding='utf-8')

NAVY=colors.HexColor('#123047');TEAL=colors.HexColor('#007F82');LIGHT=colors.HexColor('#EAF4F5');INK=colors.HexColor('#243746');GRAY=colors.HexColor('#627582')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleX',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=NAVY,spaceAfter=12))
styles.add(ParagraphStyle(name='SubX',fontSize=10,leading=15,textColor=GRAY,spaceAfter=12))
styles.add(ParagraphStyle(name='BodyX',fontSize=10,leading=15,textColor=INK,spaceAfter=8))
styles.add(ParagraphStyle(name='HeadX',fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=TEAL,spaceBefore=10,spaceAfter=8))
styles.add(ParagraphStyle(name='CellX',fontSize=8.6,leading=12,textColor=INK))
styles.add(ParagraphStyle(name='SmallX',fontSize=8,leading=11,textColor=GRAY,spaceAfter=6))
def P(s,sty='BodyX'):return Paragraph(s,styles[sty])
def T(rows,widths):
 t=Table([[P(str(c),'CellX') for c in row] for row in rows],colWidths=widths,hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('LINEBELOW',(0,0),(-1,0),1,TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,1),(-1,-1),0.4,colors.HexColor('#D8E3E8'))]))
 return t

class Schema(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=495;self.height=276
 def draw(self):
  c=self.canv;x=38;w=418;y=22;h=244
  c.setFillColor(colors.white);c.setStrokeColor(TEAL);c.roundRect(x,y,w,h,8,fill=1,stroke=1)
  c.setFillColor(NAVY);c.roundRect(x,y+h-38,w,38,8,fill=1,stroke=0);c.rect(x,y+h-38,w,15,fill=1,stroke=0)
  c.setFillColor(colors.white);c.setFont('Helvetica-Bold',12);c.drawString(x+14,y+h-24,'WHOLESALE_CUSTOMERS')
  for i,(name,typ,_,_) in enumerate(fields):
   yy=y+h-58-i*23
   if i==2:c.setStrokeColor(TEAL);c.line(x+12,yy+14,x+w-12,yy+14)
   c.setFillColor(INK);c.setFont('Helvetica',10);c.drawString(x+14,yy,name)
   c.setFillColor(GRAY);c.setFont('Helvetica',8.8);c.drawRightString(x+w-14,yy,'kode kategori' if i<2 else 'pengeluaran tahunan (m.u.)')
  c.setFillColor(GRAY);c.setFont('Helvetica',8);c.drawCentredString(self.width/2,5,'1 baris = 1 pelanggan | Tanpa ID eksplisit atau relasi antartabel')

def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#D8E3E8'));c.line(48,43,A4[0]-48,43)
 c.setFont('Helvetica',8);c.setFillColor(GRAY);c.drawString(48,29,'WHOLESALE CUSTOMERS  /  Panduan struktur dan pembacaan data')
 c.drawRightString(A4[0]-48,29,str(doc.page))

story=[P('Wholesale Customers','TitleX'),P('Struktur data untuk latihan infografis bisnis<br/>Diunduh dan diperiksa pada 22 Oktober 2026','SubX'),
 P('440 pelanggan. Delapan kolom. Satu tabel.','HeadX'),
 P('Satu baris merangkum jenis pelanggan, wilayah, dan belanja tahunan pada enam kategori produk. Dataset ini bukan catatan transaksi individual.'),
 T([['Baris','Kolom','Nilai kosong','Baris duplikat'],['440','8','0','0']],[124,124,124,123]),
 P('Diagram struktur satu tabel','HeadX'),Schema(),
 P('<b>Status ERD:</b> tidak ada hubungan antartabel dalam berkas asli. Diagram menampilkan satu entitas tanpa menambahkan kunci atau relasi yang tidak disediakan. Channel dan Region adalah kode kategori, bukan ID pelanggan.'),
 P('Kelompok pelanggan','HeadX'),
 T([['Dimensi','Kategori dan jumlah'],['Channel','1 = Horeca: 298 (67,7%); 2 = Retail: 142 (32,3%).'],['Region','1 = Lisbon: 77; 2 = Oporto: 47; 3 = wilayah lain: 316.']],[90,405]),
 P('Sumber: UCI Machine Learning Repository, Wholesale customers. Jumlah dan kualitas struktur diperiksa langsung pada CSV yang diunduh.','SmallX'),PageBreak(),
 P('Kamus kolom','TitleX'),P('Nama kolom dipertahankan sesuai CSV asli. Seluruh nilai tersimpan sebagai bilangan bulat; peran analitisnya berbeda.','SubX'),
 T([['Kolom','Makna','Rentang aktual']]+[[n,d,r] for n,_,d,r in fields],[112,291,92]),
 P('Satuan dan kode yang perlu dijaga','HeadX'),
 P('<b>m.u. = monetary units.</b> Dokumentasi yang diperiksa tidak menetapkan mata uang spesifik. Jangan melabeli nilai sebagai rupiah atau euro. Channel dan Region berskala kategori; menghitung rerata kodenya tidak bermakna.'),
 P('<b>Delicassen</b> adalah ejaan nama kolom dalam berkas asli. Gunakan ejaan tersebut saat memilih kolom. Rentang minimum-maksimum pada tabel dihitung dari 440 baris aktual.'),
 P('Berkas siap dianalisis','HeadX'),
 P('CSV menggunakan koma sebagai pemisah dan memiliki header. Pemeriksaan menemukan delapan kolom konsisten, seluruh nilai dapat dibaca sebagai bilangan bulat, tidak ada sel kosong atau penanda umum nilai hilang, serta tidak ada baris identik. Enam kolom pengeluaran seluruhnya positif.'),
 P('Tidak diperlukan imputasi atau penghapusan duplikat untuk mulai membuat ringkasan deskriptif. Memberi label kategori dan menghitung agregat tetap diperlukan. Nilai tinggi tidak otomatis salah; pemeriksaan struktur bukan validasi independen atas identitas atau kebenaran setiap pelanggan.'),PageBreak(),
 P('Dari tabel ke infografis','TitleX'),P('Pertanyaan berikut adalah arah eksplorasi, bukan kesimpulan yang sudah dibuktikan.','SubX'),
 T([['Pertanyaan latihan','Ukuran dan visual'],['Bagaimana pola belanja Horeca dan Retail berbeda?','Median pengeluaran tiap kategori; batang berkelompok atau small multiples.'],['Bagaimana komposisi nilai belanja kelompok?','Pangsa enam kategori dari total pengeluaran kelompok; batang bertumpuk 100%.'],['Seberapa lebar variasi belanja pelanggan?','Median dan kuartil; boxplot menurut kategori atau Channel.'],['Apakah pola belanja berbeda antarwilayah?','Median tiap kategori menurut Region; heatmap.']],[236,259]),
 P('Aturan pembacaan','HeadX'),
 P('<b>1. Perhatikan ukuran kelompok.</b> Horeca berisi 298 pelanggan, Retail 142. Total kelompok menjawab kontribusi belanja; median atau rerata per pelanggan lebih tepat untuk membandingkan profil belanja.'),
 P('<b>2. Definisikan komposisi.</b> Pangsa kategori dari total belanja kelompok berbeda dari rata-rata pangsa kategori per pelanggan. Jika menjumlahkan enam kategori, sebut total enam kategori yang tercatat.'),
 P('<b>3. Batasi klaim.</b> Nilai belanja bukan laba, margin, atau jumlah barang. Tidak ada tanggal transaksi untuk tren bulanan. Hubungan wilayah dan pengeluaran tidak membuktikan sebab-akibat; hasil tidak otomatis mewakili seluruh pasar.'),
 P('<b>4. Jangan mengarang periode.</b> Tahun pengamatan tidak dijelaskan pada halaman sumber yang diperiksa. Tahun publikasi dataset bukan tahun belanja.'),
 P('Sumber, lisensi, dan berkas','HeadX'),
 P('Cardoso, M. (2013). <i>Wholesale customers</i> [Dataset]. UCI Machine Learning Repository. Lisensi CC BY 4.0; atribusi diperlukan. Tahun sitasi mengikuti UCI, bukan tahun pengamatan.','SmallX'),
 P(f'<link href="{doi}" color="#007F82">{doi}</link><br/><link href="{source}" color="#007F82">Halaman sumber dan kamus variabel UCI</link>','SmallX'),
 P('Pendamping: penjelasan_dataset.md, CSV asli, arsip unduhan, diagram_struktur_data.png, dan hasil_pemeriksaan.json.','SmallX')]
pdf=OUT/'penjelasan_struktur_data.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=57,title='Wholesale Customers - Penjelasan Struktur Data',author='Dokumentasi latihan final CDW')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
# Standalone diagram, rendered at 2x for clear reuse.
dp=ROOT/'tmp'/'wholesale_diagram.pdf'
c=canvas.Canvas(str(dp),pagesize=(525,306));c.translate(15,15);Schema().drawOn(c,0,0);c.save()
d=pdfium.PdfDocument(str(dp));d[0].render(scale=2).to_pil().save(OUT/'diagram_struktur_data.png')
qa=ROOT/'tmp'/'pdfs'/'wholesale';qa.mkdir(parents=True,exist_ok=True)
r=pdfium.PdfDocument(str(pdf))
for i in range(len(r)):r[i].render(scale=1.3).to_pil().save(qa/f'page-{i+1}.png')
reader=PdfReader(pdf)
assert len(reader.pages)==3, f'Unexpected pages: {len(reader.pages)}'
text='\n'.join(page.extract_text() for page in reader.pages)
assert all(x in text for x in ['Delicassen','440','Lisbon','Sumber, lisensi'])
print(json.dumps({'pdf':str(pdf),'pages':len(reader.pages),'markdown':str(OUT/'penjelasan_dataset.md'),'qa':str(qa)},indent=2))
