import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
process.on('uncaughtException',e=>{console.error(e.message);process.exit(1)});
const work=path.dirname(fileURLToPath(import.meta.url));
const out=path.join(work,'..','Laboratorio studio DSA','Percorsi individuali','_MODELLO');
const wb=Workbook.create();
const specs=[
['Incontri',['Data','Compito','Obiettivo','ID risorsa e versione','Correttezza osservata','Aiuti ricevuti','Uso dello strumento','Tempo indicativo (min)','Fatica riferita','Passo successivo','Data di revisione'],[150,300,300,240,320,320,320,190,320,320,170]],
['Piano',['Data prevista','Scadenza scolastica','Compito o domanda di ripasso','Primo passo','Tempo disponibile (min)','Supporti','Esito e variazioni'],[150,180,380,350,210,330,450]],
['Obiettivi',['ID obiettivo','Data di accordo','Compito e azione osservabile','Strumenti e condizioni','Punto di partenza','Criterio di verifica','Data di revisione','Esito e decisione'],[150,170,380,380,350,350,180,400]]];
await fs.mkdir(out,{recursive:true});await fs.mkdir(path.join(work,'registro-qa'),{recursive:true});
for(const [name,heads,widths] of specs){
 const s=wb.worksheets.add(name);s.showGridLines=false;const n=heads.length;
 s.getRangeByIndexes(0,0,17,n).format.font={name:'Arial',size:12,color:'#202833'};
 s.getRange('A2').values=[[name+' - modello individuale']];s.getRange('A2').format.font={name:'Arial',size:18,bold:true,color:'#16384B'};s.getRange('A2').format.rowHeightPx=40;
 s.getRange('A3').values=[['Codice studente:']];s.getRange('B3').values=[['']];s.getRange('B3').format.fill='#FFF2CC';s.getRange('C3').values=[['Salva nella cartella del codice. Le righe sono vuote e si possono aggiungere.']];
 s.getRangeByIndexes(4,0,1,n).values=[heads];
 s.getRangeByIndexes(4,0,1,n).format={fill:'#16384B',font:{name:'Arial',size:12,bold:true,color:'#FFFFFF'},wrapText:true,verticalAlignment:'center'};s.getRangeByIndexes(4,0,1,n).format.rowHeightPx=50;
 s.getRangeByIndexes(5,0,12,n).values=Array.from({length:12},()=>Array(n).fill(null));
 for(let c=0;c<n;c++)s.getRangeByIndexes(0,c,17,1).format.columnWidthPx=widths[c];
 for(let r=5;r<17;r++){const range=s.getRangeByIndexes(r,0,1,n);range.format.rowHeightPx=78;range.format.fill=r%2?'#F1F5F7':'#FFFFFF';range.format.wrapText=true;range.format.verticalAlignment='top';}
 heads.forEach((h,c)=>{if(h.includes('Data')||h.includes('Scadenza'))s.getRangeByIndexes(5,c,12,1).setNumberFormat('dd/mm/yyyy');if(h.includes('(min)'))s.getRangeByIndexes(5,c,12,1).setNumberFormat('0');});
 s.tables.add(s.getRangeByIndexes(4,0,13,n),true,'Tabella'+name).showFilterButton=true;s.freezePanes.freezeRows(5);s.freezePanes.freezeColumns(1);
}
wb.recalculate();
for(const [name,heads] of specs){
 for(let c=0;c<heads.length;c+=4){const r=String.fromCharCode(65+c)+'5:'+String.fromCharCode(65+Math.min(c+3,heads.length-1))+'7';const b=await wb.render({sheetName:name,range:r,scale:1,format:'png'});await fs.writeFile(path.join(work,'registro-qa',name+'-'+c+'.png'),new Uint8Array(await b.arrayBuffer()));}
 if(wb.worksheets.getItem(name).getRangeByIndexes(5,0,12,heads.length).values.flat().some(v=>v!==null&&v!==''&&v!==undefined))throw Error('Dati inattesi nel modello');
}
await fs.writeFile(path.join(work,'registro-qa','inspect.ndjson'),(await wb.inspect({kind:'table',range:'Incontri!A5:K7',include:'values,formulas',tableMaxRows:3,tableMaxCols:11,maxChars:3000})).ndjson);
await (await SpreadsheetFile.exportXlsx(wb)).save(path.join(work,'Registro.xlsx'));
const result=spawnSync('C:\\Program Files\\LibreOffice\\program\\soffice.exe',[`-env:UserInstallation=${pathToFileURL(path.join(work,'lo-catalogo')).href}`,'--headless','--convert-to','ods','--outdir',out,path.join(work,'Registro.xlsx')],{windowsHide:true,timeout:120000,encoding:'utf8'});
if(result.status!==0||result.error)throw Error(result.stderr||String(result.error));console.log(result.stdout);
