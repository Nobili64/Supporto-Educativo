from pathlib import Path
import json,zipfile,xml.etree.ElementTree as E,hashlib,sys
B=Path(__file__).parent
objectives={
'matematica-studente':'Risolvere equazioni e controllare le soluzioni',
'matematica-tutor':'Guidare i passaggi e correggere gli esercizi',
'storia-studente':'Distinguere cause, sviluppo e conseguenze della guerra',
'storia-tutor':'Guidare mappa ed esposizione; verificare le risposte',
'scienze-studente':'Distinguere le grandezze e applicare la legge di Ohm',
'scienze-tutor':'Guidare l’uso del formulario e verificare i risultati',
'01-lettura-attiva':'Leggere per rispondere a una domanda',
'02-sintesi':'Selezionare informazioni e conservare i legami',
'03-scelta-strumento':'Scegliere un supporto in funzione del compito',
'04-memoria-ripasso':'Organizzare domande, ripassi e controlli delle risposte',
'05-incontri':'Organizzare un incontro da 60 o 90 minuti',
'06-osservazione':'Osservare scelta, uso e adattamento del supporto',
'07-check-in':'Individuare un piccolo adattamento utile sul compito',
'08-confronto-scuola':'Raccogliere le indicazioni scolastiche sui materiali',
'modello-formulario':'Costruire un formulario con condizioni ed esempio',
'modello-argomento':'Progettare un kit con aiuti graduali e controlli',
'guida-uso':'Consultare, modificare e ampliare la biblioteca',
'fonti-verifiche':'Consultare le fonti e le verifiche dei tre kit'
}
data=json.loads((B/'catalog-data.json').read_text(encoding='utf-8'))
for r in data:
    if r['id'] in objectives:r['objective']=objectives[r['id']]
(B/'catalog-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
path=B/'library'/'Catalogo.ods'
with zipfile.ZipFile(path)as z:info=z.infolist();files={i.filename:z.read(i.filename)for i in info}
NS={n:'urn:oasis:names:tc:opendocument:xmlns:'+v+':1.0' for n,v in [('office','office'),('table','table'),('text','text'),('config','config')]}
for n,u in NS.items():E.register_namespace(n,u)
def tag(n,a):return '{'+NS[n]+'}'+a
content=E.fromstring(files['content.xml'])
for row in content.findall('.//table:table-row',NS):
    cells=row.findall('table:table-cell',NS)
    if len(cells)<12:continue
    ident=''.join(cells[0].itertext())
    if ident in objectives:
        cell=cells[5];old=cell.find('text:p',NS);attrs={}if old is None else dict(old.attrib)
        for c in list(cell):cell.remove(c)
        E.SubElement(cell,tag('text','p'),attrs).text=objectives[ident]
files['content.xml']=E.tostring(content,encoding='utf-8',xml_declaration=True)
settings=E.fromstring(files['settings.xml'])
container=settings.find('office:settings',NS)
view=next(x for x in container if x.get(tag('config','name'))=='ooo:view-settings')
existing=view.find('config:config-item-map-indexed',NS)
if existing is not None:view.remove(existing)
views=E.SubElement(view,tag('config','config-item-map-indexed'),{tag('config','name'):'Views'})
entry=E.SubElement(views,tag('config','config-item-map-entry'))
def item(parent,name,type,value):E.SubElement(parent,tag('config','config-item'),{tag('config','name'):name,tag('config','type'):type}).text=str(value)
item(entry,'ViewId','string','view1');item(entry,'ActiveTable','string','Risorse')
tabs=E.SubElement(entry,tag('config','config-item-map-named'),{tag('config','name'):'Tables'})
table=E.SubElement(tabs,tag('config','config-item-map-entry'),{tag('config','name'):'Risorse'})
for name,typ,value in [('CursorPositionX','int',2),('CursorPositionY','int',5),('HorizontalSplitMode','short',2),('VerticalSplitMode','short',2),('HorizontalSplitPosition','int',2),('VerticalSplitPosition','int',5),('ActiveSplitRange','short',2),('PositionLeft','int',0),('PositionRight','int',2),('PositionTop','int',0),('PositionBottom','int',5),('ZoomType','short',0),('ZoomValue','int',100),('PageViewZoomValue','int',60),('ShowGrid','boolean','false')]:item(table,name,typ,value)
files['settings.xml']=E.tostring(settings,encoding='utf-8',xml_declaration=True)
tmp=path.with_suffix('.tmp')
with zipfile.ZipFile(tmp,'w')as z:
    for i in info:z.writestr(i,files[i.filename])
tmp.replace(path)
print(json.dumps({'patched':'Catalogo.ods','objectives':len(objectives),'frozen_columns':2,'frozen_rows':5,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
