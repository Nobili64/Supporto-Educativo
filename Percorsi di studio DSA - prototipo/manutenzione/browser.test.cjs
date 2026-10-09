const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),crypto=require('node:crypto');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..'),source=path.join(root,'Cinque percorsi guidati.html');
assert.ok(fs.existsSync(source),'Manca il prototipo autonomo da aprire offline');
const out=path.join(__dirname,'verifiche'),isolated=path.join(out,'isolato');fs.mkdirSync(isolated,{recursive:true});
const file=path.join(isolated,'Cinque percorsi guidati.html');fs.copyFileSync(source,file);
const routes=[
 {id:'M02-02',choices:['Affronta un compito','Italiano','Poesia','Fare la parafrasi']},
 {id:'M08-08',choices:['Affronta un compito','Matematica','Algebra','Risolvere un’equazione']},
 {id:'M21-04',choices:['Affronta un compito','In tutte le materie','Lezione in classe','Prendere appunti a due colonne']},
 {id:'MC-01',choices:['Costruisci una mappa','Mappa concettuale','Italiano','La favola']},
 {id:'MM-01',choices:['Costruisci una mappa','Mappa mentale','Italiano','La favola']}
];
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.BROWSER_EXE||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const context=await browser.newContext({offline:true,viewport:{width:1366,height:900}}),page=await context.newPage();
 const errors=[],requests=[],log=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
 async function click(name){await page.getByRole('button',{name,exact:true}).click()}
 async function open(route){await page.goto(pathToFileURL(file).href);for(const name of route.choices)await click(name)}
 for(const route of routes){
  await open(route);assert.equal(await page.locator('.slide').count(),1);const total=Number(await page.locator('.slide').getAttribute('data-total'));
  assert.ok(total>8,'Un percorso deve contenere spiegazione, prova e controllo');
  let mapCounts=[];
  for(let index=0;index<total;index++){
   assert.equal(Number(await page.locator('.slide').getAttribute('data-index')),index);
   const title=await page.locator('h1').innerText();assert.ok(title.length>0);
   if(index>0){await click('Indietro');await click('Avanti');assert.equal(await page.locator('h1').innerText(),title)}
   await click('Mi serve una spiegazione');assert.equal(await page.locator('.slide').count(),0);await click('Torna al passaggio');assert.equal(await page.locator('h1').innerText(),title);
   assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Mi serve una spiegazione');
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow desktop');
   assert.ok(await page.evaluate(()=>document.querySelector('main').getBoundingClientRect().bottom<=document.querySelector('.navigation').getBoundingClientRect().top+1),'La navigazione non deve sovrapporsi alla zona di lettura');
   const visual=page.locator('svg[data-map]:visible');if(await visual.count())mapCounts.push(await visual.locator('[data-node]').count());
   log.push({course:route.id,index,title});
   if(index===4)await page.screenshot({path:path.join(out,route.id+'-desktop.png'),fullPage:true});
   if(index<total-1)await click('Avanti');
  }
  assert.ok(await page.getByRole('button',{name:'Concludi',exact:true}).isEnabled(),'L’ultimo passaggio deve permettere di concludere');
  await click('Menu');await click('Guida per il professionista');assert.ok((await page.locator('main').innerText()).includes('Osservare'));
  await click('Torna al percorso');assert.equal(Number(await page.locator('.slide').getAttribute('data-index')),total-1);
  await click('Menu');await click('Schede da stampare');assert.equal(await page.locator('.print-page').count(),3);
  await page.pdf({path:path.join(out,route.id+'.pdf'),format:'A4',printBackground:false,preferCSSPageSize:true});
  await click('Torna al percorso');assert.equal(Number(await page.locator('.slide').getAttribute('data-index')),total-1);
  if(route.id.startsWith('M')&&route.id.includes('-01'))assert.ok(new Set(mapCounts).size>=3,'La mappa deve costruirsi progressivamente');
  await page.setViewportSize({width:360,height:800});
  for(let index=total-1;index>=0;index--){assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Overflow mobile '+route.id+' '+index);if(index===4)await page.screenshot({path:path.join(out,route.id+'-mobile.png'),fullPage:true});if(index>0)await click('Indietro')}
  await page.setViewportSize({width:1366,height:900});
 }
 await open(routes[1]);await page.keyboard.press('Tab');assert.ok(await page.evaluate(()=>document.activeElement.tagName==='BUTTON'||document.activeElement.tagName==='A'));
 await click('Menu');await click('Testo più grande');await click('Torna al percorso');assert.ok(await page.locator('main').evaluate(e=>parseFloat(getComputedStyle(e).fontSize)>=23));
 await page.screenshot({path:path.join(out,'testo-ingrandito.png')});
 await page.reload();assert.equal(await page.locator('.slide').count(),0);assert.equal(await page.evaluate(()=>localStorage.length),0);
 assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
 fs.writeFileSync(path.join(out,'risultati.json'),JSON.stringify({status:'PASS',browser:browser.version(),offline:true,sha256:crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex'),slides:log,errors,requests},null,2));
 console.log('PASS: '+log.length+' schermate, cinque percorsi, aiuti e ritorni, guide, stampa, mobile, testo ingrandito, offline.');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
