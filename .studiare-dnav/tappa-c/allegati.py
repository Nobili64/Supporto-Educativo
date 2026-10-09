"""Schede originali A4: contenuto esplicito, spazi manoscritti, nessun punteggio."""
from pathlib import Path
import re
R=Path(__file__).resolve().parent;B=R.parent/'tappa-b'
def page(ident,run,title,body):return f'<!-- PAGE {ident}|{run} -->\n# {title}\n\n{body}\n\n'
def field(label,lines='two'):
 return f'<div class="field"><span class="label">{label}</span><div class="lines {lines}"></div></div>\n\n'
def head():return 'Nome o sigla __________________________  Data ______________\n\n'
def source(s):return f'<div class="source">Scheda originale · {s} · Puoi rispondere a voce, indicare, dettare o lasciare un campo per dopo. Non è un test.</div>'
def ordinary(n,title,intro,fields,tail='',ident=None):
 body=head()+intro+'\n\n'+''.join(field(*f) if isinstance(f,tuple) else field(f) for f in fields)+tail+'\n\n'+source(f'Scheda {n} · blocchi B–C')
 return page(ident or f'sch{n}',f'Scheda {n} · Versione ordinaria',f'{n}. {title}',body)
def simple(n,title,intro,fields,tail=''):
 body=head()+'<div class="simple">\n\n'+intro+'\n\n'+''.join(field(f,'two') for f in fields)+tail+'\n\n</div>\n\n'+source(f'Scheda {n} · proposta concreta 8–10 anni, adattabile')
 return page(f'sch{n}-semplice',f'Scheda {n} · Versione concreta',f'{n}. {title} · un passo alla volta',body)
def existing(kind):
 text=(B/f'{kind}.md').read_text(encoding='utf-8')
 chunks=re.split(r'(?=^<!-- PAGE )',text,flags=re.M)
 return {re.match(r'<!-- PAGE ([^|]+)',p)[1]:p for p in chunks if p.strip()}
