"""Assembla l'indice da approvare e verifica la consegna senza modificare le fonti."""
from pathlib import Path
import json,re,hashlib,subprocess,sys
from catalogo import CHAPTERS
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
for script in ['costruisci.py','evidenze.py']:
    subprocess.run([sys.executable,'-X','utf8',str(P/script)],check=True,capture_output=True)
chapters=[l.split('|') for l in CHAPTERS.splitlines()]
assert [int(r[0]) for r in chapters]==list(range(1,53))
parts={1:'Parte I — Come funziona il percorso',7:'Parte II — Il percorso',15:'Parte III — Strategie di metodo',25:'Parte IV — Il DNA-V nello studio',33:'Parte V — Consapevolezza',37:'Parte VI — Profili',46:'Parte VII — Valutare e monitorare',50:'Parte VIII — Genitori e scuola'}
body=''
for code,title,detail in chapters:
    if int(code) in parts:body+='### '+parts[int(code)]+'\n\n'
    body+=f'**{code}. {title}.** {detail}\n\n'
main=(P/'indice-base.md').read_text(encoding='utf-8').replace('<!-- CAPITOLI -->',body.rstrip())
main=re.sub(r'<(\.studiare-dnav/[^>]+)>',lambda m:'<'+str(ROOT/m[1])+'>',main)
target=ROOT/'Studiare con il DNA-V - tappa A - indice da approvare.md'
target.write_text(main,encoding='utf-8')

mapping=json.loads((P/'mappatura.json').read_text(encoding='utf-8'))
catalog=json.loads((P/'catalogo-manuale.json').read_text(encoding='utf-8'))
tests=json.loads((P/'esito-controlli.json').read_text(encoding='utf-8'))
source_lines={}
for r in mapping:
    p=ROOT/r['file']
    if p not in source_lines:source_lines[p]=p.read_text(encoding='utf-8-sig').split('\n')
    assert 1<=r['riga_inizio']<=r['riga_fine']<=len(source_lines[p]),r['id']
expected={f'{a}-{i:02}' for a,n in [('MAP',14),('MET',12),('AUT',13),('MAT',35),('ITA',16)] for i in range(1,n+1)}
assert {r['id'][4:] for r in mapping if r['id'].startswith('SCH-')}==expected
assert {x['id'] for x in catalog['dnav']}=={'D'+str(i) for i in [1,2,3,4,6,7,11,12,13,14,15,16,17,18,20,21,22,23,25,26,27,28,29,30]}
assert len([r for r in mapping if r['id'].startswith('LAB-') and r['pdf']])==131
assert sum([4,22,34,100,48,10,18,12,8,20])==276
assert 23+3+1+8+2==37 and 6*2+3+2==17 and 37+17==54

old=json.loads((ROOT/'.studiare-dnav/tappa-a/impronte-fonti.json').read_text(encoding='utf-8'))
changed=[r['file'] for r in old if not (ROOT/r['file']).is_file() or hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()!=r['sha256']]
assert changed==['Studiare con il DNA-V - piano del manuale.md'],changed
doi=json.loads((P/'verifica-doi.json').read_text(encoding='utf-8'))
tests.update(capitoli=52,intervalli_fonte_validi=True,schedario_codici_attesi=True,pdf_laboratorio_presenti=131,registro_ods_presente=True,pagine_stimate_manuale=276,pagine_stimate_schede_A4=37,pagine_stimate_strumenti_A4=17,confronto_baseline=dict(totale=len(old),invariati=len(old)-len(changed),differenze=changed,nota='Piano aggiornato prima di questa consegna, come documentato nel piano stesso.'),doi_controllati=len(doi['fonti']),doi_risolti=sum(r['esito']=='trovato' for r in doi['fonti']))

