from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parent;C=R.parent/'tappa-c';P=R.parent.parent
def page(i,run,title,body):return f'<!-- PAGE {i}|{run} -->\n{title}\n\n{body}\n\n'
def chunks(t):return {re.match(r'<!-- PAGE ([^|]+)',c)[1]:c for c in re.split(r'(?=^<!-- PAGE )',t,flags=re.M) if c.strip()}
mapping=json.loads((R/'fonti-schede.json').read_text(encoding='utf-8'))
allrecords={d['id']:d for v in mapping.values() for d in v}
selected={32:'SCH-MAP-11',33:'R1-53',34:'R1-41',35:'SCH-AUT-04',36:'R2-11',37:'SCH-AUT-05',38:'SCH-MET-07',39:'R3-3-5',40:'R2-26',41:'SCH-MAP-09',42:'R3-5-1',43:'R3-3-5',44:'R3-6-6',45:'R3-7-4',46:'R2-10',47:'R3-8-6',48:'R3-9-5',49:'R3-LINGUE',50:'LAB-ENG01-T'}
registry=json.loads((C/'registro-citazioni-s.json').read_text(encoding='utf-8'))
data=json.loads((C/'strategie.json').read_text(encoding='utf-8'))
def citation(n):
 d=allrecords[selected[n]];p=P/d['file'];lo,hi=d['riga_inizio'],d['riga_fine'];assert 0<lo<=hi<=len(p.read_text(encoding='utf-8').split('\n'))
 registry.append({'scheda':f'S{n}','id':d['id'],'file':d['file'],'righe':[lo,hi],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'base':'proposta locale criticamente riscritta; esempi originali'})
 label='Schedario' if d['id'].startswith('SCH-') else 'Laboratorio' if d['id'].startswith('LAB-') else d['id'].split('-')[0]
 return f'{label}, «{d["titolo"]}», righe {lo}–{hi} del testo locale. Esempi e varianti originali; limiti e correzioni editoriali nella nota critica e nei riferimenti D.'
def strategies():
 out='';intros=chunks((R/'strategie-introduzioni.md').read_text(encoding='utf-8'))
 for file in sorted(R.glob('strategie-*.txt')):
  for raw in re.split(r'\n\s*\n(?=S\d+\|)',file.read_text(encoding='utf-8').strip()):
   lines=raw.split('\n');code,title,summary=lines[0].split('|',2);n=int(code[1:]);d={s.split(': ',1)[0]:s.split(': ',1)[1] for s in lines[1:] if ': ' in s};assert len(d)==12
   chapter=21 if n<=33 else 22 if n<=37 else 23 if n<=40 else 24
   if n in [32,34,38,41]:
    out+=intros[f'cap{chapter}']
    if n==38:out+=intros['strumenti-lingue']
   extra=[r['id'].replace('SCH-','Schedario ').replace('LAB-','Laboratorio ') for r in mapping[code] if r['id'].startswith(('SCH-','LAB-'))][:2]
   assert extra,code
   ready='**Materiali pronti facoltativi:** '+', '.join(extra)+'. Controlla pertinenza e cautele delle fonti; il procedimento qui è autonomo.\n\n'
   body=f'**{summary}.** Durata orientativa.\n\n'+ready+'## A che cosa serve\n\n'+d['SCOPO']+'\n\n## Insegna in quattro tempi\n\n'
   for k,label in [('MODELLO','Esempio commentato'),('GUIDA','Traccia guidata'),('PERSONALE','Costruzione personale'),('NUOVO','Compito nuovo e trasferimento')]:body+=f'**{label}.** {d[k]}\n\n'
   body+='**Esempio disciplinare.** '+d['ESEMPIO'];body=re.sub(r'«([^»]+)»',r'*«\1»*',body);body=re.sub(r'“([^”]+)”',r'*“\1”*',body)
   out+=page(code.lower(),f'{chapter} · {code} · Procedura',f'# {code} · {title}',body)
   body=''
   for k,label in [('ETÀ','Età: modifica il carico, conserva lo scopo'),('PROFILI','Profili: ipotesi di accessibilità'),('LIVELLI','Quattro livelli descrittivi'),('ERRORI','Errori da evitare'),('AGGANCIO','Agganci DNA-V e consapevolezza')]:body+=f'## {label}\n\n{d[k]}\n\n'
   body+='**Nota critica.** '+d['NOTA']+'\n\n<div class="source">'+citation(n)+'</div>'
   out+=page(code.lower()+'-uso',f'{chapter} · {code} · Adattare e verificare',f'## {code} · Uso e limiti',body)
   data.append({'codice':code,'titolo':title,'campi':d,'materiali_pronti':extra})
 return out
