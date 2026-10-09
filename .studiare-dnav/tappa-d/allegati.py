from pathlib import Path
import re
R=Path(__file__).resolve().parent;C=R.parent/'tappa-c'
def page(i,run,title,body):return f'<!-- PAGE {i}|{run} -->\n# {title}\n\n{body}\n\n'
def field(label,n='two'):return f'<div class="field"><span class="label">{label}</span><div class="lines {n}"></div></div>\n\n'
def head():return 'Nome o sigla __________________________  Data ______________\n\n'
def source(n):return f'<div class="source">Scheda {n} · Formulazione originale, non un test. Puoi rispondere a voce, indicare, dettare o lasciare un campo per dopo. Condivisione da concordare.</div>'
def sheet(n,title,intro,fields,tail='',ident=None,run=None):
 return page(ident or f'sch{n}',run or f'Scheda {n} · Versione ordinaria',f'{n}. {title}',head()+intro+'\n\n'+''.join(field(*f) if isinstance(f,tuple) else field(f) for f in fields)+tail+'\n\n'+source(n))
def existing(kind):
 chunks=re.split(r'(?=^<!-- PAGE )',(C/f'{kind}.md').read_text(encoding='utf-8'),flags=re.M)
 return {re.match(r'<!-- PAGE ([^|]+)',p)[1]:p for p in chunks if p.strip()}
