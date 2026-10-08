import {test} from 'node:test';
import assert from 'node:assert/strict';
import {levels,sandbox} from '../src/levels.ts';
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
test('До калитки: кратчайший путь требует все выданные одиночные камни',()=>{
 const l=levels[0],minimum=findPath(l.start,l.goal,allDry(l))!.length-2;
 assert.equal(l.pieces.reduce((n,p)=>n+p.shape.length,0),minimum);
 assert.equal(Object.keys(l.solution).length,l.pieces.length);
});
test('Яблоня и клумба: маршрут не пересекает закрытые клетки; можно не использовать весь набор',()=>{
 for(const l of [levels[1],levels[2]]){
  assert.ok(Object.values(l.terrain).some(t=>t==='tree'||t==='flower'));
  assert.ok(winningPath(l,l.solution)!.every(h=>terrainAt(l,h)==='ground'));
  assert.ok(Object.keys(l.solution).length<l.pieces.length);
 }
});
test('Ручей и мельница: сухие клетки не соединяются, мост обязателен',()=>{
 for(const l of [levels[4],levels[5]]){
  assert.equal(findPath(l.start,l.goal,allDry(l)),null);
  const broken={...l.solution};delete broken.bridge;assert.equal(winningPath(l,broken),null);
 }
});
test('Лесной указатель: фон без реки, маршрут из камня без моста',()=>{
 const l=levels[7];assert.ok(l.pieces.every(p=>p.kind!=='bridge'));
 assert.ok(Object.values(l.terrain).every(t=>t!=='water'));assert.ok(winningPath(l,l.solution));
});
test('Вода, сухие концы моста, вращение и пересечения',()=>{
 const l=levels[4],p=l.solution.bridge;
 assert.equal(validPlacement(l,'stream-a',{anchor:p.anchor,turns:0},{}),false);
 assert.equal(validPlacement(l,'bridge',{anchor:{q:1,r:1},turns:0},{}),false);
 assert.equal(validPlacement(l,'bridge',p,{bridge:p}),true);
 assert.equal(validPlacement(l,'stream-a',{anchor:p.anchor,turns:0},{bridge:p}),false);
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
