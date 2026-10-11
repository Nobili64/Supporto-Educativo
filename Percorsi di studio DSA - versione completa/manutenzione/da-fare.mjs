// Aggiorna da-fare.json togliendo i percorsi che hanno già un file valido in contenuti/.
// Uso: node da-fare.mjs
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validaPercorso} from './valida.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url));
const file=path.join(dir,'da-fare.json'),dati=JSON.parse(fs.readFileSync(file,'utf8'));
const pronto=id=>{const f=path.join(dir,'contenuti',id+'.json');if(!fs.existsSync(f))return false;try{return validaPercorso(JSON.parse(fs.readFileSync(f,'utf8')),id).err.length===0;}catch{return false;}};
dati.gruppi=dati.gruppi.map(g=>({...g,items:g.items.filter(x=>!pronto(x.id))})).filter(g=>g.items.length);
fs.writeFileSync(file,JSON.stringify(dati,null,1));
const n=dati.gruppi.reduce((s,g)=>s+g.items.length,0);
console.log(`Percorsi ancora da scrivere: ${n}`);for(const g of dati.gruppi)console.log(` - ${g.nome}: ${g.items.map(x=>x.id).join(' ')}`);
