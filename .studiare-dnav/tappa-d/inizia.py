from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;P=R.parent.parent;C=R.parent/'tappa-c'
(R/'qa').mkdir(exist_ok=True)
def save(name,x): (R/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
snapshot=[{'file':p.relative_to(P).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (P/'Studiare con il DNA-V - blocco C').rglob('*') if p.is_file()]
if not (R/'impronte-blocco-c.json').exists():save('impronte-blocco-c.json',snapshot)
save('stato.json',{'fase':'D','stato':'in redazione','autorizzazione':'Approvo C: procedi con D','data':'2026-10-01','arresto':'Consegna D per revisione; E non autorizzata'})
(R.parent/'attesa-revisione-c.json').write_text(json.dumps({'stato':'risolta','approvazione':'Approvo C: procedi con D','data':'2026-10-01'},ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copytree(C/'font',R/'font',dirs_exist_ok=True)
shutil.copy2(C/'stile.css',R/'stile.css')
shutil.copy2(C/'impronte-blocco-b.json',R/'impronte-blocco-b.json')
builder=(C/'costruisci.py').read_text(encoding='utf-8').replace('blocco C','blocco D').replace('B-C','B-D').replace('B–C','B–D').replace('Avvio, fondamenta, elaborazione e memoria','Dal primo incontro al mantenimento').replace('Avvio e monitoraggio delle fasi 1–3','Osservazione, monitoraggio e restituzione').replace('Fondamenti, avvio e prime strategie','Percorso, strategie e abilità complete')
(R/'costruisci.py').write_text(builder,encoding='utf-8')
mapping=json.loads((R.parent/'tappa-a-consegna/mappatura.json').read_text(encoding='utf-8'))
codes=[f'S{i}' for i in range(32,51)]+[f'D{i}' for i in [20,21,22,23,25,26,27,28,29,30]]+['C6','C7']
save('fonti-schede.json',{c:[r for r in mapping if c in r['destinazioni']] for c in codes})
print('D inizializzata; C fotografata:',len(snapshot),'file')
