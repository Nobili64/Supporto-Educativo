# Redazione B — matematica, scienze, lingue e tecnologia

Consegna: `guide-b.json`, array UTF-8 di **61 record**, uno per ciascun ID assegnato nell’inventario autoritativo. Il brief e il contratto sono stati letti prima della redazione. Sono stati usati solo inventario e istruzioni della cartella; `Casi` non è stato aperto, gli originali e gli altri lotti non sono stati modificati.

## Copertura

| Gruppo | ID inclusi | Record |
|---|---|---:|
| Aritmetica e algebra | M08-01–M08-12 | 12 |
| Geometria, dati e probabilità | M09-01–M09-10 | 10 |
| Scienze | M10-01–M10-11 | 11 |
| Inglese | M11-01–M11-11 | 11 |
| Seconda lingua | M12-01–M12-08 | 8 |
| Tecnologia | M13-01–M13-09 | 9 |
| Totale | Tutti e soli gli ID con group da 8 a 13 | **61** |

Confronto automatico con inventario: nessun ID mancante, aggiuntivo o duplicato. Ogni record ha esattamente i 13 campi di primo livello del contratto, 2 tecniche, 3 passaggi, 3 criteri, 3 istruzioni a casa, 1 adattamento e 3 passaggi nell’esempio. Sono presenti consegna completa, svolgimento, risposta, prova diversa con soluzione/criteri e un errore spiegato e corretto.

## Revisione semantica

- Matematica: esempi e prove distinti, con dati, operazioni, unità e risposte. Sono espliciti calcolo mentale/scritto; multipli/divisori/potenze/radici; rapporti/proporzioni/percentuali; aritmetica/algebra; figure/solidi; misure lineari/aree/volumi/capacità/massa; perimetri/aree/superfici/volumi; Pitagora/similitudine; piano cartesiano/traslazione/simmetria; media/mediana/moda/frequenze.
- Scienze: osservazione separata da ipotesi e spiegazione; modelli con limiti; confronto controllato con variabile, misura e condizioni uguali; dati simulati dichiarati; tabelle e grafici con unità; relazione con origine dei dati; collegamenti salute/ambiente senza garanzie assolute.
- Inglese: ascolti con copioni forniti da leggere, testi e risposte, dialoghi a turni, presentazione e racconto distinti, tutte le varianti messaggio/e-mail/descrizione/racconto; grammatica, collocazioni, traduzioni e rappresentazioni con esempi completi. Pronuncia e intonazione richiedono un modello sonoro competente e riconoscimento reale da un ascoltatore.
- Seconda lingua: **tutte le 8 guide contengono francese, spagnolo e tedesco**, come alternative. Sono presenti note specifiche su età, articoli/genere, accusativo nella richiesta tedesca, negazione, elisione, segni di domanda spagnoli, accenti/ñ/umlaut, maiuscole dei nomi tedeschi, consonanti finali francesi e liaison. Si lavora nella lingua del corso, non nelle tre insieme.
- Cultura: contesti didattici immaginari dichiarati, parole di quantità conservate e confronto di pratiche delimitate. Nessuno stereotipo viene presentato come informazione su una nazione.
- Tecnologia: sono espliciti materiali/energia/sistemi, produzione/funzionamento, strumenti/convenzioni, progetto/realizzazione/documentazione, etichette/istruzioni/consumi. La guida M13-09 distingue programmi digitali, algoritmo e robotica con salvataggio/esportazione/stampa e due percorsi tracciabili su carta.

Gli adattamenti indicano un bisogno osservabile in prima persona, un passaggio preciso e un aiuto concreto. Per organizzazione, turno orale, manualità generale e tracciamento si usa `trasversale`; non si attribuisce automaticamente una difficoltà a una diagnosi. Il professionista riduce i suggerimenti didattici mentre mantiene gli strumenti compensativi utili.

## Controlli quantitativi e linguistici

Eseguiti **49 controlli quantitativi indipendenti e 2 simulazioni dei percorsi robotici**, tutti superati. Le verifiche hanno ricalcolato esempi e prove matematiche, variazioni dei grafici, densità/velocità, scale, area interna dell’etichetta ed energia delle lampade. Sono stati usati interi in centesimi per gli importi e frazioni esatte per rapporti e conversioni; non solo confronti tra formulazioni del JSON.

