from pathlib import Path
import zipfile,subprocess,hashlib,textwrap,sys
from produci import ROOT,MAINT,WORK,writer,LO,LEDGER,load,write_json,sha

TYPES=[('MAP01','Mappa concettuale'),('MAP02','Mappa mentale'),('MAP03','Cronologia'),('MAP04','Tabella comparativa'),('MAP05','Schema procedurale'),('MAP06','Formulario'),('MAP07','Scaletta')]
source=ROOT/'Modelli riutilizzabili/Modificabili/modello-mappa-concettuale.odg'
with zipfile.ZipFile(source) as z:styles=z.read('styles.xml').decode()
def text(s,x,y,w,h=1.2,para='Body'):
    return f'<draw:frame draw:style-name="Text" svg:x="{x}cm" svg:y="{y}cm" svg:width="{w}cm" svg:height="{h}cm"><draw:text-box>{writer.p(s,para)}</draw:text-box></draw:frame>'
def box(s,x,y,w,h=2.2):
    s='\n'.join('\n'.join(textwrap.wrap(part,width=max(12,int((w-.5)*3.6)),break_long_words=False,break_on_hyphens=False)) for part in s.split('\n'))
    return f'<draw:rect draw:style-name="Blank" svg:x="{x}cm" svg:y="{y}cm" svg:width="{w}cm" svg:height="{h}cm">{writer.p(s)}</draw:rect>'
def line(x,y,a,b,arrow=True):
    return f'<draw:line draw:style-name="{"ArrowLine" if arrow else "Line"}" svg:x1="{x}cm" svg:y1="{y}cm" svg:x2="{a}cm" svg:y2="{b}cm"/>'
