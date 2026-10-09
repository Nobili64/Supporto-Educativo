from pathlib import Path
import re

def build_maps(out,pkg,ns,p,e):
    records=[]
    styles=f'''<office:document-styles {ns} office:version="1.3"><office:font-face-decls><style:font-face style:name="Arial" svg:font-family="Arial"/></office:font-face-decls><office:styles>
    <style:default-style style:family="graphic"><style:graphic-properties draw:stroke="solid" svg:stroke-color="#344B58" svg:stroke-width="0.035cm" draw:fill="solid" draw:fill-color="#EEF2F3" draw:textarea-vertical-align="middle" fo:padding-left="0.25cm" fo:padding-right="0.25cm" fo:padding-top="0.2cm" fo:padding-bottom="0.2cm"/><style:text-properties style:font-name="Arial" fo:font-size="14pt" fo:color="#182B35"/></style:default-style>
    <style:style style:name="Box" style:family="graphic"/>
    <style:style style:name="Core" style:family="graphic"><style:graphic-properties draw:fill-color="#DFE8ED" svg:stroke-width="0.06cm"/></style:style>
    <style:style style:name="Blank" style:family="graphic"><style:graphic-properties draw:fill-color="#FFFFFF"/></style:style>
    <style:style style:name="Text" style:family="graphic"><style:graphic-properties draw:stroke="none" draw:fill="none" fo:padding-left="0cm" fo:padding-right="0cm" fo:padding-top="0cm" fo:padding-bottom="0cm"/></style:style>
    <style:style style:name="Label" style:family="graphic"><style:graphic-properties draw:stroke="none" draw:fill="solid" draw:fill-color="#FFFFFF" fo:padding-left="0cm" fo:padding-right="0cm" fo:padding-top="0cm" fo:padding-bottom="0cm"/></style:style>
    <draw:marker draw:name="Arrow" svg:viewBox="0 0 10 10" svg:d="M5 0 L10 10 L0 10 Z"/>
    <style:style style:name="ArrowLine" style:family="graphic"><style:graphic-properties draw:stroke="solid" svg:stroke-width="0.045cm" svg:stroke-color="#344B58" draw:marker-end="Arrow" draw:marker-end-width="0.28cm" draw:marker-end-center="false" draw:fill="none"/></style:style>
    <style:style style:name="Line" style:family="graphic"><style:graphic-properties draw:stroke="solid" svg:stroke-width="0.045cm" svg:stroke-color="#344B58" draw:fill="none"/></style:style>
    <style:style style:name="Title" style:family="paragraph"><style:paragraph-properties fo:text-align="left"/><style:text-properties style:font-name="Arial" fo:font-size="23pt" fo:font-weight="bold" fo:color="#16384B"/></style:style>
    <style:style style:name="Body" style:family="paragraph"><style:paragraph-properties fo:text-align="center" fo:line-height="115%"/><style:text-properties style:font-name="Arial" fo:font-size="14pt" fo:color="#182B35"/></style:style>
    <style:style style:name="Bold" style:family="paragraph" style:parent-style-name="Body"><style:text-properties fo:font-size="16pt" fo:font-weight="bold"/></style:style>
    <style:style style:name="Left" style:family="paragraph" style:parent-style-name="Body"><style:paragraph-properties fo:text-align="left"/></style:style>
    <style:style style:name="Small" style:family="paragraph" style:parent-style-name="Body"><style:text-properties fo:font-size="10pt" fo:color="#566974"/></style:style>
    </office:styles><office:automatic-styles><style:page-layout style:name="A4L"><style:page-layout-properties fo:page-width="29.7cm" fo:page-height="21cm" style:print-orientation="landscape" fo:margin="0cm"/></style:page-layout></office:automatic-styles><office:master-styles><style:master-page style:name="Standard" style:page-layout-name="A4L"/></office:master-styles></office:document-styles>'''

    def text(s,x,y,w,h,kind='Text',para='Body'):
        return f'<draw:frame draw:style-name="{kind}" svg:x="{x}cm" svg:y="{y}cm" svg:width="{w}cm" svg:height="{h}cm"><draw:text-box>{p(s,para)}</draw:text-box></draw:frame>'
    def box(s,x,y,w,h,kind='Box',title=None):
        paras=(p(title,'Bold') if title else '')+p(s)
        return f'<draw:rect draw:style-name="{kind}" svg:x="{x}cm" svg:y="{y}cm" svg:width="{w}cm" svg:height="{h}cm" draw:corner-radius="0.16cm">{paras}</draw:rect>'
    def line(x1,y1,x2,y2,arrow=True):
        return f'<draw:line draw:style-name="{"ArrowLine" if arrow else "Line"}" svg:x1="{x1}cm" svg:y1="{y1}cm" svg:x2="{x2}cm" svg:y2="{y2}cm"/>'
    def label(s,x,y,w,h=1.1):return text(s,x,y,w,h,'Label')
    def start(title,sub):return text(title,1.2,0.65,27.3,1.2,para='Title')+text(sub,1.2,2.0,27.3,1.0,para='Left')
    def footer(note,n=1):return text(note,1.2,18.7,27.3,1.05,para='Left')+text(f'LABORATORIO STUDIO DSA  /  2026-09-28  /  {n}',1.2,20.05,27.3,0.45,para='Small')
    def save(id,title,subject,topic,folder,kind,level,pages):
        folder=Path(folder)
        src=folder/'Modificabili'/(id+'.odg'); pdf=folder/'Studente'/(id+'.pdf')
        (out/pdf).parent.mkdir(parents=True,exist_ok=True)
        body=''.join(f'<draw:page draw:name="Pagina{i+1}" draw:master-page-name="Standard">{body}</draw:page>' for i,body in enumerate(pages))
        para_styles=''.join(re.findall(r'<style:style\b[^>]*style:family="paragraph"[^>]*>.*?</style:style>',styles,re.S))
        content=f'<office:document-content {ns} office:version="1.3"><office:automatic-styles>{para_styles}</office:automatic-styles><office:body><office:drawing>{body}</office:drawing></office:body></office:document-content>'
        pkg(out/src,'graphics',content,styles)
        records.append(dict(id=id,title=title,subject=subject,topic=topic,school='Terza / adattabile',objective={'Mappa concettuale':'Spiegare i legami tra i concetti','Schema operativo':'Scegliere passaggi e controllare il risultato','Schema di circuito':'Leggere un circuito elettrico elementare','Modello':'Costruire e usare un supporto personale'}[kind],kind=kind,level=level,audience='Studente',pdf=pdf.as_posix(),source=src.as_posix(),date='2026-09-28',expected_pages=len(pages)))

    for guided in [False,True]:
        suffix='guidato' if guided else 'esempio'
        b=start('Equazioni: il percorso', 'Completa gli spazi. Poi crea sul tuo foglio uno schema utile a un nuovo esercizio.' if guided else 'Schema operativo. Usa i passaggi che servono e spiega perché conservano le soluzioni.')
        b+=line(9.5,6.4,10.7,6.4)+line(19,6.4,20.2,6.4)+line(24.35,9.4,24.35,11.1,False)+line(24.35,11.1,21.05,11.1,False)+line(21.05,11.1,21.05,12.4)+line(16.9,14.6,12.8,14.6)
        steps=[('1. Leggo','Trovo i due membri\ne l’incognita.'),('2. Semplifico','Distribuisco nelle parentesi.\nSommo i termini simili.'),('3. Mantengo l’equilibrio','Eseguo la stessa operazione\nsu entrambi i membri.\nPer moltiplicare o dividere\nuso un numero diverso da zero.'),('4. Riconosco il caso','ax = b\na diverso da 0: x = b/a\n0x = 0: tutti i numeri reali\n0x = b, b diverso da 0:\nnessuna soluzione'),('5. Controllo','Sostituisco nell’equazione\niniziale e confronto i membri.\nSe non coincidono,\nricontrollo i passaggi.')]
        if guided:
            steps[2]=('3. Mantengo l’equilibrio','Eseguo la stessa operazione\nsu ____________________.\nPer moltiplicare o dividere\nuso un numero diverso da ____.')
            steps[3]=('4. Riconosco il caso','ax = b\na diverso da 0: x = ______\n0x = 0: __________________\n0x = 5: __________________')
            steps[4]=('5. Controllo','Sostituisco nell’equazione\n____________________.\nConfronto i due membri.\nChe cosa verifico?\n________________________')
        for i,(title,s) in enumerate(steps):
            x,y=(1.2+9.5*i,3.8) if i<3 else ((16.9,12.4) if i==3 else (4.5,12.4))
            b+=box(s,x,y,8.3,5.6 if i<3 else 5.5,'Blank' if guided else 'Box',title)
        b+=footer('Gli strumenti restano disponibili. Controlla i completamenti confrontandoli con lo schema di esempio.')
        save('matematica-schema-'+suffix,'Equazioni - schema '+suffix,'Matematica','Equazioni di primo grado','Materie/Matematica/Equazioni di primo grado','Schema operativo','Completamento' if guided else 'Esempio',[b])

    for guided in [False,True]:
        suffix='guidata' if guided else 'esempio'
        pages=[]
        b=start('Prima guerra mondiale: origini e sviluppo','Completa i concetti e leggi ogni freccia come una frase.' if guided else 'Mappa concettuale 1 di 2. Le parole sulle frecce spiegano il rapporto tra i concetti.')
        b+=line(7.2,6.1,11.2,8.0)+line(18.6,8.0,22.6,6.1)+line(11.2,11.0,7.2,13.7)+line(18.6,11.0,22.6,13.7)
        b+=label('contribuiscono\nal contesto della',1.2,6.35,6.0,1.25)+label('ha come evento\nscatenante',22.8,6.35,5.7,1.25)
        b+=label('si sviluppa come',6.3,11.6,5.5)+label('coinvolge anche',18.2,11.6,5.5)
        b+=box('1914-1918',10.35,8,9,3,'Core','Prima guerra mondiale')
        b+=box('Rivalità tra potenze,\nnazionalismi e armamenti' if not guided else 'Rivalità tra potenze,\n____________ e armamenti',1.2,3.6,10,2.5,title='Tensioni precedenti')
        b+=box('28 giugno 1914' if not guided else 'Data: __________________',18.5,3.6,10,2.5,title='Attentato di Sarajevo')
        b+=box('Più fronti, trincee\ne coinvolgimento dei civili' if not guided else 'Più fronti, ____________\ne coinvolgimento dei civili',1.2,13.7,10,3,title='Conflitto esteso')
        b+=box('Maggio 1915' if not guided else 'Maggio ______',18.5,13.7,10,3,title='Italia con l’Intesa')
        b+=footer('Le decisioni politiche estesero il conflitto: il sistema delle alleanze non funzionò come un automatismo.',1)
        pages.append(b)
        b=start('Prima guerra mondiale: fine e conseguenze','Completa usando il testo. Poi spiega la differenza tra armistizio e trattato.' if guided else 'Mappa concettuale 2 di 2. La fine delle ostilità e i trattati sono passaggi distinti.')
        b+=line(8.4,8.5,11.4,6.0)+line(18.4,5.7,21.4,5.7)+line(8.4,10.6,13,14.1)
        b+=label('vede cessare\ni combattimenti con',1.2,5.35,7.0,1.9)+label('sono seguiti\nda',18.55,4.2,2.7,1.3)+label('produce',7.4,12.0,5)
        b+=box('1914-1918',1.2,8,7.2,3,'Core','Prima guerra mondiale')
        b+=box('4 novembre: fronte italiano\n11 novembre: Germania' if not guided else '___ novembre: fronte italiano\n___ novembre: Germania',11.4,4.2,7,3.7,title='Armistizi del 1918')
        b+=box('Versailles:\nGermania, 1919' if not guided else 'Versailles:\nGermania, ______',21.4,4.2,7.1,3.7,title='Trattati di pace')
        b+=box('Perdite umane e materiali;\ncaduta di imperi; nuovi confini' if not guided else 'Perdite umane e materiali;\n________________________\n________________________',10.2,14.1,15,3.4,title='Conseguenze')
        b+=footer('Usa la cronologia del kit per distinguere l’ordine degli eventi. Questa mappa seleziona solo alcuni legami.',2)
        pages.append(b)
        save('storia-mappa-'+suffix,'Prima guerra mondiale - mappa '+suffix,'Storia','Prima guerra mondiale','Materie/Storia/Prima guerra mondiale','Mappa concettuale','Completamento' if guided else 'Esempio',pages)

    for guided in [False,True]:
        suffix='guidata' if guided else 'esempio'
        b=start('Elettricità: grandezze e relazioni','Completa simboli, unità e formula, poi spiega i collegamenti.' if guided else 'Il nostro esempio contiene un generatore, fili conduttori e un resistore ohmico.')
        b+=line(10.5,4.8,5.0,7.0)+line(19.2,4.8,24.8,7.0)+line(5.0,8.8,5.0,11.0)+line(24.8,8.8,24.8,11.0)+line(8.5,12.8,11.3,15.1)+line(21.2,12.8,18.5,15.1)+line(14.85,11.8,14.85,15.1)
        b+=label('comprende un',5.5,5.35,5.3)+label('comprende un',19,5.35,5.3)+label('mantiene una',1.5,9.1,7.1)+label('ha una',21.2,9.1,7.1)
        b+=label('nel circuito chiuso\nsostiene la',4.6,13.25,5.7,1.6)+label('a U costante, se aumenta\nfa diminuire la',19.5,13.3,8.3,1.6)+label('calcola\nI = U / R',11.7,12.3,6.3,1.8)
        b+=box('Circuito chiuso',10.5,3.2,8.7,2.0,'Core')
        b+=box('Generatore',1.5,7.0,7,1.8)+box('Resistore',21.2,7.0,7,1.8)
        b+=box('Tensione U\nvolt (V)' if not guided else 'Tensione ____\nunità: __________',1.5,11,7,2)
        b+=box('Resistenza R\nohm (Ω)' if not guided else 'Resistenza ____\nunità: __________',21.2,11,7,2)
        b+=box('U = R × I' if not guided else 'U = ____ × ____',10.5,9.6,8.7,2.2,title='Legge di Ohm')
        b+=box('Corrente I · ampere (A)' if not guided else 'Corrente ____ · unità: ______',10.5,15.1,8.7,2.0,'Core')
        b+=footer('Legge di Ohm: conduttore ohmico a temperatura costante. I = U/R richiede R ≠ 0; R = U/I richiede I ≠ 0.')
        save('scienze-mappa-'+suffix,'Elettricità - mappa '+suffix,'Scienze','Elettricità','Materie/Scienze/Elettricità','Mappa concettuale','Completamento' if guided else 'Esempio',[b])

    b=start('Un circuito elementare','Schema teorico con generatore ideale, fili ideali e resistore ohmico.')
    for a in [(6,6,23,6),(23,6,23,9.2),(23,11.8,23,15),(23,15,6,15),(6,15,6,10),(6,9.5,6,6),(5.05,9.5,6.95,9.5),(5.5,10,6.5,10)]:b+=line(*a,arrow=False)
    b+=box('',22.2,9.2,1.6,2.6,'Blank')
    b+=text('+',3.9,9.0,1.2,0.7)+text('−',3.9,9.8,1.2,0.7)
    b+=text('Generatore\nU = 12 V',1.2,6.7,4.3,1.7)+text('Resistore\nR = 4 Ω',24.0,9.6,4.5,2.0)
    b+=line(12.2,6,16.4,6)+text('Corrente convenzionale I',9.2,4.5,10.3,1.0)
    b+=box('I = U / R = 12 V / 4 Ω = 3 A',8.8,9.4,11.1,2.3,'Core')
    b+=text('Il percorso è chiuso. Nel circuito esterno la corrente convenzionale va dal polo + al polo −.',5.2,16.0,23,1.7,para='Left')
    b+=footer('Descrivi il percorso completo sul foglio. Per il calcolo assumiamo resistenza costante e fili ideali.')
    save('scienze-circuito','Elettricità - circuito elementare','Scienze','Elettricità','Materie/Scienze/Elettricità','Schema di circuito','Esempio',[b])

    b=start('Costruisco una mappa concettuale','Scrivi una domanda. Inserisci concetti nei riquadri e parole-legame sulle frecce.')
    b+=text('Domanda: __________________________________________________________________',1.2,3.2,27.3,1.1,para='Left')
    b+=line(14.8,7.5,7.5,11.5)+line(14.8,7.5,22.2,11.5)+line(7.5,13.7,7.5,16.0)+line(22.2,13.7,22.2,16.0)
    for a in [(10,5.2,9.6,2.3),(2.7,11.5,9.6,2.2),(17.4,11.5,9.6,2.2),(2.7,16,9.6,2.2),(17.4,16,9.6,2.2)]:b+=box('____________________',*a,'Blank')
    b+=label('parole-legame\n____________________',5.7,9.2,7.4,1.6)+label('parole-legame\n____________________',16.8,9.2,8,1.6)+label('____________________',3.8,14.2,7.3)+label('____________________',18.6,14.2,7.3)
    b+=footer('Leggi ogni collegamento come una frase. Poi rispondi alla domanda usando la mappa; modifica ciò che manca.')
    save('modello-mappa-concettuale','Modello - mappa concettuale','Modelli riutilizzabili','Mappe','Modelli riutilizzabili','Modello','Costruzione',[b])
    b=start('Costruisco una mappa mentale','Parti dall’argomento centrale. Raggruppa idee affini nei rami; aggiungi dettagli utili.')
    b+=line(10.4,9.5,6.2,5.6,False)+line(19.3,9.5,23.5,5.6,False)+line(10.4,11.5,6.2,15.5,False)+line(19.3,11.5,23.5,15.5,False)
    b+=box('Argomento: ______________',10.4,8.7,8.9,3,'Core')
    for a in [(1.2,3.7),(20,3.7),(1.2,14.3),(20,14.3)]:b+=box('Gruppo di idee: _________\n______________________\n______________________',*a,8.5,3.6,'Blank')
    b+=footer('Usa parole o disegni che riconosci. Per spiegare cause e relazioni precise, valuta una mappa concettuale.')
    save('modello-mappa-mentale','Modello - mappa mentale','Modelli riutilizzabili','Mappe','Modelli riutilizzabili','Modello','Costruzione',[b])
    return records
