"""Controllo indipendente: Fraction/Decimal, distinto dai contenuti Writer."""
from fractions import Fraction as F
from decimal import Decimal,getcontext
import math
from statistics import mean,median,multimode
from itertools import product
from produci import write_json,MAINT
getcontext().prec=30
C=[]
def check(label,actual,expected):
    C.append(dict(label=label,actual=str(actual),expected=str(expected),passed=actual==expected))
def L02():
    for label,a,e in [
      ('MAT01 A',F(2,3)*12,8),('MAT01 B',F(10,15),F(2,3)),
      ('MAT01 C',F(5,6)>F(3,4),True),('MAT01 D',F(2,5)+F(1,10),F(1,2)),
      ('MAT01 E',F(7,8)-F(1,4),F(5,8)),('MAT01 F',F(3,5)*F(10,9),F(2,3)),
      ('MAT01 G',F(2,3)/F(4,5),F(5,6)),('MAT01 H',F(2,3)*18,12),
      ('MAT01 I',sorted([-2,F(1,2),F(-1,2),0]),[-2,F(-1,2),0,F(1,2)]),
      ('MAT01 J',[-4+7,-2-3,-3*5,F(-12,-4)],[3,-5,-15,3]),
      ('MAT01 K',F('0.25'),F(1,4)),('MAT01 strumento',F(1,2)+F(1,3),F(5,6)),
      ('MAT01 trasferimento1',F(3,4)-F(1,6),F(7,12)),('MAT01 trasferimento2',F(5,6)/F(2,3),F(5,4)),
      ('MAT01 trasferimento3',F(3,5)*25,15),('MAT01 delta temperatura',4-(-2),6),
      ('MAT01 confronto finale',F(1,2)<F(2,3)<F(3,4),True),
      ('MAT02 esempio',18-2*(3+1)**2/4,10),('MAT02 A',24/3*2,16),
      ('MAT02 B',5+2*(7-4),11),('MAT02 C',(5+2)*(7-4),21),
      ('MAT02 D',2**4*2**3,128),('MAT02 E',7**3/7**2,7),('MAT02 F',(2**2)**3,64),
      ('MAT02 G',[(-2)**4,-2**4],[16,-16]),('MAT02 H',Decimal(64).sqrt(),8),
      ('MAT02 I',5<Decimal(30).sqrt()<6,True),('MAT02 J',[Decimal(25).sqrt(),Decimal(9).sqrt()+Decimal(16).sqrt()],[5,7]),
      ('MAT02 collaudo',30-12/3*2,22),('MAT02 T1',40-3*(2+1)**2,13),
      ('MAT02 T2',3**2*3**3/3**4,3),('MAT02 T3',Decimal(144).sqrt()+2**3,20),
      ('MAT02 T4',(-4)**2-Decimal(25).sqrt(),11),('MAT02 T5',Decimal(50).sqrt().quantize(Decimal('.01')),Decimal('7.07')),
      ('MAT02 controesempio',24/(3*2),4),('MAP05 esempio',2+3*4,14),('MAP05 guidata',5+2*3,11),
      ('MAP06 rettangolo A',5*3,15),('MAP06 rettangolo P',2*(5+3),16),
    ]:check(label,a,e)
