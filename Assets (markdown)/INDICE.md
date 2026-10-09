# Indice dei manuali convertiti in formato Markdown

*Ultimo aggiornamento: 24 settembre 2026 — quattordici volumi indicizzati.*

Questo documento raccoglie, per ciascun manuale presente nella cartella "Assets (markdown)", i riferimenti principali (autore, argomento, struttura interna) che permettono di orientarsi rapidamente nel contenuto senza dover rileggere l'intero file. Per ogni voce della struttura viene indicato il numero di riga del file Markdown corrispondente, in modo da poter raggiungere direttamente la sezione desiderata (per esempio con una ricerca del tipo "vai alla riga 749" oppure con il comando `sed -n '749,780p' nomefile.md`).

Nota metodologica: i file PDF sono stati convertiti utilizzando la libreria pymupdf4llm, che applica il riconoscimento ottico dei caratteri (OCR tramite Tesseract) sulle pagine composte da immagini scansionate. I file EPUB sono stati convertiti con Pandoc. Alcuni titoli, in particolare quelli derivati da pagine scansionate, possono contenere piccoli errori di trascrizione tipici dell'OCR (per esempio lettere scambiate o parole spezzate); il contenuto resta comunque pienamente utilizzabile per la consultazione e la ricerca testuale.

---

## 1. Didattica ludica

