from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parent;B=R.parent/'tappa-b';P=R.parent.parent
def page(i,run,title,body):return f'<!-- PAGE {i}|{run} -->\n{title}\n\n{body}\n\n'
mapping=json.loads((R/'fonti-schede.json').read_text(encoding='utf-8'))
selected={1:'SCH-MET-12',2:'R1-12',3:'R1-13',4:'R1-4',5:'R1-15',6:'R1-18',7:'R1-14',8:'R1-21',9:'R2-1',10:'R1-25',11:'R1-24',12:'R3-1-1',13:'R1-27',14:'R1-28',15:'R1-30',16:'R1-29',17:'R1-33',18:'R2-MAP1',19:'R2-MAP3',20:'R2-MAP1',21:'SCH-MAP-08',22:'SCH-MAP-10',23:'SCH-MAP-09',24:'R3-TABLET',25:'R2-MAP7',26:'R2-6',27:'R1-40',28:'SCH-MET-04',29:'R1-37',30:'R1-39',31:'R2-14'}
allrecords={r['id']:r for v in mapping.values() for r in v}
registry=[]
def citation(n):
 rec=allrecords[selected[n]];path=P/rec['file'];a=path.read_text(encoding='utf-8').split('\n')
 lo,hi=rec['riga_inizio'],rec['riga_fine']
 assert lo>0 and hi<=len(a),(n,lo,hi,len(a))
 file=rec['file'];label='R1' if '/1 Metodo' in file else 'R2' if '/2 Metacognizione' in file else 'R3' if '/3 Supporto' in file else 'Schedario'
 registry.append({'scheda':f'S{n}','id':rec['id'],'file':file,'righe':[lo,hi],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'base':'proposta locale, riscritta criticamente'})
 return f'{label}, «{rec["titolo"]}», righe {lo}–{hi}. Procedura, esempi e varianti editoriali originali; evidenze e limiti nella nota critica e nei riferimenti.'
