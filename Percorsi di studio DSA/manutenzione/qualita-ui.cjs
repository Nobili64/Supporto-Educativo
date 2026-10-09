const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto');
const {chromium}=require('C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const label=process.env.BROWSER_LABEL||'edge',exe=process.env.BROWSER_EXE||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const out=path.join(__dirname,'verifiche'),source=path.resolve(__dirname,'../Metodo di studio DSA.html'),copy=path.join(out,'copia-isolata','Metodo di studio DSA.html');fs.copyFileSync(source,copy);
const inventory=JSON.parse(fs.readFileSync(path.join(__dirname,'inventario.json'))),maps=JSON.parse(fs.readFileSync(path.join(__dirname,'mappe.json')));
const data=JSON.parse(fs.readFileSync(source,'utf8').match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const report={browser:label,sha256:crypto.createHash('sha256').update(fs.readFileSync(source)).digest('hex'),errors:[],requests:[],bounds:[],zooms:[],printProducts:0,reachable:0};
async function code(page,id){await page.locator('#lookup').evaluate(e=>e.open=true);await page.locator('#code').fill(id);await page.locator('#lookup-form').press('Enter');}
async function overflow(page){return page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);}
function track(p){p.on('pageerror',e=>report.errors.push(e.message));p.on('request',r=>{if(/^https?:/.test(r.url()))report.requests.push(r.url());});}
(async()=>{
 const browser=await chromium.launch({executablePath:exe,headless:true}),c=await browser.newContext({offline:true,viewport:{width:1366,height:900}}),p=await c.newPage();track(p);await p.goto(require('url').pathToFileURL(copy).href);report.version=browser.version();
 // Tutte le voci sono effettivamente offerte nei livelli materia/ambito.
 for(const subject of [...new Set(inventory.map(i=>i.subject))]){
  await p.locator('[data-action=home]').first().click();await p.locator('[data-action=tasks]').click();await p.locator(`[data-action=subject][data-value="${subject}"]`).click();
  for(const area of [...new Set(inventory.filter(i=>i.subject===subject).map(i=>i.area))]){
   await p.locator('[data-action=area]').filter({hasText:area}).first().click();
   const ids=await p.locator('[data-action=method]').evaluateAll(es=>es.map(e=>e.dataset.value));assert.deepEqual(ids.sort(),inventory.filter(i=>i.subject===subject&&i.area===area).map(i=>i.id).sort());report.reachable+=ids.length;
   await p.locator(`[data-action=subject][data-value="${subject}"]`).click();
  }
 }
 // Fogli per casa di ogni metodo: ID, aiuti scelti, testo disponibile e assenza di overflow.
 let longest={id:null,len:0};
 for(const m of data.methods){await code(p,m.id);await p.locator('#supports').evaluate(e=>e.open=true);await p.locator('[data-support]').first().check();await p.locator('[data-action=print-method]').click();const t=await p.locator('#print-sheet').innerText();assert.ok(t.includes(m.id)&&t.includes(m.adaptations[0].aid));assert.equal(await overflow(p),false);report.printProducts++;if(t.length>longest.len)longest={id:m.id,len:t.length};await p.locator('[data-action=close-print]').click();}
 await code(p,longest.id);await p.locator('[data-action=print-method]').click();await p.pdf({path:path.join(out,`${label}-scheda-lunga.pdf`),format:'A4',printBackground:false});await p.locator('[data-action=close-print]').click();report.longestMethod=longest;
 for(const m of maps){
  await code(p,m.id);
  const bounds=await p.locator('main .map-visual').evaluate(svg=>{const issues=[];const contains=(r,b)=>b.x>=r.x-1&&b.y>=r.y-1&&b.x+b.width<=r.x+r.width+1&&b.y+b.height<=r.y+r.height+1;for(const n of svg.querySelectorAll('.map-node')){const r=n.querySelector('rect').getBBox();for(const t of n.querySelectorAll('text'))if(!contains(r,t.getBBox()))issues.push({node:n.dataset.mapNode,text:t.textContent,reason:'testo oltre il nodo'});}for(const ed of svg.querySelectorAll('.map-edge')){const t=ed.querySelector('text'),r=ed.querySelector('rect');if(t&&r&&!contains(r.getBBox(),t.getBBox()))issues.push({text:t.textContent,reason:'testo oltre il fondo del legame'});}return issues;});report.bounds.push(...bounds.map(x=>({map:m.id,...x})));
  await p.locator('[data-action=map-step][data-value="2"]').click();const selected=await p.locator('main .map-node.selected').evaluateAll(es=>es.map(e=>e.dataset.mapNode));assert.deepEqual(selected,m.instructions[2].nodes);
  await p.locator('[data-map-node=n7]').focus();await p.keyboard.press('Enter');assert.ok((await p.locator('#map-instruction').innerText()).includes(m.instructions[4].title));
  await p.locator('[data-action=map-full]').click();await p.locator('main .map-visual').screenshot({path:path.join(out,`${label}-${m.id}.png`)});
  for(const action of ['print-map','print-scaffold']){await p.locator(`[data-action=${action}]`).click();assert.equal(await p.locator('#print-sheet .map-node').count(),9);assert.ok((await p.locator('#print-sheet').innerText()).includes(m.id));report.printProducts++;if(label==='edge')await p.pdf({path:path.join(out,`${m.id}-${action}.pdf`),format:'A4',printBackground:false});await p.locator('[data-action=close-print]').click();}
 }
 // Tastiera: percorso completo attraverso Tab/Invio senza click del mouse.
 await p.reload();async function tabTo(sel){for(let i=0;i<100;i++){if(await p.evaluate(s=>document.activeElement.matches(s),sel))return;await p.keyboard.press('Tab');}throw Error('Tastiera non raggiunge '+sel);}
 for(const sel of ['[data-action=tasks]','[data-action=subject][data-value=italiano]','[data-action=area][data-value=Poesia]','[data-action=method][data-value=M02-02]','[data-action=next]']){await tabTo(sel);const focus=await p.evaluate(()=>({style:getComputedStyle(document.activeElement).outlineStyle,width:getComputedStyle(document.activeElement).outlineWidth}));assert.equal(focus.style,'solid');assert.equal(focus.width,'3px');await p.keyboard.press('Enter');}assert.ok((await p.locator('main').innerText()).includes('Tecniche utili'));report.keyboard='PASS percorso completo e focus visibile';
 // Cambio metodo elimina selezioni e stampa residua; filtro categorie senza automatismi.
 await code(p,'M02-02');await p.locator('#supports').evaluate(e=>e.open=true);await p.locator('[data-support]').first().check();await code(p,'M21-10');await p.locator('#supports').evaluate(e=>e.open=true);assert.equal(await p.locator('[data-support]:checked').count(),0);await p.locator('#coach').evaluate(e=>e.open=true);await p.locator('[data-action=category][data-value=dislessia]').click();assert.ok((await p.locator('#coach-adaptations').innerText()).includes('dislessia'));report.aidReset='PASS';
 // Contrasti dei colori effettivamente usati per testo e focus, con sfondi di progetto.
 const colors=await p.evaluate(()=>{const s=getComputedStyle(document.documentElement);return Object.fromEntries(['ink','muted','green','paper','tint','focus'].map(k=>[k,s.getPropertyValue('--'+k).trim()]));});
 const lum=h=>{const a=h.replace('#','').match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return a[0]*.2126+a[1]*.7152+a[2]*.0722;};const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};report.contrast=[['testo',colors.ink,colors.paper],['secondario',colors.muted,'#ffffff'],['pulsante','#ffffff',colors.green],['collegamento','#105d58','#ffffff'],['focus',colors.focus,colors.paper],['etichette mappa','#304e43','#ffffff'],['numeri mappa','#52675e','#f4f6f2']].map(([name,a,b])=>({name,ratio:ratio(a,b)}));for(const x of report.contrast)assert.ok(x.ratio>=(x.name==='focus'?3:4.5),x.name);
 await browser.close();
 // Zoom del browser reale: profili effimeri con preferenza Chromium, non CSS zoom.
 for(const zoom of [1,2]){const dir=fs.mkdtempSync(path.join(out,`${label}-zoom-${zoom}-`));fs.mkdirSync(path.join(dir,'Default'));fs.writeFileSync(path.join(dir,'Default','Preferences'),JSON.stringify({partition:{default_zoom_level:{x:Math.log(zoom)/Math.log(1.2)}}}));const z=await chromium.launchPersistentContext(dir,{executablePath:exe,headless:true,viewport:null,offline:true,args:['--window-size=1366,900']});const q=z.pages()[0];track(q);await q.goto(require('url').pathToFileURL(copy).href);const metric=await q.evaluate(()=>({width:innerWidth,dpr:devicePixelRatio,outer:outerWidth}));assert.equal(metric.dpr,zoom);assert.equal(await overflow(q),false);for(const id of ['M21-04','MC-05','MM-17']){await code(q,id);assert.equal(await overflow(q),false);if(id.startsWith('M2')){for(let i=0;i<6;i++)await q.locator('[data-action=next]').click();}else assert.ok(await q.locator('.map-outline-auto').isVisible()=== (zoom===2));}await q.screenshot({path:path.join(out,`${label}-zoom-${zoom*100}.png`),fullPage:true});report.zooms.push({zoom,...metric});await z.close();}
 assert.deepEqual(report.errors,[]);assert.deepEqual(report.requests,[]);report.status=report.bounds.length?'FAIL diagram bounds':'PASS';fs.writeFileSync(path.join(out,`${label}-qualita.json`),JSON.stringify(report,null,2));assert.deepEqual(report.bounds,[]);console.log(`${label}: PASS qualità, ${report.printProducts} anteprime, ${report.reachable} voci, zoom 100/200%, tastiera, contrasti`);
})().catch(e=>{fs.writeFileSync(path.join(out,`${label}-qualita-parziale.json`),JSON.stringify(report,null,2));console.error(e);process.exit(1)});

