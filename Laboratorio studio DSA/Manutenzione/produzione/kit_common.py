"""Contenuti originali per lotti piccoli; i PDF restano da verificare."""
from produci import MAINT,write_json
from registro_kit import KITS

def P(title,*blocks):return dict(title=title,blocks=list(blocks))
def H(h,t):return dict(h=h,p=t)
def T(t):return dict(p=t)
def B(*items):return dict(bullets=list(items))
def L(n=3):return dict(lines=n)
def TAB(headers,rows,widths=None):
    x=dict(headers=headers,rows=rows)
    if widths:x['widths']=widths
    return dict(table=x)
def LINK(label,url):return dict(link=dict(label=label,url=url))

def kit(kid,objective,prerequisites,tool,pages,answers,errors,sources,coverage,gaps,**kw):
    k=KITS[kid]
    pages[0]['subtitle']=k['title']+' · Prerequisiti: '+prerequisites
    common=dict(kit=kid,objective=objective,prerequisites=prerequisites,tool=tool,
        task=kw.get('task',objective),difficulty=kw.get('difficulty','Selezione delle informazioni, sequenza dei passaggi e spiegazione delle scelte: osservare separatamente.'),
        school=kw.get('school','Triennio / priorità terza'),sources='; '.join(s[0]+': '+s[1] for s in sources))
    docs=[dict(common,id=kid+'-S',title=k['title']+' — attività',audience='Studente',pages=pages),
          dict(common,id=kid+'-T',title=k['title']+' — guida tutor',audience='Tutor',pages=[
              P('Soluzioni e criteri',*answers),
              P('Condurre e adattare',H('Errori da distinguere',errors),
                H('Aiuto graduato, strumento disponibile','Prima chiedere una spiegazione; poi offrire un indizio sul punto critico; infine mostrare un passaggio. Annotare l’aiuto senza confonderlo con la correttezza. Si può leggere la consegna, rispondere oralmente o usare la sintesi vocale. Ridurre l’aiuto non significa togliere lo strumento utile.'),
                H('Ripasso e osservazione','Scegliere una domanda finale e riprovarla in un giorno diverso. Registrare correttezza, aiuti, uso dello strumento, tempo indicativo e fatica riferita separatamente. Modificare l’intervallo in base alla scadenza e all’esito.'),
                H('Copertura e limite',coverage+' Non ancora coperto: '+gaps),
                H('Fonti e natura del materiale','Testi, esempi e consegne sono adattamenti editoriali originali; le fonti seguenti sostengono i contenuti o il metodo, non validano questo kit sul campo.'),
                *[LINK(label,url) for label,url in sources])])]
    if kw.get('source_page'):
        conduct=docs[1]['pages'][1]['blocks']
        split=next(i for i,b in enumerate(conduct) if b.get('h')=='Fonti e natura del materiale')
        docs[1]['pages'].append(P('Fonti e uso delle unità',*conduct[split:],H('Unità brevi','Scegliere una pagina di contenuto per incontro, con la domanda associata. Riprendere poi lo strumento e una consegna nuova. Non occorre completare tutte le pagine nello stesso incontro. I collegamenti alle fonti richiedono rete; le attività sono interamente utilizzabili offline.')))
        del conduct[split:]
        conduct.insert(0,H('Obiettivo del kit',objective+'.'))
    write_json(MAINT/'produzione/contenuti'/(kid+'.json'),dict(id=kid,coverage=coverage,gaps=gaps,sources=sources,version='1.0'))
    return docs

def save(batch,docs):
    ids={d['kit'] for d in docs}
    assert len(ids)<=4
    write_json(MAINT/'produzione/dati'/(batch+'.json'),docs)
    print(batch,len(ids),'kit',sum(len(d['pages']) for d in docs),'pagine previste')
