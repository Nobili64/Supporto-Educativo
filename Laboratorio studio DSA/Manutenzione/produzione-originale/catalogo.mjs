import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

// Authoring and QA stay in this delivery's temporary directory.
const base = path.dirname(fileURLToPath(import.meta.url));
const library = path.join(base, 'library');
const qa = path.join(base, 'catalogo-qa');
const headings = ['ID','Titolo','Materia','Argomento','Classe','Obiettivo','Tipo','Guida','Destinatario','PDF','Sorgente','Revisione'];
const keys = ['id','title','subject','topic','school','objective','kind','level','audience','pdf','source','date'];
const widths = [235,350,190,230,160,440,180,180,160,620,680,145];
const headerRow = 5;

function checkRelative(value, extension, id) {
  if (typeof value !== 'string' || path.win32.isAbsolute(value) || value.includes(':') || value.split(/[\\/]/).some(part => !part || part === '..')) {
    throw new Error(`${id}: percorso relativo non valido: ${value}`);
  }
  if (!extension.includes(path.extname(value).toLowerCase())) throw new Error(`${id}: formato non valido: ${value}`);
}

function lineCount(value, width) {
  const capacity = Math.max(5, Math.floor((width - 18) / 8.6));
  return String(value).split('\n').reduce((sum, paragraph) => {
    let lines = 1, length = 0;
    for (const piece of paragraph.split(/(?<=[ /-])/)) {
      if (length && length + piece.length > capacity) { lines++; length = 0; }
      if (piece.length > capacity) {
        lines += Math.floor((piece.length - 1) / capacity);
        length = (piece.length - 1) % capacity + 1;
      } else length += piece.length;
    }
    return sum + lines;
  }, 0);
}

const records = JSON.parse((await fs.readFile(path.join(base, 'catalog-data.json'), 'utf8')).replace(/^\uFEFF/, ''));
if (!Array.isArray(records) || !records.length) throw new Error('catalog-data.json deve contenere risorse.');
const seen = new Set();
for (const record of records) {
  for (const key of keys) if (typeof record[key] !== 'string' || !record[key].trim()) throw new Error(`${record.id ?? '?'}: campo ${key} mancante.`);
  const normalized = record.id.toLocaleLowerCase('it');
  if (seen.has(normalized)) throw new Error(`ID duplicato: ${record.id}`);
  seen.add(normalized);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(record.date) || new Date(`${record.date}T00:00:00Z`).toISOString().slice(0,10) !== record.date) throw new Error(`${record.id}: data non valida.`);
  checkRelative(record.pdf, ['.pdf'], record.id);
  checkRelative(record.source, ['.odt','.odg'], record.id);
}

await fs.mkdir(qa, {recursive:true});
await fs.mkdir(library, {recursive:true});
const workbook = Workbook.create();
const sheet = workbook.worksheets.add('Risorse');
const lastRow = headerRow + records.length;
const populated = sheet.getRange(`A1:L${lastRow}`);
populated.format.font = {name:'Arial', size:12, color:'#202833'};
populated.format.verticalAlignment = 'center';
sheet.showGridLines = false;
sheet.tabColor = '#16384B';
for (let col = 0; col < widths.length; col++) sheet.getRangeByIndexes(0,col,lastRow,1).format.columnWidthPx = widths[col];
sheet.getRange('A1:L1').format.rowHeightPx = 12;
sheet.getRange('A2').values = [['Catalogo delle risorse']];
sheet.getRange('A2').format.font = {name:'Arial',size:18,bold:true,color:'#16384B'};
sheet.getRange('A2:L2').format.rowHeightPx = 36;
sheet.getRange('A3').values = [['Modifica le righe e salva. Poi avvia Aggiorna indice nella cartella del laboratorio.']];
sheet.getRange('A3').format.font = {name:'Arial',size:12,color:'#52616C'};
sheet.getRange('A3:L3').format.rowHeightPx = 28;
sheet.getRange('A4:L4').format.rowHeightPx = 12;
sheet.getRange(`A${headerRow}:L${headerRow}`).values = [headings];

