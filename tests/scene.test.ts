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

test('Ограда: непрерывные секции, единственные стойки и привязка к краям калитки',async()=>{
  const {fenceRoute,fencePosts,courtyard}=await import('../src/environment.ts');
  for(const [width,height] of [[1280,550],[844,260],[390,650]]){
    const s=sceneLayout(width,height,level.cols,level.rows,level.start,level.goal);
    const v={left:-s.origin.x/s.scale,top:-s.origin.y/s.scale,right:(width-s.origin.x)/s.scale,bottom:(height-s.origin.y)/s.scale};
    const route=fenceRoute(s.gate,s.bounds,v,height>width),posts=fencePosts(route);
    for(const [actual,anchor] of [[posts[0],courtyard.attachments.gateLeft],[posts.at(-1)!,courtyard.attachments.gateRight]] as const){
      close(actual.x,s.gate.x+s.gate.width*anchor.x);close(actual.y,s.gate.y+s.gate.height*anchor.y);
    }
    assert.equal(new Set(posts.map(p=>`${p.x},${p.y}`)).size,posts.length);
    for(let i=1;i<posts.length;i++)assert.ok(Math.hypot(posts[i].x-posts[i-1].x,posts[i].y-posts[i-1].y)<=courtyard.boundaries.postSpacing+1e-7);
    // Both full horizontal fence sections must remain visible, including post tops.
    for(const point of [route[2],route[3],route[4],route[1]]){
      const x=point.x*s.scale+s.origin.x,y=point.y*s.scale+s.origin.y;
      assert.ok(x-.09*s.scale>=0 && x+.09*s.scale<=width);
      assert.ok(y-(courtyard.boundaries.height+.05)*s.scale>=0 && y+.02*s.scale<=height);
    }
    // All intermediate perimeter posts lie outside the logical field envelope.
    for(const p of posts.slice(1,-1))assert.ok(p.x<s.bounds.left||p.x>s.bounds.right||p.y<s.bounds.top||p.y>s.bounds.bottom);
    if(height>width)assert.ok(Math.max(...route.map(p=>p.y))-Math.min(...route.map(p=>p.y))<=s.bounds.bottom-s.bounds.top+2.4+1e-7);
  }
});