def build(kid,name,mode):
    example=mode==0;guided=mode==1
    suffix=['Esempio','Traccia guidata','Modello da adattare'][mode]
    b=text(name+' - '+suffix,1.2,.7,27.3,1.25,'Title')
    task='Leggi lo strumento, poi usalo per rispondere a una domanda.' if example else 'Completa e modifica. Prova lo strumento su un compito, poi rivedilo.'
    b+=text(task,1.2,2.2,27.3,1.1,'Left')
    if kid=='MAP01':
        b+=text('Domanda focale: come costruisco una sintesi fedele?' if example or guided else 'Domanda focale: ___________________________________________________',1.2,3.4,27.3,1.3,'Left')
        nodes=['Testo di partenza','Idee principali','Sintesi','Domanda di studio']
        if guided:nodes=['Testo di partenza','_______________','Sintesi','_______________']
        if mode==2:nodes=['Concetto: __________']*4
        b+=line(7.8,7,12,7)+line(17.7,8.7,17.7,12)+line(6.7,13.3,12,8.8)
        for v,x,y,w in [(nodes[0],1.2,6,6.6),(nodes[1],12,6,11.5),(nodes[2],12,12,11.5),(nodes[3],1.2,13,7.5)]:b+=box(v,x,y,w,2.6)
        for v,x,y,w in [('contiene',8,5.2,3.8),('vengono collegate nella',18,9.4,10),('orienta la scelta delle',1.2,9.8,9.5)]:
            b+=text(v if example else 'legame: __________',x,y,w,1.5)
        linear='Versione lineare: il testo contiene idee principali; queste vengono collegate nella sintesi. La domanda di studio orienta la scelta delle idee principali.'
    elif kid=='MAP02':
        vals=['Materiali: testo e appunti','Domande: significato, esempio','Tempi: giorno da concordare','Controllo: verifica e correzione']
        b+=line(14.8,10,6,6,False)+line(14.8,10,24,6,False)+line(14.8,10,6,14,False)+line(14.8,10,24,14,False)
        b+=box('Ripasso' if mode<2 else 'Tema: __________',10.5,8.6,8.7,2.6)
        for i,(x,y) in enumerate([(1.2,4.4),(20,4.4),(1.2,13.3),(20,13.3)]):b+=box(vals[i] if example else vals[i].split(':')[0]+': ______' if guided else 'Ramo: __________\n_______________',x,y,8.5,3.1)
        linear='Versione lineare: per organizzare il ripasso scelgo materiali, domande, tempi e modalità di controllo. I rami raccolgono idee; non indicano da soli rapporti causali.'
    elif kid=='MAP03':
        b+=text('Italia: alcuni passaggi tra guerra e Costituzione' if mode<2 else 'Argomento e periodo: _______________________________________________',1.2,3.5,27.3,1.2,'Left')
        events=[('1945','Fine della guerra in Italia'),('1946','Referendum: scelta repubblicana'),('1948','Entrata in vigore della Costituzione')]
        b+=line(3,8,26.5,8)
        for i,(date,event) in enumerate(events):
            x=1.2+i*9.2;b+=line(x+4,7.6,x+4,8.4,False)
            b+=text(date if mode<2 else 'Data: ______',x,5.8,8.8,1)
            b+=box(event if example else 'Evento: __________\n_________________',x,9,8.8,4)
        b+=text('Linea ordinata, non in scala proporzionale. Per intervalli precisi aggiungi una scala.',1.2,14.3,27.3,1.5,'Left')
        linear='Versione lineare: nel 1945 finisce la guerra in Italia; nel 1946 si sceglie la Repubblica; nel 1948 entra in vigore la Costituzione. L’ordine temporale non dimostra da solo una causa.'
    elif kid=='MAP04':
        vals=[['Criterio','Evaporazione','Ebollizione'],['Dove avviene','Alla superficie','In tutto il liquido'],['Condizioni','Può avvenire a varie temperature','Alla temperatura di ebollizione per quella pressione'],['Che cosa osservo','Perdita graduale di liquido','Formazione di bolle nel liquido']]
        for r,row in enumerate(vals):
            for c,v in enumerate(row):
                s=v if example or (guided and (r==0 or c==0)) else ('Criterio / caso' if r==0 else '________________')
                b+=box(s,1.2+c*9.1,4+r*2.8,9.1,2.8)
        linear='Versione lineare: entrambi sono passaggi da liquido a gas. L’evaporazione riguarda la superficie; l’ebollizione interessa il liquido con bolle. La temperatura di ebollizione dipende dalla pressione.'
    elif kid=='MAP05':
        steps=['1. Calcolo 2 + 3 × 4','2. Prima la moltiplicazione, poi la somma','3. 3 × 4 = 12; poi 2 + 12 = 14','4. Il risultato è 14: ho rispettato le precedenze']
        if guided:steps=['1. Calcola 5 + 2 × 3','2. Quale operazione esegui prima? __________','3. Scrivi i due passaggi: __________________','4. Controlla con una calcolatrice: __________']
        for i,v in enumerate(steps):
            y=3.9+i*3.1
            if i<3:b+=line(14.8,y+2.2,14.8,y+3.05)
            b+=box(v if example or guided else f'{i+1}. ______________________',5,y,19.7,2.2)
        linear='Versione lineare: comprendo il compito, scelgo una regola pertinente, la applico e controllo. Se il controllo non torna, individuo il passaggio da rivedere; non cambio soltanto il risultato.'
    elif kid=='MAP06':
        vals=[['Grandezza e condizioni','Formula','Simboli e unità'],['Area rettangolo','A = b × h','b e h in cm; A in cm²'],['Perimetro rettangolo','P = 2 × (b + h)','b e h in cm; P in cm'],['Ipotenusa, solo triangolo rettangolo','c = √(a² + b²)','a, b cateti; c ipotenusa; stessa unità']]
        for r,row in enumerate(vals):
            for c,v in enumerate(row):
                s=v if example or (guided and (r==0 or c==0)) else ('Nome / formula / unità' if r==0 else '________________')
                b+=box(s,1.2+c*9.1,4+r*2.8,9.1,2.8)
        linear='Esempio d’uso: rettangolo con b = 5 cm e h = 3 cm. A = 15 cm²; P = 16 cm. Un formulario deve dire quando la formula vale e che cosa significano simboli e unità.'
    else:
        vals=['Apertura: di che cosa parlo e perché','Punto 1: l’acqua evapora dalla superficie','Punto 2: un esempio, il vaso al sole','Punto 3: confronto con l’ebollizione','Chiusura: che cosa abbiamo chiarito']
        for i,v in enumerate(vals):b+=box(v if example else v.split(':')[0]+': _________________________________' if guided else f'{i+1}. ______________________________________',2,4+i*2.35,25.7,2.15)
        linear='Versione lineare: introduco l’argomento, spiego l’evaporazione, presento un esempio, confronto con l’ebollizione e chiudo. La scaletta può contenere frasi, parole o richiami visivi utili.'
    b+=text(linear if example else 'Dopo la prova: quale parte ti è servita? Che cosa vuoi aggiungere, spostare o togliere?',1.2,17.2,27.3,2.2,'Left')
    b+=text('LABORATORIO STUDIO DSA  /  '+kid+'  /  2026-09-29  /  '+str(mode+1),1.2,20,27.3,.5,'Small')
    return b
