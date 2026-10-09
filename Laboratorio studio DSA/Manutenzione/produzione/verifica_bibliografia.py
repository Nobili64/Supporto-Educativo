"""Controlla migrazione delle fonti e rilettura del catalogo ODS corrente."""
import json,hashlib,zipfile,xml.etree.ElementTree as ET
from prepara_catalogo import read_ods,ROOT,M,W,main
old={r['ID']:r for r in read_ods(M/'archivio/Catalogo-pre-bibliografia-101.ods')}
new={r['ID']:r for r in read_ods(ROOT/'Catalogo.ods')}
bib={r['ID']:r['Riferimenti'] for r in read_ods(ROOT/'Catalogo.ods','Bibliografia')}
checks=[]
def check(name,ok):
    checks.append(dict(name=name,passed=bool(ok)))
check('Tutte le 101 righe precedenti conservate',set(old)<=set(new))
check('Campi precedenti diversi da Fonti invariati',all(all(n.get(k)==v for k,v in o.items() if k!='Fonti') for rid,o in old.items() for n in [new[rid]]))
check('Fonti precedenti conservate integralmente in Bibliografia',all(bib.get(rid)==r['Fonti'] for rid,r in old.items()))
check('Una bibliografia per ogni risorsa corrente',set(new)==set(bib))
check('Rimandi corretti',all(r['Fonti']=='Riferimenti completi nel foglio Bibliografia: '+rid+'.' for rid,r in new.items()))
for d in json.loads((M/'produzione/registrazioni/L06-storia-scienze.json').read_text(encoding='utf-8')):
    check('Fonti nuove '+d['id'],bib[d['id']]==d['sources'])
before=json.loads((W/'catalogo-input.json').read_text(encoding='utf-8'))
main()
after=json.loads((W/'catalogo-input.json').read_text(encoding='utf-8'))
check('Rilettura e preparazione ODS senza perdita di dati',before==after)
ns={'style':'urn:oasis:names:tc:opendocument:xmlns:style:1.0','table':'urn:oasis:names:tc:opendocument:xmlns:table:1.0','text':'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
def heights(file):
    with zipfile.ZipFile(file) as z:x=ET.fromstring(z.read('content.xml'))
    styles={s.get('{'+ns['style']+'}name'):s.find('style:table-row-properties',ns) for s in x.findall('.//style:style',ns)}
    tab=next(t for t in x.findall('.//table:table',ns) if t.get('{'+ns['table']+'}name')=='Risorse')
    out={}
    for row in tab.findall('.//table:table-row',ns):
        cell=row.find('table:table-cell',ns)
        if cell is None:continue
        rid=''.join(cell.itertext())
        p=styles.get(row.get('{'+ns['table']+'}style-name'))
        if p is not None:out[rid]=p.get('{'+ns['style']+'}row-height')
    return out
oh=heights(M/'archivio/Catalogo-pre-bibliografia-101.ods');nh=heights(ROOT/'Catalogo.ods')
report=dict(catalog_sha256=hashlib.sha256((ROOT/'Catalogo.ods').read_bytes()).hexdigest(),resources=len(new),bibliographies=len(bib),checks=checks,row_height_examples={rid:dict(before=oh.get(rid),after=nh.get(rid)) for rid in ['STO03-S','STO05-S','SCI03-S']},passed=all(c['passed'] for c in checks))
(M/'verifiche/catalogo-bibliografia.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
assert report['passed']
