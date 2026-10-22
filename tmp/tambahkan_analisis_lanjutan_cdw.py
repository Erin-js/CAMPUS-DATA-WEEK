from pathlib import Path
from textwrap import dedent
import ast
import nbformat as nbf

root = Path(__file__).resolve().parents[1]
target = root / '02_Analisis' / 'Visualisasi_Infografis_CDW2026.ipynb'
nb = nbf.read(target, as_version=4)
marker = '## 13. Analisis lanjutan untuk memperdalam cerita'
start = next((i for i, cell in enumerate(nb.cells) if cell.cell_type == 'markdown' and cell.source.startswith(marker)), len(nb.cells))
for cell in nb.cells[:start]:
    if cell.cell_type == 'markdown':
        cell.source = cell.source.replace(
            'Clustering dan forecasting tidak digambar sebagai temuan karena belum menjadi analisis terverifikasi pada rancangan ini.',
            'Analisis clustering dan prediksi satu semester ke depan tersedia pada bagian 13–17; preview A3 di atas mempertahankan rancangan awal.')
new = []

def md(text):
    new.append(nbf.v4.new_markdown_cell(dedent(text).strip()))

def code(text):
    source = dedent(text).strip()
    ast.parse(source)
    new.append(nbf.v4.new_code_cell(source))