def learner():
 old=existing('ragazzo');items=[]
 items += [v for k,v in old.items() if k.startswith('sch1') and not k.startswith('sch14')]
 items.append(ordinary(2,'La mia settimana','Prima segna gli impegni già fissati e le scadenze. Scrivi azioni piccole e concrete. Lascia spazio per cambiare il piano.',[
 ('Settimana dal __________ al __________ · Orario di chiusura del lavoro concordato','one')],
 '''| Giorno | Impegni / scadenze | Azione di studio e ripresa |
|---|---|---|
| Lunedì | &nbsp; | &nbsp; |
| Martedì | &nbsp; | &nbsp; |
| Mercoledì | &nbsp; | &nbsp; |
| Giovedì | &nbsp; | &nbsp; |
| Venerdì | &nbsp; | &nbsp; |
| Sabato | &nbsp; | &nbsp; |
| Domenica | &nbsp; | &nbsp; |

'''+field('Margine / aiuto da chiedere / che cosa modifico','three')+'Un piano può cambiare. Se il lavoro non entra, chiediamo un accordo: non serve riempire ogni spazio.'))
 items.append(simple(2,'La mia settimana','Cominciamo da oggi e domani. Un adulto può leggere e scrivere con te.',[
 'Oggi ho già questi impegni','Oggi provo questo piccolo pezzo','Domani mi serve…','Chi mi aiuta e quando guardiamo di nuovo il piano']))
 items.append(ordinary(3,'Il primo passo','Scegli un compito. Prepariamo un inizio possibile e il modo di riprendere dopo una pausa.',[
 'Il compito e ciò che mi serve','Il primo gesto che posso fare','Quando o dopo quale segnale comincio','Dove mi fermo e da dove riparto dopo la pausa','L’aiuto concordato e quando lo chiedo','Dopo la prova: che cosa è successo? Che cosa cambiamo?']))
 items.append(simple(3,'Il primo passo','Non devi finire tutto adesso. Scegliamo come cominciare.',[
 'Il compito di oggi','Per iniziare faccio questo gesto','Mi può aiutare…','Dopo la prova: che cosa tengo o cambio?']))
 items.append(ordinary(4,'Leggere con una domanda','Puoi leggere, ascoltare o farti leggere il testo. Controlla la risposta nella fonte.',[
 'Titolo / fonte / tratto da usare','La domanda a cui voglio rispondere','La mia risposta, con parole mie','Il punto del testo che la sostiene','Una parola o un legame da chiarire','Che cosa correggo o voglio verificare']))
 items.append(simple(4,'Leggere con una domanda','Un adulto può leggere il testo e scrivere ciò che dici.',[
 'La domanda di oggi','La mia risposta','Dove troviamo la risposta nel testo?','Che cosa voglio capire meglio?']))
 items.append(ordinary(5,'Scheletro di mappa: domanda e legami','Scrivi o detta pochi concetti. Scegli i legami e leggili come frasi. Puoi usare anche un elenco, se è più chiaro.',[
 ('La domanda guida','two'),('Fonte e tratto usato','one'),('Concetti candidati, da scegliere e spostare','two')],
 '<div class="writebox" style="min-height:72mm">Spazio per concetti, frecce e parole-legame<br><br>Ogni collegamento deve poter essere letto come una frase.</div>'+field('Leggo e controllo un legame: che cosa confermo o correggo?','two')))
 items.append(ordinary(6,'La mappa a memoria','Dopo aver studiato, copri la fonte di contenuto e prova a ricostruire. Puoi rispondere anche con frasi orali o scritte. Poi riapri e correggi.',[
 ('Domanda e contenuto studiato','two'),('Supporti che restano disponibili','one')],
 '<div class="writebox" style="min-height:82mm">Il mio tentativo: concetti e legami, oppure una risposta in frasi</div>'+field('Dopo il controllo: che cosa aggiungo o correggo?','three')+'Segna con un asterisco le aggiunte fatte dopo aver riaperto la fonte. Non è un voto.'))
 items.append(ordinary(7,'I tre mucchi del ripasso','Prova a rispondere prima di controllare. Dopo il controllo scegli: da riprendere / con aiuto / riesco a spiegare. Anche le risposte sicure si ricontrollano più avanti.',[
 ('Argomento e fonte delle risposte corrette','one')],
 '''| Domanda / carta | Data e aiuti | Dopo il controllo: mucchio | Prossima ripresa |
|---|---|---|---|
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |

'''+field('Una risposta che ho corretto e la versione corretta','three')+field('Che cosa cambio nel prossimo ripasso?','two')+'I mucchi descrivono una prova, non il tuo valore. Gli intervalli si possono cambiare.'))
 items.append(ordinary(10,'Il mio strumento: prova e scelta','Confrontiamo modi accessibili di lavorare. Non serve togliere un aiuto necessario per dimostrare che ti serve.',[
 'Compito e risultato che voglio ottenere','Strumento / configurazione e come ho imparato a usarlo','Che cosa ho saputo fare e con quali aiuti','Tempo indicativo, fatica e gradimento: che cosa ho notato?','Quando mi aiuta / quando non basta','Prossima prova o accordo da chiarire con la scuola']))
 items.append(ordinary(11,'I miei punti di forza','Cerchiamo episodi concreti. Puoi non riconoscerti in una parola e proporne un’altra.',[
 'Una capacità o un modo di agire che riconosco','Primo episodio: che cosa ho fatto e quale risultato ho visto?','Quali supporti o persone mi hanno aiutato?','Un secondo episodio, oppure «da verificare»','Quando questa risorsa non basta o mi serve aiuto','Dove vorrei provarla di nuovo']))
 items += [v for k,v in old.items() if k.startswith('sch14')]
 cards=[('Curiosità','Fare una domanda per capire qualcosa che mi interessa.'),('Cura','Trattare con attenzione me, gli altri o ciò che uso.'),('Collaborazione','Dare e chiedere aiuto rispettando i limiti di ciascuno.'),('Autonomia','Partecipare alle scelte e usare gli aiuti che mi servono.'),('Correttezza','Dire ciò che so e ciò che devo ancora controllare.'),('Coraggio','Provare una scelta importante, con protezione e supporti.'),('Rispetto','Considerare i bisogni miei e degli altri.'),('Creatività','Cercare una possibilità nuova, quando è utile.'),('Responsabilità','Prendermi cura di un impegno realistico e degli accordi.'),('Equilibrio','Dare spazio anche a riposo, relazioni e attività importanti.')]
 body=head()+'Queste parole sono possibilità, non obblighi. Scegline poche, cambiale o aggiungine una tua. Le descrizioni sono esempi: puoi non riconoscerti.\n\n<div class="cards">'+''.join(f'<div class="card"><strong>{a}</strong><p>{b}</p></div>' for a,b in cards)+'<div class="card"><strong>Una parola mia</strong><br>________________________</div><div class="card"><strong>Per ora non scelgo</strong><p>Posso tornarci più avanti.</p></div></div>\n\n'+source('Scheda 15 · carte originali per D4, non riproduzione di mazzi pubblicati')
 items.append(page('sch15-carte','Scheda 15 · Carte dei valori · 1 di 2','15. Carte dei valori per lo studio',body))
 items.append(ordinary(15,'Una direzione e un gesto','Non serve scegliere un valore per sempre. Partiamo da una situazione concreta.',[
 'La parola che scelgo, oppure una parola mia','Un episodio in cui questa direzione ha contato per me','Un gesto piccolo e possibile nello studio','Gli aiuti e i limiti di cui tengo conto','Quando lo provo e quando ne riparliamo','Dopo: che cosa è successo? Voglio cambiare qualcosa?'],ident='sch15-scelta'))
 items.append(ordinary(16,'Il mio Consulente quando studio','Puoi parlare di «pensiero» senza dargli un nome o un volto. Non devi scrivere ciò che vuoi tenere privato.',[
 'Situazione concreta','Una frase che noto, se voglio condividerla','Quando la seguo, che cosa faccio?','Che cosa è utile controllare nella situazione reale?','Quale gesto o aiuto scelgo adesso?','Dopo la prova: che cosa noto?']))
 items.append(simple(16,'Una frase della mia mente','Una frase può arrivare mentre studi. Non devi farla sparire.',[
 'Che cosa stavo facendo?','Una frase che voglio raccontare, oppure lascio vuoto','Che cosa mi aiuterebbe adesso?','Il piccolo gesto che scelgo, oppure mi fermo']))
 items.append(ordinary(17,'Mappa dell’efficacia','Guarda un episodio, senza giudicarti. Scrivi «non so» quando manca un’informazione.',[
 'Prima: situazione e ciò che mi serviva','Che cosa ho fatto, concretamente','Subito dopo: benefici, costi o cambiamenti','Più tardi: ciò che so / ciò che devo verificare','Una possibilità da provare, con aiuti e possibilità di stop','Dopo la prova: risultato osservato, diverso dalla previsione?']))
 items.append(ordinary(19,'AND prima di una prova','Puoi usare questa traccia, modificarla o non usarla. Occhi aperti se preferisci. Non devi evocare un ricordo difficile né diventare calmo.',[
 ('A · Attenzione: che cosa noto qui e ora? Posso scegliere un oggetto esterno.','three'),('N · Nominare: quali parole concrete descrivono ciò che noto?','three'),('D · Descrivere: riconosco un’emozione? Posso scrivere «non so».','three'),('Il prossimo gesto, aiuto o pausa che scelgo','three')],
 'Se la prova dà fastidio, la interrompiamo. Nominare una sensazione non dimostra quale emozione sia.'))
 guide=page('guida','Schede di lavoro · uso e limiti','Scegli una pagina utile',
 'Allegato cumulativo dei blocchi B–C: Schede 1–7, 10–11, 14–17 e 19. Le Schede 1, 2, 3, 4, 14 e 16 includono una proposta più concreta per 8–10 anni, adattabile anche ad altre età. La numerazione segue il catalogo completo: i salti sono intenzionali.\n\n'
 'Stampa solo la pagina necessaria in A4, bianco e nero, dimensioni effettive / 100%. I fogli sono pensati per carta e penna e non contengono campi elettronici. Puoi leggere, trascrivere sotto dettatura o usare un foglio più grande. Non trasformare la compilazione in un compito aggiuntivo.\n\n'
 'Le schede sono tracce originali, senza punteggi, norme o soglie. Una risposta vuota non indica assenza di difficoltà. Concorda che cosa conservare e condividere entro mandato, riservatezza e obblighi applicabili; non consegnare automaticamente l’intero foglio a scuola o famiglia.\n\n'
 'La prova fisica di stampa e la prova in seduta restano da effettuare. Gli esempi e le varianti per età sono proposte editoriali, non versioni validate. Per scelta e procedura usa il manuale, non il solo foglio.\n\n'
 'La Scheda 15 occupa due pagine: carte e scelta operativa. Puoi usare le carte senza ritagliarle. Le altre pagine sono autonome; l’indice riporta la pagina di ogni versione.')
 return guide+page('indice','Consultazione','Indice','[INDICE]')+''.join(items)