const rows = records.map(record => keys.map(key => key === 'date' ? new Date(`${record.date}T00:00:00Z`) : record[key]));
sheet.getRange(`A${headerRow+1}:L${lastRow}`).values = rows;
sheet.getRange(`L${headerRow+1}:L${lastRow}`).setNumberFormat('dd/mm/yyyy');
const table = sheet.tables.add(`A${headerRow}:L${lastRow}`, true, 'CatalogoRisorse');
table.style = 'TableStyleLight9';
table.showFilterButton = true;
const header = sheet.getRange(`A${headerRow}:L${headerRow}`);
header.format = {fill:'#16384B',font:{name:'Arial',size:12,bold:true,color:'#FFFFFF'},wrapText:true,horizontalAlignment:'center',verticalAlignment:'center'};
header.format.rowHeightPx = 42;
header.format.borders = {insideVertical:{style:'thin',color:'#FFFFFF'}};
sheet.getRange(`A${headerRow+1}:L${lastRow}`).format.wrapText = true;
sheet.getRange(`A${headerRow+1}:K${lastRow}`).format.horizontalAlignment = 'left';
sheet.getRange(`A${headerRow+1}:K${lastRow}`).format.verticalAlignment = 'top';
sheet.getRange(`L${headerRow+1}:L${lastRow}`).format.horizontalAlignment = 'center';
for (let i=0;i<records.length;i++) {
  const rowNumber = headerRow + 1 + i;
  const rowRange = sheet.getRange(`A${rowNumber}:L${rowNumber}`);
  const height = Math.max(66, ...keys.slice(0,-1).map((key,col) => lineCount(records[i][key], widths[col])*21+18));
  rowRange.format.rowHeightPx = height;
  rowRange.format.fill = i%2 ? '#F1F5F7' : '#FFFFFF';
  rowRange.format.borders = {bottom:{style:'thin',color:'#D4DEE4'}};
}
sheet.freezePanes.freezeRows(headerRow);
sheet.freezePanes.freezeColumns(2);

workbook.recalculate();
const logs = [];
for (const range of [`A${headerRow}:L${Math.min(lastRow,headerRow+3)}`,`A${Math.max(headerRow+1,lastRow-2)}:L${lastRow}`]) {
  const result = await workbook.inspect({kind:'table',sheetId:'Risorse',range,include:'values,formulas',tableMaxRows:5,tableMaxCols:12,tableMaxCellChars:250,maxChars:15000});
  logs.push(result.ndjson);
}
const errors = await workbook.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:30},summary:'Controllo errori catalogo'});
logs.push(errors.ndjson);
const actual = sheet.getRange(`A${headerRow+1}:K${lastRow}`).values;
for (let i=0;i<records.length;i++) for (let col=0;col<11;col++) {
  if (actual[i][col] !== records[i][keys[col]]) throw new Error(`Differenza dati ${records[i].id}, ${keys[col]}.`);
}
await fs.writeFile(path.join(qa,'inspect.ndjson'),logs.join('\n'),'utf8');

// Bounded crops preserve readable text at scale 2 and cover every column.
const crops = [['A','C'],['D','F'],['G','I'],['J','J'],['K','L']];
const intervals = [[2,Math.min(lastRow,headerRow+5)],[Math.max(headerRow+1,lastRow-4),lastRow]];
for (let section=0;section<intervals.length;section++) {
  const [top,bottom] = intervals[section];
  for (const [left,right] of crops) {
    const range = `${left}${top}:${right}${bottom}`;
    const preview = await workbook.render({sheetName:'Risorse',range,scale:2,format:'png'});
    await fs.writeFile(path.join(qa,`crop2-${section+1}-${left}-${right}.png`),new Uint8Array(await preview.arrayBuffer()));
  }
}
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
const intermediate = path.join(qa,'Catalogo.xlsx');
await xlsx.save(intermediate);

