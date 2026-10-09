// Controlla i file in contenuti/: struttura, leggibilità, parole da evitare, immagini e mappe.
// Uso: node valida.mjs            → tutti i file presenti
//      node valida.mjs M01-01 ... → solo i percorsi indicati
// Esce con errore se trova problemi. Gli "avvisi" non bloccano, ma vanno letti.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const catalog=JSON.parse(fs.readFileSync(path.join(dir,'catalogo.json'),'utf8'));
const sources=JSON.parse(fs.readFileSync(path.join(dir,'fonti.json'),'utf8'));
const known=new Map([...catalog.tasks.map(t=>[t.id,'task']),...catalog.maps.map(m=>[m.id,'map'])]);

export const LIMITI={schermateMin:8,schermateMax:18,paroleSchermata:85,paroleAiuto:45,parolePerFrase:25,gulpeaseMin:60,titolo:60,intro:110};
const FASI={'Preparazione':0,'Controllo della preparazione':0,'Esempio spiegato':1,'Controllo dell’esempio':1,'Prova guidata':2,'Controllo guidato':2,'Compito nuovo':3,'Controllo':3,'Ripresa a casa':4};
const PAROLE_DA_EVITARE=[/conserv/i,/sottintes/i,/pertinent/i,/esplicit/i,/\bqualora\b/i,/suddett/i,/\bovvero\b/i,/\bpertanto\b/i,/\bmediante\b/i,/\bnonché\b/i,/\bladdove\b/i,/\bcodest/i,/\bTODO\b/,/\bXXX\b/,/lorem ipsum/i];

export function gulpease(t){const parole=t.split(/\s+/).filter(Boolean).length,lettere=t.replace(/[^A-Za-zÀ-ÿ]/g,'').length,frasi=Math.max(1,(t.match(/[.?!]/g)||[]).length);return Math.round(89+(300*frasi-10*lettere)/parole);}
const frasi=t=>t.split(/(?<=[.?!:;])\s+/).filter(Boolean);
const parole=t=>t.split(/\s+/).filter(Boolean).length;
const isStr=x=>typeof x==='string'&&x.trim().length>0;
const isStrArr=(x,min,max)=>Array.isArray(x)&&x.length>=min&&x.length<=max&&x.every(isStr);

