from pathlib import Path
import json
B=Path(__file__).parent
docs=[]
def doc(id,title,pages,audience='Studente',kind='Scheda',folder='Metodo di studio',topic='Strategie trasversali'):
    docs.append(dict(id=id,title=title,pages=pages,audience=audience,kind=kind,level='Adattabile',subject='Metodo di studio' if folder=='Metodo di studio' else folder,topic=topic,folder=folder,school='Triennio / adattabile'))
def page(title,subtitle,*blocks):return dict(title=title,subtitle=subtitle,blocks=list(blocks))
def h(a,b=''):return {'h':a,**({'p':b} if b else {})}
def bullets(*s):return {'bullets':list(s)}
def lines(n):return {'lines':n}
def call(s):return {'callout':s}

doc('01-lettura-attiva','Lettura attiva',[page('Leggere con una domanda','Scegli un paragrafo breve del libro o una scheda del kit.',
h('1. Prima di leggere','Guarda titolo, sottotitoli e immagini pertinenti. Che cosa cerchi di capire? Scrivi una domanda.'),lines(2),
h('2. Un pezzo alla volta','Leggi un paragrafo. Se decifrare il testo ti affatica, concorda lettura del tutor o ascolto: la comprensione resta il compito.'),
bullets('Cerchia al massimo due parole da chiarire.','Sottolinea ciò che risponde alla domanda, non tutto il paragrafo.','Spiega il passaggio a parole tue, poi controlla nel testo.'),
h('3. Controlla il significato','Scrivi una risposta breve. Quale informazione del testo la sostiene?'),lines(3),
call('Se non trovi la risposta, cambia domanda o chiedi un chiarimento. Non serve leggere più velocemente.') )])

doc('02-sintesi','Sintesi senza perdere i legami',[page('Dal testo alla sintesi','Prima scegli le informazioni, poi decidi come rappresentarle.',
h('Un esempio','Testo: «Il generatore mantiene una tensione tra due morsetti. In un circuito chiuso può circolare corrente.»\nParole chiave: generatore, tensione, circuito chiuso, corrente.\nLegame: il generatore mantiene la tensione; il circuito chiuso permette il passaggio della corrente.'),
h('Prova con il tuo testo','Qual è l’idea principale?'),lines(2),
{'table':{'headers':['Informazione necessaria','Perché serve alla domanda?'],'rows':[['',''],['',''],['','']]}},
h('Scrivi una sintesi di 2-3 frasi'),lines(3),
call('Rileggi il testo: hai conservato chi fa cosa, quando e perché? Una lista di parole isolate può perdere il significato.') )])

doc('03-scelta-strumento','Scegliere lo strumento',[page('Quale supporto mi serve?','La scelta dipende dal compito. Puoi combinare due strumenti.',
{'table':{'headers':['Devo…','Posso provare…'],'widths':[8.4,9.2],'rows':[
['Spiegare rapporti tra concetti','Mappa concettuale: frecce con parole-legame.'],
['Raccogliere e raggruppare idee','Mappa mentale: argomento centrale e rami.'],
['Mettere in ordine gli eventi','Cronologia: date e avvenimenti.'],
['Confrontare elementi','Tabella: stessi criteri per ogni elemento.'],
['Scegliere e usare una formula','Formulario: significato, unità, condizioni, esempio.'],
['Seguire un procedimento','Sequenza operativa: passaggi e controlli.']]}},
h('La mia scelta','Oggi devo…'),lines(1),
{'p':'Scelgo… perché…'},lines(2),
call('Provalo su una domanda o un esercizio. Se non ti aiuta a rispondere, modifica il supporto: non giudicarlo solo dall’aspetto.') )])

