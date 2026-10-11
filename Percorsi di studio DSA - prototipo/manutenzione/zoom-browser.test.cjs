const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto'),{pathToFileURL}=require('url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=path.join(__dirname,'verifiche'),source=path.resolve(__dirname,'../Cinque percorsi guidati.html');
const routes=[['Affronta un compito','Italiano','Poesia','Fare la parafrasi'],['Affronta un compito','Matematica','Algebra','Risolvere un’equazione'],['Affronta un compito','In tutte le materie','Lezione in classe','Prendere appunti a due colonne'],['Costruisci una mappa','Mappa concettuale','Italiano','La favola'],['Costruisci una mappa','Mappa mentale','Italiano','La favola']];
(async()=>{
 const data=[];let baseline;
 for(const factor of [1,2]){
  const profile=fs.mkdtempSync(path.join(out,'profilo-zoom-'+factor+'-'));fs.mkdirSync(path.join(profile,'Default'));
  fs.writeFileSync(path.join(profile,'Default/Preferences'),JSON.stringify({partition:{default_zoom_level:{x:Math.log(factor)/Math.log(1.2)}}}));
  const context=await chromium.launchPersistentContext(profile,{executablePath:process.env.BROWSER_EXE||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true,viewport:null,offline:true,args:['--window-size=1366,900','--force-device-scale-factor=1']});
  const page=await context.newPage();await page.goto(pathToFileURL(source).href);
  const metrics=await page.evaluate(()=>({width:innerWidth,height:innerHeight,dpr:devicePixelRatio,zoom:getComputedStyle(document.documentElement).zoom}));
  console.log('zoom browser',factor,JSON.stringify(metrics));
  if(factor===1)baseline=metrics;else {assert.ok(Math.abs(metrics.dpr/baseline.dpr-2)<.02,'Lo zoom nativo deve raddoppiare DPR');assert.ok(Math.abs(metrics.width/baseline.width-.5)<.02,'Il viewport CSS deve dimezzarsi');assert.equal(metrics.zoom,'1','Non deve essere uno zoom CSS');}
  let steps=0;
  if(factor===2) for(const route of routes){
   await page.goto(pathToFileURL(source).href);for(const name of route)await page.getByRole('button',{name,exact:true}).click();
   const total=Number(await page.locator('.slide').getAttribute('data-total'));
   for(let i=0;i<total;i++){
    assert.ok(await page.evaluate(()=>{const r=document.querySelector('.navigation').getBoundingClientRect();return r.bottom<=innerHeight+1&&r.top>=0&&r.right<=innerWidth+1}),'Navigazione sempre visibile al 200%');
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Nessun overflow orizzontale');
    if(i===Math.floor(total/2))await page.screenshot({path:path.join(out,'zoom-nativo-'+routes.indexOf(route)+'.png')});
    steps++;if(i<total-1)await page.getByRole('button',{name:'Avanti',exact:true}).click();
   }
  }
  data.push({factor,metrics,steps,profile});await context.close();
 }
 fs.writeFileSync(path.join(out,'zoom-browser-risultati.json'),JSON.stringify({status:'PASS',sha256:crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex'),data},null,2));console.log('PASS zoom nativo 200% su tutti i percorsi');
})().catch(e=>{console.error(e);process.exit(1)});
