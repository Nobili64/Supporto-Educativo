const DATA=JSON.parse(document.getElementById('data').textContent),courses=DATA.courses;
const tasks=courses.filter(c=>c.kind==='task'),mapCourses=courses.filter(c=>c.kind==='map');
const app=document.getElementById('app');
const state={route:[],course:null,index:0,view:'choose',large:false,returnView:'choose',lessonScroll:0,query:''};
const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const p=s=>`<p>${e(s)}</p>`;
const button=(label,action,value='',cls='')=>`<button type="button" class="${cls}" data-action="${action}" data-value="${e(value)}">${e(label)}</button>`;
const course=()=>courses.find(c=>c.id===state.course);
const backLabel=()=>state.returnView==='help'?'Torna alla spiegazione':state.course?'Torna al percorso':'Torna alla scelta';
const ordered=(names,all)=>all.filter(n=>names.includes(n));
function choice(label,action,value,description=''){return `<button type="button" class="choice" aria-label="${e(label)}" data-action="${action}" data-value="${e(value)}"><span><span class="choice-title">${e(label)}</span>${description?`<span class="choice-sub">${e(description)}</span>`:''}</span><span class="choice-arrow" aria-hidden="true">→</span></button>`;}
function render(focus=true,focusAction=''){
 document.documentElement.classList.toggle('large',state.large);
 if(state.view==='print'){app.innerHTML=printView();}
 else {
  const content=state.view==='lesson'?lesson():state.view==='help'?help():state.view==='menu'?menu():state.view==='coach'?coach():state.view==='search'?search():chooser();
  const subtitle=state.course?course().title:`${tasks.length} lavori e ${mapCourses.length} mappe per imparare un metodo`;
  app.innerHTML=`<header class="topbar"><div class="brand"><strong>Un passo alla volta</strong><span>${e(subtitle)}</span></div>${state.view!=='menu'?button('Menu','menu'):''}</header><div class="shell"><main id="main" tabindex="-1">${content}</main></div>${state.view==='lesson'?navigation():''}`;
 }
 if(state.view==='search')updateResults();
 if(focus){const target=focusAction?app.querySelector(`[data-action="${focusAction}"]`):state.view==='search'?app.querySelector('#cerca'):app.querySelector('h1');if(target){if(!focusAction&&state.view!=='search')target.setAttribute('tabindex','-1');if(focusAction==='help')app.querySelector('main').scrollTop=state.lessonScroll;target.focus({preventScroll:true});if(focusAction)target.scrollIntoView({block:'nearest'});}window.scrollTo(0,0);}
}
function areasOf(list,subject){const s=DATA.subjects.find(x=>x.name===subject);return ordered([...new Set(list.filter(c=>c.subject===subject).map(c=>c.area))],s?s.areas:[]);}
function chooser(){
 const r=state.route;let title='Da che cosa vuoi partire?',intro='Scegli un lavoro. Guarda un esempio, poi prova sul foglio. Puoi fermarti e tornare indietro in ogni momento.',choices='';
 if(!r.length){choices=choice('Affronta un compito','pick','tasks','Scegli la materia e il lavoro che devi fare.')+choice('Costruisci una mappa','pick','maps','Mappe concettuali e mappe mentali, con un esempio per materia.')+choice('Cerca un percorso','search','','Scrivi una parola del compito oppure un codice.');}
 else if(r[0]==='tasks'){
  const subjects=DATA.subjects.map(s=>s.name).filter(s=>tasks.some(c=>c.subject===s));
  if(r.length===1){title='Scegli la materia';intro='Quale materia riguarda il compito?';choices=subjects.map(s=>choice(s,'pick',s)).join('');}
  else{
   const areas=areasOf(tasks,r[1]),area=r[2]||(areas.length===1?areas[0]:null);
   if(!area){title='Scegli l’ambito';intro=`Materia scelta: ${r[1]}.`;choices=areas.map(a=>choice(a,'pick',a)).join('');}
   else{title='Scegli il lavoro';intro=`${r[1]} · ${area}`;choices=tasks.filter(c=>c.subject===r[1]&&c.area===area).map(c=>choice(c.title,'open',c.id,c.intro)).join('');}
  }
 } else {
  const types=['Mappa concettuale','Mappa mentale'];
  if(r.length===1){title='Scegli il tipo di mappa';intro='Le due mappe organizzano le informazioni in modo diverso.';choices=choice(types[0],'pick',types[0],'Collegamenti da leggere come frasi.')+choice(types[1],'pick',types[1],'Un tema al centro, con rami e dettagli.');}
  if(r.length===2){title='Scegli la materia';intro=`Tipo scelto: ${r[1]}.`;choices=DATA.subjects.map(s=>s.name).filter(s=>mapCourses.some(c=>c.mapType===r[1]&&c.subject===s)).map(s=>choice(s,'pick',s)).join('');}
  if(r.length===3){title='Scegli l’argomento';intro=`${r[2]} · ${r[1]}`;choices=mapCourses.filter(c=>c.mapType===r[1]&&c.subject===r[2]).map(c=>choice(c.topic,'open',c.id,c.intro)).join('');}
 }
 return `<section class="paper"><p class="kicker">Scegli il percorso</p><h1>${e(title)}</h1><p class="intro">${e(intro)}</p><div class="choices">${choices}</div>${r.length?`<div class="simple-back">${button('Indietro','route-back')}</div>`:''}</section>`;
}
const plain=s=>String(s).toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[’']/g,' ');
function matches(q){const words=plain(q).split(/\s+/).filter(Boolean);if(!words.length)return [];return courses.filter(c=>{const hay=plain([c.id,c.title,c.subject,c.area,c.mapType,c.topic,c.intro].filter(Boolean).join(' '));return words.every(w=>hay.includes(w));}).slice(0,25);}
function search(){return `<section class="paper"><p class="kicker">Cerca un percorso</p><h1>Che cosa stai cercando?</h1><label class="search-label" for="cerca">Scrivi una parola del compito oppure il codice stampato sulla scheda. Per esempio: riassunto, frazioni, M02-02.</label><input id="cerca" class="search-input" type="search" autocomplete="off" spellcheck="false" value="${e(state.query)}"><p class="small" id="esito" aria-live="polite"></p><div class="choices" id="risultati"></div><div class="simple-back">${button('Indietro','search-back')}</div></section>`;}
function updateResults(){const box=app.querySelector('#risultati'),info=app.querySelector('#esito');if(!box)return;const found=matches(state.query);box.innerHTML=found.map(c=>choice(c.title,'open',c.id,c.kind==='map'?`${c.mapType} · ${c.subject}`:`${c.subject} · ${c.area} · ${c.id}`)).join('');info.textContent=!state.query.trim()?'':found.length?`Percorsi trovati: ${found.length}.`:'Nessun percorso trovato. Prova con un’altra parola.';}
function lesson(){const c=course(),s=c.slides[state.index];return `<article class="paper slide" data-index="${state.index}" data-total="${c.slides.length}"><p class="kicker">${e(s.phase)}</p><h1>${e(s.title)}</h1><div class="copy">${s.text.map(p).join('')}</div>${visual(s.visual,c)}<p class="action"><span class="action-label">Adesso</span>${e(s.action)}</p>${button('Mi serve una spiegazione','help','','help-link')}</article>`;}
function navigation(){const n=course().slides.length;return `<nav class="navigation" aria-label="Passaggi del percorso"><div class="navigation-inner">${button('Indietro','prev')}<span class="counter">Passaggio ${state.index+1} di ${n}</span>${button(state.index===n-1?'Concludi':'Avanti',state.index===n-1?'finish':'next','','primary')}</div></nav>`;}
function help(){const c=course(),s=c.slides[state.index];return `<section class="paper"><p class="kicker">Una spiegazione in più</p><h1>${e(s.title)}</h1>${p(s.hint)}${visual(s.visual,c)}${button('Torna al passaggio','help-back','','primary')}</section>`;}
function menu(){return `<section class="paper"><p class="kicker">Strumenti</p><h1>Che cosa ti serve?</h1><div class="choices menu-list">${choice(backLabel(),'return','')}${state.course?choice('Schede da stampare','print',''):''}${choice('Guida per il professionista','coach','')}${choice(state.large?'Testo normale':'Testo più grande','size','')}${state.course?choice('Scegli un altro percorso','home',''):''}</div><p class="small">Il file funziona senza Internet. Le scelte restano solo durante questa apertura: non vengono salvati nomi, risposte o progressi.</p></section>`;}
function coach(){
 const c=course();if(!c)return `<section class="paper"><h1>Guida per il professionista</h1><p>Apri prima un percorso: nel suo menu trovi la guida con preparazione, aiuti e controlli. Le indicazioni per l’adulto sono separate dalle schermate dello studente.</p><p>Puoi anche cercare un percorso per parola o per codice.</p>${button('Cerca un percorso','search','','primary')} ${button('Torna alla scelta','return')}</section>`;
 const g=c.coach;return `<article class="paper coach-print"><p class="kicker">Guida per il professionista · ${e(c.id)}</p><h1>${e(c.title)}</h1><div class="screen-only print-tools">${button(backLabel(),'return','','primary')}${button('Stampa questa guida','print-now')}</div><h2>Che cosa insegnare</h2>${p(g.goal)}<h2>Preparare l’incontro</h2>${p(g.prepare)}${g.scripts&&g.scripts.length?`<h2>Testi per la lettura</h2>${g.scripts.map(s=>`<section class="coach-section"><h3>${e(s.title)}</h3>${p(s.instruction)}<div class="script">${p(s.text)}</div></section>`).join('')}`:''}<h2>Osservare il procedimento</h2>${p(g.observe)}<h2>Aiuti da scegliere sul compito</h2><p>Le associazioni con i DSA indicano possibilità da osservare, non assegnazioni automatiche. Gli strumenti compensativi necessari restano disponibili anche quando si riducono i suggerimenti didattici.</p>${g.adaptations.map(a=>`<section class="coach-adapt"><h3>${e(a[0])}</h3><p><strong>Osservare:</strong> ${e(a[1])}</p><p><strong>Provare e verificare:</strong> ${e(a[2])}</p></section>`).join('')}<h2>Verificare la comprensibilità</h2>${observation()}<p>Osservare lo strumento, non valutare lo studente. Annotare quale consegna ha richiesto una riformulazione e quale aiuto ha permesso di proseguire. Non è previsto registrare dati personali nel file.</p><h2>Fonti e limiti</h2><p>Le sequenze, i testi e gli esempi sono elaborazioni editoriali originali. Le fonti sostengono i principi indicati; non certificano questi percorsi.${g.checks?' '+e(g.checks):''}</p>${sources(g.sources)}<p class="small">La comprensibilità con studenti reali resta da osservare negli incontri.</p></article>`;
}
function sources(ids){return `<ul class="source-list">${ids.map(i=>{const s=DATA.sources[i];if(!s)return '';const label=s.url?`<a href="${e(s.url)}" target="_blank" rel="noopener noreferrer">${e(s.title)}</a>`:`<strong>${e(s.title)}</strong>`;return `<li>${label}<p class="small">${e(s.kind)}. ${e(s.note)}</p></li>`}).join('')}</ul>`;}
function observation(){return `<table class="observation"><thead><tr><th>Osservazione</th><th>Da annotare sul foglio</th></tr></thead><tbody>${['Capisce che cosa fare?','Trova le informazioni nella schermata?','Inizia senza una riformulazione?','Il controllo lo aiuta a correggere?','Riprende il metodo su un compito diverso?'].map(t=>`<tr><td>${e(t)}</td><td>Passaggio / aiuto utile:</td></tr>`).join('')}</tbody></table>`;}
function visual(v,c){
 if(!v)return '';
 if(v.type==='notes')return `<figure class="visual">${notes(v)}</figure>`;
 if(v.type==='map')return `<figure class="visual map-wrap">${mapFigure(c.maps[v.map],v.show,v.focus)}</figure>`;
 let body='';
 if(v.type==='quote')body=`<p class="quote">${e(v.text)}</p>`;
 else if(v.type==='math')body=`<div class="math-lines">${v.lines.map(t=>`<div>${e(t)}</div>`).join('')}</div>`;
 else if(v.type==='list')body=`<ul>${v.items.map(t=>`<li>${e(t)}</li>`).join('')}</ul>`;
 else if(v.type==='table')body=`<div class="table-wrap"><table class="data-table"><thead><tr>${v.columns.map(t=>`<th scope="col">${e(t)}</th>`).join('')}</tr></thead><tbody>${v.rows.map(r=>`<tr>${r.map((t,i)=>i===0?`<th scope="row">${e(t)}</th>`:`<td>${e(t)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
 else if(v.type==='timeline')body=`<ol class="timeline">${v.events.map(x=>`<li><span class="when">${e(x.when)}</span><span class="what">${e(x.what)}</span></li>`).join('')}</ol>`;
 return `<section class="visual"><p class="visual-label">${e(v.label)}</p>${body}</section>`;
}
function notes(v){
 const blank='<div class="note-line"></div>',lines=(list,n)=>list&&list.length?list.map(p).join(''):blank.repeat(n);
 const f=v.focus||'';
 return `<div class="note-sheet" aria-label="Pagina di appunti a due colonne"><div class="note-heading">${e(v.title||'Titolo della lezione: …')}</div><div class="note-columns"><div class="note-col ${f==='questions'?'note-active':''}"><b>DOMANDE · DOPO</b>${lines(v.questions,2)}</div><div class="note-col ${f==='notes'?'note-active':''}"><b>APPUNTI · DURANTE</b>${lines(v.notes,2)}</div></div><div class="note-summary ${f==='summary'?'note-active':''}"><b>IN POCHE PAROLE · DOPO</b>${v.summary?p(v.summary):blank}</div></div>`;
}
/* Mappe: il disegno si calcola dall'elenco dei nodi; i nodi compaiono nell'ordine dell'elenco. */
function wrapWords(text,max){const lines=[''];for(const w of String(text).split(' ')){const i=lines.length-1;if(lines[i]&&(lines[i]+' '+w).length>max)lines.push(w);else lines[i]+=(lines[i]?' ':'')+w;}return lines;}
function tree(def){const nodes=def.nodes.map((n,i)=>({...n,order:i,kids:[]})),by=Object.fromEntries(nodes.map(n=>[n.id,n]));for(const n of nodes)if(n.parent)by[n.parent].kids.push(n);const root=nodes.find(n=>!n.parent);(function depth(n,d){n.depth=d;n.kids.forEach(k=>depth(k,d+1));})(root,0);return {nodes,by,root};}
function nodeBox(n,maxChars,charW,lineH,minW){const lines=wrapWords(n.label,maxChars),w=Math.max(minW,Math.max(...lines.map(l=>l.length))*charW+34),h=lines.length*lineH+22;return {lines,w,h};}
function layoutConcept(t){
 for(const n of t.nodes)Object.assign(n,nodeBox(n,16,12.2,27,130));
 const gap=36,levelGap=112,maxH=Math.max(...t.nodes.map(n=>n.h));
 const sw=n=>n.sw??(n.sw=Math.max(n.w,n.kids.reduce((s,k)=>s+sw(k),0)+gap*Math.max(0,n.kids.length-1)));
 (function place(n,left){n.x=left+sw(n)/2;n.y=n.depth*(maxH+levelGap)+n.h/2;let x=left+(sw(n)-(n.kids.reduce((s,k)=>s+sw(k),0)+gap*Math.max(0,n.kids.length-1)))/2;for(const k of n.kids){place(k,x);x+=sw(k)+gap;}})(t.root,0);
 return {width:sw(t.root)};
}
function layoutMental(t){
 for(const n of t.nodes)Object.assign(n,nodeBox(n,15,12.2,27,120));
 const GAPY=14,GAPX=56,BRANCH=30;
 const bh=n=>n.bh??(n.bh=Math.max(n.h,n.kids.reduce((s,k)=>s+bh(k),0)+GAPY*Math.max(0,n.kids.length-1)));
 const place=(n,edge,top,dir)=>{n.x=edge+dir*n.w/2;n.y=top+bh(n)/2;const inner=n.kids.reduce((s,k)=>s+bh(k),0)+GAPY*Math.max(0,n.kids.length-1);let y=top+(bh(n)-inner)/2;for(const k of n.kids){place(k,n.x+dir*(n.w/2+GAPX),y,dir);y+=bh(k)+GAPY;}};
 const r=t.root;r.x=0;r.y=0;
 for(const dir of [1,-1]){const side=r.kids.filter((_,i)=>(i%2===0)===(dir===1));const total=side.reduce((s,b)=>s+bh(b),0)+BRANCH*Math.max(0,side.length-1);let y=-total/2;for(const b of side){place(b,dir*(r.w/2+GAPX+20),y,dir);y+=bh(b)+BRANCH;}}
 const minX=Math.min(...t.nodes.map(n=>n.x-n.w/2));for(const n of t.nodes)n.x-=minX-10;
 const minY=Math.min(...t.nodes.map(n=>n.y-n.h/2));for(const n of t.nodes)n.y-=minY;
 return {width:Math.max(...t.nodes.map(n=>n.x+n.w/2))+10};
}
function layoutOutline(t,concept){
 const order=[];(function walk(n){order.push(n);n.kids.forEach(walk);})(t.root);let y=8;
 for(const n of order){n.x0=10+n.depth*30;const w=340-n.x0-8;Object.assign(n,nodeBox(n,Math.max(8,Math.floor((w-30)/11)),11,25,0));n.w=w;if(n.depth>0&&concept)y+=30;n.y0=y;n.x=n.x0+n.w/2;n.y=y+n.h/2;y+=n.h+14;}
 return {width:340,height:y};
}
function mapSvg(def,show,focus,narrow){
 const concept=def.type==='concettuale',t=tree(def),limit=show??t.nodes.length,vis=n=>n.order<limit;
 const L=narrow?layoutOutline(t,concept):concept?layoutConcept(t):layoutMental(t);
 const marker=`freccia-${def.id||'m'}-${narrow?'s':'l'}-${limit}`;let paths='',boxes='';
 for(const n of t.nodes){if(!n.parent||!vis(n))continue;const pa=t.by[n.parent];
  if(narrow){const xL=pa.x0+14,yTop=pa.y0+pa.h;paths+=`<path d="M ${xL} ${yTop} L ${xL} ${n.y} L ${n.x0-2} ${n.y}" fill="none" stroke="#55776a" stroke-width="2.5"${concept?` marker-end="url(#${marker})"`:''}/>`;if(concept)paths+=`<text x="${n.x0+4}" y="${n.y0-8}" font-size="19" font-style="italic" fill="#243f37">${e(n.link)}</text>`;}
  else if(concept){const top=n.y-n.h/2,bus=top-58;paths+=`<path d="M ${pa.x} ${pa.y+pa.h/2} L ${pa.x} ${bus} L ${n.x} ${bus} L ${n.x} ${top-3}" fill="none" stroke="#55776a" stroke-width="2.5" marker-end="url(#${marker})"/>`;const lw=Math.max(60,String(n.link).length*11.5+18);paths+=`<rect x="${n.x-lw/2}" y="${top-46}" width="${lw}" height="30" rx="5" fill="#f2f6f3"/><text x="${n.x}" y="${top-24}" text-anchor="middle" font-size="21" fill="#243f37">${e(n.link)}</text>`;}
  else paths+=`<line x1="${pa.x}" y1="${pa.y}" x2="${n.x}" y2="${n.y}" stroke="#55776a" stroke-width="4"/>`;}
 for(const n of t.nodes){if(!vis(n))continue;const x=n.x-n.w/2,y=n.y-n.h/2,sel=focus===n.id,fs=narrow?19:22;
  boxes+=`<g data-node="${e(n.id)}"${sel?' class="selected"':''}><rect x="${x}" y="${y}" width="${n.w}" height="${n.h}" rx="${concept?9:24}" fill="${n.depth===0?'#deecdf':sel?'#fff4dc':'white'}" stroke="${sel?'#b75216':'#426b5d'}" stroke-width="${sel?4:2}"/>${n.lines.map((l,j)=>`<text x="${narrow?x+14:n.x}" y="${y+11+(j+1)*(narrow?25:27)-6}"${narrow?'':' text-anchor="middle"'} font-family="Arial, sans-serif" font-size="${fs}" fill="#203a30">${e(l)}</text>`).join('')}</g>`;}
 const shown=t.nodes.filter(vis),minY=Math.min(...shown.map(n=>(narrow?n.y0:n.y-n.h/2)-(n.depth&&concept?(narrow?32:60):0)))-12,maxY=Math.max(...shown.map(n=>n.y+n.h/2))+12;
 return `<svg class="${narrow?'map-narrow':'map-wide'}" data-map="${e(def.type)}" viewBox="0 ${minY} ${L.width} ${maxY-minY}" role="img" aria-label="${e(def.type==='concettuale'?'Mappa concettuale. ':'Mappa mentale. ')}${e(mapSentences(t,limit).join(' '))}"><defs><marker id="${marker}" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="none" stroke="#55776a" stroke-width="1"/></marker></defs>${paths}${boxes}</svg>`;
}
function mapSentences(t,limit){const out=[];for(const n of t.nodes){if(!n.parent||n.order>=limit)continue;const pa=t.by[n.parent];out.push(n.link?`${pa.label} → ${n.link} → ${n.label}.`:`${pa.label} → ${n.label}.`);}if(!out.length)out.push(`${t.root.label}.`);return out;}
function mapFigure(def,show,focus){const t=tree(def),limit=show??t.nodes.length;return mapSvg(def,show,focus,false)+mapSvg(def,show,focus,true)+`<details class="map-text"><summary>Leggi la mappa in parole</summary><ul>${mapSentences(t,limit).map(s=>`<li>${e(s)}</li>`).join('')}</ul></details>`;}
function printView(){const c=course(),d=c.print;return `<main class="print-view" id="main"><div class="print-tools">${button(backLabel(),'return')}${button('Stampa o salva PDF','print-now','','primary')}</div><section class="print-page"><p class="page-id">${e(c.id)} · Modello · 1 / 3</p><h1>${e(c.title)}</h1><h2>${e(d.modelTitle)}</h2>${d.visual?visual(d.visual,c):''}${d.model.map(p).join('')}<p class="small">Tieni il modello a disposizione mentre lavori. Gli strumenti e gli aiuti necessari restano disponibili.</p></section><section class="print-page"><p class="page-id">${e(c.id)} · Prove sul foglio · 2 / 3</p><h1>Ora prova tu</h1>${d.practice.map(a=>`<section class="practice-item"><h2>${e(a[0])}</h2><p class="quote">${e(a[1])}</p>${d.blankNotes?'':'<div class="writing-space"></div>'}</section>`).join('')}${d.blankNotes?notes({}):''}<p class="small">Lavora su questa traccia o su un foglio più grande. Usa la pagina seguente quando vuoi controllare.</p></section><section class="print-page"><p class="page-id">${e(c.id)} · Controllo e casa · 3 / 3</p><h1>Controlla e riprendi</h1><h2>Soluzioni e criteri</h2>${d.answers.map(p).join('')}<h2>Il metodo per casa</h2><ol>${d.home.map(t=>`<li>${e(t)}</li>`).join('')}</ol><h2>Che cosa ti ha aiutato?</h2><p>Scrivi o racconta quale passaggio vorresti riprovare e quale aiuto vuoi tenere a disposizione.</p><div class="writing-space"></div><p class="small">Esempi originali. Queste pagine servono per esercitarsi: non sono una verifica.</p></section></main>`;}
app.addEventListener('input',event=>{if(event.target.id==='cerca'){state.query=event.target.value;updateResults();}});
app.addEventListener('click',event=>{const target=event.target.closest('button[data-action]');if(!target)return;const a=target.dataset.action,v=target.dataset.value;
 switch(a){case 'pick':state.route.push(v);break;case 'route-back':state.route.pop();break;case 'search':state.course=null;state.view='search';state.returnView='choose';break;case 'search-back':state.view='choose';break;case 'open':state.course=v;state.index=0;state.view='lesson';state.returnView='lesson';break;case 'next':state.index=Math.min(state.index+1,course().slides.length-1);break;case 'prev':if(state.index>0)state.index--;else {state.view='choose';state.course=null;}break;case 'help':state.lessonScroll=app.querySelector('main').scrollTop;state.view='help';break;case 'help-back':state.view='lesson';render(true,'help');return;case 'menu':state.returnView=state.view;state.view='menu';break;case 'return':state.view=state.course?(state.returnView==='help'?'help':'lesson'):(state.returnView==='search'?'search':'choose');break;case 'size':state.large=!state.large;render(true,'size');return;case 'coach':state.view='coach';break;case 'print':state.view='print';break;case 'print-now':window.print();return;case 'home':case 'finish':state.course=null;state.index=0;state.route=[];state.view='choose';state.returnView='choose';break;default:return;}render();
});
render(false);
