"""Registra la revisione dichiarata dopo l'ispezione effettiva delle pagine."""
import sys,hashlib
from produci import MAINT,ROOT,load,write_json
batch=sys.argv[1];note=sys.argv[2]
f=MAINT/'verifiche'/(batch+'.json');report=load(f,None)
if not report or report['issues']:raise SystemExit('Rapporto assente o problemi aperti')
for r in report['files']:
    for key,hashkey in [('pdf','sha256'),('source','source_sha256')]:
        if hashlib.sha256((ROOT/r[key]).read_bytes()).hexdigest()!=r[hashkey]:raise SystemExit('File cambiato dopo il controllo: '+r[key])
report['visual_review']='eseguita su tutte le pagine del lotto, montaggi in scala di grigi';report['review_note']=note
write_json(f,report)
rfile=MAINT/'produzione/registrazioni'/(batch+'.json');rows=load(rfile,[])
for r in rows:r['status']='pronto'
write_json(rfile,rows)
statefile=MAINT/'stato.json';state=load(statefile,{})
state['completed_batches']=list(dict.fromkeys(state.get('completed_batches',[])+[batch]));state['phase']='3' if any(x.startswith('L0') for x in state['completed_batches']) else '2';state['status']='produzione e controllo per lotti in corso';write_json(statefile,state)
print(batch,': revisione registrata,',len(rows),'risorse pronte')
