const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const out=path.join(__dirname,'verifiche'),source=path.resolve(__dirname,'../Cinque percorsi guidati.html');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const context=await browser.newContext({viewport:{width:360,height:800},offline:true}),page=await context.newPage(),results=[];
 const click=async name=>page.getByRole('button',{name,exact:true}).click();
 await page.goto(pathToFileURL(source).href);for(const name of ['Affronta un compito','Italiano','Poesia','Fare la parafrasi'])await click(name);
 await click('Mi serve una spiegazione');await click('Torna al passaggio');
 const focus=await page.evaluate(()=>{const a=document.activeElement.getBoundingClientRect(),m=document.querySelector('main').getBoundingClientRect();return {top:a.top,bottom:a.bottom,mainTop:m.top,mainBottom:m.bottom,visible:a.top>=m.top&&a.bottom<=m.bottom}});
 results.push({check:'focus visibile dopo aiuto',...focus});
 await click('Mi serve una spiegazione');await click('Menu');await click('Testo più grande');
 const returnHelp=page.getByRole('button',{name:'Torna alla spiegazione',exact:true});
 results.push({check:'menu conserva la spiegazione',available:await returnHelp.count()===1});
 if(await returnHelp.count()) {await returnHelp.click();assert.equal(await page.locator('.slide').count(),0);await click('Torna al passaggio');}
 fs.writeFileSync(path.join(out,'interazioni-risultati.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results));
 await browser.close();assert.ok(focus.visible&&results[1].available,'Focus o ritorno al contesto da correggere');
})().catch(e=>{console.error(e);process.exit(1)});
