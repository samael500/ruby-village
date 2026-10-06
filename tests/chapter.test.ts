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
test('До калитки: ни один собственный поднабор фигур не может победить (полный перебор)',()=>{
  const l=levels[0];
  for(const piece of l.pieces) for(const anchor of boardCells(l.cols,l.rows)) for(let turns=0;turns<6;turns++){
    const candidate={[piece.id]:{anchor,turns}};
    if(validateLayout(l,candidate))assert.equal(winningPath(l,candidate),null);
  }
  assert.equal(Object.keys(l.solution).length,l.pieces.length);
});
test('Сад: прямая дорога закрыта; даже при замощении всей земли нужно обойти преграду снизу',()=>{
  const l=levels[1];
  assert.ok(Object.keys(l.solution).length<l.pieces.length);
  const upper=new Set(boardCells(l.cols,l.rows).filter(h=>h.r<4&&terrainAt(l,h)==='ground').map(key));
  assert.equal(findPath(l.start,l.goal,upper),null);
  const route=winningPath(l,l.solution)!;assert.ok(route.some(h=>h.r>=4));
  const obstructed={anchor:{q:3,r:2},turns:0};
  assert.equal(validPlacement(l,'garden-a',obstructed,{}),false);
});
test('Мост: перебор всех размещений даёт две переправы; дальняя невозможна даже со всеми камнями',()=>{
  const l=levels[2],dry=allDry(l),crossings=new Map<string,{placement:Placement;pathLength:number}>();
  assert.equal(findPath(l.start,l.goal,dry),null);
  for(const anchor of boardCells(l.cols,l.rows))for(let turns=0;turns<6;turns++){
    const placement={anchor,turns};if(!validPlacement(l,'bridge',placement,{}))continue;
    const cells=placedCells('bridge',placement,l.pieces);
    const path=findPath(l.start,l.goal,new Set([...dry,...cells.map(key)]));
    if(path)crossings.set(cells.map(key).sort().join('|'),{placement,pathLength:path.length});
  }
  assert.equal(crossings.size,2);
  const capacity=l.pieces.reduce((n,p)=>n+p.shape.length,0);
  const feasible=[...crossings.values()].filter(c=>c.pathLength-2<=capacity);
  assert.equal(feasible.length,1);
  assert.equal(key(feasible[0].placement.anchor),key(l.solution.bridge.anchor));
  const far=[...crossings.values()].find(c=>c.pathLength-2>capacity)!;
  assert.ok(far); // Even arbitrary single stones cannot cover this lower bound.
  console.log(`Wrong crossing needs at least ${far.pathLength-2} paved cells; inventory has ${capacity}.`);
  assert.ok(Object.keys(l.solution).length<l.pieces.length);
});
test('Вода, сухие концы моста, вращение и пересечения проверяются независимо',()=>{
  const l=levels[2],p=l.solution.bridge;
  assert.equal(validPlacement(l,'mill-extra',{anchor:p.anchor,turns:0},{}),false);
  assert.equal(validPlacement(l,'bridge',{anchor:{q:1,r:1},turns:0},{}),false);
  assert.equal(validPlacement(l,'bridge',{anchor:{q:5,r:3},turns:0},{}),false);
  assert.equal(validPlacement(l,'bridge',p,{bridge:p}),true);
  assert.equal(validPlacement(l,'mill-extra',{anchor:{q:4,r:1},turns:0},{bridge:p}),false);
  assert.equal(validPlacement(l,'missing',p,{}),false);
  assert.equal(validPlacement(l,'bridge',{anchor:p.anchor,turns:.5},{}),false);
  for(let turns=0;turns<6;turns++){
    const synthetic:Level={...sandbox(9,6),pieces:[l.pieces[0]],terrain:{'3,2':'water'}};
    const bridge={anchor:{q:3,r:2},turns};
    assert.ok(validPlacement(synthetic,'bridge',bridge,{}));
    const end=placedCells('bridge',bridge,synthetic.pieces)[1];
    synthetic.terrain[key(end)]='water';assert.equal(validPlacement(synthetic,'bridge',bridge,{}),false);
    synthetic.terrain[key(end)]='rock';assert.equal(validPlacement(synthetic,'bridge',bridge,{}),false);
  }
  const original=l.pieces[0].shape;assert.deepEqual(original.map(h=>rotate(h,6)),original);
});
test('Прогресс: версия, повреждения, порядок, повторы, песочница и сброс',()=>{
  for(const raw of [null,'{','null','[]','{"version":2,"completed":["gate"]}','{"version":1,"completed":"gate"}']) assert.deepEqual(parseProgress(raw),[]);
  assert.deepEqual(parseProgress('{"version":1,"completed":["mill","gate","gate","unknown"]}'),['gate']);
  assert.ok(available('gate',[]));assert.equal(available('garden',[]),false);
  let done:string[]=[];for(const l of levels)done=completeLevel(l.id,done);
  assert.deepEqual(done,['gate','garden','mill']);assert.deepEqual(completeLevel('gate',done),done);
  assert.deepEqual(completeLevel('sandbox',done),done);assert.deepEqual(completeLevel('mill',[]),[]);
  const memory=new Map<string,string>();const storage={getItem:(k:string)=>memory.get(k)??null,setItem:(k:string,v:string)=>{memory.set(k,v);}};
  assert.ok(saveProgress(done,storage));assert.deepEqual(loadProgress(storage),done);
  assert.ok(memory.has(PROGRESS_KEY));saveProgress([],storage);assert.deepEqual(loadProgress(storage),[]);
  const denied={getItem:()=>{throw Error('denied');},setItem:()=>{throw Error('denied');}};
  assert.deepEqual(loadProgress(denied),[]);assert.equal(saveProgress(done,denied),false);assert.equal(saveProgress(done),false);
});
