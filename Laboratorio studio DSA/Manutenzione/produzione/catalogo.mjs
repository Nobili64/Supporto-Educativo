import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const work=path.dirname(fileURLToPath(import.meta.url));
const root=path.join(work,'..','Laboratorio studio DSA');
const input=JSON.parse(await fs.readFile(path.join(work,'catalogo-input.json'),'utf8'));
const wb=Workbook.create();
function make(name,title,heads,rows,widths){
 const s=wb.worksheets.add(name);s.showGridLines=false;
 const n=rows.length+5,m=heads.length;
 s.getRangeByIndexes(0,0,n,m).format.font={name:'Arial',size:12,color:'#202833'};
 s.getRange('A2').values=[[title]];s.getRange('A2').format.font={name:'Arial',size:18,bold:true,color:'#16384B'};
 s.getRangeByIndexes(1,0,1,m).format.rowHeightPx=38;
 s.getRangeByIndexes(4,0,1,m).values=[heads];s.getRangeByIndexes(5,0,rows.length,m).values=rows;
 const h=s.getRangeByIndexes(4,0,1,m);h.format={fill:'#16384B',font:{name:'Arial',size:12,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center'};h.format.rowHeightPx=48;
 for(let c=0;c<m;c++)s.getRangeByIndexes(0,c,n,1).format.columnWidthPx=widths[c]??280;
 const b=s.getRangeByIndexes(5,0,rows.length,m);b.format.wrapText=true;b.format.verticalAlignment='top';
 for(let i=0;i<rows.length;i++){
  const lines=Math.max(...rows[i].map((v,c)=>Math.ceil(String(v??'').length/Math.max(12,(widths[c]??280)/8))));
  const r=s.getRangeByIndexes(i+5,0,1,m);r.format.rowHeightPx=name==='Bibliografia'?Math.max(85,lines*28+45):Math.max(65,lines*21+20);r.format.fill=i%2?'#F1F5F7':'#FFFFFF';
 }
 const t=s.tables.add(s.getRangeByIndexes(4,0,rows.length+1,m),true,name+'Tabella');t.style='TableStyleLight9';t.showFilterButton=true;
 s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);return s;
}
const rows=input.rows.map(r=>r.map((v,i)=>i===11?new Date(v+'T00:00:00Z'):v));
const resources=make('Risorse','Catalogo delle risorse',input.headings,rows,[230,370,190,280,205,390,210,150,150,530,550,150,125,330,330,330,230,400,340,430,160,160]);
resources.getRange('A3').values=[['Salva e chiudi, poi avvia Aggiorna indice. Solo lo stato pronto entra nella biblioteca.']];
resources.getRange(`L6:L${rows.length+5}`).setNumberFormat('dd/mm/yyyy');
resources.getRange(`V6:V${rows.length+5}`).dataValidation={rule:{type:'list',values:['bozza','da verificare','pronto','ritirato']}};
const cov=make('Copertura','Copertura disciplinare: 47 kit previsti',['Kit','Materia','Nucleo previsto','Stato','Copertura essenziale','Ampliamenti o lacune','Risorse collegate','Numero risorse'],input.coverage,[120,190,360,170,450,450,450,170]);
cov.getRange('A3').values=[['Kit pronti']];cov.getRange('B3').formulas=[['=COUNTIFS(D6:D52,"pronto")']];cov.getRange('C3').values=[['su 47. Stato riferito ai controlli editoriali e tecnici, non all’efficacia individuale.']];
cov.getRange('H6:H52').setNumberFormat('0');
const instructions=[['ID','Unico per risorsa; non riusare un ID ritirato. Kit raggruppa studente, tutor e strumenti.'],['Percorsi','PDF e Sorgente sono percorsi relativi dentro la biblioteca. Percorsi individuali esclusi.'],['Stato','bozza, da verificare, pronto, ritirato. Tutte le righe sono controllate; solo pronto è mostrato.'],['Modifica','Gli ODT/ODG sono le sorgenti correnti. Esporta di nuovo il PDF con lo stesso nome, controllalo, poi aggiorna la revisione.'],['Fonti','Il foglio Bibliografia conserva i riferimenti completi per ID; il campo Fonti delle Risorse vi rimanda. Modifica i riferimenti in Bibliografia. Le guide tutor spiegano fonti e limiti. Distingui ricerca, istituzioni, manuali e adattamenti.'],['Coorti','II-III 2026/27: D.M. 254/2012. I 2026/27: D.M. 221/2025. Verificare il curricolo d’istituto.'],['Copertura','Il foglio registra il perimetro e le lacune. Aggiornalo quando aggiungi risorse; il conteggio pronto si ricalcola.'],['Osservazione','La difficoltà è una descrizione del compito; non è assegnata automaticamente dalla diagnosi.']];
make('Istruzioni','Uso del catalogo',['Campo','Indicazione'],instructions,[180,830]);
const bibliography=make('Bibliografia','Fonti complete delle risorse',['ID','Kit','Riferimenti'],input.bibliography,[230,125,1450]);
bibliography.getRange('A3').values=[['Cerca l’ID della risorsa. Le guide tutor riportano anche natura delle fonti e limiti del materiale.']];
wb.recalculate();
await fs.mkdir(path.join(work,'catalogo-qa'),{recursive:true});
for(const [sheet,range] of [['Risorse','A5:D8'],['Risorse','M5:P8'],['Risorse','Q5:V8'],['Copertura','A2:D9'],['Copertura','E5:H8'],['Istruzioni','A2:B13'],['Bibliografia','A5:C8'],['Risorse',`A${rows.length+4}:F${rows.length+5}`],['Bibliografia',`A${rows.length+4}:C${rows.length+5}`]]){
 const b=await wb.render({sheetName:sheet,range,scale:1.25,format:'png'});await fs.writeFile(path.join(work,'catalogo-qa',sheet+'-'+range.replace(':','-')+'.png'),new Uint8Array(await b.arrayBuffer()));
}
const audit=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:30},maxChars:2000});
await fs.writeFile(path.join(work,'catalogo-qa','error-scan.json'),audit.ndjson);
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(path.join(work,'Catalogo.xlsx'));
const lo='C:\\Program Files\\LibreOffice\\program\\soffice.exe';
const result=spawnSync(lo,[`-env:UserInstallation=${pathToFileURL(path.join(work,'lo-catalogo')).href}`,'--headless','--convert-to','ods','--outdir',root,path.join(work,'Catalogo.xlsx')],{windowsHide:true,timeout:120000,encoding:'utf8'});
if(result.status!==0||result.error)throw Error(result.stderr||String(result.error));
console.log(JSON.stringify({resources:rows.length,kits:input.coverage.length,output:path.join(root,'Catalogo.ods'),conversion:result.stdout}));
