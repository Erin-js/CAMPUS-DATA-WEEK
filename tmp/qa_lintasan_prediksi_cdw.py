from pathlib import Path
import ast
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import nbformat
import numpy as np
import pandas as pd
from PIL import Image

root = Path(__file__).resolve().parents[1]
nb = nbformat.read(root / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb', as_version=4)
nbformat.validate(nb)
codes = [c for c in nb.cells if c.cell_type == 'code']
assert all(c.execution_count is not None for c in codes)
assert not [o for c in codes for o in c.outputs if o.output_type == 'error']
for cell in codes:
    ast.parse(cell.source)
    assert not any(line.lstrip().startswith('#') for line in cell.source.splitlines())
out = root / '04_Visualisasi' / 'output_visualisasi_cdw' / 'prediksi_kelompok'
table = pd.read_csv(out / 'tabel' / 'rerata_ip_dan_prediksi_kelompok.csv')
assert table.n.sum() == 1213
assert table.n.tolist() == [765, 448]
assert 'ID_Mahasiswa' not in table.columns
profile = pd.read_csv(root / '02_Analisis' / 'data' / '1_profil_mahasiswa_umum.csv', sep=';')
family = pd.read_csv(root / '02_Analisis' / 'data' / '3_generasi_pertama_kuliah.csv', sep=';')
history = pd.read_csv(root / '02_Analisis' / 'data' / '5_riwayat_ipk_semester.csv', sep=';')
panel = history.pivot(index='ID_Mahasiswa', columns='Semester_Ke', values='IP_Semester')[[1, 2, 3, 4]].dropna()
panel = panel.merge(profile[['ID_Mahasiswa', 'Angkatan']], left_index=True, right_on='ID_Mahasiswa', validate='one_to_one')
panel = panel.merge(family[['ID_Mahasiswa', 'Status_Generasi_Pertama']], on='ID_Mahasiswa', validate='one_to_one')
train = panel.loc[panel.Angkatan.le(2022)]
test = panel.loc[panel.Angkatan.eq(2024)].copy()
matrix = train[[1, 2, 3]].to_numpy()
center, scale = matrix.mean(axis=0), matrix.std(axis=0)
scaled = (matrix-center)/scale
target_center = train[4].mean()
coef = np.linalg.solve(scaled.T@scaled+0.01*np.eye(3), scaled.T@(train[4].to_numpy()-target_center))
test['pred'] = np.clip(((test[[1, 2, 3]].to_numpy()-center)/scale)@coef+target_center, 0, 4)
for value, title in [('Tidak', 'Bukan generasi pertama'), ('Ya', 'Generasi pertama')]:
    source = test.loc[test.Status_Generasi_Pertama.eq(value)]
    row = table.loc[table.kelompok.eq(title)].iloc[0]
    assert len(source) == row.n
    assert np.allclose(source[[1, 2, 3]].mean().to_numpy(), row[['ip1', 'ip2', 'ip3']].to_numpy(dtype=float), atol=1e-10)
    assert np.isclose(source.pred.mean(), row.pred_ip4, atol=1e-10)
    assert np.isclose(source[4].mean(), row.actual_ip4, atol=1e-10)
for name in ['23_lintasan_ip_prediksi_dua_kelompok', '24_lintasan_ip_prediksi_panel_kelompok']:
    Image.open(out / 'png' / f'{name}.png').verify()
    svg = ET.parse(out / 'svg' / f'{name}.svg')
    assert svg.findall('.//{http://www.w3.org/2000/svg}text')
    assert not svg.findall('.//{http://www.w3.org/2000/svg}image')
    paths = svg.findall('.//{http://www.w3.org/2000/svg}path')
    assert any('stroke-dasharray' in p.attrib.get('style', '') for p in paths)
    assert (root / '04_Visualisasi' / 'svg_plot_cdw2026' / f'{name}.svg').is_file()
with ZipFile(root / '04_Visualisasi' / 'output_visualisasi_cdw' / 'Aset_Infografis_CDW2026.zip') as archive:
    assert archive.testzip() is None
    assert len([p for p in archive.namelist() if p.startswith('prediksi_kelompok/svg/')]) == 2
print('Notebook valid; seluruh sel kode selesai tanpa error. Dua grafik SVG native, garis prediksi putus-putus, ZIP valid.')
print('Rerata dan prediksi cocok dengan penghitungan independen hingga 1e-10.')
print(table.round(4).to_string(index=False))
