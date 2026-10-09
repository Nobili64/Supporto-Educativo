# Controlli della consegna

30 settembre 2026. Controlli di integrità e coerenza editoriale; non validazione clinica del manuale.

| Controllo | Esito |
|---|---|
| Repertori | 175 tecniche: 53 / 34 / 49 / 39 |
| Schedario | 90 codici attesi, tutti presenti: MAP 14, MET 12, AUT 13, MAT 35, ITA 16 |
| Laboratorio | 132 risorse; 131 PDF esistenti e Registro.ods esistente |
| Compendio | 26 tecniche e 10 schede; tutte mappate |
| Totale principale | 433 righe |
| Supplementi | 40 righe; totale tabella 473 |
| Destinazioni | Tutti i codici rimandano a S/D/C, capitoli, allegati o appendici definiti |
| Catalogo | 50 S, 24 D, 7 C, 23 schede con 7 varianti semplificate, 7 strumenti |
| Indice | Capitoli 1–52 senza lacune o duplicati |
| Provenienza | Tutte le S hanno almeno una corrispondenza registrata; D27–D30 esplicitamente nuove |
| Intervalli delle fonti | Righe iniziali/finali entro i file correnti; codici di tabella univoci |
| Pagine | Somma stima manuale 276; allegati 37 + 17 = 54 |
| Metadati scientifici | 38/38 DOI risolti su Crossref, inclusi tre aggiornamenti; autori/titoli controllati |
| Confronto precedente | 256/257 file invariati; unica differenza: piano già aggiornato e dichiarato tale nelle fonti |

La presenza dei file e la validità dei codici sono controlli automatici. La pertinenza delle corrispondenze e le decisioni nel rapporto sono valutazioni editoriali, non esiti prodotti da un validatore. Non sono state certificate tutte le affermazioni dei repertori o le pagine dei materiali pronti.

## Copertura effettiva

Sono stati usati testi forniti per la ricognizione, fonti primarie o siti dei titolari per le verifiche esterne, abstract per conclusioni circoscritte e sezioni pertinenti dei documenti normativi. Le limitazioni di accesso e le versioni test non confermate sono nel registro fonti e nel rapporto test. I metadati Crossref attestano identità bibliografica, non validità degli studi.

Non è stata svolta la revisione clinica indipendente della tappa F, né una prova in seduta, né una prova di stampa del manuale, che non è ancora redatto. Nessun caso reale è stato letto o utilizzato. La cartella Casi non è stata enumerata. Nessuna modifica al materiale originale è necessaria per consultare questa consegna.

## Come ripetere i controlli

`finalizza.py` ricostruisce inventario, mappatura, catalogo, registro ragionato, indice e rapporto. Legge soltanto i percorsi esplicitamente ammessi nei file di costruzione; scrive nella cartella della consegna e nel nuovo indice in radice. Le impronte delle fonti correnti sono in `impronte-fonti-consegna.json`; il confronto con la ricognizione precedente è riportato in `esito-controlli.json`. I materiali della vecchia tappa A non vengono sovrascritti.

I controlli non autorizzano la tappa B: serve l'approvazione dell'indice prevista dal piano. Le eventuali fonti da acquisire nelle fasi successive sono identificate per singola affermazione; fino ad allora quelle affermazioni non entrano nel testo come verificate.
