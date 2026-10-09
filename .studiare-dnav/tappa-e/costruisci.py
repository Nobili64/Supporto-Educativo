"""Edizione cumulativa B-E. Legge B e genera soltanto la nuova consegna."""
from pathlib import Path
import sys,re,json,subprocess,hashlib
ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
B=ROOT.parent/'tappa-b'
DELIVERY=PROJECT/'Studiare con il DNA-V - blocco E'
sys.path.insert(0,str(B/'strumenti/python-libs'))
import markdown2
NAMES={k:f'Studiare con il DNA-V - {v} - blocchi B-E.pdf' for k,v in {'manuale':'manuale operativo','ragazzo':'schede di lavoro A4','clinico':'strumenti per il clinico A4'}.items()}
def cover(kind):
 sub={'manuale':'Manuale operativo per un percorso di metodo di studio e di supporto psicologico con ragazzi e ragazze dagli 8 ai 16 anni con disturbi specifici dell’apprendimento','ragazzo':'Schede di lavoro per il ragazzo<br>Dal primo incontro al mantenimento','clinico':'Strumenti per il clinico<br>Osservazione, monitoraggio e restituzione'}[kind]
 return f'<section class="cover" id="copertina"><div class="band"></div><div class="eyebrow">Strumenti per il tutoraggio dell’apprendimento</div><h1>Studiare con il DNA-V</h1><p class="subtitle">{sub}</p><p class="edition">Blocchi B–E · edizione provvisoria<br>Testo completo per revisione</p><div class="cover-model">Metodo di studio<br>Flessibilità psicologica<br>Consapevolezza</div><p class="byline">a cura di Dott. Alberto Nespoli</p><p class="coverfoot">Materiale di lavoro ad uso professionale · ottobre 2026</p></section>'
def parts(text):
 p=re.split(r'^<!-- PAGE (.*?) -->\s*$',text,flags=re.M)
 if p[0].strip():raise ValueError('Testo fuori dalle pagine')
 return [(m,*m.split('|',1),b) for m,b in zip(p[1::2],p[2::2])]
def build(kind):
 text=(ROOT/f'{kind}.md').read_text(encoding='utf-8')
 source=parts(text); ids=[p[1] for p in source]
 if len(ids)!=len(set(ids)):raise ValueError('ID duplicati')
 toc=[(ident,re.search(r'^# (.+)$',body,re.M)[1]) for _,ident,run,body in source if re.search(r'^# (.+)$',body,re.M) and ident not in ['indice','edizione','guida']]
 if kind=='ragazzo':
  toc=[(i,('14. ' if i.startswith('sch14') else '1. ')+t+(' · 8–10 anni' if i.endswith('-semplice') else ' · ordinaria') if i in ['sch1','sch1-semplice','sch14','sch14-semplice'] else t) for i,t in toc]
 sections=[];tocpages=0
 for meta,ident,running,body in source:
  if ident=='indice':
   for start in range(0,len(toc),15):
    rows=toc[start:start+15];tocpages+=1
    sections.append(f'<section class="page" id="indice-{tocpages}"><div class="running">Indice · blocchi B–E</div><h1>Indice{ " · continua" if start else ""}</h1><div class="toc">'+''.join(f'<a href="#{i}">{t}</a>' for i,t in rows)+'</div></section>')
   continue
  body=body.replace('<div class="simple">','<div class="simple" markdown="1">')
  vectors=[]
  def keep_svg(m):
   vectors.append(m[0]);return f'<div class="figure-slot">FIGURE{len(vectors)-1}</div>'
  body=re.sub(r'<svg\b[\s\S]*?</svg>',keep_svg,body)
  html=markdown2.markdown(body,extras=['tables','break-on-newline','markdown-in-html'])
  for n,svg in enumerate(vectors):html=html.replace(f'<div class="figure-slot">FIGURE{n}</div>',svg)
  def lines(m):
   cls=m[1]; count=4 if 'four' in cls else 3 if 'three' in cls else 1 if 'one' in cls else 2
   return f'<div class="{cls}">'+('<span class="rule"></span>'*count)+'</div>'
  html=re.sub(r'<div class="(lines[^"]*)"></div>',lines,html)
  sections.append(f'<section class="page" id="{ident}"><div class="running">{running}</div>{html}</section>')
 html='<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="author" content="Dott. Alberto Nespoli"><title>'+NAMES[kind][:-4]+'</title><link rel="stylesheet" href="stile.css"></head><body class="'+kind+'">'+cover(kind)+''.join(sections)+'</body></html>'
 for link in re.findall(r'href="#([^"]+)"',html):
  if link not in ids and not link.startswith('indice-'):raise ValueError('Rimando assente '+link)
 (ROOT/f'{kind}.html').write_text(html,encoding='utf-8')
 DELIVERY.mkdir(exist_ok=True)
 out=DELIVERY/NAMES[kind]
 exe=B/'strumenti/weasyprint/onedir/weasyprint/weasyprint.exe'
 r=subprocess.run([str(exe),str(ROOT/f'{kind}.html'),str(out)],capture_output=True,text=True,encoding='utf-8')
 (ROOT/'qa'/f'weasyprint-{kind}.log').write_text(r.stdout+r.stderr,encoding='utf-8')
 if r.returncode:raise RuntimeError(r.stderr)
 result={'documento':kind,'file':str(out),'pagine_progettate':1+len(source)+(tocpages-1 if 'indice' in ids else 0),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'sezioni':[i for i in ids if i!='indice']}
 print(kind,result['pagine_progettate'],'pagine progettate')
 return result
if __name__=='__main__':
 results=[build(k) for k in sys.argv[1:] or list(NAMES)]
 (ROOT/'qa/generazione.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
