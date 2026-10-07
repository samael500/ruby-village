import './style.css';
import {sceneLayout} from './scene-layout.ts';
import {artUrl,backdrop,scenery,stoneDetail,drawGrid,drawInstanceEdges} from './level-art.ts';
import {type Hex, boardCells, key, hexCenter, pixelHex, rotate} from './hex.ts';
import {pieceById as lookupPiece, placedCells as cellsForPiece, validPlacement, terrainAt, winningPath, type Layout} from './game.ts';
import {levels,sandbox} from './levels.ts';
import {chapter,storyFor,invitation,ending,type Dialogue} from './story.ts';
import type {Level} from './model.ts';
import {loadState,saveProgress,completeLevel,available,type StorageLike} from './progress.ts';

const app = document.querySelector<HTMLDivElement>('#app')!;
app.innerHTML = `
<header><button id="scene-back" hidden aria-label="Вернуться на карту"></button><div class="brand"><span class="ruby" aria-hidden="true">◆</span><h1>Рубиновая деревня<span class="sr-only"> · первая глава</span></h1></div><span id="scene-event" hidden></span><div id="status" role="status" aria-live="polite">Выбери плиту, затем клетку.</div><button id="scene-help" hidden aria-label="Как играть">?</button></header>
<div class="portrait">↻ Поверни телефон — поле станет крупнее</div>
<section id="chapter-map" aria-label="Карта первой главы">
<div class="map-intro"><span class="ruta-small" aria-hidden="true">◆</span><p>Дороги исчезают… Поможем Руте вернуть их?</p></div>
<div class="map-landscape"><svg id="map-background" viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true"><path d="M 15 170 Q 300 230 480 190 T 980 200" fill="none" stroke="#a4c4bd" stroke-width="25"/><path d="M 90 360 L 120 325 L 150 360 M 760 20 L 790 55 L 820 20" fill="none" stroke="#789065" stroke-width="12"/></svg><svg id="map-roads" viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true"></svg><div id="map-places"></div></div>
<div class="map-actions"><button id="sandbox-open">⬡ Песочница</button><span id="save-status" role="status"></span><button id="chapter-ending" hidden>✦ Письма через лес</button><button id="letter-open" hidden>✉ Приглашение</button><button id="reset-open">Начать главу заново</button></div>
</section>
<main id="field"><svg id="board" role="group" aria-label="Гексагональное поле. Деревня слева, мельница справа"></svg></main>
<footer id="game-controls">
<div id="tray" aria-label="Набор фигур"></div>
<div id="selection-actions" hidden>
<button id="other"><b>‹</b><span>Другие плиты</span></button><button id="selected-drag" aria-label="Перетащить выбранную фигуру" hidden></button>
<button id="left" aria-label="Повернуть влево"><b>↶</b><span>Влево</span></button>
<button id="right" aria-label="Повернуть вправо"><b>↷</b><span>Вправо</span></button>
<button id="place" class="primary"><b>＋</b><span>Поставить</span></button>
<button id="return"><b>↥</b><span>В набор</span></button></div>
<button id="check" class="check"><b>⚑</b><span>Проверить дорогу</span></button>
<button id="undo" aria-label="Отменить последнее действие"><b>↩</b><span>Отменить</span></button>
<button id="settings-open" aria-label="Настройки" aria-haspopup="dialog"><b>⚙</b><span>Настройки</span></button>
</footer>
<dialog id="settings-panel" aria-labelledby="settings-title">
<div class="dialog-heading"><h2 id="settings-title">Настройки площадки</h2><button id="settings-close" aria-label="Закрыть настройки">✕</button></div>
<div class="settings"><label id="size-setting">Размер поля<select id="size" aria-label="Размер поля"><option value="7,5">7 × 5 — крупнее</option><option value="9,6" selected>9 × 6</option><option value="11,7">11 × 7 — мельче</option></select></label>
<label>Управление<select id="mode" aria-label="Режим управления"><option value="select">Выбрать и поставить</option><option value="drag">Перетаскивать</option></select></label></div>
<p id="metric"></p><p id="hint">Выбери плиту → клетку → «Поставить»</p>
<p class="settings-note">Смена размера очищает поле. Поворот телефона сохраняет плиты.</p>
<div class="settings-actions"><button id="map-return">На карту</button><button id="clear">Начать уровень заново</button><button id="story-replay">Реплики</button><button id="fullscreen" hidden>Полный экран</button></div>
</dialog>
<dialog id="story" aria-labelledby="story-title"><div class="story-layout">
<svg class="ruta-portrait" viewBox="0 0 100 110" role="img" aria-label="Условный портрет Руты: русые волосы и красный платок">
<path d="M20 68V32C20 0 80 0 80 32V75" fill="#b39058"/><path d="M21 110V82Q50 59 79 82V110" fill="#6c8853"/>
<ellipse cx="50" cy="40" rx="24" ry="29" fill="#f1d2a6"/><path d="M24 33Q30 2 62 14L76 37Q59 27 52 17Q43 32 24 33" fill="#b39058"/>
<circle cx="41" cy="40" r="3" fill="#5688ab"/><circle cx="60" cy="40" r="3" fill="#5688ab"/>
<path d="M44 54Q51 60 58 53" fill="none" stroke="#8c5b43" stroke-width="2"/><path d="M26 71L69 68L56 90L43 77L29 99" fill="#b34f56"/>
<path d="M67 82L84 100" stroke="#725440" stroke-width="6"/><rect x="69" y="94" width="23" height="15" rx="3" fill="#a27a4c"/>
</svg><div><p class="eyebrow">Рута · первая глава</p><h2 id="story-title"></h2><p id="story-text"></p></div></div><div class="story-buttons"><button id="story-skip">Пропустить</button><button id="story-action" class="primary">В путь →</button></div></dialog>
<dialog id="help-panel" aria-labelledby="help-title"><h2 id="help-title">Проложи дорогу от дома до калитки</h2><p>Выбери плиту → клетку → «Поставить». Поворачивай плиты, чтобы они поместились. Когда дорога готова, нажми «Проверить».</p><button id="help-close">Понятно</button></dialog>
<dialog id="reset-dialog" aria-labelledby="reset-title"><h2 id="reset-title">Начать главу заново?</h2><p>Все восемь дорог на карте снова исчезнут.</p><div class="settings-actions"><button id="reset-cancel">Оставить дороги</button><button id="reset-confirm">Да, начать заново</button></div></dialog>`;
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const svg = document.getElementById('board') as unknown as SVGSVGElement;
let level:Level=sandbox();
let pieces=level.pieces;
const pieceById=(id:string)=>lookupPiece(id,pieces);
const placedCells=(id:string,p:Layout[string])=>cellsForPiece(id,p,pieces);
let screen:'map'|'game'='map';
let phase:'intro'|'playing'|'walking'|'won'='playing';
let storage:StorageLike|undefined;
const artCheck=import.meta.env.DEV && new URLSearchParams(location.search).has('art-check');
try {if(!artCheck)storage=window.localStorage;} catch { /* Private browsing may deny storage access. */ }
const loaded=loadState(storage);
let completed=loaded.completed,introSeen=loaded.introSeen,storageAvailable=!!storage;
function persist(){storageAvailable=saveProgress(completed,storage,introSeen);}
let firstVictory=false, victoryAt=0;
let route:Hex[]=[], journey=0, frame=0;
let cols = 9, rows = 6, layout: Layout = {}, history: Layout[] = [];
let selected: string | null = null, anchor: Hex | null = null, turns = 0;
// Once clicked, keep the destination while the pointer travels to the controls.
let anchorPinned = false;
let mode = 'select', path = new Set<string>();
let radius = 20, origin = {x:0,y:0};
let drag: {pointer: number; startX: number; startY: number; moved: boolean; beforeAnchor: Hex | null; beforeTurns: number} | null = null;
let suppressClick = false, deferDock = false, dockFrame = 0;
// The dock changes under a released pointer. Consume its synthetic click so it
// cannot activate a different button; the next real gesture starts afresh.
app.addEventListener('pointerdown',()=>{suppressClick=false;},true);
app.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' ')suppressClick=false;},true);
app.addEventListener('click',e=>{
  if(drag||suppressClick){suppressClick=false;e.preventDefault();e.stopImmediatePropagation();}
  else suppressClick=false;
},true);
const ns = 'http://www.w3.org/2000/svg';
function el(tag: string, attrs: Record<string,string|number>, parent: Element, text?: string) {
  const node = document.createElementNS(ns,tag);
  for (const [k,v] of Object.entries(attrs)) node.setAttribute(k,String(v));
  if (text !== undefined) node.textContent = text;
  parent.append(node); return node;
}
function polygon(h: Hex, r: number, ox=0, oy=0) {
  const c = hexCenter(h,r);
  return Array.from({length:6},(_,i) => { const a=(60*i-90)*Math.PI/180; return `${c.x+ox+r*Math.cos(a)},${c.y+oy+r*Math.sin(a)}`; }).join(' ');
}
function message(text: string) { $('status').textContent = text; $('status').classList.toggle('feedback',/Пока дорога|не помещается|недоступен/.test(text)); }
function endpoints() { return [level.start,level.goal]; }
function previewValid() { return !!(selected && anchor && validPlacement(level,selected,{anchor,turns},layout)); }
function snapshot() { history.push(structuredClone(layout)); path.clear(); }
function resetSelection() { selected=null; anchor=null; turns=0; anchorPinned=false; }
function select(id: string) {
  selected=id; anchor=layout[id]?.anchor ?? null; turns=layout[id]?.turns ?? 0; anchorPinned=!!layout[id]; path.clear();
  message(`${pieceById(id).name}: ${mode === 'select' ? 'выбери клетку и нажми «Поставить».' : 'перетащи на поле. Можно повернуть кнопками.'}`);
}
function commit() {
  if (phase!=='playing' || !selected || !anchor || !previewValid()) return false;
  snapshot(); layout[selected]={anchor:{...anchor},turns}; resetSelection(); message('Плита на месте. Выбери следующую!'); render(); return true;
}
function updateControls() {
  for(const button of document.querySelectorAll<HTMLButtonElement>('footer button')) button.disabled=false;
  app.classList.toggle('drag-mode',mode==='drag');
  $('selected-drag').setAttribute('aria-label',mode==='drag'?'Перетащить выбранную фигуру':'Выбранная фигура');
  $('selected-drag').hidden=!selected||(mode!=='drag'&&level.id==='sandbox');
  $('tray').hidden=!!selected;
  $('selection-actions').hidden=!selected;
  $('check').hidden=!!selected;
  for (const id of ['left','right']) $(id).toggleAttribute('disabled',!selected);
  $('place').toggleAttribute('disabled',!previewValid());
  $('return').toggleAttribute('disabled',!selected);
  $('undo').toggleAttribute('disabled',history.length===0);
  $('clear').toggleAttribute('disabled',phase==='walking');
  for(const button of document.querySelectorAll<HTMLButtonElement>('footer button')) if(phase!=='playing') button.disabled=true;
}
function drawPieceIcon(button:HTMLElement,p:Level['pieces'][number],orientation=0) {
  const shape=p.shape.map(h=>rotate(h,orientation));
  const centers=shape.map(h=>hexCenter(h,15));
  const minX=Math.min(...centers.map(c=>c.x))-17, maxX=Math.max(...centers.map(c=>c.x))+17;
  const minY=Math.min(...centers.map(c=>c.y))-17, maxY=Math.max(...centers.map(c=>c.y))+17;
  const icon=el('svg',{viewBox:`${minX} ${minY} ${maxX-minX} ${maxY-minY}`,'aria-hidden':'true'},button);
  for (const h of shape) {
    el('polygon',{points:polygon(h,15),fill:p.color,stroke:'#543b70','stroke-width':1.5},icon);
    if(level.id!=='sandbox'&&p.kind!=='bridge'){const c=hexCenter(h,15);stoneDetail(icon,h,15,c.x,c.y,pieces.indexOf(p),new Set(shape.map(key)),{pieceId:p.id,local:rotate(h,-orientation),turns:orientation});}
  }
  if(p.kind==='bridge') el('text',{x:0,y:-6,'text-anchor':'middle','font-size':15,fill:'#493620'},icon,'≋');
  if(level.id!=='gate'||selected===p.id)el('circle',{cx:0,cy:0,r:level.id==='gate'?1.6:2.8,fill:'#fff6dc'},icon);
}
function renderTray() {
  const tray=$('tray'); tray.replaceChildren();
  const handle=$('selected-drag');handle.replaceChildren();
  if(selected){drawPieceIcon(handle,pieceById(selected),turns);const label=document.createElement('span');label.textContent=mode==='drag'?'Тяни отсюда':'Выбрано';handle.append(label);}
  for (const p of pieces) {
    const button=document.createElement('button'); button.className='piece'; button.dataset.piece=p.id;
    button.setAttribute('aria-label',`${p.name}${layout[p.id] ? ', на поле' : ', в наборе'}`);
    button.setAttribute('aria-pressed',String(selected===p.id));
    if (layout[p.id]) button.classList.add('placed');
    drawPieceIcon(button,p);
    const label=document.createElement('span'); label.textContent=p.name; button.append(label);
    if(layout[p.id]) {const mark=document.createElement('em'); mark.textContent='✓'; button.append(mark);}
    tray.append(button);
  }
}
function renderPreview() {
  document.getElementById('placement-preview')?.remove();
  if(selected && anchor) {
    const ok=previewValid(), preview=el('g',{id:'placement-preview','pointer-events':'none','data-preview':ok?'valid':'invalid'},svg);
    for(const h of placedCells(selected,{anchor,turns})) el('polygon',{points:polygon(h,radius,origin.x,origin.y),class:ok?'preview valid':'preview invalid'},preview);
    const c=hexCenter(anchor,radius);
    el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.23,'text-anchor':'middle','font-size':radius*.8,fill:ok?'#47285f':'#7a1c26','font-weight':900},preview,ok?'•':'⊘');
  }
}
function renderBoard() {
  if(screen!=='game') return;
  if(drag){renderPreview();return;}
  const rect=svg.getBoundingClientRect(), padding=8;
  const illustrated=level.id==='gate',chapterLevel=level.id!=='sandbox';
  const sceneTransform=illustrated?sceneLayout(rect.width,rect.height,cols,rows,level.start,level.goal,matchMedia('(orientation:portrait)').matches):null;
  const availableWidth=rect.width-2*padding;
  radius=Math.max(1,Math.min(availableWidth/(Math.sqrt(3)*(cols+0.5)),(rect.height-2*padding)/(1.5*(rows-1)+2)));
  const w=Math.sqrt(3)*radius*(cols+0.5), h=radius*(1.5*(rows-1)+2);
  origin={x:(rect.width-w)/2+Math.sqrt(3)*radius/2,y:(rect.height-h)/2+radius};
  if(sceneTransform){radius=sceneTransform.scale;origin=sceneTransform.origin;}
  svg.setAttribute('viewBox',`0 0 ${rect.width} ${rect.height}`); svg.replaceChildren();
  if(sceneTransform)backdrop(svg,rect.width,rect.height,sceneTransform);
  const owners=new Map<string,string>();
  for(const [id,p] of Object.entries(layout)) for(const h of placedCells(id,p)) owners.set(key(h),id);
  const [start,end]=endpoints();
  const paved=new Set(owners.keys());
  if(chapterLevel){paved.add(key(start));paved.add(key(end));}
  const landmarks=document.createElementNS(ns,'g');landmarks.setAttribute('pointer-events','none');
  for(const h of boardCells(cols,rows)) {
    const k=key(h), owner=owners.get(k), c=hexCenter(h,radius), terrain=terrainAt(level,h),terminal=chapterLevel&&(k===key(start)||k===key(end));
    const g=el('g',{'data-cell':k,'data-terrain':terrain,'data-owner':owner??'',role:'button',tabindex:0,'aria-label':`Клетка ${h.q+Math.floor(h.r/2)+1}, ряд ${h.r+1}${owner ? ', '+pieceById(owner).name : ''}${k===key(start)?', '+level.startName:k===key(end)?', '+level.goalName:''}${terrain==='ground'?'':', '+({tree:'дерево',rock:'камень',water:'вода',house:'дом',flower:'клумба'}[terrain])}`},svg);
    el('polygon',{points:polygon(h,radius,origin.x,origin.y),'pointer-events':'all',class:`cell ${illustrated?(owner||terminal?'flagstone':'meadow-cell'):''} ${path.has(k)?'path':''}`,fill:owner?pieceById(owner).color:terrain==='water'?'#83b9c5':terrain==='rock'?'#a4aa91':((h.r+Math.floor(h.q/2))%2===0?'#b1c59b':'#a9be93'),opacity:owner===selected?0.45:1},g);
    if(chapterLevel && (owner||terminal) && (!owner||pieceById(owner).kind!=='bridge')){const material=el('g',{opacity:owner===selected ? 0.45 : 1},g);stoneDetail(material,h,radius,c.x+origin.x,c.y+origin.y,owner?pieces.indexOf(pieceById(owner)):0,paved,owner?{pieceId:owner,local:rotate({q:h.q-layout[owner].anchor.q,r:h.r-layout[owner].anchor.r},-layout[owner].turns),turns:layout[owner].turns}:{pieceId:'endpoint',local:h,turns:0});}
    if(!owner && terrain!=='ground' && terrain!=='house') el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.28,'text-anchor':'middle','font-size':radius*.95,fill:terrain==='water'?'#d8eef0':'#526446','pointer-events':'none'},g,({water:'≈',tree:'♠',rock:'⬟',flower:'✿'}[terrain]));
    if(owner && pieceById(owner).kind==='bridge') {
      const deck=el('g',{transform:`translate(${c.x+origin.x} ${c.y+origin.y}) rotate(${layout[owner].turns*60})`,'pointer-events':'none'},g);
      for(const dx of [-.35,0,.35]) el('line',{x1:radius*dx,x2:radius*dx,y1:-radius*.65,y2:radius*.65,stroke:'#775032','stroke-width':2},deck);
    }
    if(owner && (!illustrated||owner===selected) && key(layout[owner].anchor)===k) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y,r:Math.max(2,radius*.09),fill:'#fff5d6','pointer-events':'none'},g);
    if(!illustrated && (k===key(start)||k===key(end))) {
      el('text',{x:c.x+origin.x,y:c.y+origin.y-radius*.1,class:'landmark','font-size':radius*.62},landmarks,k===key(start)?'⌂':'⚑');
      el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.45,class:'landmark label','font-size':Math.max(10,Math.min(12,radius*.35))},landmarks,k===key(start)?level.startName:level.goalName);
    }
    if(path.has(k)) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y-radius*.6,r:Math.max(2,radius*.08),fill:'#fffbd3','pointer-events':'none'},g);
  }
  if(illustrated)drawGrid(svg,cols,rows,radius,origin,new Set(boardCells(cols,rows).filter(h=>terrainAt(level,h)==='house').map(key)));
  if(chapterLevel)drawInstanceEdges(svg,owners,radius,origin);
  svg.append(landmarks);
  if(sceneTransform)scenery(svg,sceneTransform);
  else if(chapterLevel)prototypeRuta();
  $('scene-event').replaceChildren();$('scene-event').hidden=true;
  if(chapterLevel&&(completed.includes(level.id)||phase==='won'))victoryDecoration();

  renderPreview();
  if(level.id==='mill') {
    const c=hexCenter(level.goal,radius);
    const wheel=el('g',{transform:`translate(${origin.x+c.x} ${origin.y+c.y-radius*.35})`,'pointer-events':'none'},svg);
    const spokes=el('g',{class:phase==='won'||completed.includes(level.id)?'mill-wheel turning':'mill-wheel','data-wheel':phase==='won'||completed.includes(level.id)?'running':'still'},wheel);
    el('circle',{r:radius*.28,fill:'#dbbd87',stroke:'#765239','stroke-width':2},spokes);
    for(let i=0;i<4;i++){const a=i*Math.PI/4;el('line',{x1:-Math.cos(a)*radius*.28,y1:-Math.sin(a)*radius*.28,x2:Math.cos(a)*radius*.28,y2:Math.sin(a)*radius*.28,stroke:'#765239','stroke-width':2},spokes);}
  }
  if(route.length) {el('g',{id:'ruta-marker','pointer-events':'none','aria-label':'Рута идёт по дороге'},svg);updateRutaMarker();}
  $('metric').textContent=`Гекс ${Math.round(Math.sqrt(3)*radius)} × ${Math.round(2*radius)} px`;
}
function prototypeRuta(){
 const c=hexCenter(level.start,radius),visible=radius*2*1.1,height=visible*1300/1232,width=height*1209/1300;
 const layer=el('g',{'pointer-events':'none'},svg);
 if(!route.length){
 el('ellipse',{cx:c.x+origin.x,cy:c.y+origin.y,rx:radius*.23,ry:radius*.08,fill:'#3f3b32',opacity:.25},layer);
 el('image',{id:'ruta-idle',href:artUrl('ruta-idle'),x:c.x+origin.x-width*.55,y:c.y+origin.y-height*1277/1300,width,height,'aria-label':'Рута у начала дороги'},layer);
 }

}
function victoryDecoration(){
 const labels:Record<string,[string,string]>={gate:['⚑','Калитка открыта'],garden:['◉','Яблоки на столе'],well:['✿','Цветы политы'],bakery:['♨','Хлеб готов'],stream:['➜','Переход готов'],mill:['▣','Мука на тележке'],post:['✉','Почта в пути'],forest:['♠','Яблоневый сад →']};
 const [,text]=labels[level.id],host=$('scene-event');host.hidden=false;host.setAttribute('role','img');host.setAttribute('aria-label',text);
 const badge=el('svg',{width:34,height:34,viewBox:'0 0 36 36','aria-hidden':'true'},host);
 const event=el('g',{'pointer-events':'none','data-victory-event':storyFor(level.id)!.mapEvent},badge);
 const sketch=el('g',{transform:'translate(2 4)',fill:'none',stroke:'#f2d49b','stroke-width':2,'stroke-linecap':'round'},event);
 const drawings:Record<string,string>={
  gate:'M 0 25 V 0 M 25 25 V 0 M 0 5 L 16 0 V 21 L 0 25 M 5 4 V 23',
  garden:'M 0 13 H 28 M 5 13 V 25 M 23 13 V 25 M 6 2 L 8 11 H 20 L 22 2 Z',
  well:'M 2 6 L 5 24 H 17 L 20 6 Z M 5 6 Q 10 -3 17 6 M 20 10 L 29 6 M 26 17 V 25',
  bakery:'M 0 12 L 4 25 H 25 L 29 12 Z M 4 12 Q 2 -1 10 3 Q 14 -3 19 3 Q 28 0 25 12',
  stream:'M 0 23 V 7 H 29 V 23 M 0 13 H 29 M 6 8 V 18 M 14 8 V 18 M 22 8 V 18',
  mill:'M 1 18 H 22 L 27 8 H 32 M 4 18 V 2 H 19 V 18 M 8 2 V 0 H 15 V 2',
  post:'M 0 3 H 28 V 22 H 0 Z M 0 3 L 14 14 L 28 3 M 1 21 L 10 12 M 27 21 L 18 12',
  forest:'M 13 26 V 0 M 0 2 H 26 L 32 9 L 26 16 H 0 Z'};
 el('path',{d:drawings[level.id]},sketch);
 if(level.id==='garden')for(const [x,y] of [[10,6],[16,6],[14,2]])el('circle',{cx:x,cy:y,r:3,fill:'#ac4950',stroke:'none'},sketch);
 if(level.id==='well')el('path',{d:'M 25 13 L 25 15 M 29 11 L 29 13',stroke:'#559eae'},sketch);
 if(level.id==='mill')for(const x of [6,20])el('circle',{cx:x,cy:23,r:3,fill:'#88603b'},sketch);
 if(level.id==='forest')el('circle',{cx:30,cy:8,r:3,fill:'#ab70cc',stroke:'none',class:phase==='won'&&firstVictory&&performance.now()-victoryAt<1200?'forest-glimmer':'',style:`animation-delay:-${Math.max(0,performance.now()-victoryAt)}ms`},sketch);
}
function render() {
  if(deferDock){
    if(!dockFrame)dockFrame=requestAnimationFrame(()=>{dockFrame=0;deferDock=false;render();});
    return;
  }
  renderBoard();renderTray();updateControls();
}
function eventHex(e: PointerEvent, lift=false): Hex | null {
  const rect=svg.getBoundingClientRect(), x=e.clientX-rect.left, y=e.clientY-rect.top-(lift && e.pointerType==='touch'?Math.max(42,radius*1.6):0);
  if(x<0||y<0||x>rect.width||y>rect.height) return null;
  return pixelHex(x-origin.x,y-origin.y,radius);
}
function ownerAt(h: Hex) { return Object.entries(layout).find(([id,p])=>placedCells(id,p).some(c=>key(c)===key(h)))?.[0]; }
$('tray').addEventListener('click',e=>{
  if(suppressClick || phase!=='playing') return;
  const id=(e.target as Element).closest<HTMLElement>('[data-piece]')?.dataset.piece;
  if(id) { select(id); render(); }
});
svg.addEventListener('click',e=>{
  if(mode!=='select'||suppressClick||phase!=='playing') return;
  const cell=(e.target as Element).closest('[data-cell]')?.getAttribute('data-cell');
  if(!cell) return;
  const [q,r]=cell.split(',').map(Number), h={q,r}, owner=ownerAt(h);
  if(owner && owner!==selected) select(owner);
  else if(selected) {
    anchor=h; anchorPinned=true;
    message(previewValid() ? 'Место выбрано. Нажми «Поставить» или выбери другую клетку.' : 'Здесь плита не помещается. Выбери другую клетку или поверни её.');
  }
  render();
});
svg.addEventListener('keydown',e=>{
  if(e.key==='Enter'||e.key===' ') {e.preventDefault(); (e.target as Element).dispatchEvent(new MouseEvent('click',{bubbles:true}));}
});
svg.addEventListener('pointermove',e=>{
  if(phase==='playing' && mode==='select' && selected && !anchorPinned && e.pointerType==='mouse' && !e.buttons) {anchor=eventHex(e); renderBoard(); updateControls();}
});
function startDrag(e: PointerEvent,id: string) {
  if(phase!=='playing'||mode!=='drag'||!e.isPrimary||e.button!==0||drag) return;
  // touch-action:none handles scrolling; keep native tap/click synthesis intact.
  if(selected!==id) select(id);
  drag={pointer:e.pointerId,startX:e.clientX,startY:e.clientY,moved:false,beforeAnchor:anchor?{...anchor}:null,beforeTurns:turns};
  app.setPointerCapture(e.pointerId); renderBoard();
}
$('selected-drag').addEventListener('pointerdown',e=>{if(selected)startDrag(e,selected);});
$('tray').addEventListener('pointerdown',e=>{
  const id=(e.target as Element).closest<HTMLElement>('[data-piece]')?.dataset.piece;
  if(id) startDrag(e,id);
});
svg.addEventListener('pointerdown',e=>{
  const h=eventHex(e), id=h && ownerAt(h); if(id) startDrag(e,id);
});
app.addEventListener('pointermove',e=>{
  if(!drag||e.pointerId!==drag.pointer) return;
  if(Math.hypot(e.clientX-drag.startX,e.clientY-drag.startY)>5) drag.moved=true;
  if(drag.moved) {anchor=eventHex(e,true); renderBoard();}
});
function finishDrag(e: PointerEvent,cancel: boolean) {
  if(!drag||e.pointerId!==drag.pointer) return;
  const previous=drag; drag=null;
  // Keep the original touch target alive through touchend and native click.
  deferDock=e.pointerType==='touch';
  if(app.hasPointerCapture(e.pointerId)) app.releasePointerCapture(e.pointerId);
  suppressClick=true;
  if(!cancel && previous.moved) {
    anchor=eventHex(e,true);
    if(commit()) return;
    message('Здесь не помещается. Плита вернулась на прежнее место.');
  }
  anchor=previous.beforeAnchor; turns=previous.beforeTurns;
  if(cancel) message('Перетаскивание отменено. Плита сохранена.');
  render();
}
app.addEventListener('pointerup',e=>finishDrag(e,false));
app.addEventListener('pointercancel',e=>finishDrag(e,true));
app.addEventListener('lostpointercapture',e=>{if(drag) finishDrag(e,true);});
for(const [id,delta] of [['left',-1],['right',1]] as const) $(id).onclick=()=>{if(selected){turns=(turns+delta+6)%6;render();}};
$('place').onclick=commit;
$('other').onclick=()=>{resetSelection();message('Выбери другую плиту.');render();};
const settings=$('settings-panel') as HTMLDialogElement;
$('settings-open').onclick=()=>settings.showModal();
$('settings-close').onclick=()=>settings.close();
$('return').onclick=()=>{
  if(!selected) return;
  if(layout[selected]) {snapshot();delete layout[selected];}
  resetSelection(); message('Плита в наборе.'); render();
};
$('undo').onclick=()=>{const prior=history.pop();if(prior){layout=prior;path.clear();resetSelection();message('Последнее действие отменено.');render();}};
$('clear').onclick=()=>{if(phase!=='playing')return;if(Object.keys(layout).length)snapshot();layout={};path.clear();route=[];resetSelection();message('Начнём снова. Все плиты в наборе.');render();};
$('check').onclick=()=>{
  if(phase!=='playing')return;
  const result=winningPath(level,layout);
  path=new Set(result?.map(key));
  if(!result){message('Пока дорога не соединена. Попробуй переложить плиты');renderBoard();return;}
  if(level.id==='sandbox'){message('Дорога готова! Из деревни можно дойти до мельницы.');renderBoard();return;}
  phase='walking';route=result;journey=0;resetSelection();
  firstVictory=!completed.includes(level.id);
  completed=completeLevel(level.id,completed);persist();
  if(level.id==='gate'){phase='won';route=[];message('Дорога готова!');render();finishVictory();return;}
  message('Получилось! Рута проверяет дорожку.');render();
  const began=performance.now(),duration=Math.min(3500,result.length*230);
  const animate=(now:number)=>{
    if(phase!=='walking'||screen!=='game')return;
    journey=matchMedia('(prefers-reduced-motion: reduce)').matches?result.length-1:Math.max(0,Math.min(1,(now-began)/duration))*(result.length-1);
    updateRutaMarker();
    if(journey>=result.length-1){phase='won';victoryAt=performance.now();renderBoard();finishVictory();}
    else frame=requestAnimationFrame(animate);
  };
  frame=requestAnimationFrame(animate);
};
$('size').onchange=()=>{
  [cols,rows]=($('size') as HTMLSelectElement).value.split(',').map(Number);
  if(level.id!=='sandbox')return;
  level=sandbox(cols,rows);pieces=level.pieces;
  layout={};history=[];path.clear();resetSelection();message('Новое поле. Все плиты снова в наборе.');render();
};
$('mode').onchange=()=>{
  mode=($('mode') as HTMLSelectElement).value; resetSelection();
  $('hint').textContent=mode==='select'?'Выбери плиту → клетку → «Поставить»':'Тяни за плиту · на телефоне цель выше пальца';
  message(mode==='select'?'Выбери плиту в наборе или на поле.':'Перетащи плиту на поле. Отпусти, чтобы поставить.');render();
};
if(document.fullscreenEnabled) {
  $('fullscreen').hidden=false;
  $('fullscreen').onclick=async()=>{
    try {if(document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen();}
    catch {message('Полный экран недоступен. Можно играть так.');}
  };
}
window.addEventListener('keydown',e=>{if(e.key==='Escape' && !drag && screen==='game' && phase==='playing' && !settings.open){resetSelection();render();}});
new ResizeObserver(()=>renderBoard()).observe($('field'));

function updateRutaMarker() {
  const marker=document.getElementById('ruta-marker');if(!marker||!route.length)return;
  const index=Math.min(Math.floor(journey),route.length-1),next=Math.min(index+1,route.length-1),t=journey-index;
  const a=hexCenter(route[index],radius),b=hexCenter(route[next],radius);
  marker.setAttribute('transform',`translate(${origin.x+a.x+(b.x-a.x)*t} ${origin.y+a.y+(b.y-a.y)*t})`);
  marker.replaceChildren();
  el('circle',{r:radius*.29,fill:'#f5ddb1',stroke:'#7c4d42','stroke-width':2},marker);
  el('path',{d:`M ${-radius*.26} ${radius*.18} L ${radius*.27} ${radius*.18} L 0 ${radius*.55} Z`,fill:'#b94455'},marker);
}
const story=$('story') as HTMLDialogElement;
function bridgeGuide(parent:Element){
 const diagram=el('svg',{id:'bridge-guide',viewBox:'0 0 240 78',role:'img','aria-label':'Мост: сухой берег, вода посередине, сухой берег'},parent);
 for(let i=0;i<3;i++){
  el('polygon',{points:polygon({q:i,r:0},22,65,36),fill:i===1?'#8bbccc':'#afc58c',stroke:'#5e7555'},diagram);
  el('text',{x:65+i*Math.sqrt(3)*22,y:74,'font-size':11,'text-anchor':'middle',fill:'#435c39'},diagram,i===1?'Вода':'Берег');
 }
 el('rect',{x:50,y:26,width:108,height:20,fill:'#c59b65',stroke:'#795332'},diagram);
 for(let i=0;i<7;i++)el('line',{x1:54+i*16,x2:54+i*16,y1:27,y2:45,stroke:'#795332'},diagram);
}
function dialogPages(title:string,pages:Dialogue[],finish:()=>void,lastLabel:string){
 let index=0;
 document.querySelector('svg.ruta-portrait')!.setAttribute('hidden','');
 let portrait=document.getElementById('story-ruta') as HTMLImageElement|null;
 if(!portrait){portrait=document.createElement('img');portrait.id='story-ruta';portrait.className='ruta-portrait';portrait.alt='Рута';portrait.src=artUrl('ruta-idle');document.querySelector('.story-layout')!.prepend(portrait);}
 portrait.hidden=false;
 const draw=()=>{
  document.getElementById('bridge-guide')?.remove();
  if(pages[index].speaker==='Мост')bridgeGuide($('story-text').parentElement!);
  $('story-title').textContent=title;
  document.querySelector('#story .eyebrow')!.textContent=`${pages[index].speaker} · ${index+1}/${pages.length}`;
  $('story-text').textContent=pages[index].text;
  $('story-action').textContent=index===pages.length-1?lastLabel:'Дальше →';
 };
 const close=()=>{story.close();finish();};
 $('story-action').onclick=()=>{if(index===pages.length-1)close();else{index++;draw();}};
 $('story-skip').onclick=close;draw();if(!story.open)story.showModal();
}
function showStory(outro=false){
 const data=storyFor(level.id)!;
 const pages:Dialogue[]=[...(outro?data.after:data.before)];
 if(!outro&&level.id==='stream')pages.push({speaker:'Мост',text:'Две опоры — на сухих берегах. Середина мостика — над водой. Обычные плиты на воду не ставим.'});
 if(outro){pages.push({speaker:'После победы',text:data.victoryScene});if(level.id==='post')pages.push({speaker:'Старое приглашение',text:invitation.text});}
 dialogPages(level.name,pages,()=>{
  if(outro){if(level.id==='forest')showEnding();else showMap();}
  else{if(!introSeen.includes(level.id))introSeen.push(level.id);persist();phase='playing';render();}
 },outro?'На карту →':'В путь →');
}
function readStory(id:string){
 const data=storyFor(id)!;
 const pages:Dialogue[]=[...data.before];
 if(completed.includes(id)){pages.push(...data.after,{speaker:'После победы',text:data.victoryScene});if(id==='post')pages.push({speaker:'Старое приглашение',text:invitation.text});}
 if(id==='stream')pages.push({speaker:'Мост',text:'Края на сухих берегах, середина над водой. Обычные плиты — только на земле.'});
 dialogPages(data.title,pages,()=>{},'Закрыть');
}
function showEnding(){
 dialogPages(`Глава «${chapter.title}» пройдена`,[{speaker:'Рута',text:'Мы помогли деревне и нашли путь к старому саду.'},{speaker:'Следующая глава',text:`«${ending.title}». Рута отправится за письмами через лес. Продолжение готовится.`}],showMap,'На карту →');
}
function finishVictory(){if(firstVictory)showStory(true);else{message('Дорога снова готова!');dialogPages(level.name,[{speaker:'Рута',text:'Получилось! Дорога снова соединена.'}],showMap,'На карту →');}}
story.addEventListener('cancel',e=>{e.preventDefault();$('story-skip').click();});
function enterLevel(next:Level) {
  if(next.id!=='sandbox'&&!available(next.id,completed))return;
  cancelAnimationFrame(frame);screen='game';phase=next.id==='sandbox'||introSeen.includes(next.id)?'playing':'intro';
  level=next;pieces=level.pieces;cols=level.cols;rows=level.rows;layout={};history=[];route=[];journey=0;path.clear();resetSelection();
  app.classList.toggle('illustrated-level',level.id!=='sandbox');
  app.classList.toggle('prototype-level',level.id!=='sandbox'&&level.id!=='gate');
  sceneChrome(level.id!=='sandbox');
  document.querySelector('h1')!.textContent=level.id==='sandbox'?'Рубиновая деревня':level.name;
  if(level.id!=='sandbox'&&level.id!=='gate'){const note=document.createElement('small');note.textContent='Условная сцена';note.dataset.prototype='';document.querySelector('h1')!.append(note);}
  $('chapter-map').hidden=true;$('field').hidden=false;$('game-controls').hidden=false;
  $('size-setting').hidden=level.id!=='sandbox';
  $('clear').textContent=level.id==='sandbox'?'Очистить поле':'Начать уровень заново';
  document.querySelector('.settings-note')!.textContent=level.id==='sandbox'?'Смена размера очищает поле. Поворот телефона сохраняет плиты.':'Перезапуск очищает плиты этого уровня. Дороги на карте сохраняются.';
  svg.setAttribute('aria-label',`${level.name}: ${level.startName} → ${level.goalName}`);
  message(level.id==='gate'?'Проложи дорогу от дома до калитки':level.id==='sandbox'?level.intro:level.name);render();
  $('story-replay').hidden=level.id==='sandbox';
  if(phase==='intro')showStory();
}
function mapGeometry(){
 const portrait=matchMedia('(orientation:portrait)').matches;
 const points=portrait?[[250,50],[750,50],[750,150],[250,150],[250,250],[750,250],[750,350],[250,350]]:[[120,95],[365,95],[610,95],[855,95],[855,300],[610,300],[365,300],[120,300]];
 const roads=$('map-roads');roads.replaceChildren();
 let previous=portrait?[25,50]:[20,95];
 levels.forEach((l,i)=>{
  const [x,y]=points[i],done=completed.includes(l.id);
  el('path',{d:`M ${previous[0]} ${previous[1]} L ${x} ${y}`,fill:'none',stroke:done?'#9062b0':'#a2ab8c','stroke-width':10,'stroke-dasharray':done?'none':'10 12','data-road':l.id,'data-complete':String(done)},roads);
  const node=document.querySelector<HTMLElement>(`[data-map-node="${l.id}"]`);
  if(node){node.style.left=`${x/10}%`;node.style.top=`${y/4}%`;}
  previous=[x,y];
 });
}
function showMap(){
 $('scene-event').hidden=true;
 app.classList.remove('illustrated-level','prototype-level');sceneChrome(false);document.querySelector('h1')!.textContent='Рубиновая деревня';
 cancelAnimationFrame(frame);screen='map';phase='playing';route=[];resetSelection();
 if(settings.open)settings.close();if(story.open)story.close();
 $('field').hidden=true;$('game-controls').hidden=true;$('chapter-map').hidden=false;
 message(completed.length===levels.length?`Глава «${chapter.title}» пройдена`:`Первая глава · ${chapter.title}`);
 $('save-status').textContent=storageAvailable?'':'Прогресс хранится только до обновления или закрытия страницы.';
 const places=$('map-places');places.replaceChildren();
 for(const [index,l] of levels.entries()){
  const data=storyFor(l.id)!,unlocked=available(l.id,completed),done=completed.includes(l.id);
  const node=document.createElement('div');node.className='map-node';node.dataset.mapNode=l.id;
  const button=document.createElement('button');button.dataset.level=l.id;button.className='level-card';button.disabled=!unlocked;
  button.setAttribute('aria-label',`${l.name}${done?', пройдено, можно переиграть':unlocked?', открыто':', пока закрыто'}`);
  const symbol=document.createElement('span');symbol.className='place-symbol';symbol.textContent=['⌂','♧','♜','♨','≋','✣','✉','♠'][index];
  const title=document.createElement('strong');title.textContent=`${index+1}. ${l.name}`;
  const state=document.createElement('span');state.className='map-state';state.textContent=done?'✓ Пройден':unlocked?'▶ В путь':'🔒 Закрыто';
  button.append(symbol,title,state);button.onclick=()=>enterLevel(l);node.append(button);
  if(unlocked){const book=document.createElement('button');book.className='map-book';book.textContent='▤';book.setAttribute('aria-label',`Реплики: ${data.title}`);book.onclick=()=>readStory(l.id);node.append(book);}
  places.append(node);
 }
 mapGeometry();
 $('chapter-ending').hidden=!completed.includes('forest');$('letter-open').hidden=!completed.includes('post');
 $('reset-open').toggleAttribute('disabled',completed.length===0);
}
new ResizeObserver(()=>{if(screen==='map')mapGeometry();}).observe($('chapter-map'));
$('chapter-ending').onclick=showEnding;
$('letter-open').onclick=()=>dialogPages('Старое приглашение',[{speaker:'Хранитель сада',text:invitation.text}],()=>{},'Закрыть');
$('story-replay').onclick=()=>{settings.close();readStory(level.id);};
$('sandbox-open').onclick=()=>enterLevel(sandbox(...(($('size') as HTMLSelectElement).value.split(',').map(Number) as [number,number])));
$('map-return').onclick=showMap;
const resetDialog=$('reset-dialog') as HTMLDialogElement;
$('reset-open').onclick=()=>resetDialog.showModal();
$('reset-cancel').onclick=()=>resetDialog.close();
$('reset-confirm').onclick=()=>{completed=[];introSeen=[];persist();resetDialog.close();showMap();};
function icon(button:HTMLElement,path:string){
  const target=button.querySelector('b')??button;
  target.innerHTML=`<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="${path}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}
function sceneChrome(illustrated:boolean){
  $('scene-back').hidden=!illustrated;$('scene-help').hidden=!illustrated;
  const settingsButton=$('settings-open');
  (illustrated?document.querySelector('header')!:$('game-controls')).append(settingsButton);
  $('check').querySelector('span')!.textContent=illustrated?'Проверить':'Проверить дорогу';
}
icon($('scene-back'),'M 15 5 L 7 12 L 15 19');
icon($('settings-open'),'M 9 3 H 15 L 16 6 L 19 7 L 22 11 L 20 14 L 19 17 L 15 18 L 14 21 H 10 L 9 18 L 5 17 L 4 14 L 2 11 L 5 7 L 8 6 Z M 15 12 A 3 3 0 1 1 9 12 A 3 3 0 1 1 15 12');
icon($('undo'),'M 8 5 L 3 10 L 8 15 M 3 10 H 15 A 5 5 0 0 1 15 20');
icon($('left'),'M 6 4 L 2 9 L 8 10 M 3 9 A 8 8 0 1 1 5 19');
icon($('right'),'M 18 4 L 22 9 L 16 10 M 21 9 A 8 8 0 1 0 19 19');
icon($('check'),'M 4 12 L 9 17 L 20 6');
icon($('place'),'M 5 12 H 19 M 12 5 V 19');
icon($('return'),'M 4 14 V 20 H 20 V 14 M 12 16 V 3 M 7 8 L 12 3 L 17 8');
icon($('other'),'M 15 5 L 7 12 L 15 19');
$('scene-back').onclick=showMap;
$('scene-help').onclick=()=>{document.querySelector('#help-panel #bridge-guide')?.remove();if(pieces.some(p=>p.kind==='bridge'))bridgeGuide($('help-panel'));$('help-title').textContent=`${level.startName} → ${level.goalName}`;($('help-panel') as HTMLDialogElement).showModal();};
$('help-close').onclick=()=>($('help-panel') as HTMLDialogElement).close();
showMap();

// Development-only visual fixture; storage is disconnected for its whole session.
if(artCheck){enterLevel(levels[0]);story.close();phase='playing';layout=Object.fromEntries(Object.entries(levels[0].solution).slice(0,3).map(([id,p])=>[id,structuredClone(p)]));render();}
