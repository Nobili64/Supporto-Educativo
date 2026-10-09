# Contratto di scrittura dei percorsi

Questo documento vale per chiunque scriva un percorso della versione completa, persona o agente. Un percorso è un file `contenuti/<CODICE>.json`. Il file HTML si costruisce con `node costruisci.mjs`; nessun percorso entra nel file se non supera `node valida.mjs <CODICE>`.

## 1. Per chi scriviamo

- Un ragazzo o una ragazza di 11-14 anni con un disturbo specifico dell’apprendimento (dislessia, disortografia, disgrafia, discalculia, spesso associati).
- La prima volta usa il percorso **durante un incontro individuale**, accompagnato da un professionista. Poi lo riprende **da solo a casa**, sul proprio compito.
- Lavora **su carta** (o con lo strumento, in palestra, con il libro). Lo schermo spiega, mostra e controlla; non raccoglie risposte.

L’utente ha giudicato inutilizzabile la versione precedente perché i testi erano **troppo sintetici**: «un adulto fa fatica a comprendere le istruzioni e gli esempi». Il rimedio non è scrivere di più a caso, ma spiegare **ogni passaggio necessario**, un passaggio per schermata.

## 2. I modelli da imitare

Prima di scrivere il primo percorso, leggi **per intero** almeno due di questi file. Sono stati revisionati con l’utente e rappresentano il livello richiesto:

- `contenuti/M02-02.json` — Fare la parafrasi (procedura su un testo)
- `contenuti/M08-08.json` — Risolvere un’equazione (procedura di calcolo)
- `contenuti/M21-04.json` — Prendere appunti a due colonne (ascolto, con testi letti dall’adulto)
- `contenuti/MC-01.json` e `contenuti/MM-01.json` — Mappe sulla favola (costruzione progressiva)

Imita: la progressione, la quantità di spiegazione, il modo in cui ogni schermata dice che cosa fare sul foglio, l’aiuto che spiega in un altro modo, il controllo con soluzione commentata.

## 3. Il materiale di partenza

Per ogni attività esiste un record nella versione precedente, in `../../Percorsi di studio DSA/manutenzione/guide-a.json`, `guide-b.json`, `guide-c.json`, `guide-d.json` (cercalo per `id`). Contiene obiettivo, tecniche, un esempio svolto, i passaggi, una prova nuova, un errore tipico, gli adattamenti e le note per l’adulto.

- Usalo come **inventario**: che cosa va insegnato, quale tecnica, quale errore tipico.
- **Non copiarne le frasi**: sono telegrafiche. Riscrivi tutto.
- Se l’esempio è debole, scorretto o troppo difficile, **sostituiscilo** con uno migliore.
- Un titolo nel catalogo può raggruppare più compiti (per esempio «Diario, lettera, e-mail, articolo, recensione e regolamento»). Insegna il metodo comune su un caso, poi mostra in una schermata come cambia per gli altri.

Non aprire mai la cartella `Casi` né altri materiali con dati di ragazzi reali.

## 4. Struttura del file

```json
{
 "id": "M01-09",
 "title": "Fare un riassunto",
 "intro": "Una frase che dice che cosa imparerai a fare (massimo 110 caratteri).",
 "maps": { "nome": { "type": "concettuale", "nodes": [ ... ] } },
 "slides": [
  {"phase":"Preparazione","title":"…","text":["paragrafo","paragrafo"],"visual":{…} ,"action":"…","hint":"…"}
 ],
 "coach": {"goal":"…","prepare":"…","observe":"…","scripts":[{"title":"…","text":"…","instruction":"…"}],"adaptations":[["titolo","che cosa osservare","che cosa provare e come verificarne l’utilità"]],"sources":["dunlosky2013","ies2007"],"checks":"facoltativo"},
 "print": {"modelTitle":"…","visual":{…},"model":["…"],"practice":[["Prova guidata","…"],["Compito nuovo","…"]],"answers":["…"],"home":["…","…","…"],"blankNotes":false}
}
```

- `maps` serve solo se una schermata mostra una mappa.
- `visual` può essere `null`.
- `scripts` serve solo quando l’adulto deve leggere un testo ad alta voce (ascolto, dettato, comprensione orale). In quel caso la schermata dice: «Chi ti accompagna trova il testo nel Menu → Guida per il professionista».
- `title` è il nome che vede il ragazzo: può essere più chiaro del titolo del catalogo («Fare la parafrasi» invece di «Parafrasi»).

## 5. Le schermate

### Fasi, nell’ordine