export function validaPercorso(c,id){
 const err=[],avv=[],E=m=>err.push(m),A=m=>avv.push(m);
 if(c.id!==id)E(`id "${c.id}" diverso dal nome del file`);
 if(!known.has(id))E('codice assente dal catalogo');
 const isMap=known.get(id)==='map';
 if(!isStr(c.title)||c.title.length>LIMITI.titolo)E(`titolo mancante o più lungo di ${LIMITI.titolo} caratteri`);
 if(!isStr(c.intro)||c.intro.length>LIMITI.intro)E(`intro mancante o più lunga di ${LIMITI.intro} caratteri`);
 // Mappe definite nel percorso
 const maps=c.maps||{};
 for(const [k,m] of Object.entries(maps)){
  const q=`mappa "${k}"`;
  if(!['concettuale','mentale'].includes(m.type))E(`${q}: type deve essere "concettuale" o "mentale"`);
  if(!Array.isArray(m.nodes)||m.nodes.length<2||m.nodes.length>13){E(`${q}: servono da 2 a 13 nodi`);continue;}
  const ids=new Set(),kids={};let roots=0;
  for(const n of m.nodes){
   if(!isStr(n.id)||ids.has(n.id))E(`${q}: id di nodo mancante o ripetuto (${n.id})`);ids.add(n.id);
   if(!isStr(n.label)||n.label.length>30)E(`${q}: etichetta mancante o più lunga di 30 caratteri (${n.id})`);
   if(!n.parent)roots++;
   else{kids[n.parent]=(kids[n.parent]||0)+1;if(m.type==='concettuale'&&(!isStr(n.link)||n.link.length>20))E(`${q}: nella mappa concettuale ogni nodo tranne il primo ha "link" (massimo 20 caratteri) (${n.id})`);if(m.type==='mentale'&&n.link)E(`${q}: nella mappa mentale i collegamenti non hanno parole (${n.id})`);}
  }
  if(roots!==1||m.nodes[0].parent)E(`${q}: deve esserci un solo nodo senza "parent", ed è il primo dell’elenco`);
  for(const n of m.nodes)if(n.parent&&!ids.has(n.parent))E(`${q}: "${n.id}" ha un parent inesistente`);
  m.nodes.forEach((n,i)=>{if(n.parent&&m.nodes.findIndex(x=>x.id===n.parent)>i)E(`${q}: "${n.id}" compare prima del suo parent; l’ordine dell’elenco è l’ordine di costruzione`);});
  const root=m.nodes[0]?.id;if((kids[root]||0)>5)E(`${q}: al massimo 5 rami principali`);
  for(const [p,n] of Object.entries(kids))if(p!==root&&n>3)E(`${q}: al massimo 3 dettagli per ramo (${p})`);
  const depth=id=>{let d=0,n=m.nodes.find(x=>x.id===id);while(n&&n.parent&&d<9){d++;n=m.nodes.find(x=>x.id===n.parent);}return d;};
  if(m.nodes.some(n=>depth(n.id)>3))E(`${q}: al massimo 3 livelli sotto il centro`);
  const foglie=m.nodes.filter(n=>!m.nodes.some(x=>x.parent===n.id)).length;if(m.type==='concettuale'&&foglie>6)E(`${q}: al massimo 6 riquadri finali (senza figli) in una mappa concettuale, altrimenti il testo diventa troppo piccolo; ora sono ${foglie}`);
 }
 // Immagini
 function visual(v,where){
  if(v===null||v===undefined)return;
  const q=`${where}: immagine "${v.type}"`;
  switch(v.type){
   case 'quote':if(!isStr(v.label)||!isStr(v.text)||v.text.length>700)E(`${q} vuole label e text (massimo 700 caratteri)`);break;
   case 'math':if(!isStr(v.label)||!isStrArr(v.lines,1,8))E(`${q} vuole label e da 1 a 8 lines`);break;
   case 'list':if(!isStr(v.label)||!isStrArr(v.items,1,7))E(`${q} vuole label e da 1 a 7 items`);break;
   case 'table':if(!isStr(v.label)||!isStrArr(v.columns,2,3)||!Array.isArray(v.rows)||v.rows.length<1||v.rows.length>7||!v.rows.every(r=>Array.isArray(r)&&r.length===v.columns.length&&r.every(x=>typeof x==='string')))E(`${q} vuole label, da 2 a 3 columns (sul telefono di più non si leggono) e da 1 a 7 rows della stessa lunghezza`);break;
   case 'timeline':if(!isStr(v.label)||!Array.isArray(v.events)||v.events.length<2||v.events.length>8||!v.events.every(x=>isStr(x.when)&&isStr(x.what)))E(`${q} vuole label e da 2 a 8 events con when e what`);break;
   case 'notes':if(!Array.isArray(v.questions??[])||!Array.isArray(v.notes??[])||(v.summary&&typeof v.summary!=='string')||(v.focus&&!['notes','questions','summary'].includes(v.focus)))E(`${q}: questions e notes sono elenchi, summary è un testo, focus è notes, questions o summary`);break;
   case 'map':{const m=maps[v.map];if(!m){E(`${q}: la mappa "${v.map}" non è definita in "maps"`);break;}if(v.show!==null&&v.show!==undefined&&!(Number.isInteger(v.show)&&v.show>=1&&v.show<=m.nodes.length))E(`${q}: show va da 1 a ${m.nodes.length} oppure null`);if(v.focus&&!m.nodes.some(n=>n.id===v.focus))E(`${q}: focus "${v.focus}" non è un nodo`);break;}
   default:E(`${where}: tipo di immagine sconosciuto "${v.type}"`);
  }
 }
 function testoRagazzo(t,where,{leggibilita=true}={}){
  for(const r of PAROLE_DA_EVITARE)if(r.test(t))E(`${where}: parola da evitare (${r.source}) → «${t.slice(0,90)}…»`);
  if(!leggibilita)return;
  const g=gulpease(t);if(g<LIMITI.gulpeaseMin)E(`${where}: indice Gulpease ${g}, sotto ${LIMITI.gulpeaseMin} → «${t.slice(0,90)}…»`);
  for(const f of frasi(t)){if(parole(f)>LIMITI.parolePerFrase)E(`${where}: frase di ${parole(f)} parole → «${f.slice(0,90)}…»`);if(/\bnon\b.*\bnon\b/i.test(f))A(`${where}: doppia negazione nella stessa frase → «${f.slice(0,90)}»`);}
 }
 // Schermate
 const s=c.slides;
 if(!Array.isArray(s)||s.length<LIMITI.schermateMin||s.length>LIMITI.schermateMax)E(`servono da ${LIMITI.schermateMin} a ${LIMITI.schermateMax} schermate`);
 else{
  let rank=0;const fasi=s.map(x=>x.phase);
  if(fasi[0]!=='Preparazione')E('la prima schermata ha fase "Preparazione"');
  if(fasi.at(-1)!=='Ripresa a casa')E('l’ultima schermata ha fase "Ripresa a casa"');
  for(const f of ['Esempio spiegato','Prova guidata','Compito nuovo'])if(!fasi.includes(f))E(`manca almeno una schermata "${f}"`);
  if(!fasi.some(f=>f==='Controllo'||f==='Controllo guidato'))E('manca una schermata di controllo');
  s.forEach((x,i)=>{
   const w=`schermata ${i+1}`;
   if(!(x.phase in FASI))E(`${w}: fase sconosciuta "${x.phase}"`);else{if(FASI[x.phase]<rank)E(`${w}: la fase "${x.phase}" torna indietro nella progressione`);rank=Math.max(rank,FASI[x.phase]);}
   if(!isStr(x.title)||x.title.length>LIMITI.titolo)E(`${w}: titolo mancante o più lungo di ${LIMITI.titolo} caratteri`);
   if(!isStrArr(x.text,1,3))E(`${w}: text è un elenco da 1 a 3 paragrafi`);
   if(!isStr(x.action))E(`${w}: manca action (riquadro «Adesso»)`);
   if(!isStr(x.hint))E(`${w}: manca hint (aiuto)`);
   if(!isStrArr(x.text,1,3)||!isStr(x.action)||!isStr(x.hint))return;
   testoRagazzo(x.title,`${w} titolo`,{leggibilita:false});
   testoRagazzo(x.text.join(' '),`${w} testo`);testoRagazzo(x.action,`${w} adesso`);testoRagazzo(x.hint,`${w} aiuto`);
   const n=parole(x.text.join(' ')+' '+x.action);if(n>LIMITI.paroleSchermata)E(`${w}: ${n} parole tra testo e «Adesso» (massimo ${LIMITI.paroleSchermata})`);
   if(parole(x.hint)>LIMITI.paroleAiuto)E(`${w}: aiuto di ${parole(x.hint)} parole (massimo ${LIMITI.paroleAiuto})`);
   if(x.hint.trim()===x.action.trim())E(`${w}: l’aiuto ripete il riquadro «Adesso»`);
   visual(x.visual,w);
  });
  const titoli=s.map(x=>x.title);if(new Set(titoli).size!==titoli.length)A('due schermate hanno lo stesso titolo');
 }
 if(isMap){const usate=s?.some(x=>x.visual?.type==='map');if(!usate)E('un percorso sulle mappe deve mostrare la mappa in costruzione');}
 // Guida per il professionista
 const g=c.coach;
 if(!g||!isStr(g.goal)||!isStr(g.prepare)||!isStr(g.observe))E('coach: servono goal, prepare e observe');
 else{
  if(!Array.isArray(g.adaptations)||g.adaptations.length<1||g.adaptations.length>4||!g.adaptations.every(a=>isStrArr(a,3,3)))E('coach.adaptations: da 1 a 4 elementi, ognuno [titolo, che cosa osservare, che cosa provare e come verificare]');
  if(g.scripts!==undefined&&(!Array.isArray(g.scripts)||!g.scripts.every(x=>isStr(x.title)&&isStr(x.text)&&isStr(x.instruction))))E('coach.scripts: elenco di {title, text, instruction}');
  if(!Array.isArray(g.sources)||!g.sources.length||!g.sources.every(x=>x in sources))E(`coach.sources: elenco di codici tra ${Object.keys(sources).join(', ')}`);
  if(g.checks!==undefined&&!isStr(g.checks))E('coach.checks è un testo');
 }
 // Schede di stampa
 const d=c.print;
 if(!d||!isStr(d.modelTitle)||!isStrArr(d.model,1,7)||!Array.isArray(d.practice)||d.practice.length<1||d.practice.length>3||!d.practice.every(x=>isStrArr(x,2,2))||!isStrArr(d.answers,1,5)||!isStrArr(d.home,3,5))E('print: servono modelTitle, model (1-7), practice (1-3 coppie [titolo, testo]), answers (1-5), home (3-5)');
 else{
  for(const t of [...d.model,...d.practice.flat(),...d.answers,...d.home])testoRagazzo(t,'scheda stampata',{leggibilita:false});
  visual(d.visual,'scheda stampata');
  if(d.blankNotes!==undefined&&typeof d.blankNotes!=='boolean')E('print.blankNotes è true o false');
 }
 return {err,avv};
}

