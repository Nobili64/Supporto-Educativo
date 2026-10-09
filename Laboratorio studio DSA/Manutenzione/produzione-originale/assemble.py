from pathlib import Path
import json,shutil
B=Path(__file__).parent;O=B/'library';M=O/'Manutenzione';M.mkdir(exist_ok=True)
for file in ['index-template.html','aggiorna-indice.ps1']:shutil.copy2(B/file,M/file)
shutil.copy2(B/'Aggiorna indice.cmd',O/'Aggiorna indice.cmd')
for name in ['matematica','scienze']:
    d=json.loads((B/(name+'.json')).read_text(encoding='utf-8-sig'))
    folder=O/'Materie'/d['subject']/d['topic']/'Tutor'
    (folder/'verifiche-wolfram.json').write_text(json.dumps(d['checks'],ensure_ascii=False,indent=2),encoding='utf-8')
    (folder/'Leggi verifiche Wolfram.txt').write_text('VERIFICHE WOLFRAM - '+d['topic']+'\nData: 28 settembre 2026\n\nRegistro completo delle query e delle risposte effettive. I collegamenti alla documentazione del linguaggio non sono collegamenti a risultati persistenti. Le query possono essere ripetute online; la biblioteca funziona offline.\n\n'+json.dumps(d['checks'],ensure_ascii=False,indent=2),encoding='utf-8-sig')
(O/'LEGGIMI.txt').write_text('LABORATORIO STUDIO DSA\n\nPer iniziare apri Indice.html.\n\nTre kit: Equazioni di primo grado, Prima guerra mondiale, Elettricità.\nSchede studente, guide e soluzioni tutor, mappe modificabili e modelli.\n\nApri i PDF per mostrare e stampare. Le sorgenti si modificano con LibreOffice.\nDopo una modifica alla sorgente, esporta nuovamente il PDF con lo stesso nome.\n\nPer aggiungere materiali: aggiorna Catalogo.ods, salva e chiudi, poi avvia Aggiorna indice.cmd.\nLa guida completa è accessibile dall’indice.\n\nCopia tutta la cartella per trasferire la biblioteca. I collegamenti interni sono relativi.\nLa consultazione funziona senza rete. Le fonti esterne richiedono connessione.\n\nLa stampa fisica e l’efficacia con gli studenti restano da verificare negli incontri.\n',encoding='utf-8-sig')
print('Biblioteca assemblata')