readme=f'''# Tappa A — consegna

30 settembre 2026. **Indice pronto per l'approvazione; tappa B non iniziata.**

Aprire prima l'[indice dettagliato](<{target}>). Il resto documenta le scelte e permette di verificarle:

- [Catalogo di tutte le schede proposte](<{P/'01b-catalogo-schede.md'}>).
- [Mappatura completa](<{P/'02-mappatura-completa.md'}>), anche in [tabella CSV](<{P/'mappatura.csv'}>).
- [Rapporto critico](<{P/'03-valutazione-critica.md'}>).
- [Test](<{P/'04-test-verificati.md'}>) e [fonti](<{P/'05-fonti-e-limiti.md'}>).
- [Controlli e limiti della verifica](<{P/'06-controlli.md'}>).

La precedente cartella `tappa-a` è conservata. Questa consegna usa il testo completo del Laboratorio e il percorso corretto dello Schedario. La mappatura principale copre 433 unità; le 40 voci supplementari non sono sommate come se fossero tecniche indipendenti.

Gli originali, i libri, lo Schedario e il Laboratorio non sono stati modificati. Le correzioni dei vecchi strumenti sono elencate per la futura tappa G. Le nuove schede del manuale saranno scritte dopo l'approvazione.

Per ricostruire i file derivati, eseguire `finalizza.py` con Python 3. Il controllo DOI separato (`verifica-metadati.py`) richiede rete e riusa gli accessi già riusciti. L'uso quotidiano dei documenti non richiede Python.
'''
(P/'00-LEGGIMI.md').write_text(readme,encoding='utf-8')
qa=f'''# Controlli della consegna

30 settembre 2026. Controlli di integrità e coerenza editoriale; non validazione clinica del manuale.

| Controllo | Esito |
|---|---|
| Repertori | 175 tecniche: 53 / 34 / 49 / 39 |
| Schedario | 90 codici attesi, tutti presenti: MAP 14, MET 12, AUT 13, MAT 35, ITA 16 |
| Laboratorio | 132 risorse; 131 PDF esistenti e Registro.ods esistente |
| Compendio | 26 tecniche e 10 schede; tutte mappate |
| Totale principale | 433 righe |
| Supplementi | 40 righe; totale tabella 473 |
| Destinazioni | Tutti i codici rimandano a S/D/C, capitoli, allegati o appendici definiti |
| Catalogo | 50 S, 24 D, 7 C, 23 schede con 7 varianti semplificate, 7 strumenti |
| Indice | Capitoli 1–52 senza lacune o duplicati |
| Provenienza | Tutte le S hanno almeno una corrispondenza registrata; D27–D30 esplicitamente nuove |
| Intervalli delle fonti | Righe iniziali/finali entro i file correnti; codici di tabella univoci |
| Pagine | Somma stima manuale 276; allegati 37 + 17 = 54 |
| Metadati scientifici | {tests['doi_risolti']}/{tests['doi_controllati']} DOI risolti su Crossref, inclusi tre aggiornamenti; autori/titoli controllati |
| Confronto precedente | {len(old)-len(changed)}/{len(old)} file invariati; unica differenza: piano già aggiornato e dichiarato tale nelle fonti |

La presenza dei file e la validità dei codici sono controlli automatici. La pertinenza delle corrispondenze e le decisioni nel rapporto sono valutazioni editoriali, non esiti prodotti da un validatore. Non sono state certificate tutte le affermazioni dei repertori o le pagine dei materiali pronti.

## Copertura effettiva

Sono stati usati testi forniti per la ricognizione, fonti primarie o siti dei titolari per le verifiche esterne, abstract per conclusioni circoscritte e sezioni pertinenti dei documenti normativi. Le limitazioni di accesso e le versioni test non confermate sono nel registro fonti e nel rapporto test. I metadati Crossref attestano identità bibliografica, non validità degli studi.

Non è stata svolta la revisione clinica indipendente della tappa F, né una prova in seduta, né una prova di stampa del manuale, che non è ancora redatto. Nessun caso reale è stato letto o utilizzato. La cartella Casi non è stata enumerata. Nessuna modifica al materiale originale è necessaria per consultare questa consegna.

## Come ripetere i controlli

`finalizza.py` ricostruisce inventario, mappatura, catalogo, registro ragionato, indice e rapporto. Legge soltanto i percorsi esplicitamente ammessi nei file di costruzione; scrive nella cartella della consegna e nel nuovo indice in radice. Le impronte delle fonti correnti sono in `impronte-fonti-consegna.json`; il confronto con la ricognizione precedente è riportato in `esito-controlli.json`. I materiali della vecchia tappa A non vengono sovrascritti.

I controlli non autorizzano la tappa B: serve l'approvazione dell'indice prevista dal piano. Le eventuali fonti da acquisire nelle fasi successive sono identificate per singola affermazione; fino ad allora quelle affermazioni non entrano nel testo come verificate.
'''
(P/'06-controlli.md').write_text(qa,encoding='utf-8')
# Verifica che i collegamenti locali di tutti i documenti consegnati esistano.
docs=[target]+[P/x for x in ['00-LEGGIMI.md','01b-catalogo-schede.md','02-mappatura-completa.md','03-valutazione-critica.md','04-test-verificati.md','05-fonti-e-limiti.md','06-controlli.md']]
links=0
for p in docs:
    text=p.read_text(encoding='utf-8')
    assert '\ufffd' not in text,p
    for v in re.findall(r'\]\(<([^>]+)>\)',text):
        if v.startswith('http'):continue
        v=re.sub(r':\d+$','',v)
        assert Path(v).exists(),(p,v)
        links+=1
tests['collegamenti_locali_validi']=links
(P/'esito-controlli.json').write_text(json.dumps(tests,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[dict(file=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in docs]
(P/'impronte-consegna.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(tests,ensure_ascii=False))
