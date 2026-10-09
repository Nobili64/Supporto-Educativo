import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
const dir=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1'));
const base=decodeURIComponent(dir);
const read=n=>JSON.parse(fs.readFileSync(path.join(base,n),'utf8').replace(/^\uFEFF/,''));
const inventory=read('inventario.json');
const required=['goal','materials','techniques','example','steps','transfer','checks','error','home','adaptations','coach','sources'];
const groups=['a','b','c','d']; let methods=[];
for(const g of groups){assert.ok(fs.existsSync(path.join(base,`guide-${g}.json`)),`Mancano le guide ${g}`);methods.push(...read(`guide-${g}.json`));}
assert.equal(new Set(methods.map(x=>x.id)).size,methods.length,'ID duplicati');
assert.deepEqual(methods.map(x=>x.id).sort(),inventory.map(x=>x.id).sort(),'Copertura differente dal repertorio');
const ids=new Set(inventory.map(x=>x.id));
for(const m of methods){
 assert.ok(ids.has(m.id));
 for(const key of required) assert.ok(m[key] && (!Array.isArray(m[key]) || m[key].length),`${m.id}: ${key} mancante`);
 for(const key of ['task','work','result']) assert.ok(m.example[key]?.length,`${m.id} esempio ${key}`);
 for(const key of ['task','check']) assert.ok(m.transfer[key]?.length,`${m.id} prova ${key}`);
 for(const s of m.steps) for(const k of ['title','do','help']) assert.ok(s[k]?.length,`${m.id} passo ${k}`);
 for(const a of m.adaptations){for(const k of ['stage','difficulty','categories','signal','aid','preserve','verify'])assert.ok(a[k]?.length,`${m.id} adattamento ${k}`);for(const c of a.categories)assert.ok(['dislessia','disortografia','disgrafia','discalculia','trasversale'].includes(c));}
 assert.ok(!/\b(TODO|TBD|Lorem ipsum)\b/i.test(JSON.stringify(m)),`${m.id}: segnaposto`);
}
assert.ok(fs.existsSync(path.join(base,'mappe.json')),'Mappe assenti');
const maps=read('mappe.json'); assert.equal(maps.length,34,'Occorrono 34 esempi');
assert.equal(new Set(maps.map(x=>x.id)).size,34);
for(const m of maps){
 assert.equal(m.nodes.length,9,`${m.id}: nodi`); assert.equal(m.edges.length,8);
 const ns=new Set(m.nodes.map(n=>n.id));const seen=new Set(['n0']);
 for(const e of m.edges){assert.ok(ns.has(e.from)&&ns.has(e.to));if(m.type==='concettuale')assert.ok(e.label.length);if(seen.has(e.from))seen.add(e.to);}
 assert.equal(seen.size,9,`${m.id}: connessione`);assert.equal(m.instructions.length,6);
 for(const step of m.instructions) for(const id of step.nodes)assert.ok(ns.has(id));
 for(const k of ['sourceText','question','transfer','error','checks','scaffold'])assert.ok(m[k]?.length,`${m.id}: ${k}`);
}
const html=path.join(base,'..','Metodo di studio DSA.html');assert.ok(fs.existsSync(html),'HTML finale assente');
const h=fs.readFileSync(html,'utf8');assert.ok(!/<(?:script|link|img)[^>]+(?:src|href)=["']https?:/i.test(h),'Dipendenza remota');
assert.ok(!/\b(localStorage|sessionStorage|indexedDB|fetch)\s*[.(]/.test(h),'Persistenza o richiesta remota inattesa');
console.log(JSON.stringify({methods:methods.length,groups:21,maps:maps.length,inventory:'copertura esatta',status:'PASS'},null,2));
