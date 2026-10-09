"""Controlli ripetibili dei tre PDF; l'ispezione visiva resta separata."""
from pathlib import Path
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
import hashlib, json, re
from costruisci import NAMES, DELIVERY
BASE=Path(__file__).resolve().parent
PROJECT=BASE.parent.parent
EXPECTED={'manuale':40,'ragazzo':6,'clinico':11}
report={'data':'2026-10-01','controlli':[],'documenti':{},'limiti':['Non è una validazione clinica o psicometrica.','Non è la revisione indipendente della tappa F.','Prova fisica di stampa e prova in seduta da effettuare.']}
def check(name,ok,detail=''):
 report['controlli'].append({'controllo':name,'esito':bool(ok),'dettaglio':detail})
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

for kind,name in NAMES.items():
 path=DELIVERY/name;r=PdfReader(path);doc=pdfium.PdfDocument(path)
 out=BASE/'qa'/kind;out.mkdir(exist_ok=True)
 check(kind+': pagine previste',len(r.pages)==EXPECTED[kind],len(r.pages))
 sizes=[];fonts={};page_texts=[];bound_errors=[];dest_errors=[];thin=[]
 for n,page in enumerate(r.pages):
  text=page.extract_text();page_texts.append(text)
  if n>0 and len(text.strip())<250:thin.append(n+1)
  width,height=map(float,page.mediabox[2:]);sizes.append([round(width*25.4/72,2),round(height*25.4/72,2)])
  for value in page['/Resources'].get('/Font',{}).values():
   font=value.get_object();desc=font.get('/FontDescriptor')
   if not desc and font.get('/DescendantFonts'):desc=font['/DescendantFonts'][0].get_object().get('/FontDescriptor')
   fd=desc.get_object() if desc else {}
   fonts[str(font.get('/BaseFont'))]=any(k in fd for k in ['/FontFile','/FontFile2','/FontFile3'])
  for a in page.get('/Annots',[]):
   annot=a.get_object();dest=annot.get('/Dest')
   if isinstance(dest,str) and dest not in r.named_destinations:dest_errors.append([n+1,dest])
  tp=doc[n].get_textpage();bad=[]
  for c in range(tp.count_chars()):
   char=tp.get_text_range(c,1)
   if not char.strip():continue
   x0,y0,x1,y1=tp.get_charbox(c)
   if x0<8 or x1>width-8 or y0<8 or y1>height-8:bad.append([char,[round(v,1) for v in [x0,y0,x1,y1]]])
  if bad:bound_errors.append({'pagina':n+1,'caratteri':bad[:12]})
  doc[n].render(scale=1.7).to_pil().convert('RGB').save(out/f'pagina-{n+1:02d}.png')
 check(kind+': formato',all(s==([155.0,230.0] if kind=='manuale' else [210.0,297.0]) for s in sizes),sizes[0])
 check(kind+': caratteri incorporati',all(fonts.values()) and all(('Termes' in f or 'Heros' in f) for f in fonts),fonts)
 check(kind+': destinazioni interne',not dest_errors,dest_errors)
 check(kind+': testo entro pagina',not bound_errors,bound_errors)
 check(kind+': nessuna pagina residua breve',not thin,thin)
 whole='\n'.join(page_texts)
 check(kind+': nessuna marcatura residua',not re.search(r'(?m)^#{1,3}\s|\[INDICE\]|\ufffd|<!--',whole))
 check(kind+': motore richiesto',str(r.metadata.producer)=='WeasyPrint 70.0',str(r.metadata.producer))
 check(kind+': log pulito',not (BASE/'qa'/f'weasyprint-{kind}.log').read_text().strip())
 if kind=='manuale':
  for token in ['1. Come usare','2. Principi','3. Dal segnale','4. Che cosa','5. Diritti','6. L’incontro','7. Prima','8. Conoscere','25. Il modello','D1 ·','D2 ·','D3 ·']:
   check('manuale: contenuto '+token,token in whole)
  for source_id in ['cap25','d1','d2','d3']:
   check('manuale: sezione '+source_id,source_id in r.named_destinations)
  model_page=r.get_destination_page_number(r.named_destinations['cap25'])
  check('manuale: modello in una pagina','Schema originale per lo studio' in page_texts[model_page],model_page+1)
 if kind=='ragazzo':
  for pnum,token in [(3,'Come studio adesso'),(4,'Come studio adesso'),(5,'La mia mappa DNA-V'),(6,'La mia mappa DNA-V')]:
   check(f'ragazzo: indice pagina {pnum}',token in page_texts[pnum-1] if pnum<=len(page_texts) else False)
 if kind=='clinico':
  for pnum,token in [(3,'Colloquio iniziale'),(4,'Contesto, mandato'),(5,'Osservazione dello studio'),(6,'Dalla prova'),(7,'8–10 anni'),(8,'11–13 anni'),(9,'14–16 anni'),(10,'Profilo iniziale'),(11,'Appropriatezza e seguito')]:
   check(f'clinico: indice pagina {pnum}',token in page_texts[pnum-1] if pnum<=len(page_texts) else False)
 # Tutte le pagine in tavole da sei, per verifica visiva; PNG singoli ad alta risoluzione.
 for start in range(0,len(r.pages),6):
  tw=360;th=540 if kind=='manuale' else 515
  canvas=Image.new('RGB',(tw*3, (th+24)*2),'#ddd');draw=ImageDraw.Draw(canvas)
  for i,n in enumerate(range(start,min(start+6,len(r.pages)))):
   im=Image.open(out/f'pagina-{n+1:02d}.png');im.thumbnail((tw-12,th-10))
   x=(i%3)*tw+(tw-im.width)//2;y=(i//3)*(th+24)+22
   canvas.paste(im,(x,y));draw.text(((i%3)*tw+8,(i//3)*(th+24)+4),f'{kind} - pagina {n+1}',fill='black')
  canvas.save(BASE/'qa'/f'tavola-{kind}-{start+1:02d}.jpg',quality=90)
 (BASE/'qa'/f'testo-{kind}.txt').write_text('\n\n'.join(f'PAGINA {i+1}\n{t}' for i,t in enumerate(page_texts)),encoding='utf-8')
 report['documenti'][kind]={'file':str(path),'pagine':len(r.pages),'sha256':sha(path),'formato_mm':sizes[0],'font':fonts,'destinazioni_interne':len(r.named_destinations)}

timings={'ordinario90':[10,5,15,25,5,20,10],'ordinario60':[5,5,10,20,15,5],'dedicato90':[10,5,20,5,10,20,10,10],'primo90':[10,15,30,5,20,10],'primo60':[5,10,20,5,15,5],'vittoria20':[3,4,5,5,3],'vittoria15':[2,3,4,4,2],'secondo60':[5,5,10,15,5,15,5]}
for key,values in timings.items():check('minuti: '+key,sum(values)==int(re.search(r'\d+',key)[0]),sum(values))
snapshot=json.loads((PROJECT/'.studiare-dnav/tappa-a-consegna/impronte-fonti-consegna.json').read_text(encoding='utf-8'))
changed=[]
for record in snapshot:
 p=PROJECT/record['file']
 if not p.is_file() or sha(p)!=record['sha256']:changed.append(record['file'])
check('fonti originali: impronte invariate',not changed,{'file_controllati':len(snapshot),'differenze':changed})
report['esito']='PASS' if all(c['esito'] for c in report['controlli']) else 'DA_CORREGGERE'
(BASE/'qa/esito-controlli.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(report['esito'],len(report['controlli']),'controlli')
for c in report['controlli']:
 if not c['esito']:print(c)
print({k:v['pagine'] for k,v in report['documenti'].items()})
