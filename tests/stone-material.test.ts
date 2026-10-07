import {test} from 'node:test';
import assert from 'node:assert/strict';
import {tileVariant} from '../src/stone-material.ts';
import {footprint,rotate} from '../src/hex.ts';
import {levels} from '../src/levels.ts';
test('Материал остаётся с локальной клеткой фигуры при переносе и шести поворотах',()=>{
 for(const piece of levels[0].pieces)for(const anchor of [{q:0,r:0},{q:5,r:-2}])for(let turns=0;turns<6;turns++){
  const cells=footprint(piece.shape,anchor,turns);
  cells.forEach((h,i)=>{
   const local=rotate({q:h.q-anchor.q,r:h.r-anchor.r},-turns);
   assert.deepEqual(local,piece.shape[i]);
   assert.equal(tileVariant(piece.id,local),tileVariant(piece.id,piece.shape[i]));
  });
 }
});
test('Материал имеет шесть вариантов, повторяемый seed и безопасный индекс при отрицательных координатах',()=>{
 const variants=new Set<number>();
 for(let q=-5;q<=5;q++)for(let r=-5;r<=5;r++){
  const result=tileVariant('gate-a',{q,r});
  assert.ok(Number.isInteger(result)&&result>=0&&result<6);
  assert.equal(result,tileVariant('gate-a',{q,r}));variants.add(result);
 }
 assert.equal(variants.size,6);
});
