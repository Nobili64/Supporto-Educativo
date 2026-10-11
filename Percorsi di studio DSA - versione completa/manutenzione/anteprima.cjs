// Fotografa alcune schermate per un controllo a vista. Uso: node anteprima.cjs [ID ...]
const path=require('node:path'),fs=require('node:fs');const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const file=path.join(__dirname,'..','Metodo di studio DSA.html'),out=path.join(__dirname,'verifiche','anteprima');fs.mkdirSync(out,{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:process.env.BROWSER_EXE||undefined});
 for(const [label,vp] of [['largo',{width:1366,height:900}],['stretto',{width:390,height:844}]]){
  const page=await b.newPage({viewport:vp});const errors=[];page.on('pageerror',x=>errors.push(x.message));
  await page.goto(pathToFileURL(file).href);await page.screenshot({path:path.join(out,`${label}-inizio.png`)});
  const ids=process.argv.slice(2);
  for(const id of ids){
   await page.goto(pathToFileURL(file).href);await page.getByRole('button',{name:'Cerca un percorso',exact:true}).click();await page.fill('#cerca',id);await page.locator('#risultati button').first().click();
   const total=Number(await page.locator('.slide').getAttribute('data-total'));
   for(let i=0;i<total;i++){if(await page.locator('.visual').count()||i===0||i===total-1)await page.screenshot({path:path.join(out,`${label}-${id}-${String(i+1).padStart(2,'0')}.png`),fullPage:false});if(i<total-1)await page.getByRole('button',{name:'Avanti',exact:true}).click();}
  }
  if(errors.length)console.log('ERRORI',label,errors);await page.close();}
 await b.close();console.log('Anteprime in',out);})();
