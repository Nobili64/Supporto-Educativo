from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
GROUPS=[
('ITA','Italiano',['Comprensione e inferenze','Sintesi','Pianificazione e revisione della scrittura','Analisi grammaticale','Analisi logica','Analisi del periodo']),
('MAT','Matematica',['Numeri e frazioni','Espressioni, potenze e radici','Rapporti, proporzioni e percentuali','Algebra ed equazioni','Geometria piana e Pitagora','Solidi','Piano cartesiano e proporzionalità','Statistica e probabilità']),
('STO','Storia',['Società medievale','Rinascimento e Riforma','Rivoluzioni e formazione dell’Italia unita','Prima guerra mondiale','Totalitarismi e Seconda guerra mondiale','Dopoguerra e Italia repubblicana']),
('SCI','Scienze',['Materia e trasformazioni','Viventi ed ecosistemi','Corpo umano','Genetica ed evoluzione','Terra e Universo','Elettricità ed energia']),
('GEO','Geografia',['Carte, scale e orientamento','Paesaggi e climi','Territori, popolazioni ed economie']),
('ENG','Inglese',['Costruzione della frase','Tempi verbali e connettori frequenti','Comprensione e produzione scritta e orale']),
('FRA','Francese',['Strutture di base e lessico','Comprensione e produzione scritta e orale']),
('SPA','Spagnolo',['Strutture di base e lessico','Comprensione e produzione scritta e orale']),
('TEC','Tecnologia',['Materiali e processi','Energia e sostenibilità','Lettura e costruzione del disegno tecnico']),
('ART','Arte e immagine',['Lettura di un’opera','Confronto e contesto di opere e periodi']),
('MUS','Musica',['Ritmo e notazione essenziale','Ascolto guidato e descrizione di un brano']),
('MOT','Educazione fisica',['Movimento, salute e regole sportive']),
('CIV','Educazione civica',['Costituzione e istituzioni','Cittadinanza digitale','Sostenibilità e responsabilità'])]
KITS={f'{prefix}{i:02}':dict(id=f'{prefix}{i:02}',subject=subject,title=title) for prefix,subject,titles in GROUPS for i,title in enumerate(titles,1)}
assert len(KITS)==47
EXISTING={'MAT04':'Equazioni di primo grado','STO04':'Prima guerra mondiale','SCI06':'Elettricità'}
def folder(kid):
    k=KITS[kid]
    return Path('Materie')/k['subject']/EXISTING.get(kid,k['title'])
if __name__=='__main__':
    (ROOT/'Manutenzione/copertura-prevista.json').write_text(json.dumps(list(KITS.values()),ensure_ascii=False,indent=2),encoding='utf-8')
