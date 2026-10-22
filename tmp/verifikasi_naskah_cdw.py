from pathlib import Path
import json
import math
import re
from html.parser import HTMLParser
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
raw = [pd.read_csv(ROOT / '02_Analisis' / 'data' / f, sep=';') for f in [
    '1_profil_mahasiswa_umum.csv', '2_prestasi_mahasiswa.csv',
    '3_generasi_pertama_kuliah.csv', '4_status_sosial_ekonomi.csv',
    '5_riwayat_ipk_semester.csv']]
p, ach, gen, eco, history = raw
ach = ach.drop_duplicates()
d = p.merge(gen, on='ID_Mahasiswa', validate='one_to_one').merge(
    eco, on='ID_Mahasiswa', suffixes=('_profil', '_ekonomi'), validate='one_to_one')
d['fg'] = (d.Status_Generasi_Pertama == 'Ya').astype(int)
d['work'] = (d.Bekerja_Sambil_Kuliah == 'Ya').astype(int)
d['sch'] = (d.Status_Penerima_Beasiswa == 'Ya').astype(int)
d['achievement'] = d.ID_Mahasiswa.isin(ach.ID_Mahasiswa).astype(int)
d['natplus'] = d.ID_Mahasiswa.isin(ach.loc[ach.Tingkat_Kegiatan.isin(
    ['Tingkat Nasional','Tingkat Internasional']), 'ID_Mahasiswa']).astype(int)
d['winner'] = d.ID_Mahasiswa.isin(ach.loc[ach.Capaian_Prestasi.isin(
    ['Juara 1','Juara 2','Juara 3']), 'ID_Mahasiswa']).astype(int)
d['interrupted'] = d.Status_Mahasiswa.isin(['Cuti', 'Non-Aktif/DO']).astype(int)
ipk = history.pivot(index='ID_Mahasiswa',columns='Semester_Ke',values='IPK_Kumulatif')
ips = history.pivot(index='ID_Mahasiswa',columns='Semester_Ke',values='IP_Semester')
d = d.merge(ipk[[1,4]].rename(columns={1:'s1',4:'s4'}),left_on='ID_Mahasiswa',right_index=True)
d = d.merge(ips[[4]].rename(columns={4:'ips4'}),left_on='ID_Mahasiswa',right_index=True)
d['gain'] = d.s4-d.s1

def group(cols, data=d):
    return data.groupby(cols,observed=True).agg(
        n=('ID_Mahasiswa','size'), ipk=('IPK_Mahasiswa','mean'),
        achievement=('achievement','mean'), natplus=('natplus','mean'),
        winner=('winner','mean'), work_rate=('work','mean'), sch=('sch','mean'),
        interrupted=('interrupted','mean'), n14=('gain','count'),
        gain=('gain','mean')).reset_index().to_dict('records')

def design(data, extra=None):
    nums=['fg','work','sch','Tingkat_Dukungan_Keluarga','Jumlah_Tanggungan_Keluarga']
    cats=['Kategori_Ekonomi','Kategori_UKT','Jenis_Kelamin','Fakultas']
    if extra == 'semester': cats += ['Masa_Studi_Semester']
    if extra == 'baseline': nums += ['s1']; cats += ['Angkatan']
    frame=data[nums].astype(float)
    for col in cats:
        dummy=pd.get_dummies(data[col].astype('category'),prefix=col,drop_first=True,dtype=float)
        frame=pd.concat([frame,dummy],axis=1)
    frame.insert(0,'Intercept',1.)
    return frame.to_numpy(dtype=float),list(frame.columns)

def ols(data, outcome='IPK_Mahasiswa', extra=None):
    x, names=design(data,extra)
    y=data[outcome].to_numpy(float)
    beta=np.linalg.lstsq(x,y,rcond=None)[0]
    bread=np.linalg.pinv(x.T@x)
    residual=y-x@beta
    hat=np.einsum('ij,jk,ik->i',x,bread,x)
    v=(residual/(1-hat))**2
    cov=bread @ (x.T @ (x*v[:,None])) @ bread
    se=np.sqrt(np.diag(cov))
    result=[]
    for label in ['fg','work','sch','s1']:
        if label not in names: continue
        i=names.index(label)
        result.append({'term':label,'beta':beta[i], 'ci95':[beta[i]-1.95996398454*se[i],beta[i]+1.95996398454*se[i]],
                       'p_normal':math.erfc(abs(beta[i]/se[i])/math.sqrt(2))})
    return {'n':len(data),'r2':1-(residual@residual)/np.sum((y-y.mean())**2),'terms':result}

def logistic(data, extra=None):
    x, names=design(data,extra)
    y=data.achievement.to_numpy(float)
    beta=np.zeros(x.shape[1])
    for it in range(80):
        prob=1/(1+np.exp(-np.clip(x@beta,-35,35)))
        weight=prob*(1-prob)
        step=np.linalg.solve(x.T @ (x*weight[:,None]),x.T @ (y-prob))
        beta+=step
        if abs(step).max()<1e-10: break
    prob=1/(1+np.exp(-np.clip(x@beta,-35,35)))
    bread=np.linalg.pinv(x.T@(x*(prob*(1-prob))[:,None]))
    cov=bread@(x.T@(x*((y-prob)**2)[:,None]))@bread
    se=np.sqrt(np.diag(cov))
    terms=[]
    for label in ['fg','work','sch']:
        i=names.index(label)
        terms.append({'term':label,'or':math.exp(beta[i]),'ci95':[math.exp(beta[i]-1.95996398454*se[i]),math.exp(beta[i]+1.95996398454*se[i])]})
    return {'n':len(data),'converged':it<79,'terms':terms}

fixed=d.dropna(subset=['s1','s4']).copy()
cohort=fixed.groupby('fg').agg(n=('ID_Mahasiswa','size'),s1=('s1','mean'),s4=('s4','mean'),gain=('gain','mean'))
gap1=cohort.loc[0,'s1']-cohort.loc[1,'s1']
gap4=cohort.loc[0,'s4']-cohort.loc[1,'s4']
low=d[(d.fg==1)&(d.Kategori_Ekonomi=='Rendah')]
result={
 'overview':{'n':len(d),'fg_n':int(d.fg.sum()),'fg_rate':d.fg.mean(), 'low_n':int((d.Kategori_Ekonomi=='Rendah').sum()),
             'fg_among_low':d.loc[d.Kategori_Ekonomi=='Rendah','fg'].mean(),
             'cohort_n':len(fixed),'gain_ratio':cohort.loc[1,'gain']/cohort.loc[0,'gain'],
             'gap1':gap1,'gap4':gap4,'gap_narrowing':1-gap4/gap1,
             'low_fg_work_n':int(low.work.sum()),'low_fg_work':low.work.mean(),
             'low_fg_sch':low.sch.mean(), 'low_fg_sch_work':low.loc[low.sch==1,'work'].mean(),
             'low_fg_sch_work_n':int(low.loc[low.sch==1,'work'].sum()),
             'participant_records':int((ach.Capaian_Prestasi=='Peserta').sum())},
 'cohort':cohort.reset_index().to_dict('records'),
 'fg_economy':group(['fg','Kategori_Ekonomi']),
 'low_intersections':group(['fg','work'],data=d[d.Kategori_Ekonomi=='Rendah']),
 'original_ols':ols(d), 'duration_ols':ols(d,extra='semester'),
 'original_logistic':logistic(d), 'duration_logistic':logistic(d,extra='semester'),
 'baseline_ips4':ols(fixed,outcome='ips4',extra='baseline'),
}
print(json.dumps(result,ensure_ascii=False,indent=2,default=float))
