# Laboratorio mappe concettuali e mentali

Pagina interattiva per spiegare a ragazzi e ragazze delle medie come costruire mappe concettuali e mappe mentali. Questa cartella contiene tutto quello che serve per continuare il lavoro in locale con ChatGPT.

## Che cosa c'è nella cartella

| File | A che cosa serve |
|---|---|
| `Mappe concettuali e mentali.html` | La pagina. Un solo file, senza installazioni: si apre con doppio clic nel browser. |
| `Istruzioni per ChatGPT.md` | Le regole fisse per ChatGPT: chi sei, come vuoi le risposte, come modificare il file. Da incollare nelle istruzioni del progetto. |
| `Contesto e decisioni.md` | Lo stato del lavoro: obiettivo, fonti, decisioni già prese, struttura del file, problemi aperti, prossimi passi. |
| `Prompt iniziale.md` | Il primo messaggio da incollare in una nuova chat. |
| `fonti/W3C linee guida accessibilità cognitiva (estratto).md` | Estratto delle linee guida W3C usate per la revisione (versione leggera da caricare). |
| `strumenti/controllo-anteprima.js` | Facoltativo: crea immagini della pagina su computer e telefono, in tema chiaro e scuro, e segnala errori. |

Le altre fonti sono già nella repository e non sono duplicate qui:

| Fonte | Percorso nella repository |
|---|---|
| Rosati (2013), Mappe concettuali e mappe mentali: testo | `Assets (markdown)/Mappe concettuali e mappe mentali.md` |
| Rosati (2013): libro in PDF, con le figure | `Assets (pdf, epub)/Rosati - Mappe concettuali e mappe mentali (2013).pdf` |
| Dispense del corso «Metodo di studio» | `Metodo di studio CIU.txt` (e `Metodo di studio CIU.pdf`) |
| Linee guida W3C complete | `Making Content Usable for People with Cognitive and Learning Disabilities.html` (e `.pdf`) |

## Come partire con ChatGPT

1. In ChatGPT crea un **Progetto** (per esempio «Laboratorio mappe»).
2. Nelle **istruzioni del progetto** incolla tutto il testo di `Istruzioni per ChatGPT.md`.
3. Nei **file del progetto** carica:
   - `Mappe concettuali e mentali.html`
   - `Contesto e decisioni.md`
   - `Assets (markdown)/Mappe concettuali e mappe mentali.md`
   - `Metodo di studio CIU.txt`
   - `fonti/W3C linee guida accessibilità cognitiva (estratto).md`
4. Apri una nuova chat nel progetto e incolla il testo di `Prompt iniziale.md`.

Se non usi i Progetti: in una chat normale allega gli stessi cinque file e incolla prima le istruzioni, poi il prompt iniziale.

## Come applicare le modifiche

Il file HTML è lungo (circa 1.400 righe). Se chiedi a ChatGPT di riscriverlo tutto, rischi che salti dei pezzi. Conviene questo metodo:

1. Chiedi a ChatGPT le modifiche come blocchi **«cerca questo testo → sostituisci con questo»**. Le istruzioni glielo chiedono già.
2. Apri `Mappe concettuali e mentali.html` con un editor di testo (per esempio Visual Studio Code).
3. Per ogni blocco: cerca il testo indicato (Ctrl+F oppure Cmd+F), sostituiscilo, salva.
4. Ricarica la pagina nel browser e controlla.
5. Quando la modifica funziona, ricarica il file aggiornato in ChatGPT, così la volta dopo lavora sulla versione giusta.

## Come controllare la pagina

Controllo di base, sempre:

- Apri il file nel browser.
- Restringi la finestra fino alla larghezza di un telefono: la pagina non deve scorrere di lato.
- Prova il tema scuro del sistema operativo.
- Prova i pulsanti «In classe» e «Da solo», le tre grandezze del testo e «Ascolta».

Controllo automatico, facoltativo. Serve Node.js installato.

```bash
cd "Laboratorio mappe concettuali e mentali/strumenti"
npm install playwright
npx playwright install chromium
node controllo-anteprima.js "../Mappe concettuali e mentali.html"
```

Lo script salva le immagini nella cartella `strumenti/anteprime/` e scrive nel terminale gli errori della pagina e la larghezza misurata. Se la larghezza è maggiore della finestra, qualcosa esce dallo schermo.

## Salvare il lavoro su GitHub

La cartella fa parte della repository `Nobili64/Supporto-Educativo`, sul ramo `claude/eloquent-faraday-89wf3m`. Per averla in locale:

```bash
git clone https://github.com/Nobili64/Supporto-Educativo.git
cd Supporto-Educativo
git checkout claude/eloquent-faraday-89wf3m
```

Dopo le modifiche:

```bash
git add "Laboratorio mappe concettuali e mentali"
git commit -m "Descrivi qui la modifica"
git push
```

## Versione pubblicata su Claude

Esiste anche una versione pubblicata come artefatto di Claude: https://claude.ai/artifact/KZqpfHTNqmZ4aMSEhyBzXS. Non si aggiorna da sola con le modifiche locali. Per ripubblicarla da Claude bisogna togliere dal file le righe di apertura e chiusura del documento (`<!doctype html>`, `<html>`, `<head>`, `<meta>`, `</head>`, `<body>`, `</body>`, `</html>`): Claude le aggiunge da solo.
