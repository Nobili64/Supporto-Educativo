"""Registro ragionato delle fonti: note editoriali distinte dai metadati."""
from pathlib import Path
import json,re
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
refs=json.loads((OUT/'registro-fonti-locali.json').read_text(encoding='utf-8'))
notes='''CAP5,C3|Testo normativo locale; controllo online Normattiva|DSA riconosciuti e misure di supporto; non assimilare automaticamente ADHD o profilo non verbale ai quattro disturbi della legge.
CAP5,S25,S50,CAP52|PDF locale, artt. 4–6 e sezioni pertinenti delle linee guida|PDP, strumenti e competenza d'uso. Non usare il paragrafo sugli stili come prova scientifica. Il DM 2011 da solo non basta per le regole attuali d'esame: integrare D.Lgs. 62/2017, distinguendo cicli, dispensa ed esonero.
CAP5,CAP42,CAP44|Testo locale; pagina istituzionale BES|Misure per bisogni educativi speciali e decisioni scolastiche; non attribuire a una diagnosi associata tutti gli automatismi della legge 170.
CAP37–45|Identificazione ufficiale ISS e rinvii al PDF locale|Linea guida sanitaria su diagnosi/trattamento: fonte per profili e confini, non prova del percorso integrato. Pagine segnalate nell'indice locale da controllare sul testo quando si redige il profilo.
CAP5,CAP50|Testo locale e pagina CNOP vigente|Informazione, consenso per minori e rapporto fra committente e destinatario. Integrare regole di segreto professionale. Evitare promesse assolute sulla condivisione.
CAP5,CAP13|Testo locale artt. 1 e 3|Sostegno psicologico rientra nella professione; psicoterapia richiede formazione specifica. Non definire il confine solo in base al nome dell'esercizio.
CAP5,CAP13|PDF locale NG134, raccomandazioni 1.5.3–1.5.8 e 1.6.4–1.6.6|Trattamenti differenziati per età e gravità. Fonte internazionale: non chiamarla normativa italiana. Il sostegno del manuale non sostituisce valutazione e trattamento indicati.
CAP5,CAP13,CAP46|PDF locale CG159, 1.4.9–1.4.10 e 1.5.3–1.5.5|Riguarda ansia sociale; distingue valutazione e CBT specifica. La citazione di questionari non ne certifica norme italiane o appropriatezza per ogni ragazzo.
CAP4,S15,S16,S26–30|Abstract originale nel dossier|Alta utilità di practice testing e distribuzione; moderata per auto-spiegazione, elaborazione e interleaving; bassa generalizzabilità di altre tecniche. Bassa utilità non significa mai utile. Estensione ai singoli profili DSA da osservare.
S26,C5|Abstract originale nel dossier|Richiamo migliora ritenzione differita rispetto a ristudio nelle condizioni esaminate; fiducia soggettiva e prestazione possono divergere. Nessuna prescrizione universale di un intervallo ottimale.
S26,S36|Abstract originale nel dossier|Meta-analisi a favore delle prove di recupero; l'effetto dipende anche dalle condizioni. Non equiparare qualsiasi interrogazione o voto a una buona pratica di recupero con controllo dell'errore.
CAP2|Descrizione ERIC nel dossier, non abstract degli autori|Sostegno all'insegnamento situato delle abilità di studio. Il dettaglio del vantaggio metacognitivo non è verificato in questa descrizione: usare Donker per l'affermazione pertinente.
CAP2,C5,S38|Abstract originale nel dossier|Istruzione sulle strategie nella primaria/secondaria; utile conoscenza metacognitiva. Effetti maggiori nelle prove costruite dagli autori: non promettere analoghi cambiamenti nei voti o trasferimento lontano.
S18,S19|Abstract originale nel dossier|Mappe concettuali associate a benefici di ritenzione in contesti diversi, con eterogeneità e confronti diversi. Non prova di superiorità in ogni condizione o per ogni DSA.
S19|Abstract originale nel dossier|g=0,72 per costruzione e g=0,43 per studio sono confronti con rispettive condizioni di confronto in analisi di moderazione. Non presentarli come unico confronto diretto universale fra costruire e ricevere una mappa.
S19,S26|Abstract originale nel dossier|Recupero superiore alla specifica condizione elaborativa con mappe nello studio. La sequenza integrata dei cinque passi del manuale è un adattamento; non è il protocollo sperimentale validato da questo articolo.
S19|Abstract originale nel dossier|Studio su 124 universitari: beneficio della costruzione completa rispetto a mappa fornita. Non generalizzare direttamente a 8–16 DSA né inventare l'esito dell'interazione con autoregolazione.
S20|Abstract originale nel dossier|Piccolo studio su studenti di medicina. Vantaggio osservato a una settimana con intervallo che include zero; stima aggiustata per motivazione distinta dal dato grezzo. Mappa mentale proposta per esplorazione, senza promesse mnestiche forti.
S12,S38|Abstract e testo integrale locale disponibili; risultati pertinenti|Sintesi vocale/lettura assistita: effetto medio positivo sulla comprensione nei campioni esaminati (circa 0,35), eterogenei. Provare utilità e carico nella persona; non sostituire automaticamente ogni lettura.
S11|Descrizione/abstract nel dossier|Insegnamento reciproco: base per dialogo su previsione, domanda, chiarimento e sintesi. La versione individuale abbreviata è adattata e non equivale al programma valutato.
S42,S44|Abstract originale nel dossier|Strategie di scrittura e altre componenti possono migliorare la qualità dei testi. Istruzione grammaticale isolata non va presentata come via dimostrata per migliorare la scrittura; S44 risponde a richieste curriculari diverse.
S47|Abstract originale nel dossier|Istruzione basata su schemi nei problemi per studenti con difficoltà di apprendimento. Evitare una sola griglia meccanica per ogni problema; rappresentazione e scelta delle relazioni sono essenziali.
S1,S2,S3,CAP42|Abstract e testo integrale locale disponibili; risultati pertinenti|HOPS: campione piccolo, guadagni riferiti dai genitori non equivalenti a conferma degli insegnanti. Un planner isolato non è l'intero intervento. Verificare trasferimento a casa/scuola.
S1,S2,S40,CAP42|Abstract e testo integrale locale disponibili; risultati pertinenti|Training organizzativo strutturato per bambini con ADHD. Non attribuire gli effetti dell'intero programma alla singola lista o seduta del manuale.
CAP4,CAP13|Solo sintesi non testuale nel dossier|Liu 2023: esistenza e contesto verificabili; la sintesi non basta per riportare effetti numerici o tempi precisi degli effetti. Nel manuale solo descrizione prudente di evidenza preliminare; reperire originale se si vogliono quantificare risultati.
CAP4,CAP13|Abstract originale nel dossier|Shao 2024: assegnazione di sei classi, 139 studenti. I drm citati nell'abstract sono cambiamenti entro il gruppo in presenza, non differenze rispetto al controllo. Non trasformarli in una prova di efficacia per DSA individuale.
CAP4,D2|Abstract originale nel dossier|Non sostenuto l'abbinamento dell'insegnamento a stili fissi. Ascoltare preferenze non equivale ad adottare la teoria degli stili.
CAP4,S39|Abstract e testo integrale locale disponibili|Nessun vantaggio specifico del font esaminato: non promettere trattamento della dislessia con caratteri speciali. Consentire preferenze di leggibilità.
CAP4,S39|Abstract e testo integrale locale disponibili|Font Dyslexie senza beneficio specifico dimostrato nelle condizioni esaminate. Separare forma delle lettere, spaziatura e familiarità.
CAP4|Abstract originale nel dossier|Revisione su lenti/filtri colorati: evidenza non sufficiente per raccomandarli come intervento sulle difficoltà di lettura. Non estendere il giudizio ad altre prescrizioni oftalmologiche.
CAP4,CAP42|Abstract originale nel dossier|Allenamento della memoria di lavoro: limiti del trasferimento lontano e duraturo. Non proporlo come cura generale di studio o DSA; giochi restano occasioni osservazionali.
CAP4,S12|Abstract originale nel dossier|Compromessi fra velocità e comprensione; non promettere lettura molto più rapida conservando ogni livello di comprensione. Distinguere lettura esplorativa da studio approfondito.
C4,D17|Abstract originale nel dossier|Non emerge un vantaggio generale di creatività nella dislessia; differenze per età e misure non autorizzano stereotipi individuali.
CAP4,S12|Abstract originale nel dossier|Beneficio immediato della spaziatura in quel disegno; non dimostra rimedio stabile, universale o sostitutivo della didattica.
CAP4,S12|Abstract originale nel dossier|Spaziatura: distinguere velocità e accuratezza; risultati non autorizzano a generalizzare il primo studio positivo.
CAP4,S12|Abstract originale nel dossier|Forma speciale e spaziatura da distinguere; un effetto di impaginazione non dimostra efficacia del font come trattamento.
CAP4,S12|Abstract originale nel dossier|Controllare generalità dell'effetto e confronto con lettori senza dislessia; non attribuire specificità diagnostica dove non è dimostrata.
CAP4,S12|Abstract e testo integrale locale disponibili|Risultati su forma e spaziatura ridimensionano promesse semplici. Decisione: provare accessibilità senza prescrivere una spaziatura terapeutica unica.
CAP46|Scheda locale dell'edizione 2022; nuova verifica editore/anteprima 2026|Aggiornamento necessario: AMOS 8–16 esiste nel 2026. Vedi rapporto test per tempi, licenza e distinzione fra edizioni.
CAP46|Abstract originale e modulo ufficiale|Screening ansia, non diagnosi; versioni ragazzo/genitore. Uso italiano richiede riferimento specifico, non solo articolo di sviluppo originale.
CAP46|Abstract originale nel dossier e PubMed|Supporto psicometrico italiano negli adolescenti. Non estendere automaticamente le norme a 8 anni; integrato con Scaini 2017.
CAP46|Abstract originale e sito ufficiale UCLA|Italiano disponibile; non verificata qui una normazione italiana pertinente alla forma scelta. Riserva, con permessi aggiornati.
CAP46|Voce locale e sito Hogrefe Italia|Edizione italiana 2018, 7–17; manuale e qualifica professionale richiesti. Tempi della singola forma da confermare.
CAP46|Abstract originale e sito dei titolari|Screening multi-informatore; norme italiane consultate genitori classi 1–8. Attenzione a età, informatore e licenza.
CAP46|Abstract originale; studi italiani identificati|La forma breve italiana e la proposta a sette item nei più piccoli non sono intercambiabili. Misura inflessibilità, non tutte le componenti del DNA-V.
CAP14|Scheda bibliografica e indice del programma nel dossier|Confronto organizzativo facoltativo, non testo integralmente consultato né prova che il nuovo percorso abbia la stessa efficacia.'''.splitlines()
assert len(notes)==len(refs),(len(notes),len(refs))
intro='''# Fonti: affermazioni sostenibili e limiti

Tappa A · 30 settembre 2026. Registro di 46 voci locali, più aggiornamenti individuati in questa tappa. Una fonte bibliograficamente esistente non è automaticamente pertinente o sufficiente per una specifica affermazione. La verifica distingue metadati, abstract, estratti e testo integrale disponibile.

Il dossier locale riporta i riferimenti completi. Le righe seguenti decidono che cosa può entrare nel manuale. Non si dichiara una revisione sistematica completa della letteratura né una lettura integrale di ogni articolo. I testi integrali disponibili localmente sono sei; la loro disponibilità non viene usata per attribuire a questa tappa un audit completo di ogni metodo e risultato.

## Registro delle fonti locali

'''
for ref,note in zip(refs,notes):
    targets,access,judgment=note.split('|');ref.update(destinazioni=targets,consultazione=access,decisione=judgment)
    local=ROOT/ref['file']
    link='; '.join('['+d.rstrip('.,;)')+'](https://doi.org/'+d.rstrip('.,;)')+')' for d in ref['doi'][:1])
    intro+=f"### {ref['id']} · {ref['titolo']}\n\n- Destinazione: {targets}.\n- Base controllata: {access}.\n- Decisione: {judgment}\n- Fonte: [dossier, righe {ref['riga_inizio']}–{ref['riga_fine']}](<{local}:{ref['riga_inizio']}>). {link}\n\n"
