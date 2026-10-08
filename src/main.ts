import './style.css';
import {loadPreferences,loadSession,saveSession,type Session} from './session.ts';
import {chapterScene} from './chapter-art.ts';
import {GROUND_SCALE,project,unproject,groundTransform,sceneProjection,type Projection} from './projection.ts';
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

<section id="main-menu"><div class="menu-paper"><h2>Рубиновая деревня</h2><p>За калитку · первая глава</p><button id="continue-game" class="primary">Начать приключение</button><button id="choose-level">Выбрать уровень</button><button id="main-settings">Настройки</button><p id="menu-progress"></p><p id="menu-save-status" role="status"></p></div></section>
<section id="chapter-map" aria-label="Карта первой главы">
<div class="map-intro"><span class="ruta-small" aria-hidden="true">◆</span><p>Дороги исчезают… Поможем Руте вернуть их?</p></div>
<div class="map-landscape"><svg id="map-background" viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true"><path d="M 15 170 Q 300 230 480 190 T 980 200" fill="none" stroke="#a4c4bd" stroke-width="25"/><path d="M 90 360 L 120 325 L 150 360 M 760 20 L 790 55 L 820 20" fill="none" stroke="#789065" stroke-width="12"/></svg><svg id="map-roads" viewBox="0 0 1000 400" preserveAspectRatio="none" aria-hidden="true"></svg><div id="map-places"></div></div>
<div class="map-actions"><button id="home-menu">⌂ Меню</button><button id="map-more">Ещё…</button><span id="save-status" role="status"></span></div><dialog id="map-extra"><div class="dialog-heading"><h2>Приключение</h2><button id="map-extra-close" aria-label="Закрыть">✕</button></div><div class="pause-actions"><button id="sandbox-open">Песочница</button><button id="chapter-ending" hidden>✦ Письма через лес</button><button id="letter-open" hidden>✉ Приглашение</button><button id="reset-open">Начать главу заново</button></div></dialog>
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
<dialog id="pause-panel"><div class="dialog-heading"><h2>Небольшой привал</h2><button id="pause-close" aria-label="Вернуться в игру">✕</button></div><div class="pause-actions"><button id="pause-continue" class="primary">Продолжить</button><button id="pause-map">Карта деревни</button><button id="pause-restart">Начать заново</button><button id="pause-settings">Настройки</button></div></dialog>
<dialog id="restart-dialog"><h2>Начать уровень заново?</h2><p>Плиты вернутся в набор. Пройденные дороги сохранятся.</p><button id="restart-cancel">Продолжить</button><button id="restart-confirm">Начать заново</button></dialog>
<dialog id="completion-panel"><h2>Дорожка готова!</h2><img class="completion-art" src="${import.meta.env.BASE_URL}assets/ui/v7/completion-gate.png" alt="Восстановленная дорожка к калитке"><p id="completion-text"></p><button id="next-level" class="primary">Следующее место →</button><button id="completion-map">На карту</button></dialog>
<dialog id="settings-panel" aria-labelledby="settings-title">
<div class="dialog-heading"><h2 id="settings-title">Настройки площадки</h2><button id="settings-close" aria-label="Закрыть настройки">✕</button></div>
<div class="settings"><label id="size-setting">Размер поля<select id="size" aria-label="Размер поля"><option value="7,5">7 × 5 — крупнее</option><option value="9,6" selected>9 × 6</option><option value="11,7">11 × 7 — мельче</option></select></label>
<label>Управление<select id="mode" aria-label="Режим управления"><option value="select">Выбрать и поставить</option><option value="drag">Перетаскивать</option></select></label></div>
<label><input id="reduced-motion" type="checkbox"> Меньше движения</label><p class="settings-note">Звук и музыка пока не добавлены.</p><p id="metric"></p><p id="hint">Выбери плиту → клетку → «Поставить»</p>
<p class="settings-note">Смена размера очищает поле. Поворот телефона сохраняет плиты.</p>
<div class="settings-actions"><button id="map-return">На карту</button><button id="clear">Начать уровень заново</button><button id="story-replay">Реплики</button><button id="fullscreen" hidden>Полный экран</button></div>
</dialog>
<dialog id="story" aria-labelledby="story-title"><div class="story-layout">
<img id="story-ruta" class="ruta-portrait" src="${import.meta.env.BASE_URL}assets/ui/v7/ruta-bust.png" alt="Рута" hidden><div class="story-copy"><p class="eyebrow"></p><h2 id="story-title" class="sr-only"></h2><p id="story-text"></p></div><div class="story-buttons"><button id="story-action" class="primary">В путь →</button><button id="story-skip">Пропустить</button></div></div></dialog>
<dialog id="help-panel" aria-labelledby="help-title"><h2 id="help-title">Проложи дорогу от дома до калитки</h2><p>Выбери плиту → клетку → «Поставить». Поворачивай плиты, чтобы они поместились. Когда дорога готова, нажми «Проверить».</p><button id="help-close">Понятно</button></dialog>
<dialog id="reset-dialog" aria-labelledby="reset-title"><h2 id="reset-title">Начать главу заново?</h2><p>Все восемь дорог на карте снова исчезнут.</p><div class="settings-actions"><button id="reset-cancel">Оставить дороги</button><button id="reset-confirm">Да, начать заново</button></div></dialog>`;
const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;
const svg = document.getElementById('board') as unknown as SVGSVGElement;
let level:Level=sandbox();
let pieces=level.pieces;
const pieceById=(id:string)=>lookupPiece(id,pieces);
const placedCells=(id:string,p:Layout[string])=>cellsForPiece(id,p,pieces);
let screen:'menu'|'map'|'game'='map';
let phase:'intro'|'playing'|'walking'|'won'='playing';
let storage:StorageLike|undefined;
const artCheck=import.meta.env.DEV && new URLSearchParams(location.search).has('art-check');
try {if(!artCheck)storage=window.localStorage;} catch { /* Private browsing may deny storage access. */ }
const loaded=loadState(storage);
let completed=loaded.completed,introSeen=loaded.introSeen,storageAvailable=!!storage;
let savedSession=loadSession(storage,completed);
const preferences=loadPreferences(storage);
let reducedMotion=preferences.reducedMotion||savedSession?.reducedMotion===true;
function persist(){storageAvailable=saveProgress(completed,storage,introSeen);storageAvailable=saveSession(storage,savedSession,{mode:mode==='drag'?'drag':'select',reducedMotion})&&storageAvailable;}
function remember(){if(screen!=='game')return;savedSession={levelId:level.id,cols,rows,layout:structuredClone(layout),mode:mode==='drag'?'drag':'select',reducedMotion};persist();}
let firstVictory=false, victoryAt=0;
let orientationBlocked=false, pausedMilliseconds=0;
let resumeJourney:(()=>void)|null=null;
const portraitWindow=()=>{const v=window.visualViewport;return (v?.height??innerHeight)>(v?.width??innerWidth);};
let route:Hex[]=[], journey=0, frame=0;
let cols = 9, rows = 6, layout: Layout = {}, history: Layout[] = [];
let selected: string | null = null, anchor: Hex | null = null, turns = 0;
// Once clicked, keep the destination while the pointer travels to the controls.
let anchorPinned = false;
let mode = preferences.mode as string, path = new Set<string>();
($('mode') as HTMLSelectElement).value=mode;
let projection:Projection={scale:GROUND_SCALE,pivotY:0};
let ground:Element=svg;
let groundOffset={x:0,y:0};
const v6Preview=true;
const groundPoint=(x:number,y:number)=>{const p=project({x,y},projection);return {x:p.x+groundOffset.x,y:p.y+groundOffset.y};};
let verticalRadius=13,horizontalRadius=17;
let radius = 20, origin = {x:0,y:0};
let drag: {pointer: number; startX: number; startY: number; moved: boolean; beforeAnchor: Hex | null; beforeTurns: number; toggleOnTap: boolean} | null = null;
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
  if (orientationBlocked || phase!=='playing' || !selected || !anchor || !previewValid()) return false;
  snapshot(); layout[selected]={anchor:{...anchor},turns}; resetSelection(); message('Плита на месте. Выбери следующую!'); render(); return true;
}
function updateControls() {
  for(const button of document.querySelectorAll<HTMLButtonElement>('footer button')) button.disabled=false;
  app.classList.toggle('drag-mode',mode==='drag');
  $('selected-drag').setAttribute('aria-label',mode==='drag'?'Перетащить выбранную фигуру':'Выбранная фигура');
  $('selected-drag').hidden=true;$('other').hidden=true;$('left').hidden=true;
  $('tray').hidden=false;
  $('selection-actions').hidden=false;
  $('selection-actions').style.visibility=selected?'visible':'hidden';
  $('check').hidden=false;$('check').toggleAttribute('disabled',!!selected);
  for (const id of ['left','right']) $(id).toggleAttribute('disabled',!selected);
  $('place').toggleAttribute('disabled',!previewValid());
  $('return').toggleAttribute('disabled',!selected||!layout[selected]);
  $('return').style.visibility=selected&&layout[selected]?'visible':'hidden';
  $('place').style.visibility=mode==='select'?'visible':'hidden';
  $('undo').toggleAttribute('disabled',history.length===0);
  $('clear').toggleAttribute('disabled',phase==='walking');
  for(const button of document.querySelectorAll<HTMLButtonElement>('footer button')) if(phase!=='playing') button.disabled=true;
}
function drawPieceIcon(button:HTMLElement,p:Level['pieces'][number],orientation=0) {
  const shape=p.shape.map(h=>rotate(h,orientation));
  const centers=shape.map(h=>hexCenter(h,15));
  const minX=Math.min(...centers.map(c=>c.x))-17, maxX=Math.max(...centers.map(c=>c.x))+17;
  const minY=Math.min(...centers.map(c=>c.y))-17, maxY=Math.max(...centers.map(c=>c.y))+17;
  const viewport=el('svg',{viewBox:`${minX} ${minY*GROUND_SCALE} ${maxX-minX} ${(maxY-minY)*GROUND_SCALE}`,'aria-hidden':'true'},button);
  const icon=el('g',{transform:groundTransform({scale:GROUND_SCALE,pivotY:0})},viewport);
  for (const h of shape) {
    el('polygon',{points:polygon(h,15),fill:p.color,stroke:'#543b70','stroke-width':1.5},icon);
    if(level.id!=='sandbox'&&p.kind!=='bridge'){const c=hexCenter(h,15);stoneDetail(icon,h,15,c.x,c.y,pieces.indexOf(p),new Set(shape.map(key)),{pieceId:p.id,local:rotate(h,-orientation),turns:orientation});}
  }
  if(p.kind==='bridge') el('text',{x:0,y:-6,'text-anchor':'middle','font-size':15,fill:'#493620'},icon,'≋');
  if(selected===p.id)el('circle',{cx:0,cy:0,r:level.id==='gate'?1.6:2.8,fill:'#fff6dc'},icon);
}
function updateTraySelection(){
  for(const button of $('tray').querySelectorAll<HTMLElement>('[data-piece]'))button.setAttribute('aria-pressed',String(selected===button.dataset.piece));
}
function renderTray() {
  const tray=$('tray');
  for(const button of tray.querySelectorAll<HTMLElement>('[data-piece]')) if(!pieces.some(p=>p.id===button.dataset.piece))button.remove();
  for(const p of pieces){
    let button=Array.from(tray.querySelectorAll<HTMLButtonElement>('[data-piece]')).find(b=>b.dataset.piece===p.id);
    if(!button){button=document.createElement('button');button.className='piece';button.dataset.piece=p.id;tray.append(button);}
    button.setAttribute('aria-label',`${p.name}${layout[p.id]?', на поле':', в наборе'}`);
    button.classList.toggle('placed',!!layout[p.id]);
    button.style.setProperty('--piece-width',p.shape.length===1?'88px':'130px');
    const orientation=selected===p.id?turns:layout[p.id]?.turns??0;
    const signature=`${level.id}:${orientation}:${selected===p.id}:${!!layout[p.id]}`;
    if(button.dataset.icon!==signature){button.replaceChildren();drawPieceIcon(button,p,orientation);if(layout[p.id]){const mark=document.createElement('em');mark.textContent='✓';button.append(mark);}button.dataset.icon=signature;}
  }
  updateTraySelection();
  let note=tray.querySelector<HTMLElement>('.tray-note');
  if(!note){note=document.createElement('span');note.className='tray-note';note.textContent='Все плиты на поле';tray.append(note);}
  note.hidden=!pieces.every(p=>layout[p.id]);
}
function renderPreview() {
  document.getElementById('placement-preview')?.remove();
  if(selected && anchor) {
    const ok=previewValid(), preview=el('g',{id:'placement-preview','pointer-events':'none','data-preview':ok?'valid':'invalid'},ground);
    for(const h of placedCells(selected,{anchor,turns})) el('polygon',{points:polygon(h,radius,origin.x,origin.y),class:ok?'preview valid':'preview invalid'},preview);
    const c=hexCenter(anchor,radius);
    el('text',{x:c.x+origin.x,y:c.y+origin.y+radius*.23,'text-anchor':'middle','font-size':radius*.8,fill:ok?'#47285f':'#7a1c26','font-weight':900},preview,ok?'•':'⊘');
  }
}
function renderBoard() {
  if(screen!=='game'||orientationBlocked||portraitWindow()) return;
  if(drag){renderPreview();return;}
  const rect=svg.getBoundingClientRect(), padding=8;
  const illustrated=level.id==='gate',chapterLevel=level.id!=='sandbox';
  const sceneTransform=illustrated&&!v6Preview?sceneLayout(rect.width,rect.height,cols,rows,level.start,level.goal):null;
  const v6=v6Preview&&chapterLevel?chapterScene(level,rect.width,rect.height):null;
  const availableWidth=rect.width-2*padding;
  radius=Math.max(1,Math.min(availableWidth/(Math.sqrt(3)*(cols+0.5)),(rect.height-2*padding)/(GROUND_SCALE*(1.5*(rows-1)+2))));
  const w=Math.sqrt(3)*radius*(cols+0.5), h=radius*(1.5*(rows-1)+2);
  origin={x:(rect.width-w)/2+Math.sqrt(3)*radius/2,y:(rect.height-h*GROUND_SCALE)/(2*GROUND_SCALE)+radius};
  if(sceneTransform){radius=sceneTransform.scale;origin=sceneTransform.origin;}
  svg.setAttribute('viewBox',`0 0 ${rect.width} ${rect.height}`); svg.replaceChildren();
  if(sceneTransform&&!v6)backdrop(svg,rect.width,rect.height,sceneTransform);
  groundOffset={x:0,y:0};
  if(v6){radius=v6.radius;origin=v6.origin;groundOffset=v6.translation;el('image',{id:'chapter-background',href:`${import.meta.env.BASE_URL}assets/chapter-1/v6/${v6.art.file.split('/').pop()}`,x:v6.offset.x,y:v6.offset.y,width:v6.art.width*v6.fit,height:v6.art.height*v6.fit,'pointer-events':'none'},svg);}
  projection=sceneTransform?sceneProjection({x:sceneTransform.offset.x+sceneTransform.startArt.x*sceneTransform.fit,y:sceneTransform.offset.y+sceneTransform.startArt.y*sceneTransform.fit},{x:sceneTransform.offset.x+sceneTransform.goalArt.x*sceneTransform.fit,y:sceneTransform.offset.y+sceneTransform.goalArt.y*sceneTransform.fit}):{scale:GROUND_SCALE,pivotY:0};
  if(v6)projection=v6.projection;
  const vertices=Array.from({length:6},(_,i)=>groundPoint(radius*Math.cos((i*60-90)*Math.PI/180),radius*Math.sin((i*60-90)*Math.PI/180)));
  const xs=vertices.map(p=>p.x),ys=vertices.map(p=>p.y);horizontalRadius=(Math.max(...xs)-Math.min(...xs))/2;verticalRadius=(Math.max(...ys)-Math.min(...ys))/2;
  ground=el('g',{id:'ground-plane',transform:`translate(${groundOffset.x} ${groundOffset.y}) ${groundTransform(projection)}`},svg);
  const owners=new Map<string,string>();
  for(const [id,p] of Object.entries(layout)) for(const h of placedCells(id,p)) owners.set(key(h),id);
  const [start,end]=endpoints();
  const paved=new Set(owners.keys());
  if(chapterLevel){paved.add(key(start));paved.add(key(end));}
  const landmarks=document.createElementNS(ns,'g');landmarks.setAttribute('pointer-events','none');
  for(const h of boardCells(cols,rows)) {
    const k=key(h), owner=owners.get(k), c=hexCenter(h,radius), terrain=terrainAt(level,h),terminal=chapterLevel&&(k===key(start)||k===key(end));
    const g=el('g',{'data-cell':k,'data-terrain':terrain,'data-owner':owner??'',role:'button',tabindex:0,'aria-label':`Клетка ${h.q+Math.floor(h.r/2)+1}, ряд ${h.r+1}${owner ? ', '+pieceById(owner).name : ''}${k===key(start)?', '+level.startName:k===key(end)?', '+level.goalName:''}${terrain==='ground'?'':', '+({tree:'дерево',rock:'камень',water:'вода',house:'дом',flower:'клумба'}[terrain])}`},ground);
    el('polygon',{points:polygon(h,radius,origin.x,origin.y),'pointer-events':'all',class:`cell ${illustrated||v6?(owner||terminal?'flagstone':'meadow-cell'):''} ${path.has(k)?'path':''}`,fill:owner?pieceById(owner).color:terrain==='water'?'#83b9c5':terrain==='rock'?'#a4aa91':((h.r+Math.floor(h.q/2))%2===0?'#b1c59b':'#a9be93'),opacity:owner===selected?0.45:1},g);
    if(chapterLevel && (owner||terminal) && (!owner||pieceById(owner).kind!=='bridge')){const material=el('g',{opacity:owner===selected ? 0.45 : 1},g);stoneDetail(material,h,radius,c.x+origin.x,c.y+origin.y,owner?pieces.indexOf(pieceById(owner)):0,paved,owner?{pieceId:owner,local:rotate({q:h.q-layout[owner].anchor.q,r:h.r-layout[owner].anchor.r},-layout[owner].turns),turns:layout[owner].turns}:{pieceId:'endpoint',local:h,turns:0});}
    if(!owner && terrain!=='ground' && terrain!=='house'&&(!v6||terrain==='water')) el('text',{x:groundPoint(c.x+origin.x,c.y+origin.y).x,y:groundPoint(c.x+origin.x,c.y+origin.y).y+radius*.28,'text-anchor':'middle','font-size':radius*.95,fill:terrain==='water'?'#d8eef0':'#526446','pointer-events':'none'},landmarks,(v6&&terrain!=='water'?'⊘':{water:'≈',tree:'♠',rock:'⬟',flower:'✿'}[terrain]));
    if(owner && pieceById(owner).kind==='bridge') {
      const deck=el('g',{transform:`translate(${c.x+origin.x} ${c.y+origin.y}) rotate(${layout[owner].turns*60})`,'pointer-events':'none'},g);
      for(const dx of [-.35,0,.35]) el('line',{x1:radius*dx,x2:radius*dx,y1:-radius*.65,y2:radius*.65,stroke:'#775032','stroke-width':2},deck);
    }
    if(owner && (!illustrated||owner===selected) && key(layout[owner].anchor)===k) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y,r:Math.max(2,radius*.09),fill:'#fff5d6','pointer-events':'none'},g);
    if((!illustrated||v6) && (k===key(start)||k===key(end))) {
      el('text',{x:groundPoint(c.x+origin.x,c.y+origin.y).x,y:groundPoint(c.x+origin.x,c.y+origin.y).y-radius*.1,class:'landmark','font-size':radius*.62},landmarks,k===key(start)?'⌂':'⚑');
      el('text',{x:groundPoint(c.x+origin.x,c.y+origin.y).x,y:groundPoint(c.x+origin.x,c.y+origin.y).y+radius*.45,class:'landmark label','font-size':Math.max(10,Math.min(12,radius*.35))},landmarks,k===key(start)?level.startName:level.goalName);
    }
    if(path.has(k)) el('circle',{cx:c.x+origin.x,cy:c.y+origin.y-radius*.6,r:Math.max(2,radius*.08),fill:'#fffbd3','pointer-events':'none'},g);
  }
  if(illustrated||v6)drawGrid(ground,cols,rows,radius,origin,new Set(boardCells(cols,rows).filter(h=>!['ground','water'].includes(terrainAt(level,h))).map(key)));
  if(chapterLevel)drawInstanceEdges(ground,owners,radius,origin);
  svg.append(landmarks);
  if(sceneTransform&&!v6)scenery(svg,sceneTransform);
  else if(chapterLevel)prototypeRuta();
  $('scene-event').replaceChildren();$('scene-event').hidden=true;
  if(chapterLevel&&(completed.includes(level.id)||phase==='won'))victoryDecoration();

  renderPreview();
  if(level.id==='mill'&&!v6) {
    const c=hexCenter(level.goal,radius);
    const wheel=el('g',{transform:`translate(${groundPoint(origin.x+c.x,origin.y+c.y).x} ${groundPoint(origin.x+c.x,origin.y+c.y).y-radius*.35})`,'pointer-events':'none'},svg);
    const spokes=el('g',{class:phase==='won'||completed.includes(level.id)?'mill-wheel turning':'mill-wheel','data-wheel':phase==='won'||completed.includes(level.id)?'running':'still'},wheel);
    el('circle',{r:radius*.28,fill:'#dbbd87',stroke:'#765239','stroke-width':2},spokes);
    for(let i=0;i<4;i++){const a=i*Math.PI/4;el('line',{x1:-Math.cos(a)*radius*.28,y1:-Math.sin(a)*radius*.28,x2:Math.cos(a)*radius*.28,y2:Math.sin(a)*radius*.28,stroke:'#765239','stroke-width':2},spokes);}
  }
  if(route.length) {el('g',{id:'ruta-marker','pointer-events':'none','aria-label':'Рута идёт по дороге'},svg);updateRutaMarker();}
  $('metric').textContent=`Гекс ${Math.round(2*horizontalRadius)} × ${Math.round(2*verticalRadius)} px · проекция ${GROUND_SCALE}`;
}
function prototypeRuta(){
 const regular=hexCenter(level.start,radius),foot=groundPoint(regular.x+origin.x,regular.y+origin.y),c={x:foot.x-origin.x,y:foot.y-origin.y},visible=radius*2*1.1,height=visible*1300/1232,width=height*1209/1300;
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
  app.classList.toggle('reduced-motion',reducedMotion);
  if(screen==='game')remember();else persist();
  if(deferDock){
    if(!dockFrame)dockFrame=requestAnimationFrame(()=>{dockFrame=0;deferDock=false;render();});
    return;
  }
  renderBoard();renderTray();updateControls();
}
function eventHex(e: PointerEvent, lift=false): Hex | null {
  const rect=svg.getBoundingClientRect(), x=e.clientX-rect.left, y=e.clientY-rect.top-(lift && e.pointerType==='touch'?Math.max(42,verticalRadius*1.6):0);
  if(x<0||y<0||x>rect.width||y>rect.height) return null;
  const local=unproject({x:x-groundOffset.x,y:y-groundOffset.y},projection);
  return pixelHex(local.x-origin.x,local.y-origin.y,radius);
}
function ownerAt(h: Hex) { return Object.entries(layout).find(([id,p])=>placedCells(id,p).some(c=>key(c)===key(h)))?.[0]; }
$('tray').addEventListener('click',e=>{
  if(suppressClick || phase!=='playing') return;
  const id=(e.target as Element).closest<HTMLElement>('[data-piece]')?.dataset.piece;
  if(id) {if(selected===id){resetSelection();message('Выбор снят. Дорога сохранена.');}else select(id);render();}
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
  if(phase==='playing' && mode==='select' && selected && !anchorPinned && e.pointerType==='mouse' && !e.buttons) {anchor=eventHex(e); renderPreview(); updateControls();}
});
function startDrag(e: PointerEvent,id: string) {
  if(phase!=='playing'||mode!=='drag'||!e.isPrimary||e.button!==0||drag) return;
  // Tray permits horizontal pans; lifting a piece starts a drag on the board.
  const toggleOnTap=selected===id&&!!(e.target as Element).closest('#tray');
  if(selected!==id) select(id);
  drag={pointer:e.pointerId,startX:e.clientX,startY:e.clientY,moved:false,beforeAnchor:anchor?{...anchor}:null,beforeTurns:turns,toggleOnTap};
  app.setPointerCapture(e.pointerId);updateTraySelection();updateControls();renderBoard();
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
  if(!cancel&&!previous.moved&&previous.toggleOnTap){resetSelection();message('Выбор снят. Дорога сохранена.');}
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
const pause=$('pause-panel') as HTMLDialogElement;
$('settings-open').onclick=()=>pause.showModal();
$('pause-close').onclick=$('pause-continue').onclick=()=>pause.close();
$('pause-map').onclick=()=>{pause.close();showMap();};
$('pause-settings').onclick=()=>{pause.close();settings.showModal();};
$('pause-restart').onclick=()=>{pause.close();($('restart-dialog') as HTMLDialogElement).showModal();};
$('restart-cancel').onclick=()=>($('restart-dialog') as HTMLDialogElement).close();
$('restart-confirm').onclick=()=>{($('restart-dialog') as HTMLDialogElement).close();phase='playing';layout={};history=[];route=[];path.clear();resetSelection();render();};
$('reduced-motion').toggleAttribute('checked',reducedMotion);
$('reduced-motion').onchange=()=>{reducedMotion=($('reduced-motion') as HTMLInputElement).checked;app.classList.toggle('reduced-motion',reducedMotion);if(savedSession)savedSession.reducedMotion=reducedMotion;if(screen==='game')remember();else persist();};
$('settings-close').onclick=()=>settings.close();
$('return').onclick=()=>{
  if(!selected) return;
  if(layout[selected]) {snapshot();delete layout[selected];}
  resetSelection(); message('Плита в наборе.'); render();
};
$('undo').onclick=()=>{const prior=history.pop();if(prior){layout=prior;path.clear();resetSelection();message('Последнее действие отменено.');render();}};
$('clear').onclick=()=>{if(phase!=='playing')return;settings.close();($('restart-dialog') as HTMLDialogElement).showModal();};
$('check').onclick=()=>{
  if(orientationBlocked||phase!=='playing')return;
  const result=winningPath(level,layout);
  path=new Set(result?.map(key));
  if(!result){message('Пока дорога не соединена. Попробуй переложить плиты');renderBoard();return;}
  if(level.id==='sandbox'){message('Дорога готова! Из деревни можно дойти до мельницы.');renderBoard();return;}
  phase='walking';route=result;journey=0;resetSelection();
  firstVictory=!completed.includes(level.id);
  completed=completeLevel(level.id,completed);persist();
    message('Получилось! Рута проверяет дорожку.');render();
  const began=performance.now(),pauseAtStart=pausedMilliseconds,duration=Math.min(3500,result.length*230);
  const animate=(now:number)=>{
    if(phase!=='walking'||screen!=='game'||orientationBlocked||modalPaused)return;
    journey=(reducedMotion||matchMedia('(prefers-reduced-motion: reduce)').matches)?result.length-1:Math.max(0,Math.min(1,(now-began-(pausedMilliseconds-pauseAtStart))/duration))*(result.length-1);
    updateRutaMarker();
    if(journey>=result.length-1){phase='won';resumeJourney=null;victoryAt=performance.now();renderBoard();finishVictory();}
    else frame=requestAnimationFrame(animate);
  };
  resumeJourney=()=>{if(phase==='walking'&&!orientationBlocked&&!modalPaused)frame=requestAnimationFrame(animate);};
  resumeJourney();
};
$('size').onchange=()=>{
  [cols,rows]=($('size') as HTMLSelectElement).value.split(',').map(Number);
  if(level.id!=='sandbox')return;
  level=sandbox(cols,rows);pieces=level.pieces;
  layout={};history=[];path.clear();resetSelection();message('Новое поле. Все плиты снова в наборе.');render();
};
$('mode').onchange=()=>{
  mode=($('mode') as HTMLSelectElement).value;if(savedSession)savedSession.mode=mode==='drag'?'drag':'select';resetSelection();
  $('hint').textContent=mode==='select'?'Выбери плиту → клетку → «Поставить»':'Листай набор вбок · тяни плиту вверх на поле';
  message(mode==='select'?'Выбери плиту в наборе или на поле.':'Перетащи плиту на поле. Отпусти, чтобы поставить.');render();
};
if(document.fullscreenEnabled) {
  $('fullscreen').hidden=false;
  $('fullscreen').onclick=async()=>{
    try {if(document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen();}
    catch {message('Полный экран недоступен. Можно играть так.');}
  };
}
window.addEventListener('keydown',e=>{if(e.key==='Escape' && !drag && screen==='game' && phase==='playing' && !app.querySelector('dialog[open]')){resetSelection();render();}});
new ResizeObserver(()=>renderBoard()).observe($('field'));

function updateRutaMarker() {
  const marker=document.getElementById('ruta-marker');if(!marker||!route.length)return;
  const index=Math.min(Math.floor(journey),route.length-1),next=Math.min(index+1,route.length-1),t=journey-index;
  const a=hexCenter(route[index],radius),b=hexCenter(route[next],radius);
  const foot=groundPoint(origin.x+a.x+(b.x-a.x)*t,origin.y+a.y+(b.y-a.y)*t);
  marker.setAttribute('transform',`translate(${foot.x} ${foot.y})`);
  marker.replaceChildren();
  const height=radius*2*1.1*1300/1232,width=height*1209/1300;
  el('ellipse',{cx:0,cy:0,rx:radius*.23,ry:radius*.08,fill:'#352d24',opacity:.25},marker);
  el('image',{href:artUrl('ruta-idle'),x:-width*.55,y:-height*1277/1300,width,height,'aria-label':'Рута'},marker);
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
 pages=pages.flatMap(page=>{
  if(page.text.length<=170||/приглашение|Хранитель/.test(page.speaker))return [page];
  const chunks:string[]=[];let chunk='';
  for(const sentence of page.text.match(/[^.!?…]+[.!?…]*\s*/g)??[page.text]){
   if(chunk&&chunk.length+sentence.length>170){chunks.push(chunk.trim());chunk='';}chunk+=sentence;
  }
  if(chunk)chunks.push(chunk.trim());return chunks.map(text=>({speaker:page.speaker,text}));
 });
 let index=0;
 const portrait=$('story-ruta') as HTMLImageElement;
 story.classList.toggle('reading',screen!=='game');
 const draw=()=>{
  document.getElementById('bridge-guide')?.remove();
  if(pages[index].speaker==='Мост')bridgeGuide($('story-text').parentElement!);
  $('story-title').textContent=title;
  document.querySelector('#story .eyebrow')!.textContent=pages[index].speaker;
  portrait.hidden=pages[index].speaker!=='Рута';story.classList.toggle('has-portrait',!portrait.hidden);
  story.classList.toggle('letter',/приглашение|Хранитель/.test(pages[index].speaker));
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
  if(outro){showCompletion();}
  else{if(!introSeen.includes(level.id))introSeen.push(level.id);persist();phase='playing';render();}
 },outro?'Дальше →':'В путь →');
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
function finishVictory(){if(firstVictory)showStory(true);else{message('Дорога снова готова!');dialogPages(level.name,[{speaker:'Рута',text:'Получилось! Дорога снова соединена.'}],showCompletion,'Дальше →');}}
story.addEventListener('cancel',e=>{e.preventDefault();$('story-skip').click();});
function enterLevel(next:Level,resume:Session|null=null) {
  if(!resume&&savedSession?.levelId===next.id&&savedSession.cols===next.cols&&savedSession.rows===next.rows)resume=savedSession;
  app.classList.remove('menu-screen');($('map-extra') as HTMLDialogElement).close();
  $('main-menu').hidden=true;
  if(next.id!=='sandbox'&&!available(next.id,completed))return;
  cancelAnimationFrame(frame);resumeJourney=null;screen='game';phase=next.id==='sandbox'||introSeen.includes(next.id)?'playing':'intro';
  level=next;pieces=level.pieces;cols=level.cols;rows=level.rows;layout=resume?structuredClone(resume.layout):{};if(resume)mode=resume.mode;($('mode') as HTMLSelectElement).value=mode;history=[];route=[];journey=0;path.clear();resetSelection();
  app.classList.toggle('illustrated-level',level.id!=='sandbox');
  app.classList.toggle('prototype-level',false);
  sceneChrome(level.id!=='sandbox');
  document.querySelector('h1')!.textContent=level.id==='sandbox'?'Рубиновая деревня':level.name;
  if(level.id!=='sandbox'){const note=document.createElement('small');note.textContent=`За калитку · ${levels.indexOf(level)+1}/8`;note.dataset.prototype='';document.querySelector('h1')!.append(note);}
  $('chapter-map').hidden=true;$('field').hidden=false;$('game-controls').hidden=false;
  $('size-setting').hidden=level.id!=='sandbox';
  if(level.id==='sandbox')($('size') as HTMLSelectElement).value=`${cols},${rows}`;
  $('clear').textContent=level.id==='sandbox'?'Очистить поле':'Начать уровень заново';
  document.querySelector('.settings-note')!.textContent=level.id==='sandbox'?'Смена размера очищает поле. Поворот телефона сохраняет плиты.':'Перезапуск очищает плиты этого уровня. Дороги на карте сохраняются.';
  svg.setAttribute('aria-label',`${level.name}: ${level.startName} → ${level.goalName}`);
  message(level.id==='gate'?'Проложи дорогу от дома до калитки':level.id==='sandbox'?level.intro:level.name);render();
  $('story-replay').hidden=level.id==='sandbox';
  if(phase==='intro')showStory();
  $('clear').hidden=false;$('map-return').hidden=false;$('story-replay').hidden=level.id==='sandbox';$('metric').hidden=false;$('hint').hidden=false;
}
function mapGeometry(){
 const points=[[120,95],[365,95],[610,95],[855,95],[855,300],[610,300],[365,300],[120,300]];
 const roads=$('map-roads');roads.replaceChildren();
 let previous=[20,95];
 levels.forEach((l,i)=>{
  const [x,y]=points[i],done=completed.includes(l.id);
  el('path',{d:`M ${previous[0]} ${previous[1]} L ${x} ${y}`,fill:'none',stroke:done?'#9062b0':'#a2ab8c','stroke-width':10,'stroke-dasharray':done?'none':'10 12','data-road':l.id,'data-complete':String(done)},roads);
  const node=document.querySelector<HTMLElement>(`[data-map-node="${l.id}"]`);
  if(node){node.style.left=`${x/10}%`;node.style.top=`${y/4}%`;}
  previous=[x,y];
 });
}
function showMap(){
 app.classList.remove('menu-screen');($('map-extra') as HTMLDialogElement).close();
 $('main-menu').hidden=true;
 if(screen==='game'){if(phase==='won'){savedSession=null;persist();}else remember();}
 $('scene-event').hidden=true;
 app.classList.remove('illustrated-level','prototype-level');sceneChrome(false);document.querySelector('h1')!.textContent='Рубиновая деревня';
 cancelAnimationFrame(frame);resumeJourney=null;screen='map';phase='playing';route=[];resetSelection();
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
  const symbol=document.createElement('span');symbol.className='place-symbol';const image=document.createElement('img');image.src=`${import.meta.env.BASE_URL}assets/chapter-1/v6/${['01-courtyard','02-orchard','03-well','04-bakery','05-stream','06-mill','07-post','08-edge'][index]}.png`;image.alt='';symbol.append(image);
  const title=document.createElement('strong');title.textContent=`${index+1}. ${l.name}`;
  const state=document.createElement('span');state.className='map-state';state.textContent=done?'✓ Пройден':unlocked?'▶ В путь':'🔒 Закрыто';
  button.append(symbol,title,state);button.onclick=()=>enterLevel(l);node.append(button);
  if(unlocked){const book=document.createElement('button');book.className='map-book';book.innerHTML='<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M12 5Q6 2 2 5V20Q7 17 12 20Q17 17 22 20V5Q18 2 12 5V20" fill="none" stroke="currentColor" stroke-width="2"/></svg>';book.setAttribute('aria-label',`Реплики: ${data.title}`);book.onclick=()=>readStory(l.id);node.append(book);}
  places.append(node);
 }
 mapGeometry();
 $('chapter-ending').hidden=!completed.includes('forest');$('letter-open').hidden=!completed.includes('post');
 $('reset-open').toggleAttribute('disabled',completed.length===0);
}
new ResizeObserver(()=>{if(screen==='map')mapGeometry();}).observe($('chapter-map'));
$('chapter-ending').onclick=()=>{($('map-extra') as HTMLDialogElement).close();showEnding();};
$('letter-open').onclick=()=>{($('map-extra') as HTMLDialogElement).close();dialogPages('Старое приглашение',[{speaker:'Хранитель сада',text:invitation.text}],()=>{},'Закрыть');};
$('story-replay').onclick=()=>{settings.close();readStory(level.id);};
$('sandbox-open').onclick=()=>enterLevel(savedSession?.levelId==='sandbox'?sandbox(savedSession.cols,savedSession.rows):sandbox(...(($('size') as HTMLSelectElement).value.split(',').map(Number) as [number,number])));
$('map-return').onclick=showMap;
const resetDialog=$('reset-dialog') as HTMLDialogElement;
$('map-more').onclick=()=>($('map-extra') as HTMLDialogElement).showModal();
$('map-extra-close').onclick=()=>($('map-extra') as HTMLDialogElement).close();
$('reset-open').onclick=()=>{($('map-extra') as HTMLDialogElement).close();resetDialog.showModal();};
$('reset-cancel').onclick=()=>resetDialog.close();
$('reset-confirm').onclick=()=>{completed=[];introSeen=[];savedSession=null;persist();resetDialog.close();showMap();};
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
icon($('scene-back'),'M 3 5 L 9 3 L 15 5 L 21 3 V 19 L 15 21 L 9 19 L 3 21 Z M 9 3 V 19 M 15 5 V 21');
icon($('settings-open'),'M 4 5 H 20 M 4 12 H 20 M 4 19 H 20');
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

function showCompletion(){
 $('completion-text').textContent=level.id==='forest'?'Глава «За калитку» пройдена! Следующее приключение готовится.':level.outro;
 $('next-level').hidden=level.id==='forest';
 const next=levels[levels.indexOf(level)+1];$('next-level').textContent=level.id==='gate'?'К саду Кролика →':next?`Дальше: ${next.name} →`:'На карту';
 ($('completion-panel') as HTMLDialogElement).showModal();
}
$('completion-map').onclick=()=>{($('completion-panel') as HTMLDialogElement).close();if(level.id==='forest')showEnding();else showMap();};
$('next-level').onclick=()=>{($('completion-panel') as HTMLDialogElement).close();const next=levels[levels.indexOf(level)+1];if(next)enterLevel(next);};
($('completion-panel') as HTMLDialogElement).addEventListener('cancel',e=>{e.preventDefault();$('completion-map').click();});
function showMenu(){
 app.classList.add('menu-screen');
 app.classList.toggle('reduced-motion',reducedMotion);
 screen='menu';$('chapter-map').hidden=true;$('field').hidden=true;$('game-controls').hidden=true;$('main-menu').hidden=false;
 $('continue-game').textContent=savedSession||completed.length?'Продолжить':'Начать приключение';
 $('menu-progress').textContent=`Восстановлено дорог: ${completed.length} из 8`;
 $('menu-save-status').textContent=storageAvailable?'':'Не удалось сохранить. Можно играть до закрытия страницы.';
}
$('continue-game').onclick=()=>{const next=savedSession?.levelId==='sandbox'?sandbox(savedSession.cols,savedSession.rows):levels.find(l=>l.id===savedSession?.levelId&&available(l.id,completed))??levels.find(l=>available(l.id,completed)&&!completed.includes(l.id))??levels[0];enterLevel(next,savedSession?.levelId===next.id?savedSession:null);};
$('choose-level').onclick=showMap;
$('home-menu').onclick=showMenu;
$('main-settings').onclick=()=>{for(const id of ['clear','map-return','story-replay','metric','hint','size-setting'])$(id).hidden=true;settings.showModal();};
// A single pause clock covers overlapping modal/orientation blockers.
let modalPaused=false,clockPaused=false,clockPauseStart=0;
function syncPause(){
 const blocked=orientationBlocked||[...app.querySelectorAll<HTMLDialogElement>('dialog')].some(d=>d.open);
 modalPaused=[...app.querySelectorAll<HTMLDialogElement>('dialog')].some(d=>d.open);
 if(blocked===clockPaused)return;
 clockPaused=blocked;
 if(blocked){clockPauseStart=performance.now();cancelAnimationFrame(frame);}
 else{pausedMilliseconds+=performance.now()-clockPauseStart;resumeJourney?.();}
}
new MutationObserver(syncPause).observe(app,{subtree:true,attributes:true,attributeFilter:['open']});

const orientationScreen=document.createElement('section');
orientationScreen.id='orientation-screen';orientationScreen.hidden=true;orientationScreen.tabIndex=-1;
orientationScreen.setAttribute('role','region');orientationScreen.setAttribute('aria-label','Альбомный режим');
orientationScreen.innerHTML=`<svg viewBox="0 0 160 150" width="160" height="150" aria-hidden="true"><g transform="rotate(-25 80 75)"><rect x="53" y="28" width="54" height="94" rx="10" fill="#edcf94" stroke="#765438" stroke-width="5"/><rect x="60" y="42" width="40" height="63" rx="3" fill="#9bb279"/><circle cx="80" cy="113" r="3" fill="#765438"/></g><path d="M 22 79 A 58 58 0 0 1 121 30 M 109 28 L 124 29 L 123 44" fill="none" stroke="#8659a5" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg><h2>Поверни устройство — приключение продолжается в альбомном режиме</h2><p>Расширь окно, чтобы продолжить приключение</p>`;
document.body.append(orientationScreen);
let suspendedDialogs:HTMLDialogElement[]=[],previousFocus:HTMLElement|null=null,orientationGeneration=0;
function updateOrientation(){
 const blocked=portraitWindow();if(blocked===orientationBlocked)return;
 orientationBlocked=blocked;const generation=++orientationGeneration;
 if(blocked){
  syncPause();cancelAnimationFrame(frame);
  if(drag)finishDrag(new PointerEvent('pointercancel',{pointerId:drag.pointer}),true);
  previousFocus=document.activeElement as HTMLElement;
  suspendedDialogs=[...app.querySelectorAll<HTMLDialogElement>('dialog[open]')];
  suspendedDialogs.forEach(d=>d.close());
  app.inert=true;app.hidden=true;orientationScreen.hidden=false;orientationScreen.focus({preventScroll:true});
 }else{
  orientationScreen.hidden=true;app.hidden=false;app.inert=false;
  suspendedDialogs.forEach(d=>d.showModal());suspendedDialogs=[];
  previousFocus?.focus({preventScroll:true});
  requestAnimationFrame(()=>{if(orientationBlocked||generation!==orientationGeneration)return;if(screen==='map')mapGeometry();else if(screen==='game')render();syncPause();});
 }
}
window.addEventListener('resize',updateOrientation);
window.visualViewport?.addEventListener('resize',updateOrientation);
showMap();showMenu();updateOrientation();

// Development-only visual fixture; storage is disconnected for its whole session.
if(artCheck){enterLevel(levels[0]);story.close();phase='playing';layout=Object.fromEntries(Object.entries(levels[0].solution).slice(0,3).map(([id,p])=>[id,structuredClone(p)]));render();}
