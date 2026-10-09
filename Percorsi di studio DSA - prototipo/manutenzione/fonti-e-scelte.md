# Fonti, adattamenti e limiti

## Guida W3C fornita dall’utente

Documento: `../Making Content Usable for People with Cognitive and Learning Disabilities.html`, rispetto alla cartella del prototipo. SHA256: `2b8b79110eaa5b5dae3901762d63ba35b37f7c6b11c36ea39b6b8b7c2ede ecca` (senza lo spazio: vedi manifest finale).

Applicazioni concrete:

- §4.4.1, parole chiare: definizioni immediate di prosa, incognita, membro, morale, categoria e parola chiave.
- §4.4.12, contenuto implicito: espressioni figurate spiegate vicino al testo; precisazioni come “spesso” e “può” mantenute.
- §4.5.7, passaggi espliciti: esempio commentato, prova e controllo separati; istruzioni prima dell’azione.
- §4.6.3, quantità di contenuto: una scelta alla volta, un passaggio per schermata, guida dell’adulto separata. La brevità non è stata usata come obiettivo indipendente dalla comprensione.
- §4.7.5, carico di memoria: equazione, frase, testo o mappa necessari restano nel passaggio corrente. Il lavoro di recupero degli appunti è un’attività didattica dichiarata, non un requisito per navigare.
- §4.9.1, controllo: nessuna animazione, nessun timer, avanzamento manuale e ritorno dagli aiuti.
- §5, osservazione con utenti: griglia da utilizzare negli incontri. Nessuna prova con studenti reali è stata eseguita durante la realizzazione.

Riferimento pubblico: https://www.w3.org/TR/coga-usable/ . Il documento è una guida di progettazione; la sua applicazione non costituisce certificazione di conformità o validazione clinica.

## Metodo di studio CIU

File originali forniti, ritrovati nella radice `Supporto compiti`. PDF di 210 pagine; nei metadati l’autrice è Melissa Scagnelli. Le pagine qui indicate sono le pagine fisiche del PDF.

| Pagine | Impiego nel prototipo |
|---|---|
| 22–27 | Separazione prima/durante/dopo; pagina degli appunti; segnali linguistici che annunciano idee ed esempi; completamento successivo. |
| 96–100, 131 | Prima delle mappe: scegliere parole chiave e distinguere gruppo/dettaglio; esercizi nuovi e contestualizzati sulla favola. |
| 45–58, 125, 139 | Leggere o ascoltare prima di selezionare; rielaborare e controllare il significato. I nomi inglesi delle fasi non sono stati aggiunti al carico dello studente. |
| 208–209 | Riformulare conservando il significato e provare il procedimento su materiale diverso. |
| 210 | Feedback sul comportamento osservato e aiuti graduati, senza giudizi sulla persona. |

La guida AI è un indice secondario generato automaticamente. Sono stati controllati i passi pertinenti sul TXT e sul PDF, con esame visivo delle pagine 26, 98, 100 e 208. La parafrasi è a pagina 208, mentre pagina 209 tratta la generalizzazione. Alcuni numeri nell’indice AI superano le 210 pagine del PDF: non sono stati usati come riferimenti.

Scelte critiche: non sono stati importati percentuali di miglioramento della memoria (p. 93), tempi o quantità fissi come prescrizioni universali, né classificazioni dello studente per motivazione o successo. Queste affermazioni richiederebbero verifiche e contestualizzazione ulteriori. Le indicazioni di disposizione radiale (pp. 115–118) non sono state usate per confondere mappa mentale e mappa concettuale.

Esempi, versi, testi di ascolto e mappe del prototipo sono originali. Non sono state riutilizzate le immagini o le pagine di esercizi dei libri riprodotti nelle slide CIU.

SHA256 delle fonti:
- PDF: `226d727b9914b38c226dbbfa2d87b2f8548f833ad9a338c3c5752b08ef2d4eff`
- TXT: `5729695de58fce6cd5fe298591cc37c563cb2b24562e39b7c6b88f4d838c3ccc`
- Guida AI: `960fa2ca2652d811ab16f80954f82819f8d148cce9cd0d9e08878587a0e4d0dc`

## Altri riferimenti

- Novak e Cañas, https://cmap.ihmc.us/docs/theory-of-concept-maps : concetti, domanda di partenza, parole-legame e proposizioni. Le mappe sono modelli introduttivi, con limiti dichiarati.
- Cornell University, https://lsc.cornell.edu/how-to-study/taking-notes/cornell-note-taking-system/ : organizzazione in note, domande e sintesi; adattamento alla scuola media.
- AID, https://www.aiditalia.org/che-cosa-sono-i-dsa : distinzione delle aree di difficoltà. Gli adattamenti al singolo compito restano proposte da verificare nell’uso.
- Wolfram Language: richieste e risposta conservate in `wolfram-verifica.json`. Verificati risultati, equivalenze delle trasformazioni e un procedimento errato; non verificata la comprensibilità mediante il calcolo.

## Verifica dello zoom

La prima simulazione con CSS `zoom:2` non dimostrava lo zoom nativo. È stata sostituita da un test con profili temporanei Edge separati: `partition.default_zoom_level` è un dizionario con chiave di partizione `x`, coerentemente con il codice Chromium `chrome/browser/ui/zoom/chrome_zoom_level_prefs.cc`. Il test richiede DPR raddoppiato, viewport CSS dimezzato, CSS zoom ancora 1 e navigazione entro il viewport. Codice di riferimento: https://chromium.googlesource.com/chromium/src/+/lkgr/chrome/browser/ui/zoom/chrome_zoom_level_prefs.cc .
