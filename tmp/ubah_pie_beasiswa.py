import base64
import io
import json
from pathlib import Path
from contextlib import redirect_stdout
from copy import deepcopy

import matplotlib
matplotlib.use('Agg')

root = Path.cwd()
path = root / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb'
notebook = json.loads(path.read_text(encoding='utf-8'))
before = deepcopy(notebook)
idx = next(i for i, cell in enumerate(notebook['cells'])
           if cell['cell_type'] == 'code' and "save_visual(fig, '12_beasiswa_dan_bekerja'" in ''.join(cell['source']))
source = '''sch_work = low_fg.groupby('sch').agg(n=('ID_Mahasiswa', 'size'), bekerja=('work', 'sum'), rate=('work', 'mean')).reindex([1, 0])
fig, axes = plt.subplots(1, 2, figsize=(11.5, 6.4))
fig.subplots_adjust(left=0.07, right=0.93, top=0.75, bottom=0.29, wspace=0.35)
fig.text(0.045, 0.94, 'Beasiswa dan aktivitas bekerja dapat hadir bersamaan',
         fontsize=19, fontweight='bold', va='top')
fig.text(0.045, 0.865, 'Mahasiswa generasi pertama pada kategori ekonomi rendah',
         fontsize=10.5, color=C['muted'], va='top')
for ax, sch in zip(axes, [1, 0]):
    row = sch_work.loc[sch]
    ax.pie([row.bekerja, row.n - row.bekerja],
           colors=[C['green'] if sch else C['fg'], C['light']],
           startangle=90, counterclock=False,
           autopct=lambda value: angka(value) + '%', pctdistance=0.65,
           textprops={'fontsize': 13, 'fontweight': 'bold', 'color': C['ink']},
           wedgeprops={'edgecolor': C['bg'], 'linewidth': 2})
    ax.set_title('Penerima beasiswa' if sch else 'Bukan penerima beasiswa',
                 fontsize=13, fontweight='bold', pad=12)
    ax.text(0, -1.18, f'Bekerja: {jumlah(row.bekerja)} dari {jumlah(row.n)} mahasiswa',
            ha='center', va='top', fontsize=10, color=C['muted'])
    ax.set_aspect('equal')
fig.text(0.5, 0.18, 'Bagian berwarna: bekerja sambil kuliah | Abu muda: tidak bekerja',
         ha='center', fontsize=10, color=C['muted'])
save_visual(fig, '12_beasiswa_dan_bekerja', 'Alternatif',
            'Tidak tersedia informasi alasan bekerja atau besarnya bantuan. Perbandingan ini bukan evaluasi efektivitas beasiswa.',
            'Beasiswa dan bekerja')
sch_work.reset_index().to_csv(OUT / 'tabel' / 'beasiswa_dan_bekerja.csv', index=False, encoding='utf-8-sig')
'''
notebook['cells'][idx]['source'] = source.splitlines(keepends=True)
namespace = {}
setup = ''.join(notebook['cells'][3]['source']).replace(
    "catalog = PdfPages(OUT / 'Katalog_Visual_CDW2026.pdf')",
    "catalog = PdfPages(ROOT.parents[1] / 'tmp' / 'pie_beasiswa_verifikasi.pdf')")
setup = setup.replace('import statsmodels.api as sm\n', '')
with redirect_stdout(io.StringIO()):
    exec(compile(setup, '<persiapan>', 'exec'), namespace)
    namespace['SHOW_FIGURES'] = False
    namespace['display'] = lambda *args, **kwargs: None
    exec(compile(''.join(notebook['cells'][5]['source']), '<data>', 'exec'), namespace)
    exec(compile(source, '<pie-beasiswa>', 'exec'), namespace)
namespace['catalog'].close()
png = root / '04_Visualisasi' / 'output_visualisasi_cdw' / 'png' / '12_beasiswa_dan_bekerja.png'
notebook['cells'][idx]['outputs'] = [{
    'output_type': 'display_data',
    'data': {'image/png': base64.b64encode(png.read_bytes()).decode('ascii'),
             'text/plain': ['Dua pie chart: bekerja dan tidak bekerja menurut status beasiswa.']},
    'metadata': {}
}]
assert all(notebook['cells'][i] == before['cells'][i]
           for i in range(len(notebook['cells'])) if i != idx)
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('Sel diubah:', idx)
print(namespace['sch_work'].to_string())
print('Grafik:', png)