def learner():
 old=existing('ragazzo');new={}
 new['sch8']=sheet(8,'Piano a ritroso per la verifica','Parti dalla data della prova. Scegli azioni concrete e lascia un margine. Il piano può cambiare.',[
 ('Materia, data e richiesta della prova','one'),('Strumenti e condizioni da chiarire con la scuola','two')],
 '''| Quando | Azione e piccolo prodotto | Tempo previsto / modifica |
|---|---|---|
| Prima occasione | &nbsp; | &nbsp; |
| Ripresa | &nbsp; | &nbsp; |
| Prova e correzione | &nbsp; | &nbsp; |
| Preparazione materiali | &nbsp; | &nbsp; |

'''+field('Impegni, margine, aiuto e limite di lavoro concordato','three')+field('Che cosa è successo? Che cosa cambio nel prossimo piano?','three'))
 new['sch9']=sheet(9,'Un errore, un’informazione','Scegli un solo errore. Se non sai perché è successo, puoi scrivere «da capire». Non è un giudizio su di te.',[
 'Compito e punto da guardare','Che cosa chiede la consegna? Che cosa ho fatto?','Ipotesi da verificare: comprensione, scelta, calcolo, scrittura, controllo o altro','Una correzione e il motivo','Una nuova prova simile: risultato e aiuti','Un controllo utile per la prossima volta'])
 new['sch12']=sheet(12,'Parlare di me a scuola','Scegli una richiesta concreta. Puoi farti accompagnare o chiedere a un adulto di parlare con te. Non devi raccontare tutto.',[
 'A chi, quando e con quale adulto di supporto, se serve','Il fatto o la situazione che voglio spiegare','L’aiuto o il chiarimento che chiedo','Le mie parole: provo una frase breve','Che cosa tengo privato / che cosa condivido','Se la risposta non aiuta: a chi mi rivolgo e quale seguito concordiamo'])
 pages13=[
 ('a','Come funziona il mio studio','1 di 4 · Puoi aggiornare queste pagine quando cambia qualcosa. Una difficoltà non descrive tutto ciò che sei.',[
 'Situazioni di studio che voglio descrivere','Che cosa mi riesce: un esempio concreto','Che cosa mi costa fatica: situazione e condizioni','Che cosa so delle mie difficoltà e che cosa voglio capire meglio','Un cambiamento che ho osservato e una cosa ancora incerta']),
 ('b','Le mie risorse nelle situazioni','2 di 4 · Scegli poche strategie e strumenti davvero utili. Non occorre ricordare tutto il manuale.',[
 'Per cominciare e organizzarmi, mi aiuta…','Per capire e ricordare, mi aiuta…','Per rispondere, scrivere o risolvere, mi aiuta…','Uno strumento: quando serve e come controllo che funzioni','Un esempio in cui ho riusato una strategia / una situazione ancora da provare']),
 ('c','Ostacoli, aiuti e parole mie','3 di 4 · Puoi tenere private alcune risposte e preparare una versione più breve da condividere.',[
 'Quando mi blocco: che cosa succede, senza giudicarmi','Una risposta possibile: gesto, pausa o aiuto','Chi può aiutarmi e per quale bisogno','Una richiesta che voglio saper fare','Che cosa scelgo di condividere, con chi e in quale modo']),
 ('d','Il mio piano per proseguire','4 di 4 · Mantenere non significa riuscire sempre da soli. Scegli risorse e aiuti sostenibili.',[
 'Due o tre risorse che voglio conservare','Una prossima occasione di riuso: quando, dove e con quali aiuti','Come mi accorgo che serve rivedere il piano','Prima risposta possibile e persona a cui chiedere aiuto','Richiamo concordato, se previsto / quando chiedere aiuto prima','Che cosa abbiamo rivisto oggi e data del prossimo controllo, se utile'])]
 for suffix,title,intro,fields in pages13:new['sch13'+suffix]=sheet(13,title,intro,fields,ident='sch13'+suffix,run=f'Scheda 13 · {intro[:6]}')
 for suffix,title,intro,fields in [
 ('a','Il mio studio, un passo alla volta','Pagina 1 di 2 · Un adulto può leggere e scrivere con te.', ['Una cosa che so fare: un esempio','Una cosa difficile e un aiuto utile','Per cominciare posso…','Per capire o ricordare mi aiuta…']),
 ('b','Quando mi serve una mano','Pagina 2 di 2 · Possiamo cambiare il piano insieme.', ['Se mi blocco posso…','A chi chiedo aiuto e che cosa dico','La prossima piccola prova e chi mi aiuta','Che cosa voglio raccontare agli altri'])]:
  new['sch13-semplice-'+suffix]=page('sch13-semplice-'+suffix,'Scheda 13 · Versione concreta · '+('1' if suffix=='a' else '2')+' di 2','13. '+title,head()+'<div class="simple">\n\n'+intro+'\n\n'+''.join(field(f) for f in fields)+'\n</div>\n\n'+source(13))
 new['sch18']=sheet(18,'Diario dell’Esploratore','Una piccola prova sul metodo. Manteniamo gli aiuti necessari e cambiamo un elemento alla volta.',[
 'La domanda e che cosa prevedo','La modifica che provo, su quale compito e quando','Strumenti che restano e chi mi aiuta; quando mi fermo','Che cosa osservo: risultato, aiuti e fatica','Che cosa è successo davvero? Che cosa potrebbe aver influito?','Tengo, cambio o riprovo? Prossimo passo concordato'])
 card='''<div class="road-card">
<h2>ROAD · Una scelta possibile</h2>
<p><strong>R · Respira</strong> naturalmente, se ti va. In alternativa rallenta un gesto e guarda un oggetto.</p>
<p><strong>O · Osserva</strong> una cosa qui e ora: situazione, sensazione o pensiero.</p>
<p><strong>A · Ascolta</strong> ciò che conta per te nel prossimo passo.</p>
<p><strong>D · Decidi</strong> un gesto, un aiuto, una pausa o uno stop utile.</p>
<p>Non devi diventare calmo né completare ogni passo. Puoi non usare la carta.</p>
</div>
'''
 new['sch20']=sheet(20,'ROAD: una carta da personalizzare','Puoi ritagliare il riquadro lungo il bordo tratteggiato o usarlo sul foglio. Prima provalo con il clinico. La carta non è automaticamente ammessa nelle prove scolastiche.',[],card+field('Le parole che voglio usare io','three')+field('Una situazione e il passo che potrei scegliere','three')+field('Dopo la prova: tengo, cambio o non uso questa traccia?','two'))
 new['sch21']=sheet(21,'Il mio piano DNA-V della settimana','Scegli un obiettivo che abbia senso per te. Un piano può essere modificato; non è una promessa da rispettare a ogni costo.',[
 'Che cosa conta per me in questa situazione','Il piccolo passo: che cosa, quando e dove','Materiali, strumenti e aiuti che servono','Un ostacolo: se succede… allora posso…','Una possibilità alternativa / quando chiedere aiuto o fermarmi','Dopo: che cosa è accaduto e che cosa cambio?'])
 new['sch22']=sheet(22,'Amico di me stesso dopo un errore','Puoi scegliere un episodio piccolo o inventato. Non devi scrivere parole offensive né sentirti subito meglio.',[
 'Il fatto, descritto senza un giudizio su di me','Che cosa mi servirebbe adesso','Una frase rispettosa e credibile, oppure lascio vuoto','Un gesto: correggere, chiedere aiuto, fare una pausa o altro','Dopo la prova: che cosa aiuta e che cosa no'],tail='Non serve raccontare tutto. Se emerge un bisogno importante, ne parliamo con l’adulto o il professionista che può aiutare.')
 # Original concentric circles: no interpretation or numerical distances implied.
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 260" role="img" aria-label="Tre cerchi vuoti per persone e aiuti"><g fill="none" stroke="#333" stroke-width="1.5"><ellipse cx="300" cy="130" rx="275" ry="120"/><ellipse cx="300" cy="130" rx="180" ry="82"/><ellipse cx="300" cy="130" rx="80" ry="39"/></g><text x="300" y="135" text-anchor="middle" font-family="Heros" font-size="16">IO</text></svg>'
 new['sch23']=sheet(23,'Le persone intorno al mio studio','Puoi scrivere persone o ruoli nei cerchi, oppure usare un elenco. Scegli tu che cosa significa la vicinanza. Non è un test delle relazioni.',[],svg+field('Chi può aiutarmi e per quale bisogno','two')+field('Una richiesta e un adulto sicuro con cui prepararla','two')+field('Che cosa tengo privato / che cosa scelgo di condividere','two'))
 items={k:v for k,v in old.items() if k.startswith('sch')};items.update(new)
 def key(i):
  n=int(re.match(r'sch(\d+)',i)[1]);return (n,1 if 'semplice' in i else 0,i)
 guide=old['guida'].replace('Allegato cumulativo dei blocchi B–C: Schede 1–7, 10–11, 14–17 e 19. Le Schede 1, 2, 3, 4, 14 e 16','Allegato cumulativo dei blocchi B–D: tutte le Schede 1–23. Le Schede 1, 2, 3, 4, 13, 14 e 16').replace('La numerazione segue il catalogo completo: i salti sono intenzionali.','La numerazione conserva i codici del catalogo approvato.').replace('Le altre pagine sono autonome;','La Scheda 13 ha quattro pagine ordinarie e due concrete. Le altre pagine sono autonome;')
 return guide+old['indice']+''.join(items[k] for k in sorted(items,key=key))
