// Verifica su una copia: browser Edge reale, file:// e rete bloccata.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {chromium}=require('playwright');
const BASE=__dirname, QA=path.join(BASE,'qa');
const edge='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const normalize=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const parse=p=>JSON.parse(fs.readFileSync(p,'utf8').match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
async function main(){
 const arg=process.argv.indexOf('--library');if(arg<0)throw Error('Use --library PATH');
 const source=path.resolve(process.argv[arg+1]);fs.mkdirSync(QA,{recursive:true});
 const copy=path.join(QA,'copia-browser-'+crypto.randomUUID().slice(0,8));fs.cpSync(source,copy,{recursive:true});
 const index=path.join(copy,'Indice.html'),data=parse(index), report={source,copy,browser:edge,index_sha256:sha(index),tests:[],network_requests:[],page_errors:[],screenshots:[]};
 const save=()=>fs.writeFileSync(path.join(QA,'browser-report.json'),JSON.stringify(report,null,2));
 const check=(name,passed,evidence={})=>{report.tests.push({name,passed:!!passed,...evidence});save();if(!passed)throw Error(name+' '+JSON.stringify(evidence));};
 const context=await chromium.launchPersistentContext(path.join(QA,'edge-profile-'+crypto.randomUUID().slice(0,8)),{executablePath:edge,headless:true,viewport:{width:1440,height:1000},offline:true,args:['--disable-background-networking','--no-first-run','--no-default-browser-check']});
 try{
  await context.route(/^https?:\/\//,route=>{report.network_requests.push(route.request().url());route.abort();});
  const page=context.pages()[0]||await context.newPage(); page.on('pageerror',e=>report.page_errors.push(String(e)));
  await page.goto(pathToFileURL(index).href);await page.locator('.resource').first().waitFor();
  check('copied_folder_file_protocol_offline',page.url().startsWith('file:')&&await page.evaluate(()=>navigator.onLine)===false,{url:page.url(),onLine:await page.evaluate(()=>navigator.onLine)});
  check('all_resources_and_counter',await page.locator('.resource').count()===data.length,{rendered:await page.locator('.resource').count(),expected:data.length,count:await page.locator('#count').innerText()});
  const fullSubjectCount=new Set(data.map(x=>x.Materia)).size;
  check('subject_filter_options',await page.locator('#subject option').count()===fullSubjectCount+1);
  async function screenshot(name){const p=path.join(QA,name);await page.screenshot({path:p});report.screenshots.push(p);save();}
  await screenshot('indice-desktop.png');
  await page.locator('#search').fill('elettricita');
  const electricity=await page.locator('.resource').count();check('accent_insensitive_search',electricity>0,{count:electricity,titles:await page.locator('.resource h5').allTextContents()});
  await page.locator('#search').fill('ELETTRICITÀ');check('case_and_accent_equivalence',await page.locator('.resource').count()===electricity);
  const firstRecord=data.find(x=>normalize(x.Materia).includes('scienz'))||data[0];
  const distinctive=String(firstRecord.ID);await page.locator('#search').fill(distinctive+' '+firstRecord.Materia);
  check('multiword_AND_search',await page.locator('.resource').count()===1&&await page.locator('.resource h5').innerText()===firstRecord.Titolo,{query:distinctive+' '+firstRecord.Materia});
  await page.locator('#search').fill(distinctive+' inesistentezzzz');check('AND_does_not_return_partial_match',await page.locator('.resource').count()===0&&await page.locator('#empty').isVisible());
  await screenshot('indice-nessun-risultato.png');
  await page.locator('#reset').click();check('reset_clears_search_and_returns_all',await page.locator('#search').inputValue()===''&&await page.locator('.resource').count()===data.length&&await page.locator('#search').evaluate(el=>el===document.activeElement));
  const subject=data.find(x=>x.Materia==='Matematica')?.Materia||data[0].Materia;
  await page.locator('#subject').selectOption(subject);
  check('subject_filter',await page.locator('.resource').count()===data.filter(x=>x.Materia===subject).length,{subject,count:await page.locator('.resource').count()});
  const audience=data.find(x=>x.Materia===subject&&normalize(x.Destinatario).includes('tutor'))?.Destinatario||data.find(x=>x.Materia===subject).Destinatario;
  await page.locator('#audience').selectOption(audience);
  check('audience_filter_combines_with_subject',await page.locator('.resource').count()===data.filter(x=>x.Materia===subject&&x.Destinatario===audience).length,{audience});
  const kind=data.find(x=>x.Materia===subject&&x.Destinatario===audience).Tipo;
  await page.locator('#kind').selectOption(kind);
  check('kind_filter_combines_with_subject_and_audience',await page.locator('.resource').count()===data.filter(x=>x.Materia===subject&&x.Destinatario===audience&&x.Tipo===kind).length,{kind});
  await screenshot('indice-filtri.png');
  await page.locator('#reset').click();check('reset_clears_all_filters',await page.locator('#subject').inputValue()===''&&await page.locator('#audience').inputValue()===''&&await page.locator('#kind').inputValue()===''&&await page.locator('.resource').count()===data.length);
  await page.locator('#search').fill('    ');check('whitespace_query_is_empty',await page.locator('.resource').count()===data.length);await page.locator('#reset').click();
  const urls=await page.locator('a.file-link').evaluateAll(els=>els.map(e=>({href:e.getAttribute('href'),absolute:e.href,text:e.textContent})));
  const broken=urls.filter(x=>!x.absolute.startsWith(pathToFileURL(copy+path.sep).href)||!fs.existsSync(fileURLToPath(x.absolute))||/^[a-z]+:/i.test(x.href));
  check('all_pdf_and_source_links_resolve_inside_copied_library',urls.length===data.length*2&&broken.length===0,{links:urls.length,broken});
  const pdf=await page.locator('a.file-link.pdf').first().getAttribute('href');
  await page.locator('a.file-link.pdf').first().click();
  await page.waitForURL(url=>decodeURIComponent(url.href)===decodeURIComponent(new URL(pdf,pathToFileURL(index)).href));
  check('click_PDF_navigates_to_local_file',page.url().endsWith('.pdf'),{url:page.url()});
  await page.goBack();await page.locator('.resource').first().waitFor();
  const guide=await page.locator('#guide-link').getAttribute('href');
  check('guide_link_is_real_local_PDF',guide.toLowerCase().endsWith('.pdf')&&fs.existsSync(fileURLToPath(new URL(guide,pathToFileURL(index)))),{href:guide});
  const sourceLink=page.locator('a.file-link.source').first();
  const downloaded=page.waitForEvent('download');await sourceLink.click();const download=await downloaded;
  check('source_link_opens_local_document_download',/\.od[gt]$/i.test(download.suggestedFilename()),{filename:download.suggestedFilename()});
  // Browser viewport narrow enough to exercise reflow independently of zoom.
  await page.setViewportSize({width:390,height:844});
  const mobile=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,filters:getComputedStyle(document.querySelector('.filters')).gridTemplateColumns}));
  check('narrow_viewport_no_horizontal_overflow',mobile.scroll<=mobile.width,{...mobile});await screenshot('indice-390px.png');
  await page.locator('.resource').first().scrollIntoViewIfNeeded();await screenshot('indice-390px-risorse.png');
  check('no_runtime_errors_or_network_dependencies',report.page_errors.length===0&&report.network_requests.length===0,{errors:report.page_errors,network:report.network_requests});
 }finally{await context.close();save();}

 // Chromium's saved browser zoom preference applies actual browser zoom to file URLs.
 // The default partition key is "x" (empty relative partition path):
 // https://raw.githubusercontent.com/chromium/chromium/main/chrome/browser/ui/zoom/chrome_zoom_level_prefs.cc
 const zoomProfile=path.join(QA,'edge-zoom-profile-'+crypto.randomUUID().slice(0,8));fs.mkdirSync(path.join(zoomProfile,'Default'),{recursive:true});
 fs.writeFileSync(path.join(zoomProfile,'Default','Preferences'),JSON.stringify({partition:{default_zoom_level:{x:Math.log(2)/Math.log(1.2)}}}));
 const zoomContext=await chromium.launchPersistentContext(zoomProfile,{executablePath:edge,headless:true,viewport:null,offline:true,args:['--window-size=1440,1000','--disable-background-networking','--no-first-run','--no-default-browser-check']});
 try{
  await zoomContext.route(/^https?:\/\//,route=>{report.network_requests.push(route.request().url());route.abort();});
  const page=zoomContext.pages()[0];page.on('pageerror',e=>report.page_errors.push(String(e)));await page.goto(pathToFileURL(index).href);await page.locator('.resource').first().waitFor();
  const zoom=await page.evaluate(()=>({dpr:devicePixelRatio,innerWidth,outerWidth,scrollWidth:document.documentElement.scrollWidth,columns:getComputedStyle(document.querySelector('.results')).gridTemplateColumns}));
  check('actual_browser_zoom_200_percent',Math.abs(zoom.dpr-2)<0.05&&zoom.innerWidth<800,{...zoom});
  check('zoom_200_percent_no_horizontal_overflow',zoom.scrollWidth<=zoom.innerWidth,{...zoom});
  await page.locator('#search').fill('equazioni');check('zoom_200_percent_search_still_usable',await page.locator('.resource').count()>0);
  // The browser's native viewport capture avoids Playwright's CSS clip at non-default browser zoom.
  const zoomSession=await zoomContext.newCDPSession(page);
  async function zoomScreenshot(name){const p=path.join(QA,name),shot=await zoomSession.send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:false});fs.writeFileSync(p,Buffer.from(shot.data,'base64'));report.screenshots.push(p);save();}
  await page.evaluate(()=>scrollTo(0,0));await zoomScreenshot('indice-zoom200.png');
  await page.locator('.resource').first().scrollIntoViewIfNeeded();await zoomScreenshot('indice-zoom200-risorse.png');
  check('zoom_200_percent_resource_links_reachable',await page.locator('a.file-link.pdf').first().isVisible()&&await page.locator('a.file-link.source').first().isVisible());
 }finally{await zoomContext.close();save();}
 const updaterPath=path.join(QA,'updater-report.json');
 if(fs.existsSync(updaterPath)){
  const changed=JSON.parse(fs.readFileSync(updaterPath,'utf8')).changed_browser_copy;
  const browser=await chromium.launch({executablePath:edge,headless:true});
  try{const context=await browser.newContext({offline:true});await context.route(/^https?:\/\//,r=>{report.network_requests.push(r.request().url());r.abort();});const page=await context.newPage();page.on('pageerror',e=>report.page_errors.push(String(e)));
   await page.goto(pathToFileURL(path.join(changed,'Indice.html')).href);await page.locator('#search').fill('QA-NUOVA-RISORSA');
   check('added_catalog_resource_visible_in_browser',await page.locator('.resource').count()===1,{title:await page.locator('.resource h5').innerText()});
   const href=await page.locator('a.file-link.pdf').getAttribute('href');await page.locator('a.file-link.pdf').click();await page.waitForURL(u=>u.href.includes('.pdf'));
   check('unicode_percent_hash_relative_PDF_opens',decodeURIComponent(page.url()).includes('risorsa è # 100%.pdf'),{url:page.url(),href});
   await page.goBack();await page.locator('#search').fill('Verifica elettricita caffe');check('cell_HTML_rendered_as_text',await page.locator('.resource').count()===1&&await page.locator('.resource h5').innerText()==='Verifica elettricità: caffè <script> & "mappe"');
  }finally{await browser.close();}
 }
 check('all_contexts_no_runtime_errors_or_network_dependencies',report.page_errors.length===0&&report.network_requests.length===0,{errors:report.page_errors,network:report.network_requests});
 check('source_index_unchanged',sha(path.join(source,'Indice.html'))===report.index_sha256);
 report.passed=report.tests.every(t=>t.passed);save();console.log(JSON.stringify({passed:report.passed,tests:report.tests.length,report:path.join(QA,'browser-report.json'),screenshots:report.screenshots}));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
