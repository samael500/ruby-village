import './style.css';
import {type Hex, boardCells, key, hexCenter, pixelHex, rotate} from './hex.ts';
import {pieceById as lookupPiece, placedCells as cellsForPiece, validPlacement, terrainAt, winningPath, type Layout} from './game.ts';
import {levels,sandbox} from './levels.ts';
import type {Level} from './model.ts';
import {loadProgress,saveProgress,completeLevel,available,type StorageLike} from './progress.ts';

const app = document.querySelector<HTMLDivElement>('#app')!;
app.innerHTML = `
<header><div class="brand"><span class="ruby" aria-hidden="true">◆</span><h1>Рубиновая деревня<span class="sr-only"> · первая глава</span></h1></div><div id="status" role="status" aria-live="polite">Выбери плиту, затем клетку.</div></header>
<div class="portrait">↻ Поверни телефон — поле станет крупнее</div>
<section id="chapter-map" aria-label="Карта первой главы">
<div class="map-intro"><span class="ruta-small" aria-hidden="true">◆</span><p>Дороги исчезают… Поможем Руте вернуть их?</p></div>
<div class="map-landscape"><svg id="map-roads" viewBox="0 0 1000 160" preserveAspectRatio="none" aria-hidden="true"></svg><div id="map-places"></div></div>
<div class="map-actions"><button id="sandbox-open">⬡ Песочница</button><span id="save-status" role="status"></span><button id="reset-open">Начать главу заново</button></div>
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
<button id="settings-open" aria-haspopup="dialog"><b>⚙</b><span>Настройки</span></button>
</footer>
<dialog id="settings-panel" aria-labelledby="settings-title">
<div class="dialog-heading"><h2 id="settings-title">Настройки площадки</h2><button id="settings-close" aria-label="Закрыть настройки">✕</button></div>
<div class="settings"><label id="size-setting">Размер поля<select id="size" aria-label="Размер поля"><option value="7,5">7 × 5 — крупнее</option><option value="9,6" selected>9 × 6</option><option value="11,7">11 × 7 — мельче</option></select></label>
<label>Управление<select id="mode" aria-label="Режим управления"><option value="select">Выбрать и поставить</option><option value="drag">Перетаскивать</option></select></label></div>
<p id="metric"></p><p id="hint">Выбери плиту → клетку → «Поставить»</p>
<p class="settings-note">Смена размера очищает поле. Поворот телефона сохраняет плиты.</p>
<div class="settings-actions"><button id="map-return">На карту</button><button id="clear">Начать уровень заново</button><button id="fullscreen" hidden>Полный экран</button></div>
</dialog>
<dialog id="story" aria-labelledby="story-title"><div class="story-layout">
<svg class="ruta-portrait" viewBox="0 0 100 110" role="img" aria-label="Условный портрет Руты: русые волосы и красный платок">
<path d="M20 68V32C20 0 80 0 80 32V75" fill="#b39058"/><path d="M21 110V82Q50 59 79 82V110" fill="#6c8853"/>
<ellipse cx="50" cy="40" rx="24" ry="29" fill="#f1d2a6"/><path d="M24 33Q30 2 62 14L76 37Q59 27 52 17Q43 32 24 33" fill="#b39058"/>
<circle cx="41" cy="40" r="3" fill="#5688ab"/><circle cx="60" cy="40" r="3" fill="#5688ab"/>
<path d="M44 54Q51 60 58 53" fill="none" stroke="#8c5b43" stroke-width="2"/><path d="M26 71L69 68L56 90L43 77L29 99" fill="#b34f56"/>
<path d="M67 82L84 100" stroke="#725440" stroke-width="6"/><rect x="69" y="94" width="23" height="15" rx="3" fill="#a27a4c"/>
</svg><div><p class="eyebrow">Рута · первая глава</p><h2 id="story-title"></h2><p id="story-text"></p></div></div><button id="story-action" class="primary">В путь →</button></dialog>
<dialog id="reset-dialog" aria-labelledby="reset-title"><h2 id="reset-title">Начать главу заново?</h2><p>Все три дороги на карте снова исчезнут.</p><div class="settings-actions"><button id="reset-cancel">Оставить дороги</button><button id="reset-confirm">Да, начать заново</button></div></dialog>`;
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const svg = document.getElementById('board') as unknown as SVGSVGElement;
let level:Level=sandbox();
let pieces=level.pieces;
const pieceById=(id:string)=>lookupPiece(id,pieces);
const placedCells=(id:string,p:Layout[string])=>cellsForPiece(id,p,pieces);
let screen:'map'|'game'='map';
let phase:'intro'|'playing'|'walking'|'won'='playing';
let storage:StorageLike|undefined;
try {storage=window.localStorage;} catch { /* Private browsing may deny storage access. */ }
let completed=loadProgress(storage), storageAvailable=!!storage;
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
function message(text: string) { $('status').textContent = text; }
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
  $('selected-drag').hidden=mode!=='drag'||!selected;
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
  for (const h of shape) el('polygon',{points:polygon(h,15),fill:p.color,stroke:'#543b70','stroke-width':1.5},icon);
  if(p.kind==='bridge') el('text',{x:0,y:-6,'text-anchor':'middle','font-size':15,fill:'#493620'},icon,'≋');
  el('circle',{cx:0,cy:0,r:2.8,fill:'#fff6dc'},icon);
}
function renderTray() {
  const tray=$('tray'); tray.replaceChildren();
  const handle=$('selected-drag');handle.replaceChildren();
  if(selected){drawPieceIcon(handle,pieceById(selected),turns);const label=document.createElement('span');label.textContent='Тяни отсюда';handle.append(label);}
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
  const rect=$('field').getBoundingClientRect(), padding=8;
  radius=Math.max(1,Math.min((rect.width-2*padding)/(Math.sqrt(3)*(cols+0.5)),(rect.height-2*padding)/(1.5*(rows-1)+2)));
  const w=Math.sqrt(3)*radius*(cols+0.5), h=radius*(1.5*(rows-1)+2);
  origin={x:(rect.width-w)/2+Math.sqrt(3)*radius/2,y:(rect.height-h)/2+radius};
  svg.setAttribute('viewBox',`0 0 ${rect.width} ${rect.height}`); svg.replaceChildren();
  const owners=new Map<string,string>();
  for(const [id,p] of Object.entries(layout)) for(const h of placedCells(id,p)) owners.set(key(h),id);
  const [start,end]=endpoints();
  const landmarks=document.createElementNS(ns,'g');landmarks.setAttribute('pointer-events','none');
  for(const h of boardCells(cols,rows)) {
    const k=key(h), owner=owners.get(k), c=hexCenter(h,radius), terrain=terrainAt(level,h);
    const g=el('g',{'data-cell':k,'data-terrain':terrain,role:'button',tabindex:0,'aria-label':`Клетка ${h.q+Math.floor(h.r/2)+1}, ряд ${h.r+1}${owner ? ', '+pieceById(owner).name : ''}${terrain==='ground'?'':', '+({tree:'дерево',rock:'камень',water:'вода'}[terrain])}`},svg);
    el('polygon',{points:polygon(h,radius,origin.x,origin.y),class:`cell ${path.has(k)?'path':''}`,fill:owner?pieceById(owner).color:terrain==='water'?'#83b9c5':terrain==='rock'?'#a4aa91':((h.r+Math.floor(h.q/2))%2===0?'#b1c59b':'#a9be93'),opacity:owner===selected?0.45:1},g);
    if(!owner && terrain!=='ground') el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.28,'text-anchor':'middle','font-size':radius*.95,fill:terrain==='water'?'#d8eef0':'#526446','pointer-events':'none'},g,({water:'≈',tree:'♠',rock:'⬟'}[terrain]));
    if(owner && pieceById(owner).kind==='bridge') {
      const deck=el('g',{transform:`translate(${c.x+origin.x} ${c.y+origin.y}) rotate(${layout[owner].turns*60})`,'pointer-events':'none'},g);
      for(const dx of [-.35,0,.35]) el('line',{x1:radius*dx,x2:radius*dx,y1:-radius*.65,y2:radius*.65,stroke:'#775032','stroke-width':2},deck);
    }
    if(owner && key(layout[owner].anchor)===k) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y,r:Math.max(2,radius*.09),fill:'#fff5d6','pointer-events':'none'},g);
    if(k===key(start)||k===key(end)) {
      el('text',{x:c.x+origin.x,y:c.y+origin.y-radius*.1,class:'landmark','font-size':radius*.62},landmarks,k===key(start)?'⌂':'⚑');
      el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.45,class:'landmark label','font-size':Math.max(10,Math.min(12,radius*.35))},landmarks,k===key(start)?level.startName:level.goalName);
    }
    if(path.has(k)) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y-radius*.6,r:Math.max(2,radius*.08),fill:'#fffbd3','pointer-events':'none'},g);
  }
  svg.append(landmarks);
  renderPreview();
  if(level.id==='mill') {
    const c=hexCenter(level.goal,radius);
    const wheel=el('g',{transform:`translate(${origin.x+c.x} ${origin.y+c.y-radius*.35})`,'pointer-events':'none'},svg);
    const spokes=el('g',{class:phase==='won'?'mill-wheel turning':'mill-wheel','data-wheel':phase==='won'?'running':'still'},wheel);
    el('circle',{r:radius*.28,fill:'#dbbd87',stroke:'#765239','stroke-width':2},spokes);
    for(let i=0;i<4;i++){const a=i*Math.PI/4;el('line',{x1:-Math.cos(a)*radius*.28,y1:-Math.sin(a)*radius*.28,x2:Math.cos(a)*radius*.28,y2:Math.sin(a)*radius*.28,stroke:'#765239','stroke-width':2},spokes);}
  }
  if(route.length) {el('g',{id:'ruta-marker','pointer-events':'none','aria-label':'Рута идёт по дороге'},svg);updateRutaMarker();}
  $('metric').textContent=`Гекс ${Math.round(Math.sqrt(3)*radius)} × ${Math.round(2*radius)} px`;
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
  completed=completeLevel(level.id,completed);storageAvailable=saveProgress(completed,storage);
  message('Получилось! Рута проверяет дорожку.');render();
  const began=performance.now(),duration=Math.min(3500,result.length*230);
  const animate=(now:number)=>{
    if(phase!=='walking'||screen!=='game')return;
    journey=matchMedia('(prefers-reduced-motion: reduce)').matches?result.length-1:Math.max(0,Math.min(1,(now-began)/duration))*(result.length-1);
    updateRutaMarker();
    if(journey>=result.length-1){phase='won';renderBoard();showStory(true);}
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
function showStory(outro=false) {
  $('story-title').textContent=outro?'Дорога вернулась!':level.name;
  $('story-text').textContent=outro?level.outro:level.intro;
  $('story-action').textContent=outro?'На карту →':'В путь →';
  $('story-action').onclick=()=>{story.close();if(outro)showMap();else {phase='playing';render();}};
  if(!story.open)story.showModal();
}
story.addEventListener('cancel',e=>e.preventDefault());
function enterLevel(next:Level) {
  if(next.id!=='sandbox'&&!available(next.id,completed))return;
  cancelAnimationFrame(frame);screen='game';phase=next.id==='sandbox'?'playing':'intro';
  level=next;pieces=level.pieces;cols=level.cols;rows=level.rows;layout={};history=[];route=[];journey=0;path.clear();resetSelection();
  $('chapter-map').hidden=true;$('field').hidden=false;$('game-controls').hidden=false;
  $('size-setting').hidden=level.id!=='sandbox';
  $('clear').textContent=level.id==='sandbox'?'Очистить поле':'Начать уровень заново';
  document.querySelector('.settings-note')!.textContent=level.id==='sandbox'?'Смена размера очищает поле. Поворот телефона сохраняет плиты.':'Перезапуск очищает плиты этого уровня. Дороги на карте сохраняются.';
  svg.setAttribute('aria-label',`${level.name}: ${level.startName} → ${level.goalName}`);
  message(level.id==='sandbox'?level.intro:level.name);render();
  if(level.id!=='sandbox')showStory();
}
function showMap() {
  cancelAnimationFrame(frame);screen='map';phase='playing';route=[];resetSelection();
  if(settings.open)settings.close();if(story.open)story.close();
  $('field').hidden=true;$('game-controls').hidden=true;$('chapter-map').hidden=false;
  message(completed.length===3?'Первая глава пройдена. Можно снова отправиться в путь!':'Первая глава · исчезнувшие дороги');
  $('save-status').textContent=storageAvailable?'': 'Прогресс хранится только до обновления или закрытия страницы.';
  const roads=$('map-roads');roads.replaceChildren();
  for(let i=0;i<3;i++)el('path',{d:`M ${125+i*250} 80 Q ${250+i*250} ${i%2?140:20} ${375+i*250} 80`,fill:'none',stroke:completed.includes(levels[i].id)?'#9272af':'#a2ab8c','stroke-width':12,'stroke-dasharray':completed.includes(levels[i].id)?'none':'10 12','data-road':levels[i].id,'data-complete':String(completed.includes(levels[i].id))},roads);
  const places=$('map-places');places.replaceChildren();
  const home=document.createElement('div');home.className='map-home';home.innerHTML='<span class="place-symbol">⌂</span><strong>Дом Руты</strong>';places.append(home);
  for(const [index,l] of levels.entries()){
    const button=document.createElement('button');button.dataset.level=l.id;button.className='level-card';
    const unlocked=available(l.id,completed),done=completed.includes(l.id);
    button.disabled=!unlocked;button.setAttribute('aria-label',`${l.name}${done?', пройдено, можно переиграть':unlocked?', открыто':', пока закрыто'}`);
    button.innerHTML=`<span class="place-symbol">${['⚑','♧','✣'][index]}</span><strong>${['Калитка','Сад','Мельница'][index]}</strong><span class="map-state">${done?'✓ Ещё раз':unlocked?'▶ В путь':'🔒 Закрыто'}</span>`;
    button.onclick=()=>enterLevel(l);places.append(button);
  }
  $('reset-open').toggleAttribute('disabled',completed.length===0);
}
$('sandbox-open').onclick=()=>enterLevel(sandbox(...(($('size') as HTMLSelectElement).value.split(',').map(Number) as [number,number])));
$('map-return').onclick=showMap;
const resetDialog=$('reset-dialog') as HTMLDialogElement;
$('reset-open').onclick=()=>resetDialog.showModal();
$('reset-cancel').onclick=()=>resetDialog.close();
$('reset-confirm').onclick=()=>{completed=[];storageAvailable=saveProgress(completed,storage);resetDialog.close();showMap();};
showMap();
