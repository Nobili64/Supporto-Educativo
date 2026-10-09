# Revisione editoriale indipendente dei 34 esempi di mappe

Revisione del file `mappe.json` con SHA-256 **0d2241a558d8e5a1ce04b911fb09155b4ddafc506e56ca14c265e846c153a651**, letto l’8 ottobre 2026. Copertura: tutti i 17 temi, 17 mappe concettuali MC-01–MC-17 e 17 mappe mentali MM-01–MM-17. Il file sorgente non è stato modificato da questo revisore. Questo rapporto riguarda contenuto e consegne; non verifica il disegno dell’interfaccia.

## Esito

Sono presenti rilievi editoriali da correggere prima di considerare tutti gli esempi conformi al criterio dichiarato **“ogni collegamento si legge come una frase sensata e corretta”**. I casi principali sono predicati mancanti, un nodo preposizionale usato come soggetto e una duplicazione nella mappa dello spartito. Non sono errori clinici né prove di inefficacia delle mappe.

La distinzione fra tipi è effettiva nelle istruzioni: le MC partono da una domanda e chiedono parole-legame/proposizioni; le MM partono dal centro, costruiscono rami e chiedono di motivare le associazioni. Tutte le coppie condividono nodi e topologia; tutte le MM hanno etichette dei collegamenti vuote. **La topologia identica non è, da sola, un errore**: anche una mappa concettuale può avere una struttura prevalentemente gerarchica. Non va però insegnato che una mappa concettuale è semplicemente una mentale a cui aggiungere qualsiasi testo sulle frecce.

## Rilievi prioritari e correzioni proposte

### R01 — Proposizioni con esempi prive di predicato

Localizzazioni:

- MC-02 e1/e3/e5/e7: per esempio «fonti scritte per esempio una lettera».
- MC-05 e7: «cambiamenti di stato per esempio fusione: solido → liquido».
- MC-06 e1/e3/e5/e7: per esempio «nome per esempio My name is Alex.».
- MC-07 e1/e3/e5/e7, MC-08 e1/e3/e5/e7, MC-09 e1/e3/e5/e7: collegamenti «exemple», «ejemplo», «Beispiel».
- MC-10 e5/e7: «proprietà variabili per esempio spessore e assorbenza»; «usi diversi per esempio scrittura e imballaggio».
- MC-13 e7: «attenzione ai segnali per esempio disagio da comunicare».
- MC-14 e3/e5/e7: esempi di diritti, responsabilità e riparazione.
- MC-15 e7: «attività comunitarie per esempio preghiera e incontro».

Sono gruppi nominali o accostamenti esemplificativi, non le frasi complete richieste dalle istruzioni. L’associazione è spesso corretta: il rilievo riguarda **la forma proposizionale dichiarata**, non la pertinenza dell’esempio.

Proposte concrete: «fonti scritte — comprendono, per esempio — una lettera»; «cambiamenti di stato — comprendono, per esempio — la fusione»; «nome — può essere comunicato con la frase — “My name is Alex”»; «usi diversi — comprendono, per esempio — scrittura e imballaggio». Per MC-13 riformulare il ramo come «attenzione ai segnali — comprende — comunicare il disagio». Quando cambia una parola-legame, aggiornare anche la frase citata nell’istruzione relativa: non basta cambiare `edges`.

### R02 — MC-13: nodo n1 non adatto come soggetto

e1 produce «all’attività successiva richiede esercizi pertinenti». Il nodo n1 contiene la preposizione che serve a e0, ma non può diventare il soggetto di e1.

Proposta: n1 «attività successiva», e0 «prepara a svolgere l’», e1 «richiede esercizi di preparazione». Oppure inserire un nodo «scelta degli esercizi» e collegarlo alla pertinenza rispetto all’attività. La seconda opzione rende più chiaro che è il riscaldamento a includere esercizi preparatori.

Nello stesso esempio e3 «una progressione da impegno lieve a maggiore» manca di un predicato: usare «va da». e5 «mobilità articolare con movimenti controllati» può diventare «mobilità articolare — viene svolta con — movimenti controllati». Aggiornare testo e istruzioni; se cambia il nome del nodo, aggiornare anche MM-13 e lo scaffold. Questi interventi non introducono durate o prescrizioni individuali.

### R03 — MC-17: duplicazione e formulazione incompleta

- e3 legge «note e chiave la chiave orienta la lettura delle posizioni». Il nodo composto e il collegamento ripetono «chiave» e producono una frase malformata. Proposta: n3 «chiave», e2 «specifica le altezze anche mediante la», e3 «orienta», n4 «la lettura delle posizioni delle note». In alternativa separare note e chiave in due nodi con relazioni proprie.
- e5 legge «figure e pause rappresentano suoni e silenzi di durata». «Di durata» resta senza complemento e descrive poco precisamente la funzione. Proposta: n6 «durate di suoni e silenzi»; e5 «rappresentano le». La frase diventa «figure e pause rappresentano le durate di suoni e silenzi».
- e7 «battute separate da stanghette»: usare «sono separate da».

