import {test} from 'node:test';
import assert from 'node:assert/strict';
import {rotate,key,boardCells,canPlace,findPath,neighbors,hexCenter,pixelHex} from '../src/hex.ts';
import {pieces,valid} from '../src/game.ts';
for (const piece of pieces) {
  test(`${piece.id}: шесть последовательных вращений возвращают исходную форму`,()=>{
    let shape=piece.shape.map(h=>({...h}));
    for(let i=0;i<6;i++) shape=shape.map(h=>rotate(h,1));
    assert.deepEqual(shape,piece.shape);
    assert.deepEqual(piece.shape.map(h=>rotate(rotate(h,1),-1)),piece.shape);
  });
  test(`${piece.id}: число, уникальность и опора сохраняются при каждом повороте`,()=>{
    for(let i=-6;i<=6;i++) {
      const shape=piece.shape.map(h=>rotate(h,i));
      assert.equal(shape.length,piece.shape.length);
      assert.equal(new Set(shape.map(key)).size,piece.shape.length);
      assert.deepEqual(shape[0],{q:0,r:0});
    }
  });
}
test('проверка границы и пересечения; собственные клетки не мешают редактированию',()=>{
  const board=new Set(boardCells(7,5).map(key));
  assert.equal(canPlace([{q:0,r:0}],board,new Set()),true);
  assert.equal(canPlace([{q:-1,r:0}],board,new Set()),false);
  assert.equal(canPlace([{q:0,r:5}],board,new Set()),false);
  assert.equal(canPlace([{q:0,r:0}],board,new Set(['0,0'])),false);
  assert.equal(valid('line',{anchor:{q:5,r:0},turns:0},{},7,5),false);
  const layout={'line':{anchor:{q:0,r:0},turns:0},'one-a':{anchor:{q:3,r:0},turns:0}};
  assert.equal(valid('line',{anchor:{q:0,r:0},turns:0},layout,7,5),true);
  assert.equal(valid('line',{anchor:{q:1,r:0},turns:0},layout,7,5),false);
});
test('достижимость учитывает всех шестерых соседей',()=>{
  const start={q:0,r:0};
  for(const end of neighbors(start)) assert.deepEqual(findPath(start,end,new Set()),[start,end]);
});
test('поиск дороги не перепрыгивает пустые клетки; концы проходимы без плит',()=>{
  assert.equal(findPath({q:0,r:0},{q:2,r:0},new Set()),null);
  assert.equal(findPath({q:0,r:0},{q:1,r:1},new Set()),null);
  assert.deepEqual(findPath({q:0,r:0},{q:2,r:0},new Set(['1,0'])),[{q:0,r:0},{q:1,r:0},{q:2,r:0}]);
  assert.equal(findPath({q:0,r:0},{q:3,r:0},new Set(['1,0','2,1'])),null);
});
test('axial / пиксели: центры всех клеток и 3 размеров возвращаются в ту же клетку',()=>{
  for(const [cols,rows] of [[7,5],[9,6],[11,7]]) for(const h of boardCells(cols,rows)) {
    const c=hexCenter(h,19.5); assert.deepEqual(pixelHex(c.x,c.y,19.5),h);
  }
});
