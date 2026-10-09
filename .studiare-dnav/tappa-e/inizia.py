from pathlib import Path
import json,hashlib,shutil,collections
R=Path(__file__).resolve().parent;P=R.parent.parent;D=R.parent/'tappa-d'
(R/'qa').mkdir(exist_ok=True)
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
assert not (R/'stato.json').exists(),'Inizializzazione già eseguita'
save(R/'impronte-blocco-d.json',[{'file':p.relative_to(P).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (P/'Studiare con il DNA-V - blocco D').rglob('*') if p.is_file()])
save(R/'stato.json',{'fase':'E','stato':'in redazione','data':'2026-10-02','autorizzazione':'Approvo D: procedi con E','arresto':'Consegna E per revisione utente; F successiva'})
save(R.parent/'attesa-revisione-d.json',{'stato':'risolta','data':'2026-10-02','approvazione':'Approvo D: procedi con E'})
shutil.copytree(D/'font',R/'font',dirs_exist_ok=True)
for name in ['stile.css','ragazzo.md','clinico.md','strategie.json','registro-citazioni-s.json','registro-citazioni-d.json','impronte-blocco-b.json','impronte-blocco-c.json']:
 shutil.copy2(D/name,R/name)
t=(D/'costruisci.py').read_text(encoding='utf-8').replace('blocco D','blocco E').replace('B-D','B-E').replace('B–D','B–E').replace('Percorso, strategie e abilità complete','Testo completo per revisione')
(R/'costruisci.py').write_text(t,encoding='utf-8')
t=(D/'verifica.py').read_text(encoding='utf-8')
(R/'verifica.py').write_text(t,encoding='utf-8')
mapping=json.loads((R.parent/'tappa-a-consegna/mappatura.json').read_text(encoding='utf-8'))
save(R/'mappatura-originale-a.json',mapping)
print('Destinazioni',dict(collections.Counter(x for r in mapping for x in r['destinazioni'])))
print('Decisioni',dict(collections.Counter(r['decisione'] for r in mapping)))
