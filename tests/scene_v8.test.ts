import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {levels} from '../src/levels.ts';
import {boardCells,hexCenter,pixelHex} from '../src/hex.ts';
import {project,unproject} from '../src/projection.ts';
import {fitScene,scenePoint,sceneMetadata} from '../src/scene-camera.ts';
const sizes=[[1280,720],[844,390],[740,360],[915,412],[1024,768],[1920,1080]];
test('Геометрия, препятствия, наборы и эталоны побайтно соответствуют main d1493cd',()=>{
 const logical=levels.map(({id,cols,rows,start,goal,terrain,pieces,solution})=>({id,cols,rows,start,goal,terrain,pieces,solution}));
 assert.equal(createHash('sha256').update(JSON.stringify(logical)).digest('hex'),'ac3ba99f2f65c1f5491a425f37be379a7f481ed626fe91c074b1ef6e42ed4917');
});
test('Камера и обратная проекция определяют ту же клетку после изменения размера',()=>{
 for(const l of levels)for(const [w,h] of sizes){
  const s=fitScene(l.id,w,h-80);
  for(const hex of boardCells(l.cols,l.rows)){
   const c=hexCenter(hex,s.radius);
   for(const offset of [{x:0,y:0},{x:.3*s.radius,y:.2*s.radius},{x:-.3*s.radius,y:-.2*s.radius}]){
    const visible=project({x:c.x+offset.x,y:c.y+offset.y},s.projection);
    const pointer={x:visible.x+s.translation.x,y:visible.y+s.translation.y};
    const inverse=unproject({x:pointer.x-s.translation.x,y:pointer.y-s.translation.y},s.projection);
    assert.deepEqual(pixelHex(inverse.x,inverse.y,s.radius),hex);
   }
  }
 }
});
test('Фон покрывает viewport, исходный прямоугольник и контуры доступных гексов целиком видны',()=>{
 for(const l of levels)for(const [w,h] of sizes){
  const s=fitScene(l.id,w,h-80),m=s.metadata,r=m.originalRect;
  assert.ok(s.offset.x>=-1e-8&&s.offset.y>=-1e-8);
  assert.ok(s.offset.x-r.x*s.fit<=0&&s.offset.y-r.y*s.fit<=0);
  assert.ok(s.offset.x+(m.canvas.width-r.x)*s.fit>=w&&s.offset.y+(m.canvas.height-r.y)*s.fit>=h-80);
  for(const hex of boardCells(l.cols,l.rows))if(!l.terrain[`${hex.q},${hex.r}`]||l.terrain[`${hex.q},${hex.r}`]==='water'){
   const c=hexCenter(hex,s.radius);
   for(let i=0;i<6;i++){
    const a=(i*60-90)*Math.PI/180,p=project({x:c.x+s.radius*Math.cos(a),y:c.y+s.radius*Math.sin(a)},s.projection);
    assert.ok(p.x+s.translation.x>=0&&p.x+s.translation.x<=w&&p.y+s.translation.y>=0&&p.y+s.translation.y<=h-80,`${l.id} ${hex.q},${hex.r}`);
   }
  }
 }
});
const inside=(p:{x:number;y:number},poly:number[][])=>{
 let hit=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){
  const [x,y]=poly[i],[xx,yy]=poly[j];if((y>p.y)!==(yy>p.y)&&p.x<(xx-x)*(p.y-y)/(yy-y)+x)hit=!hit;
 }return hit;
};
test('Передняя маска не скрывает центры доступных клеток и подошвы в начале/конце',()=>{
 for(const l of levels){const m=sceneMetadata(l.id);
  for(const h of boardCells(l.cols,l.rows))if(!l.terrain[`${h.q},${h.r}`]||l.terrain[`${h.q},${h.r}`]==='water')assert.ok(!m.foreground.some(poly=>inside(scenePoint(l.id,h),poly)),`${l.id} ${h.q},${h.r}`);
 }
});

test('Заявленные опорные точки входа/цели совпадают с фактической общей камерой',()=>{
 for(const l of levels)for(const landmark of ['start','goal'] as const){
  const actual=scenePoint(l.id,l[landmark]),expected=sceneMetadata(l.id).groundAnchors[landmark];
  assert.ok(Math.hypot(actual.x-expected.x,actual.y-expected.y)<1e-6);
 }
});
test('Передние контуры не закрывают большую часть гекса; путь находится за их основаниями',()=>{
 for(const l of levels){const m=sceneMetadata(l.id),camera=m.camera;
  for(const h of boardCells(l.cols,l.rows))if(!l.terrain[`${h.q},${h.r}`]||l.terrain[`${h.q},${h.r}`]==='water'){
   const c=hexCenter(h,camera.radius);let covered=0,total=0;
   // Interior samples span the full projected footprint, not just its center.
   for(let ix=-5;ix<=5;ix++)for(let iy=-5;iy<=5;iy++){
    const x=ix*.17,y=iy*.16;if(Math.abs(x)*.577+Math.abs(y)>.98)continue;
    const p=project({x:c.x+x*camera.radius,y:c.y+y*camera.radius},{scale:camera.groundScale,pivotY:0,angle:camera.angle});p.x+=camera.origin.x;p.y+=camera.origin.y;total++;
    if(m.foreground.some(poly=>inside(p,poly)))covered++;
   }
   assert.ok(covered/total<.5,`${l.id}: ${h.q},${h.r} foreground ${covered}/${total}`);
   assert.ok(m.foreground.every(poly=>scenePoint(l.id,h).y<Math.max(...poly.map(p=>p[1]))));
  }
 }
});