def L03():
    for label,a,e in [
      ('MAT03 rapporti',[12/4*7,2*21/7,F(50,200)],[21,6,F(1,4)]),
      ('MAT03 percentuali',[150*.2,9/36*100,24/.4,60*.75,120*.8],[30,25,60,45,96]),
      ('MAT03 trasferimento',[300/4*6,200*.35,200-70,(65-50)/50*100,8*15/5,25*2/5],[450,70,130,30,24,10]),
      ('MAT05 area e perimetro',[8*5,2*(8+5),12*7/2,9*4,2*(9+5)],[40,26,42,36,28]),
      ('MAT05 Pitagora',[math.hypot(6,8),math.hypot(5,12),math.sqrt(17**2-8**2)],[10,13,15]),
      ('MAT05 cerchio',[round(6*math.pi,2),round(9*math.pi,2)],[18.85,28.27]),
      ('MAT05 trapezio',(10+6)*4/2,32),
      ('MAT05 trasferimento',[9*12,2*(9+12),math.hypot(9,12),math.sqrt(10**2-6**2),6*8/2,12*16/2],[108,42,15,8,24,96]),
      ('MAT05 area conversione',F(1,2)*100**2,5000),
      ('MAT06 esempio',[8*5*3,2*(8*5+8*3+5*3)],[120,158]),
      ('MAT06 cubo prisma',[4**3,6*4**2,12*5,16*5+2*12],[64,96,60,104]),
      ('MAT06 cono coefficienti pi',[3**2*4/3,3*5+3**2],[12,24]),
      ('MAT06 piramide',30*9/3,90),('MAT06 sfera coefficienti pi',[F(4,3)*3**3,4*3**2,4*2**2],[36,36,16]),
      ('MAT06 cilindro approssimato',[round(20*math.pi,2),round(28*math.pi,2)],[62.83,87.96]),
      ('MAT06 capacita',[20*10*15,2.5*1000,4500/1000],[3000,2500,4.5]),
      ('MAT06 trasferimento',[6*4*5,2*(24+30+20),3**2*10,2*3*10+2*3**2,6**2*8/3,F(4,3)*6**3,4*6**2],[120,148,90,78,96,288,144]),
      ('MAT07 inversa',[24/x for x in [2,3,6,8]],[12,8,4,3]),
      ('MAT07 trasferimento',[3-(-2),F(450,100)/3*5,18/3,18/6],[5,F(15,2),6,3]),
      ('MAT07 nessuna proporzione',[(2*x+1)/x for x in [1,2]],[3,2.5])
    ]:check(label,a,e)
def L04():
    for label,a,e in [
      ('MAT04 iniziale',[3*4+2,3*(4+2),3*(2*2-1)-2],[14,18,7]),
      ('MAT04 equazioni verifica',[8/2+3,3*(11-2),2*11+5,2+4*7],[7,27,27,30]),
      ('MAT04 errore e trasferimento',[-2*(1-3),-2*1-6,5*4-2*(4+3)],[4,-8,6]),
      ('MAT08 iniziale',[mean([0,1,1,2,6]),median([0,1,1,2,6]),multimode([0,1,1,2,6])],[2,1,[1]]),
      ('MAT08 guidata',[mean([1,2,2,3,7]),median([1,2,2,3,7]),multimode([1,2,2,3,7]),7-1,median([1,2,4,9])],[3,2,[2],6,3]),
      ('MAT08 trasferimento',[mean([2,2,3,5,8]),median([2,2,3,5,8]),multimode([2,2,3,5,8])],[4,3,[2]]),
      ('MAT08 percentuale',F(sum(x>3 for x in [2,2,3,5,8]),5),F(2,5)),
      ('MAT08 sacchetto',[F(3,6),F(2,6),F(1,6),F(5,6),F(4,8),F(5,8)],[F(1,2),F(1,3),F(1,6),F(5,6),F(1,2),F(5,8)])
    ]:check(label,a,e)
    esiti=list(product('TC',repeat=2))
    for label,predicate,expected in [('una testa',lambda x:x.count('T')==1,F(1,2)),('due teste',lambda x:x.count('T')==2,F(1,4)),('almeno una testa',lambda x:'T' in x,F(3,4)),('almeno una croce',lambda x:'C' in x,F(3,4))]:
        check('MAT08 '+label,F(sum(predicate(x) for x in esiti),len(esiti)),expected)
if __name__=='__main__':
    L02();L03();L04()
    write_json(MAINT/'verifiche/calcoli-python.json',dict(checks=C,passed=all(c['passed'] for c in C)))
    print(len(C),'controlli;',sum(not c['passed'] for c in C),'errori')
    if not all(c['passed'] for c in C):raise SystemExit(1)
