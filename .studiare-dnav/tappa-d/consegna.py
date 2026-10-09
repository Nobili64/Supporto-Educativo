from pathlib import Path
import json,shutil,hashlib
from costruisci import ROOT as R,PROJECT as P,DELIVERY,NAMES
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
qa=json.loads((R/'qa/esito-controlli.json').read_text(encoding='utf-8'))
assert qa['esito']=='PASS' and len(qa['controlli'])==65 and all(c['esito'] for c in qa['controlli'])
for kind,d in qa['documenti'].items():assert sha(DELIVERY/NAMES[kind])==d['sha256']
pop=json.loads((R/'qa/poppler/registro.json').read_text(encoding='utf-8'))
assert len(pop)==14
for x in pop:assert x['pdf_sha256']==qa['documenti'][x['documento']]['sha256'] and Path(x['immagine']).exists()
src=DELIVERY/'Sorgenti';src.mkdir(exist_ok=True)
names=['manuale.md','ragazzo.md','clinico.md','manuale.html','ragazzo.html','clinico.html','stile.css','fasi.md','tecniche.md','consapevolezza.md','strategie-introduzioni.md','strategie-32-40.txt','strategie-41-50.txt','fonti-d.md','strategie.json','fonti-schede.json','registro-citazioni-s.json','registro-citazioni-d.json']
for name in names:
 shutil.copy2(R/name,src/name)
 assert sha(R/name)==sha(src/name)
shutil.copytree(R/'font',src/'font',dirs_exist_ok=True)
for p in (R/'font').rglob('*'):
 if p.is_file():assert sha(p)==sha(src/'font'/p.relative_to(R/'font'))
shutil.copy2(R/'qa/esito-controlli.json',DELIVERY/'esito-controlli.json')
state={'data':'2026-10-02','tappa':'D','stato':'consegnata_per_revisione_utente','autorizzazione':'Approvo C: procedi con D','pagine':{k:v['pagine'] for k,v in qa['documenti'].items()},'strategie_nuove':list(range(32,51)),'tecniche_nuove':[20,21,22,23,25,26,27,28,29,30],'consapevolezza_nuova':[6,7],'controlli_automatici':{'esito':'PASS','numero':65},'controllo_visivo':'290 pagine in tavole complete; ricontrollo finale delle pagine modificate; 14 pagine finali anche con Poppler','fonti_originali_invariate':158,'file_consegna_B_invariati':27,'file_consegna_C_invariati':40,'revisione_F':'non effettuata','stampa_fisica':'non effettuata','prova_in_seduta':'non documentata','prossima_tappa':'Revisione utente D prima di E; obiettivo complessivo non completo'}
save(R/'stato.json',state);save(DELIVERY/'stato-consegna.json',state)
save(R.parent/'attesa-revisione-d.json',{'data':'2026-10-02','stato':'in_attesa_revisione_utente','tappa_consegnata':'D','tappa_successiva':'E','approvazione_D_ricevuta':False,'turni_consecutivi_senza_progressi':0,'motivo':'Controllo utente previsto dal piano; E non autorizzata','consegna':str(DELIVERY)})
files=[{'file':p.relative_to(DELIVERY).as_posix(),'byte':p.stat().st_size,'sha256':sha(p)} for p in sorted(DELIVERY.rglob('*')) if p.is_file() and p.name!='manifesto-consegna.json']
save(DELIVERY/'manifesto-consegna.json',{'data':'2026-10-02','esclusione':'manifesto-consegna.json stesso','file':files})
assert all(sha(DELIVERY/x['file'])==x['sha256'] for x in files)
print('Consegna D verificata:',len(files),'file; 3 PDF; 65 controlli; 14 pagine Poppler; fonti e copie coerenti.')
