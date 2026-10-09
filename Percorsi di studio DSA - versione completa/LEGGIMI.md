# Metodo di studio DSA — versione completa

Apri **Metodo di studio DSA.html** con Edge o Chrome. È un file autonomo: puoi copiarlo da solo su un altro computer e usarlo senza Internet.

Questa versione estende a tutto il repertorio (207 lavori e 34 mappe) l’impianto del prototipo *Cinque percorsi guidati*: una sola idea per schermata, **Avanti** e **Indietro**, l’aiuto **Mi serve una spiegazione**, la guida per il professionista separata, tre schede A4 da stampare per ogni percorso.

Il prototipo resta nella sua cartella, invariato, per la prova con i ragazzi.

## Come trovare un percorso

- **Affronta un compito → materia → ambito → lavoro.** Se una materia ha un solo ambito, si passa direttamente ai lavori.
- **Costruisci una mappa → mappa concettuale o mentale → materia → argomento.**
- **Cerca un percorso:** scrivi una parola del compito (per esempio «riassunto», «frazioni») oppure il codice stampato sulle schede (per esempio «M02-02»).

## Stato dei lavori

Il file contiene solo i percorsi già scritti e controllati. Gli altri compaiono man mano che vengono completati, in quest’ordine:

1. Italiano, Matematica e attività trasversali (organizzare lo studio, seguire la lezione);
2. Storia, Geografia, Scienze, Inglese;
3. Seconda lingua, Tecnologia, Arte e immagine, Musica, Educazione fisica, Educazione civica, Religione, Attività alternative, Strumento musicale;
4. Mappe concettuali e mentali per ogni materia.

## Che cosa controlla ogni percorso

Ogni percorso, prima di entrare nel file, supera due controlli automatici:

- **`valida.mjs`**: fasi nell’ordine giusto (preparazione, esempio spiegato, prova guidata, compito nuovo, controllo, ripresa a casa); da 8 a 18 schermate; frasi di massimo 25 parole; indice di leggibilità Gulpease di almeno 60 per ogni testo; nessuna parola dell’elenco da evitare («conservare», «esplicitare», «pertinente»…); mappe e tabelle entro i limiti che restano leggibili.
- **`verifica-browser.cjs`**: tutte le schermate percorse senza connessione, su schermo largo e su telefono; aiuto e ritorno; nessun riquadro delle mappe sovrapposto e nessun testo sotto i 14 pixel; guida e schede di stampa; ogni lavoro raggiungibile dalla scelta guidata.

Questi controlli dicono che il percorso è **ben formato e leggibile**, non che è **efficace** con un ragazzo. Quello si osserva negli incontri, con la *Griglia di osservazione* del prototipo.

## Manutenzione

Nella cartella **manutenzione**:

- `contenuti/` — un file per percorso (`M01-09.json`, `MC-03.json`…). È l’unico posto dove si modificano i testi.
- `contratto-scrittura.md` — le regole per scrivere o correggere un percorso.
- `catalogo.json` e `fonti.json` — elenco dei percorsi e delle fonti.
- `app.js` e `stile.css` — l’interfaccia, comune a tutti i percorsi.

Dopo una modifica, da `manutenzione`:

```
node valida.mjs
node costruisci.mjs
node verifica-browser.cjs
```

Per la verifica nel browser servono Node.js e Playwright; su un computer diverso da quello originale impostare `PLAYWRIGHT_MODULE` e `BROWSER_EXE`.
