export const T=(label,text)=>({type:'quote',label,text});
export const M=(label,...lines)=>({type:'math',label,lines});
export const L=(label,...items)=>({type:'list',label,items});
export const N=(stage)=>({type:'notes',stage});
export const G=(kind,stage)=>({type:'map',kind,stage});
export function S(phase,title,text,visual,action,hint){return {phase,title,text:Array.isArray(text)?text:[text],visual,action,hint:hint||'Rileggi la consegna insieme a chi ti accompagna. Indica la parola o il punto che non capisci: puoi fermarti qui e lavorare su quel passaggio prima di continuare.'};}
export const sources=[
 {title:'W3C — Making Content Usable for People with Cognitive and Learning Disabilities',url:'https://www.w3.org/TR/coga-usable/',kind:'Guida istituzionale per il design',note:'Usata la copia HTML fornita dall’utente: parole chiare, istruzioni esplicite, un passo alla volta, contesto disponibile e avanzamento controllato. Non è una certificazione di accessibilità.'},
 {title:'Novak e Cañas — The Theory Underlying Concept Maps',url:'https://cmap.ihmc.us/docs/theory-of-concept-maps',kind:'Riferimento metodologico',note:'Domanda iniziale, concetti e relazioni espresse da parole-legame. Le mappe del prototipo sono esempi originali e semplificati.'},
 {title:'Cornell University — The Cornell Note Taking System',url:'https://lsc.cornell.edu/how-to-study/taking-notes/cornell-note-taking-system/',kind:'Indicazioni didattiche universitarie',note:'L’organizzazione in appunti, domande e sintesi è adattata qui alla scuola media. Questa esercitazione non equivale a una validazione del formato con studenti DSA.'},
 {title:'AID — Che cosa sono i DSA',url:'https://www.aiditalia.org/che-cosa-sono-i-dsa',kind:'Informazione associativa',note:'Riferimento per distinguere lettura, ortografia, grafia e abilità numeriche. Gli aiuti proposti nei singoli passaggi sono adattamenti editoriali da osservare nella pratica.'},
 {title:'Metodo di studio CIU — PDF fornito dall’utente',kind:'Materiale didattico, adattato con esempi originali',note:'Appunti: pp. 22–27. Preparazione alle mappe: pp. 96–100 e 131. Riformulazione e generalizzazione: pp. 208–209. Feedback sul comportamento: p. 210. Rimandi controllati sul PDF e sul testo estratto; la guida AI complementare non è stata assunta come fonte autonoma.'}
];
export const fable='La favola è un racconto breve. I personaggi sono spesso animali che parlano e si comportano come persone. La storia contiene un insegnamento sui comportamenti: questo insegnamento si chiama morale. A volte la morale è scritta chiaramente; altre volte il lettore la ricava da ciò che accade.';
export const adventure='Il racconto d’avventura racconta un’impresa rischiosa. Il protagonista affronta pericoli e ostacoli. I luoghi possono essere lontani o sconosciuti. Gli eventi creano attesa: il lettore vuole scoprire come finirà l’impresa.';
