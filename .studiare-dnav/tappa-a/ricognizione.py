"""Ricognizione in sola lettura delle fonti; scrive solo in questa cartella.
Eseguire con Python 3. La cartella Casi non viene enumerata né aperta.
"""
from pathlib import Path
import hashlib, json, re, zipfile
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
LAB = ROOT / 'Laboratorio studio DSA'
def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run():
    tracked = set()
    rows = []
    for p in sorted((ROOT/'Assets (markdown)'/'Repertori skill piano intervento').glob('*.md')):
        tracked.add(p)
        n = int(p.name[0]); lines = p.read_text(encoding='utf-8-sig').splitlines()
        area = ''; starts = []
        for i, line in enumerate(lines, 1):
            a = re.match(r'^## (\d+)\. (.+)',line)
            if a: area=a.group(1)
            m = (re.match(r'^#### (\d+)\. (.+)',line) if n==1 else
                 re.match(r'^\*\*(\d+)\. (.+?)\*\*',line) if n==2 else
                 re.match(r'^(\d+)\. \*\*(.+?)\*\*',line) if n==3 else
                 re.match(r'^\*\*([PADT]\d+)\. (.+?)\*\*',line))
            if m:
                code=f'R{n}-'+(area+'-' if n==3 else '')+m.group(1)
                starts.append((i,code,m.group(2).rstrip('.')))
        for j,(start,code,title) in enumerate(starts):
            end=starts[j+1][0]-1 if j+1<len(starts) else len(lines)
            # Stop the unit at the next section heading; keep procedure and cautions.
            for k in range(start,end):
                if lines[k].startswith('##'): end=k; break
            rows.append(dict(id=code,famiglia=f'Repertorio {n}',titolo=title,
                file=p.relative_to(ROOT).as_posix(),riga_inizio=start,riga_fine=end,
                contenuto='\n'.join(lines[start-1:end])))
    html = LAB/'Indice.html'; tracked.add(html)
    txt = html.read_text(encoding='utf-8-sig')
    catalog = json.loads(re.search(r'<script id="catalog-data"[^>]*>(.*?)</script>',txt,re.S).group(1))
    labrows=[]
    for x in catalog:
        record=dict(x)
        record['source_id']='LAB-'+x['ID']
        record['file_indice']=html.relative_to(ROOT).as_posix()
        for key in ('PDF','Sorgente'):
            p=LAB/x[key]
            record[key+'_esiste']=p.is_file()
            if p.is_file(): tracked.add(p)
        p=LAB/x['Sorgente']
        if p.is_file() and p.suffix in ('.odt','.odg'):
            with zipfile.ZipFile(p) as z:
                xml=ET.fromstring(z.read('content.xml'))
                ns='{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'
                record['testo_sorgente']='\n'.join(''.join(e.itertext()) for e in xml.iter() if e.tag in (ns+'p',ns+'h'))
        labrows.append(record)
    for p in (ROOT/'Assets (markdown)').glob('*.md'): tracked.add(p)
    for name in ('Il DNA-V in seduta - compendio operativo.pdf','Il DNA-V in seduta - schede di lavoro A4.pdf','Studiare con il DNA-V - piano del manuale.md'):
        tracked.add(ROOT/name)
    save('inventario-repertori.json',rows)
    save('inventario-laboratorio.json',labrows)
    save('impronte-fonti.json',[dict(file=p.relative_to(ROOT).as_posix(),sha256=digest(p),bytes=p.stat().st_size) for p in sorted(tracked)])
    print(json.dumps({'repertori':{str(n):sum(x['famiglia']==f'Repertorio {n}' for x in rows) for n in range(1,5)},'laboratorio':len(labrows),'kit':len(set(x['Kit'] for x in labrows)), 'file_tracciati':len(tracked),'collegamenti_mancanti':[{k:x[k] for k in ('ID','PDF','Sorgente')} for x in labrows if not x['PDF_esiste'] or not x['Sorgente_esiste']]},ensure_ascii=False,indent=2))

if __name__=='__main__': run()