**File:** `Didattica ludica (Andrea Ligabue).md`
**Autore:** Andrea Ligabue — prefazione di Roberto Farné (Erickson)
**Argomento:** metodologie di apprendimento basate sul gioco (gamification e game-based learning), con schede pratiche di analisi di giochi da tavolo utilizzabili in ambito didattico
**Formato originale:** PDF (convertito dall'EPUB originale) — circa 57.500 parole, 3.894 righe nel file convertito

Nota sulla fonte: questa voce è stata riconvertita da un PDF ottenuto a partire dall'EPUB originale, che presentava una struttura poco leggibile nel Markdown risultante. La nuova conversione produce intestazioni Markdown corrette per ogni capitolo, a differenza della versione precedente.

Struttura principale (con numero di riga):

- Riga 29 — L'autore
- Riga 35 — Indice originale del volume
- Riga 47 — Prefazione
- Riga 65 — Introduzione
- Riga 85 — Capitolo 1: Che cos'è un gioco?
- Riga 411 — Capitolo 2: Cosa può insegnare un gioco da tavolo
- Riga 805 — Capitolo 3: Come strutturare una lezione con i giochi
- Riga 1159 — Capitolo 4: Schede di gioco (quindici schede di analisi di giochi da tavolo, utili come spunti operativi)
  - Riga 1219 — Ticket to Ride
  - Riga 1363 — Carcassonne
  - Riga 1479 — Jamaica
  - Riga 1608 — Co-Mix
  - Riga 1730 — Kaleidos
  - Riga 1820 — Zoom
  - Riga 1906 — Stone Age
  - Riga 2035 — Kingdomino
  - Riga 2150 — I Coloni di Catan
  - Riga 2260 — Super Farmer
  - Riga 2400 — Stone Age Jr
  - Riga 2550 — Alta Tensione
  - Riga 2688 — Pandemia
  - Riga 2912 — Viva Topo!
  - Riga 2933 — Giochi e funzioni esecutive
- Riga 3012 — Bibliografia
- Riga 3072 — Appendice: Ludografia

---

## 2. Disturbi emotivi. Cosa fare (e non) — Scuola primaria

**File:** `Disturbi emotivi - Cosa fare e non - Scuola primaria (Erika Panchieri).md`
**Autrice:** Erika Panchieri
**Argomento:** gestione delle emozioni difficili nei bambini della scuola primaria, rivolto principalmente agli insegnanti
**Formato originale:** PDF scansionato (interamente elaborato con OCR) — circa 21.800 parole, 2.109 righe nel file convertito

Struttura principale: il volume è organizzato per emozione (il primo capitolo, che comincia alla riga 30, tratta la Rabbia). L'indice testuale originale non è stato recuperato correttamente dall'OCR poiché nel PDF era realizzato come immagine, tuttavia ogni capitolo dedicato a una singola emozione segue costantemente lo stesso schema in tre parti, che è possibile individuare con una ricerca testuale nel file:

- "Cosa tenere a mente" — sintesi concettuale dell'emozione trattata
- "Come intervenire" — indicazioni operative per l'insegnante
- "I consigli dell'esperto" — approfondimento

Questo schema ricorre circa dieci volte nel volume (alle righe 331, 442, 555, 762, 856, 974, 1066, 1180, 1299, 1399, 1505, 1607, 1711, 1799 e successive), corrispondenti alle diverse emozioni trattate oltre alla rabbia. Si consiglia, per individuare rapidamente il capitolo dedicato a un'emozione specifica, una ricerca testuale del nome dell'emozione stessa. La sezione finale, alla riga 1866, tratta il benessere dei docenti.

---

## 3. Formulario di matematica

**File:** `Formulario di matematica.md`
**Argomento:** raccolta di formule di matematica per la scuola secondaria di secondo grado, dalle potenze all'analisi
**Formato originale:** PDF (in parte scansionato) — circa 10.500 parole, 1.022 righe nel file convertito

Struttura principale (con numero di riga):

- Riga 32 — Potenze
- Riga 36 — Radicali
- Riga 44 — Prodotti notevoli
- Riga 64 — Valore assoluto
- Riga 76 — Scomposizioni
- Riga 82 — Logaritmi
- Riga 95 — Disequazioni di prodotto o di polinomi e disequazioni fratte
- Riga 105 — Disequazioni irrazionali
- Riga 117 — Sistemi di disequazioni
- Riga 121 — Trigonometria (relazioni fondamentali, funzioni goniometriche inverse, funzioni iperboliche)
- Riga 232 — Formule trigonometriche (bisezione, parametriche, prostaferesi, Werner)
- Riga 270 — Triangoli (teoremi dei seni, della corda, delle proiezioni)
- Riga 309 — Applicazioni della trigonometria alla geometria
- Riga 361 — Geometria analitica
- Riga 426 — Coniche (parabola, circonferenza, ellisse, iperbole)
- Riga 546 — Successioni e limiti notevoli
- Riga 572 — Funzioni continue e punti di discontinuità
- Riga 609 — Derivate (definizione, regole di derivazione, derivate delle principali funzioni)
- Riga 671 — Integrali
- Riga 691 — Equazioni differenziali ordinarie
- Riga 799 — Serie (a termini di segno alterno, convergenza assoluta, Fourier, Taylor)
- Riga 861 — Determinante di una matrice quadrata
- Riga 899 — Geometria piana
- Riga 936 — Lunghezza di un arco di curva
- Riga 944 — Geometria nello spazio
- Riga 972 — Volume di un solido di rotazione
- Riga 978 — Costanti fondamentali
- Riga 998 — Crivello di Eratostene

---

## 4. Italiano Speciale (DSA). Scuola secondaria di primo grado. Per il docente

**File:** `Italiano Speciale (DSA) - Scuola secondaria di primo grado - Per il docente.md`
**Autori:** C. Cappa, L. Grosso, V. Rossi, S. Giulivi
**Argomento:** guida per l'insegnante di italiano rivolta a studenti con disturbi specifici dell'apprendimento (DSA) nella scuola secondaria di primo grado
**Formato originale:** PDF scansionato (interamente elaborato con OCR) — circa 25.700 parole, 2.309 righe nel file convertito

Struttura principale (con numero di riga):

- Riga 120 — Prefazione
- Riga 142 — Riflessione introduttiva
- Riga 206 — Capitolo 1: I disturbi evolutivi specifici di apprendimento (DSA)
- Riga 389 — Capitolo 2: L'insegnamento e l'apprendimento della lingua italiana
- Riga 748 — Capitolo 3: Come può il nostro allievo superare le difficoltà legate al DSA?
- Riga 840 — Capitolo 4: Leggere e scrivere (comprensione del testo, scrittura, ortografia, punteggiatura)
- Riga 1369 — Capitolo 5: La grammatica (analisi grammaticale, logica e del periodo)

Nota: nella parte iniziale del file (a partire dalla riga 73, sotto il titolo "IndIce") è presente l'indice testuale originale del volume, con i numeri di pagina della versione a stampa e i sottoparagrafi di dettaglio (per esempio 4.1, 4.2, 4.2.1 e così via) e i riquadri "Approfondimento" e "Per lo studente". Questo indice originale è utile per una consultazione più fine rispetto ai soli titoli di capitolo elencati sopra.

---

## 5. L'ansia nei bambini e negli adolescenti. Riconoscerla e affrontarla

**File:** `L'ansia nei bambini e negli adolescenti - Riconoscerla e affrontarla (Stefano Vicari, Maria Pontillo).md`
**Autori:** Maria Pontillo, Stefano Vicari (Il Mulino)
**Argomento:** riconoscimento e gestione dell'ansia in età evolutiva, cause, valutazione diagnostica e terapie, con consigli pratici per genitori e insegnanti
**Formato originale:** PDF (convertito dall'EPUB originale) — circa 29.600 parole, 1.285 righe nel file convertito

Nota sulla fonte: questa voce è stata riconvertita da un PDF ottenuto a partire dall'EPUB originale. La nuova conversione recupera una struttura più dettagliata, comprese le storie cliniche esemplificative che accompagnano ciascun disturbo d'ansia descritto nel capitolo 2.

Struttura principale (con numero di riga):

- Riga 31 — Indice originale del volume
- Riga 65 — La storia di Chiara: quando l'ansia diventa un disturbo (caso introduttivo)
- Riga 83 — Capitolo 1: Capire cos'è l'ansia
  - Riga 85 — Una risorsa o un disturbo?
  - Riga 145 — Quando l'ansia diventa patologica
  - Riga 204 — Ansia, paura e sistema nervoso
  - Riga 247 — Quali sono i principali disturbi d'ansia in età evolutiva?
  - Riga 269 — Un po' di numeri
- Riga 297 — Capitolo 2: Quanti tipi di ansia e a quali età?
  - Riga 299 — Quali sono i segni dell'ansia?
  - Riga 337 — La storia di Greta: il Disturbo d'ansia da separazione
  - Riga 355 — La storia di Elisa: il Mutismo selettivo
  - Riga 373 — La storia di Michela: la Fobia specifica
  - Riga 395 — La storia di Marco: il Disturbo d'ansia sociale
  - Riga 419 — La storia di Claudio: il Disturbo di panico
  - Riga 435 — La storia di Matteo: l'Agorafobia
  - Riga 447 — La storia di Marta: il Disturbo d'ansia generalizzata
  - Riga 465 — La storia di Alessandro: la Fobia scolare
- Riga 487 — Capitolo 3: Dove nasce l'ansia?
  - Riga 489 — Tre tipi di cause
  - Riga 493 — Fattori genetici e neurobiologici
  - Riga 501 — Quanto incidono le esperienze vissute e l'ambiente?
  - Riga 529 — Il ruolo del temperamento
- Riga 549 — Capitolo 4: La valutazione diagnostica
  - Riga 551 — Riconoscere precocemente l'ansia: il ruolo del pediatra
  - Riga 607 — La costruzione di un quadro psicopatologico
  - Riga 707 — Il colloquio clinico
  - Riga 773 — Gli strumenti diagnostici
  - Riga 781 — La diagnosi
- Riga 814 — Capitolo 5: Le terapie
  - Riga 816 — Perché è importante intervenire
  - Riga 828 — La terapia cognitivo-comportamentale
  - Riga 861 — Il ruolo dello psicoterapeuta
  - Riga 898 — Le fasi del trattamento
  - Riga 927 — Le tecniche cognitivo-comportamentali
  - Riga 998 — Le strategie terapeutiche
  - Riga 1037 — La relazione terapeutica e il lavoro cognitivo-comportamentale con i genitori
  - Riga 1045 — Il ruolo del neuropsichiatra
  - Riga 1069 — Quando si ricorre alla terapia farmacologica
- Riga 1085 — Capitolo 6: Alcuni consigli pratici per genitori e insegnanti
  - Riga 1087 — Il ruolo dei genitori
  - Riga 1156 — Il ruolo della scuola
  - Riga 1184 — Il Disturbo d'ansia sociale: cosa può fare l'insegnante?
  - Riga 1202 — Falsi miti e corrette informazioni
- Riga 1222 — Conclusioni
- Riga 1254 — Per saperne di più
- Riga 1280 — Ringraziamenti

---

## 6. Le difficoltà di apprendimento a scuola

**File:** `Le difficoltà di apprendimento a scuola.md`
**Autore:** Cesare Cornoldi
**Argomento:** panoramica sulle difficoltà di apprendimento a scuola, dai disturbi specifici dell'apprendimento ai disturbi di attenzione e iperattività, con casi clinici
**Formato originale:** PDF scansionato (interamente elaborato con OCR) — circa 36.200 parole, 1.270 righe nel file convertito
**Nota:** nella stessa cartella era già presente una versione precedente in formato `.txt` di questo stesso volume; il presente file `.md` costituisce la versione aggiornata e strutturata con intestazioni.

Struttura principale (con numero di riga):

- Riga 67 — Introduzione
- Riga 89 — Le difficoltà di apprendimento (quadro generale)
  - Riga 91 — Quanti sono i casi di difficoltà di apprendimento?
  - Riga 133 — Funzionamento intellettivo limite o borderline
  - Riga 145 — Il ruolo dell'ambiente sociale
  - Riga 159 — Il ruolo della famiglia
  - Riga 171 — Il ruolo dell'istruzione
  - Riga 197 — L'autostima
  - Riga 211 — Problemi di socializzazione con coetanei e adulti
  - Riga 221 — Gli handicap veri e propri
  - Riga 239 — L'handicap mentale
- Riga 261 — I disturbi specifici dell'apprendimento
- Riga 521 — Le dislessie
  - Riga 533 — Caso: Cristina, un esempio di dislessia specifica evolutiva
  - Riga 589 — La valutazione delle difficoltà di lettura
  - Riga 605 — La dislessia: caratteristiche generali e sottotipi
- Riga 653 — Le difficoltà e i disturbi della scrittura
  - Riga 671 — Le disgrafie
  - Riga 715 — La disortografia
  - Riga 744 — Le difficoltà di espressione scritta
- Riga 758 — Le difficoltà in matematica e le discalculie
  - Riga 792 — Le discalculie gravi
  - Riga 838 — I disturbi nella soluzione di problemi
  - Riga 878 — I disturbi della memoria e le difficoltà dell'apprendimento
- Riga 924 — Le difficoltà nella comprensione del testo e nello studio
  - Riga 932 — Caso: Marika
  - Riga 966 — Le difficoltà di studio
  - Riga 998 — Abilità automatizzate, abilità controllate e metacognizione
  - Riga 1026 — Gli interventi riabilitativi
- Riga 1036 — I disturbi non verbali
  - Riga 1038 — Caso: Denis
  - Riga 1102 — I disturbi della coordinazione motoria e le disprassie
  - Riga 1112 — L'aiuto al bambino con disturbo non verbale
- Riga 1152 — I disturbi di attenzione e di iperattività
  - Riga 1154 — Caso: Angelo
  - Riga 1192 — Attenzione e autoregolazione
  - Riga 1204 — La valutazione del disturbo
  - Riga 1214 — Le modalità di intervento e il ruolo della scuola e della famiglia
- Riga 1224 — Per saperne di più

---

## 7. Mappe concettuali e mappe mentali

**File:** `Mappe concettuali e mappe mentali.md`
**Argomento:** fondamenti teorici e uso didattico degli organizzatori grafici della conoscenza, con particolare attenzione alle differenze tra mappe concettuali e mappe mentali
**Formato originale:** PDF (in parte scansionato) — circa 20.100 parole, 1.047 righe nel file convertito

Struttura principale (con numero di riga):

- Riga 20 — Introduzione e scopo del libro
- Riga 36 — Criteri generali impiegati per la ricerca e l'utilizzo delle fonti
- Riga 54 — Knowledge graphic organizers (inquadramento generale)
- Riga 165 — Capitolo 1: Mappe concettuali
  - Riga 171 — Generalità
  - Riga 218 — Fondamenti teorici
  - Riga 272 — Affordances
  - Riga 318 — Uso di software
  - Riga 386 — Uso efficace nella didattica: ostacoli e possibili soluzioni
- Riga 504 — Capitolo 2: Mappe mentali
  - Riga 510 — Generalità
  - Riga 539 — Fondamenti teorici
  - Riga 563 — Affordances
  - Riga 599 — Uso efficace nella didattica: ostacoli e possibili soluzioni
- Riga 689 — Quando concettuali e quando mentali?
- Riga 724 — Conclusione
- Riga 772 — Appendice
  - Riga 774 — Esempi applicativi
- Riga 848 — Bibliografia
- Riga 982 — Sitografia
- Riga 1036 — Ringraziamenti

---

## 8. Tablet delle regole di matematica

**File:** `Tablet delle regole di matematica.md`
**Autrice:** Paola Ethel Demarchi
**Argomento:** strumento compensativo con le regole fondamentali di matematica per la scuola secondaria di primo grado, organizzato per aree tematiche (numeri, spazio e figure, relazioni e funzioni, dati e previsioni)
**Formato originale:** PDF scansionato (interamente elaborato con OCR) — circa 34.900 parole, 4.027 righe nel file convertito

Struttura principale (con numero di riga):

- Riga 151 — Indice originale del volume
- Riga 266 — Introduzione (perché un tablet delle regole, punti chiave, come si usa)
- Riga 325 — L'insieme N (numeri naturali)
- Riga 763 — L'insieme Z (numeri interi)
- Riga 1072 — L'insieme Q (numeri razionali)
- Riga 1395 — Numeri irrazionali e radici quadrate
- Riga 1469 — Espressioni
- Riga 1615 — Proporzioni e percentuali
- Riga 1714 — Spazio e figure (area tematica)
  - Riga 1732 — Fondamenti
  - Riga 1888 — Poligoni e piano cartesiano
  - Riga 2538 — Trasformazioni
  - Riga 2689 — Circonferenza e cerchio
  - Riga 2822 — Solidi
- Riga 3150 — Relazioni e funzioni (area tematica)
  - Riga 3161 — Funzioni
  - Riga 3301 — Monomi e polinomi
  - Riga 3492 — Equazioni
- Riga 3651 — Dati e previsioni (area tematica)
  - Riga 3667 — Statistica
  - Riga 3925 — Probabilità

---

## 9. Come imparare a studiare. Compiti a casa e metodo di studio

**File:** `Come imparare a studiare - Compiti a casa e metodo di studio (Matteo Rampin).md`
**Autore:** Matteo Rampin, medico, psichiatra e psicoterapeuta (Salani Editore, 2016)
**Argomento:** metodo di studio per ragazzi della scuola secondaria, organizzato come raccolta di ventuno strategie pratiche (una per capitolo), con un'appendice dedicata alle prove Invalsi
**Formato originale:** PDF (convertito dall'EPUB originale) — circa 13.000 parole, 792 righe nel file convertito

Nota sulla fonte: questa voce è stata riconvertita da un PDF ottenuto a partire dall'EPUB originale. A differenza della versione precedente, che non utilizzava intestazioni Markdown per i titoli dei capitoli, questa conversione produce intestazioni corrette per ciascun capitolo, elencate di seguito.

Struttura principale (con numero di riga):

- Riga 7 — Presentazione
- Riga 45 — Premessa
- Riga 77 — 1. L'arco e la freccia
- Riga 103 — 2. Gli scacchi
- Riga 131 — 3. La spada di Damocle
- Riga 167 — 4. Il fuoco della passione
- Riga 193 — 5. Il caos e l'ordine
- Riga 219 — 6. Sfruttare le correnti
- Riga 259 — 7. Lo specchio
- Riga 299 — 8. La mossa del gambero
- Riga 359 — 9. Il bisturi
- Riga 387 — 10. Carta e penna
- Riga 423 — 11. Capire di capire
- Riga 451 — 12. Prosciugare
- Riga 473 — 13. L'indagine poliziesca
- Riga 497 — 14. La ricerca del nuovo
- Riga 513 — 15. L'inversione dei ruoli
- Riga 535 — 16. L'amore dell'artigiano
- Riga 555 — 17. La strategia del falco
- Riga 599 — 18. L'antidoto alla paura
- Riga 619 — 19. Sorprendere il buonsenso
- Riga 641 — 20. Affrontare lo stress
- Riga 657 — 21. Il paradosso della disciplina
- Riga 671 — Conclusione
- Riga 691 — Appendice: come usare questi suggerimenti in vista delle prove Invalsi

---

## 10. Una mente per i numeri. Un metodo di studio (non solo) per la matematica

**File:** `Una mente per i numeri - Un metodo di studio (non solo) per la matematica (Barbara Oakley).md`
**Autrice:** Barbara Oakley, Ph.D. — titolo originale: *A Mind for Numbers: How to Excel at Math and Science (Even If You Flunked Algebra)* (#SmartSchool, Logus Mondi Interattivi, 2020)
**Argomento:** tecniche di apprendimento fondate sulle neuroscienze per lo studio della matematica e delle materie scientifiche, con particolare attenzione all'alternanza tra pensiero focalizzato e pensiero diffuso, alla gestione della procrastinazione e alla memoria
**Formato originale:** PDF (convertito dall'EPUB originale) — circa 48.500 parole, 2.780 righe nel file convertito

Nota sulla fonte: questa voce è stata riconvertita da un PDF ottenuto a partire dall'EPUB originale; la struttura complessiva è simile alla versione precedente ma con intestazioni Markdown più pulite.

Struttura principale (con numero di riga; il volume utilizza una numerazione dei capitoli da 1 a 9, ciascuno seguito da sezioni interne, esercizi "Adesso prova tu!" e note):

- Riga 296 — Prefazione all'edizione italiana
- Riga 314 — Prefazione all'edizione inglese
- Riga 338 — Premessa
- Riga 356 — Nota per il lettore
- Riga 380 — Capitolo 1: apri la porta
- Riga 462 — Capitolo 2: chi va piano, va lontano (pensiero focalizzato e pensiero diffuso)
- Riga 756 — Capitolo 3: imparare è creare (memoria di lavoro e memoria a lungo termine, sonno)
- Riga 1115 — Capitolo 4: segmentare ed evitare le illusioni di competenza
- Riga 1602 — Capitolo 5: prevenire la procrastinazione
- Riga 1759 — Capitolo 6: zombie dappertutto (abitudini)
- Riga 2052 — Capitolo 7: segmentare versus affogare (gestione dell'ansia da esame)
- Riga 2254 — Capitolo 8: strumenti, suggerimenti e trucchi
- Riga 2570 — Capitolo 9 (capitolo conclusivo)
- Riga 2771 — L'autrice

Nota: ogni capitolo termina tipicamente con le sezioni "Riassumendo" e "Migliora il tuo apprendimento (l'apprendimento)", facilmente individuabili con una ricerca testuale.

---

## 11. Come migliorare il mio metodo di studio

**File:** `Come migliorare il mio metodo di studio (Silvio Crosera, Carla Perusini).md`
**Autori:** Silvio Crosera, psicologo-psicoterapeuta; Carla Perusini, pedagogista (Giunti Editore, edizione digitale 2023)
**Argomento:** metodo di studio per ragazzi della scuola secondaria basato sul modello RTC (Riflessione, Test, Card), articolato in ventisei capitoli tematici nella prima parte, con una seconda parte dedicata alla gestione dei cambiamenti (procrastinazione, DAD/DDI, noia, ansia)
**Formato originale:** PDF scansionato (interamente elaborato con OCR) — circa 29.500 parole, 3.936 righe nel file convertito

Struttura principale (con numero di riga):

- Riga 39 — Indice originale del volume
- Riga 109 — Presentazioni di Silvio e Carla
- Riga 190 — Introduzione: il modello RTC (Riflessione, Test, Card)
- Riga 240 — Parte I: Progetto il mio metodo di studio (26 capitoli, ciascuno con le tre fasi Riflessione, Test e Card)
  - Riga 265 — Capitolo 1: Qui ci vuole un'idea!
  - Riga 352 — Capitolo 2: Non posso perdere più tempo!
  - Riga 418 — Capitolo 3: La lettura dei bisogni
  - Riga 494 — Capitolo 4: Facciamo qualche ipotesi...
  - Riga 568 — Capitolo 5: Obiettivi: sono sempre quelli, bastano per far bene a scuola?
  - Riga 694 — Capitolo 6: In pratica...
  - Riga 782 — Capitolo 7: Quali strumenti utilizzare?
  - Riga 893 — Capitolo 8: Verifica dei risultati
  - Riga 1038 — Capitolo 9: Cose da sapere per... (attenzione selettiva e sostenuta)
  - Riga 1136 — Capitolo 10: Come monitorare l'attenzione?
  - Riga 1217 — Capitolo 11: Sai che cos'è l'ascolto attivo?
  - Riga 1345 — Capitolo 12: Di che memoria sei? (memoria sensoriale, a breve e a lungo termine)
  - Riga 1486 — Capitolo 13: Il centro di controllo che dà senso a tutto
  - Riga 1601 — Capitolo 14: Posso farcela: piccola guida all'autoefficacia
  - Riga 1677 — Capitolo 15: Autostima: come si fa ad averla e a mantenerla?
  - Riga 1791 — Capitolo 16: Motivazione: spinta, interesse, voglia...
  - Riga 1948 — Capitolo 17: Programmare e tenere i tempi di gara
  - Riga 2062 — Capitolo 18: Dove? L'organizzazione degli spazi
  - Riga 2158 — Capitolo 19: Che cosa può servirmi?
  - Riga 2277 — Capitolo 20: Strategie di lettura
  - Riga 2385 — Capitolo 21: E allora, come fare per migliorare?
  - Riga 2475 — Capitolo 22: Come prendere appunti?
  - Riga 2571 — Capitolo 23: Come sottolineare le informazioni principali?
  - Riga 2666 — Capitolo 24: Come realizzare degli schemi efficaci?
  - Riga 2772 — Capitolo 25: Come rielaborare e ripassare?
  - Riga 2894 — Capitolo 26: Come prepararsi alle verifiche?
- Riga 3021 — Parte II: Affrontare i cambiamenti
  - Riga 3021 — Capitolo 1: Riprogrammare dopo un'esperienza difficile
  - Riga 3092 — Capitolo 2: Le nuove abitudini
  - Riga 3270 — Capitolo 3: DAD e DDI
  - Riga 3352 — Capitolo 4: La comunicazione in DAD e DDI
  - Riga 3402 — Capitolo 5: La procrastinazione
  - Riga 3526 — Capitolo 6: Studio e nello stesso tempo faccio...
  - Riga 3596 — Capitolo 7: La noia
  - Riga 3696 — Capitolo 8: Ansia, depressione, latitanza
  - Riga 3757 — Capitolo 9: Deposito bagagli ingombranti
  - Riga 3792 — Capitolo 10: Le App
- Riga 3865 — Conclusioni
- Riga 3891 — Bibliografia

---

## 12. I Tre Mostri da Uccidere all'Esame. Il Libro sul Metodo di Studio

**File:** `I Tre Mostri da Uccidere all'Esame - Il Libro sul Metodo di Studio (Giovanni Fenu).md`
**Autore:** Giovanni Fenu, fondatore della piattaforma di metodo di studio MemoVia, laureato in Lingue e Letterature Straniere e in Psicologia Clinica (2020)
**Argomento:** metodo di studio per la preparazione degli esami universitari, presentato attraverso la metafora di un "Viaggio attraverso Tre Regni", ciascuno difeso da un "Mostro" che rappresenta un ostacolo tipico dello studio (superficialità nella lettura, difficoltà nella selezione dei contenuti, gestione di programmi molto estesi), seguito da tre capitoli dedicati ad altrettanti "Demoni" legati alla gestione del tempo, del disordine/delle distrazioni e dell'ansia
**Formato originale:** PDF (convertito dall'EPUB originale) — circa 20.000 parole, 1.166 righe nel file convertito

Nota sulla fonte e sulla qualità della conversione: questa voce è stata riconvertita da un PDF ottenuto a partire dall'EPUB originale. Il nuovo PDF recupera intestazioni Markdown corrette, assenti nella versione precedente, ma introduce un diverso problema: buona parte del testo evidenziato nel documento originale (racchiuso in tag `<mark>`) risultava duplicata dalla conversione automatica, probabilmente per la sovrapposizione fra il livello di testo base e quello dell'evidenziazione nel PDF di origine. È stata applicata una pulizia automatica che ha rimosso la quasi totalità di queste ripetizioni (individuate confrontando frammenti di testo consecutivi molto simili); un residuo minimo di ripetizioni isolate (meno del 2% delle righe del file) può essere ancora presente qua e là, in genere limitato a singole parole.

Struttura principale (con numero di riga):

- Riga 55 — Introduzione: I 3 mostri
  - Riga 97 — Perfezioni e imperfezioni
  - Riga 129 — Panoramica del libro
- Riga 161 — Base: preparati alla battaglia
  - Riga 170 — L'equazione dello studio intelligente
  - Riga 211 — Come e quanto dovresti studiare
  - Riga 235 — Tre tipi di studenti: le Incarnazioni
  - Riga 273 — I 3 Regni Inferiori e Superiori
- Riga 310 — 1° Regno: affonda la spada nel Mostro Superficiale
  - Riga 321 — Leggi e scegli bene
  - Riga 371 — Salta il superfluo
  - Riga 389 — Per capire fai Elaborazione di Primo Livello
- Riga 453 — 2° Regno: colpisci duramente il Mostro Elettivo
  - Riga 462 — Decidi in fretta cosa è importante
  - Riga 496 — Seleziona con gli Appunti Nucleari
  - Riga 508 — Dai un senso per te
  - Riga 542 — Puoi prendere appunti al computer?
  - Riga 560 — Non farti trovare impreparato
- Riga 572 — 3° Regno: circonda e sfianca il Mostro Estensivo
  - Riga 647 — Memorizza
  - Riga 669 — Revisiona nei giorni giusti
- Riga 711 — Lo Stregone del Tempo (primo Demone: gestione del tempo)
  - Riga 735 — Riduci il tuo livello di procrastinazione
  - Riga 765 — Non usare pomodori e i cicli
  - Riga 791 — La tua segretaria (o segretario) personale
  - Riga 811 — Pianifica in termini di priorità e intensità
- Riga 825 — Il Giullare Sismico (secondo Demone: disordine e distrazioni)
  - Riga 831 — Combatti il disordine
  - Riga 843 — Resisti alle tentazioni e prendi delle buone abitudini
  - Riga 863 — Disegna il tuo ambiente fisico
  - Riga 891 — Elimina gli sfiati e divertiti al massimo
  - Riga 977 — È il caso di studiare in gruppo?
- Riga 1007 — Le Serpi e i loro Sortilegi (terzo Demone: ansia)
  - Riga 1016 — Distruggi la frase maledetta
  - Riga 1036 — Costruisci la capacità di resistere all'ansia
  - Riga 1056 — Tratta bene il motore e ti porterà lontano
- Riga 1076 — Ora puoi affrontare i 3 Demoni
- Riga 1102 — Chi sono (nota biografica dell'autore)

---

## 13. Metacognition in Learning and Instruction. Theory, Research and Practice

**File:** `Metacognition in Learning and Instruction - Theory, Research and Practice (Hope J. Hartman, a cura di).md`
**Curatrice:** Hope J. Hartman (collana Neuropsychology and Cognition, volume 19, Kluwer Academic Publishers, Dordrecht, 2001)
**Lingua:** inglese (unico volume in lingua diversa dall'italiano tra quelli indicizzati)
**Argomento:** raccolta di dodici saggi accademici sulla metacognizione nell'apprendimento e nell'insegnamento, organizzata secondo il modello BACEIS (Behavior, Affect, Cognition, Environment, Interacting Systems) elaborato da Hartman e Sternberg
**Formato originale:** PDF con strato testuale nativo, non scansionato — circa 107.500 parole, 5.560 righe nel file convertito

Struttura principale (con numero di riga):

- Riga 146 — Preface
- Riga 154 — The Book's Organization
- Riga 242 — Acknowledgments
- Riga 271 — Parte I: Students' Metacognition and Cognition
  - Riga 285 — Capitolo 1: Promoting General Metacognitive Awareness — Gregory Schraw
  - Riga 510 — Capitolo 2: Metacognition in Basic Skills Instruction — Annette F. Gourgey
  - Riga 738 — Capitolo 3: Developing Students' Metacognitive Knowledge and Skills — Hope J. Hartman
  - Riga 1500 — Capitolo 4: The Ability to Estimate Knowledge and Performance in College: A Metacognitive Analysis — Howard T. Everson, Sigmund Tobias
- Riga 1802 — Parte II: Students' Metacognition and Motivation
  - Riga 1830 — Capitolo 5: Cognitive, Metacognitive, and Motivational Aspects of Problem Solving — Richard E. Mayer
  - Riga 2100 — Capitolo 6: Contextual Differences in Student Motivation — Christopher A. Wolters, Paul R. Pintrich
- Riga 2490 — Parte III: Metacognition and Teaching
  - Riga 2504 — Capitolo 7: Mathematics Teaching as Problem Solving: A Framework for Studying Teacher Metacognition Underlying Instructional Practice in Mathematics — Alice F. Artzt, Eleanor Armour-Thomas
  - Riga 2873 — Capitolo 8: Teaching Metacognitively — Hope J. Hartman
  - Riga 3265 — Capitolo 9: Metacognition in Science Teaching and Learning — Hope J. Hartman
- Riga 3684 — Parte IV: Metacognition and Culture
  - Riga 3697 — Capitolo 10: Enhancing Self-Monitoring during Self-Regulated Learning of Speech — Dorothy Ellis, Barry J. Zimmerman
  - Riga 4127 — Capitolo 11: Metacognition and EFL/ESL Reading — Patricia L. Carrell, Linda Gajdusek, Teresa Wise
- Riga 4417 — Parte V: Conclusion
  - Riga 4421 — Capitolo 12: Metacognition, Abilities, and Developing Expertise: What Makes an Expert Student? — Robert J. Sternberg

Nota: la conversione ha mantenuto come intestazioni di livello 6 anche le testate e i piè di pagina ripetuti su ogni pagina del PDF originale (nome dell'autore o titolo del capitolo, ripetuti decine di volte all'interno di ciascun capitolo); non rappresentano nuove sezioni e possono essere ignorati nella navigazione.

---

---

## 14. Adolescenti in crescita. L'ACT per aiutare i giovani a gestire le emozioni, raggiungere obiettivi, costruire relazioni sociali

**File:** `Adolescenti in crescita.md`
**Autori:** Louise L. Hayes, Joseph Ciarrochi — titolo originale: *The Thriving Adolescent: Using Acceptance and Commitment Therapy and Positive Psychology to Help Teens Manage Emotions, Achieve Goals, and Build Connection* (2015). Edizione italiana a cura di Francesco Dell'Orco, traduzione di Marta Schweiger e Massimo Cesareo (FrancoAngeli, 2017, collana "Pratiche comportamentali e cognitive" diretta da Paolo Moderato)
**Argomento:** presentazione del modello DNA-V (Scopritore/Esploratore, Osservatore, Consulente, Valori), un approccio basato sull'ACT (Acceptance and Commitment Therapy) e sulla psicologia positiva per lo sviluppo delle competenze psicologiche negli adolescenti, con applicazioni alla gestione delle emozioni, al raggiungimento di obiettivi e alla costruzione di relazioni sociali
**Formato originale:** PDF con strato testuale nativo, in parte scansionato — circa 119.300 parole, 6.830 righe nel file convertito

Struttura principale (con numero di riga; il volume include un indice testuale originale con la numerazione di pagina della versione a stampa, non riportata qui):

- Riga 97 — Prefazione: Il coraggioso passo in avanti dei modelli ACT per il lavoro con bambini e adolescenti (di Steven C. Hayes)
- Riga 135 — Introduzione all'edizione italiana (di Francesco Dell'Orco, Francesca Pergolizzi)
- Riga 163 — Introduzione
- Riga 237 — Prima parte: Conoscere il DNA-V, le competenze di base
  - Riga 241 — Capitolo 1: Gli elementi di una crescita sana
  - Riga 544 — Capitolo 2: I valori ci aiutano a scoprire le cose importanti e la vitalità
  - Riga 804 — Capitolo 3: Il Consulente, un aiuto efficace per scoprire la nostra strada
  - Riga 1253 — Capitolo 4: L'Osservatore ci aiuta ad apprezzare e scegliere
  - Riga 1891 — Capitolo 5: L'Esploratore ci aiuta a crescere e diventare forti
  - Riga 2524 — Capitolo 6: Tornare ai valori e impegnarsi nell'azione
  - Riga 2727 — Capitolo 7: Unire le competenze DNA-V per sviluppare la forza flessibile
- Riga 3184 — Seconda parte: Competenze avanzate, utilizzare il DNA-V nel lavoro sul sé e sul mondo sociale
  - Riga 3188 — Capitolo 8: Il nostro Sé in azione
  - Riga 3559 — Capitolo 9: Sviluppare una visione di Sé flessibile
  - Riga 3907 — Capitolo 10: Dall'autolesionismo alla gentilezza verso di Sé
  - Riga 4349 — Capitolo 11: Amicizia e amore sono nel nostro DNA
  - Riga 4848 — Capitolo 12: Costruire solide reti sociali
  - Riga 5405 — Capitolo 13: Otto consigli per diventare un esperto del DNA-V
- Riga 6003 — Bibliografia
- Riga 6417 — Indice analitico

---

## Come utilizzare questo indice

I numeri di riga indicati fanno riferimento al file Markdown convertito, non al numero di pagina del documento originale (fatta eccezione per l'indice testuale originale di "Italiano Speciale", che riporta la numerazione di pagina della versione a stampa). Per raggiungere rapidamente una sezione è possibile aprire il file con un qualsiasi editor di testo e spostarsi direttamente alla riga indicata, oppure effettuare una ricerca testuale del titolo della sezione.

Per i volumi derivati da PDF scansionati (Disturbi emotivi, Italiano Speciale, Le difficoltà di apprendimento a scuola, Tablet delle regole di matematica, Come migliorare il mio metodo di studio), l'intero testo è stato ottenuto tramite riconoscimento ottico dei caratteri: è quindi possibile incontrare occasionalmente errori di trascrizione puntuali, che non compromettono comunque la leggibilità complessiva né l'affidabilità della ricerca testuale per parola chiave.
