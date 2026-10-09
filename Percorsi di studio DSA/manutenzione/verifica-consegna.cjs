const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto');
const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,n),'utf8').replace(/^\uFEFF/,''));
const file=path.resolve(__dirname,'../Metodo di studio DSA.html'),bytes=fs.readFileSync(file),html=bytes.toString('utf8'),hash=crypto.createHash('sha256').update(bytes).digest('hex');
const embedded=JSON.parse(html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
assert.deepEqual(embedded,{inventory:read('inventario.json'),methods:['a','b','c','d'].flatMap(k=>read(`guide-${k}.json`)),maps:read('mappe.json'),sources:read('fonti.json')});
for(const m of embedded.methods){for(const t of m.techniques)for(const k of ['name','how','why'])assert.ok(t[k]?.trim(),`${m.id} tecnica ${k}`);for(const k of ['wrong','why','fix'])assert.ok(m.error[k]?.trim());for(const x of [...m.checks,...m.home,...m.materials])assert.ok(x.trim());}
const evidence=[];
for(const name of ['edge-risultati','chrome-risultati','edge-qualita','chrome-qualita','tocco-stampa']){const r=read(`verifiche/${name}.json`);assert.equal(r.status,'PASS',name);assert.equal(r.sha256,hash,`Evidenza obsoleta: ${name}`);if(r.errors)assert.deepEqual(r.errors,[]);if(r.requests)assert.deepEqual(r.requests,[]);evidence.push(name);}
const pdf=read('verifiche/stampa-risultati.json');assert.equal(pdf.sha256,hash);assert.deepEqual(pdf.bounds,[]);assert.deepEqual(pdf.blank_pages,[]);assert.deepEqual(pdf.sizes,[]);assert.equal(pdf.pdf,78);
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'verifiche/copia-isolata/Metodo di studio DSA.html'))).digest('hex'),hash);
const result={status:'PASS',verifiedAt:new Date().toISOString(),file,bytes:bytes.length,sha256:hash,methods:embedded.methods.length,maps:embedded.maps.length,evidence,pdf:pdf.pdf,pages:pdf.pages,limits:'Controlli tecnici ed editoriali; nessuna validazione clinica o dell’efficacia con studenti.'};
fs.writeFileSync(path.join(__dirname,'verifiche/consegna.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
