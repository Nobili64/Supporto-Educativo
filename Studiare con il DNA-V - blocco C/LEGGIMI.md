# Studiare con il DNA-V — consegna della tappa C

Edizione provvisoria cumulativa B–C, 1 ottobre 2026. La consegna precedente del blocco B resta invariata.

## I tre documenti

| Documento | Pagine | Formato |
|---|---:|---|
| Manuale operativo, blocchi B–C | 150 | 155 × 230 mm |
| Schede di lavoro, blocchi B–C | 25 | A4 |
| Strumenti per il clinico, blocchi B–C | 16 | A4 |

Il manuale aggiunge fasi 2–3, S1–S31, D4/D6/D7/D11–D18 e C1–C5. Conserva fondamenti, avvio e D1–D3. Sono inclusi esempi originali, varianti 8–10 / 11–13 / 14–16 anni, adattamenti per profilo, criteri osservabili e fonti con limiti espliciti.

Per leggere il nuovo blocco: fasi 2–3 alle pagine 34–39; guida alle strategie a pagina 40; S1–S31 alle pagine 41–105; nuove tecniche D alle pagine 114–138; consapevolezza alle pagine 139–144. Le figure originali sono alle pagine 79, 84 e 99. Gli indici sono navigabili.

Le schede comprendono i codici 1–7, 10–11, 14–17 e 19; sei codici hanno anche una versione concreta. Gli strumenti comprendono 1–6. La numerazione segue il catalogo approvato: i salti sono intenzionali.

## Uso e stampa

Per l’uso ordinario bastano un lettore PDF, una stampante e carta/penna. Non servono programmi di produzione o collegamento a Internet, salvo aprire i riferimenti bibliografici esterni.

Stampa soltanto le pagine utili degli allegati, in A4 al 100%, bianco e nero. I PDF non contengono campi elettronici. Il manuale mantiene il formato del compendio; per una copia su A4 scegli consapevolmente dimensioni effettive o adattamento. La prova fisica sulla stampante non è stata effettuata.

## Che cosa è stato verificato

- 51 controlli automatici superati: formato, paginazione, sezioni richieste, rimandi interni, font incorporati, testo entro pagina, motore, log, esempi numerici, struttura delle strategie e tracciabilità dei riferimenti S.
- Ispezione visiva delle 191 pagine, tramite tavole complete e ingrandimenti mirati; nove pagine controllate anche con un secondo motore di rendering.
- Correzione di due pagine residue di impaginazione, dei diagrammi SVG durante la conversione e delle righe manoscritte delle nuove schede; controllo degli indici delle varianti.
- 158 file di fonte e 27 file della consegna B verificati invariati tramite impronte.

I controlli documentali non dimostrano efficacia clinica, validità psicometrica o usabilità in seduta. La revisione indipendente di un secondo agente è prevista per F e non è stata anticipata. La cartella dei casi reali non è stata consultata.

## Limite e passaggio successivo

La prova in seduta del blocco B non è documentata: non è stata presunta dall’autorizzazione a procedere. La consegna C è pronta per la **revisione dell’utente**, come richiesto dalla tabella delle tappe del piano. I blocchi D, E, F e G non sono dichiarati completati né avviati da questa consegna.

Per annotare una correzione bastano documento, pagina/codice, problema osservato e modifica desiderata. Non inserire dati identificativi di minori nelle note editoriali. Un caso riuscito non valida il percorso; un problema concreto può guidarne la revisione.

## Fonti e sorgenti

`Sorgenti` contiene copie dei tre testi Markdown, tre HTML, foglio di stile, caratteri con licenza, componenti redazionali e registri delle citazioni. Gli HTML usano caratteri locali e restano consultabili senza rete; la resa di stampa di riferimento è il PDF verificato.

La cartella di lavoro autorevole è `.studiare-dnav/tappa-c`, nella radice del progetto. La generazione usa i componenti redazionali per preparare `manuale.md`, e `allegati.py` per i due allegati. `costruisci.py` impagina con WeasyPrint 70 e i caratteri TeX Gyre Termes/Heros; `verifica.py` produce le evidenze. I programmi portabili e le librerie già disponibili nella tappa B vengono riutilizzati senza installazioni aggiuntive.

Per una rigenerazione, dalla cartella del progetto e con il Python predisposto: `prepara.py` → `allegati.py` → `costruisci.py` → `verifica.py`, tutti nella cartella della tappa C. La verifica visiva va ripetuta sulle pagine modificate. Modificare solo i PDF o le copie in `Sorgenti` non aggiorna automaticamente i componenti autorevoli.

Schedario, Compendio, Laboratorio e libri originali non sono modificati. Le proposte di correzione restano separate per la futura decisione sulla tappa G.
