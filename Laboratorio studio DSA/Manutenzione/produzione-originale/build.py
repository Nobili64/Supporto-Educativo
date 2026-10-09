from pathlib import Path
from xml.sax.saxutils import escape
import json, zipfile, subprocess, sys, shutil, re

BASE=Path(__file__).parent
OUT=BASE/'library'
DATE='2026-09-28'
LO=Path(r'C:\Program Files\LibreOffice\program\soffice.exe')
NS='''xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"'''
def e(s): return escape(str(s),{'"':'&quot;'})
def pkg(path,kind,content,styles):
    path.parent.mkdir(parents=True,exist_ok=True)
    mime='application/vnd.oasis.opendocument.'+kind
    manifest=f'''<?xml version="1.0" encoding="UTF-8"?><manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.3"><manifest:file-entry manifest:full-path="/" manifest:media-type="{mime}"/><manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/><manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/><manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/></manifest:manifest>'''
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('mimetype',mime,compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/manifest.xml',manifest)
        z.writestr('content.xml',content)
        z.writestr('styles.xml',styles)
        z.writestr('meta.xml',f'<office:document-meta {NS} office:version="1.3"><office:meta><dc:title>{e(path.stem)}</dc:title><dc:language>it-IT</dc:language><meta:creation-date>{DATE}T12:00:00</meta:creation-date></office:meta></office:document-meta>')

def p(s,style='Body'):
    # Explicit line breaks retain intended spacing in formulas and instructions.
    return f'<text:p text:style-name="{style}">'+ '<text:line-break/>'.join(e(x) for x in str(s).split('\n'))+'</text:p>'

def odt(path,doc):
    styles=f'''<office:document-styles {NS} office:version="1.3"><office:font-face-decls><style:font-face style:name="Arial" svg:font-family="Arial"/></office:font-face-decls><office:styles>
    <style:default-style style:family="paragraph"><style:paragraph-properties fo:line-height="120%" fo:margin-bottom="0.18cm" fo:orphans="2" fo:widows="2"/><style:text-properties style:font-name="Arial" fo:font-size="14pt" fo:color="#202833" fo:language="it" fo:country="IT"/></style:default-style>
    <style:style style:name="Body" style:family="paragraph"/>
    <style:style style:name="Title" style:family="paragraph"><style:paragraph-properties fo:keep-with-next="always" fo:margin-bottom="0.38cm"/><style:text-properties fo:font-size="23pt" fo:font-weight="bold" fo:color="#16384B"/></style:style>
    <style:style style:name="NewTitle" style:family="paragraph" style:parent-style-name="Title"><style:paragraph-properties fo:break-before="page"/></style:style>
    <style:style style:name="Sub" style:family="paragraph"><style:paragraph-properties fo:keep-with-next="always" fo:margin-bottom="0.35cm"/><style:text-properties fo:font-size="12pt" fo:color="#4A5963"/></style:style>
    <style:style style:name="Heading" style:family="paragraph"><style:paragraph-properties fo:keep-with-next="always" fo:margin-top="0.24cm" fo:margin-bottom="0.13cm"/><style:text-properties fo:font-weight="bold" fo:font-size="16pt" fo:color="#16384B"/></style:style>
    <style:style style:name="Bullet" style:family="paragraph"><style:paragraph-properties fo:margin-left="0.35cm" fo:text-indent="-0.3cm" fo:margin-bottom="0.15cm"/></style:style>
    <style:style style:name="Callout" style:family="paragraph"><style:paragraph-properties fo:background-color="#F1F3F3" fo:border-left="0.05cm solid #9B792A" fo:padding="0.22cm" fo:margin-top="0.22cm" fo:margin-bottom="0.26cm"/><style:text-properties fo:font-size="14pt"/></style:style>
    <style:style style:name="Write" style:family="paragraph"><style:paragraph-properties fo:line-height="0.78cm" fo:margin-bottom="0.09cm" fo:border-bottom="0.015cm solid #939AA0"/></style:style>
    <style:style style:name="Small" style:family="paragraph"><style:text-properties fo:font-size="10pt" fo:color="#52616C"/></style:style>
    <style:style style:name="Cell" style:family="table-cell"><style:table-cell-properties fo:padding="0.16cm" fo:border-bottom="0.015cm solid #B6BFC5" style:vertical-align="top"/></style:style>
    <style:style style:name="HeadCell" style:family="table-cell"><style:table-cell-properties fo:background-color="#E3E9EC" fo:padding="0.16cm" fo:border-bottom="0.025cm solid #16384B"/></style:style>
    <style:style style:name="HeadText" style:family="paragraph"><style:paragraph-properties fo:margin-bottom="0cm"/><style:text-properties fo:font-weight="bold" fo:font-size="14pt"/></style:style>
    <style:style style:name="TableText" style:family="paragraph"><style:paragraph-properties fo:margin-bottom="0.06cm"/></style:style>
    </office:styles><office:automatic-styles><style:page-layout style:name="A4"><style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm" style:print-orientation="portrait" fo:margin-top="1.5cm" fo:margin-bottom="1.4cm" fo:margin-left="1.7cm" fo:margin-right="1.7cm"/><style:footer-style><style:header-footer-properties fo:min-height="0.6cm" fo:margin-top="0.3cm"/></style:footer-style></style:page-layout></office:automatic-styles><office:master-styles><style:master-page style:name="Standard" style:page-layout-name="A4"><style:footer>{p('LABORATORIO STUDIO DSA  /  '+doc.get('audience','Tutor')+'  /  '+DATE,'Small')}<text:p text:style-name="Small">Pagina <text:page-number text:select-page="current"/></text:p></style:footer></style:master-page></office:master-styles></office:document-styles>'''
    body=[]; auto=[]; table_i=0
    for n,page in enumerate(doc['pages']):
        body.append(p(page['title'],'NewTitle' if n else 'Title'))
        body.append(p(page.get('subtitle',doc['title']),'Sub'))
        for b in page['blocks']:
            if 'h' in b: body.append(p(b['h'],'Heading'))
            if 'p' in b: body.append(p(b['p']))
            if 'link' in b:
                body.append(f'<text:p text:style-name="Body"><text:a xlink:type="simple" xlink:href="{e(b["link"]["url"])}">{e(b["link"]["label"])}</text:a></text:p>')
            for s in b.get('bullets',[]): body.append(p('• '+s,'Bullet'))
            if 'callout' in b: body.append(p(b['callout'],'Callout'))
            if 'table' in b:
                table_i+=1; t=b['table']; cols=len(t['headers']); widths=t.get('widths',[17.6/cols]*cols)
                for c,w in enumerate(widths):auto.append(f'<style:style style:name="T{table_i}C{c}" style:family="table-column"><style:table-column-properties style:column-width="{w}cm"/></style:style>')
                body.append(f'<table:table table:name="Tabella{table_i}">')
                for c in range(cols):body.append(f'<table:table-column table:style-name="T{table_i}C{c}"/>')
                for r,row in enumerate([t['headers']]+t['rows']):
                    body.append('<table:table-row>')
                    for val in row:body.append(f'<table:table-cell table:style-name="{"HeadCell" if r==0 else "Cell"}" office:value-type="string">{p(val,"HeadText" if r==0 else "TableText")}</table:table-cell>')
                    body.append('</table:table-row>')
                body.append('</table:table>')
            for _ in range(b.get('lines',0)):body.append(p(' ','Write'))
    content=f'<office:document-content {NS} office:version="1.3"><office:automatic-styles>{"".join(auto)}</office:automatic-styles><office:body><office:text>{"".join(body)}</office:text></office:body></office:document-content>'
    pkg(path,'text',content,styles)

catalog=[]
def add(doc,subject,topic,folder):
    folder=OUT/folder
    src=folder/'Modificabili'/(doc['id']+'.odt')
    pdf=folder/('Tutor' if doc['audience']=='Tutor' else 'Studente')/(doc['id']+'.pdf')
    pdf.parent.mkdir(parents=True,exist_ok=True)
    odt(src,doc)
    catalog.append(dict(id=doc['id'],title=doc['title'],subject=subject,topic=topic,school=doc.get('school','Terza / adattabile'),objective=doc.get('objective',doc['pages'][0].get('subtitle','')),kind=doc.get('kind','Scheda'),level=doc.get('level','Graduale'),audience=doc['audience'],pdf=pdf.relative_to(OUT).as_posix(),source=src.relative_to(OUT).as_posix(),date=DATE,expected_pages=len(doc['pages'])))

def convert(entry):
    src=OUT/entry['source']; dest=(OUT/entry['pdf']).parent
    dest.mkdir(parents=True,exist_ok=True)
    profile=(BASE/'lo-profile').as_uri()
    cmd=[str(LO),f'-env:UserInstallation={profile}','--headless','--convert-to','pdf','--outdir',str(dest),str(src)]
    r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=90)
    try: message=r.stdout.decode('utf-8')
    except UnicodeDecodeError: message=r.stdout.decode('cp1252',errors='replace')
    if r.returncode or not (OUT/entry['pdf']).exists():raise RuntimeError(message)
    return message.strip()

def main():
    OUT.mkdir(exist_ok=True)
    for name in ['matematica','storia','scienze']:
        f=BASE/(name+'.json')
        if not f.exists():continue
        kit=json.loads(f.read_text(encoding='utf-8-sig'))
        for doc in kit['documents']:add(doc,kit['subject'],kit['topic'],Path('Materie')/kit['subject']/kit['topic'])
    if (BASE/'trasversali.json').exists():
        for doc in json.loads((BASE/'trasversali.json').read_text(encoding='utf-8')):
            add(doc,doc.get('subject','Metodo di studio'),doc.get('topic','Strategie trasversali'),doc.get('folder','Metodo di studio'))
    if (BASE/'fonti.json').exists():
        doc=json.loads((BASE/'fonti.json').read_text(encoding='utf-8-sig'))
        add(doc,doc['subject'],doc['topic'],doc['folder'])
    from maps import build_maps
    catalog.extend(build_maps(OUT,pkg,NS,p,e))
    (BASE/'catalog-data.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Sorgenti create: {len(catalog)}',flush=True)
    for item in catalog:print(convert(item),flush=True)
    (OUT/'Manutenzione').mkdir(exist_ok=True)

if __name__=='__main__':main()