doc('04-memoria-ripasso','Memoria e ripasso',[page('Ricordare e ritrovare','Ripassi brevi in giorni diversi, con domande e controllo delle risposte.',
h('1. Prepara tre domande','Esempi: «Perché l’Italia entra in guerra nel 1915?»; «Quando vale U = R × I?»; «Come controllo una soluzione?»'),
h('2. Prova a rispondere','Se l’obiettivo è ricordare, prova senza rileggere per un momento, poi controlla. Se l’obiettivo è usare la mappa, tienila disponibile. Concorda la modalità con il tutor.'),
h('3. Riprendi gli errori','Segna una risposta incompleta e correggila. Prova ancora dopo una pausa o in un altro giorno.'),
{'table':{'headers':['Ripasso concordato','Domanda / punto da riprendere'],'rows':[['Data: __________',''],['Data: __________',''],['Data: __________','']]}},
h('Una piccola associazione','Per distinguere armistizio e trattato, immagina prima un segnale di stop alle ostilità e poi un tavolo di negoziato. Spiega anche la differenza con parole tue.'),
call('L’associazione è un aiuto personale, non una definizione storica. Gli intervalli di ripasso si adattano a scadenze e difficoltà.') )])

doc('05-incontri','Scalette per incontri da 60 e 90 minuti',[page('Un incontro, un obiettivo','Guida del tutor. Tempi orientativi, da adattare al compito e alla fatica.',
{'table':{'headers':['Fase','60 min','90 min'],'widths':[11.6,3,3],'rows':[
['Accoglienza e check-in facoltativo','5','5'],['Ripresa del lavoro precedente e obiettivo','5','10'],['Esempio ragionato / lettura guidata','10','15'],['Costruzione o adattamento del supporto','20','25'],['Pausa concordata','0*','5'],['Uso in un compito nuovo','15','20'],['Riepilogo e piccolo impegno','5','10']]}},
{'p':'* Una pausa può servire anche nei 60 minuti: ricavala dal lavoro centrale, senza allungare automaticamente l’incontro.'},
bullets('Scegli un obiettivo osservabile: per esempio spiegare due legami della mappa.','Se il compito scolastico è urgente, insegnare una strategia dentro quel compito.','Chiedi allo studente di descrivere il proprio passaggio prima di offrire un suggerimento.','Concorda un impegno breve: quando, per quanto tempo e con quale supporto.'),
call('Raccogli un esempio di riuso nell’incontro successivo. Il numero di pagine completate non misura da solo l’autonomia.') )],audience='Tutor',kind='Guida')

doc('06-osservazione','Osservare autonomia e riuso',[page('Che cosa riesce a fare con il supporto?','Scheda educativa del tutor. Nessun nome o dato clinico necessario.',
{'p':'Data: __________   Compito / argomento: ____________________'},
h('Obiettivo concreto'),lines(1),
{'table':{'headers':['Osservazione','Esempio visto / suggerimento dato'],'widths':[8.2,9.4],'rows':[
['Sceglie il supporto e spiega perché',''],['Lo usa in un compito analogo ma nuovo',''],['Trova un errore o un’informazione mancante','']]}},
{'p':'Supporto rimasto disponibile: ______________________________\nAiuti dati (quali e quanti): _________________________________'},lines(1),
{'p':'Difficoltà osservata / adattamento utile:'},lines(2),
{'p':'Prossimo passo e prova di riuso nell’incontro successivo:'},lines(2),
call('Confronta compiti simili e annota le condizioni. Meno suggerimenti del tutor può indicare progresso; togliere lo strumento compensativo non è il criterio.') )],audience='Tutor',kind='Osservazione')

doc('07-check-in','Breve check-in sul compito',[page('Rendere affrontabile il prossimo passo','Routine facoltativa di 2-3 minuti, all’inizio o durante un blocco.',
h('Chiedi e ascolta','«Come ti sembra questo compito oggi?»\n«Quale parte ti sta mettendo in difficoltà?»\nÈ possibile non rispondere o indicare direttamente il punto sul foglio.'),
h('Scegliete un piccolo adattamento'),bullets('Leggere insieme una consegna.','Dividere l’attività e iniziare da un solo passaggio.','Usare la mappa o un esempio già noto.','Fare una breve pausa concordata.'),
h('Riprendete e controllate','«Qual è il primo passo che proviamo?»\nDopo qualche minuto: «Questo cambiamento ti aiuta oppure ne proviamo un altro?»'),
call('Non attribuire automaticamente il disagio alla scuola. Accogli ciò che emerge senza forzare confidenze o introdurre punteggi clinici.'),
{'p':'Se la difficoltà è intensa o persistente, valuta un confronto appropriato con famiglia e professionisti secondo il tuo ruolo. Questa scheda organizza il lavoro educativo, non un trattamento.'})],audience='Tutor',kind='Guida')

