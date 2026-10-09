const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const source=path.resolve(__dirname,'../Metodo di studio DSA.html');
assert.ok(fs.existsSync(source),'La guida HTML deve esistere per la prova completa offline');
const out=path.join(__dirname,'verifiche'); fs.mkdirSync(out,{recursive:true});
const isolated=path.join(out,'copia-isolata');fs.mkdirSync(isolated,{recursive:true});
const copy=path.join(isolated,'Metodo di studio DSA.html');fs.copyFileSync(source,copy);
const inventory=JSON.parse(fs.readFileSync(path.join(__dirname,'inventario.json'),'utf8'));
const maps=JSON.parse(fs.readFileSync(path.join(__dirname,'mappe.json'),'utf8'));
const executable=process.env.BROWSER_EXE||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const label=process.env.BROWSER_LABEL||'edge';
(async()=>{
 const browser=await chromium.launch({executablePath:executable,headless:true});
 const context=await browser.newContext({offline:true,viewport:{width:1366,height:900}});
 const page=await context.newPage();const errors=[],requests=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
 await page.goto(pathToFileURL(copy).href);await page.getByRole('button',{name:'Affronta un compito',exact:true}).click();
 await page.locator('[data-action=subject][data-value=italiano]').click();
 await page.locator('[data-action=area][data-value=Poesia]').click();
 await page.locator('[data-action=method][data-value=M02-02]').click();
 assert.ok((await page.locator('main').innerText()).includes('M02-02'));
 await page.getByRole('button',{name:'Avanti',exact:true}).click();
 assert.ok((await page.locator('main').innerText()).includes('Tecniche utili'));
 await page.locator('[data-action=subject][data-value=italiano]').click();
 assert.ok(!(await page.locator('main').innerText()).includes('M02-02'));
 async function code(id){if(!await page.locator('#lookup').evaluate(e=>e.open))await page.locator('#lookup summary').click();await page.locator('#code').fill(id);await page.getByRole('button',{name:'Apri percorso',exact:true}).click();}
 await code(' inesistente ');assert.ok((await page.locator('#lookup-status').innerText()).length>0);
 for(const item of inventory){await code(item.id.toLowerCase());assert.ok((await page.locator('main').innerText()).includes(item.title),item.id);for(let i=1;i<7;i++)await page.getByRole('button',{name:'Avanti',exact:true}).click();assert.ok((await page.locator('main').innerText()).includes('Riprendilo a casa'));}
 for(const m of maps){await code(m.id);await page.getByRole('button',{name:'Costruzione passo passo',exact:true}).click();for(let i=1;i<6;i++)await page.getByRole('button',{name:'Passaggio successivo',exact:true}).click();await page.getByRole('button',{name:'Mappa completa',exact:true}).click();assert.equal(await page.locator('[data-map-node]').count(),9);await page.locator('[data-map-node="n3"]').click();assert.ok((await page.locator('#map-instruction').innerText()).length>20);}
 await code('M02-02');await page.locator('#supports summary').click();await page.locator('#supports input[type=checkbox]').first().check();
 await page.getByRole('button',{name:'Prepara scheda per casa',exact:true}).click();
 assert.ok((await page.locator('#print-sheet').innerText()).includes('M02-02'));
 await page.pdf({path:path.join(out,`${label}-scheda.pdf`),format:'A4',printBackground:false});
 await page.getByRole('button',{name:'Chiudi anteprima',exact:true}).click();
 await page.reload();assert.ok((await page.locator('main').innerText()).includes('Affronta un compito'));assert.equal(await page.locator('input[type=checkbox]:checked').count(),0);
 await page.keyboard.press('Tab');assert.ok(await page.evaluate(()=>document.activeElement!==document.body));
 await page.screenshot({path:path.join(out,`${label}-home.png`),fullPage:true});
 await page.setViewportSize({width:375,height:812});await code('M08-08');
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow schermo stretto');
 await page.screenshot({path:path.join(out,`${label}-stretto.png`),fullPage:true});
 await page.setViewportSize({width:683,height:450});await code(maps[0].id);
 assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'overflow viewport equivalente zoom');
 await page.screenshot({path:path.join(out,`${label}-mappa-stretta.png`),fullPage:true});
 await page.setViewportSize({width:1366,height:900});await page.getByRole('button',{name:'Prepara esempio di mappa',exact:true}).click();
 await page.pdf({path:path.join(out,`${label}-mappa.pdf`),format:'A4',printBackground:false});
 await page.getByRole('button',{name:'Chiudi anteprima',exact:true}).click();
 await page.getByRole('button',{name:'Prepara traccia da completare',exact:true}).click();
 await page.pdf({path:path.join(out,`${label}-traccia.pdf`),format:'A4',printBackground:false});
 assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);
 fs.writeFileSync(path.join(out,`${label}-risultati.json`),JSON.stringify({browser:label,version:browser.version(),executable,offline:true,isolatedCopy:copy,methods:inventory.length,maps:maps.length,errors,requests,status:'PASS',sha256:require('crypto').createHash('sha256').update(fs.readFileSync(copy)).digest('hex')},null,2));
 console.log(`${label}: PASS ${inventory.length} metodi, ${maps.length} mappe, percorso completo, ritorno, reset, stampa, tastiera, viewport`);await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

