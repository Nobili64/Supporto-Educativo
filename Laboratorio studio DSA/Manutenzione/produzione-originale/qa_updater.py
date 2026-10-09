"""Prove comportamentali su COPIA della biblioteca; mai muta l'originale."""
import argparse, copy, hashlib, json, re, shutil, subprocess, uuid, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

BASE = Path(__file__).resolve().parent
NS = {'office':'urn:oasis:names:tc:opendocument:xmlns:office:1.0', 'table':'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'text':'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}
for prefix, uri in NS.items(): ET.register_namespace(prefix, uri)
def q(prefix, key): return '{'+NS[prefix]+'}'+key
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def records(path):
    match = re.search(r'<script id="catalog-data" type="application/json">(.*?)</script>',path.read_text(encoding='utf-8'),re.S)
    return json.loads(match.group(1))
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--library',type=Path,required=True)
    args=parser.parse_args(); original=args.library.resolve()
    qa=BASE/'qa'; qa.mkdir(exist_ok=True)
    root=qa/('copia-updater-'+uuid.uuid4().hex[:8]); shutil.copytree(original,root)
    report={'library':str(original),'copy':str(root),'tests':[]}
    paths=['Catalogo.ods','Manutenzione/aggiorna-indice.ps1','Manutenzione/index-template.html','Aggiorna indice.cmd']
    report['source_hashes']={p:digest(original/p) for p in paths}
    catalog=root/'Catalogo.ods'; index=root/'Indice.html'; template=root/'Manutenzione/index-template.html'
    baseline=catalog.read_bytes(); template_bytes=template.read_bytes()
    def load():
        with zipfile.ZipFile(catalog) as z: return ET.fromstring(z.read('content.xml'))
    def save(doc):
        with zipfile.ZipFile(catalog) as z: entries=[(x,z.read(x.filename)) for x in z.infolist()]
        with zipfile.ZipFile(catalog,'w') as z:
            for info,data in entries: z.writestr(info,ET.tostring(doc,encoding='utf-8',xml_declaration=True) if info.filename=='content.xml' else data)
    def sheet(doc): return next(x for x in doc.findall('.//table:table',NS) if x.get(q('table','name'))=='Risorse')
    def rows(doc): return sheet(doc).findall('.//table:table-row',NS)
    def cells(row): return row.findall('table:table-cell',NS)
    def values(row): return [''.join(x.itertext()).strip() for x in cells(row)]
    def datarow(doc): return next(x for x in rows(doc) if len(cells(x))>=12 and values(x)[0] not in ('','ID'))
    def setcell(row,i,value):
        c=cells(row)[i]; c.clear(); c.set(q('office','value-type'),'string'); ET.SubElement(c,q('text','p')).text=value; return c
    def invoke():
        p=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(root/'Manutenzione/aggiorna-indice.ps1')],capture_output=True,timeout=30)
        return p.returncode,(p.stdout+p.stderr).decode('utf-8',errors='replace').strip()
    def invoke_cmd():
        p=subprocess.run(['cmd.exe','/d','/c',str(root/'Aggiorna indice.cmd')],input=b'\r\n',capture_output=True,timeout=30)
        return p.returncode,(p.stdout+p.stderr).decode('utf-8',errors='replace').strip()
    def record(name,ok,**evidence):
        report['tests'].append({'name':name,'passed':bool(ok),**evidence})
        (qa/'updater-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        if not ok: raise AssertionError(name+' '+str(evidence))
    code,msg=invoke(); record('generation_from_real_catalog',code==0,code=code,message=msg)
    initial=records(index); n=len(initial); report['baseline_resources']=n
    code,msg=invoke(); first_hash=digest(index)
    code,msg=invoke(); record('repeat_same_catalog_is_deterministic',code==0 and first_hash==digest(index),sha256=digest(index))
    code,msg=invoke_cmd(); record('user_CMD_updates_real_catalog',code==0 and first_hash==digest(index),code=code,message=msg)

    doc=load(); row=datarow(doc); rid=values(row)[0]
    special='Verifica elettricità: caffè <script> & "mappe"'
    setcell(row,1,special); setcell(row,5,'Recupero attivo: leggere, scegliere, usare. Aggiornamento QA.')
    dt=setcell(row,11,'02/10/2026'); dt.set(q('office','value-type'),'date'); dt.set(q('office','date-value'),'2026-10-02T00:00:00')
    # An actual new resource with fresh relative paths containing spaces, accents, # and %.
    new=copy.deepcopy(row); new_id='QA-NUOVA-RISORSA'; setcell(new,0,new_id); setcell(new,1,'Nuova risorsa QA con caratteri è # %')
    for i,key in [(9,'PDF'),(10,'Sorgente')]:
        old=next(x[key] for x in initial if x['ID']==rid); ext=Path(old).suffix
        rel='Prove QA/risorsa è # 100%'+ext; target=root/rel; target.parent.mkdir(exist_ok=True); shutil.copy2(root/old,target); setcell(new,i,rel)
    sheet(doc).append(new); save(doc)
    code,msg=invoke(); updated=records(index); old_record=next(x for x in updated if x['ID']==rid)
    record('edit_text_date_and_add_new_resource',code==0 and len(updated)==n+1 and old_record['Titolo']==special and old_record['Revisione']=='2026-10-02' and any(x['ID']==new_id for x in updated),message=msg,count=len(updated),changed_record=old_record)
    modified_hash=digest(index); code,msg=invoke()
    record('repeat_after_changes',code==0 and digest(index)==modified_hash,sha256=digest(index))
    report['changed_index']=str(index)

    # Make a second isolated copy for UI checks of text and URL escaping, before the error cases.
    ui_copy=qa/('copia-browser-caratteri-'+uuid.uuid4().hex[:8]); shutil.copytree(root,ui_copy)
    report['changed_browser_copy']=str(ui_copy)
    catalog.write_bytes(baseline); doc=load(); row=datarow(doc); rid=values(row)[0]
    # Consecutive equal cells encoded as a repeated cell, rich text, blank repeated rows and columns.
    setcell(row,2,'Area QA'); setcell(row,3,'Area QA'); cells(row)[2].set(q('table','number-columns-repeated'),'2'); row.remove(cells(row)[3])
    title=cells(row)[1]; title.clear(); title.set(q('office','value-type'),'string'); p=ET.SubElement(title,q('text','p')); p.text='Testo'; ET.SubElement(p,q('text','s'),{q('text','c'):'2'}).tail='con'; ET.SubElement(p,q('text','tab')).tail='tab'; ET.SubElement(p,q('text','line-break')).tail='seconda riga'; ET.SubElement(p,q('text','span')).text=' accentata è'
    blank=ET.Element(q('table','table-row'),{q('table','number-rows-repeated'):'1000000'}); ET.SubElement(blank,q('table','table-cell'),{q('table','number-columns-repeated'):'16384'})
    sheet(doc).append(blank); ET.SubElement(row,q('table','table-cell'),{q('table','number-columns-repeated'):'16384'})
    save(doc); code,msg=invoke(); result=records(index); changed=next(x for x in result if x['ID']==rid)
    record('ods_repeated_cells_blank_rows_and_rich_text',code==0 and len(result)==n and changed['Materia']=='Area QA' and changed['Argomento']=='Area QA' and changed['Titolo']=='Testo  con\ttab\nseconda riga accentata è',message=msg,record=changed)

    def bad(name,change):
        catalog.write_bytes(baseline); template.write_bytes(template_bytes); code,_=invoke()
        assert code==0; before=digest(index); change(); code,msg=invoke()
        record(name,code!=0 and before==digest(index) and not list(root.glob('Indice.*.tmp')),code=code,message=msg,index_unchanged=before==digest(index))
    def change_cell(i,value):
        doc=load(); setcell(datarow(doc),i,value); save(doc)
    def mutate_row(attr,value):
        doc=load(); datarow(doc).set(q('table',attr),value); save(doc)
    def duplicate():
        doc=load(); sheet(doc).append(copy.deepcopy(datarow(doc))); save(doc)
    def wrong_date():
        doc=load(); c=setcell(datarow(doc),11,'32/13/2026'); c.set(q('office','value-type'),'date'); c.set(q('office','date-value'),'2026-13-32'); save(doc)
    def wrong_header():
        doc=load(); header=next(r for r in rows(doc) if values(r) and values(r)[0]=='ID'); setcell(header,1,'Titolo errato'); save(doc)
    def extra_column():
        doc=load(); r=datarow(doc); c=ET.SubElement(r,q('table','table-cell'),{q('office','value-type'):'string'}); ET.SubElement(c,q('text','p')).text='Dato fuori schema'; save(doc)
    def missing_sheet():
        doc=load(); sheet(doc).set(q('table','name'),'Risorse sbagliato'); save(doc)
    def missing_xml():
        with zipfile.ZipFile(catalog,'w') as z: z.writestr('mimetype','application/vnd.oasis.opendocument.spreadsheet')
    bad('duplicate_ID_keeps_previous_index',duplicate)
    bad('missing_required_field_keeps_previous_index',lambda:change_cell(5,''))
    bad('missing_pdf_keeps_previous_index',lambda:change_cell(9,'inesistente.pdf'))
    bad('path_traversal_keeps_previous_index',lambda:change_cell(9,'../esterno.pdf'))
    bad('absolute_path_keeps_previous_index',lambda:change_cell(9,str(original/initial[0]['PDF'])))
    bad('remote_URL_keeps_previous_index',lambda:change_cell(9,'https://example.com/documento.pdf'))
    bad('wrong_source_extension_keeps_previous_index',lambda:change_cell(10,initial[0]['PDF']))
    bad('malformed_ODS_date_keeps_previous_index',wrong_date)
    bad('nonempty_repeated_row_keeps_previous_index',lambda:mutate_row('number-rows-repeated','2'))
    bad('invalid_repetition_keeps_previous_index',lambda:mutate_row('number-rows-repeated','0'))
    bad('wrong_header_keeps_previous_index',wrong_header)
    bad('extra_column_keeps_previous_index',extra_column)
    bad('wrong_sheet_keeps_previous_index',missing_sheet)
    bad('missing_content_XML_keeps_previous_index',missing_xml)
    bad('corrupt_ODS_keeps_previous_index',lambda:catalog.write_bytes(b'not a zip file'))
    bad('invalid_template_keeps_previous_index',lambda:template.write_text('missing data token',encoding='utf-8'))
    catalog.write_bytes(baseline); template.write_bytes(template_bytes); invoke()
    before=digest(index); change_cell(9,'inesistente.pdf'); code,msg=invoke_cmd()
    record('user_CMD_propagates_error_and_keeps_previous_index',code!=0 and before==digest(index),code=code,message=msg,index_unchanged=before==digest(index))
    catalog.write_bytes(baseline); template.write_bytes(template_bytes); invoke()
    record('original_library_unchanged',all(digest(original/p)==value for p,value in report['source_hashes'].items()))
    report['passed']=all(t['passed'] for t in report['tests'])
    (qa/'updater-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':report['passed'],'tests':len(report['tests']),'report':str(qa/'updater-report.json'),'copy':str(root),'changed_browser_copy':str(ui_copy)},ensure_ascii=False))
if __name__=='__main__': main()
