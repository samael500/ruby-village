import {test} from 'node:test';
import assert from 'node:assert/strict';
import {sceneLayout} from '../src/scene-layout.ts';
import {levels} from '../src/levels.ts';
import {boardCells,hexCenter,pixelHex,key,gridEdges,neighbors,instanceEdges,rotate} from '../src/hex.ts';
const level=levels[0],close=(a:number,b:number)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);
test('v4: единый fit изображения, клеток и ног Руты в обеих ориентациях',()=>{
 for(const [w,h,portrait] of [[1268,550,false],[832,260,false],[378,652,true],[728,238,false]] as const){
  const s=sceneLayout(w,h,7,5,level.start,level.goal,portrait);
  close(s.scale,s.art.radius*s.fit);
  close(s.ruta.x+s.ruta.width*.55,s.startArt.x);close(s.ruta.y+s.ruta.height*.965,s.startArt.y);
  assert.ok(s.ruta.height/s.art.doorHeight>=.55 && s.ruta.height/s.art.doorHeight<=.7);
  assert.ok(s.offset.x>=-1e-7&&s.offset.y>=-1e-7);
  assert.ok(s.offset.x+s.art.width*s.fit<=w+1e-7 && s.offset.y+s.art.height*s.fit<=h+1e-7);
  for(const cell of boardCells(7,5)){
   const c=hexCenter(cell,s.scale),screen={x:c.x+s.origin.x,y:c.y+s.origin.y};
   assert.deepEqual(pixelHex(screen.x-s.origin.x,screen.y-s.origin.y,s.scale),cell);
   assert.ok(screen.x-s.scale*Math.sqrt(3)/2>=0&&screen.x+s.scale*Math.sqrt(3)/2<=w);
   assert.ok(screen.y-s.scale>=0&&screen.y+s.scale<=h);
  }
 }
});
test('v4: сетка не удваивает общие стороны и сохраняет края у blocked-клеток',()=>{
 const blocked=new Set(['0,0','1,0']),cells=boardCells(7,5).filter(h=>!blocked.has(key(h))),keys=new Set(cells.map(key));
 const shared=cells.reduce((n,h)=>n+neighbors(h).filter(x=>keys.has(key(x))).length,0)/2;
 assert.equal(gridEdges(7,5,31,{x:24,y:60},blocked).length,cells.length*6-shared);
 assert.equal(gridEdges(7,5,13.123,{x:81.42,y:11.1},blocked).length,cells.length*6-shared);
});
test('v4: Рута не закрывает обычные клетки вне старта',()=>{
 for(const portrait of [false,true]){
  const s=sceneLayout(1280,720,7,5,level.start,level.goal,portrait),p=s.ruta;
  for(const h of boardCells(7,5)){
   if(['0,0','1,0',key(level.start)].includes(key(h)))continue;
   const c=hexCenter(h,s.art.radius),x=c.x+s.art.grid.x,y=c.y+s.art.grid.y,half=s.art.radius*Math.sqrt(3)/2;
   assert.ok(p.x+p.width<=x-half||p.x>=x+half||p.y+p.height<=y-s.art.radius||p.y>=y+s.art.radius,`${portrait}: ${key(h)}`);
  }
 }
});
for(const portrait of [false,true])test(`v4: подходы ${portrait?'portrait':'landscape'} вместе с шириной дорожки не пересекают обычные клетки`,()=>{
 const s=sceneLayout(1280,720,7,5,level.start,level.goal,portrait);
 assert.equal(s.approaches.length,2);
 assert.deepEqual(s.approaches[0][0],s.art.door);
 assert.deepEqual(s.approaches[1].at(-1),s.art.gate);
 const ordinary=new Set(boardCells(7,5).map(key).filter(k=>![key(level.start),key(level.goal)].includes(k)));
 for(const points of s.approaches)for(let i=1;i<points.length;i++){
  const a=points[i-1],b=points[i];
  for(let t=0;t<=100;t++)for(let angle=0;angle<12;angle++){
   const x=a.x+(b.x-a.x)*t/100+11*Math.cos(angle*Math.PI/6),y=a.y+(b.y-a.y)*t/100+11*Math.sin(angle*Math.PI/6);
   const cell=pixelHex(x-s.art.grid.x,y-s.art.grid.y,s.art.radius);
   assert.ok(!ordinary.has(key(cell)),`approach overlaps ${key(cell)}`);
  }
 }
});

test('Границы экземпляров: внутренний стык скрыт, разные фигуры разделены одной линией при шести поворотах',()=>{
 for(let turn=0;turn<6;turn++){
  const a={q:0,r:0},b=rotate({q:1,r:0},turn);
  const same=new Map([[key(a),'a'],[key(b),'a']]);
  const separate=new Map([[key(a),'a'],[key(b),'b']]);
  assert.equal(instanceEdges(same).length,10);
  assert.equal(instanceEdges(separate).length,11);
  assert.equal(instanceEdges(new Map([[key(a),'a']])).length,6);
  assert.equal(instanceEdges(new Map()).length,0);
 }
});