ledger=load(LEDGER,{})
records=[]
selected=set(sys.argv[1:])
if selected:records=[r for r in load(MAINT/'produzione/registrazioni/mappe.json',[]) if r['id'] not in selected]
for kid,name in TYPES:
    if selected and kid not in selected:continue
    base=Path('Laboratorio delle mappe')/name
    src=base/'Modificabili'/(kid+'.odg');pdf=base/'Studente'/(kid+'.pdf')
    for rel in [src,pdf]:
        if (ROOT/rel).exists() and ledger.get(rel.as_posix())!=sha(ROOT/rel):raise RuntimeError('Sorgente cambiata: '+str(rel))
    pages=[build(kid,name,m) for m in range(3)]
    import re
    paragraph_styles=''.join(re.findall(r'<style:style\b[^>]*style:family="paragraph"[^>]*>.*?</style:style>',styles,re.S))
    content=f'<office:document-content {writer.NS} office:version="1.3"><office:automatic-styles>{paragraph_styles}</office:automatic-styles><office:body><office:drawing>'+''.join(f'<draw:page draw:name="Pagina{i+1}" draw:master-page-name="Standard">{b}</draw:page>' for i,b in enumerate(pages))+'</office:drawing></office:body></office:document-content>'
    writer.pkg(ROOT/src,'graphics',content,styles);(ROOT/pdf).parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([str(LO),f'-env:UserInstallation={(WORK/"lo-produzione").as_uri()}','--headless','--convert-to','pdf','--outdir',str((ROOT/pdf).parent),str(ROOT/src)],capture_output=True,check=True,timeout=90)
    assert (ROOT/pdf).exists()
    for rel in [src,pdf]:ledger[rel.as_posix()]=sha(ROOT/rel)
    records.append(dict(id=kid,title=name+' - esempio, traccia e modello',subject='Laboratorio delle mappe',topic=name,school='Triennio / adattabile',objective='Costruire, provare e rivedere uno strumento',kind='Organizzatore modificabile',level='Esempio e completamento',audience='Studente',pdf=pdf.as_posix(),source=src.as_posix(),date='2026-09-29',expected_pages=3,kit=kid,prerequisites='Leggere brevi frasi o ascoltarle',task='Costruire uno strumento',difficulty='Selezione dei contenuti e leggibilità dei collegamenti',tool=name,curriculum='Competenze trasversali; confronto con curricolo d’istituto',sources='IHMC, Novak e Cañas, Theory Underlying Concept Maps; esempi e layout originali. Fonti disciplinari nei kit.',version='1.0',status='da verificare',batch='mappe'))
write_json(LEDGER,ledger);write_json(MAINT/'produzione/registrazioni/mappe.json',records)
print('7 organizzatori Draw, 21 pagine')