def clinician():
 old=existing('clinico');oldtext=''.join(v for k,v in old.items() if k!='guida')
 body='Codice __________________  Data __________  Professionista __________________\n\n'
 body+='I livelli sono descrittivi e riferiti al compito: 1 con modello; 2 con guida; 3 autonomo con supporti; 4 trasferisce. Non sommarli e non attribuirli alla persona nel suo insieme.\n\n'
 body+=field('Compito / richiesta / contesto e fonte dell’informazione','two')
 body+='''| Filo e obiettivo specifico | Livello / non esplorato | Prova concreta e aiuti umani |
|---|---|---|
| Metodo: strategia S____ | &nbsp; | &nbsp; |
| DNA-V: scelta o abilità D____ | &nbsp; | &nbsp; |
| Consapevolezza: descrizione C____ | &nbsp; | &nbsp; |

'''+field('Strumenti compensativi e condizioni mantenute','two')+field('Correttezza / controllo degli errori / costo riferito','three')+field('Che cosa rimane incerto o solo riferito','two')
 new=page('str5a','Strumento 5 · Padronanza · 1 di 2','5. Griglia di padronanza dei tre fili',body)
 body='Codice __________________  Data __________  Riferimento alla prova __________\n\n'
 body+='Non inferire padronanza dalla sola partecipazione, dal tono di voce o dall’assenza di ansia. Per il filo DNA-V osserva una scelta contestuale; per consapevolezza una descrizione correggibile.\n\n'
 body+=field('Seconda occasione: stesso contenuto o compito nuovo? Che cosa cambia?','three')
 body+=field('Risultato osservato e confronto con la prima prova','three')
 body+=field('Aiuti umani ridotti, mantenuti o aggiunti; supporti necessari stabili','three')
 body+=field('Decisione motivata: mantenere / insegnare ancora / adattare / rivedere obiettivo','three')
 body+=field('Prossimo riscontro, data e chi farà che cosa','two')
 body+='<div class="source">Traguardi di fase editoriali, non soglie validate. Autonomia non significa eliminazione degli strumenti. Non sostituisce una valutazione clinica o scolastica.</div>'
 new+=page('str5b','Strumento 5 · Padronanza · 2 di 2','5. Dalla prova alla decisione',body)
 body='Codice __________________  Data __________  Incontro n. ______  Fase ______\n\n'
 body+=field('Obiettivo concordato e aggiornamento di appropriatezza, se necessario','two')
 body+=field('Compito, strategia S / tecnica D / tappa C effettivamente usata','two')
 body+=field('Osservato: azioni, risultato, aiuti, tempo indicativo','three')
 body+=field('Riferito dal ragazzo o da altri: fonte e costo / gradimento','two')
 body+=field('Ipotesi professionale e alternative da verificare','two')
 body+=field('Decisione e seguito concordato, senza anticipare risultati','three')
 new+=page('str6a','Strumento 6 · Registro e monitoraggio · 1 di 2','6. Registro essenziale dell’incontro',body)
 body='Codice __________________  Periodo __________  Obiettivo __________________\n\n'
 body+='Confronta prove pertinenti. Specifica se il dato è osservato, riferito o documentato; registra ciò che cambia oltre alla strategia. Non togliere un supporto necessario per costruire una linea di base.\n\n'
 body+='''| Data / compito | Supporti e aiuti | Risultato / costo | Fonte / differenze di contesto |
|---|---|---|---|
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |
| &nbsp; | &nbsp; | &nbsp; | &nbsp; |

'''
 body+=field('Che cosa possiamo concludere, limitatamente a queste prove?','three')
 body+=field('Che cosa non è ancora verificato, soprattutto fuori dalla seduta?','three')
 body+=field('Prossima decisione / accordi di condivisione / data di revisione','three')
 body+='<div class="source">Strumento informale originale. Non calcolare un punteggio totale né dedurre efficacia causale da un solo confronto. Custodire con la documentazione professionale protetta.</div>'
 new+=page('str6b','Strumento 6 · Registro e monitoraggio · 2 di 2','6. Confronto fra prove nel tempo',body)
 guide=page('guida','Strumenti del clinico · uso e limiti','Osservare, distinguere, decidere',
 'Allegato cumulativo: Strumenti 1–4 per avvio e profilo iniziale; Strumento 5 per padronanza descrittiva dei tre fili; Strumento 6 per registro e monitoraggio delle prove. La valutazione conclusiva del percorso sarà sviluppata in una fase successiva.\n\n'
 'Compila solo ciò che serve al quesito. Distingui osservato, riferito, documentato e ipotizzato. Scrivi «non esplorato» quando manca un dato. I livelli non sono punteggi da sommare; nessun modulo contiene norme o cut-off.\n\n'
 'Conserva i supporti necessari e documenta gli aiuti umani. Non provocare fatica o disagio per misurare una prestazione senza aiuti. Il semaforo sostiene il giudizio professionale e non sostituisce valutazione del rischio, test o documentazione clinica.\n\n'
 'Custodisci i fogli nella documentazione professionale; condividi soltanto contenuti pertinenti secondo mandato, autorizzazioni e obblighi applicabili. Per osservazioni sulla bozza usa appunti privi di dati identificativi.\n\n'
 'Stampa A4 al 100%, in bianco e nero. Compilazione manoscritta; prova fisica di stampa ancora da effettuare. Le versioni per età sono adattamenti editoriali. L’indice distingue le pagine dei moduli multipagina.')
 return guide+page('indice','Consultazione','Indice','[INDICE]')+oldtext+new
if __name__=='__main__':
 (R/'ragazzo.md').write_text(learner(),encoding='utf-8')
 (R/'clinico.md').write_text(clinician(),encoding='utf-8')
