from pathlib import Path
import ast
import json
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import nbformat
import numpy as np
import pandas as pd
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
out = root / '04_Visualisasi' / 'output_visualisasi_cdw' / 'analisis_lanjutan'
nb = nbformat.read(root / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb', as_version=4)
nbformat.validate(nb)
codes = [c for c in nb.cells if c.cell_type == 'code']
assert all(c.execution_count is not None for c in codes)
assert not [o for c in codes for o in c.outputs if o.output_type == 'error']
assert not any('belum menjadi analisis terverifikasi' in c.source for c in nb.cells)
for cell in codes:
    ast.parse(cell.source)
    assert not any(line.lstrip().startswith('#') for line in cell.source.splitlines())
names = sorted((out / 'png').glob('*.png'))
assert len(names) == 9
for path in names:
    Image.open(path).verify()
    assert min(Image.open(path).size) > 1000
    svg = ET.parse(out / 'svg' / f'{path.stem}.svg')
    assert svg.findall('.//{http://www.w3.org/2000/svg}text')
    assert not svg.findall('.//{http://www.w3.org/2000/svg}image')
    assert (root / '04_Visualisasi' / 'svg_plot_cdw2026' / f'{path.stem}.svg').is_file()
    assert len(PdfReader(out / 'pdf' / f'{path.stem}.pdf').pages) == 1
assert len(PdfReader(out / 'Katalog_Analisis_Lanjutan_CDW2026.pdf').pages) == 9
for path in (out / 'tabel').glob('*.csv'):
    assert 'ID_Mahasiswa' not in pd.read_csv(path).columns
with ZipFile(root / '04_Visualisasi' / 'output_visualisasi_cdw' / 'Aset_Infografis_CDW2026.zip') as archive:
    assert archive.testzip() is None
    assert len([p for p in archive.namelist() if p.startswith('analisis_lanjutan/svg/')]) == 9
results = json.loads((out / 'Ringkasan_Analisis_Lanjutan.json').read_text(encoding='utf-8'))
profiles = pd.read_csv(out / 'tabel' / 'profil_cluster.csv')
assert profiles.n.sum() == 5000
perf = pd.read_csv(out / 'tabel' / 'kinerja_prediksi_holdout.csv')
assert perf.n_test.eq(1213).all()
assert perf.iloc[-1].mae < perf.iloc[0].mae
assert np.isclose(perf.iloc[0].mae-perf.iloc[-1].mae, results['forecast']['mae_improvement_vs_ip3'])
audit = pd.read_csv(out / 'tabel' / 'audit_prediksi_per_kelompok.csv')
for factor, frame in audit.groupby('factor'):
    assert frame.n.sum() == 1213
    assert np.isclose(np.average(frame.mae, weights=frame.n), perf.iloc[-1].mae)
    assert np.isclose(np.average(frame.coverage90, weights=frame.n), results['forecast']['coverage90'])
profile_raw = pd.read_csv(root / '02_Analisis' / 'data' / '1_profil_mahasiswa_umum.csv', sep=';')
history_raw = pd.read_csv(root / '02_Analisis' / 'data' / '5_riwayat_ipk_semester.csv', sep=';')
panel = history_raw.pivot(index='ID_Mahasiswa', columns='Semester_Ke', values='IP_Semester')[[1, 2, 3, 4]].dropna()
panel = panel.merge(profile_raw[['ID_Mahasiswa', 'Angkatan']], left_index=True, right_on='ID_Mahasiswa', validate='one_to_one')
train = panel.loc[panel.Angkatan.le(2022)]
holdout = panel.loc[panel.Angkatan.eq(2024)]
calibration = panel.loc[panel.Angkatan.eq(2023)]
matrix = train[[1, 2, 3]].to_numpy()
center, scale = matrix.mean(axis=0), matrix.std(axis=0)
scaled = (matrix-center)/scale
target_center = train[4].mean()
coef = np.linalg.solve(scaled.T@scaled+0.01*np.eye(3), scaled.T@(train[4].to_numpy()-target_center))
pred = np.clip(((holdout[[1, 2, 3]].to_numpy()-center)/scale)@coef+target_center, 0, 4)
independent_mae = np.abs(holdout[4].to_numpy()-pred).mean()
assert np.isclose(independent_mae, perf.iloc[-1].mae, atol=1e-10)
pred_cal = np.clip(((calibration[[1, 2, 3]].to_numpy()-center)/scale)@coef+target_center, 0, 4)
residuals = np.sort(np.abs(calibration[4].to_numpy()-pred_cal))
qhat = residuals[int(np.ceil((len(residuals)+1)*0.90))-1]
assert np.isclose(qhat, results['forecast']['qhat'], atol=1e-10)
coverage = ((holdout[4].to_numpy() >= np.clip(pred-qhat, 0, 4)) & (holdout[4].to_numpy() <= np.clip(pred+qhat, 0, 4))).mean()
assert np.isclose(coverage, results['forecast']['coverage90'])
family = pd.read_csv(root / '02_Analisis' / 'data' / '3_generasi_pertama_kuliah.csv', sep=';')
economy = pd.read_csv(root / '02_Analisis' / 'data' / '4_status_sosial_ekonomi.csv', sep=';')
financial = family.loc[family.Kendala_Utama.eq('Finansial')].merge(economy, on='ID_Mahasiswa', validate='one_to_one')
assert len(financial) == 1648
assert np.isclose(financial.Status_Generasi_Pertama.eq('Ya').mean(), profiles.loc[profiles.cluster.eq('C2'), 'generasi_pertama'].iloc[0])
assert np.isclose(financial.Kategori_Ekonomi.eq('Rendah').mean(), profiles.loc[profiles.cluster.eq('C2'), 'ekonomi_rendah'].iloc[0])
for part, group in enumerate([names[:4], names[4:8], names[8:]]):
    sheet = Image.new('RGB', (2000, 1200), '#f3f3f3')
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(group):
        x, y = (i % 2)*1000, (i // 2)*600
        thumb = ImageOps.contain(Image.open(path).convert('RGB'), (970, 565))
        sheet.paste(thumb, (x+(1000-thumb.width)//2, y+30))
        draw.text((x+15, y+7), path.stem, fill='#233044')
    sheet.save(root / 'tmp' / f'qa_advanced_{part+1}.png')
print(json.dumps({'notebook_cells': len(nb.cells), 'executed_code_cells': len(codes),
                  'errors': 0, 'new_figures': len(names), 'editable_native_svgs': 9,
                  'advanced_catalog_pages': 9, 'tables_without_ids': len(list((out/'tabel').glob('*.csv'))),
                  'cluster_profiles_total': int(profiles.n.sum()), 'test_students': 1213,
                  'independent_ridge_and_coverage': 'agree within 1e-10',
                  'zip': 'valid'}, indent=2))
