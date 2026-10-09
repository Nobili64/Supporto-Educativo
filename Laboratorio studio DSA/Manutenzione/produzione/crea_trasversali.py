from produci import write_json,MAINT

IES='IES, Organizing Instruction and Study to Improve Student Learning (2007), raccomandazioni 1, 2, 5-7. https://ies.ed.gov/ncee/wwc/PracticeGuide/1'
MAP='Novak e Cañas, The Theory Underlying Concept Maps and How to Construct and Use Them (IHMC). https://cmap.ihmc.us/docs/theory-of-concept-maps'
LOCAL='Manuali locali: Cappa et al., Italiano Speciale (DSA), capp. 3-5; Hartman (a cura di), Metacognition in Learning and Instruction, capp. 1-4. Repertori locali usati come orientamento, non come validazione.'
def p(title,*blocks):return dict(title=title,blocks=list(blocks))
def H(h,t):return dict(h=h,p=t)
def L(n):return dict(lines=n)
def doc(id,title,area,audience,objective,pages,**kw):
    return dict(id=id,title=title,folder=area,subject=area,topic=title,audience=audience,objective=objective,pages=pages,**kw)

# Proposte originali adattabili: un compito concreto e una guida distinta.
METHODS=[
('M01','Comprendere la consegna','Individuare azione, prodotto e vincoli','Checklist',
'Leggi o ascolta: «Confronta due ambienti: scrivi una somiglianza e due differenze usando la tabella». Sottolinea che cosa devi fare; cerchia quanti elementi servono.',
['Azione: confrontare. Prodotto: tabella. Vincoli: una somiglianza e due differenze.','Riformula: «Devo mettere a confronto gli stessi aspetti, non fare due descrizioni separate».','Prima di iniziare, controlla se hai informazioni su entrambi gli ambienti.'],
'Nuova consegna: «Spiega in quattro frasi perché il ghiaccio fonde; usa un esempio». Costruisci la tua checklist e usala prima di rispondere.',
'La checklist nuova deve includere spiegazione, quattro frasi ed esempio. Non basta contare le frasi: occorre spiegare il passaggio di stato. Se mancano dati o una parola è ambigua, chiedere chiarimento.',
'Saltare un vincolo; partire prima di aver compreso il verbo; confondere descrivere con spiegare.'),
('M02','Pianificare la settimana','Distribuire compiti, pause e ripassi','Agenda',
'Esempio: lunedì arriva una verifica di storia per venerdì. Martedì hai 30 minuti, mercoledì 20, giovedì 25. Non riempire tutto: lascia un margine.',
['Martedì: scegli due nuclei, leggi e prepara tre domande.','Mercoledì: rispondi alle domande; riapri il testo per correggere.','Giovedì: prova una breve esposizione con lo strumento; riprendi il punto più incerto.'],
'Progetta una settimana reale: impegno, tempo disponibile, primo passo, ripasso, margine. Segna anche come cambierai il piano se un compito richiede più tempo.',
'Il piano è adeguato se considera le scadenze, i tempi disponibili e un controllo del ricordo. Non è necessario usare gli stessi intervalli dell’esempio. Alla verifica successiva confrontare tempo previsto e indicativo effettivo.',
'Riempire ogni minuto; confondere tempo seduti e lavoro utile; rimandare il ripasso all’ultima sera.'),
('M03','Avviare e dividere un compito','Completare un primo passo riconoscibile','Scaletta',
'«Studiare scienze» è troppo ampio. Primo passo possibile: aprire il paragrafo assegnato, leggere il titolo e scrivere la domanda a cui risponde.',
['Dividi il compito in azioni visibili: leggere un paragrafo, segnare due idee, spiegarle, controllare.','Scegli un blocco affrontabile e una pausa; concorda quando riprendere.','Tieni a portata lo strumento utile. Se un passaggio si blocca, indica precisamente dove.'],
'Dividi «preparare un testo su un’esperienza» in tre o quattro azioni. Esegui la prima e segna ciò che hai effettivamente prodotto.',
'Esempio possibile: scegliere l’episodio; ordinare tre eventi; scrivere una prima versione; rileggere con checklist. L’avvio deve produrre qualcosa di osservabile, anche una scelta o una domanda.',
'Usare «impegnarmi» come passo; scegliere blocchi troppo grandi; trasformare la pausa in una prova da meritare.'),
('M04','Leggere attivamente','Formulare una domanda e controllare la risposta','Domande guida',
'Testo originale: «Un vaso lasciato al sole perde acqua anche senza bollire. L’acqua evapora dalla superficie. Il fenomeno può avvenire a diverse temperature». Domanda: serve bollire per evaporare?',
['Anticipa lo scopo dal titolo. Leggi un breve segmento o ascoltalo.','Rispondi con parole tue e indica la frase che sostiene la risposta.','Segna ciò che non è chiaro; rileggi, ascolta o chiedi il significato necessario.'],
'Nuovo testo: «Una bottiglia fredda si copre di goccioline esterne. Il vapore presente nell’aria condensa sulla superficie fredda». Formula una domanda e rispondi usando il testo.',
'Prima risposta: no, l’evaporazione può avvenire senza ebollizione. Nuova domanda possibile: da dove arriva l’acqua esterna? Dal vapore dell’aria che condensa, non da una perdita della bottiglia.',
'Copiare senza capire; sottolineare tutto; confondere difficoltà nel decifrare con difficoltà di comprensione.'),
('M05','Selezionare e sintetizzare','Conservare l’idea centrale e un legame utile','Tabella informazioni',
'Testo originale: «La classe ha confrontato due contenitori uguali, uno al sole e uno all’ombra. Dopo un’ora l’acqua di quello al sole era più calda. Prima della prova entrambi contenevano la stessa quantità d’acqua alla stessa temperatura».',
['Scopo: spiegare il confronto. Tieni condizione, osservazione e controllo iniziale.','Sintesi: «A parità di quantità e temperatura iniziale, dopo un’ora l’acqua al sole era più calda».','Non trasformare un’osservazione in una legge universale senza altre prove.'],
'Scrivi una sintesi per chi deve ripetere l’esperimento. Poi una per chi vuole solo sapere il risultato: che cosa cambia?',
'Per ripetere servono anche contenitori uguali, durata e condizioni iniziali; per il risultato basta un confronto correttamente delimitato. Una sintesi cambia con il suo destinatario: non si valuta solo dalla brevità.',
'Eliminare i nessi; aggiungere opinioni; conservare dettagli irrilevanti e perdere le condizioni.'),
('M06','Scegliere uno strumento','Scegliere il supporto in base al compito','Tabella di scelta',
'Tre compiti: mettere in ordine eventi; confrontare climi; risolvere un’equazione. Quale supporto rende visibile ciò che devi fare?',
['Ordine nel tempo: cronologia. Stessi criteri su casi diversi: tabella comparativa.','Passaggi da eseguire: schema procedurale. Relazioni da spiegare: mappa concettuale.','Prova il supporto su un compito. Se non aiuta a trovare o usare l’informazione, cambialo.'],
'Devi preparare un’esposizione di due minuti. Scegli tra scaletta, formulario e cronologia; spiega la scelta e costruisci una prima versione.',
'La scaletta è una scelta plausibile per ordinare l’esposizione; una cronologia è utile se il tema richiede una sequenza storica. Non esiste una scelta corretta indipendente dal contenuto e dallo scopo. Chiedere una prova d’uso.',
'Scegliere per bellezza; attribuire automaticamente un formato alla diagnosi; togliere uno strumento perché diminuisce l’aiuto del tutor.'),
('M07','Costruire e rivedere mappe','Leggere i collegamenti come proposizioni','Mappa concettuale',
'Domanda focale: «Da dove vengono le gocce fuori da una bottiglia fredda?». Nodi: vapore dell’aria, superficie fredda, condensazione, gocce liquide.',
['Collega: il vapore dell’aria, a contatto con la superficie fredda, può subire condensazione.','Collega: la condensazione produce gocce liquide. Leggi ciascun legame come una frase.','Controlla se la mappa risponde alla domanda. Sposta, aggiungi o elimina ciò che serve.'],
'Costruisci una mappa sull’evaporazione. Scrivi anche una versione lineare equivalente di due o tre frasi. Scambia i due formati e verifica che dicano le stesse cose.',
'Devono risultare passaggio da liquido a gas, superficie e assenza dell’obbligo di bollire. Accettare layout diversi; valutare i legami. Una mappa pronta può essere analizzata, corretta e adattata. Non imporre una pagina o sole parole chiave.',
'Frecce senza parole-legame; collegamenti vaghi; confondere sequenza e causa; decorazioni che nascondono il contenuto.'),
('M08','Usare tecniche mnemoniche','Ricordare un’informazione e verificarne il senso','Carta domanda-risposta',
'Per ricordare i punti cardinali in senso orario puoi usare «Nord, Est, Sud, Ovest» con la frase inventata «Nina Esce Senza Ombrello». Il promemoria aiuta l’ordine, ma non spiega l’orientamento.',
['Scegli un’informazione breve che serve ricordare. Prima chiariscine il significato.','Crea una frase, un’immagine o un raggruppamento che riconosci facilmente.','Recupera il dato e poi usalo in un compito: dall’Est, ruotando di un quarto di giro in senso orario, vai a Sud.'],
'Prepara una carta su un contenuto del kit che stai studiando. Davanti: domanda. Dietro: risposta, esempio e promemoria facoltativo. Provala dopo un’altra attività.',
'Valutare separatamente recupero e applicazione. Se lo studente ricorda la frase ma non il dato, il promemoria va cambiato. Non usare acronimi come sostituti della comprensione; mantenere il supporto se utile.',
'Memorizzare una regola sbagliata; inventare troppi codici; scambiare familiarità con capacità di recuperare.'),
('M09','Recuperare e ripassare','Trovare ciò che ricordi e ciò da riprendere','Carte e agenda',
'Dopo una spiegazione prepara tre domande: che cosa significa? come si usa? quale errore evitare? Prova a rispondere prima di rileggere la spiegazione.',
['Concorda quali supporti restano disponibili: il recupero non richiede togliere il formulario utile.','Controlla con testo o soluzione. Correggi il punto incerto e spiegalo nuovamente.','Prevedi un altro breve recupero in un giorno diverso, adattando l’intervallo alla scadenza e all’esito.'],
'Sul tema appena studiato scrivi una domanda di spiegazione e una di applicazione. Indica quando le riproverai e che cosa ti farà anticipare o rinviare il ripasso.',
'Un ripasso utile rende visibili le risposte prima della verifica. Le date sono scelte operative rivedibili, non un calendario universale. Se la domanda è troppo difficile, fornire un indizio e registrarlo separatamente dalla correttezza.',
'Rileggere soltanto; esercitarsi sempre sullo stesso quesito; contare come autonoma una risposta appena suggerita.'),
('M10','Preparare l’esposizione orale','Spiegare un nucleo con ordine ed esempio','Scaletta',
'Tema: evaporazione. Scaletta: 1) significato; 2) esempio del vaso; 3) differenza dall’ebollizione. Apertura possibile: «L’evaporazione è il passaggio di un liquido a gas dalla superficie».',
['Scegli il destinatario e un tempo orientativo; prepara una scaletta leggibile.','Prova a spiegare con la scaletta. Il tutor fa una domanda sul perché o su un esempio.','Rivedi un solo punto alla volta: ordine, chiarezza o uso del supporto.'],
'Spiega la condensazione con tre punti. Se ti interrompi, indica sullo strumento da dove ripartire. Alla fine annota una domanda rimasta aperta.',
'Verificare contenuto, ordine e uso dello strumento separatamente. Non penalizzare automaticamente esitazioni o necessità di leggere un termine. La registrazione è facoltativa e richiede un accordo sul suo uso.',
'Imparare un copione senza comprenderlo; usare solo nomi senza legami; correggere ogni esitazione durante la prova.'),
('M11','Controllare errori e risultati','Individuare il primo passaggio da correggere','Checklist di controllo',
'Esempio: 2 + 3 × 4 = 20 è sbagliato. Prima viene la moltiplicazione: 3 × 4 = 12; poi 2 + 12 = 14. L’errore è nell’ordine delle operazioni.',
['Rileggi la domanda: il risultato risponde a ciò che era richiesto?','Controlla un criterio alla volta: dati, regola, passaggi, unità, plausibilità.','Correggi il primo passaggio errato e riprova su un quesito diverso.'],
'Una soluzione dice: «Il rettangolo di lati 3 cm e 5 cm ha area 16 cm». Individua che cosa è stato calcolato e scrivi area e perimetro corretti.',
'16 cm è il perimetro: 2 × (3 + 5). L’area è 15 cm²: 3 × 5. Distinguere scelta della grandezza, calcolo e unità. Una risposta corretta ottenuta con ragionamento errato va esplorata, non data per acquisita.',
'Cancellare senza capire; correggere solo il numero finale; usare il tempo come unico indice di riuscita.'),
('M12','Provare strumenti digitali','Confrontare accesso, accuratezza e fatica','Sintesi vocale e strumenti digitali',
'Scegli un testo breve e una domanda. Confronta lettura abituale e ascolto con una voce installata. Lo scopo è rispondere alla domanda, non finire più in fretta.',
['Sintesi vocale: prova Assistente vocale di Windows con un documento di prova; verifica voce, pause e funzionamento senza rete.','Dettatura: in un documento di prova, premi Windows + H e detta due frasi. Questa funzione richiede rete secondo la documentazione Microsoft. Ricontrolla parole e punteggiatura.','Calcolatrice: stima 18 × 4, poi controlla il risultato. Annotazione: apri una copia di PDF in Draw, inserisci un commento, salva ed esporta.'],
'Registra per ogni prova: strumento, attività, errori, aiuti, fatica riferita e rete richiesta. Non usare dati personali per la prova online. Il tutor può trascrivere come alternativa senza rete.',
'Calcolo atteso: 72. Valutare se ascolto e dettatura aiutano il compito; le correzioni restano necessarie. LibreOffice Draw e Calcolatrice sono utilizzabili localmente. La disponibilità di una voce non prova che tutte le voci funzionino offline: provarla sul computer.',
'Confondere riconoscimento vocale e sintesi; accettare una trascrizione non riletta; chiamare offline una funzione soltanto perché l’app è installata.')]

