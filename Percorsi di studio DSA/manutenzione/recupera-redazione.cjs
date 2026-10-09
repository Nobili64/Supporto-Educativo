// Recupera soltanto celle editoriali pure dai tre lavori interrotti.
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const source='C:/Users/megan/.codex/sessions/2026/10/08/';
const specs=[['a','01a11adb-6859','records-a'],['c','01a11adb-d89c','c_records']];
(async()=>{for(const [part,session,key] of specs){
 const file=fs.readdirSync(source).find(n=>n.includes(session));
 const cells=fs.readFileSync(path.join(source,file),'utf8').trim().split('\n').map(JSON.parse).filter(r=>r.payload?.type==='custom_tool_call'&&r.payload.name==='exec').map(r=>r.payload.input).filter(s=>typeof s==='string'&&!s.includes('tools.')&&(s.includes('store(')||s.includes('load(')));
 const data=new Map();const sandbox={store:(k,v)=>data.set(k,v),load:k=>data.get(k),text:()=>{}};vm.createContext(sandbox);
 for(const [i,cell]of cells.entries()){await vm.runInContext(`(async()=>{${cell}\n})()`,sandbox,{timeout:10000});fs.writeFileSync(path.join(__dirname,`recupero-${part}-${i}.txt`),cell);}
 const records=data.get(key);if(!Array.isArray(records))throw Error('Nessun record recuperato '+part);
 fs.writeFileSync(path.join(__dirname,`guide-${part}.json`),JSON.stringify(records,null,2));
 console.log(part,records.length,'record recuperati');
}})().catch(e=>{console.error(e);process.exit(1)});
