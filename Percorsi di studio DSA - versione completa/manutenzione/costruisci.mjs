// Costruisce "Metodo di studio DSA.html" da catalogo.json, fonti.json e contenuti/*.json.
// Entrano solo i percorsi che hanno un file di contenuto; gli altri sono elencati come mancanti.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const read=f=>JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
const catalog=read('catalogo.json'),sources=read('fonti.json');
const entries=[...catalog.tasks.map(t=>({...t,kind:'task'})),...catalog.maps.map(m=>({...m,kind:'map',area:m.mapType}))];
const courses=[],missing=[];
for(const entry of entries){
 const file=path.join(dir,'contenuti',entry.id+'.json');
 if(!fs.existsSync(file)){missing.push(entry.id);continue;}
 const content=JSON.parse(fs.readFileSync(file,'utf8'));
 if(content.id!==entry.id)throw new Error(`${file}: id ${content.id} diverso da ${entry.id}`);
 const maps=Object.fromEntries(Object.entries(content.maps||{}).map(([k,v])=>[k,{...v,id:`${entry.id}-${k}`.replace(/[^A-Za-z0-9-]/g,'')}]));
 courses.push({...content,maps,kind:entry.kind,subject:entry.subject,area:entry.area,mapType:entry.mapType,topic:entry.topic,language:entry.language});
}
const payload=JSON.stringify({subjects:catalog.subjects,courses,sources}).replace(/</g,'\\u003c');
const css=fs.readFileSync(path.join(dir,'stile.css'),'utf8'),js=fs.readFileSync(path.join(dir,'app.js'),'utf8');
const html=`<!doctype html>\n<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>Un passo alla volta — metodo di studio</title><style>${css}</style></head><body><a class="skip" href="#main">Vai al contenuto</a><div id="app"></div><noscript>Per aprire i percorsi, abilita JavaScript nel browser. Il file funziona senza Internet.</noscript><script id="data" type="application/json">${payload}</script><script>${js}</script></body></html>`;
fs.writeFileSync(path.join(dir,'..','Metodo di studio DSA.html'),html);
const screens=courses.reduce((n,c)=>n+c.slides.length,0);
console.log(`Creato HTML: ${courses.length} percorsi su ${entries.length}, ${screens} schermate. Mancanti: ${missing.length}.`);