Il testo di partenza distingue correttamente durata notata e durata reale dipendente dal tempo; conservarlo. Correggere le istruzioni 3/4/5 e, per i nodi cambiati, la corrispondente MM-17.

### R04 — Altre forme non leggibili come proposizioni autonome

- MC-10 e3: «un impasto acquoso che viene steso, pressato e asciugato» è un gruppo nominale con relativa, non una proposizione autonoma. Sostituire «che viene» con «viene».
- MC-11 e3/e5/e7: «arancione/verde/viola classificato come secondario» richiede «è classificato come». e2/e4/e6 contengono «mescola … per arancione/verde/viola»: aggiungere «ottenere» dopo «per», oppure «associa la miscela di … al colore …» per mantenere chiaro che è un modello.
- MC-15 e1/e3/e5: «chiese associate al cristianesimo» e analoghe richiedono «sono associate…» nel criterio di lettura come frase.
- MC-16 e5: «ascolto permette comprendere le proposte» richiede «permette di».

Le omissioni ordinarie di articoli nei nodi non sono qui trattate come difetti automatici: sono stati segnalati i casi in cui manca o si rompe la relazione predicativa. Aggiornare sempre le istruzioni che riportano le stesse frasi.

### R05 — Mini-prova dello spartito non autonoma

MC-17/MM-17 `transfer` richiede «un semplice spartito scelto dal docente», non fornito nel record. Per una seduta è un’attività applicabile quando il docente consegna lo spartito; per una mini-prova autonoma a casa manca il materiale.

Proposta: fornire un piccolo estratto originale con chiave, figure, pausa e stanghette. Se si vuole evitare un’immagine in questa fase, fornire una rappresentazione simbolica con legenda completa e dichiarare che verifica il significato dei simboli, non la lettura di posizioni reali sul pentagramma. Non chiamare completa una prova che richiede un materiale ancora da scegliere.

### R06 — Modelli di relazione plurilingui da rendere coerenti

MC-07/08/09 combinano radice e nodi nella lingua studiata con «comprende» in italiano e un’etichetta nominale per l’esempio. Frasi modello quali «Sich vorstellen comprende Name» non sono una frase tedesca, italiana o una spiegazione bilingue formulata chiaramente. Le frasi di presentazione e le mini-prove, invece, sono corrette nei dati e nelle strutture fornite.

Proposta didattica semplice: nodi metalinguistici in italiano («Presentarsi in tedesco», «nome», «età», ecc.), collegamenti italiani completi («può comunicare», «si esprime, per esempio, con») e frasi tedesche/francesi/spagnole nei nodi esempio fra virgolette. È possibile scegliere relazioni interamente nella lingua studiata, ma richiede una revisione grammaticale completa. Non basta tradurre isolatamente «comprende».

## Miglioramenti editoriali distinti dai difetti prioritari

- MC-01/MM-01: la morale proposta è plausibile, ma il vento che porta via il cibo non è una conseguenza causale della derisione. Evitare una freccia «derisione causa vento/perdita». Se si vuole esercitare una sequenza conflitto-conseguenza, aggiungere nel mini-racconto una scelta del corvo (es. lasciare il cibo esposto) e una scelta prudente della formica. Non c’è un’unica morale da imporre se motivata dagli eventi.
- MC-05: etichette «solida/liquida/gassosa» sono utili come rami della MM. Nella MC, per una lettura indipendente di ogni collegamento, «materia allo stato solido/liquido/gassoso» è più chiaro di «solida ha…». Nel nodo del liquido riprendere «forma della parte del recipiente occupata», già presente correttamente nel testo.
- MC-10/MM-10: la prova confronta foglio e cartone senza fornire campioni o descrizioni di spessore/struttura. La soluzione non deve inventare misure. Per uso autonomo aggiungere due schede fittizie complete, oppure chiedere esplicitamente di annotare ciò che è ignoto. Già positivo il limite sulla riciclabilità e le indicazioni locali.
- MC-11/MM-11: la mini-prova aggiunge una mescolanza reale senza specificare materiali disponibili. Rendere facoltativa la prova pratica e offrire una variante su carta con i dati del testo; se realizzata, distinguere miscela attesa nel modello ed esito effettivamente osservato. Non è un difetto del modello RYB quando è qualificato come tradizionale e distinto da RGB/CMY.
- MC-13/MM-13: `transferCheck` contiene una corretta cautela sulle durate, ma esplicitare anche la progressione cammino → corsa leggera e il disagio da comunicare renderebbe i criteri più verificabili senza prescrivere un allenamento.
- MC-16: «ruoli distribuiscono compiti» è una scorciatoia poco precisa: sono persone o un accordo ad assegnare i compiti; il ruolo li definisce. Possibile relazione «ruoli — definiscono — compiti». Conservare il controllo della comprensione comune.
- Tutte le coppie: `transfer` e `transferCheck` sono identici tra MC e MM. Non è automaticamente sbagliato usare lo stesso contenuto, ma aggiungere nel controllo della MC due relazioni verbalizzabili e nel controllo della MM collocazione dei dettagli e motivazione dei rami renderebbe il trasferimento del metodo più esplicito. I criteri generali già differiscono e quindi la distinzione non è assente.

