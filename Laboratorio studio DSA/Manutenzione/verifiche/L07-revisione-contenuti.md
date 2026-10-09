# L07 — revisione del 30 settembre 2026

Quattro kit nel lotto: SCI04 genetica/evoluzione, SCI05 Terra/Universo, integrazione energia di SCI06, GEO01 carte/scale. Otto documenti, 33 pagine A4 esportate dai sorgenti Writer con LibreOffice. La base recuperata di elettricità resta distinta e conservata.

## Contenuti e fonti

- SCI04: gene/allele/genotipo/fenotipo; meiosi e mitosi; modello inventato a dominanza completa con condizioni esplicite. Gli incroci sono enumerati indipendentemente. Probabilità non equivale a certezza su pochi discendenti; dominante non significa frequente o migliore. La sopravvivenza osservata non dimostra da sola un cambiamento ereditario nella generazione successiva. Riferimenti NHGRI e OpenStax Biology 2e elencati nella guida.
- SCI05: interno terrestre prevalentemente solido nel mantello, deformabile su tempi geologici; distinzione crosta/litosfera e ipocentro/epicentro. Cicli dell'acqua e delle rocce con più percorsi. Stagioni legate ad asse e rivoluzione, fasi lunari distinte dalle eclissi. La pagina NASA Earth Facts è impiegata per movimenti e atmosfera: la sua descrizione semplificata del mantello non è stata adottata; per questo punto prevale il chiarimento USGS sulle placche che non galleggiano in un oceano di magma. INGV descrive un percorso didattico, non costituisce da solo una verifica di tutte le proposizioni geologiche. Dati e interpretazioni verificati anche con NPS, NOAA e pagine NASA specifiche.
- SCI06: energia, temperatura/calore, modi di trasferimento, rendimento riferito allo scopo, P = VI nel caso dichiarato in corrente continua, E = Pt a potenza costante. Conversioni e confronti di durata. Aggiunte fonti OpenStax Physics 19.4 e College Physics 2e 7.6 per potenza elettrica e rendimento; le parti della discussione sugli apparecchi in corrente alternata della prima fonte non sono trasferite al kit. Esempi numerici originali.
- GEO01: carte selettive, orientamento indicato, coordinate, scala e conversioni; reticolo locale inventato con distanze dichiarate fra centri e dimensioni stampate esplicitamente non misurabili come scala. Percorso distinto dalla distanza rettilinea; scala numerica dopo ridimensionamento. Riferimenti USGS e NOAA.

## Verifiche

`verifica_scienze_geo_l07.py`: 19/19 gruppi di controlli esatti su incroci, percentuali, bilanci, potenze/energie, scale, percorsi e rotazione degli orientamenti. `L07-wolfram.json` conserva richiesta e risposta reali: risultati concordi e conversioni dimensionali a W, J, m e km. Nessun errore di valutazione; le ambiguità lessicali iniziali di secondo e centimetro sono risolte nelle conversioni risultanti.

Revisione visiva di tutte le pagine in grigio: prime montature 001–008 prima della correzione, poi tutte le pagine modificate e restanti nelle montature finali 001–003 e 008–017. Le pagine non modificate di SCI04-T e SCI05-S erano già viste integralmente. Eliminati due slittamenti di una sola area di risposta in SCI04-S e GEO01-S mediante riduzione delle ripetizioni, senza ridurre il corpo del testo. Controllo finale: 33 pagine previste e presenti, nessuna anomalia automatica di formato, margini o contenuto estratto. Tabelle native editabili, spazi di risposta presenti; la prova di modifica manuale dell'ambiente resta nel collaudo finale.

Limiti: nessuna stampa fisica o sperimentazione educativa osservata; i dati inventati non sono misure reali. Le lacune per nucleo sono riportate nelle guide e in `produzione/contenuti`. Il lotto chiude la dotazione essenziale di scienze prevista, non tutta la disciplina.
