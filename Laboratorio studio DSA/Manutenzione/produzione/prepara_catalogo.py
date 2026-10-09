from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET,hashlib
from registro_kit import ROOT,KITS
M=ROOT/'Manutenzione';W=ROOT.parent/'.lavorazione-dsa'
NS={x:'urn:oasis:names:tc:opendocument:xmlns:'+x+':1.0' for x in ['office','table','text']}
HEAD=['ID','Titolo','Materia','Argomento','Classe','Obiettivo','Tipo','Guida','Destinatario','PDF','Sorgente','Revisione','Kit','Prerequisiti','Compito','Difficolta','Strumento','Curricolo','Coorte','Fonti','Versione','Stato']
KEYS=['id','title','subject','topic','school','objective','kind','level','audience','pdf','source','date','kit','prerequisites','task','difficulty','tool','curriculum','cohort','sources','version','status']
def read_ods(file,sheet='Risorse'):
    with zipfile.ZipFile(file) as z:r=ET.fromstring(z.read('content.xml'))
    table=next((t for t in r.findall('.//table:table',NS) if t.get('{'+NS['table']+'}name')==sheet),None)
    if table is None:return []
    out=[];heads=None
    for row in table.findall('.//table:table-row',NS):
        cells=[]
        for c in row:
            if c.tag.split('}')[-1] not in ['table-cell','covered-table-cell']:continue
            v=c.get('{'+NS['office']+'}date-value') or '\n'.join(''.join(p.itertext()) for p in c.findall('text:p',NS))
            if not v:v=c.get('{'+NS['office']+'}value','')
            n=min(int(c.get('{'+NS['table']+'}number-columns-repeated','1')),max(0,len(HEAD)-len(cells)))
            cells.extend([v]*n)
        if cells and cells[0]=='ID':heads=cells;continue
        if heads and any(cells):out.append(dict(zip(heads,cells)))
    return out
def main():
    rows=read_ods(ROOT/'Catalogo.ods');records={r['ID']:r for r in rows}
    bib={r['ID']:r.get('Riferimenti','') for r in read_ods(ROOT/'Catalogo.ods','Bibliografia')}
    for r in records.values():
        if r.get('Fonti')=='Riferimenti completi nel foglio Bibliografia: '+r['ID']+'.':
            if not bib.get(r['ID']):raise ValueError('Bibliografia mancante per '+r['ID'])
            r['Fonti']=bib[r['ID']]
    for r in records.values():
        kit={'Matematica':'MAT04','Storia':'STO04','Scienze':'SCI06'}.get(r['Materia'],r['ID'])
        defaults=dict(Kit=kit,Prerequisiti='Comprendere la consegna con i supporti abituali',Compito=r['Obiettivo'],Difficolta='Osservare avvio, selezione delle informazioni e controllo',Strumento=r['Tipo'],Curricolo='D.M. 254/2012: '+r['Materia']+'; D.M. 221/2025 per le nuove coorti, confronto con la scuola',Coorte='II-III 2026/27: quadro 2012; I 2026/27: quadro 2025',Fonti='Riferimenti nella guida tutor e nella guida alle fonti recuperate',Versione='1.0 recuperata',Stato='pronto')
        for k,v in defaults.items():r.setdefault(k,v)
    for f in sorted((M/'produzione/registrazioni').glob('*.json')):
        for d in json.loads(f.read_text(encoding='utf-8')):
            if d.get('private'):continue
            if d['id'] in records:continue # Catalogo esistente prevale su dati di produzione.
            d.setdefault('cohort','II-III 2026/27: quadro 2012; I 2026/27: quadro 2025')
            records[d['id']]={h:str(d.get(k,'')) for h,k in zip(HEAD,KEYS)}
    coverage=[]
    for kid,k in KITS.items():
        rr=[r for r in records.values() if r['Kit']==kid]
        status='pronto' if rr and all(r['Stato']=='pronto' for r in rr) else 'da verificare' if rr else 'mancante'
        specfile=M/'produzione/contenuti'/(kid+'.json')
        spec=json.loads(specfile.read_text(encoding='utf-8')) if specfile.exists() else {}
        coverage.append([kid,k['subject'],k['title'],status,spec.get('coverage','Kit recuperato: vedere schede e guida' if rr else 'Da produrre'),spec.get('gaps','Approfondimenti e ulteriori esempi da concordare con la scuola' if rr else 'Intero kit'),'; '.join(r['ID'] for r in rr),len(rr)])
    W.mkdir(exist_ok=True)
    bibliography=[[r['ID'],r['Kit'],r.get('Fonti','')] for r in records.values()]
    display_rows=[]
    for r in records.values():
        display=dict(r,Fonti='Riferimenti completi nel foglio Bibliografia: '+r['ID']+'.')
        display_rows.append([display.get(h,'') for h in HEAD])
    (W/'catalogo-input.json').write_text(json.dumps(dict(headings=HEAD,rows=display_rows,coverage=coverage,bibliography=bibliography),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(records)} risorse; {len(coverage)} kit previsti')
if __name__=='__main__':main()
