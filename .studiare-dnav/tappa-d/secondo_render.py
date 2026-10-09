from pathlib import Path
import subprocess,json,hashlib
from costruisci import ROOT as R,DELIVERY,NAMES
exe=Path(r'C:\Users\megan\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe')
out=R/'qa/poppler';out.mkdir(exist_ok=True)
pages={'manuale':[49,137,159,163,167,203,217,224],'ragazzo':[17,26,37,40],'clinico':[17,18]}
results=[]
for kind,ns in pages.items():
 p=DELIVERY/NAMES[kind]
 for n in ns:
  prefix=out/f'{kind}-{n:03d}'
  subprocess.run([str(exe),'-f',str(n),'-l',str(n),'-r','120','-singlefile','-png',str(p),str(prefix)],check=True,capture_output=True)
  results.append({'documento':kind,'pagina':n,'pdf_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'immagine':str(prefix)+'.png'})
(out/'registro.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Secondo rendering:',len(results),'pagine')
