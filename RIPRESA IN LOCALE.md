# Ripresa del lavoro in locale

Stato all’11 ottobre 2026. Tutto il lavoro è sul ramo GitHub **`claude/supporto-compiti-github-repo-9zi550`**, raccolto nella richiesta di unione [Nobili64/Supporto-Educativo#1](https://github.com/Nobili64/Supporto-Educativo/pull/1), ancora in bozza.

## 1. A che punto siamo

| Strumento | Stato |
|---|---|
| **Prototipo** (`Percorsi di studio DSA - prototipo/`) | Completo. 5 percorsi, 86 schermate. Testi riscritti e approvati (`Revisione dei testi - prima e dopo.md`). Schede PDF in `Schede/`. Verifiche in `Rapporto di verifica.md`. Da non modificare durante la prova con i ragazzi. |
| **Versione completa** (`Percorsi di studio DSA - versione completa/`) | **122 percorsi su 241**, 1919 schermate. Tutti superano `valida.mjs` e il test nel browser. Mancano 119 percorsi (sezione 4). |

Percorsi pronti nella versione completa:

- **Italiano**: antologia (14/14), poesia (9/9), epica 6/8, grammatica (8/8), scrittura 9/13.
- **Matematica**: aritmetica e algebra 11/12, geometria e dati 8/10.
- **In tutte le materie**: organizzare lo studio 7/11, seguire la lezione (10/10).
- **Storia** 9/10, **Geografia** 9/10, **Scienze** 8/11, **Inglese** 9/11.
- **Tecnologia** 1/9, **Arte** 1/10, **Educazione fisica** 1/10.
- **Mappe**: 2/34 (concettuale e mentale sulla favola).

Il lavoro si è interrotto due volte per i limiti di utilizzo dell’account (settimanale e di sessione), non per errori. I percorsi scritti fino a quel momento sono salvati.

## 2. Portare il lavoro sul computer

La cartella `C:\Users\megan\Desktop\Progetti\Supporto compiti` sembra già collegata a GitHub con Git, perché i primi due salvataggi della repository sono partiti da lì. In **PowerShell**:

```powershell
cd "C:\Users\megan\Desktop\Progetti\Supporto compiti"
git status
```

- Se `git status` mostra **modifiche locali**, salvale prima (`git add -A` e `git commit -m "Modifiche locali"`) oppure mettile da parte con `git stash`.
- Poi scarica il ramo di lavoro e passaci sopra:

```powershell
git fetch origin
git switch claude/supporto-compiti-github-repo-9zi550
git pull
```

La cartella `Casi` non viene toccata: non è su GitHub.

**Se la cartella non è collegata a Git** (`git status` risponde «not a git repository»), usa l’archivio ZIP che ti ho mandato in chat. Contiene solo le cartelle e i file nuovi o modificati. Estrailo nella cartella del progetto e accetta di sovrascrivere i file con lo stesso nome.

## 3. Strumenti da installare (una volta sola)

1. **Node.js** versione LTS, da https://nodejs.org. Serve per costruire e controllare il file.
2. **Playwright**, solo per la verifica nel browser. Nella cartella `manutenzione` della versione completa:

```powershell
cd "Percorsi di studio DSA - versione completa\manutenzione"
npm install playwright
```

Playwright non scarica un browser: si usa Edge, già presente in Windows. Prima di ogni verifica:

```powershell
$env:BROWSER_EXE = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

## 4. Che cosa manca

Elenco completo e aggiornabile in `manutenzione/da-fare.json` (`node da-fare.mjs` lo aggiorna):

| Gruppo | Percorsi |
|---|---|
| P · Italiano e organizzare lo studio | M03-07, M03-08, M05-02, M05-11, M05-12, M05-13, M20-08, M20-09, M20-10, M20-11 |
| Q · Matematica, Storia, Geografia, Scienze, Inglese | M08-12, M09-09, M09-10, M06-10, M07-10, M10-09, M10-10, M10-11, M11-10, M11-11 |
| R · Seconda lingua comunitaria | M12-01 … M12-08 |
| S · Tecnologia | M13-02 … M13-09 |
| T · Arte e immagine | M14-02 … M14-10 |
| U · Musica | M15-01 … M15-09 |
| V · Educazione fisica | M16-02 … M16-10 |
| W · Educazione civica | M17-01 … M17-08 |
| X · Religione e attività alternative | M18-01 … M18-09 |
| Y · Strumento musicale | M19-01 … M19-07 |
| Z1-Z3 · Mappe | MC-02 … MC-17 e MM-02 … MM-17 |

## 5. Riprendere la scrittura con Claude Code

Apri Claude Code nella cartella del progetto. Il file `CLAUDE.md` gli spiega da solo com’è fatto il progetto. Poi scrivi, per esempio:

> Leggi «RIPRESA IN LOCALE.md». Riprendi la scrittura dei percorsi della versione completa: usa un workflow con un agente per ogni gruppo di `manutenzione/da-fare.json`, con le istruzioni di `manutenzione/prompt-agenti.md`. Comincia dai gruppi P e Q. Alla fine valida, costruisci, verifica nel browser i percorsi nuovi e fai il commit.

Alcune indicazioni pratiche:

- **Quanti agenti insieme.** Ogni flusso di lavoro fa lavorare insieme un numero di agenti pari ai processori del computer meno 2. Su un computer con 8 processori sono 6 agenti.
- **Quanto costa.** Ogni percorso richiede circa 35.000 token, quindi i 119 rimanenti circa 4 milioni. Conviene procedere **un gruppo di materie alla volta**, così un limite di utilizzo non interrompe tutto.
- **Se un agente si ferma.** I file già scritti restano. `node da-fare.mjs` mostra che cosa manca e un agente salta i percorsi già validi.

Per lavorare senza agenti, su un percorso alla volta, basta chiedere a Claude Code: «Scrivi il percorso M12-01 seguendo il contratto di scrittura».

## 6. Controlli dopo ogni gruppo

Da `Percorsi di studio DSA - versione completa\manutenzione`:

```powershell
node valida.mjs
node costruisci.mjs
node verifica-browser.cjs M12-01 M12-02
git add -A
git commit -m "Versione completa: percorsi di seconda lingua"
git push
```

`verifica-browser.cjs` senza codici controlla tutti i percorsi: circa 10 minuti.

## 7. Questioni aperte

1. **Dubbi didattici del primo gruppo di percorsi** (Italiano, antologia), ancora senza risposta:
   - **M01-07, sequenze.** Aggiungere una schermata sui tipi di sequenza (narrativa, descrittiva, dialogica, riflessiva), oppure basta una nota per il professionista?
   - **M01-09, riassunto.** Regola fissa (presente e terza persona) oppure «il tempo del testo o quello chiesto dall’insegnante»?
   - **M01-02, lettura ad alta voce.** Il consiglio di chiedere il brano in anticipo resta nella schermata per il ragazzo o va solo nella guida per il professionista?
   - **M01-10, racconto orale.** Il compito nuovo è solo in ascolto: va bene, o il testo deve essere anche visibile sullo schermo?
   - **M01-08, informazioni principali e secondarie.** Due categorie bastano, o servono le tre (essenziale, di supporto, non necessaria)?
   - **M01-06, analisi narrativa.** Struttura semplificata, oppure con i termini dei libri di testo (fabula e intreccio, Spannung, esordio, complicazione)?
2. **Dubbi degli altri agenti.** Sono andati persi: i limiti di utilizzo hanno interrotto gli agenti prima del riepilogo finale. Conviene una rilettura a campione dei percorsi di matematica e scienze.
3. **Rimandi tra percorsi.** Alcuni percorsi citano per titolo percorsi scritti dopo (per esempio M20-07 rimanda a «Presentare un elaborato», M20-09). Quando tutti i percorsi saranno scritti va controllato che i titoli citati esistano.
4. **Prova su Windows.** La versione completa è stata provata solo con Chromium su Linux. Aprire `Metodo di studio DSA.html` almeno una volta con Edge e con Chrome.
5. **Mappa mentale sul telefono.** Diventa un elenco a rami, con il centro in alto invece che nel mezzo. È un limite noto e voluto: lo schermo stretto non permette di più senza rimpicciolire il testo.
6. **Richiesta di unione #1.** Resta in bozza; si porta sul ramo principale quando i percorsi sono completi.
7. **Efficacia.** I controlli automatici dicono che i percorsi sono ben formati e leggibili, non che funzionano con un ragazzo: questo si osserva negli incontri.
