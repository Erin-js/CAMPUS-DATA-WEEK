from pathlib import Path
from textwrap import dedent
import ast
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(dedent(text).strip()))


def code(text):
    source = dedent(text).strip()
    ast.parse(source)
    cells.append(nbf.v4.new_code_cell(source))


md('''
# Visualisasi Infografis CDW 2026
## Sama-Sama Kuliah, Tak Sama Bebannya

Jalankan semua sel dari atas. Simpan notebook bersama lima CSV; di Colab, unggah kelima CSV terlebih dahulu.
Hasil tersimpan di `output_visualisasi_cdw`: PNG 300 dpi, PNG transparan, SVG dengan teks editable, PDF, tabel agregat, dan ZIP aset.
Setiap plot juga disimpan sebagai SVG di folder baru `svg_plot_cdw2026`, terpisah dari folder ekspor sebelumnya.

Urutan: ikon latar → konteks → lintasan → irisan kondisi → model → PETA → mockup JEMBATAN.
Visual tambahan disediakan sebagai alternatif, bukan untuk dimasukkan semuanya dalam satu poster.
Data CDW adalah Real World Fake Data dari universitas anonim. Temuan tidak mewakili seluruh mahasiswa Indonesia.
''')
md('''
## 1. Persiapan
Sel ini memasang pustaka hanya jika belum tersedia. Tidak mengubah notebook eksplorasi atau CSV sumber.
''')
code(r'''
import importlib.util
import subprocess
import sys

packages = {'numpy': 'numpy', 'pandas': 'pandas', 'matplotlib': 'matplotlib', 'statsmodels': 'statsmodels'}
missing = [package for module, package in packages.items() if importlib.util.find_spec(module) is None]
if missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
print('Pustaka siap.')
''')
code(r'''
from pathlib import Path
from textwrap import fill
from zipfile import ZipFile, ZIP_DEFLATED
import json
import hashlib
import platform
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import statsmodels
import statsmodels.api as sm
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, Arc, FancyArrowPatch
from matplotlib.ticker import FuncFormatter, NullLocator
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import display, Image, Markdown, FileLink

DATA_DIR = None
DPI = 300
TRANSPARENT_PNG = True
SHOW_FIGURES = True

FILES = ['1_profil_mahasiswa_umum.csv', '2_prestasi_mahasiswa.csv',
         '3_generasi_pertama_kuliah.csv', '4_status_sosial_ekonomi.csv',
         '5_riwayat_ipk_semester.csv']
candidates = [Path(DATA_DIR)] if DATA_DIR else [p / "02_Analisis" / "data" for p in [Path.cwd(), *Path.cwd().parents]] + [p / "data" for p in [Path.cwd(), *Path.cwd().parents]] + [Path.cwd(), *Path.cwd().parents]
ROOT = next((p for p in candidates if all((p / name).is_file() for name in FILES)), None)
if ROOT is None:
    raise FileNotFoundError('Lima CSV belum ditemukan. Unggah ke folder kerja atau isi DATA_DIR.')
OUT = ROOT.parents[1] / '04_Visualisasi' / 'output_visualisasi_cdw'
SVG_OUT = ROOT.parents[1] / '04_Visualisasi' / 'svg_plot_cdw2026'
SVG_OUT.mkdir(parents=True, exist_ok=True)
for folder in ['png', 'png_transparan', 'svg', 'pdf', 'tabel']:
    (OUT / folder).mkdir(parents=True, exist_ok=True)

C = {'fg': '#E8710A', 'nonfg': '#1B3A5F', 'risk': '#A8402D', 'green': '#2E8B57',
     'bg': '#FBF7EE', 'ink': '#233044', 'muted': '#627080', 'line': '#D8DCD9',
     'light': '#EDEFEA', 'white': '#FFFFFF'}
GROUP = {1: 'Generasi pertama', 0: 'Bukan generasi pertama'}
COLORS = {1: C['fg'], 0: C['nonfg']}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'text.color': C['ink'], 'axes.labelcolor': C['ink'],
                     'xtick.color': C['muted'], 'ytick.color': C['muted'],
                     'axes.facecolor': C['bg'], 'figure.facecolor': C['bg'],
                     'svg.fonttype': 'none', 'pdf.fonttype': 42,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.spines.left': False, 'axes.spines.bottom': False})
manifest = []
catalog = PdfPages(OUT / 'Katalog_Visual_CDW2026.pdf')

def angka(value, digits=1):
    return f'{value:,.{digits}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def jumlah(value):
    return angka(value, 0)

def persen(value):
    return angka(100 * value) + '%'

def canvas(title, subtitle='', size=(11, 5.8), bottom=0.20):
    fig, ax = plt.subplots(figsize=size)
    fig.subplots_adjust(left=0.10, right=0.93, top=0.77, bottom=bottom)
    fig.text(0.045, 0.94, title, fontsize=19, fontweight='bold', va='top')
    if subtitle:
        fig.text(0.045, 0.865, subtitle, fontsize=10.5, color=C['muted'], va='top')
    return fig, ax

def save_visual(fig, name, section, note, title=None):
    fig.text(0.045, 0.075, note, fontsize=8.5, color=C['muted'], va='top')
    fig.text(0.045, 0.029, 'Sumber: lima CSV CDW 2026. Data fiktif; unit analisis mahasiswa.',
             fontsize=8, color=C['muted'], va='bottom')
    fig.savefig(OUT / 'png' / f'{name}.png', dpi=DPI, bbox_inches='tight', pad_inches=0.22)
    if TRANSPARENT_PNG:
        fig.savefig(OUT / 'png_transparan' / f'{name}.png', dpi=DPI,
                    bbox_inches='tight', pad_inches=0.22, transparent=True)
    fig.savefig(OUT / 'svg' / f'{name}.svg', bbox_inches='tight', pad_inches=0.22, transparent=True)
    fig.savefig(SVG_OUT / f'{name}.svg', format='svg', bbox_inches='tight', pad_inches=0.22, transparent=True)
    fig.savefig(OUT / 'pdf' / f'{name}.pdf', bbox_inches='tight', pad_inches=0.22)
    catalog.savefig(fig, bbox_inches='tight', pad_inches=0.22)
    manifest.append({'nama': name, 'bagian': section, 'judul': title or name,
                     'catatan': note, 'png': f'png/{name}.png', 'svg': f'svg/{name}.svg'})
    if SHOW_FIGURES:
        display(fig)
    plt.close(fig)

def box(ax, x, y, w, h, face=C['white'], edge=C['line'], lw=1.2):
    patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.012,rounding_size=0.025',
                           facecolor=face, edgecolor=edge, linewidth=lw)
    ax.add_patch(patch)
    return patch

def clean_percent(ax):
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x:.0f}%'))
    ax.grid(axis='x', alpha=0.35, color=C['line'])
    ax.set_axisbelow(True)

print('Folder data:', ROOT)
print('Folder ekspor:', OUT)
print('Folder SVG baru:', SVG_OUT)
''')
md('''
## 2. Data dan unit analisis

Sumber: `1_profil_mahasiswa_umum.csv`, `2_prestasi_mahasiswa.csv`, `3_generasi_pertama_kuliah.csv`,
`4_status_sosial_ekonomi.csv`, `5_riwayat_ipk_semester.csv`.
CSV dipisahkan titik koma. Prestasi diringkas per mahasiswa, termasuk peserta, finalis, dan juara.
Status cuti/nonaktif adalah snapshot, bukan prediksi DO. Generasi pertama merujuk pendidikan orang tua, bukan seluruh anggota keluarga.
''')
code(r'''
raw = [pd.read_csv(ROOT / name, sep=';') for name in FILES]
profil, prestasi_raw, generasi, ekonomi, riwayat = raw
for frame in [profil, generasi, ekonomi]:
    assert frame.ID_Mahasiswa.is_unique, 'ID mahasiswa berulang pada tabel utama.'
    assert not frame.ID_Mahasiswa.isna().any(), 'ID mahasiswa kosong.'
    assert set(frame.ID_Mahasiswa) == set(profil.ID_Mahasiswa), 'Cakupan ID tabel utama berbeda.'
assert not riwayat.duplicated(['ID_Mahasiswa', 'Semester_Ke']).any(), 'Riwayat semester berulang.'
assert set(prestasi_raw.ID_Mahasiswa).issubset(set(profil.ID_Mahasiswa))
assert set(riwayat.ID_Mahasiswa) == set(profil.ID_Mahasiswa)

prestasi = prestasi_raw.drop_duplicates().copy()
d = profil.merge(generasi, on='ID_Mahasiswa', validate='one_to_one').merge(
    ekonomi, on='ID_Mahasiswa', suffixes=('_profil', '_ekonomi'), validate='one_to_one')
for col in ['Status_Generasi_Pertama', 'Bekerja_Sambil_Kuliah', 'Status_Penerima_Beasiswa']:
    assert d[col].isin(['Ya', 'Tidak']).all(), f'Kategori tidak dikenal: {col}'
d['fg'] = d.Status_Generasi_Pertama.eq('Ya').astype(int)
d['work'] = d.Bekerja_Sambil_Kuliah.eq('Ya').astype(int)
d['sch'] = d.Status_Penerima_Beasiswa.eq('Ya').astype(int)
d['achievement'] = d.ID_Mahasiswa.isin(prestasi.ID_Mahasiswa).astype(int)
d['winner'] = d.ID_Mahasiswa.isin(prestasi.loc[
    prestasi.Capaian_Prestasi.isin(['Juara 1', 'Juara 2', 'Juara 3']), 'ID_Mahasiswa']).astype(int)
d['natplus'] = d.ID_Mahasiswa.isin(prestasi.loc[
    prestasi.Tingkat_Kegiatan.isin(['Tingkat Nasional', 'Tingkat Internasional']), 'ID_Mahasiswa']).astype(int)
d['interrupted'] = d.Status_Mahasiswa.isin(['Cuti', 'Non-Aktif/DO']).astype(int)
ipk = riwayat.pivot(index='ID_Mahasiswa', columns='Semester_Ke', values='IPK_Kumulatif')
ips = riwayat.pivot(index='ID_Mahasiswa', columns='Semester_Ke', values='IP_Semester')
assert {1, 4}.issubset(ipk.columns)
d = d.merge(ipk[[1, 4]].rename(columns={1: 's1', 4: 's4'}),
            left_on='ID_Mahasiswa', right_index=True, how='left', validate='one_to_one')
d = d.merge(ips[[4]].rename(columns={4: 'ips4'}),
            left_on='ID_Mahasiswa', right_index=True, how='left', validate='one_to_one')
d['gain'] = d.s4 - d.s1
fixed = d.dropna(subset=['s1', 's4']).copy()
low = d.loc[d.Kategori_Ekonomi.eq('Rendah')].copy()
low_fg = low.loc[low.fg.eq(1)].copy()

def summary(frame, groups):
    return frame.groupby(groups, observed=True).agg(
        n=('ID_Mahasiswa', 'size'), ipk=('IPK_Mahasiswa', 'mean'),
        achievement=('achievement', 'mean'), winner=('winner', 'mean'),
        natplus=('natplus', 'mean'), interrupted=('interrupted', 'mean'),
        work_rate=('work', 'mean'), scholarship=('sch', 'mean')).reset_index()

cohort = fixed.groupby('fg').agg(n=('ID_Mahasiswa', 'size'), s1=('s1', 'mean'),
                                s4=('s4', 'mean'), gain=('gain', 'mean'))
intersection = summary(low, ['fg', 'work']).sort_values(['fg', 'work'])
economy_summary = summary(d, ['fg', 'Kategori_Ekonomi'])
gap1 = cohort.loc[0, 's1'] - cohort.loc[1, 's1']
gap4 = cohort.loc[0, 's4'] - cohort.loc[1, 's4']
gain_ratio = cohort.loc[1, 'gain'] / cohort.loc[0, 'gain']
narrowing = 1 - gap4 / gap1
headlines = pd.DataFrame([
    ['Generasi pertama / seluruh mahasiswa', int(d.fg.sum()), len(d)],
    ['Generasi pertama / mahasiswa ekonomi rendah', int(low.fg.sum()), len(low)],
    ['Bekerja / generasi pertama ekonomi rendah', int(low_fg.work.sum()), len(low_fg)]
], columns=['indikator', 'pembilang', 'penyebut'])
headlines['proporsi'] = headlines.pembilang / headlines.penyebut
audit = pd.DataFrame({'sumber': FILES, 'baris_mentah': [len(f) for f in raw]})
display(audit, headlines, cohort, intersection)
for name, frame in {'audit_sumber': audit, 'headline': headlines,
                    'kohort_s1_s4': cohort.reset_index(), 'irisan_ekonomi_rendah': intersection,
                    'capaian_menurut_ekonomi': economy_summary}.items():
    frame.to_csv(OUT / 'tabel' / f'{name}.csv', index=False, encoding='utf-8-sig')
''')
md('''
## 3. Latar belakang: ikon dan teks saja
Ikon dibuat sebagai bentuk vektor sederhana, tanpa grafik data. SVG dapat disunting di aplikasi desain.
''')
code(r'''
def icon(ax, kind, color):
    ax.set(xlim=(0, 1), ylim=(0, 1), aspect='equal')
    ax.axis('off')
    if kind == 'family':
        for x, y, r in [(0.25, 0.70, 0.10), (0.75, 0.70, 0.10), (0.50, 0.49, 0.08)]:
            ax.add_patch(Circle((x, y), r, fill=False, ec=color, lw=2.6))
        for x, y, w, h in [(0.08, 0.27, 0.34, 0.29), (0.58, 0.27, 0.34, 0.29), (0.38, 0.09, 0.24, 0.25)]:
            ax.add_patch(Arc((x+w/2, y), w, 2*h, theta1=0, theta2=180, ec=color, lw=2.6))
    elif kind == 'wallet':
        box(ax, 0.12, 0.25, 0.76, 0.46, face='none', edge=color, lw=2.6)
        ax.add_patch(Rectangle((0.58, 0.39), 0.31, 0.19, fill=False, ec=color, lw=2.6))
        ax.add_patch(Circle((0.67, 0.48), 0.025, color=color))
        ax.add_patch(Circle((0.34, 0.81), 0.11, fill=False, ec=color, lw=2.6))
        ax.plot([0.34, 0.34, 0.40], [0.89, 0.81, 0.81], color=color, lw=2)
    else:
        ax.add_patch(Polygon([(0.30, 0.82), (0.70, 0.82), (0.64, 0.45),
                              (0.50, 0.34), (0.36, 0.45)], fill=False, ec=color, lw=2.6))
        ax.add_patch(Arc((0.30, 0.64), 0.30, 0.30, theta1=90, theta2=270, ec=color, lw=2.6))
        ax.add_patch(Arc((0.70, 0.64), 0.30, 0.30, theta1=-90, theta2=90, ec=color, lw=2.6))
        ax.plot([0.5, 0.5], [0.34, 0.17], color=color, lw=2.6)
        ax.plot([0.32, 0.68], [0.14, 0.14], color=color, lw=2.6)

fig, ax = canvas('Di balik angka, ada perjalanan',
                 'Sama-Sama Kuliah, Tak Sama Bebannya', size=(12, 5.6))
ax.axis('off')
items = [('family', 'Titik berangkat', 'Generasi pertama: kedua orang tua belum pernah menempuh pendidikan tinggi.', C['fg']),
         ('wallet', 'Kondisi perjalanan', 'Ekonomi, aktivitas kerja, dan dukungan keluarga menyertai kebutuhan yang berbeda.', C['nonfg']),
         ('trophy', 'Membaca capaian', 'Pahami hasil yang tercatat bersama titik awal dan perkembangan mahasiswa.', C['green'])]
for i, (kind, title, text, color) in enumerate(items):
    x = 0.055 + i * 0.315
    small = fig.add_axes([x+0.075, 0.46, 0.14, 0.23])
    icon(small, kind, color)
    fig.text(x+0.14, 0.405, title, ha='center', weight='bold', fontsize=13, color=color)
    fig.text(x+0.14, 0.345, fill(text, 34), ha='center', va='top', fontsize=11, linespacing=1.5)
save_visual(fig, '00_latar_ikon_teks', 'Latar belakang',
            'Latar konseptual; ikon bukan ukuran data.', 'Di balik angka, ada perjalanan')
''')
md('''
## 4. Pembahasan: konteks sederhana
Tiga angka besar memiliki penyebut berbeda. Jangan menjumlahkan persentasenya.
''')
code(r'''
fig, ax = canvas('Kelompok besar, kondisi yang beririsan',
                 'Tiga sudut pandang dengan penyebut yang berbeda', size=(12.5, 5.8))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis('off')
labels = ['Generasi pertama\ndi antara seluruh\nmahasiswa',
          'Generasi pertama\ndi antara mahasiswa\nekonomi rendah',
          'Bekerja\ndi antara generasi pertama\nekonomi rendah']
for i, row in headlines.iterrows():
    x = i * 0.335
    color = [C['fg'], C['nonfg'], C['risk']][i]
    box(ax, x+0.02, 0.11, 0.285, 0.83)
    ax.text(x+0.16, 0.72, persen(row.proporsi), ha='center', fontsize=35, weight='bold', color=color)
    ax.text(x+0.16, 0.48, labels[i], ha='center', va='center', fontsize=11, linespacing=1.6)
    ax.text(x+0.16, 0.23, f'{jumlah(row.pembilang)} / {jumlah(row.penyebut)} mahasiswa', ha='center', fontsize=10)
save_visual(fig, '01_konteks_angka_besar', 'Pembahasan',
            'Persentase dihitung per mahasiswa; penyebut dicantumkan pada setiap kartu.', 'Konteks utama')
''')
code(r'''
econ_order = ['Rendah', 'Menengah', 'Tinggi']
econ_counts = pd.crosstab(d.fg, d.Kategori_Ekonomi).reindex(index=[1, 0], columns=econ_order, fill_value=0)
econ_pct = econ_counts.div(econ_counts.sum(axis=1), axis=0) * 100
fig, ax = canvas('Profil ekonomi kedua kelompok berbeda',
                 'Komposisi ekonomi di dalam masing-masing kelompok generasi pertama', size=(11.5, 5.7))
econ_colors = [C['risk'], '#DCA56B', C['nonfg']]
left = np.zeros(2)
for label, color in zip(econ_order, econ_colors):
    values = econ_pct[label].to_numpy()
    ax.barh([1, 0], values, left=left, height=0.38, color=color, label=label)
    for y, start, value in zip([1, 0], left, values):
        ax.text(start+value/2, y, angka(value)+'%', ha='center', va='center',
                color=C['white'] if label != 'Menengah' else C['ink'], fontsize=11, weight='bold')
    left += values
ax.set_yticks([1, 0], [f'{GROUP[g]}\nn={jumlah(econ_counts.loc[g].sum())}' for g in [1, 0]], fontsize=10)
clean_percent(ax)
ax.set_ylim(-0.6, 1.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.52, 1.05), ncol=3, frameon=False)
ax.set_xlabel('Persentase dalam masing-masing kelompok')
fig.subplots_adjust(left=0.24)
save_visual(fig, '02_ekonomi_stacked_100', 'Pembahasan',
            f'Penyebut bar berbeda dari headline {persen(low.fg.mean())}: headline memakai {jumlah(len(low))} mahasiswa ekonomi rendah.',
            'Komposisi ekonomi')
econ_pct.reset_index().to_csv(OUT / 'tabel' / 'komposisi_ekonomi_persen.csv', index=False, encoding='utf-8-sig')
''')
code(r'''
work_summary = low.groupby('fg').agg(n=('ID_Mahasiswa', 'size'), bekerja=('work', 'sum'), rate=('work', 'mean')).reindex([1, 0])
fig, ax = canvas('Hampir separuh generasi pertama ekonomi rendah bekerja',
                 'Perbandingan dibatasi pada mahasiswa kategori ekonomi rendah', size=(12, 5.7))
for y, g in zip([1, 0], [1, 0]):
    row = work_summary.loc[g]
    ax.barh(y, 100*row.rate, height=0.35, color=COLORS[g])
    ax.text(100*row.rate+2, y, f'{persen(row.rate)}  ({jumlah(row.bekerja)}/{jumlah(row.n)})', va='center', fontsize=12)
ax.set_yticks([1, 0], [GROUP[1], GROUP[0]], fontsize=10)
ax.set_ylim(-0.55, 1.55)
ax.set_xlabel('Mahasiswa bekerja sambil kuliah')
clean_percent(ax)
fig.subplots_adjust(left=0.24)
save_visual(fig, '03_bekerja_ekonomi_rendah', 'Pembahasan',
            'Data tidak mencatat alasan bekerja, jam kerja, atau kapan mahasiswa mulai bekerja.', 'Bekerja pada ekonomi rendah')
work_summary.reset_index().to_csv(OUT / 'tabel' / 'bekerja_ekonomi_rendah.csv', index=False, encoding='utf-8-sig')
''')
md('''
## 5. Analisis lintasan: kohort tetap semester 1 dan 4
Kenaikan tidak otomatis membuktikan ketangguhan atau efek intervensi. Nilai awal dan batas atas IPK perlu dipertimbangkan.
''')
code(r'''
fig, ax = canvas('Kenaikan lebih besar, selisih masih tersisa',
                 f'Kohort tetap: {jumlah(len(fixed))} mahasiswa dengan catatan semester 1 dan 4', size=(11.5, 6.3))
for g in [0, 1]:
    row = cohort.loc[g]
    values = [row.s1, row.s4]
    ax.plot([0, 1], values, color=COLORS[g], lw=3.5, marker='o', ms=10)
    for x, value in zip([0, 1], values):
        ax.annotate(angka(value, 2), (x, value), xytext=(-16 if x == 0 else 16, 0),
                    textcoords='offset points', ha='right' if x == 0 else 'left',
                    va='center', fontsize=15, weight='bold', color=COLORS[g])
    ax.text(1.23, row.s4, f'{GROUP[g]}\nn={jumlah(row.n)}; +{angka(row.gain, 2)} poin',
            va='center', fontsize=10.5, color=COLORS[g], linespacing=1.5)
ax.set(xlim=(-0.30, 1.92), ylim=(2.45, 3.7), ylabel='Rata-rata IPK kumulatif')
ax.set_xticks([0, 1], ['Semester 1', 'Semester 4'])
ax.grid(axis='y', alpha=0.35, color=C['line'])
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: angka(x, 1)))
fig.text(0.50, 0.825, f'Kenaikan {angka(gain_ratio, 2)}× lebih besar; selisih menyempit {angka(100*narrowing, 0)}%',
         ha='center', fontsize=11.5, weight='bold')
save_visual(fig, '04_slope_ipk_kohort_tetap', 'Analisis inti',
            'Sumbu IPK diperbesar (2,45–3,70); angka turunan dihitung sebelum pembulatan.', 'Lintasan IPK kohort tetap')
''')
md('''
## 6. Analisis irisan: matriks 2×2
Empat kelompok pada ekonomi rendah, bukan tangga sebab-akibat. Setiap kartu memiliki penyebut sendiri.
''')
code(r'''
fig, ax = canvas('Ekonomi sama, kombinasi kondisi berbeda',
                 'Kategori ekonomi rendah: generasi pertama × bekerja sambil kuliah', size=(12.8, 8.2), bottom=0.17)
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis('off')
fig.subplots_adjust(left=0.16, right=0.94, top=0.79)
for col, work in enumerate([0, 1]):
    ax.text(0.25+col*0.5, 0.96, ['Tidak bekerja', 'Bekerja'][col], ha='center', fontsize=13, weight='bold')
for row_index, fg in enumerate([0, 1]):
    y = 0.51 if row_index == 0 else 0.04
    ax.text(-0.045, y+0.20, 'Bukan generasi\npertama' if fg == 0 else 'Generasi\npertama',
            ha='right', va='center', fontsize=11, color=COLORS[fg], weight='bold')
    for col, work in enumerate([0, 1]):
        row = intersection.loc[intersection.fg.eq(fg) & intersection.work.eq(work)].iloc[0]
        x = 0.02+col*0.5
        edge = C['risk'] if fg == 1 and work == 1 else C['line']
        box(ax, x, y, 0.44, 0.38, edge=edge, lw=2.5 if fg == 1 and work == 1 else 1.2)
        ax.text(x+0.025, y+0.32, 'n = '+jumlah(row.n), fontsize=10, color=C['muted'])
        ax.text(x+0.025, y+0.19, angka(row.ipk, 2), fontsize=28, weight='bold', color=COLORS[fg])
        ax.text(x+0.19, y+0.21, 'IPK terakhir', fontsize=10, va='center')
        ax.text(x+0.025, y+0.11, persen(row.achievement)+'  catatan prestasi/kegiatan', fontsize=10)
        ax.text(x+0.025, y+0.04, persen(row.interrupted)+'  cuti atau nonaktif/DO', fontsize=10, color=edge if edge==C['risk'] else C['ink'])
save_visual(fig, '05_matriks_irisan_2x2', 'Analisis inti',
            'Cuti/nonaktif adalah status tercatat, bukan prediksi. Catatan kegiatan termasuk peserta, finalis, dan juara.',
            'Matriks irisan ekonomi rendah')
''')
md('''
## 7. Model terkontrol dan forest plot

OLS memakai standard error HC3; logistik binomial memakai kovarians sandwich HC0. Interval kepercayaan 95% menggunakan pendekatan normal.
Model utama menambahkan kategori lama studi. Model nilai semester 4 mempertimbangkan nilai semester 1 dan angkatan.
Outcome model terakhir adalah **IP semester 4**, bukan IPK kumulatif. OR bukan persentase probabilitas.
''')
code(r'''
def model_frame(data, outcome, extra):
    nums = ['fg', 'work', 'sch', 'Tingkat_Dukungan_Keluarga', 'Jumlah_Tanggungan_Keluarga']
    cats = ['Kategori_Ekonomi', 'Kategori_UKT', 'Jenis_Kelamin', 'Fakultas']
    if extra == 'duration':
        cats += ['Masa_Studi_Semester']
    if extra == 'baseline':
        nums += ['s1']
        cats += ['Angkatan']
    subset = data.dropna(subset=[outcome, *nums, *cats]).copy()
    x = subset[nums].astype(float)
    for col in cats:
        x = pd.concat([x, pd.get_dummies(subset[col].astype('category'),
                       prefix=col, drop_first=True, dtype=float)], axis=1)
    x = sm.add_constant(x, has_constant='add')
    assert np.linalg.matrix_rank(x.to_numpy()) == x.shape[1], 'Matriks model tidak full rank.'
    return subset[outcome].astype(float), x

def fit_ols(data, outcome='IPK_Mahasiswa', extra='duration'):
    y, x = model_frame(data, outcome, extra)
    return sm.OLS(y, x).fit(cov_type='HC3', use_t=False)

def fit_logistic(data, extra='duration'):
    y, x = model_frame(data, 'achievement', extra)
    fit = sm.GLM(y, x, family=sm.families.Binomial()).fit(cov_type='HC0')
    assert fit.converged, 'Regresi logistik belum konvergen.'
    return fit

ols_original = fit_ols(d, extra='original')
logit_original = fit_logistic(d, extra='original')
ols_duration = fit_ols(d)
logit_duration = fit_logistic(d)
ols_baseline = fit_ols(fixed, outcome='ips4', extra='baseline')

def coefficients(fit, name, odds=False):
    ci = fit.conf_int()
    result = pd.DataFrame({'term': fit.params.index, 'estimate': fit.params.to_numpy(),
                          'low': ci.iloc[:, 0].to_numpy(), 'high': ci.iloc[:, 1].to_numpy(),
                          'p': fit.pvalues.to_numpy()})
    if odds:
        result[['estimate', 'low', 'high']] = np.exp(result[['estimate', 'low', 'high']])
    result['model'] = name
    result['n'] = int(fit.nobs)
    result['ukuran'] = 'Odds ratio' if odds else 'Koefisien IP/IPK'
    return result

model_tables = [coefficients(ols_original, 'OLS notebook'),
                coefficients(logit_original, 'Logistik notebook', True),
                coefficients(ols_duration, 'OLS + lama studi'),
                coefficients(logit_duration, 'Logistik + lama studi', True),
                coefficients(ols_baseline, 'IP semester 4 + baseline')]
model_results = pd.concat(model_tables, ignore_index=True)
model_results.to_csv(OUT / 'tabel' / 'koefisien_semua_model.csv', index=False, encoding='utf-8-sig')
model_info = pd.DataFrame([
    ['OLS notebook', int(ols_original.nobs), ols_original.rsquared, 'HC3'],
    ['OLS + lama studi', int(ols_duration.nobs), ols_duration.rsquared, 'HC3'],
    ['IP semester 4 + baseline', int(ols_baseline.nobs), ols_baseline.rsquared, 'HC3']
], columns=['model', 'n', 'r_squared', 'standard_error'])
model_info.to_csv(OUT / 'tabel' / 'ringkasan_model_ols.csv', index=False, encoding='utf-8-sig')
display(model_info, model_results.loc[model_results.term.isin(['fg', 'work', 'sch'])])
''')
code(r'''
TERM_LABEL = {'fg': 'Generasi pertama', 'work': 'Bekerja sambil kuliah', 'sch': 'Penerima beasiswa'}
TERM_COLOR = {'fg': C['fg'], 'work': C['risk'], 'sch': C['green']}

def forest(frame, title, subtitle, name, xlabel, reference, limits, note, log_scale=False):
    rows = frame.set_index('term').loc[['fg', 'work', 'sch']]
    fig, ax = canvas(title, subtitle, size=(12.6, 6.0))
    fig.subplots_adjust(left=0.23, right=0.66)
    ax.axvline(reference, color=C['muted'], ls='--', lw=1.4)
    for y, (term, row) in zip([2, 1, 0], rows.iterrows()):
        ax.errorbar(row.estimate, y, xerr=[[row.estimate-row.low], [row.high-row.estimate]],
                    fmt='o', color=TERM_COLOR[term], capsize=5, ms=9, lw=2)
        ax.text(1.045, y, f'{angka(row.estimate, 3)}  [{angka(row.low, 3)}; {angka(row.high, 3)}]',
                transform=ax.get_yaxis_transform(), va='center', fontsize=10)
    ax.text(1.045, 2.62, 'Estimasi [CI 95%]', transform=ax.get_yaxis_transform(), fontsize=10, weight='bold')
    ax.set_yticks([2, 1, 0], [TERM_LABEL[t] for t in rows.index], fontsize=10)
    ax.set(xlim=limits, ylim=(-0.7, 2.85), xlabel=xlabel)
    if log_scale:
        ax.set_xscale('log')
        ax.set_xticks([0.4, 0.5, 0.75, 1, 1.5, 2])
        ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: angka(x, 2)))
    ax.grid(axis='x', color=C['line'], alpha=0.35)
    save_visual(fig, name, 'Analisis inti', note, title)

forest(model_tables[2], 'Selisih IPK tetap terlihat setelah penyesuaian',
       f'OLS; n={jumlah(ols_duration.nobs)}; R²={angka(ols_duration.rsquared, 3)}; standard error HC3',
       '06_forest_ipk_terkontrol', 'Koefisien terhadap IPK terakhir (poin)', 0, (-0.32, 0.25),
       'Kontrol: ekonomi, UKT, bekerja, beasiswa, dukungan, tanggungan, gender, fakultas, lama studi. Asosiasi, bukan kausal.')
''')
code(r'''
forest(model_tables[3], 'Odds catatan kegiatan berbeda setelah penyesuaian',
       f'Logistik binomial; n={jumlah(logit_duration.nobs)}; interval kepercayaan 95%; kovarians robust HC0',
       '07_forest_odds_prestasi', 'Odds ratio (sumbu log; acuan = 1)', 1, (0.36, 2.1),
       'Outcome: ≥1 catatan kegiatan, termasuk peserta/finalis/juara. OR 0,50 bukan probabilitas 50%.', log_scale=True)
''')
code(r'''
forest(model_tables[4], 'Nilai awal dan perkembangan memberi gambaran lain',
       f'Outcome: IP semester 4; n={jumlah(ols_baseline.nobs)}; R²={angka(ols_baseline.rsquared, 3)}',
       '08_forest_ip_semester4_baseline', 'Koefisien terhadap IP semester 4 (poin)', 0, (-0.11, 0.15),
       'Kontrol: nilai semester 1, angkatan, ekonomi, UKT, bekerja, beasiswa, dukungan, tanggungan, gender, fakultas.')
''')
md('''
## 8. Jembatan strategi: PETA
Diagram berikut adalah strategi yang diusulkan, bukan hasil model sebab-akibat.
''')
code(r'''
fig, ax = canvas('Sebelum membangun JEMBATAN, tentukan PETA',
                 'Dari pembacaan kebutuhan menuju dukungan yang ditindaklanjuti', size=(12.5, 6.3))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis('off')
ax.plot([0.07, 0.93], [0.39, 0.39], color=C['green'], lw=5, alpha=0.45)
steps = [('P', 'Petakan kebutuhan', 'Ekonomi, kerja, dukungan\ndan kendala'),
         ('E', 'Evaluasi perkembangan', 'Lintasan nilai\ndan titik awal'),
         ('T', 'Tautkan dukungan', 'Konfirmasi kebutuhan\ndan rujukan layanan'),
         ('A', 'Audit hasil', 'Keterjangkauan\ndan tindak lanjut')]
for i, (letter, title, text) in enumerate(steps):
    x = 0.125+i*0.25
    ax.add_patch(Circle((x, 0.39), 0.063, facecolor=C['green'], edgecolor=C['bg'], lw=3))
    ax.text(x, 0.39, letter, ha='center', va='center', fontsize=24, weight='bold', color=C['white'])
    ax.text(x, 0.67, title.replace(' ', '\n', 1), ha='center', va='center', fontsize=12, weight='bold', linespacing=1.4)
    ax.text(x, 0.16, text, ha='center', va='center', fontsize=10, linespacing=1.5)
    if i < 3:
        ax.add_patch(FancyArrowPatch((x+0.072, 0.39), (x+0.17, 0.39), arrowstyle='->',
                                    mutation_scale=14, color=C['green'], lw=2))
save_visual(fig, '09_strategi_peta', 'Jembatan strategi',
            'PETA adalah usulan alur pendampingan. Keputusan layanan tetap memerlukan konfirmasi mahasiswa.', 'Strategi PETA')
''')
md('''
## 9. Solusi: mockup JEMBATAN
Mockup statis, bukan aplikasi operasional. Angka kelompok berasal dari CSV; layanan merupakan contoh antarmuka.
Waktu respons dan penggunaan layanan belum tersedia pada dataset, sehingga tidak diberi angka rekaan.
''')
code(r'''
fig, ax = canvas('JEMBATAN: dari data menuju pendampingan',
                 'Usulan prototipe; dashboard kelompok, lintasan akademik, rujukan, dan tindak lanjut', size=(13.5, 8.2), bottom=0.15)
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis('off')
box(ax, 0.005, 0.02, 0.985, 0.95, edge=C['nonfg'], lw=1.7)
ax.add_patch(Rectangle((0.005, 0.85), 0.985, 0.12, color=C['nonfg']))
ax.text(0.03, 0.91, 'JEMBATAN', color=C['white'], fontsize=18, weight='bold', va='center')
ax.text(0.97, 0.91, 'MOCKUP STATIS', color=C['white'], fontsize=10, ha='right', va='center')
ax.add_patch(Rectangle((0.015, 0.035), 0.19, 0.79, facecolor=C['light'], edgecolor='none'))
for y, text in zip([0.75, 0.63, 0.51, 0.39], ['Peta kebutuhan', 'Lintasan nilai', 'Rujukan', 'Tindak lanjut']):
    ax.text(0.03, y, text, fontsize=10, weight='bold' if y==0.75 else 'normal')
ax.text(0.235, 0.79, 'Angka kartu: generasi pertama · ekonomi rendah', fontsize=11, weight='bold')
cards = [('Mahasiswa', jumlah(len(low_fg))), ('Bekerja', persen(low_fg.work.mean())),
         ('Catatan kegiatan', persen(low_fg.achievement.mean()))]
for i, (label, value) in enumerate(cards):
    x = 0.235+i*0.25
    box(ax, x, 0.57, 0.215, 0.15)
    ax.text(x+0.02, 0.675, label, fontsize=9, color=C['muted'])
    ax.text(x+0.02, 0.605, value, fontsize=22, weight='bold', color=C['fg'])
box(ax, 0.235, 0.105, 0.34, 0.39)
ax.text(0.25, 0.455, 'Lintasan IPK kelompok', fontsize=11, weight='bold')
for g in [0, 1]:
    row = cohort.loc[g]
    yy = 0.20 + (np.array([row.s1, row.s4])-2.5)*0.18
    ax.plot([0.28, 0.51], yy, color=COLORS[g], lw=2.5, marker='o')
    ax.text(0.515, yy[-1], angka(row.s4, 2), fontsize=9, color=COLORS[g], va='center')
ax.text(0.28, 0.17, 'S1', fontsize=9)
ax.text(0.51, 0.17, 'S4', fontsize=9)
ax.text(0.25, 0.12, f'Semua ekonomi; n={jumlah(len(fixed))}; dua kelompok', fontsize=8.5, color=C['muted'])
box(ax, 0.605, 0.105, 0.34, 0.39)
ax.text(0.625, 0.455, 'Rujukan sesuai kebutuhan', fontsize=11, weight='bold')
for y, text in zip([0.38, 0.32, 0.26], ['Mentor akademik', 'Informasi bantuan biaya', 'Pendamping kegiatan']):
    ax.add_patch(Circle((0.636, y), 0.007, facecolor=C['green']))
    ax.text(0.652, y, text, fontsize=9.5, va='center')
ax.text(0.625, 0.195, 'Contoh layanan; perlu verifikasi kampus', fontsize=8, color=C['muted'])
ax.text(0.625, 0.135, 'Tindak lanjut: menunggu data pilot', fontsize=8.5, color=C['green'], weight='bold')
save_visual(fig, '10_mockup_jembatan', 'Solusi',
            'Angka kartu: mahasiswa generasi pertama ekonomi rendah. Mockup bukan sistem prediksi/penentu kelayakan bantuan.',
            'Mockup JEMBATAN')
''')
md('''
## 10. Visual alternatif: prestasi menurut ekonomi
Gunakan sebagai pengganti salah satu visual konteks jika cerita ingin lebih menonjolkan kegiatan/prestasi.
''')
code(r'''
fig, ax = canvas('Perbedaan catatan kegiatan terlihat pada setiap kategori ekonomi',
                 'Persentase mahasiswa dengan ≥1 catatan; bukan jumlah entri kegiatan', size=(12.3, 6.3))
fig.subplots_adjust(left=0.18)
for y, econ in zip([2, 1, 0], econ_order):
    rows = economy_summary.loc[economy_summary.Kategori_Ekonomi.eq(econ)].set_index('fg')
    a, b = 100*rows.loc[1, 'achievement'], 100*rows.loc[0, 'achievement']
    ax.plot([a, b], [y, y], color=C['line'], lw=5)
    for g in [1, 0]:
        value = 100*rows.loc[g, 'achievement']
        ax.scatter(value, y, s=120, color=COLORS[g], label=GROUP[g] if y==2 else None, zorder=3)
        ax.text(value, y+0.17 if g==0 else y-0.20,
                f'{angka(value)}% (n={jumlah(rows.loc[g, "n"])})', ha='center', fontsize=9.5, color=COLORS[g])
ax.set_yticks([2, 1, 0], econ_order)
ax.set_ylim(-0.6, 2.7)
ax.set_xlabel('Mahasiswa dengan catatan prestasi/kegiatan')
clean_percent(ax)
ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.12), frameon=False, ncol=2, fontsize=10)
save_visual(fig, '11_dumbbell_prestasi_ekonomi', 'Alternatif',
            'Perbedaan catatan bukan ukuran langsung akses lomba atau kemampuan; kategori ekonomi tinggi generasi pertama n=122.',
            'Catatan kegiatan menurut ekonomi')
''')
md('''
### Alternatif: beasiswa dan aktivitas bekerja
Penerimaan beasiswa dan bekerja dapat hadir bersamaan. Grafik ini tidak mengukur kecukupan atau dampak beasiswa.
''')
code(r'''
sch_work = low_fg.groupby('sch').agg(n=('ID_Mahasiswa', 'size'), bekerja=('work', 'sum'), rate=('work', 'mean')).reindex([1, 0])
fig, ax = canvas('Beasiswa dan aktivitas bekerja dapat hadir bersamaan',
                 'Mahasiswa generasi pertama pada kategori ekonomi rendah', size=(11.5, 5.7))
fig.subplots_adjust(left=0.25)
for y, sch in zip([1, 0], [1, 0]):
    row = sch_work.loc[sch]
    ax.barh(y, row.rate*100, height=0.35, color=C['green'] if sch else C['fg'])
    ax.text(row.rate*100+2, y, f'{persen(row.rate)} ({jumlah(row.bekerja)}/{jumlah(row.n)})', va='center', fontsize=11)
ax.set_yticks([1, 0], ['Penerima beasiswa', 'Bukan penerima beasiswa'], fontsize=10)
ax.set_ylim(-0.6, 1.6)
ax.set_xlabel('Mahasiswa yang bekerja sambil kuliah')
clean_percent(ax)
save_visual(fig, '12_beasiswa_dan_bekerja', 'Alternatif',
            'Tidak tersedia informasi alasan bekerja atau besarnya bantuan. Perbandingan ini bukan evaluasi efektivitas beasiswa.',
            'Beasiswa dan bekerja')
sch_work.reset_index().to_csv(OUT / 'tabel' / 'beasiswa_dan_bekerja.csv', index=False, encoding='utf-8-sig')
''')
md('''
### Alternatif: lintasan lengkap semester 1–4
Memakai mahasiswa yang sama dan memeriksa kelengkapan keempat semester sebelum menggambar garis.
''')
code(r'''
trajectory = ipk.reindex(fixed.ID_Mahasiswa)[[1, 2, 3, 4]]
assert not trajectory.isna().any().any(), 'Ada semester antara 1–4 yang kosong; jangan menggambar lintasan sebagai lengkap.'
trajectory = trajectory.join(fixed.set_index('ID_Mahasiswa')[['fg']])
trajectory_mean = trajectory.groupby('fg')[[1, 2, 3, 4]].mean()
fig, ax = canvas('Lintasan empat semester pada mahasiswa yang sama',
                 f'Kohort tetap n={jumlah(len(trajectory))}; IPK kumulatif, bukan forecasting', size=(11.5, 6))
for g in [0, 1]:
    values = trajectory_mean.loc[g].to_numpy()
    ax.plot(range(1, 5), values, color=COLORS[g], marker='o', lw=3,
            label=f'{GROUP[g]} (n={jumlah(cohort.loc[g, "n"])})')
    for x, value in zip(range(1, 5), values):
        ax.annotate(angka(value, 2), (x, value), xytext=(0, 12), textcoords='offset points',
                    ha='center', fontsize=11, color=COLORS[g])
ax.set(xlim=(0.7, 4.3), ylim=(2.4, 3.75), ylabel='Rata-rata IPK kumulatif')
ax.set_xticks(range(1, 5), [f'Semester {s}' for s in range(1, 5)])
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: angka(x, 1)))
ax.grid(axis='y', alpha=0.35, color=C['line'])
ax.legend(loc='upper left', fontsize=10, frameon=False)
save_visual(fig, '13_lintasan_semester_1_4', 'Alternatif',
            'Sumbu IPK diperbesar (2,40–3,75). Nilai pada semester berikutnya tidak diprediksi.', 'Lintasan empat semester')
trajectory_mean.rename(columns=lambda x: f'semester_{x}').reset_index().to_csv(
    OUT / 'tabel' / 'lintasan_semester_1_4.csv', index=False, encoding='utf-8-sig')
''')
md('''
## 11. Preview susunan poster A3
Preview menggabungkan visual utama, bukan seluruh alternatif. Ini referensi susunan, bukan pengganti penyuntingan desain final.
SVG preview A3 menyertakan gambar raster; gunakan SVG individual untuk mengedit elemen grafik.
''')
code(r'''
main_visuals = ['00_latar_ikon_teks', '01_konteks_angka_besar', '04_slope_ipk_kohort_tetap',
                '05_matriks_irisan_2x2', '06_forest_ipk_terkontrol', '07_forest_odds_prestasi',
                '08_forest_ip_semester4_baseline', '09_strategi_peta', '10_mockup_jembatan']
fig = plt.figure(figsize=(11.69, 16.54), facecolor=C['bg'])
grid = fig.add_gridspec(7, 2, left=0.025, right=0.975, bottom=0.04, top=0.94,
                       hspace=0.035, wspace=0.03, height_ratios=[1, 1, 1.12, 1.3, 1.05, 1, 1.3])
positions = [(grid[0, :], main_visuals[0]), (grid[1, :], main_visuals[1]),
             (grid[2, :], main_visuals[2]), (grid[3, :], main_visuals[3]),
             (grid[4, 0], main_visuals[4]), (grid[4, 1], main_visuals[5]),
             (grid[5, 0], main_visuals[6]), (grid[5, 1], main_visuals[7]),
             (grid[6, :], main_visuals[8])]
for slot, name in positions:
    ax = fig.add_subplot(slot)
    ax.imshow(plt.imread(OUT / 'png' / f'{name}.png'))
    ax.axis('off')
fig.text(0.05, 0.975, 'Sama-Sama Kuliah, Tak Sama Bebannya', fontsize=21, weight='bold', va='top')
fig.text(0.05, 0.95, 'Preview susunan A3; gunakan SVG individual untuk layout dengan teks lebih besar.',
         fontsize=9, color=C['muted'])
fig.text(0.05, 0.012, 'CDW 2026 · Data fiktif · Temuan asosiasional · JEMBATAN: usulan prototipe', fontsize=8)
fig.savefig(OUT / 'Preview_Susunan_A3.png', dpi=180, bbox_inches='tight', pad_inches=0.1)
fig.savefig(OUT / 'Preview_Susunan_A3.pdf', bbox_inches='tight', pad_inches=0.1)
fig.savefig(SVG_OUT / 'Preview_Susunan_A3.svg', format='svg', bbox_inches='tight', pad_inches=0.1)
if SHOW_FIGURES:
    display(fig)
plt.close(fig)
''')
md('''
## 12. Pemeriksaan dan ekspor
SVG mempertahankan teks, sehingga font dapat diganti saat desain. Tabel ekspor hanya agregat/koefisien, tanpa ID mahasiswa.
Clustering dan forecasting tidak digambar sebagai temuan karena belum menjadi analisis terverifikasi pada rancangan ini.
''')
code(r'''
catalog.close()
manifest_df = pd.DataFrame(manifest)
manifest_df.to_csv(OUT / 'Manifest_Visual.csv', index=False, encoding='utf-8-sig')
assert len(manifest_df) == 14
assert not manifest_df.nama.duplicated().any()
for name in [*manifest_df.nama, 'Preview_Susunan_A3']:
    file = SVG_OUT / f'{name}.svg'
    assert file.is_file() and file.stat().st_size > 1000, f'Ekspor SVG gagal: {file}'
for row in manifest:
    for folder, ext in [('png', 'png'), ('svg', 'svg'), ('pdf', 'pdf')]:
        file = OUT / folder / f'{row["nama"]}.{ext}'
        assert file.is_file() and file.stat().st_size > 1000, f'Ekspor gagal: {file}'
assert len(d) == len(profil)
assert int(intersection.n.sum()) == len(low)
assert int(cohort.n.sum()) == len(fixed)
assert np.isclose(econ_pct.sum(axis=1), 100).all()
assert np.isfinite(model_results[['estimate', 'low', 'high']].to_numpy()).all()

provenance = {'python': platform.python_version(), 'numpy': np.__version__, 'pandas': pd.__version__,
              'matplotlib': matplotlib.__version__, 'statsmodels': statsmodels.__version__,
              'sumber': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES},
              'mahasiswa': len(d), 'kohort_s1_s4': len(fixed), 'jumlah_visual': len(manifest),
              'gain_ratio': float(gain_ratio), 'gap_narrowing': float(narrowing),
              'data': 'Real World Fake Data; asosiasi bukan sebab-akibat'}
with (OUT / 'Provenance.json').open('w', encoding='utf-8') as file:
    json.dump(provenance, file, ensure_ascii=False, indent=2)
zip_path = OUT / 'Aset_Infografis_CDW2026.zip'
assets = sorted(p for p in OUT.rglob('*') if p.is_file() and p.suffix.lower() in {'.png', '.svg', '.pdf', '.csv', '.json'})
with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED) as archive:
    for file in assets:
        archive.write(file, arcname=file.relative_to(OUT))
display(manifest_df[['nama', 'bagian']])
print(f'{len(manifest)} visual individual + preview A3; seluruh pemeriksaan selesai.')
print('Folder:', OUT)
display(FileLink(str(zip_path)), FileLink(str(OUT / 'Katalog_Visual_CDW2026.pdf')))
''')

notebook = nbf.v4.new_notebook(cells=cells)
notebook.metadata = {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                     'language_info': {'name': 'python', 'version': '3.12'},
                     'cdw': {'sources': ['Naskah_Final_Infografis_CDW2026.md',
                                         'Eksplorasi_Insight_Mahasiswa_CDW2026.ipynb'],
                             'purpose': 'Visualisasi seluruh rancangan infografis'}}
nbf.validate(notebook)
target = ROOT / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb'
nbf.write(notebook, target)
print(target)
print(f'{len(cells)} sel; {sum(c.cell_type == "code" for c in cells)} sel kode.')