all_docs=[]
for id,title,goal,tool,example,steps,transfer,solution,errors in METHODS:
    source=MAP if id=='M07' else IES if id in ['M02','M08','M09','M10'] else LOCAL
    if id=='M12':source='Microsoft Support: Use voice typing to talk instead of type on your PC; Complete guide to Narrator. https://support.microsoft.com/en-us/accessibility/windows/use-voice-typing-to-talk-instead-of-type-on-your-pc ; https://support.microsoft.com/en-us/accessibility/windows/narrator/complete-guide-to-narrator'
    common=dict(kit=id,tool=tool,task=goal,sources=source)
    student=doc(id+'-studente',title,'Metodo di studio','Studente',goal,[p(title,H('Obiettivo',goal),H('Un esempio',example),dict(h='Prova in tre passi',bullets=steps),H('Tocca a te',transfer),L(3))],**common)
    tutor=doc(id+'-tutor',title+' - guida','Metodo di studio','Tutor',goal,[p('Guida: '+title,H('Prima e durante','Chiedi come affronta già il compito. Mostra un passaggio, invitalo a provare e concorda quale aiuto usare. La scheda è una proposta educativa adattabile.'),H('Risposta e criteri',solution),H('Errori da esplorare',errors),H('Adattamenti e osservazione','Riduci il numero di elementi, offri lettura o risposta orale, amplia lo spazio su un foglio. Registra correttezza, aiuti, uso dello strumento, tempo indicativo e fatica in campi separati.'),H('Prossimo incontro','Riprendi la stessa funzione su un contenuto diverso. Chiedi allo studente che cosa terrebbe o cambierebbe nello strumento.'),H('Riferimenti',source))],**common)
    all_docs += [student,tutor]
write_json(MAINT/'produzione/dati/trasversali-metodo.json',all_docs)
print(len(all_docs),'documenti di metodo')
