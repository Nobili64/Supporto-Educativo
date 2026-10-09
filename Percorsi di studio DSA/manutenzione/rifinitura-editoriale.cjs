// Correzioni editoriali motivate dalla revisione finale; esecuzione idempotente.
const fs=require('fs'),path=require('path');const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,n),'utf8'));const save=(n,d)=>fs.writeFileSync(path.join(__dirname,n),JSON.stringify(d,null,2)+'\n');
const maps=read('mappe.json');
for(const m of maps){
 if(['MC-05','MM-05'].includes(m.id)){const old=m.nodes.find(n=>n.id==='n4').label;const label='volume proprio e forma variabile';m.nodes.find(n=>n.id==='n4').label=label;for(const s of m.instructions)s.text=s.text.replaceAll(old,label);}
 m.transferCheck=m.transferCheck.replace('semiminima/minima indicano 1/2 pulsazioni rispettivamente','semiminima e minima indicano rispettivamente 1 e 2 pulsazioni');
 if(m.id==='MC-15'){for(const ed of m.edges)if(ed.label==='sono associate all’')ed.label='sono legate alla tradizione dell’';}
}
// La spaziatura prima di un apostrofo finale si risolve nella lettura, mantenendo i nodi separati.
for(const m of maps.filter(m=>m.type==='concettuale'))for(let branch=1;branch<=4;branch++){
 const root=m.nodes[0],a=m.nodes.find(n=>n.id===`n${branch*2-1}`),b=m.nodes.find(n=>n.id===`n${branch*2}`),ea=m.edges[(branch-1)*2],eb=m.edges[(branch-1)*2+1];
 const phrase=(x,r,y)=>`${x} ${r} ${y}`.replace(/’ /g,'’');
 m.instructions[branch].text=`Aggiungi «${a.label}» e «${b.label}». Collega con «${ea.label}» e «${eb.label}». Leggi: «${phrase(root.label,ea.label,a.label)}»; «${phrase(a.label,eb.label,b.label)}». Confronta queste frasi con il testo.`;
}
save('mappe.json',maps);
const guides=read('guide-d.json'),g=guides.find(x=>x.id==='M21-10');g.adaptations[0].signal='Osserva se, coperti gli appunti, il ragazzo fatica a formulare la domanda o ad avviare la spiegazione. Distingui l’accesso al testo dalla comprensione e dal recupero; questa osservazione non identifica da sola un DSA.';g.adaptations[0].verify='Su due domande simili, confronta chiarezza e correttezza della spiegazione con il supporto scelto; verifica che il ragazzo controlli e corregga la propria risposta. Considera anche lo sforzo riferito.';g.home=['Scegli un piccolo gruppo di appunti già controllati e ricavane due o tre domande.','Prova a rispondere prima di rileggere, confronta e correggi. Riprendi una domanda e un esempio variato in un altro giorno, mantenendo gli strumenti utili.','Se non riesci a formulare le domande o il contenuto degli appunti è dubbio, mostra il punto a chi ti accompagna e concorda il prossimo aiuto.'];save('guide-d.json',guides);
console.log('Rifiniture mappe e M21-10 salvate.');
