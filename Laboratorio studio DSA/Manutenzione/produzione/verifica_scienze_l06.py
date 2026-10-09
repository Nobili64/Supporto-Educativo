"""Ricalcolo indipendente degli esercizi numerici SCI01; non valida la didattica."""
from fractions import Fraction as F
from collections import Counter
from produci import MAINT,write_json

checks=[]
def check(label,actual,expected):
    checks.append(dict(label=label,actual=str(actual),expected=str(expected),passed=actual==expected))

for label,m,v,expected in [('esempio',20,10,F(2)),('guidata A',54,20,F(27,10)),('trasferimento 1',36,12,F(3))]:
    check('Densità g/cm³ '+label,F(m,v),expected)
# Definizioni metriche: 1 cm = 1/100 m; 1 mL = 1/1 000 000 m³.
check('20 cm³ in mL',20*F(1,100)**3/F(1,1000000),20)
check('Soluzione chiusa in g',sum([100,5]),105)
check('Esempio sistema aperto in g',250-3,247)
check('Nuovo sistema aperto in g',180-4,176)
check('Bilancio includendo gas uscito in g',176+4,180)
left=Counter(H=2*2,O=1*2)
right=Counter(H=2*2,O=2*1)
check('2 H2 + O2 -> 2 H2O: conservazione atomi',left,right)
check('Densità diverse a pari volume',F(3)*12>F(2)*12,True)
write_json(MAINT/'verifiche/L06-calcoli.json',dict(scope='SCI01: densità, conversioni metriche, bilanci di massa, conteggio atomi',checks=checks,passed=all(c['passed'] for c in checks)))
assert all(c['passed'] for c in checks),checks
print(len(checks),'controlli numerici superati')
