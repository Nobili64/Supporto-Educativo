// Controllo grossolano della leggibilità dei testi rivolti al ragazzo (indice Gulpease).
// Uso: node leggibilita.mjs   — elenca i testi sotto la soglia ed esce con errore se ce ne sono.
import parafrasi from './parafrasi.mjs';
import equazioni from './equazioni.mjs';
import appunti from './appunti.mjs';
import mappe from './mappe.mjs';
const SOGLIA=60;
const gulpease=t=>{const parole=t.split(/\s+/).filter(Boolean).length,lettere=t.replace(/[^A-Za-zÀ-ÿ]/g,'').length,frasi=Math.max(1,(t.match(/[.?!]/g)||[]).length);return Math.round(89+(300*frasi-10*lettere)/parole);};
const campi=[['testo',s=>s.text.join(' ')],['adesso',s=>s.action],['aiuto',s=>s.hint]];
let totale=0,somma=0;const bassi=[];
for(const c of [parafrasi,equazioni,appunti,...mappe])c.slides.forEach((s,i)=>{for(const [nome,leggi] of campi){const t=leggi(s),g=gulpease(t);totale++;somma+=g;if(g<SOGLIA)bassi.push(`${c.id} passaggio ${i+1} [${nome}] ${g}: ${t}`);}});
console.log(`Testi: ${totale}. Indice medio: ${(somma/totale).toFixed(1)}. Sotto ${SOGLIA}: ${bassi.length}.`);
for(const b of bassi)console.log(b);
process.exitCode=bassi.length?1:0;