| Fase | A che cosa serve |
|---|---|
| `Preparazione` (e `Controllo della preparazione`) | Che cosa devi ottenere, con quali materiali, quali parole servono. Qui si spiegano i termini scolastici. |
| `Esempio spiegato` (e `Controllo dell’esempio`) | Un esempio originale svolto **un passaggio per schermata**, con il perché di ogni passaggio. |
| `Prova guidata` e `Controllo guidato` | Il ragazzo prova su un secondo caso, con aiuti; subito dopo confronta. |
| `Compito nuovo` e `Controllo` | Un terzo caso, con meno aiuti; poi soluzione commentata, un errore tipico da riconoscere e come correggerlo. |
| `Ripresa a casa` | Ultima schermata: la sequenza da applicare al proprio compito, quando ripassare, quando chiedere aiuto. |

Le fasi non tornano mai indietro. La prima è sempre `Preparazione`, l’ultima sempre `Ripresa a casa`.

### Quante schermate

Da **8 a 18**, secondo la difficoltà:

- **8-11** per attività semplici o brevi (per esempio lettura silenziosa, associare parole e immagini);
- **12-15** per la maggior parte delle attività;
- **16-18** per procedure lunghe con molti passaggi (analisi logica, equazioni, testo argomentativo).

Non allungare per riempire; non comprimere due passaggi in una schermata.

### Ogni schermata

- **`text`**: 1-3 paragrafi. Spiega **una sola idea o un solo passaggio**.
- **`visual`**: il materiale su cui si lavora **in quel momento**: il testo, l’esercizio, la tabella, la mappa. Se il passaggio usa un dato della schermata prima, **ripetilo qui**: il ragazzo non deve ricordare ciò che è sparito.
- **`action`** (riquadro «Adesso»): che cosa fare, **dove** (sul foglio, a voce, con lo strumento) e **quale risultato** osservare. Esempio buono: «Scrivi sul foglio la frase riordinata. Controlla che ci siano il colle, la luce e il mattino.» Esempio da evitare: «Individua soggetto, verbo e riferimenti.»
- **`hint`** (aiuto «Mi serve una spiegazione»): **un’altra strada** per capire lo stesso passaggio: un esempio più semplice, una domanda guida, un’immagine. Non ripete l’«Adesso».
- Massimo **85 parole** tra testo e «Adesso»; massimo **45 parole** nell’aiuto.

## 6. Come scrivere (guida W3C sull’accessibilità cognitiva)

1. **Una idea per frase.** Frasi brevi: il limite è 25 parole, l’obiettivo è 15.
2. **Forma positiva.** Di’ che cosa fare. Evita «non X, ma Y», «cambierebbe invece…», le doppie negazioni.
3. **Parole concrete e comuni.** «Tenere», «scrivere», «ricordare»; non «conservare», «esplicitare», «pertinente». Il validatore blocca un elenco di parole da evitare.
4. **Spiega ogni termine scolastico alla prima comparsa**, nella stessa schermata, con un esempio: «Il soggetto è chi fa l’azione. In “Il gatto dorme”, il soggetto è “il gatto”.»
5. **Dai del tu.** Nessuna ironia, nessun giudizio sulla persona («sei bravo», «è facile»).
6. **Nessuna sigla** nel testo per il ragazzo, salvo quelle scolastiche note (a.C., d.C., km).
7. **L’esempio accanto alla regola**, non due schermate dopo.
8. Indice Gulpease di ogni testo **almeno 60** (il validatore lo calcola). Non barare spezzando frasi a caso: se un testo è difficile, semplifica le parole.

## 7. Correttezza dei contenuti

- **Esempi originali e inventati**, brevi, adatti alla scuola media. Si possono citare autori e opere famose con brevissimi passi di pubblico dominio (per esempio Leopardi, Omero in traduzione storica); altrimenti inventa.
- **Fatti verificati.** Date, luoghi, regole grammaticali, definizioni scientifiche al livello della scuola media e senza ambiguità. Se non sei sicuro di un fatto, cambia esempio.
- **Calcoli verificati.** Per matematica, scienze, geografia (scale, distanze), tecnologia: calcola ogni risultato con Python prima di scriverlo. Scrivi in `coach.checks` che cosa hai verificato.
- **Lingue straniere** (inglese, francese, spagnolo, tedesco): frasi corrette e naturali, livello A1-A2, con la traduzione italiana accanto.
- **Nessun dato personale**: nessun nome di ragazzi reali, nessuna diagnosi, nessuna scuola reale.

## 8. Aiuti per i DSA (`coach.adaptations`)

Da 1 a 4 elementi, ciascuno `[titolo, che cosa osservare, che cosa provare e come verificarne l’utilità]`.

