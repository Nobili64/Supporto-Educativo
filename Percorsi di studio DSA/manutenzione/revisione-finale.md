# Revisione indipendente finale

Data: 8 ottobre 2026. Perimetro: esclusivamente `Percorsi di studio DSA`; nessun accesso a `Casi` o ad altri progetti. Nessuna modifica all'implementazione o ai contenuti.

## Esito

**Nessun difetto concreto aperto identificato nella revisione svolta.** Non emergono motivi tecnici bloccanti per la consegna entro il perimetro verificato. La revisione è conclusa; questo esito non equivale a certificazione WCAG, validazione educativa o controllo semantico integrale delle 207 guide.

Hash SHA-256 del file HTML ricalcolato direttamente durante la revisione:

`9dc02126c38ac84f251db0dd52ae7f79e65cd09013a00a76741026429c414e12`

Lo stesso hash compare nei cinque rapporti `edge-risultati.json`, `chrome-risultati.json`, `edge-qualita.json`, `chrome-qualita.json`, `tocco-stampa.json`, tutti con stato PASS. Il controllo incrociato conferma che le evidenze si riferiscono al file consegnato; non consiste in una seconda esecuzione indipendente dei test browser.

## Controlli indipendenti effettuati

Letti `obiettivo.md`, `piano.md`, `app.js`, `stile.css`, `modello.html`, `costruisci.mjs`, `controlla.mjs` e `browser.test.cjs`; rilette le modifiche finali a posizionamento delle etichette SVG e regole di stampa. Consultati `chiusura-revisione.md`, `verifiche/consegna.json` e il rapporto di consegna.

| Requisito | Riscontro della revisione |
|---|---|
| Navigazione progressiva e ritorno | Materie, ambiti e attività derivano dallo stesso inventario. Le azioni di ritorno cancellano metodo, fase, aiuti e categoria; apertura per codice ricostruisce materia e ambito. Non individuati riferimenti operativi residui a metodi abbandonati. |
| Sette fasi, esempio, prova nuova, controlli e casa | Le sette viste espongono i campi previsti dal contratto. Il controllo statico confronta esattamente gli ID delle guide con l'inventario. La presenza dei campi è distinta dalla loro correttezza semantica. |
| Aiuti e categorie DSA | Selezione degli aiuti separata dalla consultazione delle categorie; nessun instradamento diagnostico. La scheda attinge agli aiuti del metodo corrente. Compensativi e riduzione dei suggerimenti sono distinti esplicitamente. |
| Mappe e interazione bidirezionale | Tipi MC/MM distinti, costruzione progressiva e selezione nodo → istruzione presenti; istruzione → nodi evidenziati presente. Elenco testuale disponibile e usato nel reflow stretto. Le tracce mantengono centro/primo nodo coerentemente con il testo del campione. |
| Offline, trasferibilità e riservatezza | Dati, stili e script incorporati; nessuna API di archiviazione o richiesta di rete nel codice applicativo letto. Fonti esterne sono collegamenti volontari, dichiarati come richiedenti Internet. Stato volatile inizializzato a ogni caricamento. |
| Stampa | Tre prodotti distinti; aiuti selezionati inclusi nella scheda; anteprima e app mutuamente visibili; stampa diretta distingue metodo, mappa e pagina corrente. Regole A4, nero su bianco e controllo delle interruzioni presenti. |
| Accessibilità dell'interazione | Elementi nativi per navigazione e aiuti; etichette del modulo, collegamento al contenuto, focus visibile e ripristino dopo anteprima. Nodi SVG attivabili con Invio/Spazio; cambio fase e istruzione sposta il focus sul contenuto pertinente. |
| Evidenze finali | Rapporti dei due browser e del tocco associati allo stesso hash. Conteggi finali dichiarati: 207 guide, 34 mappe, 275 anteprime, 78 PDF e 150 pagine. Per zoom nativo, contrasto e controllo visivo si usano le evidenze del coordinatore, non una nuova verifica autonoma. |

## Campione editoriale ragionato

Controllati obiettivi, esempi, risultati, prove nuove ed errori commentati di 18 guide, scegliendo punti con rischio di errore verificabile: `M02-03`, `M04-05`, `M07-04`, `M08-03`, `M08-04`, `M08-08`, `M09-04`, `M09-05`, `M09-09`, `M09-10`, `M10-06`, `M12-06`, `M13-08`, `M15-02`, `M16-09`, `M17-05`, `M18-01`, `M20-01`. Ricontrollati i calcoli aritmetici, geometrici e statistici riportati nel campione, non soltanto la presenza dei risultati.

Letti esempi e prove nuove delle dieci guide aggiuntive `M21-01`–`M21-10`; controllati i criteri specifici e la distinzione tra lettura del copione e prova effettiva d'ascolto. Nessun errore concreto rilevato nei risultati del campione.

Riletti semanticamente sei esempi di mappa: `MC-01`, `MM-01`, `MC-05`, `MC-09`, `MC-15`, `MM-17`. Il campione verifica la distinzione fra struttura concettuale e mentale, proposizioni con predicato, condizioni del modello scientifico introduttivo, presentazione in tedesco, pluralità delle tradizioni religiose e limite esplicito della notazione musicale testuale. Non rilevate contraddizioni fra materiale iniziale, nodi, relazioni e controllo della prova nuova negli esempi letti. La revisione delle altre mappe resta quella documentata dagli autori e dal revisore delle mappe.

## Rilievo emerso e chiuso

**P2 editoriale, risolto — `guide-d.json`, record `M21-10`, `adaptations[0].signal` e `verify`.** Nella lettura iniziale il segnale descriveva ascolto e scrittura simultanei, mentre la guida riguarda il recupero dagli appunti. La versione finale osserva formulazione della domanda e avvio della spiegazione ad appunti coperti, distinguendo accesso, comprensione e recupero. Verificata anche la nuova prosecuzione a casa, specifica del compito. Il rilievo non resta aperto.

## Limiti e precisione della documentazione

- Non è stato riletto integralmente ogni campo delle 207 guide: il campione non garantisce assenza di errori nelle voci non campionate.
- Non sono stati ripetuti i test completi Chrome/Edge né le ispezioni visive: questi risultati sono evidenze del coordinatore verificate per corrispondenza dell'hash.
- Non effettuati test con lettore di schermo, stampa fisica, osservazione con studenti o validazione clinica/educativa. Non inferire apprendimento dai PASS tecnici.
- La dichiarazione precedente in `chiusura-revisione.md` e nel rapporto di consegna, secondo cui questa revisione aggiuntiva era rimasta interrotta, descrive uno stato precedente: è superata dalla presente chiusura. L'aggiornamento dei rapporti di consegna compete al coordinatore; questo revisore ha scritto soltanto il presente file.
