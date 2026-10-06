import './style.css';
import {type Hex, boardCells, key, offsetHex, hexCenter, pixelHex, findPath} from './hex.ts';
import {pieces, pieceById, placedCells, occupied, valid, type Layout} from './game.ts';

const app = document.querySelector<HTMLDivElement>('#app')!;
app.innerHTML = `
<header><div class="brand"><span class="ruby" aria-hidden="true">◆</span><h1>Рубиновая деревня<small>проверка управления</small></h1></div>
<div class="settings"><label>Поле<select id="size" aria-label="Размер поля"><option value="7,5">7 × 5</option><option value="9,6" selected>9 × 6</option><option value="11,7">11 × 7</option></select></label>
<label>Управление<select id="mode" aria-label="Режим управления"><option value="select">Выбрать и поставить</option><option value="drag">Перетаскивать</option></select></label>
<button id="fullscreen" aria-label="Полный экран" title="Полный экран" hidden>⛶</button></div></header>
<div class="portrait">↻ Удобнее играть, повернув телефон горизонтально</div>
<main id="field"><svg id="board" role="group" aria-label="Гексагональное поле. Деревня слева, мельница справа"></svg><span id="metric"></span></main>
<footer><div class="tray-row"><div id="tray" aria-label="Набор фигур"></div><p class="hint" id="hint">Выбери плиту → клетку → «Поставить»</p></div>
<div class="actions"><button id="left"><b>↶</b><span>Повернуть влево</span></button><button id="right"><b>↷</b><span>Повернуть вправо</span></button><button id="place" class="primary"><b>＋</b><span>Поставить</span></button><button id="return"><b>↥</b><span>Вернуть в набор</span></button><button id="undo"><b>↩</b><span>Отменить действие</span></button><button id="clear"><b>⌫</b><span>Очистить поле</span></button><button id="check" class="check"><b>⚑</b><span>Проверить дорогу</span></button></div>
<div id="status" role="status" aria-live="polite">Соедини деревню и мельницу фиолетовыми плитами.</div></footer>`;
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const svg = document.getElementById('board') as unknown as SVGSVGElement;
let cols = 9, rows = 6, layout: Layout = {}, history: Layout[] = [];
let selected: string | null = null, anchor: Hex | null = null, turns = 0;
// Once clicked, keep the destination while the pointer travels to the controls.
let anchorPinned = false;
let mode = 'select', path = new Set<string>();
let radius = 20, origin = {x:0,y:0};
let drag: {pointer: number; startX: number; startY: number; moved: boolean; beforeAnchor: Hex | null; beforeTurns: number} | null = null;
let suppressClick = false;
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
function endpoints() { const row = Math.floor(rows/2); return [offsetHex(0,row),offsetHex(cols-1,row)]; }
function previewValid() { return !!(selected && anchor && valid(selected,{anchor,turns},layout,cols,rows)); }
function snapshot() { history.push(structuredClone(layout)); path.clear(); }
function resetSelection() { selected=null; anchor=null; turns=0; anchorPinned=false; }
function select(id: string) {
  selected=id; anchor=layout[id]?.anchor ?? null; turns=layout[id]?.turns ?? 0; anchorPinned=!!layout[id]; path.clear();
  message(`${pieceById(id).name}: ${mode === 'select' ? 'выбери клетку и нажми «Поставить».' : 'перетащи на поле. Можно повернуть кнопками.'}`);
}
function commit() {
  if (!selected || !anchor || !previewValid()) return false;
  snapshot(); layout[selected]={anchor:{...anchor},turns}; resetSelection(); message('Плита на месте. Выбери следующую!'); render(); return true;
}
function updateControls() {
  for (const id of ['left','right']) $(id).toggleAttribute('disabled',!selected);
  $('place').toggleAttribute('disabled',!previewValid());
  $('return').toggleAttribute('disabled',!selected);
  $('undo').toggleAttribute('disabled',history.length===0);
  $('clear').toggleAttribute('disabled',Object.keys(layout).length===0);
}
function renderTray() {
  const tray=$('tray'); tray.replaceChildren();
  for (const p of pieces) {
    const button=document.createElement('button'); button.className='piece'; button.dataset.piece=p.id;
    button.setAttribute('aria-label',`${p.name}${layout[p.id] ? ', на поле' : ', в наборе'}`);
    button.setAttribute('aria-pressed',String(selected===p.id));
    if (layout[p.id]) button.classList.add('placed');
    const centers=p.shape.map(h=>hexCenter(h,15));
    const minX=Math.min(...centers.map(c=>c.x))-17, maxX=Math.max(...centers.map(c=>c.x))+17;
    const minY=-17, maxY=Math.max(...centers.map(c=>c.y))+17;
    const icon=el('svg',{viewBox:`${minX} ${minY} ${maxX-minX} ${maxY-minY}`,'aria-hidden':'true'},button);
    for (const h of p.shape) el('polygon',{points:polygon(h,15),fill:p.color,stroke:'#543b70','stroke-width':1.5},icon);
    el('circle',{cx:0,cy:0,r:2.8,fill:'#fff6dc'},icon);
    const label=document.createElement('span'); label.textContent=p.name; button.append(label);
    if(layout[p.id]) {const mark=document.createElement('em'); mark.textContent='✓'; button.append(mark);}
    tray.append(button);
  }
}
function renderBoard() {
  const rect=$('field').getBoundingClientRect(), padding=8;
  radius=Math.max(1,Math.min((rect.width-2*padding)/(Math.sqrt(3)*(cols+0.5)),(rect.height-2*padding)/(1.5*(rows-1)+2)));
  const w=Math.sqrt(3)*radius*(cols+0.5), h=radius*(1.5*(rows-1)+2);
  origin={x:(rect.width-w)/2+Math.sqrt(3)*radius/2,y:(rect.height-h)/2+radius};
  svg.setAttribute('viewBox',`0 0 ${rect.width} ${rect.height}`); svg.replaceChildren();
  const owners=new Map<string,string>();
  for(const [id,p] of Object.entries(layout)) for(const h of placedCells(id,p)) owners.set(key(h),id);
  const [start,end]=endpoints();
  for(const h of boardCells(cols,rows)) {
    const k=key(h), owner=owners.get(k), c=hexCenter(h,radius);
    const g=el('g',{'data-cell':k,role:'button',tabindex:0,'aria-label':`Клетка ${h.q+Math.floor(h.r/2)+1}, ряд ${h.r+1}${owner ? ', '+pieceById(owner).name : ''}`},svg);
    el('polygon',{points:polygon(h,radius,origin.x,origin.y),class:`cell ${path.has(k)?'path':''}`,fill:owner?pieceById(owner).color:((h.r+Math.floor(h.q/2))%2===0?'#b1c59b':'#a9be93'),opacity:owner===selected?0.45:1},g);
    if(owner && key(layout[owner].anchor)===k) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y,r:Math.max(2,radius*.09),fill:'#fff5d6','pointer-events':'none'},g);
    if(k===key(start)||k===key(end)) {
      el('text',{x:c.x+origin.x,y:c.y+origin.y-radius*.1,class:'landmark','font-size':radius*.62},g,k===key(start)?'⌂':'⚑');
      el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.45,class:'landmark label','font-size':Math.max(10,Math.min(12,radius*.35))},g,k===key(start)?'Деревня':'Мельница');
    }
    if(path.has(k)) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y-radius*.6,r:Math.max(2,radius*.08),fill:'#fffbd3','pointer-events':'none'},g);
  }
  if(selected && anchor) {
    const ok=previewValid(), preview=el('g',{'pointer-events':'none','data-preview':ok?'valid':'invalid'},svg);
    for(const h of placedCells(selected,{anchor,turns})) el('polygon',{points:polygon(h,radius,origin.x,origin.y),class:ok?'preview valid':'preview invalid'},preview);
    const c=hexCenter(anchor,radius);
    el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.23,'text-anchor':'middle','font-size':radius*.8,fill:ok?'#47285f':'#7a1c26','font-weight':900},preview,ok?'•':'⊘');
  }
  $('metric').textContent=`Гекс ${Math.round(Math.sqrt(3)*radius)} × ${Math.round(2*radius)} px`;
}
function render() { renderTray(); renderBoard(); updateControls(); }
function eventHex(e: PointerEvent, lift=false): Hex | null {
  const rect=svg.getBoundingClientRect(), x=e.clientX-rect.left, y=e.clientY-rect.top-(lift && e.pointerType==='touch'?Math.max(42,radius*1.6):0);
  if(x<0||y<0||x>rect.width||y>rect.height) return null;
  return pixelHex(x-origin.x,y-origin.y,radius);
}
function ownerAt(h: Hex) { return Object.entries(layout).find(([id,p])=>placedCells(id,p).some(c=>key(c)===key(h)))?.[0]; }
$('tray').addEventListener('click',e=>{
  if(suppressClick) return;
  const id=(e.target as Element).closest<HTMLElement>('[data-piece]')?.dataset.piece;
  if(id) { select(id); render(); }
});
svg.addEventListener('click',e=>{
  if(mode!=='select'||suppressClick) return;
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
  if(mode==='select' && selected && !anchorPinned && e.pointerType==='mouse' && !e.buttons) {anchor=eventHex(e); renderBoard(); updateControls();}
});
function startDrag(e: PointerEvent,id: string) {
  if(mode!=='drag'||!e.isPrimary||e.button!==0||drag) return;
  e.preventDefault();
  if(selected!==id) select(id);
  drag={pointer:e.pointerId,startX:e.clientX,startY:e.clientY,moved:false,beforeAnchor:anchor?{...anchor}:null,beforeTurns:turns};
  app.setPointerCapture(e.pointerId); render();
}
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
  if(drag.moved) {anchor=eventHex(e,true); renderBoard(); updateControls();}
});
function finishDrag(e: PointerEvent,cancel: boolean) {
  if(!drag||e.pointerId!==drag.pointer) return;
  const previous=drag; drag=null;
  if(app.hasPointerCapture(e.pointerId)) app.releasePointerCapture(e.pointerId);
  suppressClick=true; setTimeout(()=>suppressClick=false,0);
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
$('return').onclick=()=>{
  if(!selected) return;
  if(layout[selected]) {snapshot();delete layout[selected];}
  resetSelection(); message('Плита в наборе.'); render();
};
$('undo').onclick=()=>{const prior=history.pop();if(prior){layout=prior;path.clear();resetSelection();message('Последнее действие отменено.');render();}};
$('clear').onclick=()=>{if(Object.keys(layout).length){snapshot();layout={};resetSelection();message('Поле чистое. Все плиты в наборе.');render();}};
$('check').onclick=()=>{
  const [start,end]=endpoints(), result=findPath(start,end,occupied(layout));
  path=new Set(result?.map(key));
  message(result?'Дорога готова! Из деревни можно дойти до мельницы.':'Пока дорога не соединена. Попробуй переложить плиты');
  renderBoard();
};
$('size').onchange=()=>{
  [cols,rows]=($('size') as HTMLSelectElement).value.split(',').map(Number);
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
window.addEventListener('keydown',e=>{if(e.key==='Escape'){resetSelection();render();}});
new ResizeObserver(()=>renderBoard()).observe($('field'));
render();
