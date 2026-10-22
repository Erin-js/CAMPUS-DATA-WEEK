from pathlib import Path
from textwrap import dedent
import ast
import nbformat

root = Path(__file__).resolve().parents[1]
target = root / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb'
nb = nbformat.read(target, as_version=4)
marker = '## 18. Riwayat IP dan prediksi rata-rata menurut generasi pertama'
start = next((i for i, c in enumerate(nb.cells) if c.cell_type == 'markdown' and c.source.startswith(marker)), len(nb.cells))
old_cells = nb.cells[:start]
new = []

def md(source):
    new.append(nbformat.v4.new_markdown_cell(dedent(source).strip()))

def code(source):
    source = dedent(source).strip()
    ast.parse(source)
    new.append(nbformat.v4.new_code_cell(source))

md('''
## 18. Riwayat IP dan prediksi rata-rata menurut generasi pertama

Garis penuh: rerata **IP semester** 1–3. Garis putus-putus: sambungan IP3 ke rerata prediksi IP4 dari model sebelumnya.
Kedua kelompok memakai mahasiswa uji angkatan 2024 yang sama pada setiap titik: generasi pertama n=448; pembanding n=765.
Prediksi individual dihitung terlebih dahulu, baru dirata-ratakan per kelompok; status generasi pertama bukan fitur model.

Tersedia satu grafik dengan dua garis serta alternatif dua panel berskala sama. Pilih salah satu untuk infografis.
Ini pengujian retrospektif pada data simulasi, bukan forecasting semester 5–8 atau bukti sebab-akibat.
Interval prediksi individual tidak dirata-ratakan menjadi interval rata-rata kelompok. Grafik ini tidak menampilkan band ketidakpastian.
Ekspor: PNG dan SVG di `output_visualisasi_cdw/prediksi_kelompok`; SVG juga di `svg_plot_cdw2026`.
''')
code(r'''
from matplotlib.lines import Line2D

GROUP_OUT = OUT / 'prediksi_kelompok'
for folder in ['png', 'svg', 'tabel']:
    (GROUP_OUT / folder).mkdir(parents=True, exist_ok=True)

assert test.ID_Mahasiswa.is_unique
assert test[['ip1', 'ip2', 'ip3', 'pred']].notna().all().all()
assert test.Angkatan.eq(test_year).all()
assert set(test.fg) == {0, 1}
assert np.allclose(test.pred, np.clip(predictor.predict(test[['ip1', 'ip2', 'ip3']]), 0, 4))
trajectory = test.groupby('fg', observed=True).agg(
    n=('ID_Mahasiswa', 'size'), ip1=('ip1', 'mean'), ip2=('ip2', 'mean'),
    ip3=('ip3', 'mean'), pred_ip4=('pred', 'mean'), actual_ip4=('target', 'mean')).reset_index()
trajectory['kelompok'] = trajectory.fg.map(GROUP)
assert trajectory.n.sum() == len(test)
export_trajectory = trajectory[['kelompok', 'n', 'ip1', 'ip2', 'ip3', 'pred_ip4', 'actual_ip4']].copy()
export_trajectory.to_csv(GROUP_OUT / 'tabel' / 'rerata_ip_dan_prediksi_kelompok.csv', index=False, encoding='utf-8-sig')

group_plot_names = []

def save_group_plot(fig, name):
    fig.text(0.045, 0.070, 'IP semester, bukan IPK kumulatif. Kohort tetap; prediksi individual dirata-ratakan per kelompok.', fontsize=8, color=C['muted'])
    fig.text(0.045, 0.030, 'Sumber: CSV CDW 2026. Data simulasi; evaluasi retrospektif, bukan prediksi DO.', fontsize=8, color=C['muted'])
    fig.savefig(GROUP_OUT / 'png' / f'{name}.png', dpi=DPI, bbox_inches='tight', pad_inches=0.22)
    for path in [GROUP_OUT / 'svg' / f'{name}.svg', SVG_OUT / f'{name}.svg']:
        fig.savefig(path, format='svg', bbox_inches='tight', pad_inches=0.22, transparent=True)
    group_plot_names.append(name)
    if SHOW_FIGURES:
        display(fig)
    plt.close(fig)

def draw_group_history(ax, row):
    color = COLORS[int(row.fg)]
    history = np.array([row.ip1, row.ip2, row.ip3])
    ax.plot([1, 2, 3], history, color=color, marker='o', lw=2.8, ms=6)
    ax.plot([3, 4], [row.ip3, row.pred_ip4], color=color, ls=(0, (4, 3)), lw=2.8)
    ax.scatter([4], [row.pred_ip4], facecolors=C['bg'], edgecolors=color, s=80, linewidths=2, zorder=5)
    for semester, value in enumerate([*history, row.pred_ip4], start=1):
        offset, alignment = ((0, -14), 'top') if int(row.fg) == 1 else ((0, 11), 'bottom')
        ax.annotate(angka(value, 2), (semester, value), xytext=offset, textcoords='offset points', ha='center', va=alignment, fontsize=10.5, color=C['ink'])
    ax.set_xticks([1, 2, 3, 4], ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4\n(prediksi)'])
    ax.set(xlim=(0.80, 4.30), ylim=(0, 4.10), ylabel='Rata-rata IP semester (skala 0–4)')
    ax.set_yticks(np.arange(0, 4.1, 0.5))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, pos: angka(value, 1)))
    ax.axvspan(3.5, 4.30, color=C['ink'], alpha=0.035, zorder=0)
    ax.grid(axis='y', color=C['line'], alpha=0.45)
    ax.set_axisbelow(True)

display(export_trajectory.round(3))
''')
code(r'''
fig, ax = canvas('Membaca Arah, Bukan Menentukan Nasib',
                 f'Riwayat IP semester 1–3 dan prediksi semester 4; angkatan uji {test_year}, n={jumlah(len(test))}', size=(12.2, 7.0), bottom=0.26)
for row in trajectory.itertuples():
    draw_group_history(ax, row)
handles = [
    Line2D([0], [0], color=COLORS[fg], marker='o', lw=2.5,
           label=f'{GROUP[fg]} (n={jumlah(trajectory.loc[trajectory.fg.eq(fg), "n"].iloc[0])})') for fg in [1, 0]
]+[
    Line2D([0], [0], color=C['muted'], lw=2, label='Nilai tercatat'),
    Line2D([0], [0], color=C['muted'], lw=2, ls='--', label='Prediksi model')
]
fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(0.51, 0.125), ncol=2, fontsize=9, frameon=False)
save_group_plot(fig, '23_lintasan_ip_prediksi_dua_kelompok')
''')
code(r'''
fig, _ = canvas('Dua Perjalanan, Satu Cara Membaca Arah',
                f'Kohort tetap angkatan {test_year}; garis penuh = nilai tercatat, putus-putus = prediksi IP4', size=(14.0, 7.2), bottom=0.24)
fig.axes[0].remove()
for i, fg in enumerate([1, 0]):
    row = next(r for r in trajectory.itertuples() if r.fg == fg)
    ax = fig.add_axes([0.075+i*0.48, 0.24, 0.38, 0.48])
    draw_group_history(ax, row)
    ax.set_title(f'{GROUP[fg]}\nn={jumlah(row.n)}', fontsize=12, pad=14)
    if i==1:
        ax.set_ylabel('')
save_group_plot(fig, '24_lintasan_ip_prediksi_panel_kelompok')
''')
code(r'''
assert len(group_plot_names) == 2
for name in group_plot_names:
    assert (GROUP_OUT / 'png' / f'{name}.png').is_file()
    assert (GROUP_OUT / 'svg' / f'{name}.svg').is_file()
    assert (SVG_OUT / f'{name}.svg').is_file()
assert 'ID_Mahasiswa' not in export_trajectory.columns
with ZipFile(OUT / 'Aset_Infografis_CDW2026.zip', 'w', compression=ZIP_DEFLATED) as archive:
    for file in sorted(OUT.rglob('*')):
        if file.is_file() and file.suffix.lower() in {'.png', '.svg', '.pdf', '.csv', '.json'}:
            archive.write(file, arcname=file.relative_to(OUT))
print('Dua alternatif lintasan kelompok tersimpan; prediksi hanya semester 4.')
print('SVG:', SVG_OUT)
''')

nb.cells = old_cells + new
nb.metadata['cdw']['group_prediction_plot'] = 'IP semester 1–3 aktual dan rerata prediksi IP4 pada kohort uji tetap; tanpa band interval individu'
nbformat.validate(nb)
nbformat.write(nb, target)
print(f'Tambahan {len(new)} sel; total {len(nb.cells)}. Sel sebelumnya dipertahankan.')
