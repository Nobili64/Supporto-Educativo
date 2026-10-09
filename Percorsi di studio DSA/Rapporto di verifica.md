# Rapporto di consegna — Metodo di studio DSA

Versione 1, 8 ottobre 2026. File quotidiano: **Metodo di studio DSA.html**, autonomo e trasferibile da solo.

SHA-256 del file verificato:
`9dc02126c38ac84f251db0dd52ae7f79e65cd09013a00a76741026429c414e12`

## Contenuto consegnato

207 percorsi: 197 attività dell’inventario originario più 10 guide per seguire la lezione e prendere appunti. La nuova sezione si trova in **Affronta un compito → In tutte le materie → Seguire la lezione e prendere appunti**, codici M21-01–M21-10.

34 mappe complete: 17 concettuali e 17 mentali. Coprono tutte le materie previste, con tre versioni della seconda lingua: francese, spagnolo e tedesco. Ogni esempio comprende materiale originale, istruzioni collegate ai nodi, costruzione progressiva, traccia, nuova prova e criteri di controllo.

Le attività coprono l’inventario concordato; non rappresentano ogni possibile consegna o ogni argomento dei programmi scolastici. Le produzioni restano su carta. Il file non assegna diagnosi, punteggi o permessi automatici e non registra dati personali o progressi.

## Riscontri per requisito

| Requisito dell’obiettivo | Evidenza corrente |
|---|---|
| Materia → ambito → attività → metodo | Tutte le 207 voci offerte nei livelli corretti in entrambi i browser; confronto degli ID esatto con inventario.json. |
| Sette passaggi per ogni metodo | 207 percorsi attraversati in tutte le sette fasi per browser; esempi, aiuti, prove, controlli e ripresa a casa presenti. |
| Tecniche applicate al compito | Revisione editoriale nei rapporti a/b/c e nelle 10 guide aggiuntive; risultati intermedi e prove nuove con controlli. |
| Adattamenti legati al bisogno e DSA | Campi passaggio, difficoltà, segnale, aiuto, obiettivo e verifica; pannello professionale con categorie esplicite e nessun instradamento diagnostico. |
| Mantenimento dei compensativi | Dichiarato nella guida, nei metodi e nelle prove con meno suggerimenti; riduzione degli aiuti didattici distinta dagli strumenti necessari. |
| Codici e ritorno ai livelli precedenti | Verificati apertura per codice anche minuscolo, errore per codice sconosciuto, cambio materia, reset degli aiuti e ricaricamento. |
| Due tipi di mappe, tutte le materie | 34 record e diagrammi; MC con parole-legame e proposizioni, MM radiali per rami. Controlli editoriali su tutti i 17 temi e relative coppie. |
| Rimandi bidirezionali nelle mappe | Per tutte le mappe: costruzione in sei passaggi, evidenziazione dei nodi dall’istruzione, apertura dell’istruzione dal nodo; attivazione da tastiera. |
| Tre prodotti stampabili | Tutte le 275 anteprime controllate in entrambi i browser: 207 schede, 34 esempi, 34 tracce. Aiuto scelto presente nella scheda corrispondente. |
| Offline e singolo file copiabile | Copia isolata contenente il solo HTML, aperta con file:// e contesto offline; zero richieste HTTP/HTTPS dell’app e zero errori JavaScript. Nessuna risorsa esterna richiesta. |
| Nessun archivio personale | Nessuna API di persistenza nel codice; selezioni solo in memoria, verificate dopo cambio metodo e ricaricamento. |
| Tastiera, focus e contrasto | Percorso completo usando Tab/Invio; focus visibile da 3 px. Contrasti testo verificati da 5,58:1 a 11,10:1; focus 5,18:1 sullo sfondo. |
| Zoom 200% e schermo stretto | Zoom nativo dei browser: devicePixelRatio da 1 a 2 e larghezza CSS dimezzata. Nessun overflow orizzontale nei percorsi provati. Schermo 375 px e tocco simulato 390 px verificati. Le mappe usano l’elenco interattivo su spazi stretti. |
| A4 e bianco e nero | 78 PDF, 150 pagine: formato A4, nessuna pagina vuota e nessuna parola fuori dai margini controllati. Rilettura visiva di 12 pagine in scala di grigi e di tutti i 34 diagrammi. |
| Fonti e proposte editoriali distinte | Registro di fonti con tipo e nota; riferimenti scientifici, istituzionali/associativi e costruzione editoriale distinta nel pannello professionale. |
| Materiali originali preservati | Tutti i file prodotti sono nella nuova cartella Percorsi di studio DSA. Non è stata usata la cartella Casi. |

## Prove effettive e loro portata

I browser installati sono stati avviati realmente tramite Playwright, in modalità senza finestra e con profili temporanei: Edge 154.0.4258.62 e Chrome 154.0.8037.98. Non si tratta di una simulazione del DOM. I due rapporti di navigazione, i due di qualità e il rapporto del tocco riportano lo stesso hash del file consegnato.

Le prove coprono le funzioni e i casi elencati; non costituiscono certificazione completa WCAG, test con lettore di schermo o test su ogni dispositivo. Il tocco è emulato. Non è stata effettuata stampa fisica: sono stati generati, analizzati e renderizzati i PDF del browser. Per lo zoom, le catture complete automatiche possono ritagliare la superficie: le immagini *zoom200-native.png ottenute direttamente dal browser mostrano il viewport corretto, e chrome-zoom200-mappa.png mostra l’elenco ingrandito.

La revisione dei contenuti e le correzioni sono documentate in manutenzione/rapporto-a.md, rapporto-b.md, rapporto-c.md, revisione-mappe.md e chiusura-revisione.md. La revisione indipendente finale è conclusa in manutenzione/revisione-finale.md: codice, corrispondenza degli hash, 18 guide disciplinari/trasversali, dieci guide nuove e sei mappe finali, senza difetti concreti aperti nel campione. Le prove effettive nei browser e la verifica visiva sono del coordinatore.

L’efficacia nei percorsi individuali deve essere osservata con gli studenti: correttezza del risultato, fatica, comprensione e trasferimento a casa e in classe. Il successo tecnico non dimostra apprendimento. Copioni, mini-testi e dati inventati sono strumenti di esercizio, non contenuti autentici da memorizzare come fatti. Le convenzioni scolastiche e i compensativi vanno adattati al compito e alla persona.

## Ripetere i controlli

Per l’uso quotidiano bastano Chrome o Edge e il file HTML. Gli strumenti seguenti servono soltanto alla manutenzione:

1. `node manutenzione/costruisci.mjs` e `node manutenzione/controlla.mjs` ricostruiscono e controllano copertura e struttura.
2. `node manutenzione/browser.test.cjs` attraversa tutti i metodi e le mappe.
3. `node manutenzione/qualita-ui.cjs` controlla livelli, anteprime, diagrammi, tastiera, contrasti e zoom nativo.
4. `node manutenzione/tocco-stampa.cjs` verifica tocco e stampa diretta.
5. `python manutenzione/verifica-stampa.py` analizza e renderizza i PDF prodotti.
6. `node manutenzione/verifica-consegna.cjs` confronta gli hash e i risultati salvati con il file corrente.

Le prove browser richiedono Playwright e browser locali; i percorsi predefiniti riflettono questo computer. BROWSER_EXE e BROWSER_LABEL selezionano browser ed etichetta; PLAYWRIGHT_MODULE è configurabile nel test di navigazione. La verifica PDF usa Pillow, pypdf, pdfplumber e Poppler. I rapporti di prova precedenti o parziali e ui-provvisoria.html non sono il prodotto da utilizzare.

