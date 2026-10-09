# Contratto per la redazione delle guide
Scrivere solo i file assegnati nella nuova cartella. Non aprire Casi, non modificare originali. Nessun subagente. Tutto italiano rivolto a 11-14 anni. Scopo: guide operative per seduta professionista-ragazzo e uso autonomo a casa, carta e penna; nessun dato personale.
Inventario autoritativo: manutenzione/inventario.json. Ogni voce deve avere esattamente un record con id identico. Il record completo è:
{
"id":"M01-01",
"goal":"risultato concreto atteso",
"materials":["..."],
"techniques":[{"name":"nome tecnica","how":"come applicarla proprio qui","why":"a cosa serve"}],
"example":{"task":"consegna originale con tutti i dati/testo necessari","work":["2-5 passaggi svolti specifici"],"result":"risposta completa oppure produzione esemplificativa motivata"},
"steps":[{"title":"verbo e oggetto","do":"azione applicabile al compito scolastico portato","help":"suggerimento concreto"}],
"transfer":{"task":"mini compito originale diverso dall'esempio, con materiale necessario","check":"soluzione verificabile o criteri specifici per produzione aperta"},
"checks":["2-4 criteri osservabili specifici"],
"error":{"wrong":"errore esemplificato specifico","why":"perché è un errore","fix":"correzione concreta"},
"home":["3 brevi istruzioni su applicazione, ripresa distribuita e quando chiedere aiuto"],
"adaptations":[{"stage":"passaggio preciso","difficulty":"prima persona ragazzo, es. Perdo il punto leggendo","categories":["dislessia"],"signal":"cosa osservare senza presumere diagnosi","aid":"adattamento concreto","preserve":"obiettivo che resta invariato","verify":"come osservare utilità"}],
"coach":"indicazioni professionista su fading degli aiuti didattici, non strumenti compensativi; limiti specifici",
"sources":["dunlosky2013","ies2007","eef2025","aid"]
}
Usare 2 tecniche pertinenti, 3-5 steps concreti, 1-3 adattamenti significativi per record. Categorie ammesse: dislessia,disortografia,disgrafia,discalculia,trasversale. Non inventare legami diagnostici: trasversale per organizzazione, memoria, fatica, problemi motori generali. Il record deve contenere esempio svolto effettivo e prova nuova effettiva, non istruzioni vaghe 'scegli un brano'. Raggruppamenti originali: coprire esplicitamente tutte le varianti (per es. schede/ricerche/esposizioni), anche con note nei passaggi. Nessun placeholder. Nessuna falsa validazione clinica. Sources indicano principi generali, applicazioni ed esempi sono editoriali originali. Gli adattamenti non sono prescrizioni automatiche.
Questo è contenuto editoriale: revisione semantica e controlli di copertura sono più adatti di test che ne rispecchiano la formulazione. Scrivere JSON UTF-8 e controllare parsing, IDs/numero contro inventario assegnato, campi richiesti. Riferimenti già verificati dal coordinatore: Dunlosky recupero/ripasso, IES esempi/spiegazione, EEF metacognizione; AID scelta compensativi in base al bisogno. Fonti specialistiche nuove si verificano sul web prima di affermarle; non serve ricerca clinica individuale.

