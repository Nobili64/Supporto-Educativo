"""Verifica indipendente: incroci enumerati, grandezze esatte e percorsi."""
from fractions import Fraction as F
from collections import Counter
from itertools import product
from produci import MAINT, write_json

checks=[]
def check(name, actual, expected):
    checks.append(dict(name=name,actual=str(actual),expected=str(expected),passed=actual==expected))
def cross(a,b):
    counts=Counter(''.join(sorted(x)) for x in product(a,b))
    return {k:F(v,4) for k,v in counts.items()}

check('Aa x Aa',cross('Aa','Aa'),{'AA':F(1,4),'Aa':F(1,2),'aa':F(1,4)})
check('AA x aa',cross('AA','aa'),{'Aa':F(1)})
check('Aa x aa',cross('Aa','aa'),{'Aa':F(1,2),'aa':F(1,2)})
check('AA x Aa',cross('AA','Aa'),{'AA':F(1,2),'Aa':F(1,2)})
check('Fenotipi e percentuali', [F(3,4)*100,F(1,4)*100,F(2,10)*100,F(2,4)*100], [75,25,20,50])
check('Cromosomi tipici',23+23,46)
check('Bilanci e rendimenti', [200-120,F(120,200)*100,500-350,F(350,500)*100],[80,60,150,70])
for label,v,i,minutes,p,e in [('Esempio',9,F(1,5),10,F(9,5),1080),('Guidata',6,F(1,2),2,3,360),('Trasferimento',12,F(2,5),5,F(24,5),1440)]:
    check(label+' P ed E',[v*i,v*i*minutes*60],[p,e])
check('W ore -> Wh',[6*5,15*2,8*3,12*F(1,2),3*3,8*1],[30,30,24,6,9,8])
check('Wh -> kWh',[F(x,1000) for x in [30,24,8]],[F('0.030'),F('0.024'),F('0.008')])
check('kWh -> J',1000*3600,3600000)
check('Scala: distanza in m',[2*25000/100,F('3.6')*50000/100,F('4.5')*20000/100,3*20000/100],[500,1800,900,600])
check('Scala inversa in cm',[750*100/25000,1000*100/25000],[3,4])
check('Metri -> km',F(1800,1000),F('1.8'))
coords={'A1':(0,0),'B1':(1,0),'C1':(2,0),'C2':(2,1),'C3':(2,2),'B2':(1,1),'A2':(0,1),'A3':(0,2),'B3':(1,2)}
def route(names):
    pts=[coords[x] for x in names]
    steps=[(b[0]-a[0],b[1]-a[1]) for a,b in zip(pts,pts[1:])]
    assert all(abs(x)+abs(y)==1 for x,y in steps)
    return (steps,200*len(steps))
check('Percorso esempio',route(['B2','A2','A3']),([(-1,0),(0,1)],400))
check('Percorso guidato',route(['A1','B1','C1','C2','C3']),([(1,0),(1,0),(0,1),(0,1)],800))
# Rotazione oraria del foglio: N(0,1) -> (1,0), E(1,0) -> (0,-1).
rot=lambda p:(p[1],-p[0])
check('Orientamento N a destra',[rot((0,1)),rot((1,0)),rot((0,-1))],[(1,0),(0,-1),(-1,0)])
out=dict(date='2026-09-30',batch='L07-scienze-geografia',checks=checks,passed=sum(x['passed'] for x in checks),total=len(checks),limits='Controllo di modelli e dati didattici, non validazione genetica, misura sperimentale o carta per navigazione.')
write_json(MAINT/'verifiche/L07-calcoli.json',out)
print(f"{out['passed']}/{out['total']} controlli superati")
assert all(x['passed'] for x in checks)
