const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {chromium}=require('playwright');
const source=path.resolve(process.argv[2]);
const qa=path.join(__dirname,'qa-esteso');fs.mkdirSync(qa,{recursive:true});
const copy=path.join(qa,'biblioteca-'+crypto.randomUUID().slice(0,8));fs.mkdirSync(copy);
const whitelist=['Materie','Metodo di studio','Laboratorio delle mappe','Preparazione all’esame','Modelli riutilizzabili','Guida all’uso','Indice.html','Catalogo.ods'];
for(const name of whitelist)if(fs.existsSync(path.join(source,name)))fs.cpSync(path.join(source,name),path.join(copy,name),{recursive:true});
const index=path.join(copy,'Indice.html');
const data=JSON.parse(fs.readFileSync(index,'utf8').match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const report={source,copy,sha256:crypto.createHash('sha256').update(fs.readFileSync(index)).digest('hex'),tests:[],network:[],errors:[]};
const save=()=>fs.writeFileSync(path.join(qa,'report.json'),JSON.stringify(report,null,2));
function check(name,passed,details={}){report.tests.push({name,passed:!!passed,...details});save();if(!passed)throw Error(name);}
const edge='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
async function run(){
 const browser=await chromium.launch({executablePath:edge,headless:true});
 const ctx=await browser.newContext({offline:true,viewport:{width:1440,height:1000}});
 await ctx.route(/^https?:\/\//,r=>{report.network.push(r.request().url());r.abort();});
 try{
  const p=await ctx.newPage();p.on('pageerror',e=>report.errors.push(String(e)));await p.goto(pathToFileURL(index).href);
  const count=()=>p.locator('.resource').count();
  check('copia file offline',p.url().startsWith('file:')&&!await p.evaluate(()=>navigator.onLine));
  check('conteggio e stato',await count()===data.length&&data.every(r=>r.Stato==='pronto'),{resources:data.length});
  check('percorsi individuali fuori indice e copia',!fs.existsSync(path.join(copy,'Percorsi individuali'))&&!data.some(r=>/Percorsi individuali|\/Casi\//i.test(r.PDF+' '+r.Sorgente)));
  const fields=[['subject','Materia'],['audience','Destinatario'],['kind','Tipo'],['school','Classe'],['topic','Argomento'],['objective','Obiettivo'],['task','Compito'],['tool','Strumento'],['level','Guida']];
  const target=data.find(r=>r.ID==='MAT08-S');if(!target)throw Error('MAT08-S mancante');
  for(const [id,key] of fields){await p.locator('#reset').click();await p.locator('#'+id).selectOption(target[key]);check('filtro '+key,await count()===data.filter(r=>r[key]===target[key]).length);}
  await p.locator('#reset').click();
  for(const [id,key] of fields)await p.locator('#'+id).selectOption(target[key]);
  check('nove filtri combinati',await count()===1&&await p.locator('.resource h5').innerText()===target.Titolo);
  for(let i=0;i<4;i++){await p.locator('.quick').nth(i).click();check('accesso rapido '+i,await count()>0,{count:await count()});}
  await p.locator('#reset').click();await p.locator('#search').fill('MAT08-S statistica');check('ricerca AND per ID e materia',await count()===1);
  await p.locator('#search').fill('MAT08-S inesistentezz');check('nessun falso risultato',await count()===0&&await p.locator('#empty').isVisible());
  await p.locator('#reset').click();
  const links=await p.locator('.resource a.file-link').evaluateAll(a=>a.map(x=>x.href));
  const broken=links.filter(u=>!u.startsWith(pathToFileURL(copy+path.sep).href)||!fs.existsSync(fileURLToPath(u)));
  check('tutti i collegamenti delle risorse locali',links.length===data.length*2&&!broken.length,{links:links.length,broken});
  const utility=await p.locator('a.file-link:not(.resource a), #guide-link').evaluateAll(a=>a.map(x=>x.href));
  check('catalogo e guida locali',utility.length===2&&utility.every(u=>u.startsWith(pathToFileURL(copy+path.sep).href)&&fs.existsSync(fileURLToPath(u))),{links:utility});
  await p.locator('#search').focus();await p.keyboard.press('Tab');check('tastiera ricerca verso materia',await p.locator('#subject').evaluate(el=>el===document.activeElement));
  await p.keyboard.press('Home');await p.keyboard.press('ArrowDown');await p.keyboard.press('Enter');check('selezione materia da tastiera',await p.locator('#subject').inputValue()!=='');
  await p.locator('#reset').focus();await p.keyboard.press('Enter');check('reset da tastiera',await count()===data.length&&await p.locator('#search').evaluate(el=>el===document.activeElement));
  await p.locator('#search').fill('MAT05-S');await p.locator('details summary').first().focus();await p.keyboard.press('Enter');check('dettagli da tastiera',await p.locator('details').first().getAttribute('open')!==null);
  await p.locator('#reset').click();await p.screenshot({path:path.join(qa,'desktop.png')});
  await p.setViewportSize({width:390,height:844});check('nessun overflow stretto',await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));await p.screenshot({path:path.join(qa,'stretto.png')});
  check('assenza rete ed errori',!report.network.length&&!report.errors.length);
 }finally{await browser.close();save();}
 const profile=path.join(qa,'zoom-'+crypto.randomUUID().slice(0,8));fs.mkdirSync(path.join(profile,'Default'),{recursive:true});
 fs.writeFileSync(path.join(profile,'Default','Preferences'),JSON.stringify({partition:{default_zoom_level:{x:Math.log(2)/Math.log(1.2)}}}));
 const zoom=await chromium.launchPersistentContext(profile,{executablePath:edge,headless:true,offline:true,viewport:null,args:['--window-size=1440,1000','--disable-background-networking','--no-first-run']});
 try{
  const p=zoom.pages()[0];await p.goto(pathToFileURL(index).href);
  const metrics=await p.evaluate(()=>({dpr:devicePixelRatio,w:innerWidth,s:document.documentElement.scrollWidth}));
  check('zoom browser 200%',Math.abs(metrics.dpr-2)<.05&&metrics.s<=metrics.w,metrics);
  await p.locator('#search').fill('MAT08-S');check('ricerca a 200%',await p.locator('.resource').count()===1);
  const cdp=await zoom.newCDPSession(p);const shot=await cdp.send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});fs.writeFileSync(path.join(qa,'zoom200.png'),Buffer.from(shot.data,'base64'));
 }finally{await zoom.close();save();}
 report.passed=report.tests.every(t=>t.passed);save();console.log(JSON.stringify({passed:report.passed,tests:report.tests.length,resources:data.length,report:path.join(qa,'report.json')}));
}
run().catch(e=>{save();console.error(e.message);process.exitCode=1;});
