"""Produzione protetta. Gli ODT modificati a mano non vengono sovrascritti."""
from pathlib import Path
import json,hashlib,importlib.util,subprocess,sys,shutil,argparse
from registro_kit import ROOT,folder,KITS
from writer_native import fix_tables
MAINT=ROOT/'Manutenzione'; WORK=ROOT.parent/'.lavorazione-dsa'
LO=Path(r'C:\Program Files\LibreOffice\program\soffice.exe')
spec=importlib.util.spec_from_file_location('writer_base',MAINT/'produzione-originale/build.py')
writer=importlib.util.module_from_spec(spec);spec.loader.exec_module(writer)
writer.DATE='2026-09-29'
LEDGER=MAINT/'produzione/impronte-produzione.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p,default):return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default
def write_json(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def paths(d):
    base=folder(d['kit']) if d.get('kit') in KITS else Path(d['folder'])
    src=base/'Modificabili'/(d['id']+'.odt')
    pdf=base/('Tutor' if d['audience']=='Tutor' else 'Studente')/(d['id']+'.pdf')
    return src,pdf
def main():
    ap=argparse.ArgumentParser();ap.add_argument('batch');ap.add_argument('--only',nargs='+');args=ap.parse_args()
    batch=Path(__file__).parent/'dati'/(args.batch+'.json');full=load(batch,None)
    if not full:raise SystemExit('Lotto dati non trovato')
    if args.only and not set(args.only)<={d['id'] for d in full}:raise SystemExit('ID --only non presente nel lotto')
    data=[d for d in full if not args.only or d['id'] in args.only]
    kids={d.get('kit') for d in data if d.get('kit') in KITS}
    if len(kids)>4:raise SystemExit('Massimo quattro kit disciplinari per lotto')
    ledger=load(LEDGER,{});records=[]
    # Preflight completo prima di scrivere file.
    for d in data:
        for rel in paths(d):
            f=ROOT/rel
            if f.exists() and ledger.get(rel.as_posix())!=sha(f):raise SystemExit(f'Modifica manuale o file non gestito: {rel}. Conservato.')
    for d in data:
        src,pdf=paths(d);dest=ROOT/pdf;dest.parent.mkdir(parents=True,exist_ok=True)
        writer.DATE=d.get('date','2026-09-29')
        writer.odt(ROOT/src,d)
        fix_tables(ROOT/src,d)
        cmd=[str(LO),f'-env:UserInstallation={(WORK/"lo-produzione").as_uri()}','--headless','--convert-to','pdf','--outdir',str(dest.parent),str(ROOT/src)]
        proc=subprocess.run(cmd,capture_output=True,timeout=90)
        if proc.returncode or not dest.exists():raise RuntimeError(proc.stdout.decode(errors='replace')+proc.stderr.decode(errors='replace'))
        for rel in [src,pdf]:ledger[rel.as_posix()]=sha(ROOT/rel)
        k=KITS.get(d.get('kit'),{})
        records.append(dict(id=d['id'],title=d['title'],subject=d.get('subject',k.get('subject')),topic=d.get('topic',k.get('title')),school=d.get('school','Triennio / priorità terza'),objective=d['objective'],kind=d.get('kind','Schede' if d['audience']=='Studente' else 'Guida e soluzioni'),level=d.get('level','Graduale'),audience=d['audience'],pdf=pdf.as_posix(),source=src.as_posix(),date=writer.DATE,expected_pages=len(d['pages']),kit=d.get('kit',d['id']),prerequisites=d.get('prerequisites','Lettura della consegna con supporto disponibile'),task=d.get('task',d['objective']),difficulty=d.get('difficulty','Da osservare nel compito: selezione delle informazioni e uso dello strumento'),tool=d.get('tool','Schema adattabile'),curriculum=d.get('curriculum','D.M. 254/2012: '+str(k.get('subject',d.get('subject','competenze trasversali')))+'; classi II-III 2026/27. Prime 2026/27: confronto con D.M. 221/2025 e curricolo d’istituto.'),sources=d.get('sources','Adattamento editoriale; riferimenti nella guida tutor'),version='1.0',status='da verificare',batch=args.batch))
        records[-1]['private']=d.get('private',False)
        write_json(LEDGER,ledger)
        print(d['id'],flush=True)
    registration=MAINT/'produzione/registrazioni'/(args.batch+'.json')
    byid={r['id']:r for r in load(registration,[])}
    byid.update({r['id']:r for r in records})
    write_json(registration,[byid[d['id']] for d in full if d['id'] in byid])
    print(f'Lotto {args.batch}: {len(records)} documenti, {len(kids)} kit. Verificare prima del lotto successivo.')
if __name__=='__main__':main()
