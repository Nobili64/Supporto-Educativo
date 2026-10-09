# Controllo visivo — tappa C

Data: 1 ottobre 2026. Operatore: agente redattore. Non è la revisione indipendente della tappa F.

## Copertura

Ispezionate le tavole complete del manuale (pagine 1–150), dell’allegato ragazzo (1–25) e dell’allegato clinico (1–16): 191 pagine complessive. Controllati titoli, tabelle, margini, foliazione, continuità dei contenuti, spazi di risposta e leggibilità delle figure.

Ingrandimenti specifici: manuale 47, 79, 84, 99, 135; ragazzo 3, 9, 10, 20, 25; clinico 15–16. Dopo le correzioni alle righe A4 sono state riaperte le tavole ragazzo 7–24 e clinico 13–16 e i campioni singoli pertinenti.

Secondo rendering con Poppler sul PDF finale: manuale 79, 84, 99, 135; ragazzo 10, 20, 25; clinico 15, 16. Tutte le nove immagini sono state ispezionate. Le figure vettoriali, le frecce, il tratteggio, le righe e il testo risultano leggibili anche con questo motore.

## Difetti individuati e risolti

1. La nota della fase 2 e la nota della figura S19 finivano su una pagina residua. Corrette la larghezza della tabella e la dimensione della figura, senza ridurre il corpo del testo.
2. La conversione Markdown aggiungeva interruzioni HTML dentro i diagrammi SVG: le figure non apparivano correttamente. Ora i diagrammi sono preservati durante la conversione e renderizzati come vettori.
3. La classe delle due righe attivava una griglia a due colonne e, nelle versioni concrete, un secondo retino di righe. Ora le righe sono continue, verticalmente separate e senza sovrapposizioni.
4. Nell’indice degli allegati due coppie di titoli del blocco B erano indistinguibili. Aggiunti codice e variante nell’indice cumulativo, lasciando intatta la consegna B.

Non risultano ulteriori difetti di impaginazione nelle immagini ispezionate. La verifica non è una prova su stampante né una valutazione di comprensione da parte di ragazzi o clinici.

Le impronte dei PDF finali sono in `esito-controlli.json` e `manifesto-consegna.json`. Le immagini e i log restano nella cartella di lavoro `.studiare-dnav/tappa-c/qa`.
