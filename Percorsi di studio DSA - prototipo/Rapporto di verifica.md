# Rapporto di verifica — Cinque percorsi guidati

Data: 9 ottobre 2026.
File verificato: `Cinque percorsi guidati.html`.
Impronta SHA-256: `bb1392cb61090ac18ec1e0f643b0d9cb74bdcbc62b33d72e7508123185789e7a`.

Il rapporto separa tre tipi di controllo: **tecnico** (lo strumento funziona), **matematico** (i calcoli sono giusti) e **di leggibilità** (stime sui testi). Nessuno dei tre dimostra che un ragazzo con DSA capisca davvero le schermate: questo si osserva solo negli incontri, con la *Griglia di osservazione*.

## 1. Contenuto della consegna

| Percorso | Codice | Schermate |
|---|---|---|
| Fare la parafrasi | M02-02 | 16 |
| Risolvere un’equazione | M08-08 | 17 |
| Prendere appunti a due colonne | M21-04 | 18 |
| Mappa concettuale: la favola | MC-01 | 18 |
| Mappa mentale: la favola | MM-01 | 17 |
| **Totale** | | **86** |

Ogni percorso ha tre pagine A4 da stampare (modello, prove, controllo e promemoria). Le copie PDF sono nella cartella **Schede**, insieme ai testi che l’adulto legge nella prova sugli appunti.

## 2. Controlli tecnici

Eseguiti con Chromium 141 su Linux, a file aperto localmente e **senza connessione**, su una copia del file isolata in un’altra cartella.

| Controllo | Script | Esito |
|---|---|---|
| Percorrere tutte le 86 schermate dei cinque percorsi, con Avanti, Indietro, aiuto e ritorno su ogni schermata | `browser.test.cjs` | Superato |
| Guida per il professionista, schede di stampa, schermo stretto (telefono), testo ingrandito | `browser.test.cjs` | Superato |
| Nessuna richiesta di rete durante l’uso | `browser.test.cjs` | Superato |
| Dopo l’aiuto, il pulsante di ritorno resta visibile; il menu conserva l’aiuto aperto | `interazioni.test.cjs` | Superato |
| Ingrandimento reale del browser al 200% su tutti i percorsi | `zoom-browser.test.cjs` | Superato |
| Schede PDF: 5 × 3 pagine, nessuna pagina vuota, nessun contenuto fuori dai margini | `verifica-stampa.py` | Superato |
| Controllo a vista delle mappe complete (schermo largo e stretto) e di una stampa | `visivo.cjs` e lettura delle immagini | Superato dopo la correzione al punto 5 |

**Limite.** In questa sessione non è stato possibile provare Edge e Chrome su Windows. Le prove su Windows registrate nella sessione precedente riguardano una versione anteriore del file (impronta che inizia con `a821c0…`). Chromium usa lo stesso motore di Chrome ed Edge, quindi il rischio è basso, ma conviene aprire il file almeno una volta sul computer degli incontri.

## 3. Controllo matematico

I passaggi delle tre equazioni del percorso M08-08 sono stati verificati due volte, in modo indipendente:

- nella sessione precedente con Wolfram (richieste e risposte in `manutenzione/wolfram-verifica.json`);
- in questa sessione con un calcolo separato in Python.

| Equazione | Soluzione | Verifica nell’originale |
|---|---|---|
| 3x + 5 = 20 | x = 5 | 3 × 5 + 5 = 20 |
| 2z + 4 = 18 | z = 7 | 2 × 7 + 4 = 18 |
| 4y − 7 = 13 | y = 5 | 4 × 5 − 7 = 13 |
| Errore mostrato: 3x = 20 | x = 20/3 | 3 × 20/3 + 5 = 25, diverso da 20 |

Sono corretti anche gli esempi di appoggio: “se x fosse 2, 3 × 2 + 5 = 11” e “12 − 5 = 12 − 5, cioè 7 = 7”.

## 4. Stime di leggibilità sui testi del ragazzo

Calcolate su tre testi per schermata (testo principale, riquadro “Adesso”, aiuto), titoli esclusi: 258 testi in tutto.

- Frasi analizzate: 724. Lunghezza media: **8,6 parole**. Frasi con più di 25 parole: **nessuna**.
- Indice Gulpease medio del testo principale: tra **66** (mappa mentale) e **78** (equazioni).
- Testi con indice **sotto 60**: **44** su 258.

Come leggere questi numeri: l’indice Gulpease è tarato sull’italiano. Sotto 60 un testo risulta difficile per chi ha la licenza media, sotto 80 per chi ha la licenza elementare. Un ragazzo di 13 anni con dislessia sta nel mezzo, e la sua difficoltà di lettura abbassa ancora la soglia. L’indice misura solo lunghezza di parole e frasi: non dice nulla su concetti astratti, doppie negazioni o mancanza di esempi, che sono i problemi più rilevanti per un DSA.

Gli schemi linguistici ricorrenti nei testi sotto 60 sono:

- frasi del tipo “non X, ma Y” o “cambierebbe invece…”, che chiedono di tenere a mente due ipotesi;
- parole astratte ripetute: “conservare” (17 volte), “categoria”, “organizzazione”, “coerente”, “sottinteso”;
- spiegazioni sul metodo (“Scegliere parole chiave non vuol dire eliminare tutte le altre parole per sempre”) più che sull’azione da compiere.

Questi testi **non sono stati riscritti** in questa sessione: la riscrittura è una scelta didattica che spetta a chi segue i ragazzi.

## 5. Correzioni fatte in questa sessione

- **Mappa mentale:** “Messaggio” e “Morale” erano disegnati quasi a contatto, con un ramo cortissimo. I due nodi sono stati spostati; ora i tre rami hanno lunghezze simili, a schermo e in stampa.
- **Consegna completata:** create la cartella **Schede** e questo rapporto, entrambi citati nel LEGGIMI ma mancanti.
- **Script di verifica:** `interazioni.test.cjs`, `zoom-browser.test.cjs`, `visivo.cjs` e `verifica-stampa.py` accettano ora i percorsi di browser e strumenti tramite variabili d’ambiente (`PLAYWRIGHT_MODULE`, `BROWSER_EXE`, `PDFTOPPM`), come già faceva `browser.test.cjs`. Senza variabili usano i percorsi di Windows di prima.
- **Pulizia:** rimossi dalla repository 689 file di profili temporanei del browser e la copia isolata creata dai test; aggiunte le regole corrispondenti a `.gitignore`.

## 6. Come ripetere le verifiche

Da `manutenzione`, dopo aver modificato contenuti o stile:

```
node costruisci.mjs
node browser.test.cjs
node interazioni.test.cjs
node zoom-browser.test.cjs
node visivo.cjs
python verifica-stampa.py
```

Su un computer diverso da quello originale, impostare prima `PLAYWRIGHT_MODULE`, `BROWSER_EXE` e, per la stampa, `PDFTOPPM`.
