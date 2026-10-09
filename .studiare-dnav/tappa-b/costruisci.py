"""Generazione locale del blocco B; non modifica fonti o consegne precedenti."""
from pathlib import Path
import sys, re, json, subprocess, hashlib
ROOT = Path(__file__).resolve().parent
DELIVERY = ROOT.parent.parent / 'Studiare con il DNA-V - blocco B'
sys.path.insert(0, str(ROOT / 'strumenti/python-libs'))
import markdown2

NAMES = {
 'manuale': 'Studiare con il DNA-V - manuale operativo - blocco B.pdf',
 'ragazzo': 'Studiare con il DNA-V - schede di lavoro A4 - blocco B.pdf',
 'clinico': 'Studiare con il DNA-V - strumenti per il clinico A4 - blocco B.pdf',
}
def cover(kind):
 sub = {'manuale': 'Manuale operativo per un percorso di metodo di studio e di supporto psicologico con ragazzi e ragazze dagli 8 ai 16 anni con disturbi specifici dell’apprendimento', 'ragazzo': 'Schede di lavoro per il ragazzo\nSchede 1 e 14, con versioni per 8–10 anni', 'clinico': 'Strumenti per il clinico\nStrumenti 1–4, con tre interviste per età'}[kind]
 return f'''<section class="cover" id="copertina"><div class="band"></div><div class="eyebrow">Strumenti per il tutoraggio dell’apprendimento</div><h1>Studiare con il DNA-V</h1><p class="subtitle">{sub.replace(chr(10), '<br>')}</p><p class="edition">Blocco B · edizione provvisoria<br>Fondamenti e avvio del percorso</p><div class="cover-model">Metodo di studio<br>Flessibilità psicologica<br>Consapevolezza</div><p class="byline">a cura di Dott. Alberto Nespoli</p><p class="coverfoot">Materiale di lavoro ad uso professionale · 1 ottobre 2026</p></section>'''

def build(kind):
 text = (ROOT / f'{kind}.md').read_text(encoding='utf-8')
 parts = re.split(r'^<!-- PAGE (.*?) -->\s*$', text, flags=re.M)
 if parts[0].strip(): raise ValueError('Testo fuori dalle pagine')
 sections=[]; toc=[]; ids=[]
 for meta, body in zip(parts[1::2], parts[2::2]):
  ident, running = meta.split('|',1)
  if ident in ids: raise ValueError('ID duplicato '+ident)
  ids.append(ident)
  body = body.replace('<div class="simple">', '<div class="simple" markdown="1">')
  html = markdown2.markdown(body, extras=['tables', 'break-on-newline', 'markdown-in-html'])
  def lines(match):
   cls=match[1]; count=4 if 'four' in cls else 3 if 'three' in cls else 1 if 'one' in cls else 2
   return '<div class="'+cls+'">'+('<span class="rule"></span>'*count)+'</div>'
  html=re.sub(r'<div class="(lines[^"]*)"></div>',lines,html)
  sections.append(f'<section class="page" id="{ident}"><div class="running">{running}</div>{html}</section>')
  first=re.search(r'^# (.+)$',body,re.M)
  if first and ident not in ['edizione', 'indice']:
   toc.append((ident,first[1]))
 toc_html='<div class="toc">'+''.join(f'<a href="#{ident}">{title}</a>' for ident,title in toc)+'</div>'
 html='<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="author" content="Dott. Alberto Nespoli"><title>'+NAMES[kind][:-4]+'</title><link rel="stylesheet" href="stile.css"></head><body class="'+kind+'">'+cover(kind)+''.join(sections).replace('[INDICE]',toc_html)+'</body></html>'
 (ROOT/f'{kind}.html').write_text(html,encoding='utf-8')
 for link in re.findall(r'href="#([^"]+)"',html):
  if link not in ids: raise ValueError('Rimando assente '+link)
 exe=ROOT/'strumenti/weasyprint/onedir/weasyprint/weasyprint.exe'
 output=DELIVERY/NAMES[kind];output.parent.mkdir(exist_ok=True)
 result=subprocess.run([str(exe),str(ROOT/f'{kind}.html'),str(output)],capture_output=True,text=True,encoding='utf-8')
 (ROOT/'qa'/f'weasyprint-{kind}.log').write_text(result.stdout+result.stderr,encoding='utf-8')
 if result.returncode: raise RuntimeError(result.stderr)
 print(kind, len(ids)+1, 'pagine progettate;', output.name)
 return {'documento':kind,'file':str(output),'pagine_progettate':len(ids)+1,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'sezioni':ids}

if __name__=='__main__':
 kinds=sys.argv[1:] or list(NAMES)
 results=[build(kind) for kind in kinds]
 (ROOT/'qa/generazione.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')

