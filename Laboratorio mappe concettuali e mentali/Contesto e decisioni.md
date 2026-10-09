# Contesto e decisioni

Stato del lavoro al 9 ottobre 2026. Il lavoro è stato fatto con Claude e prosegue in locale con ChatGPT.

## 1. Obiettivo

Una pagina web interattiva che aiuta a spiegare a ragazzi e ragazze delle medie **come costruire mappe concettuali e mappe mentali**. Il pubblico comprende studenti con disturbi specifici dell'apprendimento.

La pagina ha due modalità:

- **In classe**: proiettata da chi insegna. Le mappe sono già complete e si spiegano passo per passo.
- **Da solo**: lo studente la usa in autonomia. Ogni parte ha un riquadro «Il tuo compito» con una casella «Fatto». Le mappe partono dal primo passo. Le note per chi insegna sono nascoste.

## 2. Fonti

| Fonte | Uso | Percorso nella repository |
|---|---|---|
| Ivana Rosati (2013), «Mappe concettuali e mappe mentali», Tangram | Fonte di verità per la teoria: Novak (mappe concettuali), Buzan (mappe mentali), differenze, usi, ostacoli | `Assets (markdown)/Mappe concettuali e mappe mentali.md` e il PDF in `Assets (pdf, epub)/` |
| Dispense del corso «Metodo di studio» | Fonte di verità per la pratica: metodo SQ4R, esercizi preparatori, regole per la mappa mentale (Salvo, 2015), esempi del deserto e del clima, testo sul Po | `Metodo di studio CIU.txt` |
| W3C, «Making Content Usable for People with Cognitive and Learning Disabilities» | Revisione dell'accessibilità | `Making Content Usable for People with Cognitive and Learning Disabilities.html` ed estratto in `fonti/` |

## 3. Decisioni già prese (non riaprirle senza motivo)

### Decise dall'utente

1. **Distinzione rigorosa tra mappa concettuale e schema.** Gli esempi delle dispense (deserto, Raffaello, clima) sono alberi senza parole sulle frecce. Secondo Novak sono schemi di classificazione, non mappe concettuali: senza parola-legame non c'è una frase da verificare. La pagina tiene la distinzione e aggiunge le parole-legame all'esempio del clima.
2. **Due modalità**, «In classe» e «Da solo» (vedi sopra).
3. **Nessuna esercitazione finale** in cui gli studenti costruiscono una mappa da zero. Si potrà fare sul testo «I gatti» indicato dalle dispense, ma il testo vero non è disponibile: il file contiene solo il titolo.
4. **La barra in alto resta con sei voci**, anche se le linee guida W3C ne consigliano al massimo cinque. Ogni voce corrisponde a una parte reale della pagina.
5. **Per ora nessuna scheda di osservazione** per la prova con gli studenti.

### Scelte sui contenuti

6. **Affermazioni escluse perché senza prove:**
   - dalle dispense: «ripetere ad alta voce migliora la memorizzazione di almeno l'80%» (numero senza fonte, poco credibile);
   - le affermazioni sul «cervello destro e sinistro» legate alle mappe mentali (Rosati stessa le giudica discutibili).
