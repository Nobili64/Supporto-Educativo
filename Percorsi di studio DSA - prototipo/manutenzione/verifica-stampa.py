from pathlib import Path
import json, subprocess
from pypdf import PdfReader
import pdfplumber
from PIL import Image, ImageDraw
base=Path(__file__).parent/'verifiche'
pop=Path('C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe')
report=[]
for name in ['M02-02','M08-08','M21-04','MC-01','MM-01']:
    file=base/(name+'.pdf')
    reader=PdfReader(file)
    item={'file':file.name,'pages':len(reader.pages),'blank':[],'out_of_bounds':[]}
    with pdfplumber.open(file) as doc:
        for i,page in enumerate(doc.pages):
            if not page.extract_text().strip():item['blank'].append(i+1)
            for w in page.extract_words():
                if w['x0']<25 or w['top']<25 or w['x1']>page.width-25 or w['bottom']>page.height-25:item['out_of_bounds'].append([i+1,w['text']])
    subprocess.run([str(pop),'-gray','-scale-to','1350','-png',str(file),str(base/('stampa-'+name))],check=True,capture_output=True)
    pages=sorted(base.glob('stampa-'+name+'-*.png'))
    contact=Image.new('RGB',(960,720),'#dedede');draw=ImageDraw.Draw(contact)
    for i,f in enumerate(pages[:3]):
        im=Image.open(f).convert('RGB');im.thumbnail((310,675));contact.paste(im,(10+320*i,30));draw.text((10+320*i,8),f'{name} - {i+1}',fill='black')
    contact.save(base/('contatto-'+name+'.png'))
    report.append(item)
(base/'stampa-risultati.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False))
assert all(x['pages']==3 and not x['blank'] and not x['out_of_bounds'] for x in report), 'Controllare pagine o contenuto fuori margine'
