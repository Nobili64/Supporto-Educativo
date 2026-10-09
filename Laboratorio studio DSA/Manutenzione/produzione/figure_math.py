"""Schemi geometrici originali, vettoriali, con etichette indipendenti dai colori."""
from html import escape
def text(x,y,s,size=23):return f'<text x="{x}" y="{y}" font-size="{size}" font-family="Arial" fill="#111">{escape(str(s))}</text>'
def line(x1,y1,x2,y2,dash=False):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="2"'+(' stroke-dasharray="7 5"' if dash else '')+'/>'
def fig(id,body,h,alt):
    return {'p':'@@FIG:'+id+'@@','figure':dict(id=id,svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="{h}" viewBox="0 0 800 {h}"><rect width="800" height="{h}" fill="white"/>{body}</svg>',height=round(h*17.6/800,3),alt=alt)}
def triangle():
    body='<path d="M120 210 L120 30 L360 210 Z" fill="none" stroke="#222" stroke-width="3"/><path d="M120 190 L140 190 L140 210" fill="none" stroke="#222" stroke-width="2"/>'
    body+=text(30,125,'6 cm')+text(220,242,'8 cm')+text(275,112,'10 cm')+text(440,85,'Cateti: 6 cm e 8 cm')+text(440,130,'Ipotenusa: 10 cm')+text(440,185,'Angolo retto segnato')
    return fig('triangolo-6-8-10',body,265,'Triangolo rettangolo: cateti 6 e 8 cm, ipotenusa 10 cm. Angolo retto fra i cateti.')
def circle():
    body='<circle cx="180" cy="125" r="85" fill="none" stroke="#222" stroke-width="3"/>'+line(180,125,265,125)+text(188,112,'r')+text(172,151,'O')
    body+=text(330,90,'r = 3 cm; d = 2r = 6 cm')+text(330,138,'C = 6π cm')+text(330,185,'A = 9π cm²')
    return fig('cerchio-r3',body,240,'Cerchio con centro O e raggio r uguale a 3 cm; diametro 6 cm, circonferenza 6 pi cm e area 9 pi cm quadrati.')
def prism():
    front=[(130,190),(360,190),(360,90),(130,90)];back=[(190,140),(420,140),(420,40),(190,40)]
    body=''
    for poly in [front,back]:
      for a,b in zip(poly,poly[1:]+poly[:1]):body+=line(*a,*b)
    for a,b in zip(front,back):body+=line(*a,*b)
    body+=text(205,225,'a = 8 cm')+text(10,145,'c = 3 cm')+text(375,213,'b = 5 cm')+text(500,95,'A base = a × b')+text(500,143,'V = a × b × c')+text(500,191,'Schema non in scala')
    return fig('parallelepipedo',body,240,'Parallelepipedo rettangolo di lati 8, 5, 3 cm. Diagramma schematico non in scala.')
def grid(id='piano',points=None,blank=False):
    # Unità identica sui due assi: 28 pixel. Spazio di scrittura a destra.
    ox,oy=190,190;step=28;body=''
    for n in range(-5,6):
      x=ox+n*step;y=oy-n*step
      body+=f'<path d="M{x} 50 V330 M50 {y} H330" fill="none" stroke="#aaa" stroke-width="0.7"/>'
    body+=line(40,oy,350,oy)+line(ox,340,ox,35)+text(353,oy+8,'x')+text(ox+8,35,'y')
    for n in [-4,-2,2,4]:body+=text(ox+n*step-9,oy+23,n,18)+text(ox-30,oy-n*step+6,n,18)
    body+=text(ox+6,oy+22,'0',18)
    for name,x,y in (points or []):
      body+=f'<circle cx="{ox+x*step}" cy="{oy-y*step}" r="4" fill="#111"/>'+text(ox+x*step+8,oy-y*step-6,name,21)
    body+=text(425,80,'Una casella = 1 unità')+text(425,127,'Prima x: destra / sinistra')+text(425,174,'Poi y: alto / basso')
    if points:
      for i,(name,x,y) in enumerate(points):body+=text(425,227+i*34,f'{name} = ({x}; {y})')
    return fig(id,body,360,'Piano cartesiano con assi perpendicolari, origine e unità identica su entrambi gli assi. '+str(points or 'Griglia da completare.'))
def bars():
    body=line(85,200,695,200)+line(85,200,85,30)
    for y,lab in [(200,0),(140,1),(80,2)]:
        body+=text(55,y+7,lab,20)
        body+=f'<line x1="85" y1="{y}" x2="695" y2="{y}" stroke="#999" stroke-width="0.7"/>'
    for x,lab,f in [(150,0,1),(280,1,2),(410,2,1),(540,6,1)]:
        body+=f'<rect x="{x}" y="{200-60*f}" width="55" height="{60*f}" fill="#dedede" stroke="#111" stroke-width="2"/>'+text(x+16,231,lab,21)
    body+=text(110,26,'Frequenza: numero di risposte')+text(150,270,'Categoria: libri letti (dati inventati)')
    return fig('frequenze-libri',body,295,'Diagramma a barre delle frequenze: 0 libri una risposta; 1 libro due risposte; 2 libri una risposta; 6 libri una risposta. Categorie distinte, non scala numerica continua.')