7. **Prove sulle mappe mentali presentate con prudenza.** Rosati riporta un vantaggio piccolo: ricordo a una settimana +10% contro +6% (Farrand e colleghi, 2002). La pagina non dice che la mappa mentale è «il metodo migliore».
8. **Le regole di un tipo di mappa non si mescolano con l'altro.** La pagina 116 delle dispense mischia frecce (mappa concettuale) e immagini (mappa mentale); ogni regola è stata assegnata al suo tipo.
9. **Contenuti aggiunti che NON vengono dalle fonti** (da segnalare se si modificano):
   - le parole-legame della mappa del clima e i due collegamenti trasversali («l'altitudine, quando sale, abbassa la temperatura»; «la vicinanza al mare rende più mite la temperatura»): nozioni di geografia corrette;
   - le icone della mappa del deserto (sole, luna, goccia);
   - i paragoni per i numeri: 15 metri = palazzo di circa 5 piani; 10 tonnellate = circa 2 elefanti;
   - le situazioni del quiz «Quale mappa scelgo?», costruite sui criteri di Rosati;
   - le definizioni del glossario, scritte a partire dalle fonti.

### Scelte di accessibilità (dalle linee guida W3C)

10. Frasi brevi, istruzioni numerate, nessun corsivo né maiuscolo nelle etichette, metafore spiegate.
11. Glossario «Parole da sapere» e termini sottolineati a puntini che aprono la definizione con un clic.
12. Versione «Leggi la mappa come elenco» per entrambe le mappe.
13. Riquadro «Scegli come usare la pagina»: modalità, grandezza del testo su tre livelli, lettura ad alta voce.
14. Passi con stato visibile (✓ fatto, pieno = sei qui, tratteggiato = da fare) e «Passo n di N».
15. Pulsanti distinguibili dal testo, area da premere di almeno 44 pixel, ✓ e ✗ insieme ai colori.
16. Sfondo pieno dietro al testo (i quadretti restano solo ai lati).
17. Caselle, modalità e grandezza del testo salvate nel browser.
18. Liste di controllo accanto alla mappa a cui si riferiscono.

## 4. Struttura del file `Mappe concettuali e mentali.html`

Un solo file con stile e codice dentro. Caratteri da Google Fonts: Bricolage Grotesque (titoli) e Atkinson Hyperlegible (testo, scelto per l'alta leggibilità).

### Aspetto grafico

- **Tema chiaro**: quaderno a quadretti. **Tema scuro**: lavagna. Segue il tema del sistema operativo.
- **Colori principali** (variabili in `:root`): `--pen` blu penna = mappa concettuale; `--marker` magenta = mappa mentale; `--b1`…`--b4` = colori dei quattro rami; `--ok` e `--no` = giusto e sbagliato; `--hl` = evidenziatore giallo.

### Parti della pagina

| `id` | Contenuto |
|---|---|
| (in alto) | Barra di navigazione con icone; titolo; riquadro «In breve»; riquadro «Scegli come usare la pagina» |
| `due-mappe` | Tabella di confronto, frase «rigore/vigore» spiegata, avviso, glossario |
| `prima` | Tre abilità preparatorie, metodo SQ4R in sei fasi, esercizio «trova le parole chiave» sulla frase del Po |
| `concettuale` | Mappa del clima in 6 passi (`#cb`, testi nel `<template id="cb-steps">`, disegno `#csvg`), versione a elenco, esercizio sulle parole-legame, mappe che descrivono e che spiegano, lista di controllo |
| `mentale` | Mappa del deserto in 5 passi (`#mb`, testi in `#mb-steps`, disegno `#msvg` generato dal codice), versione a elenco, scaletta del deserto, «prima tutte le idee, poi in ordine», lista di controllo |
| `quale` | Quiz con 6 situazioni e pulsante per ricominciare |
| `studio` | Ciclo capitolo per capitolo, quattro consigli, riquadro di aiuto, «Per chi insegna» |

### Blocchi del codice (in fondo al file, in ordine)

1. Salvataggio nel browser: chiave `mappe-stato-v2`.
2. Glossario (oggetto `GL`) e finestrella delle definizioni.
3. Lettura ad alta voce (sintesi vocale del dispositivo; i pulsanti si nascondono se non è disponibile).
4. Esercizio parole chiave sul Po.
5. `Builder`: costruttore a passi, usato da entrambe le mappe.
6. Mappa concettuale: frasi da evidenziare (`props`).
7. Esercizio parole-legame (`lwData`).
8. Mappa mentale: rami (`branches`) disegnati dal codice. La lunghezza di ogni ramo si adatta alla parola.
9. Quiz (`quiz`).
10. Liste di controllo salvate.
11. Modalità e grandezza del testo.
12. Evidenziazione della parte corrente nella barra in alto.

**Identificativi salvati nel browser:** `cc1`…`cc7` (lista della mappa concettuale), `cm1`…`cm7` (lista della mappa mentale), `g1`…`g6` (caselle «Fatto»). Non rinominarli.

## 5. Problemi aperti

1. **Lettura ad alta voce mai ascoltata.** Il browser di prova non aveva voci installate. Va provata sui dispositivi della scuola.
2. **Mappe sul telefono.** Sullo schermo stretto le mappe vanno fatte scorrere di lato. C'è un avviso e c'è la versione a elenco, ma le linee guida sconsigliano le zone che scorrono dentro la pagina. Soluzione migliore: ridisegnare le mappe in verticale per il telefono.
3. **Mai provata con studenti reali.** Le linee guida W3C chiedono di farlo.
4. **Il salvataggio vale solo su un browser.** Cambiando dispositivo, le spunte si perdono.

## 6. Prossimi passi possibili

In ordine di importanza suggerito:

1. Provare la pagina con 2-3 studenti e correggere dove si bloccano.
2. Versione verticale delle mappe per il telefono.
3. Esercitazione finale sul testo «I gatti», se si recupera il testo.
4. Versione stampabile (scheda con le regole delle due mappe e le liste di controllo). In locale la stampa funziona; nell'artefatto di Claude no.
5. Altre mappe di esempio prese dalle fonti, per esempio le mappe di Rosati sulla materia: «Quali sono le differenze tra fenomeni chimici e fenomeni fisici?», «Come si comporta la materia nei passaggi di stato?».

## 7. Lista di controllo prima di considerare finita una modifica

- [ ] La pagina si apre senza errori (console del browser vuota).
- [ ] A 400 pixel di larghezza non c'è scorrimento laterale della pagina.
- [ ] Tema chiaro e tema scuro leggibili.
- [ ] Le tre grandezze del testo funzionano anche sugli elementi nuovi.
- [ ] Le modalità «In classe» e «Da solo» funzionano.
- [ ] I testi nuovi rispettano le regole di scrittura (frasi brevi, elenchi numerati, parole spiegate).
- [ ] Ogni contenuto nuovo viene dalle fonti, oppure è dichiarato come aggiunto.
