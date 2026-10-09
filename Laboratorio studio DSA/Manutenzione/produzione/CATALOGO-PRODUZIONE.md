# Produzione del catalogo

L'uso quotidiano richiede soltanto Calc e il comando Aggiorna indice. Questi strumenti di produzione servono al manutentore e usano dipendenze esterne alla biblioteca, non incluse nel pacchetto condivisibile.

`Catalogo.ods` è l'autorità editoriale: `prepara_catalogo.py` conserva le righe esistenti e aggiunge soltanto gli ID nuovi dalle registrazioni. Il foglio Bibliografia conserva il contenuto completo del campo Fonti; Risorse contiene un rimando esatto per ID. Alla rilettura il riferimento viene risolto dal foglio Bibliografia. La mancanza della bibliografia corrispondente provoca un errore, senza ricrearla silenziosamente.

Per la ricostruzione: eseguire `prepara_catalogo.py`, copiare il generatore corrente `catalogo.mjs` nella cartella di lavoro `.lavorazione-dsa` del progetto e avviarlo con Node e il pacchetto `@oai/artifact-tool` disponibile in quell'ambiente. Il generatore crea XLSX, immagini di controllo e converte il risultato in ODS tramite LibreOffice. La copia qui conservata è la sorgente del generatore; non va avviata direttamente dalla cartella produzione perché i percorsi di lavoro sono relativi allo script.

Prima di sostituire il catalogo corrente conservare una copia. Dopo la conversione controllare fogli, formule, date, campi e immagini; quindi aggiornare l'indice e verificare la copia offline. La migrazione a Bibliografia del 30/09/2026 è documentata da `verifica_bibliografia.py` e `verifiche/catalogo-bibliografia.json`. Quel controllo usa la copia storica a 101 risorse: attesta questa migrazione, non tutte le future modifiche manuali.

Le citazioni per intero restano anche nelle guide tutor. Un rimando del catalogo a una fonte non implica che la fonte convalidi l'efficacia didattica del kit.
