# Istruzioni per gli agenti che scrivono i percorsi

Questo è il testo dato a ogni agente nelle ondate di scrittura. Un agente riceve **un gruppo** di `da-fare.json`: al posto di `{CARTELLA}` va il percorso assoluto della cartella `manutenzione`, al posto di `{ELENCO}` la lista dei percorsi del gruppo (una riga per percorso: `- codice — materia / ambito — «titolo»`), al posto di `{NOTA}` il campo `nota` del gruppo (se è vuoto, si toglie la riga).

---

Scrivi in italiano alcuni percorsi didattici per uno strumento HTML di metodo di studio per ragazzi di 11-14 anni con DSA.

Cartella di lavoro: {CARTELLA}

PRIMA DI TUTTO leggi per intero {CARTELLA}/contratto-scrittura.md: contiene tutte le regole, il formato JSON, i modelli da imitare e la procedura. Poi leggi per intero almeno due modelli in {CARTELLA}/contenuti/ (M02-02.json e M08-08.json; più M21-04.json se un tuo percorso riguarda ascolto o appunti; MC-01.json e MM-01.json se riguarda mappe).

I tuoi percorsi:
{ELENCO}

Indicazioni specifiche per questo gruppo: {NOTA}

In {CARTELLA}/contenuti/ ci sono già più di cento percorsi scritti da altri. Guarda i titoli di quelli vicini ai tuoi argomenti: non ripeterne gli esempi. Se rimandi a un altro percorso, citane il titolo esatto: quello del campo "title" del suo file, se esiste, altrimenti quello di {CARTELLA}/catalogo.json.
Se uno dei tuoi file esiste già e supera node valida.mjs senza errori, saltalo: è già stato scritto.

Per ciascuno, uno alla volta:
1. Cerca il record di partenza con lo stesso id in `../../Percorsi di studio DSA/manutenzione/guide-a.json`, `guide-b.json`, `guide-c.json` o `guide-d.json` (per le mappe: `mappe.json` e `temi-mappe.json` nella stessa cartella). È solo un inventario telegrafico: riscrivi tutto.
2. Progetta la sequenza di schermate (8-18, secondo la difficoltà) seguendo il contratto.
3. Verifica con Python ogni calcolo e controlla ogni fatto. Se non sei sicuro di un fatto, cambia esempio.
4. Scrivi {CARTELLA}/contenuti/<id>.json.
5. Esegui `node valida.mjs <id>` nella cartella di lavoro e correggi finché non ci sono errori; leggi anche gli avvisi.
6. Rileggi ogni schermata come un ragazzo di 13 anni con dislessia e migliora ciò che non è chiaro.

Poi passa al successivo. Scrivi ogni file appena è pronto: non accumulare.

Vincoli: scrivi SOLO i file contenuti/<id>.json elencati sopra. Non eseguire costruisci.mjs e non modificare app.js, stile.css, catalogo.json, fonti.json, valida.mjs, i percorsi di altri o qualsiasi file fuori da contenuti/. Non aprire la cartella Casi. Nessun dato personale.

Alla fine restituisci un riepilogo: per ogni percorso completato il numero di schermate, che cosa hai verificato e le note; i percorsi non completati con il motivo; i dubbi didattici da sottoporre alla persona che segue i ragazzi.
