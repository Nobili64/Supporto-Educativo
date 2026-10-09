from pathlib import Path
import json,sys,subprocess,hashlib,concurrent.futures
from pypdf import PdfReader
import pdfplumber
from PIL import Image,ImageOps,ImageDraw
from produci import ROOT,MAINT,WORK,write_json,load
POP=Path(r'C:\Users\megan\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe')
batch=sys.argv[1]
records=load(MAINT/'produzione/registrazioni'/(batch+'.json'),[])
qa=WORK/'verifiche'/batch;qa.mkdir(parents=True,exist_ok=True)
def check(r):
    f=ROOT/r['pdf'];reader=PdfReader(f);issues=[];pages=[]
    if len(reader.pages)!=r['expected_pages']:issues.append(f'Pagine attese {r["expected_pages"]}, presenti {len(reader.pages)}')
    subprocess.run([str(POP),'-r','96','-png',str(f),str(qa/r['id'])],capture_output=True,check=True)
    with pdfplumber.open(f) as pp:
        for i,(page,ppage) in enumerate(zip(reader.pages,pp.pages)):
            w,h=map(float,(page.mediabox.width,page.mediabox.height));text=page.extract_text()
            if abs(min(w,h)-595.28)>2 or abs(max(w,h)-841.89)>2:issues.append(f'Pagina {i+1}: non A4')
            if len(text.strip())<40:issues.append(f'Pagina {i+1}: testo insufficiente')
            off=[c.get('text') for c in ppage.chars if c['x0']<8 or c['x1']>w-8 or c['top']<8 or c['bottom']>h-8]
            if off:issues.append(f'Pagina {i+1}: caratteri fuori margine: {off[:12]}')
            png=next(qa.glob(r['id']+'-'+str(i+1).zfill(len(str(len(reader.pages))))+'.png'),None)
            if png is None:png=qa/f'{r["id"]}-{i+1}.png'
            gray=png.with_stem(png.stem+'-grigio');ImageOps.grayscale(Image.open(png)).save(gray)
            pages.append(dict(page=i+1,image=str(png),gray=str(gray),text=text))
    return dict(id=r['id'],pdf=r['pdf'],source=r['source'],sha256=hashlib.sha256(f.read_bytes()).hexdigest(),source_sha256=hashlib.sha256((ROOT/r['source']).read_bytes()).hexdigest(),issues=issues,pages=pages)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(check,records))
flat=[(r['id'],p) for r in result for p in r['pages']]
for i in range(0,len(flat),2):
    canvas=Image.new('RGB',(1620,1180),'#dddddd');draw=ImageDraw.Draw(canvas)
    for j,(rid,p) in enumerate(flat[i:i+2]):
        im=Image.open(p['gray']);im.thumbnail((794,1125));canvas.paste(im,(j*810+8,25));draw.text((j*810+12,1152),rid+' / '+str(p['page']),fill='black')
    canvas.save(qa/f'visione-{i//2+1:03}.png')
report=dict(batch=batch,documents=len(records),pages=len(flat),issues=[dict(id=r['id'],issues=r['issues']) for r in result if r['issues']],files=result,visual_review='da eseguire')
write_json(MAINT/'verifiche'/(batch+'.json'),report)
print(json.dumps(dict(documents=len(records),pages=len(flat),issues=report['issues'],montages=(len(flat)+1)//2,qa=str(qa)),ensure_ascii=False))
if report['issues']:sys.exit(1)
