import {test} from 'node:test';
import assert from 'node:assert/strict';
import {sceneLayout} from '../src/scene-layout.ts';
import {levels} from '../src/levels.ts';
import {boardCells,hexCenter,pixelHex,key} from '../src/hex.ts';
import {terrainAt} from '../src/game.ts';
const level=levels[0],close=(a:number,b:number)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);
test('Единая сцена: ноги на старте, source anchors и hit-test сохраняются при resize',()=>{
  for(const [w,h] of [[1268,550],[832,260],[378,650],[724,240]]){
    const scene=sceneLayout(w,h,level.cols,level.rows,level.start,level.goal);
    const start=hexCenter(level.start,1);
    close(scene.ruta.anchor.x,start.x);close(scene.ruta.anchor.y,start.y);
    for(const p of [scene.house,scene.ruta,scene.gate]){
      close(p.x+p.width*p.source.x,p.anchor.x);close(p.y+p.height*p.source.y,p.anchor.y);
      const x=p.x*scene.scale+scene.origin.x,y=p.y*scene.scale+scene.origin.y;
      assert.ok(x>=0&&y>=0&&x+p.width*scene.scale<=w&&y+p.height*scene.scale<=h);
    }
    for(const cell of boardCells(level.cols,level.rows)){
      const c=hexCenter(cell,scene.scale),screen={x:c.x+scene.origin.x,y:c.y+scene.origin.y};
      assert.deepEqual(pixelHex(screen.x-scene.origin.x,screen.y-scene.origin.y,scene.scale),cell);
    }
    assert.ok(scene.house.width/(scene.bounds.right-scene.bounds.left)<=.24);
    assert.ok(scene.house.height/scene.ruta.height>=2.5);
    assert.ok(Math.hypot(scene.gate.anchor.x-hexCenter(level.goal,1).x,scene.gate.anchor.y-hexCenter(level.goal,1).y)<1.25);
  }
});
test('Декор не перекрывает обычные проходимые клетки; дом занимает данные blocked-клетки',()=>{
  const scene=sceneLayout(844,280,level.cols,level.rows,level.start,level.goal);
  for(const cell of boardCells(level.cols,level.rows)){
    if(terrainAt(level,cell)!=='ground'||[key(level.start),key(level.goal)].includes(key(cell)))continue;
    const c=hexCenter(cell,1),left=c.x-Math.sqrt(3)/2,right=c.x+Math.sqrt(3)/2,top=c.y-1,bottom=c.y+1;
    for(const p of [scene.house,scene.ruta,scene.gate])assert.ok(p.x+p.width<=left||p.x>=right||p.y+p.height<=top||p.y>=bottom,`decor over ${key(cell)}`);
  }
});
