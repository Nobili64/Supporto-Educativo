"""Recupero non distruttivo della base verificabile del 29 settembre 2026."""
from pathlib import Path
import hashlib, json, shutil, zipfile
ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(r'C:\Users\megan\AppData\Local\Temp\codex-dsa-01a0e714')
MAINT = ROOT / 'Manutenzione'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if not (SOURCE/'library/Catalogo.ods').is_file():
        raise SystemExit('Base temporanea non disponibile: recupero interrotto.')
    inventory=[]
    for src in sorted((SOURCE/'library').rglob('*')):
        if src.is_symlink() or src.is_junction():
            raise RuntimeError(f'Collegamento non portabile: {src}')
        if not src.is_file(): continue
        rel=src.relative_to(SOURCE/'library'); dst=ROOT/rel
        if dst.exists() and sha(dst)!=sha(src):
            raise RuntimeError(f'Destinazione differente: {dst}. Nessuna sovrascrittura.')
        dst.parent.mkdir(parents=True,exist_ok=True)
        if not dst.exists(): shutil.copy2(src,dst)
        assert sha(src)==sha(dst)
        inventory.append(dict(path=rel.as_posix(),bytes=src.stat().st_size,sha256=sha(src)))
    prod=MAINT/'produzione-originale'; prod.mkdir(exist_ok=True)
    for src in SOURCE.iterdir():
        if src.is_file() and src.suffix in {'.py','.json','.mjs','.cjs','.ps1','.cmd','.html'}:
            shutil.copy2(src,prod/src.name)
    reports=MAINT/'verifiche-originali'; reports.mkdir(exist_ok=True)
    for folder in ['qa','catalogo-qa']:
        for src in (SOURCE/folder).glob('*'):
            if src.is_file(): shutil.copy2(src,reports/(folder+'-'+src.name))
    archive=MAINT/'archivio'; archive.mkdir(exist_ok=True)
    backup=archive/'base-recuperata-2026-09-29.zip'
    if not backup.exists():
        with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as z:
            for row in inventory: z.write(SOURCE/'library'/row['path'],row['path'])
    report=dict(source=str(SOURCE/'library'),destination=str(ROOT),files=inventory,
                count=len(inventory),verified_equal=True,archive_sha256=sha(backup),
                excluded=['node_modules junction','profili LibreOffice e Edge','copie temporanee QA'],
                note='Casi non consultata e non modificata. Rapporti originali storici: non attestano la futura versione.')
    (MAINT/'inventario-recupero.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (MAINT/'stato.json').write_text(json.dumps(dict(phase='0',status='base recuperata; indice da riallineare e riverificare',disciplinary_target=47,disciplinary_recovered=3,completed_batches=[],next='Riallineare indice, verificare base; definire catalogo e copertura'),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(files=len(inventory),pdf=sum(x['path'].endswith('.pdf') for x in inventory),odt=sum(x['path'].endswith('.odt') for x in inventory),odg=sum(x['path'].endswith('.odg') for x in inventory),verified=True)))
if __name__=='__main__': main()
