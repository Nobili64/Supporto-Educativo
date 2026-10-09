"""Ricostruisce gli allegati della sola tappa A; nessuna scrittura alle fonti.
Uso: python costruisci.py. Libreria standard; percorsi ammessi espliciti.
"""
from pathlib import Path
import json,re,hashlib,csv,html
from collections import Counter
from catalogo import S,D,C,SHEETS,SHEET_TARGETS,INSTRUMENTS,CHAPTERS
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
MAT=ROOT/'Studiare con il DNA-V - materiali per la redazione'
tracked=set(); rows=[]
def read(p):
    p=p.resolve(); assert 'Casi' not in p.parts
    tracked.add(p); return p.read_text(encoding='utf-8-sig')
def save(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def table(headers,data):
    def cell(x): return str(x).replace('|',' / ').replace('\n',' ')
    return '| '+' | '.join(headers)+' |\n|'+'|'.join('---' for _ in headers)+'|\n'+''.join('| '+' | '.join(cell(v) for v in row)+' |\n' for row in data)
def add(code,title,p,start,end,targets,decision='Integrare riscrivendo',note='',kind='principale',pdf=''):
    ts=targets.split(',') if isinstance(targets,str) else targets
    rows.append(dict(id=code,titolo=title,file=p.relative_to(ROOT).as_posix(),riga_inizio=start,riga_fine=end,destinazioni=ts,decisione=decision,nota=note,gruppo=kind,pdf=pdf))
def sections(p,pattern):
    lines=read(p).split('\n'); starts=[(i+1,m) for i,l in enumerate(lines) if (m:=re.match(pattern,l))]
    return lines,[(a,(starts[j+1][0]-1 if j+1<len(starts) else len(lines)),m) for j,(a,m) in enumerate(starts)]

# Corrispondenze decise editorialmente per ciascun codice, non inferite dal titolo.
r1=['C1,C5','C1,S38','C4,D17','S4,D21','D20','D1','S34','S38','C5,D16','S4','CAP6','S2','S3','S7','S5','S5','S6','S6','S5','S4','S8','S10','S10','S11','S10','S10','S13','S14','S16','S15','S15','S14,D6','S17','S20','S19,S26','S27','S29','S33','S30','S27','S34','S36','D4','D20,S3','S4','S4,D21','D14,S4','CAP4','D16,S5','S4,D21','D6,D12','S37,D18','D12,D22,S33']
r2=['S9','S10','S11','S11','S16,S18','S26','S15','S27','S3,S29','S46','S36,S46','S26,S36','S29','S31','S5','S47,D29','S47','S47,S48','S47','S46','S37','S8,S37','S41','S38,C5','CAP2','S40','S36,C5','C5','S5','D20','S2','D29,S38','S4','C2']
r3={1:['S12','S12,S33','S13','S12'],2:['S10','S11','S13','S13,S28','S8'],3:['S43','S43','S42','S43','S39,S43'],4:['S39','S42','S39,S42','S39,S40'],5:['S42','S42','S42','S42','S42'],6:['S44','S44','S44','S44','S44','S44'],7:['S37,S45','S45','S46','S45'],8:['S47','S47','S47','S47','S47','S47,S46'],9:['S48','S48','S48','S48','S48'],11:['S8','S40','S2','S3','CAP6,CAP42']}
r4={'P':['D30,STR6','D12','D12,S4','D15','D6','D4','S4','D21','D1','S34','D4,D17','S33'], 'D':['D6','D6','D7','D6','D12','D13','D14','S5','S35','D18,S37','S40,D26','S5'], 'A':['D18','D16,C5','D18,S37','D25','D25','D18','S4,D21','D11,D25','D16'], 'T':['S4','D14','D16','D12','D18','S26']}
repfiles=sorted((ROOT/'Assets (markdown)'/'Repertori skill piano intervento').glob('*.md'))
for p in repfiles:
    n=int(p.name[0]); lines=read(p).split('\n'); area=''; starts=[]
    for i,l in enumerate(lines,1):
        m=re.match(r'^## (\d+)\.',l)
        if m: area=m[1]
        pat=r'^#### (\d+)\. (.+)' if n==1 else r'^\*\*(\d+)\. (.+?)\*\*' if n==2 else r'^(\d+)\. \*\*(.+?)\*\*' if n==3 else r'^\*\*([PADT]\d+)\. (.+?)\*\*'
        m=re.match(pat,l)
        if m: starts.append((i,area,m[1],m[2].rstrip('.')))
    for j,(start,area,num,title) in enumerate(starts):
        end=starts[j+1][0]-1 if j+1<len(starts) else len(lines)
        for k in range(start,end):
            if lines[k].startswith('##'): end=k; break
        code=f'R{n}-'+(area+'-' if n==3 else '')+num
        target=r1[int(num)-1] if n==1 else r2[int(num)-1] if n==2 else r3[int(area)][int(num)-1] if n==3 else r4[num[0]][int(num[1:])-1]
        note='Conservare il rimando bibliografico nel repertorio; verificare la pagina del volume prima di una citazione nel manuale.'
        decision='Integrare riscrivendo'
        if code=='R1-48': decision='Escludere la procedura';note='Divieto paradossale di studiare: non proporre come intervento standard; usare avvio concordato e analisi della funzione (S4).'
        if code=='R1-45': note='La formula della procrastinazione è una metafora orientativa, non un’equazione predittiva validata del singolo ragazzo.'
        if code=='R1-51': decision='Riformulare';note='Non insegnare a eliminare pensieri: riconoscerli e tornare a un’azione scelta.'
        if code in ['R3-1-3','R3-3-4']: note='Solo supporto al compito e comprensione di parole; distinguere da trattamento riabilitativo della lettura o dell’ortografia.'
        if code=='R3-11-5': note='Gioco per osservare e provare strategie; nessuna promessa di generalizzazione automatica o riabilitazione delle funzioni esecutive.'
        if code in ['R4-P4','R4-T4']: decision='Variante facoltativa';note='Alternativa esperienziale breve; non necessaria per procedere e non condizione per eliminare ansia.'
        if code in ['R4-D11','R4-A6','R4-T5']: decision='Riformulare';note='Aiuti e feedback concordati; non sottrarre supporti necessari né usare premi/punizioni per imporre l’adesione.'
        add(code,title,p,start,end,target,decision,note)

# Blocchi non numerati: tenuti separati dai 175 metodi.
p=repfiles[1]; lines=read(p).split('\n')
for n,target in enumerate(['S18,S20','S18','S19','S19','S19,S26','S19','S25'],1):
    start=next(i+1 for i,l in enumerate(lines) if l.startswith(f'### 3.{n} ')); end=next((i for i in range(start,len(lines)) if lines[i].startswith('##')),len(lines))
    add(f'R2-MAP{n}',lines[start-1].split(' ',2)[2],p,start,end,target,kind='supplementare',note='Sezione sulle mappe non inclusa nelle 34 tecniche numerate.')
start=next(i+1 for i,l in enumerate(lines) if l.startswith('## 4. '));end=next(i for i in range(start,len(lines)) if lines[i].startswith('## 5.'))
add('R2-CICLO','Ciclo metacognitivo in seduta',p,start,end,'CAP6','Riformulare','Allineare al calendario unico del manuale; tappa G per modificare l’originale.',kind='supplementare')
p=repfiles[2];lines=read(p).split('\n')
for n,code,tgt in [(0,'PRINCIPI','CAP2,CAP37'),(10,'LINGUE','S49,S50'),(12,'LUDICA','CAP6,CAP42'),(13,'TABLET','S24,S46,S48')]:
    start=next(i+1 for i,l in enumerate(lines) if l.startswith(f'## {n}. '));end=next((i for i in range(start,len(lines)) if lines[i].startswith('## ')),len(lines))
    add('R3-'+code,lines[start-1].split(' ',2)[2],p,start,end,tgt,kind='supplementare',note='Blocco non contato fra le 49 tecniche; la dispensa nelle lingue richiede condizioni specifiche, non discende automaticamente dalla diagnosi.' if n==10 else 'Contesto d’uso; adattamenti e limiti da mantenere.')
game_start=next(i for i,l in enumerate(lines) if l.startswith('| Gioco |'))
games=[]
for i in range(game_start+2,len(lines)):
    if not lines[i].startswith('|'): break
    fields=[x.strip() for x in lines[i].strip('|').split('|')];games.append(fields[0])
    add(f'R3-GIOCO{len(games):02}',fields[0],p,i+1,i+1,'CAP6,CAP42','Opzione di setting','Non indispensabile al percorso; età e funzioni nel repertorio non costituiscono prove di efficacia né indicazioni aggiornate d’acquisto.',kind='supplementare')

smap={'MAP': ['S18','S19','S19','S19','S19,S41','S19,S41','S19,S41','S21,S41','S23,S41','S22','S32','S42,S19','S17,S19','S19'],
'MET':['CAP4,S26,S27','S26','S27','S28','CAP4','S9,S10,S11','S38,C3,CAP5','S2','S17','S34,S36,S46','S9,S10','S1'],
'AUT':['S5','S37','D12,D22,S33','S35','D18,S37','S34','CAP51','CAP5,CAP13','S4,D21','S7','S31','S3,S5','S37,D25'],
'MAT':['S45,S46','S45','S46','S46,S47','S46','S46','S46','S48','S48','S48','S48','S48','S45,S46','S45','S47','S46','S46','S46','S46','S46','S46','S48','S48','S46','S46','S48','S45','S45','S45,S46','S45','S45','S48','S48','S47','S45,S46'],
'ITA':['S44','S44','S44','S44','S44','S44','S44','S44','S44','S44','S44','S13,S41','S44','S44','S44','S43']}
p=MAT/'01 Schedario di Studio'/'Schedario di Studio - le schede in testo.md'
lines,secs=sections(p,r'^## ((MAP|MET|AUT|MAT|ITA)-(\d+)) · (.+)')
for start,end,m in secs:
    note='Materiale già pronto: selezionare secondo compito, classe e prerequisiti; il rimando non sostituisce la spiegazione nel manuale.';decision='Materiale pronto'
    if m[1]=='AUT-08':decision='Superata: non distribuire come confine del manuale';note='Ruolo descritto come solo educativo: nel manuale è previsto anche sostegno psicologico. Correzione dell’originale rinviata alla tappa G.'
    if m[1]=='AUT-01':note='La batteria è una metafora, non un modello quantitativo dell’attenzione; osservare la persona e il compito.'
    if m[2]=='MAT' and 16<=int(m[3])<=27:note='Esempio curricolare prevalentemente 14–16; non introdurre anticipatamente né dedurre prerequisiti dalla sola età.'
    add('SCH-'+m[1],m[4],p,start,end,smap[m[2]][int(m[3])-1],decision,note)

lmap={'01-lettura-attiva':'S9,S10,S11','02-sintesi':'S14,S16','03-scelta-strumento':'S38','04-memoria-ripasso':'S26,S27',
'05-incontri':'CAP6','06-osservazione':'STR2,STR5','07-check-in':'D30,STR6','08-confronto-scuola':'CAP52','modello-formulario':'S24','modello-argomento':'S41',
'guida-uso':'CAP1','fonti-verifiche':'APP-C','modello-mappa-concettuale':'S19','modello-mappa-mentale':'S20','IN60':'CAP6','IN90':'CAP6','IN-EMO':'D11,D12,D25','ES01':'S34','ES02':'CAP52','REL01':'S41','REL01-tutor':'S41',
'P01':'STR1,STR4','P02':'STR4,STR5','P03':'STR6','P04':'S2,S27,STR6','P05':'S38,STR2','P06':'STR7','Registro':'STR6,STR7'}
method=['S8','S2','S3,S4','S9,S10,S11','S14,S16','S38','S19','S30','S26,S27','S32,S33','S37','S39,S40']
for i,t in enumerate(method,1):
    for suffix in ['studente','tutor']:lmap[f'M{i:02}-{suffix}']=t
for i,t in enumerate(['S19','S20','S21','S22','S23','S24','S32'],1):lmap[f'MAP{i:02}']=t
for pref,ts in {'ITA':['S11,S13','S16','S42','S44','S44','S44'],'MAT':['S45','S46','S46,S47','S46','S48','S48','S48','S45'],'STO':['S41']*6,'SCI':['S41']*6,'GEO':['S41,S48','S41','S41'],'ENG':['S50','S49,S50']}.items():
    for i,t in enumerate(ts,1):
        for suffix in ['S','T']:lmap[f'{pref}{i:02}-{suffix}']=t
for suffix in ['studente','tutor','schema-esempio','schema-guidato']:lmap['matematica-'+suffix]='S46'
for pref in ['storia','scienze']:
    for suffix in ['studente','tutor','mappa-esempio','mappa-guidata']:lmap[pref+'-'+suffix]='S19,S41'
lmap['scienze-circuito']='S23,S41'
p=MAT/'03 Laboratorio in testo'/'Laboratorio studio DSA - risorse in testo.md'; lines,secs=sections(p,r'^## (\S+) · (.+)')
for start,end,m in secs:
    code,title=m[1],m[2]; content='\n'.join(lines[start-1:end]); pdfm=re.search(r'^PDF: `([^`]+)`',content,re.M);pdf=pdfm[1] if pdfm else ''
    if pdf:
        pdfp=ROOT/'Laboratorio studio DSA'/pdf; assert pdfp.is_file(),pdf;tracked.add(pdfp)
    note='Risorsa complementare: esempio, traccia o guida; versione studente e tutor non sono doppioni eliminabili.'
    if code in ['GEO02-S','GEO02-T','GEO03-S','GEO03-T','ENG01-S','ENG01-T','ENG02-S','ENG02-T']:
        title={'GEO02':'Paesaggi e climi','GEO03':'Territori, popolazioni ed economie','ENG01':'Costruzione della frase','ENG02':'Tempi verbali e connettori frequenti'}[code[:5]]+(' — studente' if code.endswith('S') else ' — tutor');note='Presente in cartella ma assente dall’indice HTML; titolo descrittivo ricavato dalla guida alle fonti, intestazione del testo conserva il codice.'
    if code in ['IN60','IN90','05-incontri']:note='Tre scalette da allineare al capitolo 6; nessuna modifica ora (tappa G).'
    if code=='P03':note='Base del registro incluso nello Strumento 6: aggiungere DNA-V e consapevolezza solo nel nuovo allegato; tappa G per aggiornare l’originale.'
    if code=='Registro':
        tracked.add(ROOT/'Laboratorio studio DSA'/'Percorsi individuali'/'_MODELLO'/'Registro.ods');note='Registro originale con fogli incontri, piano e obiettivi; non modificato. Solo modello vuoto.'
    add('LAB-'+code,title,p,start,end,lmap[code],'Materiale pronto',note,pdf=pdf)

p=MAT/'02 Compendio DNA-V'/'Il DNA-V in seduta - compendio operativo (testo).md';lines=read(p).split('\n')
starts=[]
for i,l in enumerate(lines):
    m=re.search(r'► Tecnica (\d+)\s*[–—-]\s*(.+)',l)
    if m: starts.append((i+1,int(m[1]),m[2]))
assert len(starts)==26,len(starts)
selected={int(x['id'][1:]) for x in D if x['origine']=='compendio'}
for j,(start,n,title) in enumerate(starts):
    end=starts[j+1][0]-1 if j+1<len(starts) else next(i for i in range(start,len(lines)) if 'Seconda parte' in lines[i])
    add('COMP-T'+str(n),title,p,start,end,'D'+str(n) if n in selected else 'APP-B','Integrare riscrivendo' if n in selected else 'Solo rimando facoltativo','Nessun esercizio escluso è necessario per il percorso autonomo.' if n not in selected else 'Conservare il numero originale; testo riscritto sullo studio. D2: rimuovere il riferimento ai ragazzi cinestesici.')
sheetstarts=[]
for i,l in enumerate(lines):
    if i<1400:continue
    m=re.match(r'^\s*\f?\s*Scheda (\d+)\s*·\s*(.+)',l)
    if m: sheetstarts.append((i+1,int(m[1]),m[2]))
assert len(sheetstarts)==10,len(sheetstarts)
conv={1:14,2:15,3:16,4:19,5:17,6:21,7:20,8:22,9:23,10:18}
for j,(start,n,title) in enumerate(sheetstarts):
    end=sheetstarts[j+1][0]-1 if j+1<len(sheetstarts) else len(lines)
    add('COMP-SCH'+str(n),title,p,start,end,'SCH'+str(conv[n]),'Riscrivere allegato','La scheda 1 originale è per il tutor: la nuova 14 sarà per il ragazzo, con linguaggio e campi da riprogettare.' if n==1 else 'Corrispondenza funzionale: ordine delle nuove schede diverso dall’ordine del compendio.')

valid={x['id'] for x in S+D+C}|{f'CAP{i}' for i in range(1,53)}|{f'SCH{i}' for i in range(1,24)}|{f'STR{i}' for i in range(1,8)}|{'APP-B','APP-C'}
assert len(rows)==len({r['id'] for r in rows})
assert all(t in valid for r in rows for t in r['destinazioni']),[(r['id'],r['destinazioni']) for r in rows if any(t not in valid for t in r['destinazioni'])]
count=Counter(r['id'].split('-')[0] for r in rows if r['gruppo']=='principale')
assert sum(count.values())==433,count
assert [count[k] for k in ['R1','R2','R3','R4','SCH','LAB','COMP']]==[53,34,49,39,90,132,36],count
assert all(any(x['id'] in r['destinazioni'] for r in rows) for x in S),[x['id'] for x in S if not any(x['id'] in r['destinazioni'] for r in rows)]
save('mappatura.json',rows); save('catalogo-manuale.json',dict(strategie=S,dnav=D,consapevolezza=C,schede=[dict(id='SCH'+str(i),titolo=t,agganci=SHEET_TARGETS[i-1].split(','),semplificata=i in [1,2,3,4,13,14,16]) for i,t in enumerate(SHEETS,1)],strumenti=[dict(id='STR'+str(i),titolo=t) for i,t in enumerate(INSTRUMENTS,1)]))
with (OUT/'mappatura.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f,delimiter=';');w.writerow(['Codice','Titolo','Destinazioni','Decisione','Nota','File fonte','Riga inizio','Riga fine','Gruppo','PDF nel Laboratorio'])
    for r in rows:w.writerow([r['id'],r['titolo'],', '.join(r['destinazioni']),r['decisione'],r['nota'],r['file'],r['riga_inizio'],r['riga_fine'],r['gruppo'],r['pdf']])
md='# Tabella completa di corrispondenza\n\nTappa A · 30 settembre 2026 · proposta da approvare.\n\n433 unità principali: 175 tecniche dei repertori, 90 schede dello Schedario, 132 risorse del Laboratorio, 26 tecniche e 10 schede del compendio. Seguono anche 40 blocchi supplementari (comprese 28 righe di giochi). Una corrispondenza è una decisione editoriale, non una prova di equivalenza o efficacia. Nessun originale modificato.\n\nLegenda: SCH- = Schedario; SCH senza trattino = nuovo allegato del manuale; COMP-T = tecnica del compendio; COMP-SCH = scheda del compendio; LAB- = Laboratorio; CAP = capitolo; STR = nuovo strumento del clinico. Righe contate sui file UTF-8 con separatore LF, conservando i salti pagina.\n\n'
for prefix,label in [('R1-','Repertorio 1'),('R2-','Repertorio 2'),('R3-','Repertorio 3'),('R4-','Repertorio 4'),('SCH-','Schedario di Studio'),('LAB-','Laboratorio'),('COMP-','Compendio')]:
    group=[r for r in rows if r['id'].startswith(prefix)]
    md+='## '+label+'\n\n'+table(['Codice · titolo','Destinazione','Decisione / nota','Fonte'],[[r['id']+' · '+r['titolo'],', '.join(r['destinazioni']),r['decisione']+'. '+r['nota'],'['+str(r['riga_inizio'])+'–'+str(r['riga_fine'])+'](<'+str(ROOT/r['file'])+':'+str(r['riga_inizio'])+'>)'] for r in group])+'\n'
(OUT/'02-mappatura-completa.md').write_text(md,encoding='utf-8')
catalog='# Catalogo definitivo proposto per l’indice\n\nNumerazione da fissare con l’approvazione della tappa A; le procedure saranno scritte nelle tappe B–E. Tutte le schede avranno le voci richieste dal piano, incluse varianti per età e profilo, padronanza e fonti.\n\n## Strategie di metodo: 50\n\n'+table(['Codice','Titolo','Cap.','Fase iniziale','Risultato da insegnare'],[[x['id'],x['titolo'],x['capitolo'],x['fase'],x['obiettivo']] for x in S])
catalog+='\n## DNA-V: 24 schede complete\n\n20 tecniche del compendio più D27–D30. D5, D8, D9, D10, D19 e D24 restano solo rimandi facoltativi. Le varianti 8–10 di D2, D12, D15 e D22 sono interne alle rispettive schede, senza nuovi numeri.\n\n'+table(['Codice','Titolo','Cap.','Fase','Agganci S','Origine'],[[x['id'],x['titolo'],x['capitolo'],x['fase'],', '.join(x['agganci']),x['origine']] for x in D])
catalog+='\n## Consapevolezza: 7 tappe\n\n'+table(['Codice','Titolo','Cap.','Fase','Documento finale'],[[x['id'],x['titolo'],x['capitolo'],x['fase'],x['obiettivo']] for x in C])
catalog+='\n## Schede per il ragazzo: 23, con 7 versioni semplificate\n\n'+table(['Scheda','Titolo','Aggancio','Anche 8–10 semplificata'],[[i,t,SHEET_TARGETS[i-1],'Sì' if i in [1,2,3,4,13,14,16] else 'No; istruzioni adattate nella scheda S/D/C'] for i,t in enumerate(SHEETS,1)])
catalog+='\nLa Scheda 13 avrà quattro pagine nella versione ordinaria e due in quella semplificata. Le altre avranno una pagina salvo la Scheda 15 (due pagine di carte). Stima: 27 + 8 pagine, comprese le varianti, più 2 pagine di istruzioni: **37 pagine A4**. Le carte saranno originali. Le figure saranno funzionali e stampabili in bianco e nero.\n\n## Strumenti del clinico: 7\n\n'+table(['Strumento','Titolo','Pagine A4 stimate'],[[i,t,2 if i in [1,2,4,5,6,7] else 3] for i,t in enumerate(INSTRUMENTS,1)])
catalog+='\nLo Strumento 6 incorpora il registro basato su Laboratorio P03 con righe DNA-V e consapevolezza: non si crea un ottavo strumento. Tre versioni dell’intervista (Strumento 3). Stima: **15 pagine A4**, più copertina e istruzioni: **17**. Totale dei due allegati: **54 pagine**, superiore alle 35–45 ipotizzate perché si contano tutte le versioni e gli spazi di scrittura. I questionari proprietari non sono riprodotti.\n\n## Provenienza inversa\n\nOgni strategia ha una destinazione distinta. I rimandi qui sotto sono una selezione editoriale completa delle corrispondenze registrate, non bibliografia scientifica. D27–D30 sono adattamenti nuovi; la loro base e i limiti sono nel rapporto critico.\n\n'
catalog+=table(['Destinazione','Risorse mappate'],[[x['id']+' · '+x['titolo'],', '.join(r['id'] for r in rows if x['id'] in r['destinazioni']) or 'Nuovo adattamento: vedi rapporto critico'] for x in S+D+C])
(OUT/'01b-catalogo-schede.md').write_text(catalog,encoding='utf-8')

# Registro delle fonti già predisposte: nessun abstract viene copiato nell'output.
p=MAT/'05 Letteratura scientifica'/'Riferimenti bibliografici - citazioni, collegamenti e sintesi.md'; lines,secs=sections(p,r'^### (.+)')
refs=[]
for start,end,m in secs:
    content='\n'.join(lines[start-1:end]); dois=list(dict.fromkeys(re.findall(r'10\.\d{4,9}/[^\s<>\]）]+',content)))
    refs.append(dict(id=f'F{len(refs)+1:02}',titolo=m[1],file=p.relative_to(ROOT).as_posix(),riga_inizio=start,riga_fine=end,doi=dois))
save('registro-fonti-locali.json',refs)

# Impronte della base testuale, dei PDF pronti e degli originali esplicitamente usati.
for p in [ROOT/'Studiare con il DNA-V - piano del manuale.md',MAT/'00 LEGGIMI - dove trovare ogni elemento del piano.md',MAT/'01 Schedario di Studio'/'Schedario di Studio.html',ROOT/'Il DNA-V in seduta - compendio operativo.pdf',ROOT/'Il DNA-V in seduta - schede di lavoro A4.pdf',ROOT/'Laboratorio studio DSA'/'Indice.html',ROOT/'Laboratorio studio DSA'/'Manutenzione'/'PIANO.md']:
    tracked.add(p)
for folder in [MAT/'04 Normativa', MAT/'05 Letteratura scientifica'/'Testi integrali da PubMed Central',MAT/'06 Tecniche ACT citate']:
    for p in folder.glob('*.md'):tracked.add(p)
imprints=[dict(file=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(tracked)]
save('impronte-fonti-consegna.json',imprints)
report=dict(data='2026-09-30',unita_principali=sum(count.values()),conteggi=dict(count),supplementari=len(rows)-433,totale_righe=len(rows),schede_S=len(S),schede_D=len(D),tappe_C=len(C),schede_ragazzo=len(SHEETS),strumenti_clinico=len(INSTRUMENTS),riferimenti_locali=len(refs),fonti_con_impronta=len(imprints),destinazioni_valide=True,codici_univoci=True,tutte_S_con_provenienza=True,copertura_clinica_validata=False,stato='Tappa A: proposta editoriale da approvare; B non iniziata')
save('esito-controlli.json',report)
print(json.dumps(report,ensure_ascii=False))
