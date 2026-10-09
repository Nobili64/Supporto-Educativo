from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageOps,ImageDraw
from pypdf import PdfReader
import pdfplumber
base=Path(__file__).parent/'verifiche'
pop=Path('C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin')
files=sorted(base.glob('M*-print-*.pdf'))+sorted(base.glob('*-scheda*.pdf'))+sorted(base.glob('*-mappa.pdf'))+sorted(base.glob('*-traccia.pdf'))
files=[f for f in files if not f.name.startswith('prima-')]
files += [base/'tocco-stampa-diretta.pdf',base/'stampa-inizio.pdf']
report={'sha256':hashlib.sha256((base.parent.parent/'Metodo di studio DSA.html').read_bytes()).hexdigest(),'pdf':len(files),'pages':0,'bounds':[],'blank_pages':[],'sizes':[]}
for f in files:
 r=PdfReader(f)
 for i,p in enumerate(r.pages):
  report['pages']+=1
  w,h=float(p.mediabox.width),float(p.mediabox.height)
  if abs(w-595.28)>2 or abs(h-841.89)>2: report['sizes'].append([f.name,i+1,w,h])
  if not (p.extract_text() or '').strip():report['blank_pages'].append([f.name,i+1])
 with pdfplumber.open(f) as doc:
  for i,p in enumerate(doc.pages):
   for word in p.extract_words():
    if word['x0']<39 or word['top']<39 or word['x1']>p.width-39 or word['bottom']>p.height-39:report['bounds'].append([f.name,i+1,word])
 (base/'stampa-risultati.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
screens=sorted(base.glob('edge-M[CM]-*.png'))
for start in range(0,len(screens),4):
 sheet=Image.new('RGB',(1920,1400),'white');draw=ImageDraw.Draw(sheet)
 for k,f in enumerate(screens[start:start+4]):
  im=Image.open(f).convert('RGB');im.thumbnail((940,645));x=(k%2)*960;y=(k//2)*700
  draw.text((x+12,y+8),f.stem,fill='black',font_size=23);sheet.paste(im,(x+10,y+42))
 sheet.save(base/f'mappe-contatto-{start//4+1:02}.png')
for name in ['MC-05-print-map','MM-05-print-map','MC-17-print-map','MM-17-print-scaffold','edge-scheda-lunga','chrome-scheda','MC-11-print-map']:
 f=base/(name+'.pdf')
 if f.exists():
  for old in base.glob('pagina-'+name+'-*.png'):old.unlink()
  subprocess.run([str(pop/'pdftoppm.exe'),'-gray','-scale-to','1500','-png',str(f),str(base/('pagina-'+name))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print(json.dumps(report,ensure_ascii=False))
