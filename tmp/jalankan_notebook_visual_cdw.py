from pathlib import Path
import os
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
os.environ['JUPYTER_PATH'] = str(root / 'tmp' / 'jupyter')
os.environ['JUPYTER_RUNTIME_DIR'] = str(root / 'tmp' / 'jupyter_runtime')
os.environ['IPYTHONDIR'] = str(root / 'tmp' / 'ipython')
os.environ['MPLCONFIGDIR'] = str(root / 'tmp' / 'mplconfig')
target = root / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb'
nb = nbformat.read(target, as_version=4)

def progress(cell, cell_index, **kwargs):
    print(f'Sel {cell_index + 1}/{len(nb.cells)}: {cell.cell_type}', flush=True)

client = NotebookClient(nb, timeout=240, kernel_name='cdw_visual',
                        resources={'metadata': {'path': str(root)}},
                        on_cell_start=progress)
try:
    client.execute()
finally:
    nbformat.write(nb, target)
errors = [output for cell in nb.cells if cell.cell_type == 'code'
          for output in cell.get('outputs', []) if output.output_type == 'error']
assert not errors, errors
nbformat.validate(nb)
print('Selesai; notebook tersimpan dengan output, tanpa error.', flush=True)