intro+='''## Aggiornamento DNA-V al 30 settembre 2026

Ricerca mirata con combinazioni di DNA-V, trial, adolescenti, 2025/2026 e systematic review; consultazione di PubMed, metadati Crossref e portali degli autori/editore. La pagina del coautore del modello è stata usata per rintracciare studi, non come valutazione indipendente della loro efficacia.

| Fonte aggiunta | Verifica ottenuta | Implicazione per il manuale |
|---|---|---|
| Byrne e Sherlock (2026), revisione sistematica, DOI 10.1016/j.jcbs.2025.100973 | Titolo, autori e pubblicazione confermati nei metadati Crossref. Accesso all'originale dell'editore non riuscito; non verificati qui risultati e qualità della revisione. | Citare nel registro degli aggiornamenti da acquisire; non ripetere come accertati i giudizi riportati dal sito del modello. Non fondare su questa fonte conclusioni nuove prima di leggere almeno l'abstract originale. |
| Petersen, Petersen e Pimentel (2026), DOI 10.1176/appi.psychotherapy.20250034 | Abstract originale PubMed: sette adolescenti, otto incontri di gruppo, studio preliminare senza controllo; flessibilità relativamente stabile, lievi riduzioni di ansia/inflessibilità e accettabilità positiva. | Indizio di fattibilità/accettabilità, non dimostrazione di efficacia del presente percorso individuale per DSA. |
| Nisar et al. (2025), DOI 10.1016/j.jcbs.2025.100886 | Abstract nel portale universitario degli autori: 20 scuole, 745 bambini; confronto fra sostegno aggiuntivo e standard all'implementazione dello stesso programma Connect PSHE. Nessuna differenza sull'esito primario del sostegno aggiuntivo. | Il confronto non isola l'effetto del curriculum rispetto ad assenza di intervento. Non usarlo per affermare efficacia specifica del pacchetto DNA-V del manuale o delle sue varianti 8–10. |

Fonti dirette: [metadati della revisione](https://api.crossref.org/works/10.1016/j.jcbs.2025.100973), [Petersen et al., abstract originale](https://pubmed.ncbi.nlm.nih.gov/41656521/), [Nisar et al., portale University of Bath](https://researchportal.bath.ac.uk/en/publications/adding-implementation-support-to-a-universal-acceptance-and-commi/).

**Formulazione proposta:** il DNA-V offre una cornice evolutiva per lavorare su scelte, consapevolezza e flessibilità. Esistono studi preliminari in popolazioni e contesti diversi; questa ricognizione non identifica una validazione del pacchetto individuale integrato 8–16 DSA qui proposto. Non affermare che il metodo tratti la depressione o che migliori il rendimento scolastico in virtù del solo DNA-V. Gli adattamenti di questo manuale saranno riconoscibili come tali.

## Affermazioni da non importare dalle sintesi

- Non presentare i due effetti della meta-analisi di Schroeder come un confronto diretto universale fra costruire e ricevere mappe.
- Non chiamare la sequenza mappa aperta → mappa chiusa un protocollo validato da Karpicke e Blunt: il suo uso qui è una sintesi editoriale di principi distinti.
- Non ricavare da Shao effetti fra gruppi a partire dai cambiamenti entro gruppo riportati nell'abstract.
- Non attribuire a Hattie dettagli metacognitivi non presenti nella descrizione ERIC consultata.
- Non equiparare maggiore motivazione, gradimento, flessibilità e voti: sono esiti diversi.
- «Non trovato in questa ricerca» non significa «non esiste». Le fonti non accessibili sono segnalate; non vengono completate per congettura.

## Verifiche residue nella fase di redazione

Gli elementi non risolti non sono nascosti: testo originale Liu per affermazioni quantitative; revisione Byrne–Sherlock prima di riportarne le conclusioni; norme italiane RCADS se si decide di usarla; manuali e diritti delle versioni test effettivamente scelte; pagine stampate dei libri nelle citazioni definitive; raccomandazioni ISS pertinenti al singolo profilo; norme d'esame per ciclo e anno. L'indice può essere approvato mantenendo queste limitazioni perché non dipende da affermazioni non verificate o da un test obbligatorio.
'''
(OUT/'05-fonti-e-limiti.md').write_text(intro,encoding='utf-8')
(OUT/'registro-fonti-commentato.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf-8')
print('Registro: '+str(len(refs))+' voci commentate')
