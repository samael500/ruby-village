import {test} from 'node:test';
import assert from 'node:assert/strict';
import {levels,sandbox,wellAlternative} from '../src/levels.ts';
import {boardCells,key,findPath,rotate} from '../src/hex.ts';
import {validPlacement,validateLayout,winningPath,placedCells,terrainAt} from '../src/game.ts';
import {PROGRESS_KEY,parseProgress,loadProgress,saveProgress,available,completeLevel} from '../src/progress.ts';
import type {Level,Placement} from '../src/model.ts';
const allDry=(level:Level)=>new Set(boardCells(level.cols,level.rows).filter(h=>terrainAt(level,h)==='ground').map(key));
for(const level of levels) {
  test(`${level.id}: эталон соответствует набору, местности и соединяет цель`,()=>{
    assert.equal(new Set(level.pieces.map(p=>p.id)).size,level.pieces.length);
    assert.equal(terrainAt(level,level.start),'ground');assert.equal(terrainAt(level,level.goal),'ground');
    assert.ok(Object.keys(level.solution).every(id=>level.pieces.some(p=>p.id===id)));
    assert.ok(validateLayout(level,level.solution));assert.ok(winningPath(level,level.solution));
    const cells=Object.entries(level.solution).flatMap(([id,p])=>placedCells(id,p,level.pieces).map(key));
    assert.equal(new Set(cells).size,cells.length);
    assert.equal(winningPath(level,{}),null);
  });
}
test('До калитки: кратчайший путь требует весь набор, дом непроходим',()=>{
  const l=levels[0],shortest=findPath(l.start,l.goal,allDry(l))!;
  const capacity=l.pieces.reduce((n,p)=>n+p.shape.length,0);
  assert.equal(shortest.length-2,capacity);
  // Even arbitrary independent stones from any proper subset cannot span the gap.
  for(let mask=0;mask<(1<<l.pieces.length)-1;mask++){
    const cells=l.pieces.reduce((n,p,i)=>n+((mask&(1<<i))?p.shape.length:0),0);
    assert.ok(cells<shortest.length-2);
  }
  assert.equal(Object.keys(l.solution).length,l.pieces.length);
  for(const h of [{q:0,r:0},{q:1,r:0}])assert.equal(validPlacement(l,'gate-1',{anchor:h,turns:0},{}),false);
  assert.ok(l.goal.r>l.start.r && l.goal.q>l.start.q);
});
test('Сад: обход яблони снизу и первый поворот без лишней фигуры',()=>{
 const l=levels[1];assert.equal(Object.keys(l.solution).length,l.pieces.length);
 const upper=new Set(boardCells(l.cols,l.rows).filter(h=>h.r<4&&terrainAt(l,h)==='ground').map(key));
 assert.equal(findPath(l.start,l.goal,upper),null);
 assert.ok(winningPath(l,l.solution)!.some(h=>h.r>=4));
 assert.notEqual(l.solution['garden-a'].turns,0);
});
test('Колодец: проверены два разных допустимых обхода клумбы',()=>{
 const l=levels[2];assert.ok(validateLayout(l,wellAlternative));assert.ok(winningPath(l,wellAlternative));
 assert.notDeepEqual(winningPath(l,l.solution),winningPath(l,wellAlternative));
 for(const route of [l.solution,wellAlternative])assert.ok(winningPath(l,route)!.every(h=>terrainAt(l,h)==='ground'));
});
test('Уровни 1–6: в эталонах нет намеренных лишних фигур; разрыв не выигрывает',()=>{
 for(const l of levels.slice(0,6)){
  assert.equal(Object.keys(l.solution).length,l.pieces.length);
  for(const id of Object.keys(l.solution)){
   const broken={...l.solution};delete broken[id];assert.equal(winningPath(l,broken),null,`${l.id}: ${id}`);
  }
 }
});
test('Уровни 1–6: ёмкость набора равна нижней границе пути, любой поднабор недостаточен',()=>{
 for(const l of levels.slice(0,6)){
  // Treat water as usable too: this relaxes bridge constraints and only lowers the bound.
  const allowed=new Set(boardCells(l.cols,l.rows).filter(h=>['ground','water'].includes(terrainAt(l,h))).map(key));
  const minimum=findPath(l.start,l.goal,allowed)!.length-2;
  const capacity=l.pieces.reduce((n,p)=>n+p.shape.length,0);assert.equal(capacity,minimum);
  for(const p of l.pieces)assert.ok(capacity-p.shape.length<minimum);
 }
});
test('Почта: ровно одна лишняя фигура, победа с остатком разрешена',()=>{
 const l=levels[6];assert.equal(l.pieces.length-Object.keys(l.solution).length,1);assert.ok(winningPath(l,l.solution));
});
test('Ручей, мельница и лес: без моста нет дороги даже по всей сухой земле',()=>{
 for(const l of [levels[4],levels[5],levels[7]]){
  assert.equal(findPath(l.start,l.goal,allDry(l)),null);
  const noBridge={...l.solution};delete noBridge.bridge;assert.equal(winningPath(l,noBridge),null);
 }
});
test('Вода, сухие концы моста, вращение и пересечения',()=>{
 const l=levels[4],p=l.solution.bridge;
 assert.equal(validPlacement(l,'stream-a',{anchor:p.anchor,turns:0},{}),false);
 assert.equal(validPlacement(l,'bridge',{anchor:{q:1,r:1},turns:0},{}),false);
 assert.equal(validPlacement(l,'bridge',p,{bridge:p}),true);
 assert.equal(validPlacement(l,'stream-a',{anchor:{q:3,r:3},turns:0},{bridge:p}),false);
 assert.equal(validPlacement(l,'missing',p,{}),false);
 assert.equal(validPlacement(l,'bridge',{anchor:p.anchor,turns:.5},{}),false);
 for(let turns=0;turns<6;turns++){
  const synthetic:Level={...sandbox(9,6),pieces:[l.pieces.find(p=>p.kind==='bridge')!],terrain:{'3,2':'water'}};
  const p={anchor:{q:3,r:2},turns};assert.ok(validPlacement(synthetic,'bridge',p,{}));
  const end=placedCells('bridge',p,synthetic.pieces)[1];
  synthetic.terrain[key(end)]='water';assert.equal(validPlacement(synthetic,'bridge',p,{}),false);
  synthetic.terrain[key(end)]='rock';assert.equal(validPlacement(synthetic,'bridge',p,{}),false);
 }
});
