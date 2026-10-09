from pathlib import Path
from pypdf import PdfReader
import json,hashlib
R=Path(__file__).resolve().parent;P=R.parent.parent
base=P/'Studiare con il DNA-V - materiali per la redazione'
specs=[('cornoldi','Assets (markdown)/Le difficoltà di apprendimento a scuola.md',[(589,620),(655,695),(715,742),(770,810),(948,965),(1086,1135),(1192,1223)]),('genitori',str((base/'01 Schedario di Studio/Schedario di Studio - le schede in testo.md').relative_to(P)),[(627,645)]),('laboratorio',str((base/'03 Laboratorio in testo/Laboratorio studio DSA - risorse in testo.md').relative_to(P)),[(673,713),(1268,1294),(5999,6028)])]
reg=[]
for key,rel,ranges in specs:
 p=P/rel;ls=p.read_text(encoding='utf-8').split('\n');t=''
 for lo,hi in ranges:t+=f'\n{rel}: righe {lo}–{hi}\n'+'\n'.join(f'{n}: {ls[n-1]}' for n in range(lo,hi+1))+'\n'
 (R/'qa'/f'fonte-{key}.txt').write_text(t,encoding='utf-8')
 reg.append({'file':rel,'righe':ranges,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
p=base/'04 Normativa/Istituto Superiore di Sanità - Linea guida sulla gestione dei DSA (2022).pdf';reader=PdfReader(p)
for n in [50,51,137,138,139,140,227,228,321,330,335,340,352]:
 t=reader.pages[n-1].extract_text()
 (R/'qa'/f'iss-lettore-{n}.txt').write_text(t,encoding='utf-8')
 print(n,t[:100].replace('\n',' '),t[-60:].replace('\n',' '))
reg.append({'file':str(p.relative_to(P)),'pagine_lettore':[50,51,137,138,139,140,227,228,321,330,335,340,352],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(R/'registro-letture-e.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2),encoding='utf-8')