doc('08-confronto-scuola','Confronto con la scuola per l’esame',[page('Concordare l’uso dei materiali','Scheda di preparazione al confronto, da compilare con le indicazioni della scuola.',
{'p':'Anno scolastico: __________   Classe: __________\nData del confronto: __________   Ruolo dell’interlocutore: __________'},
{'table':{'headers':['Punto da chiarire','Indicazione raccolta'],'widths':[8.4,9.2],'rows':[
['Materiale e versione esatta',''],['Uso abituale durante l’anno',''],['Riferimento pertinente nel PDP',''],['Prova / situazione di utilizzo',''],['Modifiche o limiti indicati dalla scuola',''],['Prossima verifica e data','']]}},
call('Porta un esempio reale già utilizzato dallo studente. Una mappa pronta o questo modulo non costituiscono un’autorizzazione all’esame.'),
{'p':'Controllare con la scuola le disposizioni applicabili all’anno dell’esame. Riferimento generale: DM 741/2017, art. 14; fonte nella guida.'})],audience='Tutor',kind='Confronto scuola')

doc('modello-formulario','Modello di formulario ragionato',[page('Una formula che so usare','Compila una scheda per volta; aggiungi il tuo esempio.',
{'p':'Materia / argomento: _____________________________________'},
h('Domanda a cui risponde la formula'),lines(2),
h('Formula e significato dei simboli'),lines(3),
{'table':{'headers':['Simbolo','Che cosa rappresenta','Unità'],'widths':[3,10.6,4],'rows':[['','',''],['','',''],['','','']]}},
h('Quando posso usarla?'),lines(2),
h('Un esempio con dati, sostituzione e risultato'),lines(3),
call('Controllo: il risultato risponde alla domanda? L’unità è coerente? Ho rispettato le condizioni?') )],folder='Modelli riutilizzabili',kind='Modello',topic='Formulari')

doc('modello-argomento','Modello per un nuovo argomento',[page('Progettare un piccolo kit','Scheda del tutor da duplicare prima di aggiungere un argomento.',
{'p':'Materia: __________   Argomento: __________________________\nClasse orientativa: __________   Data / versione: ______________'},
h('Obiettivo e prerequisiti'),lines(2),
h('Quale strumento serve al compito?'),lines(2),
{'table':{'headers':['Materiale da preparare','Controllo'],'widths':[12.6,5],'rows':[
['Breve testo o spiegazione originale',''],['Esempio corretto e commentato',''],['Traccia guidata e consegna su foglio libero',''],['Applicazione nuova e soluzioni separate',''],['Fonti controllate / verifiche numeriche',''],['Sorgenti modificabili e PDF leggibili','']]}},
{'p':'Percorso della nuova cartella: Materie / materia / argomento.'},
call('Dopo la prova, annota che cosa ha aiutato e che cosa va adattato. Aggiungi il materiale al catalogo solo quando i file sono presenti.') )],audience='Tutor',folder='Modelli riutilizzabili',kind='Modello',topic='Nuovi argomenti')