const soffice = 'C:\\Program Files\\LibreOffice\\program\\soffice.exe';
const profile = pathToFileURL(path.join(base,'lo-catalogo-profile')).href;
const converted = spawnSync(soffice,[`-env:UserInstallation=${profile}`,'--headless','--convert-to','ods','--outdir',library,intermediate],{encoding:'utf8',timeout:120000,windowsHide:true});
await fs.writeFile(path.join(qa,'libreoffice-conversion.txt'),`${converted.stdout??''}\n${converted.stderr??''}`,'utf8');
if (converted.error) throw converted.error;
if (converted.status !== 0) throw new Error(`LibreOffice: codice ${converted.status}. ${converted.stderr}`);
const output = path.join(library,'Catalogo.ods');
const python = 'C:\\Users\\megan\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe';
const patched = spawnSync(python,['-X','utf8',path.join(base,'patch_catalogo.py')],{encoding:'utf8',timeout:30000,windowsHide:true});
if (patched.status !== 0) throw new Error(`Riquadri ODS: ${patched.stderr || patched.stdout}`);
const stat = await fs.stat(output);
if (stat.size < 1000) throw new Error('Catalogo.ods vuoto o incompleto.');
const nativeAudit = String.raw`
import json, pathlib, sys, zipfile, xml.etree.ElementTree as E
base=pathlib.Path(sys.argv[1]); source=json.loads((base/'catalog-data.json').read_text(encoding='utf-8-sig'))
keys=['id','title','subject','topic','school','objective','kind','level','audience','pdf','source','date']
heads=['ID','Titolo','Materia','Argomento','Classe','Obiettivo','Tipo','Guida','Destinatario','PDF','Sorgente','Revisione']
ns={'table':'urn:oasis:names:tc:opendocument:xmlns:table:1.0','office':'urn:oasis:names:tc:opendocument:xmlns:office:1.0','text':'urn:oasis:names:tc:opendocument:xmlns:text:1.0','config':'urn:oasis:names:tc:opendocument:xmlns:config:1.0'}
def key(n,a):return '{'+ns[n]+'}'+a
def text(c):
 if c.get(key('office','value-type'))=='date':return c.get(key('office','date-value'))[:10]
 return '\n'.join(''.join(p.itertext()) for p in c.findall('text:p',ns))
with zipfile.ZipFile(base/'library'/'Catalogo.ods') as z:
 root=E.fromstring(z.read('content.xml')); settings=E.fromstring(z.read('settings.xml'))
 sheet=root.find('.//table:table',ns); assert sheet.get(key('table','name'))=='Risorse'
 found=False; values=[]; dates=0
 for row in sheet.findall('.//table:table-row',ns):
  cells=[]
  for c in row:
   if c.tag not in [key('table','table-cell'),key('table','covered-table-cell')]:continue
   repeat=int(c.get(key('table','number-columns-repeated'),'1'))
   cells.extend([text(c)]*min(repeat,max(0,12-len(cells))))
   if c.get(key('office','value-type'))=='date':dates+=1
  if cells and cells[0]=='ID':assert cells==heads;found=True;continue
  if found and any(cells):values.append(cells)
 assert values==[[r[k] for k in keys] for r in source], 'Confronto ODS con JSON fallito'
 assert dates==len(source), 'Date native mancanti'
 filters=root.findall('.//table:database-range',ns)
 assert len(filters)==1 and filters[0].get(key('table','display-filter-buttons'))=='true','Filtri mancanti'
 items={e.get(key('config','name')):e.text for e in settings.findall('.//config:config-item',ns)}
 pane={k:items.get(k) for k in ['HorizontalSplitMode','VerticalSplitMode','HorizontalSplitPosition','VerticalSplitPosition','ShowGrid']}
 assert pane['HorizontalSplitPosition']=='2' and pane['VerticalSplitPosition']=='5',str(pane)
 report={'rows':len(values),'cellsCompared':len(values)*12,'typedDates':dates,'nativeFilter':True,'panes':pane,'formulaCells':len(root.findall('.//*[@table:formula]',ns))}
 (base/'catalogo-qa'/'native-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report))
`;
const audited = spawnSync(python,['-c',nativeAudit,base],{encoding:'utf8',timeout:30000,windowsHide:true});
if (audited.error) throw audited.error;
if (audited.status !== 0) throw new Error(`Verifica ODS: ${audited.stderr || audited.stdout}`);
await fs.writeFile(path.join(qa,'catalogo-report.json'),JSON.stringify({rows:records.length,columns:headings,sourceRecordsValidated:true,textCellsCompared:records.length*11,dateFormat:'dd/mm/yyyy',dateValues:'Date UTC',source:path.join(base,'catalog-data.json'),output,bytes:stat.size,renderedRanges:intervals.flatMap(([top,bottom])=>crops.map(([left,right])=>`${left}${top}:${right}${bottom}`)),nativeConversionExitCode:converted.status,nativeAudit:JSON.parse(audited.stdout)},null,2),'utf8');
console.log(JSON.stringify({output,records:records.length,previews:intervals.length*crops.length,bytes:stat.size,nativeAudit:'passed'}));
