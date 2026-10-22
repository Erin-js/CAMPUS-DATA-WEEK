from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import runpy
import json
import ast
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import nbformat
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader
from zipfile import ZipFile

root = Path(__file__).resolve().parents[1]
out = root / '04_Visualisasi' / 'output_visualisasi_cdw'
nb = nbformat.read(root / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb', as_version=4)
nbformat.validate(nb)
code_cells = [c for c in nb.cells if c.cell_type == 'code']
assert all(c.execution_count is not None for c in code_cells)
assert not [o for c in code_cells for o in c.outputs if o.output_type == 'error']
for cell in code_cells:
    ast.parse(cell.source)
    assert not [line for line in cell.source.splitlines() if line.lstrip().startswith('#')]

capture = StringIO()
with redirect_stdout(capture):
    runpy.run_path(str(root / 'tmp' / 'verifikasi_naskah_cdw.py'))
expected = json.loads(capture.getvalue())
results = pd.read_csv(out / 'tabel' / 'koefisien_semua_model.csv')
mapping = [('original_ols', 'OLS notebook', 'beta'),
           ('duration_ols', 'OLS + lama studi', 'beta'),
           ('original_logistic', 'Logistik notebook', 'or'),
           ('duration_logistic', 'Logistik + lama studi', 'or'),
           ('baseline_ips4', 'IP semester 4 + baseline', 'beta')]
for key, label, stat in mapping:
    for term in expected[key]['terms']:
        row = results.loc[results.model.eq(label) & results.term.eq(term['term'])].iloc[0]
        assert np.allclose([row.estimate, row.low, row.high],
                           [term[stat], *term['ci95']], atol=1e-7), (key, term['term'])

names = sorted((out / 'png').glob('*.png'))
assert len(names) == 14
for file in names:
    image = Image.open(file)
    image.verify()
    assert min(Image.open(file).size) > 1000
    alpha = Image.open(out / 'png_transparan' / file.name).getchannel('A')
    assert alpha.getextrema()[0] == 0
    svg = ET.parse(out / 'svg' / (file.stem+'.svg'))
    assert svg.findall('.//{http://www.w3.org/2000/svg}text')
    assert len(PdfReader(out / 'pdf' / (file.stem+'.pdf')).pages) == 1
assert len(PdfReader(out / 'Katalog_Visual_CDW2026.pdf').pages) == 14
with ZipFile(out / 'Aset_Infografis_CDW2026.zip') as archive:
    assert archive.testzip() is None
    assert len([p for p in archive.namelist() if p.startswith('svg/')]) == 14
for file in (out / 'tabel').glob('*.csv'):
    assert 'ID_Mahasiswa' not in pd.read_csv(file).columns

for part, group in enumerate([names[:7], names[7:]]):
    sheet = Image.new('RGB', (1600, 4*430), '#f3f3f3')
    draw = ImageDraw.Draw(sheet)
    for i, file in enumerate(group):
        x, y = (i % 2)*800, (i // 2)*430
        thumb = ImageOps.contain(Image.open(file).convert('RGB'), (780, 400))
        sheet.paste(thumb, (x+(800-thumb.width)//2, y+25))
        draw.text((x+15, y+7), file.stem, fill='#233044')
    sheet.save(root / 'tmp' / f'qa_contact_{part+1}.png')

report = {'cells': len(nb.cells), 'executed_code_cells': len(code_cells),
          'errors': 0, 'visuals': len(names), 'model_comparison': 'All 5 models agree within 1e-7',
          'zip': 'valid', 'pdf_pages': 14, 'svg_text': 'editable',
          'exported_csvs': len(list((out/'tabel').glob('*.csv')))}
print(json.dumps(report, ensure_ascii=False, indent=2))
