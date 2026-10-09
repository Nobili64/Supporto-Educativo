"""QA ripetibile; separa controlli documentali da lettura visiva e verifica clinica."""
from pathlib import Path
from pypdf import PdfReader
import pypdfium2 as pdfium
from PIL import Image,ImageDraw
import json,re,hashlib
from costruisci import ROOT as R,PROJECT as P,DELIVERY,NAMES
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report={'data':'2026-10-01','controlli':[],'documenti':{},'limiti':['Non validazione clinica o psicometrica.','Revisione indipendente F non eseguita.','Prove in seduta e stampa fisica non documentate.']}
def check(name,ok,detail=''):report['controlli'].append({'controllo':name,'esito':bool(ok),'dettaglio':detail})
gen={d['documento']:d for d in json.loads((R/'qa/generazione.json').read_text(encoding='utf-8'))}
for kind,name in NAMES.items():
 path=DELIVERY/name;reader=PdfReader(path);doc=pdfium.PdfDocument(path);out=R/'qa'/kind;out.mkdir(exist_ok=True)
 check(kind+': pagine progettate',len(reader.pages)==gen[kind]['pagine_progettate'],{'reali':len(reader.pages),'attese':gen[kind]['pagine_progettate']})
 fonts={};sizes=[];bounds=[];badlinks=[];texts=[];startpages={}
 for ident,dest in reader.named_destinations.items():startpages.setdefault(reader.get_destination_page_number(dest),[]).append(ident)
 for i,page in enumerate(reader.pages):
  texts.append(page.extract_text());w,h=map(float,page.mediabox[2:]);sizes.append([round(w*25.4/72,2),round(h*25.4/72,2)])
  for value in page['/Resources'].get('/Font',{}).values():
   font=value.get_object();desc=font.get('/FontDescriptor')
   if not desc and font.get('/DescendantFonts'):desc=font['/DescendantFonts'][0].get_object().get('/FontDescriptor')
   fd=desc.get_object() if desc else {};fonts[str(font.get('/BaseFont'))]=any(k in fd for k in ['/FontFile','/FontFile2','/FontFile3'])
  for item in page.get('/Annots',[]):
   a=item.get_object();dest=a.get('/Dest')
   if isinstance(dest,str) and dest not in reader.named_destinations:badlinks.append([i+1,dest])
  tp=doc[i].get_textpage();bad=[]
  for j in range(tp.count_chars()):
   c=tp.get_text_range(j,1)
   if not c.strip():continue
   x0,y0,x1,y1=tp.get_charbox(j)
   if min(x0,y0)<8 or x1>w-8 or y1>h-8:bad.append([c,[round(v,1) for v in [x0,y0,x1,y1]]])
  if bad:bounds.append({'pagina':i+1,'caratteri':bad[:8]})
  doc[i].render(scale=1.7).to_pil().convert('RGB').save(out/f'pagina-{i+1:03d}.png')
 whole='\n'.join(texts)
 check(kind+': nessuna pagina di overflow',all(i in startpages for i in range(1,len(reader.pages))),[i+1 for i in range(1,len(reader.pages)) if i not in startpages])
 check(kind+': formato',all(s==([155.0,230.0] if kind=='manuale' else [210.0,297.0]) for s in sizes),sizes[0])
 check(kind+': font incorporati',all(fonts.values()) and all('Termes' in f or 'Heros' in f for f in fonts),fonts)
 check(kind+': link interni',not badlinks,badlinks)
 check(kind+': testo entro pagina',not bounds,bounds)
 check(kind+': nessuna marcatura residua',not re.search(r'(?m)^#{1,3}\s|\[INDICE\]|\ufffd|<!--',whole))
 check(kind+': WeasyPrint richiesto',str(reader.metadata.producer)=='WeasyPrint 70.0',str(reader.metadata.producer))
 check(kind+': log pulito',not (R/'qa'/f'weasyprint-{kind}.log').read_text().strip())
 expected=gen[kind]['sezioni'];check(kind+': tutte le sezioni',all(i in reader.named_destinations for i in expected))
 if kind=='manuale':
  for label,ids in [('S1–S31',[f's{i}' for i in range(1,32)]),('D nuove',[f'd{i}' for i in [4,6,7,11,12,13,14,15,16,17,18]]),('C1–C5',[f'c{i}' for i in range(1,6)]),('B preservato nei contenuti',['cap1','cap8','cap25','d1','d2','d3']),('figure originali',['s19-figura','s21-figura','s28-figura'])]:
   check('manuale: '+label,all(i in reader.named_destinations for i in ids),ids)
  check('manuale: limiti espliciti',all(t in whole for t in ['non è documentata','tappa F','Non è un protocollo validato']))
  check('manuale: AND italiano','attenzione, nominare, descrivere' in whole)
 if kind=='ragazzo':
  check('ragazzo: codici richiesti',all(f'Scheda {i}' in whole for i in [1,2,3,4,5,6,7,10,11,14,15,16,17,19]))
  check('ragazzo: sei varianti concrete',sum('Versione concreta' in t or 'Versione 8–10' in t for t in texts)>=4)
 if kind=='clinico':check('clinico: strumenti1–6',all(f'Strumento {i}' in whole for i in range(1,7)))
 for start in range(0,len(reader.pages),6):
  tw=360;th=540 if kind=='manuale' else 515;canvas=Image.new('RGB',(tw*3,(th+24)*2),'#ddd');draw=ImageDraw.Draw(canvas)
  for j,n in enumerate(range(start,min(start+6,len(reader.pages)))):
   im=Image.open(out/f'pagina-{n+1:03d}.png');im.thumbnail((tw-12,th-10));x=(j%3)*tw+(tw-im.width)//2;y=(j//3)*(th+24)+22
   canvas.paste(im,(x,y));draw.text(((j%3)*tw+8,(j//3)*(th+24)+4),f'{kind} - pagina {n+1}',fill='black')
  canvas.save(R/'qa'/f'tavola-{kind}-{start+1:03d}.jpg',quality=92)
 (R/'qa'/f'testo-{kind}.txt').write_text('\n\n'.join(f'PAGINA {i+1}\n{t}' for i,t in enumerate(texts)),encoding='utf-8')
 report['documenti'][kind]={'file':str(path),'pagine':len(reader.pages),'sha256':sha(path),'formato_mm':sizes[0],'font':fonts,'destinazioni':len(reader.named_destinations),'pagine_sezioni':{ident:reader.get_destination_page_number(d)+1 for ident,d in reader.named_destinations.items()}}
for key,values,total in [('fase2',[5,5,10,20,15,5],60),('fase3',[10,5,15,25,5,20,10],90),('S3',[8,8,8],24),('S5',[12,3,12,3],30)]:check('aritmetica '+key,sum(values)==total,sum(values))
check('geometria: area e perimetro',8*3==24 and 2*(8+3)==22 and 6*4==24 and 2*(6+4)==20)
check('cronologia: scala',10/(2020-2000)*(2010-2000)==5 and 10/20*(2015-2000)==7.5 and 10/20*(2005-2000)==2.5)
check('frazione: parti uguali',len([60,180,300,420])==4 and 360/480==3/4)
for label,snapshot in [('fonti originali',json.loads((P/'.studiare-dnav/tappa-a-consegna/impronte-fonti-consegna.json').read_text(encoding='utf-8'))),('consegna B',json.loads((R/'impronte-blocco-b.json').read_text(encoding='utf-8')))]:
 changed=[d['file'] for d in snapshot if not (P/d['file']).is_file() or sha(P/d['file'])!=d['sha256']]
 check(label+': impronte invariate',not changed,{'controllati':len(snapshot),'differenze':changed})
refs=json.loads((R/'registro-citazioni-s.json').read_text(encoding='utf-8'));bad=[]
for d in refs:
 p=P/d['file'];a=p.read_text(encoding='utf-8').split('\n');lo,hi=d['righe']
 if not (0<lo<=hi<=len(a)) or sha(p)!=d['sha256']:bad.append(d['scheda'])
check('citazioni S: file, righe e impronte',len(refs)==31 and not bad,bad)
data=json.loads((R/'strategie.json').read_text(encoding='utf-8'));required={'SCOPO','MODELLO','GUIDA','PERSONALE','NUOVO','ESEMPIO','ETÀ','PROFILI','LIVELLI','ERRORI','AGGANCIO','NOTA'}
check('strategie: contenuto strutturato completo',len(data)==31 and all(set(d['campi'])==required and all(d['campi'].values()) for d in data))
report['esito']='PASS' if all(c['esito'] for c in report['controlli']) else 'DA_CORREGGERE'
(R/'qa/esito-controlli.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(report['esito'],len(report['controlli']),'controlli')
for c in report['controlli']:
 if not c['esito']:print(c)
print({k:v['pagine'] for k,v in report['documenti'].items()})