- Titolo nella forma «Passaggio — possibile difficoltà con dislessia» (oppure disortografia, disgrafia, discalculia, o «difficoltà trasversale» per attenzione, memoria, organizzazione, fatica).
- Collega l’aiuto a una **difficoltà osservabile in un passaggio preciso**, non alla diagnosi in generale. Una diagnosi non assegna automaticamente un aiuto.
- Gli **strumenti compensativi** necessari (sintesi vocale, calcolatrice, tavole, mappe) restano sempre disponibili, anche quando si riducono gli aiuti didattici.

## 9. Guida per il professionista e schede

- `coach.goal`: che cosa insegnare e che cosa osservare. `coach.prepare`: che cosa preparare prima dell’incontro. `coach.observe`: domande da fare, come distinguere un errore di metodo da un errore di calcolo, lettura o scrittura.
- `coach.sources`: codici da `fonti.json`. I principi generali vengono da `dunlosky2013` (recupero, ripasso distribuito), `ies2007` (esempi svolti, spiegazioni), `eef2025` (pianificare, controllare, valutare); `aid` e `aiddsa` per strumenti e DSA; `w3c-coga` per la scrittura; `novak` e `aidmappe` per le mappe; `cornell` e `ciu` per gli appunti. Non citare fonti che non sostengono davvero ciò che scrivi.
- `print`: tre pagine A4. Pagina 1: `modelTitle`, `visual` facoltativo e `model` (l’esempio svolto, in passi numerati). Pagina 2: `practice` (prova guidata e compito nuovo, **con tutto il materiale necessario scritto dentro**). Pagina 3: `answers` (soluzioni o criteri) e `home` (3-5 passi del metodo). Valgono le stesse regole di scrittura.

## 10. Immagini disponibili (`visual`)

| `type` | Campi | Limiti |
|---|---|---|
| `quote` | `label`, `text` (a capo con `\n`) | 700 caratteri |
| `math` | `label`, `lines` | 1-8 righe |
| `list` | `label`, `items` | 1-7 voci |
| `table` | `label`, `columns`, `rows` | 2-3 colonne, 1-7 righe; la prima colonna fa da intestazione di riga |
| `timeline` | `label`, `events` [{`when`,`what`}] | 2-8 eventi |
| `notes` | `title`, `questions`, `notes`, `summary`, `focus` (`notes`/`questions`/`summary`) | pagina a due colonne |
| `map` | `map` (nome in `maps`), `show` (quanti nodi mostrare, oppure `null` per tutti), `focus` (id del nodo da evidenziare) | vedi sotto |

**Mappe** (`maps`): `nodes` è un elenco nell’**ordine di costruzione**; il primo è il centro e non ha `parent`. Ogni altro nodo ha `parent`; nella mappa concettuale ha anche `link`, la parola-legame sulla freccia (massimo 20 caratteri), e la frase «parent link nodo» deve leggersi bene. Limiti: massimo 13 nodi, 5 rami principali, 3 dettagli per ramo, 3 livelli; nella concettuale massimo 6 riquadri finali. Etichette **brevi** (meglio sotto i 20 caratteri): il test nel browser blocca le mappe con testo più piccolo di 14 pixel. Per costruire una mappa passo per passo, usa `show` crescente su schermate successive.

## 11. Attività pratiche

Per musica, strumento, arte ed educazione fisica il lavoro non avviene sul foglio. Adatta «Adesso» al luogo reale: «Batti il ritmo con le mani», «Prova il passaggio lento tre volte con lo strumento», «In palestra, prova la sequenza». Lo schermo spiega e mostra; il controllo usa criteri osservabili (per esempio «Le quattro battute hanno la stessa durata?»), anche con l’aiuto dell’adulto.

## 12. Procedura per ogni percorso

1. Leggi il record di partenza (sezione 3) e un modello (sezione 2).
2. Progetta la sequenza: quali passaggi, quanti esempi, quante schermate (sezione 5).
3. Verifica fatti e calcoli (sezione 7).
4. Scrivi `contenuti/<CODICE>.json` in UTF-8.
5. Esegui `node valida.mjs <CODICE>` e correggi finché non ci sono errori. Leggi anche gli avvisi.
6. **Rileggi ogni schermata come un ragazzo di 13 anni con dislessia**: capisco che cosa fare senza chiedere? Il materiale è sulla schermata? So dove scrivere e che cosa controllare? Se no, riscrivi.

Scrivi **solo** i file `contenuti/` che ti sono stati assegnati. Non modificare `app.js`, `stile.css`, `catalogo.json`, `fonti.json`, `valida.mjs` né i percorsi di altri.