## Copertura dei 17 temi

| Coppia | Esame di contenuto e mini-prova | Esito |
|---|---|---|
| MC/MM-01 Favola | Personaggi possibili, conflitto, morale motivata; mini-racconto completo | Associazioni adeguate; cautela causale proposta sopra |
| MC/MM-02 Fonti storiche | Tipi di fonti, sovrapposizione, punto di vista e tre esempi nuovi | Contenuto adeguato; R01 sui predicati degli esempi |
| MC/MM-03 Orientamento | Nord della pianta dichiarato; biblioteca est e parco sud | Prova verificabile, nessun errore nel rapporto direzionale |
| MC/MM-04 Operazioni | 4+3=7, 9−5=4, 3×4=12, 12:3=4; prova 8/4/12/3 | Calcoli corretti; resto e divieto di zero nel testo |
| MC/MM-05 Stati | Modello introduttivo qualificato; ghiaccio/acqua/aria e fusione | Contenuto adeguato; R01 e chiarezza dei nodi adjectivali |
| MC/MM-06 Inglese | Età con be; prova Sam/11/Spain/football | Frasi corrette; R01 sulle relazioni verso gli esempi |
| MC/MM-07 Francese | avoir per età; apostrofi; Camille/11/Paris/sport | Frasi corrette; R01/R06 sui legami |
| MC/MM-08 Spagnolo | tener per età; gusta con musica/calcio singolari | Frasi corrette; R01/R06 sui legami |
| MC/MM-09 Tedesco | sein per età, wohnort, mag; Kim/11/Berlin/Sport | Frasi corrette; R01/R06 sui legami |
| MC/MM-10 Carta | Materiale, fasi, proprietà e usi; riciclo non dedotto dal solo nome | R01/R04; precisare dati della prova autonoma |
| MC/MM-11 Colori | RYB qualificato, RGB/CMY distinti, dipendenza dai pigmenti | R04; pratica reale facoltativa con variante su carta |
| MC/MM-12 Suono | Altezza/intensità/durata/timbro; tamburo senza altezza inventata | Adeguato nei dati e nella soluzione |
| MC/MM-13 Riscaldamento | Progressione, pertinenza, segnali, nessuna durata prescritta | R02/R01; controllo della prova da concretizzare |
| MC/MM-14 Convivenza | Diritti/responsabilità/riparazione; interruzioni e restituzione di spazio | Contenuto adeguato; R01 sui predicati degli esempi |
| MC/MM-15 Culto | Associazioni delimitate e differenze interne riconosciute | Contenuto adeguato; R01/R04 sui legami |
| MC/MM-16 Cooperazione | Obiettivo, compiti, ascolto, verifica condivisa | R04; precisare ruolo/assegnazione, nessuna riduzione a mera divisione |
| MC/MM-17 Spartito | Pentagramma/chiave/durate/battute; tempo distinto dai secondi | R03 e R05 prioritari |

## Evidenza e limiti

Eseguiti parsing JSON, conteggio 34 record, confronto delle 17 coppie, controllo dei riferimenti a nodi, controllo delle etichette vuote nelle MM, esame di domande/testi/nodi/proposizioni/mini-prove/errori e lettura degli scaffold iniziali/finali di tutte le mappe. Tutte le MC citano le proprie proposizioni nelle istruzioni 2–5; tutte le MM insegnano costruzione per rami negli stessi passaggi. Nessun ID o riferimento a nodo fuori dall’esempio rilevato.

La revisione valuta la coerenza rispetto ai testi e alle conoscenze scolastiche di base. Non è validazione clinica, verifica sperimentale dell’apprendimento, revisione normativa o certificazione della pronuncia. Il passaggio da un sospetto a un rilievo qui è basato su stringhe citate e riferimenti specifici: le proposte su causalità della favola, uniformità bilingue e materiale autonomo sono tenute distinte dalle frasi effettivamente malformate. Dopo le correzioni occorre rigenerare e rileggere le proposizioni complete: un controllo del JSON da solo non può verificarne il significato.
