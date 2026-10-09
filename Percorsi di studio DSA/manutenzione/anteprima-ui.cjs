const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require('C:/Users/megan/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,n),'utf8'));
const methods=['a','b','c','d'].flatMap(x=>read(`guide-${x}.json`));const ids=new Set(methods.map(x=>x.id));
const data={inventory:read('inventario.json').filter(x=>ids.has(x.id)),methods,maps:read('mappe.json'),sources:read('fonti.json')};
const dir=path.join(__dirname,'verifiche');fs.mkdirSync(dir,{recursive:true});
const html=fs.readFileSync(path.join(__dirname,'modello.html'),'utf8').replace('/*STYLE*/',()=>fs.readFileSync(path.join(__dirname,'stile.css'),'utf8')).replace('/*DATA*/',()=>JSON.stringify(data).replace(/</g,'\\u003c')).replace('/*SCRIPT*/',()=>fs.readFileSync(path.join(__dirname,'app.js'),'utf8'));
const file=path.join(dir,'ui-provvisoria.html');fs.writeFileSync(file,html);
(async()=>{const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});const context=await browser.newContext({offline:true,viewport:{width:1366,height:1000}});const page=await context.newPage();page.on('pageerror',e=>console.error(e));await page.goto(pathToFileURL(file).href);await page.screenshot({path:path.join(dir,'prima-home.png'),fullPage:true});
async function code(id){await page.locator('#lookup summary').click();await page.locator('#code').fill(id);await page.getByRole('button',{name:'Apri percorso',exact:true}).click();}
await code('M02-02');await page.screenshot({path:path.join(dir,'prima-guida.png'),fullPage:true});await code('MC-05');await page.screenshot({path:path.join(dir,'prima-mappa.png'),fullPage:true});await page.getByRole('button',{name:'Prepara esempio di mappa',exact:true}).click();await page.pdf({path:path.join(dir,'prima-mappa.pdf'),format:'A4'});console.log('Anteprima tecnica parziale',data.inventory.length);await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
