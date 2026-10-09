from pathlib import Path
import json,subprocess,concurrent.futures,hashlib
from pypdf import PdfReader
from PIL import Image,ImageOps,ImageDraw
import pdfplumber
B=Path(__file__).parent;O=B/'library';Q=B/'qa'/'pages';Q.mkdir(parents=True,exist_ok=True)
POP=Path(r'C:\Users\megan\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
D=json.loads((B/'catalog-data.json').read_text(encoding='utf-8'))
def render(r):
    f=O/r['pdf'];reader=PdfReader(f)
    assert len(reader.pages)==r['expected_pages'],(r['id'],len(reader.pages),r['expected_pages'])
    subprocess.run([str(POP/'pdftoppm.exe'),'-r','100','-png',str(f),str(Q/r['id'])],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    with pdfplumber.open(f) as native:
        words=[page.extract_words() for page in native.pages]
    (Q/(r['id']+'-testo.json')).write_text(json.dumps(words,ensure_ascii=False),encoding='utf-8')
    pages=[]
    for i,p in enumerate(reader.pages):
        w,h=map(float,(p.mediabox.width,p.mediabox.height))
        assert abs(min(w,h)-595.28)<2 and abs(max(w,h)-841.89)<2,(r['id'],w,h)
        assert len(p.extract_text().strip())>60,(r['id'],i,'pagina vuota')
        png=Q/f'{r["id"]}-{i+1}.png'
        assert png.exists(),png
        with Image.open(png) as img:ImageOps.grayscale(img).save(Q/f'{r["id"]}-{i+1}-grigio.png')
        pages.append(dict(id=r['id'],page=i+1,png=str(png),width=w,height=h))
    return dict(id=r['id'],pages=pages,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(render,D))
allpages=[p for r in results for p in r['pages']]
(B/'qa'/'pdf-report.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for n in range(0,len(allpages),6):
    sheet=Image.new('RGB',(1500,1500),'#e5e5e5');draw=ImageDraw.Draw(sheet)
    for j,p in enumerate(allpages[n:n+6]):
        img=Image.open(p['png']);img.thumbnail((480,695))
        x=(j%3)*500+(500-img.width)//2;y=(j//3)*750+25
        sheet.paste(img,(x,y));draw.text(((j%3)*500+10,(j//3)*750+730),p['id']+' / '+str(p['page']),fill='black')
    sheet.save(B/'qa'/f'panoramica-{n//6+1}.png')
print(json.dumps({'pdf':len(results),'pagine':len(allpages),'report':str(B/'qa'/'pdf-report.json')}))