def strategies():
 result='';data=[]
 for file in sorted(R.glob('strategie-*.txt')):
  for chunk in re.split(r'\n\s*\n(?=S\d+\|)',file.read_text(encoding='utf-8').strip()):
   lines=chunk.split('\n');code,title,summary=lines[0].split('|',2);n=int(code[1:]);d={a.split(': ',1)[0]:a.split(': ',1)[1] for a in lines[1:] if ': ' in a}
   assert len(d)==12,(code,d.keys())
   chapter=15 if n<=7 else 16 if n==8 else 17 if n<=13 else 18 if n<=17 else 19 if n<=25 else 20
   extra=[r['id'].replace('SCH-','Schedario ').replace('LAB-','Laboratorio ') for r in mapping[code] if r['id'].startswith(('SCH-','LAB-'))][:2]
   ready='**Materiali pronti facoltativi:** '+', '.join(extra)+'. Controlla pertinenza e cautele delle fonti; il procedimento qui è autonomo.\n\n' if extra else ''
   body=f'**{summary}.** Durata orientativa.\n\n'+ready+'## A che cosa serve\n\n'+d['SCOPO']+'\n\n## Insegna in quattro tempi\n\n'
   labels=[('MODELLO','Esempio commentato'),('GUIDA','Traccia guidata'),('PERSONALE','Costruzione personale'),('NUOVO','Compito nuovo e trasferimento')]
   for key,label in labels:body+=f'**{label}.** {d[key]}\n\n'
   body+='**Esempio disciplinare.** '+d['ESEMPIO']
   body=re.sub(r'«([^»]+)»',r'*«\1»*',body)
   result+=page(code.lower(),f'{chapter} · {code} · Procedura',f'# {code} · {title}',body)
   body='## Età: modifica il carico, conserva lo scopo\n\n'+d['ETÀ']+'\n\n## Profili: ipotesi di accessibilità\n\n'+d['PROFILI']+'\n\n## Quattro livelli descrittivi\n\n'+d['LIVELLI']+'\n\n## Errori da evitare\n\n'+d['ERRORI']+'\n\n## Agganci DNA-V e consapevolezza\n\n'+d['AGGANCIO']+'\n\n**Nota critica.** '+d['NOTA']+f'\n\n<div class="source">{citation(n)}</div>'
   result+=page(code.lower()+'-uso',f'{chapter} · {code} · Adattare e verificare',f'## {code} · Uso e limiti',body)
   if n in [19,21,28]:
    figures=(R/'figure.md').read_text(encoding='utf-8');chunks=re.split(r'(?=^<!-- PAGE )',figures,flags=re.M)
    result+=''.join(c for c in chunks if c.startswith(f'<!-- PAGE s{n}-figura|'))
   data.append({'codice':code,'titolo':title,'campi':d,'materiali_pronti':extra})
 (R/'strategie.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 (R/'registro-citazioni-s.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
 return result
def prepare():
 t=(B/'manuale.md').read_text(encoding='utf-8')
 a=t.index('<!-- PAGE cap1|')
 intro=page('edizione','Edizione provvisoria · blocchi B–C','# Che cosa contiene questa edizione',
 'Il manuale intreccia **metodo di studio, abilità DNA-V e consapevolezza** nel lavoro individuale con ragazzi e ragazze di 8–16 anni con DSA. Si rivolge al clinico entro competenze e mandato concordati.\n\n'
 'Questa edizione cumulativa conserva il blocco B e aggiunge le fasi 2–3, le strategie **S1–S31**, le tecniche **D4, D6–D7 e D11–D18** e le tappe **C1–C5**. Restano disponibili D1–D3. I salti di numerazione seguono l’indice approvato; i blocchi successivi non sono ancora redatti.\n\n'
 'Tieni accanto i due allegati A4: **Schede di lavoro**, con i fogli pertinenti alle fasi 1–3, e **Strumenti per il clinico**, con Strumenti 1–6. Gli indici riportano le pagine delle singole versioni. Materiali e procedure necessari alle attività di questa edizione sono descritti qui; i rimandi agli archivi locali sono facoltativi.\n\n'
 '## Come leggere le fonti\n\n'
 '**Evidenza scientifica:** studi e revisioni, senza validazione automatica del percorso. **Indicazione istituzionale:** norme e linee guida, distinte da prove di efficacia. **Proposta da manuale:** procedure descritte nelle fonti. **Adattamento editoriale:** esempi, schede e varianti riscritti per questo progetto, da verificare nella pratica.\n\n'
 'Le frasi in corsivo sono esempi originali. Nessun caso reale o item di test proprietario è riprodotto. Il modello DNA-V è di Louise L. Hayes e Joseph Ciarrochi; non si implica affiliazione o approvazione degli autori.\n\n'
 '<div class="box"><strong>Stato.</strong> Bozza per la revisione della tappa C. La prova in seduta del blocco B non è documentata in questa consegna. Revisione indipendente complessiva nella tappa F; prova fisica di stampa e verifica sul campo ancora da effettuare. Non è un protocollo validato.</div>')
 t=intro+page('indice','Consultazione','# Indice','[INDICE]')+t[a:]
 insert=(R/'fasi.md').read_text(encoding='utf-8')+strategies()
 t=t.replace('<!-- PAGE cap25|',insert+'<!-- PAGE cap25|')
 insert=(R/'tecniche.md').read_text(encoding='utf-8')+(R/'consapevolezza.md').read_text(encoding='utf-8')
 t=t.replace('<!-- PAGE riferimenti|',insert+'<!-- PAGE riferimenti|')
 t=t.replace('C1 e C4–C5 saranno sviluppate nel blocco C.','C1 e C4–C5 sono sviluppate in questa edizione.')
 t=t.replace('Riferimenti del blocco B','Riferimenti · base del blocco B')
 t=t.replace('Questa bussola offre una **prima azione già descritta nel blocco B**. La colonna finale indica le future schede estese, in preparazione: non sono necessarie per svolgere l’azione proposta.','Questa bussola provvisoria collega le prime azioni alle schede disponibili nei blocchi B–C. I rimandi ancora da sviluppare sono indicati; la bussola completa arriverà nella tappa E.')
 t=t.replace('Sviluppo successivo','Schede / seguito').replace('Prima azione nel blocco B','Prima azione disponibile')
 t=t.replace('| S38–S40, C3 |','| [C3](#c3); S38–S40 in seguito |')
 for label,target in [('S4, S8','s4'),('S10–S13','s10'),('S14–S17','s14'),('S26–S27','s26'),('S18–S25','s18')]:
  t=t.replace('| '+label+' |','| ['+label+'](#'+target+') |')
 t=t.replace('Le tecniche ulteriori per Consulente, Osservatore, gentilezza, AND e ROAD saranno sviluppate nei blocchi successivi. Qui non sono prescritte in forma abbreviata.','Sono ora disponibili [D6–D7](#d6), [D11–D15](#d11) e [D16–D18](#d16), con scelta, adattamenti e limiti. Gentilezza e ROAD arriveranno nei blocchi successivi. La bussola non sostituisce la lettura della procedura.')
 t=t.replace('Gli Strumenti 1–4 servono a organizzare il ragionamento clinico; Schede 1 e 14 sostengono la conversazione e la scelta del ragazzo.','Gli Strumenti 1–6 organizzano osservazioni e ragionamento clinico; le Schede A4 sostengono conversazione, prova e scelta del ragazzo.')

 t+=(R/'fonti-c.md').read_text(encoding='utf-8')
 (R/'manuale.md').write_text(t,encoding='utf-8')
if __name__=='__main__':prepare()
