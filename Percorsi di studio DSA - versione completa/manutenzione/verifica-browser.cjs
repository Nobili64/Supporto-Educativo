// Percorre nel browser i percorsi presenti nel file HTML, senza connessione.
// Uso: node verifica-browser.cjs            → tutti i percorsi
//      node verifica-browser.cjs M01-01 ... → solo quelli indicati
// Variabili: PLAYWRIGHT_MODULE (modulo playwright), BROWSER_EXE (eseguibile Chrome, Edge o Chromium).
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),source=path.join(root,'Metodo di studio DSA.html');
assert.ok(fs.existsSync(source),'Manca il file HTML: eseguire prima node costruisci.mjs');
const out=path.join(__dirname,'verifiche');fs.mkdirSync(out,{recursive:true});
const isolated=fs.mkdtempSync(path.join(require('node:os').tmpdir(),'percorsi-'));const file=path.join(isolated,'Metodo di studio DSA.html');fs.copyFileSync(source,file);
const html=fs.readFileSync(file,'utf8');const data=JSON.parse(html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1].replace(/\\u003c/g,'<'));
const wanted=process.argv.slice(2);const courses=data.courses.filter(c=>!wanted.length||wanted.includes(c.id));
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.BROWSER_EXE||undefined,headless:true});
 const problems=[],report=[];
 for(const [label,viewport] of [['largo',{width:1366,height:900}],['stretto',{width:390,height:844}]]){
  const context=await browser.newContext({offline:true,viewport}),page=await context.newPage();
  const errors=[],requests=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  const click=name=>page.getByRole('button',{name,exact:true}).click();
  for(const c of courses){
   const fail=m=>problems.push(`${label} ${c.id}: ${m}`);
   try{
    await page.goto(pathToFileURL(file).href);await click('Cerca un percorso');await page.fill('#cerca',c.id);
    const hit=page.locator('#risultati button',{hasText:c.title});if(await hit.count()<1){fail('non trovato con la ricerca per codice');continue;}
    await hit.first().click();
    const total=Number(await page.locator('.slide').getAttribute('data-total'));if(total!==c.slides.length)fail(`schermate ${total} invece di ${c.slides.length}`);
    for(let i=0;i<total;i++){
     const title=await page.locator('h1').innerText();if(title.trim()!==c.slides[i].title.trim())fail(`schermata ${i+1}: titolo inatteso «${title}»`);
     if(label==='largo'){await click('Mi serve una spiegazione');await click('Torna al passaggio');if(await page.locator('h1').innerText()!==title)fail(`schermata ${i+1}: il ritorno dall’aiuto non riporta al passaggio`);}
     const geo=await page.evaluate(()=>{const m=document.querySelector('main');const over=m.scrollWidth>m.clientWidth+2;const svgs=[...document.querySelectorAll('svg[data-map]')].filter(s=>s.getBoundingClientRect().width>0);let overlap=null;for(const s of svgs){const r=[...s.querySelectorAll('g[data-node] rect')].map(x=>x.getBoundingClientRect());for(let a=0;a<r.length;a++)for(let b=a+1;b<r.length;b++){const A=r[a],B=r[b];if(A.left<B.right-1&&B.left<A.right-1&&A.top<B.bottom-1&&B.top<A.bottom-1)overlap=[a,b];}const vb=s.viewBox.baseVal,scale=vb&&vb.width?s.getBoundingClientRect().width/vb.width:1,fonts=[...s.querySelectorAll('g[data-node] text')].map(t=>Number(t.getAttribute('font-size'))*scale);if(fonts.length&&Math.min(...fonts)<14)overlap=overlap||['testo troppo piccolo',Math.min(...fonts).toFixed(1)+' px'];}return {over,overlap};});
     if(geo.over)fail(`schermata ${i+1}: il contenuto esce dai bordi in orizzontale`);
     if(geo.overlap)fail(`schermata ${i+1}: mappa con riquadri sovrapposti o testo troppo piccolo (${geo.overlap})`);
     if(i<total-1){await click('Avanti');}
    }
    if(label==='largo'){
     await click('Menu');await click('Guida per il professionista');if(!(await page.locator('main').innerText()).includes('Osservare il procedimento'))fail('guida per il professionista incompleta');await click('Torna al percorso');
     await click('Menu');await click('Schede da stampare');const pages=await page.locator('.print-page').count();if(pages!==3)fail(`schede di stampa: ${pages} pagine invece di 3`);await click('Torna al percorso');
    }
    await click('Concludi');if(!(await page.locator('h1').innerText()).includes('Da che cosa vuoi partire'))fail('«Concludi» non riporta alla scelta iniziale');
    report.push({id:c.id,vista:label,schermate:total});
   }catch(x){fail('interruzione: '+x.message.split('\n')[0]);}
  }
  if(errors.length)problems.push(`${label}: errori JavaScript: ${[...new Set(errors)].join(' | ')}`);
  if(requests.length)problems.push(`${label}: richieste di rete durante l’uso: ${requests.length}`);
  await context.close();
 }
 // Scelta guidata: ogni lavoro deve essere raggiungibile da materia → ambito → lavoro.
 const page=await browser.newPage({viewport:{width:1366,height:900}});
 for(const c of courses){
  await page.goto(pathToFileURL(file).href);const click=name=>page.getByRole('button',{name,exact:true}).first().click();
  try{
   if(c.kind==='task'){await click('Affronta un compito');await click(c.subject);if(await page.locator('h1').innerText()==='Scegli l’ambito')await click(c.area);}
   else{await click('Costruisci una mappa');await click(c.mapType);await click(c.subject);}
   await page.locator(`button[data-action="open"][data-value="${c.id}"]`).click();if(await page.locator('.slide').count()!==1)problems.push(`${c.id}: non si apre dalla scelta guidata`);
  }catch(x){problems.push(`${c.id}: non raggiungibile dalla scelta guidata (${x.message.split('\n')[0]})`);}
 }
 await browser.close();fs.rmSync(isolated,{recursive:true,force:true});
 const esito={stato:problems.length?'NON SUPERATO':'SUPERATO',browser:browser.version?.()||'',percorsi:courses.length,schermate:courses.reduce((n,c)=>n+c.slides.length,0),problemi:problems};
 fs.writeFileSync(path.join(out,'esito-browser.json'),JSON.stringify(esito,null,1));
 console.log(`${esito.stato}: ${esito.percorsi} percorsi, ${esito.schermate} schermate, viste larga e stretta, senza connessione.`);for(const p of problems)console.log(' - '+p);
 process.exitCode=problems.length?1:0;
})();