doc('guida-uso','Guida all’uso della biblioteca',[
page('Inizia da qui','Biblioteca locale per il tutor; materiali su carta per lo studente.',
bullets('Apri Indice.html. Cerca un argomento o filtra per materia e destinatario.','Scegli il PDF per mostrare o stampare. Usa il collegamento alla sorgente per aprire LibreOffice.','In ciascun kit: schede dello studente, mappa o schema completo, traccia guidata, guida e soluzioni del tutor.','Le schede propongono attività modulari: non occorre completare tutto in un incontro.'),
h('Un primo uso possibile','Scegli un obiettivo. Mostra un esempio spiegando le scelte. Costruite una parte insieme. Fai usare il supporto su una domanda nuova. Annotate una modifica utile.'),
h('Carta e accessibilità','Stampa in A4 al 100%, controllando orientamento e anteprima. Colori e sfondi sono discreti; significati e collegamenti restano leggibili in grigio. Per ampliare il testo, modifica la sorgente e dividi la pagina se necessario.'),
call('Tutte le attività funzionano senza rete. I collegamenti alle fonti e a Wolfram servono solo per approfondire o ripetere le verifiche online.')),
page('Modificare senza perdere l’ordine','Le sorgenti native si trovano nella cartella Modificabili di ogni sezione.',
h('Testi e schede: Writer (.odt)','Apri la sorgente. Modifica testo, tabelle o spazi. Usa File > Esporta come > Esporta nel formato PDF. Salva nella cartella Studente o Tutor, mantenendo lo stesso nome del PDF precedente.'),
h('Mappe e schemi: Draw (.odg)','Seleziona un riquadro per spostarlo; entra nel testo per cambiarlo. I collegamenti sono oggetti modificabili. Dopo modifiche di struttura, verifica frecce, parole-legame e spazi. Esporta il PDF sovrascrivendo la sua versione precedente.'),
h('Prima di sostituire un materiale','Conserva una copia della versione precedente fuori dalle cartelle dei materiali correnti. Apri il nuovo PDF e controlla ogni pagina, anche in bianco e nero.'),
call('L’indice apre il PDF salvato: modificare una sorgente senza esportarla non aggiorna la versione da stampare.')),
page('Aggiungere e ritrovare risorse','Catalogo.ods è l’unico elenco da aggiornare.',
bullets('Crea Materie / materia / argomento e le sottocartelle Studente, Tutor e Modificabili.','Duplica un modello, prepara la sorgente e salva il PDF nella cartella corretta.','Apri Catalogo.ods, foglio Risorse. Aggiungi una riga con ID unico, titolo, materia, argomento e le altre colonne.','Nei percorsi PDF e Sorgente usa nomi relativi alla biblioteca, con / tra cartelle. Esempio: Materie/Storia/Nuovo argomento/Studente/scheda.pdf.','Salva e chiudi il catalogo. Avvia Aggiorna indice.cmd. L’aggiornamento controlla percorsi, ID e campi necessari.','Se c’è un errore, correggi la riga indicata: l’indice precedente resta disponibile. Riapri o ricarica Indice.html.'),
call('Per trasferire la biblioteca, copia tutta la cartella Laboratorio studio DSA. Per modificare e aggiornare serve Windows con LibreOffice; consultare i PDF richiede soltanto un lettore.')),
page('Valutare l’uso, adattare i materiali','La qualità della biblioteca e il suo effetto educativo richiedono controlli diversi.',
bullets('I contenuti sono originali, con fonti disciplinari e didattiche elencate nel documento Fonti e verifiche.','Il pilota copre tre argomenti, non il programma completo del triennio. Gli esempi non sono una prescrizione unica per i DSA.','Osserva scelta dello strumento, uso in un compito nuovo e correzione di errori. Conserva disponibili gli strumenti compensativi.','Fai il confronto con la scuola prima dell’uso all’esame, sulla versione concreta e sulle disposizioni dell’anno.','La routine sul compito è facoltativa. Non sostituisce una valutazione o un intervento clinico.'),
h('Da verificare negli incontri','Leggibilità per quel ragazzo o quella ragazza, quantità di informazioni, tempi, prerequisiti e utilità del supporto. La stampa fisica e l’efficacia educativa non si deducono dai controlli informatici.'),
call('Usa la scheda di osservazione per scegliere la prossima modifica. Un materiale meno denso può essere più utile, anche se contiene meno informazioni.'))
],audience='Tutor',folder='Guida all’uso',kind='Guida',topic='Uso della biblioteca')

(B/'trasversali.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2),encoding='utf-8')
print(len(docs),'documenti trasversali')
