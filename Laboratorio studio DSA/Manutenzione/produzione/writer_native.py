"""Correzioni ODF locali, senza alterare il generatore originale recuperato."""
import zipfile,xml.etree.ElementTree as ET
from copy import deepcopy
from xml.sax.saxutils import escape

O='urn:oasis:names:tc:opendocument:xmlns:office:1.0'
S='urn:oasis:names:tc:opendocument:xmlns:style:1.0'
T='urn:oasis:names:tc:opendocument:xmlns:table:1.0'
F='urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0'
TX='urn:oasis:names:tc:opendocument:xmlns:text:1.0'

def fix_tables(path,doc=None):
    with zipfile.ZipFile(path) as z:parts={n:z.read(n) for n in z.namelist()}
    root=ET.fromstring(parts['content.xml']);styles=ET.fromstring(parts['styles.xml'])
    auto=root.find('{'+O+'}automatic-styles')
    # LibreOffice importa in modo affidabile gli stili automatici delle celle.
    for node in styles.findall('.//{'+S+'}style'):
        if node.get('{'+S+'}family')=='table-cell':auto.append(deepcopy(node))
    row=ET.SubElement(auto,'{'+S+'}style',{'{'+S+'}name':'WritingRow','{'+S+'}family':'table-row'})
    ET.SubElement(row,'{'+S+'}table-row-properties',{'{'+S+'}min-row-height':'1.35cm'})
    for row in root.findall('.//{'+T+'}table-row'):
        if any(not ''.join(cell.itertext()).strip() for cell in row.findall('{'+T+'}table-cell')):
            row.set('{'+T+'}style-name','WritingRow')
    # Figure vettoriali originali incorporate: nessuna dipendenza dalla rete.
    D='urn:oasis:names:tc:opendocument:xmlns:drawing:1.0'
    V='urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0'
    X='http://www.w3.org/1999/xlink'
    M='urn:oasis:names:tc:opendocument:xmlns:manifest:1.0'
    manifest=ET.fromstring(parts['META-INF/manifest.xml'])
    for page in (doc or {}).get('pages',[]):
      for block in page['blocks']:
       if 'figure' in block:
        fig=block['figure'];name='Pictures/'+fig['id']+'.svg'
        parts[name]=fig['svg'].encode('utf-8')
        ET.SubElement(manifest,'{'+M+'}file-entry',{'{'+M+'}full-path':name,'{'+M+'}media-type':'image/svg+xml'})
        para=next(p for p in root.findall('.//{'+TX+'}p') if ''.join(p.itertext())==block['p'])
        para.clear();para.set('{'+TX+'}style-name','Body')
        frame=ET.SubElement(para,'{'+D+'}frame',{'{'+D+'}name':fig['id'],'{'+TX+'}anchor-type':'as-char','{'+V+'}width':'17.6cm','{'+V+'}height':str(fig['height'])+'cm'})
        ET.SubElement(frame,'{'+D+'}image',{'{'+X+'}href':name,'{'+X+'}type':'simple','{'+X+'}show':'embed','{'+X+'}actuate':'onLoad'})
        ET.SubElement(frame,'{'+V+'}desc').text=fig['alt']
    parts['META-INF/manifest.xml']=ET.tostring(manifest,encoding='utf-8',xml_declaration=True)
    parts['content.xml']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for n,v in parts.items():z.writestr(n,v,compress_type=zipfile.ZIP_STORED if n=='mimetype' else zipfile.ZIP_DEFLATED)
