const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=path.join(__dirname,'verifiche'),file=path.resolve(__dirname,'../Cinque percorsi guidati.html');
(async()=>{
 const b=await chromium.launch({executablePath:process.env.BROWSER_EXE||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const c=await b.newContext({offline:true,viewport:{width:1366,height:900}}),p=await c.newPage();
 const click=async n=>p.getByRole('button',{name:n,exact:true}).click();
 await p.goto(pathToFileURL(file).href);await p.screenshot({path:path.join(out,'inizio.png')});
 for(const type of ['Mappa concettuale','Mappa mentale']){
  await p.goto(pathToFileURL(file).href);for(const n of ['Costruisci una mappa',type,'Italiano','La favola'])await click(n);
  while(!['Leggiamo la mappa completa','Usiamo la mappa completa'].includes(await p.locator('h1').innerText()))await click('Avanti');
  const name=type==='Mappa concettuale'?'concettuale':'mentale';
  await p.screenshot({path:path.join(out,name+'-completa.png')});
  await p.setViewportSize({width:360,height:800});await p.locator('svg:visible').screenshot({path:path.join(out,name+'-mobile-grafico.png')});
  await p.setViewportSize({width:1366,height:900});
 }
 await p.goto(pathToFileURL(file).href);for(const n of ['Affronta un compito','In tutte le materie','Lezione in classe','Prendere appunti a due colonne'])await click(n);
 while((await p.locator('h1').innerText())!=='Dopo, costruisci una domanda')await click('Avanti');
 await p.screenshot({path:path.join(out,'appunti-domanda.png')});
 await click('Menu');await click('Guida per il professionista');await p.pdf({path:path.join(out,'Guida-professionista-appunti.pdf'),format:'A4',printBackground:false});
 await b.close();console.log('Immagini dei modelli completi e guida stampata prodotte.');
})().catch(e=>{console.error(e);process.exit(1)});