def prepare():
 t=(C/'manuale.md').read_text(encoding='utf-8');parts=chunks(t)
 intro=parts['edizione'].replace('B–C','B–D').replace('Questa edizione cumulativa conserva il blocco B e aggiunge le fasi 2–3, le strategie **S1–S31**, le tecniche **D4, D6–D7 e D11–D18** e le tappe **C1–C5**. Restano disponibili D1–D3. I salti di numerazione seguono l’indice approvato; i blocchi successivi non sono ancora redatti.','Questa edizione cumulativa conserva B–C e completa il percorso fino alla fase 5, il sostegno intensificato, **S1–S50**, le **24 tecniche D previste** e **C1–C7**. Profili, valutazione estesa, genitori/scuola, appendici e bussola definitiva restano nella tappa E; la revisione indipendente e finale nella tappa F. I salti dei numeri D sono intenzionali.').replace('con i fogli pertinenti alle fasi 1–3','con tutte le Schede 1–23 e sette varianti concrete').replace('con Strumenti 1–6','con Strumenti 1–7').replace('tappa C','tappa D')
 t=intro+t[len(parts['edizione']):]
 t=t.replace('<!-- PAGE cap15|',(R/'fasi.md').read_text(encoding='utf-8')+'<!-- PAGE cap15|')
 t=t.replace('<!-- PAGE cap25|',strategies()+'<!-- PAGE cap25|')
 t=t.replace('<!-- PAGE cap33|',(R/'tecniche.md').read_text(encoding='utf-8')+'<!-- PAGE cap33|')
 t=t.replace('<!-- PAGE riferimenti|',(R/'consapevolezza.md').read_text(encoding='utf-8')+'<!-- PAGE riferimenti|')
 t=t.replace('Gentilezza e ROAD arriveranno nei blocchi successivi.','Gentilezza e ROAD sono descritte in [D25](#d25) e [D22](#d22).')
 t=t.replace('[C3](#c3); S38–S40 in seguito','[C3](#c3); [S38–S40](#s38)').replace('disponibili nei blocchi B–C','disponibili nei blocchi B–D').replace('Gli Strumenti 1–6 organizzano','Gli Strumenti 1–7 organizzano')
 t=t.replace('Il blocco successivo svilupperà preparazione alle prove e ulteriori strumenti. Questa consegna si ferma alla revisione delle fasi 2–3: non equivale a conclusione del percorso né a validazione sul campo.','La preparazione alle prove prosegue nella [fase 4](#cap11), con ulteriori strumenti. Il passaggio non equivale a validazione sul campo del percorso.')
 t=t.replace('Se l’esposizione pubblica è il problema centrale, rinvia al lavoro specifico del blocco successivo.','Se l’esposizione pubblica è il problema centrale, consulta [S33](#s33) e valuta l’appropriatezza con il [capitolo 13](#cap13).')
 t=t.replace('La Scheda 13 conclusiva e le tappe C6–C7 saranno sviluppate in seguito: non anticipare un profilo definitivo.','La Scheda 13 e [C6–C7](#c6) raccolgono progressivamente risultati e scelte: non anticipare un profilo definitivo.')
 t=t.replace('I rimandi ancora da sviluppare sono indicati; la bussola completa arriverà nella tappa E.','Il repertorio S/D/C è disponibile; la bussola completa arriverà nella tappa E.')
 t=t.replace('L’aggancio futuro è S4 per l’avvio, S26 per il recupero, S34 per preparare una prova. In questo blocco usa la piccola vittoria.','Gli agganci sono [S4](#s4) per l’avvio, [S26](#s26) per il recupero e [S34](#s34) per preparare una prova. Nella fase iniziale puoi usare la piccola vittoria.')
 t=t.replace('l’aggancio futuro è S4 per l’avvio, S26 per il recupero, S34 per preparare una prova. In questo blocco usa la', 'gli agganci sono [S4](#s4) per l’avvio, [S26](#s26) per il recupero e [S34](#s34) per preparare una prova. Nella fase iniziale usa la')
 t=t.replace('Le tappe C1–C5 aiutano a descrivere', 'Le tappe C1–C7 aiutano a descrivere')
 t+=(R/'fonti-d.md').read_text(encoding='utf-8')
 (R/'manuale.md').write_text(t,encoding='utf-8')
 for name,x in [('strategie.json',data),('registro-citazioni-s.json',registry)]: (R/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
 dr=[]
 for n in [20,21,22,23,25,26]:
  d=allrecords[f'COMP-T{n}'];p=P/d['file'];dr.append({'scheda':f'D{n}','file':d['file'],'righe':[d['riga_inizio'],d['riga_fine']],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 (R/'registro-citazioni-d.json').write_text(json.dumps(dr,ensure_ascii=False,indent=2),encoding='utf-8')
 print('Preparato: 50 strategie cumulative, 19 nuove; D20–D30 selezionate, C6–C7')
if __name__=='__main__':prepare()