if(process.argv[1]&&fileURLToPath(import.meta.url)===path.resolve(process.argv[1])){
 const cdir=path.join(dir,'contenuti');
 const ids=process.argv.slice(2).length?process.argv.slice(2):fs.readdirSync(cdir).filter(f=>f.endsWith('.json')).map(f=>f.slice(0,-5)).sort();
 let errori=0,avvisi=0;
 for(const id of ids){
  const f=path.join(cdir,id+'.json');
  if(!fs.existsSync(f)){console.log(`✗ ${id}: file mancante`);errori++;continue;}
  let c;try{c=JSON.parse(fs.readFileSync(f,'utf8'));}catch(x){console.log(`✗ ${id}: JSON non valido — ${x.message}`);errori++;continue;}
  const {err,avv}=validaPercorso(c,id);errori+=err.length;avvisi+=avv.length;
  console.log(`${err.length?'✗':'✓'} ${id}${err.length?` — ${err.length} errori`:''}${avv.length?` — ${avv.length} avvisi`:''}`);
  for(const m of err)console.log('   errore: '+m);for(const m of avv)console.log('   avviso: '+m);
 }
 const presenti=fs.readdirSync(cdir).filter(f=>f.endsWith('.json')).length;
 console.log(`\nPercorsi controllati: ${ids.length}. Errori: ${errori}. Avvisi: ${avvisi}. File presenti: ${presenti} su ${known.size}.`);
 process.exitCode=errori?1:0;
}
