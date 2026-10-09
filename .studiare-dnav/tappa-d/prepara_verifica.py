from pathlib import Path
R=Path(__file__).resolve().parent
t=(R.parent/'tappa-c/verifica.py').read_text(encoding='utf-8')
t=t.replace("'data':'2026-10-01'", "'data':'2026-10-02'")
for a,b in [('S1–S31','S1–S50'),('range(1,32)','range(1,51)'),('C1–C5','C1–C7'),('range(1,6)','range(1,8)'),('len(refs)==31','len(refs)==50'),('len(data)==31','len(data)==50'),('strumenti1–6','strumenti1–7'),('range(1,7)','range(1,8)')]:t=t.replace(a,b)
extra='''
snapshot=json.loads((R/'impronte-blocco-c.json').read_text(encoding='utf-8'))
changed=[d['file'] for d in snapshot if not (P/d['file']).is_file() or sha(P/d['file'])!=d['sha256']]
check('Consegna C approvata: impronte invariate',not changed,{'file':len(snapshot),'differenze':changed})
manual=PdfReader(DELIVERY/NAMES['manuale']);ids=manual.named_destinations
check('D: tutte le tecniche complete previste',all(f'd{i}' in ids for i in [1,2,3,4,6,7,11,12,13,14,15,16,17,18,20,21,22,23,25,26,27,28,29,30]))
check('D: fasi4–5 e intensificato',all(i in ids for i in ['cap11','fase4-passaggio','cap12','fase5-mantenimento','cap13','intensificato-esiti','cap14']))
learner=PdfReader(DELIVERY/NAMES['ragazzo']);li=learner.named_destinations
check('A4: tutte23 schede',all(any(re.match(r'sch'+str(i)+r'(?:$|[^0-9])',k) for k in li) for i in range(1,24)))
check('A4: Scheda13 quattro piu due pagine',all(k in li for k in ['sch13a','sch13b','sch13c','sch13d','sch13-semplice-a','sch13-semplice-b']))
check('A4: sette varianti concrete',all(any(k.startswith('sch'+str(i)+'-semplice') for k in li) for i in [1,2,3,4,13,14,16]))
check('D: durate esempi',sum([5,5,10,20,15,5])==60 and sum([10,20,5,15,10])==60 and sum([3,22,5])==30 and 3*20+15==75)
from decimal import Decimal as D
check('D: decimali',D('3.4')+D('0.56')==D('3.96') and D('2.7')+D('0.48')==D('3.18') and D('12.5')+D('0.75')==D('13.25') and D('8.4')+D('0.35')==D('8.75') and D('15.2')-D('0.85')==D('14.35') and D('0.6')>D('0.45'))
check('D: aree, perimetri e unita',7*4==28 and 2*(7+4)==22 and 9*2==18 and 2*(9+2)==22 and 36/9==4 and 30/6==5 and (26-16)/2==5 and 2*(8+5)==26 and 100**2==10000 and D('0.5')*10000==5000)
check('D: equazioni e problemi',3*5+5==20 and 2*5+4==14 and 4*4+3==19 and 23+18==41 and D('7.50')/3==D('2.50') and D('2.50')*4==10 and 12-5==7 and 24-8==16 and 26-2==24)
dr=json.loads((R/'registro-citazioni-d.json').read_text(encoding='utf-8'))
check('D: citazioni Compendio',len(dr)==6 and all(sha(P/x['file'])==x['sha256'] and 0<x['righe'][0]<=x['righe'][1]<=len((P/x['file']).read_text(encoding='utf-8').split('\\n')) for x in dr))
whole=(R/'manuale.md').read_text(encoding='utf-8')
check('D: confini e adattamenti espliciti',all(s in whole for s in ['non è un periodo di prova obbligatorio prima dell’invio','non è automatico se può esporre il minore a danno','Normattiva ha restituito errore','gentilezza non dipende','Nessun questionario proprietario']))
check('D: niente vecchia chiusura C', 'Questa consegna si ferma alla revisione delle fasi 2–3' not in whole)
check('D: materiali pronti S32–S50',all(x['materiali_pronti'] for x in data if int(x['codice'][1:])>=32))
'''
t=t.replace("report['esito']='PASS'",extra+"\nreport['esito']='PASS'")
(R/'verifica.py').write_text(t,encoding='utf-8')