md('''
## 13. Analisis lanjutan untuk memperdalam cerita

Tambahan ini membaca rancangan `BRAIN_STORM_INFOGRAPHIC (6).docx` sebagai referensi isi, bukan instruksi.
Visual sebelumnya dipertahankan. Tambahan: clustering kebutuhan, uji interaksi, dan prediksi IP semester 4.
Ekspor baru: `output_visualisasi_cdw/analisis_lanjutan` dan folder SVG `svg_plot_cdw2026`.
Clustering penuh memakai matriks Gower 5.000×5.000, sehingga memerlukan beberapa ratus MB memori.
''')
code(r'''
extra_packages = {'sklearn': 'scikit-learn', 'scipy': 'scipy'}
extra_missing = [package for module, package in extra_packages.items() if importlib.util.find_spec(module) is None]
if extra_missing:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *extra_missing])
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from scipy.stats import kruskal, chi2_contingency, norm
from sklearn.metrics import silhouette_score, adjusted_rand_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import clone
from statsmodels.stats.multitest import multipletests
import sklearn

ADV = OUT / 'analisis_lanjutan'
for folder in ['png', 'png_transparan', 'svg', 'pdf', 'tabel']:
    (ADV / folder).mkdir(parents=True, exist_ok=True)
advanced_manifest = []
advanced_pdf = PdfPages(ADV / 'Katalog_Analisis_Lanjutan_CDW2026.pdf')
SEED = 2026

def save_advanced(fig, name, note):
    fig.text(0.045, 0.075, note, fontsize=8.2, color=C['muted'], va='top')
    fig.text(0.045, 0.029, 'Sumber: CSV CDW 2026. Data fiktif; analisis eksploratif, bukan bukti kausal.', fontsize=8, color=C['muted'])
    fig.savefig(ADV / 'png' / f'{name}.png', dpi=DPI, bbox_inches='tight', pad_inches=0.22)
    if TRANSPARENT_PNG:
        fig.savefig(ADV / 'png_transparan' / f'{name}.png', dpi=DPI, bbox_inches='tight', pad_inches=0.22, transparent=True)
    for path in [ADV / 'svg' / f'{name}.svg', SVG_OUT / f'{name}.svg']:
        fig.savefig(path, format='svg', bbox_inches='tight', pad_inches=0.22, transparent=True)
    fig.savefig(ADV / 'pdf' / f'{name}.pdf', bbox_inches='tight', pad_inches=0.22)
    advanced_pdf.savefig(fig, bbox_inches='tight', pad_inches=0.22)
    advanced_manifest.append({'nama': name, 'catatan': note})
    if SHOW_FIGURES:
        display(fig)
    plt.close(fig)

def export_table(frame, name):
    assert 'ID_Mahasiswa' not in frame.columns
    frame.to_csv(ADV / 'tabel' / f'{name}.csv', index=False, encoding='utf-8-sig')

print('Analisis lanjutan siap.')
''')
md('''
## 14. Clustering profil kebutuhan dengan jarak Gower

Fitur awal: ekonomi ordinal, bekerja, beasiswa, dukungan keluarga, tanggungan, dan kendala utama; bobot sama per fitur.
UKT tidak ikut agar ekonomi tidak dihitung berulang. IPK, prestasi, status akademik, dan generasi pertama tidak membentuk cluster.
Generasi pertama dan outcome baru diprofilkan setelah cluster terbentuk, sehingga perbedaannya tidak dibuat otomatis oleh input.

Model awal memisahkan status beasiswa secara sempurna. Karena beasiswa adalah dukungan yang diterima, bukan kebutuhan itu sendiri,
analisis kebutuhan utama didefinisikan ulang tanpa beasiswa. Ini perubahan spesifikasi eksploratif setelah diagnostik,
bukan konfirmasi independen. Status beasiswa tetap ditampilkan sebagai profil eksternal. Validasi kedua spesifikasi disimpan.

Metode: hierarchical average linkage pada jarak Gower. Pilih k=2–6 berdasarkan silhouette, minimal 5% anggota,
dan median ARI pada empat subsampel 70%. ARI ≥0,70 adalah ambang kerja eksploratif, bukan standar universal.
Silhouette <0,25 diberi peringatan pemisahan lemah. Label C1, C2, dst. tidak berarti tingkat risiko.
''')
code(r'''
needs = d[['Kategori_Ekonomi', 'work', 'sch', 'Tingkat_Dukungan_Keluarga',
           'Jumlah_Tanggungan_Keluarga', 'Kendala_Utama']].copy()
assert not needs.isna().any().any(), 'Fitur clustering kosong; perlu keputusan penanganan missing terlebih dahulu.'
num = pd.DataFrame({
    'ekonomi': needs.Kategori_Ekonomi.map({'Rendah': 0, 'Menengah': 0.5, 'Tinggi': 1}),
    'bekerja': needs.work.astype(float), 'beasiswa': needs.sch.astype(float),
    'dukungan': (needs.Tingkat_Dukungan_Keluarga-1)/4,
    'tanggungan': (needs.Jumlah_Tanggungan_Keluarga-1)/8
})
assert not num.isna().any().any()
n_cluster = len(needs)
distance = np.zeros((n_cluster, n_cluster), dtype=np.float32)
for col in num:
    values = num[col].to_numpy(dtype=np.float32)
    distance += np.abs(values[:, None]-values[None, :])
constraint = pd.Categorical(needs.Kendala_Utama).codes
distance += (constraint[:, None] != constraint[None, :]).astype(np.float32)
distance /= 6
np.fill_diagonal(distance, 0)
ks = list(range(2, 7))
rng = np.random.default_rng(SEED)
quality_ids = np.sort(rng.choice(n_cluster, size=min(1500, n_cluster), replace=False))

def evaluate_clusters(matrix):
    tree = linkage(squareform(matrix, checks=False), method='average')
    assignments = {k: fcluster(tree, k, criterion='maxclust') for k in ks}
    sample_distance = matrix[np.ix_(quality_ids, quality_ids)]
    stability = {k: [] for k in ks}
    for repeat in range(4):
        ids = np.sort(np.random.default_rng(SEED+repeat).choice(n_cluster, size=int(0.70*n_cluster), replace=False))
        sub_tree = linkage(squareform(matrix[np.ix_(ids, ids)], checks=False), method='average')
        for k in ks:
            sub_labels = fcluster(sub_tree, k, criterion='maxclust')
            stability[k].append(adjusted_rand_score(assignments[k][ids], sub_labels))
    scores = pd.DataFrame([
        {'k': k, 'silhouette_gower': silhouette_score(sample_distance, assignments[k][quality_ids], metric='precomputed'),
         'ari_median': np.median(stability[k]), 'ari_min': np.min(stability[k]),
         'cluster_terkecil': int(pd.Series(assignments[k]).value_counts().min()),
         'proporsi_terkecil': float(pd.Series(assignments[k]).value_counts(normalize=True).min())}
        for k in ks])
    scores['lolos_ukuran_stabilitas'] = scores.proporsi_terkecil.ge(0.05) & scores.ari_median.ge(0.70)
    return scores, assignments

quality_with_sch, labels_with_sch = evaluate_clusters(distance)
initial_k = int(quality_with_sch.sort_values('silhouette_gower', ascending=False).iloc[0].k)
initial_sch_profile = pd.crosstab(labels_with_sch[initial_k], needs.sch, normalize='index')
export_table(quality_with_sch, 'validasi_cluster_awal_dengan_beasiswa')
display(quality_with_sch, initial_sch_profile)
sch_dist = np.abs(num.beasiswa.to_numpy(np.float32)[:, None]-num.beasiswa.to_numpy(np.float32)[None, :])
without_sch = np.maximum((distance*6-sch_dist)/5, 0)
np.fill_diagonal(without_sch, 0)
quality, labels_by_k = evaluate_clusters(without_sch)
eligible = quality.loc[quality.lolos_ukuran_stabilitas]
cluster_gate = not eligible.empty
pool = eligible if cluster_gate else quality
chosen_k = int(pool.sort_values(['silhouette_gower', 'ari_median'], ascending=False).iloc[0].k)
chosen_quality = quality.set_index('k').loc[chosen_k]
labels = labels_by_k[chosen_k]
cluster_sensitivity = adjusted_rand_score(labels, labels_with_sch[chosen_k])

del without_sch, sch_dist, distance
dc = d.copy()
dc['cluster_raw'] = labels
order = dc.groupby('cluster_raw').work.mean().sort_values(ascending=False).index
label_map = {raw: f'C{i+1}' for i, raw in enumerate(order)}
dc['cluster'] = dc.cluster_raw.map(label_map)
cluster_profile = dc.groupby('cluster', observed=True).agg(
    n=('ID_Mahasiswa', 'size'), ekonomi_rendah=('Kategori_Ekonomi', lambda s: s.eq('Rendah').mean()),
    bekerja=('work', 'mean'), beasiswa=('sch', 'mean'), dukungan=('Tingkat_Dukungan_Keluarga', 'mean'),
    tanggungan=('Jumlah_Tanggungan_Keluarga', 'mean'), finansial=('Kendala_Utama', lambda s: s.eq('Finansial').mean()),
    generasi_pertama=('fg', 'mean'), ipk=('IPK_Mahasiswa', 'mean'), achievement=('achievement', 'mean'),
    interrupted=('interrupted', 'mean')).reset_index()
export_table(quality, 'validasi_cluster')
export_table(cluster_profile, 'profil_cluster')
display(quality, cluster_profile)
print(f'k terpilih={chosen_k}; silhouette={chosen_quality.silhouette_gower:.3f}; ARI median={chosen_quality.ari_median:.3f}')
print(f'Sensitivitas menambahkan beasiswa: ARI={cluster_sensitivity:.3f}')
if not cluster_gate:
    print('PERINGATAN: tidak ada k memenuhi ukuran/stabilitas; profil hanya eksplorasi, tidak layak headline final.')
if chosen_quality.silhouette_gower < 0.25:
    print('PERINGATAN: pemisahan cluster lemah; jangan mengklaim tipe mahasiswa yang tegas.')
''')
code(r'''
fig, _ = canvas('Apakah profil kebutuhan membentuk kelompok yang konsisten?',
                'Lima fitur kebutuhan, tanpa beasiswa/IPK/prestasi; empat pengulangan subsampel 70%', size=(12, 6.1))
fig.axes[0].remove()
for i, (col, title, color) in enumerate([
    ('silhouette_gower', 'Pemisahan: silhouette Gower', C['nonfg']),
    ('ari_median', 'Kestabilan: median ARI', C['fg'])]):
    ax = fig.add_axes([0.10+i*0.48, 0.23, 0.35, 0.49])
    ax.plot(quality.k, quality[col], 'o-', color=color, lw=2)
    ax.axvline(chosen_k, color=C['muted'], ls='--')
    for row in quality.itertuples():
        ax.annotate(angka(getattr(row, col), 3), (row.k, getattr(row, col)), xytext=(0, 9), textcoords='offset points', ha='center', fontsize=9)
    ax.set_xticks(ks)
    ax.set_xlabel('Jumlah cluster')
    ax.set_title(title, fontsize=11)
    ax.set_ylim(min(0, quality[col].min()-0.05), max(quality[col].max()+0.14, 0.5))
    ax.grid(axis='y', color=C['line'], alpha=0.4)
save_advanced(fig, '14_validasi_clustering_gower',
              f'k={chosen_k}; ukuran/stabilitas lolos={cluster_gate}; ARI menambah beasiswa={angka(cluster_sensitivity, 3)}. Ambang kerja bukan standar universal.')
''')
code(r'''
profile_cols = ['ekonomi_rendah', 'bekerja', 'beasiswa', 'dukungan', 'tanggungan', 'finansial', 'generasi_pertama']
color_values = cluster_profile[profile_cols].to_numpy().copy()
color_values[:, 3] = (color_values[:, 3]-1)/4
color_values[:, 4] = (color_values[:, 4]-1)/8
fig, ax = canvas('Kebutuhan mahasiswa tidak berhenti pada kategori ekonomi',
                 f'{chosen_k} profil eksploratif; generasi pertama diprofilkan setelah clustering, bukan sebagai input', size=(13.8, max(5.8, chosen_k*0.6+3.4)))
fig.subplots_adjust(left=0.12, right=0.93, bottom=0.26)
ax.pcolormesh(np.arange(8)-0.5, np.arange(chosen_k+1)-0.5, color_values, cmap='YlOrBr', vmin=0, vmax=1, shading='flat')
ax.set_xlim(-0.5, 6.5)
ax.set_ylim(chosen_k-0.5, -0.5)
labels_x = ['Ekonomi\nrendah', 'Bekerja', 'Beasiswa*', 'Dukungan\n(1–5)', 'Tanggungan\n(orang)', 'Kendala\nfinansial', 'Generasi\npertama*']
ax.set_xticks(range(7), labels_x, fontsize=10)
ax.set_yticks(range(chosen_k), [f'{r.cluster}\nn={jumlah(r.n)}' for r in cluster_profile.itertuples()], fontsize=10)
ax.tick_params(length=0)
for i in range(chosen_k):
    for j in range(7):
        val = cluster_profile.iloc[i][profile_cols[j]]
        text = angka(val, 1) if j in [3, 4] else persen(val)
        ax.text(j, i, text, ha='center', va='center', color='white' if color_values[i, j]>0.70 else C['ink'], fontsize=12, weight='bold')
save_advanced(fig, '15_heatmap_profil_kebutuhan',
              '*Beasiswa/generasi pertama bukan fitur cluster. Warna: 0–1 per kolom; dukungan/tanggungan tetap satuan asli.')
''')
md('''
### Membandingkan capaian setelah cluster terbentuk
IPK, catatan kegiatan, dan status akademik tidak membentuk cluster. Perbandingan tetap deskriptif, bukan efek cluster.
IPK: CI rata-rata normal; persentase: CI Wilson. Uji tiga outcome dikoreksi Holm, dengan ukuran efek.
''')
code(r'''
cluster_outcomes = []
for label, frame in dc.groupby('cluster', observed=True):
    n = len(frame)
    mean = frame.IPK_Mahasiswa.mean()
    se = frame.IPK_Mahasiswa.std(ddof=1)/np.sqrt(n)
    cluster_outcomes.append({'cluster': label, 'outcome': 'IPK terakhir', 'n': n,
                             'estimate': mean, 'low': mean-1.96*se, 'high': mean+1.96*se})
    for col, title in [('achievement', 'Catatan kegiatan'), ('interrupted', 'Cuti/nonaktif')]:
        p = frame[col].mean()
        center = (p+1.96**2/(2*n))/(1+1.96**2/n)
        half = 1.96*np.sqrt(p*(1-p)/n+1.96**2/(4*n*n))/(1+1.96**2/n)
        cluster_outcomes.append({'cluster': label, 'outcome': title, 'n': n,
                                 'estimate': p, 'low': center-half, 'high': center+half})
cluster_outcomes = pd.DataFrame(cluster_outcomes)
h, p = kruskal(*[f.IPK_Mahasiswa.to_numpy() for _, f in dc.groupby('cluster')])
cluster_tests = [{'outcome': 'IPK terakhir', 'uji': 'Kruskal–Wallis', 'stat': h, 'p': p,
                  'effect': max(0, (h-chosen_k+1)/(len(dc)-chosen_k)), 'effect_name': 'epsilon squared'}]
for col in ['achievement', 'interrupted']:
    table = pd.crosstab(dc.cluster, dc[col])
    chi, p, _, _ = chi2_contingency(table, correction=False)
    cluster_tests.append({'outcome': col, 'uji': 'Chi-square', 'stat': chi, 'p': p,
                          'effect': np.sqrt(chi/(len(dc)*min(table.shape[0]-1, table.shape[1]-1))), 'effect_name': 'Cramers V'})
cluster_tests = pd.DataFrame(cluster_tests)
cluster_tests['p_holm'] = multipletests(cluster_tests.p, method='holm')[1]
export_table(cluster_outcomes, 'capaian_cluster_ci95')
export_table(cluster_tests, 'uji_outcome_cluster')
display(cluster_tests)
fig, _ = canvas('Capaian dibandingkan setelah profil kebutuhan terbentuk',
                'Outcome tidak digunakan untuk clustering; whisker menunjukkan CI 95%', size=(13.5, 6.7))
fig.axes[0].remove()
for i, (outcome, ymax) in enumerate([('IPK terakhir', 4), ('Catatan kegiatan', 1), ('Cuti/nonaktif', 1)]):
    ax = fig.add_axes([0.065+i*0.32, 0.23, 0.26, 0.48])
    frame = cluster_outcomes.loc[cluster_outcomes.outcome.eq(outcome)].sort_values('cluster')
    ax.bar(frame.cluster, frame.estimate, color=[C['fg'], C['nonfg'], C['green'], C['risk'], '#917599', '#967455'][:chosen_k])
    ax.errorbar(frame.cluster, frame.estimate, yerr=[frame.estimate-frame.low, frame.high-frame.estimate], fmt='none', ecolor=C['ink'], capsize=4)
    for r in frame.itertuples():
        ax.text(r.cluster, r.high+0.04*ymax, angka(r.estimate, 2) if ymax==4 else persen(r.estimate), ha='center', fontsize=9.5)
    ax.set_ylim(0, ymax)
    ax.set_title(outcome, fontsize=12)
    if ymax==1:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: persen(x)))
    ax.grid(axis='y', color=C['line'], alpha=0.3)
    ax.set_axisbelow(True)
save_advanced(fig, '16_capaian_menurut_cluster',
              'Cluster bukan label risiko. Perbedaan belum disesuaikan lama studi/angkatan; status cuti/nonaktif bukan prediksi DO.')
''')
code(r'''
financial_label = cluster_profile.sort_values('finansial', ascending=False).iloc[0].cluster
financial = dc.loc[dc.cluster.eq(financial_label)].copy()
financial_composition = pd.DataFrame([
    {'aspek': 'Ekonomi', 'kategori': label, 'n': int(financial.Kategori_Ekonomi.eq(label).sum()),
     'proporsi': financial.Kategori_Ekonomi.eq(label).mean()} for label in ['Rendah', 'Menengah', 'Tinggi']
]+[
    {'aspek': 'Pendidikan orang tua', 'kategori': GROUP[value], 'n': int(financial.fg.eq(value).sum()),
     'proporsi': financial.fg.eq(value).mean()} for value in [1, 0]
])
export_table(financial_composition, 'komposisi_profil_finansial')
fig, ax = canvas('Kendala finansial tidak hanya muncul pada ekonomi rendah',
                 f'Profil {financial_label}: n={jumlah(len(financial))}; kendala utama finansial {persen(financial.Kendala_Utama.eq("Finansial").mean())}', size=(13, 6.2))
fig.subplots_adjust(left=0.23, right=0.96, bottom=0.31)
for i, aspect in enumerate(['Ekonomi', 'Pendidikan orang tua']):
    frame = financial_composition.loc[financial_composition.aspek.eq(aspect)]
    left = 0
    colors = [C['fg'], C['nonfg'], C['green']] if i==0 else [C['fg'], C['nonfg']]
    for j, row in enumerate(frame.itertuples()):
        ax.barh(1-i, row.proporsi, left=left, height=0.42, color=colors[j])
        title = row.kategori.replace('generasi pertama', 'generasi\npertama')
        ax.text(left+row.proporsi/2, 1-i, f'{title}\n{persen(row.proporsi)}', ha='center', va='center', color='white', fontsize=9.2)
        left += row.proporsi
ax.set_yticks([1, 0], ['Kategori ekonomi', 'Pendidikan\norang tua'], fontsize=10)
ax.set_xlim(0, 1)
ax.set_ylim(-0.6, 1.6)
ax.set_xticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
save_advanced(fig, '22_cluster_kendala_finansial',
              'Kategori ekonomi bukan satu-satunya penanda kebutuhan. Clustering eksploratif; kendala yang tercatat perlu dikonfirmasi kepada mahasiswa.')
''')
md('''
## 15. Uji interaksi generasi pertama dan bekerja

Model OLS dan logistik ditambah fg×work. Interaksi menguji apakah perbedaan yang terkait bekerja berbeda menurut generasi pertama.
Jika CI interaksi mencakup nol/OR satu, data belum mendukung klaim bahwa kedua kondisi saling memperbesar asosiasi.
Grafik memakai rata-rata prediksi pada distribusi kovariat yang sama di ekonomi rendah, bukan efek intervensi.
Dua uji interaksi dikoreksi Holm. Tidak ada interpretasi kausal atau difference-in-differences waktu.
''')
code(r'''
y_int, x_int = model_frame(d, 'IPK_Mahasiswa', 'duration')
x_int['fg_x_work'] = x_int.fg*x_int.work
fit_interaction = sm.OLS(y_int, x_int).fit(cov_type='HC3', use_t=False)
fit_interaction_logit = sm.GLM(d.loc[x_int.index, 'achievement'].astype(float), x_int,
                             family=sm.families.Binomial()).fit(cov_type='HC0')
assert fit_interaction_logit.converged
interaction_tests = pd.concat([
    coefficients(fit_interaction, 'Interaksi IPK').query("term == 'fg_x_work'"),
    coefficients(fit_interaction_logit, 'Interaksi logistik', True).query("term == 'fg_x_work'")], ignore_index=True)
interaction_tests['p_holm'] = multipletests(interaction_tests.p, method='holm')[1]
reference_x = x_int.loc[d.index[d.Kategori_Ekonomi.eq('Rendah')].intersection(x_int.index)].copy()
adjusted = []
for fg in [0, 1]:
    for work in [0, 1]:
        xx = reference_x.copy()
        xx['fg'], xx['work'], xx['fg_x_work'] = fg, work, fg*work
        gradient = xx.mean().to_numpy()
        estimate = float(gradient @ fit_interaction.params.to_numpy())
        se = np.sqrt(gradient @ fit_interaction.cov_params().to_numpy() @ gradient)
        probs = fit_interaction_logit.predict(xx).to_numpy()
        grad_prob = (xx.to_numpy()*(probs*(1-probs))[:, None]).mean(axis=0)
        se_prob = np.sqrt(grad_prob @ fit_interaction_logit.cov_params().to_numpy() @ grad_prob)
        adjusted.append({'fg': fg, 'work': work, 'ipk': estimate, 'ipk_low': estimate-1.96*se, 'ipk_high': estimate+1.96*se,
                         'kegiatan': probs.mean(), 'kegiatan_low': max(0, probs.mean()-1.96*se_prob),
                         'kegiatan_high': min(1, probs.mean()+1.96*se_prob), 'n_reference': len(reference_x)})
adjusted = pd.DataFrame(adjusted)
export_table(interaction_tests, 'uji_interaksi_fg_bekerja')
export_table(adjusted, 'prediksi_standar_ekonomi_rendah')
display(interaction_tests, adjusted)
fig, _ = canvas('Apakah pola bekerja berbeda menurut generasi pertama?',
                'Prediksi terstandar pada distribusi kovariat ekonomi rendah yang sama; CI 95%', size=(13, 6.7))
fig.axes[0].remove()
for i, (metric, title) in enumerate([('ipk', 'IPK terakhir terstandar'), ('kegiatan', 'Probabilitas catatan kegiatan terstandar')]):
    ax = fig.add_axes([0.10+i*0.46, 0.26, 0.36, 0.46])
    for fg in [0, 1]:
        frame = adjusted.loc[adjusted.fg.eq(fg)].sort_values('work')
        ax.errorbar(frame.work, frame[metric], yerr=[frame[metric]-frame[metric+'_low'], frame[metric+'_high']-frame[metric]],
                    marker='o', color=COLORS[fg], lw=2, capsize=5, label=GROUP[fg])
    ax.set_xticks([0, 1], ['Tidak bekerja', 'Bekerja'])
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim((2.4, 3.7) if metric=='ipk' else (0, 1))
    if metric=='kegiatan':
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: persen(x)))
    ax.set_title(title, fontsize=11)
    ax.grid(axis='y', alpha=0.3, color=C['line'])
    if i==0:
        ax.legend(loc='lower left', fontsize=8, frameon=False)
row = interaction_tests.iloc[0]
save_advanced(fig, '17_interaksi_bekerja_generasi_pertama',
              f'Interaksi OLS={angka(row.estimate, 3)} [{angka(row.low, 3)}; {angka(row.high, 3)}]; p Holm={angka(row.p_holm, 3)}. Asosiasi, bukan kausal.')
''')
md('''
## 16. Prediksi IP semester berikutnya tanpa kebocoran outcome

Target: IP semester 4 dari IP semester 1–3. Satu baris per mahasiswa; tidak memakai IPK terakhir, prestasi,
atau kondisi sosial-ekonomi saat ini sebagai fitur karena waktu pengukurannya tidak diketahui.
Angkatan dipakai untuk pembagian, bukan fitur. Generasi pertama/ekonomi hanya digunakan dalam audit hasil.

Pemisahan: latih angkatan sebelum 2022; validasi 2022; kalibrasi 2023; uji 2024.
Tahun ini diturunkan otomatis dari empat angkatan terakhir dengan catatan semester 4.
Ridge dan Random Forest dipilih hanya berdasarkan MAE validasi; kemudian dilatih ulang pada latih+validasi.
Test tidak ikut memilih model. Bandingkan dengan IP semester 3 dan rerata IP semester 1–3.

Ini pengujian retrospektif satu semester ke depan pada angkatan berbeda, bukan forecasting jumlah mahasiswa/DO.
Angkatan bukan tanggal pengamatan semester; data fiktif belum membuktikan kinerja operasional pada tahun mendatang.
''')
code(r'''
forecast = d[['ID_Mahasiswa', 'fg', 'Kategori_Ekonomi', 'Angkatan']].merge(
    ips[[1, 2, 3, 4]].rename(columns={1: 'ip1', 2: 'ip2', 3: 'ip3', 4: 'target'}),
    left_on='ID_Mahasiswa', right_index=True, validate='one_to_one').dropna(subset=['ip1', 'ip2', 'ip3', 'target']).copy()
years = sorted(forecast.Angkatan.unique())
assert len(years)>=4, 'Butuh minimal empat angkatan lengkap untuk pemisahan ini.'
valid_year, calibration_year, test_year = years[-3:]
train_idx = forecast.Angkatan.lt(valid_year)
valid_idx = forecast.Angkatan.eq(valid_year)
cal_idx = forecast.Angkatan.eq(calibration_year)
test_idx = forecast.Angkatan.eq(test_year)
assert all(mask.sum()>=50 for mask in [train_idx, valid_idx, cal_idx, test_idx])
assert forecast.ID_Mahasiswa.is_unique
X = forecast[['ip1', 'ip2', 'ip3']]
y = forecast.target
candidates = {f'Ridge alpha={alpha}': make_pipeline(StandardScaler(), Ridge(alpha=alpha)) for alpha in [0.01, 0.1, 1, 10, 100]}
for depth in [3, 5, None]:
    candidates[f'Random Forest depth={depth}'] = RandomForestRegressor(
        n_estimators=200, max_depth=depth, min_samples_leaf=10, random_state=SEED, n_jobs=1)
selection = []
for name, estimator in candidates.items():
    estimator.fit(X.loc[train_idx], y.loc[train_idx])
    pred = np.clip(estimator.predict(X.loc[valid_idx]), 0, 4)
    selection.append({'model': name, 'mae_validasi': mean_absolute_error(y.loc[valid_idx], pred)})
selection = pd.DataFrame(selection).sort_values('mae_validasi')
chosen_model_name = selection.iloc[0].model
predictor = clone(candidates[chosen_model_name])
predictor.fit(X.loc[train_idx | valid_idx], y.loc[train_idx | valid_idx])
test = forecast.loc[test_idx].copy()
test['pred'] = np.clip(predictor.predict(X.loc[test_idx]), 0, 4)
test['baseline_ip3'] = test.ip3
test['baseline_mean'] = test[['ip1', 'ip2', 'ip3']].mean(axis=1)
pred_cal = np.clip(predictor.predict(X.loc[cal_idx]), 0, 4)
cal_residual = np.abs(y.loc[cal_idx].to_numpy()-pred_cal)
coverage_target = 0.90
quantile_rank = min(int(np.ceil((len(cal_residual)+1)*coverage_target)), len(cal_residual))
qhat = float(np.sort(cal_residual)[quantile_rank-1])
test['pi_low'] = np.clip(test.pred-qhat, 0, 4)
test['pi_high'] = np.clip(test.pred+qhat, 0, 4)
test['covered'] = test.target.between(test.pi_low, test.pi_high)
test['absolute_error'] = np.abs(test.target-test.pred)
performance = []
for title, col in [('IP semester 3', 'baseline_ip3'), ('Rerata IP semester 1–3', 'baseline_mean'), (chosen_model_name, 'pred')]:
    performance.append({'model': title, 'n_test': len(test), 'mae': mean_absolute_error(test.target, test[col]),
                        'rmse': np.sqrt(mean_squared_error(test.target, test[col])), 'r2': r2_score(test.target, test[col])})
performance = pd.DataFrame(performance)
paired = np.abs(test.target-test.baseline_ip3).to_numpy()-test.absolute_error.to_numpy()
boot_rng = np.random.default_rng(SEED)
boot_improvement = np.array([boot_rng.choice(paired, size=len(paired), replace=True).mean() for _ in range(1000)])
improvement_ci = np.quantile(boot_improvement, [0.025, 0.975])
split_info = pd.DataFrame([
    ['Latih', ', '.join(map(str, years[:-3])), int(train_idx.sum())],
    ['Validasi', str(valid_year), int(valid_idx.sum())], ['Kalibrasi', str(calibration_year), int(cal_idx.sum())],
    ['Uji', str(test_year), int(test_idx.sum())]], columns=['bagian', 'angkatan', 'n'])
export_table(selection, 'seleksi_model_validasi')
export_table(performance, 'kinerja_prediksi_holdout')
export_table(split_info, 'pemisahan_angkatan')
display(split_info, selection, performance)
print(f'Model terpilih: {chosen_model_name}; coverage uji={test.covered.mean():.3f}; q={qhat:.3f}')
print(f'Pengurangan MAE vs IP semester 3: {paired.mean():.4f}; CI bootstrap95% [{improvement_ci[0]:.4f}, {improvement_ci[1]:.4f}]')
''')
code(r'''
fig, ax = canvas('Seberapa baik IP semester berikutnya dapat diperkirakan?',
                 f'Uji angkatan {test_year}, n={jumlah(len(test))}; model dipilih pada validasi, bukan pada test', size=(12.3, 6.2))
fig.subplots_adjust(left=0.31, right=0.88)
for i, row in enumerate(performance.itertuples()):
    color = C['green'] if row.model==chosen_model_name else C['nonfg']
    ax.barh(2-i, row.mae, color=color, height=0.38)
    ax.text(row.mae+0.01, 2-i, angka(row.mae, 3)+' poin', va='center', fontsize=12)
ax.set_yticks([2, 1, 0], performance.model, fontsize=10)
ax.set_xlim(0, performance.mae.max()*1.35)
ax.set_ylim(-0.6, 2.65)
ax.set_xlabel('MAE: rata-rata kesalahan absolut; lebih kecil lebih baik')
ax.grid(axis='x', color=C['line'], alpha=0.3)
ax.set_axisbelow(True)
save_advanced(fig, '18_prediksi_ip_evaluasi_baseline',
              f'Pengurangan MAE vs IP3={angka(paired.mean(), 3)}; CI95% [{angka(improvement_ci[0], 3)}; {angka(improvement_ci[1], 3)}]. Bukan prediksi DO.')
''')
code(r'''
fig, ax = canvas('Prediksi diuji terhadap nilai yang benar-benar tercatat',
                 f'{chosen_model_name}; test angkatan {test_year}; setiap titik adalah mahasiswa berbeda', size=(10.3, 7))
ax.scatter(test.pred, test.target, s=16, alpha=0.22, color=C['nonfg'], edgecolors='none')
ax.plot([0, 4], [0, 4], color=C['risk'], ls='--', lw=1.5)
ax.set(xlim=(0, 4), ylim=(0, 4), xlabel='Prediksi IP semester 4', ylabel='IP semester 4 aktual')
ax.set_aspect('equal', adjustable='box')
save_advanced(fig, '19_prediksi_vs_aktual_ip4',
              f'MAE={angka(performance.iloc[-1].mae, 3)}; RMSE={angka(performance.iloc[-1].rmse, 3)}; R²={angka(performance.iloc[-1].r2, 3)}. Garis putus-putus: prediksi tepat.')
''')
md('''
### Ketidakpastian dan audit kelompok
Interval split-conformal memakai residual kalibrasi yang terpisah. Target nominal 90% tidak otomatis terjamin ketika angkatan berbeda;
laporkan coverage aktual pada test. Ukuran sampel, MAE, dan coverage diperiksa per generasi pertama serta kategori ekonomi.
Ini audit kesalahan model, bukan bukti model bebas bias. Sampel interval dipilih acak, bukan berdasarkan prediksi terbaik.
''')
code(r'''
forecast_audit = []
for factor in ['fg', 'Kategori_Ekonomi']:
    for label, frame in test.groupby(factor, observed=True):
        title = GROUP[int(label)] if factor=='fg' else str(label)
        forecast_audit.append({'factor': factor, 'group': title, 'n': len(frame),
                               'mae': frame.absolute_error.mean(), 'bias_pred_minus_actual': (frame.pred-frame.target).mean(),
                               'coverage90': frame.covered.mean(), 'mean_width': (frame.pi_high-frame.pi_low).mean()})
forecast_audit = pd.DataFrame(forecast_audit)
export_table(forecast_audit, 'audit_prediksi_per_kelompok')
display(forecast_audit)
example = test.sample(n=min(30, len(test)), random_state=SEED).sort_values('pred').reset_index(drop=True)
fig, ax = canvas('Prediksi perlu disertai rentang ketidakpastian',
                 f'30 mahasiswa test dipilih acak; target interval 90%; coverage uji aktual {persen(test.covered.mean())}', size=(12.5, 6.6))
ax.errorbar(example.index, example.pred, yerr=[example.pred-example.pi_low, example.pi_high-example.pred],
            fmt='o', color=C['nonfg'], alpha=0.7, ms=4, capsize=2, label='Prediksi dan interval')
ax.scatter(example.index, example.target, marker='x', s=35, color=C['risk'], label='Nilai aktual', zorder=4)
ax.set(xlabel='Urutan sampel acak (diurutkan berdasarkan prediksi)', ylabel='IP semester 4', ylim=(0, 4))
ax.legend(loc='lower right', fontsize=9, frameon=False)
save_advanced(fig, '20_interval_prediksi_ip4',
              f'Kalibrasi angkatan {calibration_year}; q={angka(qhat, 3)}. Pergeseran antarangkatan dapat mengubah coverage; bukan jaminan individual.')
''')
code(r'''
fig, _ = canvas('Apakah kesalahan prediksi merata antarkelompok?',
                f'Audit test angkatan {test_year}; fitur model hanya IP semester 1–3', size=(13, 6.5))
fig.axes[0].remove()
for i, factor in enumerate(['fg', 'Kategori_Ekonomi']):
    ax = fig.add_axes([0.085+i*0.47, 0.31, 0.36, 0.39])
    frame = forecast_audit.loc[forecast_audit.factor.eq(factor)].reset_index(drop=True)
    ax.bar(range(len(frame)), frame.mae, color=C['nonfg'] if i else [C['nonfg'], C['fg']])
    for j, row in frame.iterrows():
        ax.text(j, row.mae+0.01, f'{angka(row.mae, 3)}\nn={jumlah(row.n)}', ha='center', fontsize=9)
    names = [s.replace('generasi pertama', 'generasi\npertama') for s in frame.group]
    ax.set_xticks(range(len(frame)), names, fontsize=9)
    ax.set_ylim(0, forecast_audit.mae.max()*1.55)
    ax.set_ylabel('MAE (poin IP)')
    ax.set_title('Pendidikan orang tua' if factor=='fg' else 'Kategori ekonomi', fontsize=11)
    ax.grid(axis='y', alpha=0.3, color=C['line'])
    ax.set_axisbelow(True)
save_advanced(fig, '21_audit_prediksi_per_kelompok',
              'Perbedaan MAE bersifat deskriptif. Kategori ekonomi/generasi pertama adalah audit snapshot, bukan fitur historis model.')
''')
md('''
## 17. Hasil dan batas penggunaan

Clustering membantu membaca variasi kondisi, bukan menetapkan identitas/risiko mahasiswa.
Uji interaksi memeriksa klaim penguatan pola, bukan membuktikan penyebab. Prediksi IP hanya diuji retrospektif pada data simulasi.
PETA diletakkan setelah analisis, sebagai jembatan strategi menuju JEMBATAN, bukan hasil statistik.

Referensi metode:
- [SciPy average linkage](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html)
- [Silhouette](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)
- [Adjusted Rand index](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html)
- [Split-conformal dan exchangeability](https://arxiv.org/abs/2107.07511)
''')
code(r'''
advanced_pdf.close()
advanced_manifest_df = pd.DataFrame(advanced_manifest)
export_table(advanced_manifest_df, 'manifest_analisis_lanjutan')
assert len(advanced_manifest_df)==9
assert not advanced_manifest_df.nama.duplicated().any()
for name in advanced_manifest_df.nama:
    for folder, ext in [('png', 'png'), ('svg', 'svg'), ('pdf', 'pdf')]:
        file = ADV / folder / f'{name}.{ext}'
        assert file.is_file() and file.stat().st_size>1000
    assert (SVG_OUT / f'{name}.svg').is_file()
results_advanced = {
    'cluster': {'features': ['ekonomi', 'bekerja', 'dukungan', 'tanggungan', 'kendala'],
                'initial_with_scholarship_k': initial_k,
                'initial_with_scholarship_quality': quality_with_sch.to_dict('records'),
                'k': chosen_k, 'silhouette': float(chosen_quality.silhouette_gower),
                'ari_median': float(chosen_quality.ari_median), 'quality_gate': bool(cluster_gate),
                'ari_with_scholarship': float(cluster_sensitivity),
                'profiles': cluster_profile.to_dict('records'), 'tests': cluster_tests.to_dict('records')},
    'interaction': interaction_tests.to_dict('records'),
    'forecast': {'chosen_model': chosen_model_name, 'split': split_info.to_dict('records'),
                 'performance': performance.to_dict('records'), 'coverage90': float(test.covered.mean()),
                 'qhat': qhat, 'mae_improvement_vs_ip3': float(paired.mean()),
                 'improvement_ci95': improvement_ci.tolist(), 'group_audit': forecast_audit.to_dict('records')},
    'versions': {'sklearn': sklearn.__version__}, 'new_visuals': len(advanced_manifest)}
with (ADV / 'Ringkasan_Analisis_Lanjutan.json').open('w', encoding='utf-8') as file:
    json.dump(results_advanced, file, ensure_ascii=False, indent=2)
with ZipFile(OUT / 'Aset_Infografis_CDW2026.zip', 'w', compression=ZIP_DEFLATED) as archive:
    for file in sorted(OUT.rglob('*')):
        if file.is_file() and file.suffix.lower() in {'.png', '.svg', '.pdf', '.csv', '.json'}:
            archive.write(file, arcname=file.relative_to(OUT))
display(advanced_manifest_df)
print(f'{len(advanced_manifest)} visual tambahan diekspor; {14+len(advanced_manifest)} visual individual tersedia bersama visual sebelumnya.')
print('SVG:', SVG_OUT)
display(FileLink(str(ADV / 'Katalog_Analisis_Lanjutan_CDW2026.pdf')))
''')

nb.cells = nb.cells[:start] + new
nb.metadata['cdw']['advanced_analysis'] = ['Gower average-linkage clustering', 'Robust interaction models', 'Next-semester IP prediction with cohort holdout']
nbf.validate(nb)
nbf.write(nb, target)
print(f'Ditambahkan {len(new)} sel; total {len(nb.cells)} sel. Visual sebelumnya dipertahankan.')
