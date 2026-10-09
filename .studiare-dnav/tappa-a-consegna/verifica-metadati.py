"""Verifica read-only dei DOI presso Crossref; cache locale per ripetibilità."""
from pathlib import Path
import json,re,urllib.request,concurrent.futures
P=Path(__file__).resolve().parent
refs=json.loads((P/'registro-fonti-locali.json').read_text(encoding='utf-8'))
dois=sorted(set(d.rstrip('.,;)') for r in refs for d in r['doi']))
dois+=['10.1016/j.jcbs.2025.100973','10.1016/j.jcbs.2025.100886','10.1176/appi.psychotherapy.20250034']
def get(d):
    try:
        req=urllib.request.Request('https://api.crossref.org/works/'+d,headers={'User-Agent':'BibliographicCheck/1.0'})
        with urllib.request.urlopen(req,timeout=25) as r: m=json.load(r)['message']
        return dict(doi=d,esito='trovato',titolo=m.get('title'),autori=[a.get('family','') for a in m.get('author',[])],pubblicazione=m.get('published'),doi_restituito=m.get('DOI'),url=m.get('URL'))
    except Exception as e:return dict(doi=d,esito='non verificato',errore=str(e))
cache=P/'verifica-doi.json'
previous=json.loads(cache.read_text(encoding='utf-8'))['fonti'] if cache.exists() else []
known={r['doi']:r for r in previous if r['esito']=='trovato'}
# I tentativi già riusciti non vengono ripetuti. Pochi accessi seriali evitano raffiche.
rows=[known[d] if d in known else get(d) for d in dois]
(P/'verifica-doi.json').write_text(json.dumps(dict(data='2026-09-30',nota='Metadati: non equivalgono a verifica dei risultati dello studio.',fonti=rows),ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(totale=len(rows),trovati=sum(r['esito']=='trovato' for r in rows),non_verificati=[r for r in rows if r['esito']!='trovato']),ensure_ascii=False))