Risultati particolarmente esposti a errori: 402−185=217; 3 m²=30000 cm²; superficie del parallelepipedo 5×3×2 pari a 62 cm² e volume 30 cm³; mediana di 1,2,2,5 pari a 2 e media 2,5; 224 Wh=0,224 kWh; entrambi i percorsi `AVANTI, AVANTI, DESTRA, AVANTI, AVANTI` raggiungono la meta senza uscire dalla griglia.

Rilettura linguistica editoriale di tutte le consegne, svolgimenti e prove M11/M12: controllo di dati, tempi, negazioni, articoli e corrispondenza domanda/risposta. È stata scelta la forma tedesca non marcata **Ich spiele kein Tennis**. Questa rilettura non è una certificazione esterna da parte di docenti delle quattro lingue e non verifica una produzione orale mai ascoltata.

Per i punti di fonetica/grafia sono state consultate fonti primarie online l’8 ottobre 2026:

- Le coppie ship/sheep e sit/seat sono proposte per pratica di ascolto e produzione da [British Council — Short and long i](https://africa.teachingenglish.org.uk/classroom/pronunciation/short-long-i). Il testo evita una trascrizione italiana e rinvia al modello sonoro reale.
- La h senza valore fonico nello spagnolo standard degli esempi e la ñ come lettera/fonema distinto sono documentate da [RAE-ASALE — h](https://www.rae.es/dpd/h) e [RAE-ASALE — ñ](https://www.rae.es/dpd/%C3%B1). Non viene generalizzato il silenzio della h a ogni prestito o variante dialettale.
- Il ruolo del contesto nella pronuncia di consonanti finali e liaison è spiegato da [TV5MONDE — La liaison](https://apprendre.tv5monde.com/fr/aides/prononciation-la-liaison). Le note sulle parole francesi finali sono limitate alle forme isolate, senza dedurne una regola assoluta.
- Gli umlaut richiedono suoni distinti e controllo mediante ascolto nel materiale [Goethe-Institut — Deutsche Aussprache üben mit Musik, tutorial 10](https://www.goethe.de/resources/files/pdf288/deutsche-aussprache-uben-mit-musik_arbeitsblaetter-zu-den-tutorials.pdf). Il documento conferma il confronto sonoro, non è prova della pronuncia del singolo ragazzo.

I codici `dunlosky2013`, `ies2007`, `eef2025`, `aid` rimandano ai principi generali già verificati dal coordinatore. Consegne, esempi, adattamenti e applicazioni sono **redazione editoriale originale**, non citazioni né strumenti clinicamente validati.

## Controllo ripetibile della consegna

Da questa cartella si può controllare nuovamente il JSON con Python, senza creare altri file:

```python
import json
from pathlib import Path
p = Path('.')
inventory = json.loads((p/'inventario.json').read_text(encoding='utf-8-sig'))
guides = json.loads((p/'guide-b.json').read_text(encoding='utf-8'))
expected = {x['id'] for x in inventory if 8 <= x['group'] <= 13}
required = {'id','goal','materials','techniques','example','steps','transfer',
            'checks','error','home','adaptations','coach','sources'}
assert len(guides) == len(expected) == 61
assert len({g['id'] for g in guides}) == 61
assert {g['id'] for g in guides} == expected
for g in guides:
    assert set(g) == required
    assert len(g['techniques']) == 2
    assert 3 <= len(g['steps']) <= 5
    assert 2 <= len(g['checks']) <= 4
    assert len(g['home']) == 3
    assert 1 <= len(g['adaptations']) <= 3
    assert 2 <= len(g['example']['work']) <= 5
    assert set(g['example']) == {'task','work','result'}
    assert set(g['transfer']) == {'task','check'}
    assert set(g['error']) == {'wrong','why','fix'}
    for a in g['adaptations']:
        assert set(a) == {'stage','difficulty','categories','signal','aid','preserve','verify'}
        assert set(a['categories']) <= {'dislessia','disortografia','disgrafia','discalculia','trasversale'}
print('61 record: copertura e struttura conformi')
```

## Limiti

La consegna copre le attività assegnate, con un esempio e una prova per attività: non copre automaticamente ogni contenuto dei programmi scolastici. Soluzioni aperte equivalenti sono accettabili se soddisfano i criteri, senza imporre la memorizzazione della formulazione esemplificativa. Non sono state eseguite prove con ragazzi, una validazione clinica, una verifica del rendering dell’interfaccia, produzioni orali reali o esperimenti fisici. Le attività ascoltate richiedono un lettore/audio del corso; i copioni scritti sono già inclusi. Le realizzazioni tecnologiche sono limitate a strumenti e procedure autorizzati; i risultati simulati sono dichiarati come tali.