def clinician():
 old=existing('clinico');guide=old['guida'].replace('La valutazione conclusiva del percorso sarà sviluppata in una fase successiva.','Lo Strumento 7 raccoglie il profilo finale e gli accordi. L’approfondimento della valutazione e del raccordo con gli adulti resta previsto nel blocco E.')
 body='Codice __________________ Data __________ Professionista __________________\n\nConfronta compiti e condizioni; scrivi «non osservato» quando manca un dato. Nessun punteggio totale.\n\n'
 body+=field('Obiettivi iniziali / rivisti e fonti della linea di base','two')
 body+='''| Filo | Prova attuale, fonte e limite | Raggiunto / parziale / non osservato |
|---|---|---|
| Metodo | &nbsp; | &nbsp; |
| DNA-V | &nbsp; | &nbsp; |
| Consapevolezza | &nbsp; | &nbsp; |

'''+field('Compiti comparabili? Differenze di contenuto, supporti, aiuti e contesto','three')+field('Correttezza, controllo, tempo e costo: che cosa cambia, che cosa resta incerto','three')
 a=page('str7a','Strumento 7 · Profilo finale · 1 di 2','7. Profilo finale e limiti del confronto',body)
 body='Codice __________________ Data __________ Collegamento alla prima pagina __________\n\n'
 body+=field('Restituzione al ragazzo: parole concordate, punti di accordo e disaccordo','three')+field('Risorse da mantenere e aiuti umani ancora necessari','three')+field('Obiettivi non raggiunti: revisione, prosecuzione limitata, invio o altro seguito','three')+field('Condivisione: destinatari, contenuti pertinenti, autorizzazioni e limiti','two')+field('Piano: chi fa che cosa, quando; richiamo se previsto e criteri per anticiparlo','three')+field('Canali / contatti verificati e responsabilità del raccordo','two')
 body+='<div class="source">Strumento informale originale. Non sostituisce valutazione clinica, gestione del rischio, certificazione o PDP. Per bisogni urgenti non attendere il richiamo programmato.</div>'
 b=page('str7b','Strumento 7 · Restituzione · 2 di 2','7. Accordi per proseguire',body)
 return guide+''.join(v for k,v in old.items() if k!='guida')+a+b
if __name__=='__main__':
 (R/'ragazzo.md').write_text(learner(),encoding='utf-8');(R/'clinico.md').write_text(clinician(),encoding='utf-8')
