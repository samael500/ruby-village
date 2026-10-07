import {directions,key,add,type Hex} from './hex.ts';
import {courtyard,fenceRoute,fencePosts} from './environment.ts';
import {sceneLayout,type SpriteLayout} from './scene-layout.ts';
const ns='http://www.w3.org/2000/svg';
export const artUrl=(name:string)=>`${import.meta.env.BASE_URL}assets/level-1/${name}.png`;
function node(tag:string,attrs:Record<string,string|number>,parent:Element){
  const el=document.createElementNS(ns,tag);
  for(const [k,v] of Object.entries(attrs))el.setAttribute(k,String(v));
  parent.append(el);return el;
}
export function backdrop(svg:SVGSVGElement,width:number,height:number,scene:ReturnType<typeof sceneLayout>){
  const {scale,origin}=scene,period=courtyard.ground.period;
  const defs=node('defs',{},svg);
  // Mirrored neighbours meet at exactly the same source pixels on every seam.
  const pattern=node('pattern',{id:'court-grass',patternUnits:'userSpaceOnUse',width:period*2,height:period*2,patternTransform:`translate(${origin.x} ${origin.y}) scale(${scale})`},defs);
  for(let row=0;row<2;row++)for(let col=0;col<2;col++)node('image',{href:artUrl(courtyard.ground.asset),width:period,height:period,transform:`translate(${col?period*2:0} ${row?period*2:0}) scale(${col?-1:1} ${row?-1:1})`},pattern);
  node('rect',{width,height,fill:'#94aa55','pointer-events':'none'},svg);
  node('rect',{width,height,fill:'url(#court-grass)',opacity:courtyard.ground.opacity,'pointer-events':'none','data-ground-period':period},svg);
  const soft=node('filter',{id:'court-soil-soft',x:'-30%',y:'-30%',width:'160%',height:'160%'},defs);
  node('feGaussianBlur',{stdDeviation:.055},soft);
  const world=node('g',{'pointer-events':'none',transform:`translate(${origin.x} ${origin.y}) scale(${scale})`},svg);
  const viewport={left:-origin.x/scale,top:-origin.y/scale,right:(width-origin.x)/scale,bottom:(height-origin.y)/scale};
  const posts=fencePosts(fenceRoute(scene.gate,scene.bounds,viewport,height>width));
  const fence=node('g',{'data-environment':'fence'},world);
  // Rails share endpoints; one post per junction, no extra posts over the PNG gate.
  for(let i=1;i<posts.length;i++)for(const lift of [.19,.44]){
    const a=posts[i-1],b=posts[i];
    const d=`M ${a.x} ${a.y-lift} L ${b.x} ${b.y-lift}`;
    node('path',{d,stroke:'#63401f','stroke-width':.15,'stroke-linecap':'round'},fence);
    node('path',{d,stroke:'#bd843c','stroke-width':.095},fence);
    node('path',{d,stroke:'#e2b367','stroke-width':.019,transform:'translate(0 -.04)'},fence);
  }
  for(const p of posts.slice(1,-1).sort((a,b)=>a.y-b.y)){
    node('path',{d:`M ${p.x-.075} ${p.y} L ${p.x-.075} ${p.y-courtyard.boundaries.height+.06} L ${p.x} ${p.y-courtyard.boundaries.height-.03} L ${p.x+.075} ${p.y-courtyard.boundaries.height+.06} L ${p.x+.075} ${p.y} Z`,fill:'#ad7335',stroke:'#63401f','stroke-width':.025},fence);
    node('path',{d:`M ${p.x-.035} ${p.y-.49} L ${p.x-.035} ${p.y-.06}`,stroke:'#e8b665','stroke-width':.025},fence);
  }
  function shrub(x:number,y:number,flowers=true){
    const g=node('g',{'data-environment':'shrub',transform:`translate(${x} ${y})`},world);
    for(let i=0;i<5;i++)node('ellipse',{cx:(i-2)*.12,cy:-.09-(i%2)*.1,rx:.16,ry:courtyard.decorations.shrubHeight*.34,fill:i%2?'#657f32':'#426333',stroke:'#35572b','stroke-width':.012},g);
    if(flowers)for(let i=0;i<7;i++){
      const x=(i-3)*.074,y=-.14-(i%3)*.065;
      node('circle',{cx:x,cy:y,r:courtyard.decorations.flowerRadius,fill:i%3?'#fff1c5':'#e99ca0'},g);
      node('circle',{cx:x,cy:y,r:.013,fill:'#dfb54c'},g);
    }
  }
  // Peripheral vegetation stays outside the playable rectangle, never over previews.
  for(const [i,p] of posts.entries())if(i>1&&i<posts.length-2 && (p.y>scene.bounds.bottom+.6||p.y<scene.bounds.top||p.x<scene.bounds.left||p.x>scene.bounds.right))shrub(p.x+.12,p.y+.13,i%3!==0);
  shrub(scene.house.x+.45,scene.house.y+scene.house.height-.02);
  shrub(scene.house.x+1.03,scene.house.y+scene.house.height+.02);
  for(const [x,y] of [[scene.bounds.left-.25,scene.bounds.bottom+.35],[scene.bounds.right+.28,scene.bounds.top+.7]])node('path',{d:`M ${x-.23} ${y} l .06 -.19 .2 -.09 .2 .14 -.03 .16 Z`,fill:'#989682',stroke:'#6c705c','stroke-width':.035},world);
  const soil=node('g',{fill:'#c4ae69',opacity:.7,filter:'url(#court-soil-soft)'},world);
  for(const p of [scene.ruta.anchor,scene.gate.anchor])node('path',{d:`M ${p.x-.6} ${p.y} q -.2 -.24 .35 -.32 q .9 -.15 .94 .3 q -.15 .38 -.85 .3 Z`},soil);
  const p=scene.gate.anchor;
  node('path',{d:`M ${p.x} ${p.y+.2} Q ${p.x+.2} ${p.y+1.2} ${p.x+1.8} ${p.y+2.4}`,fill:'none',stroke:'#c4ae69','stroke-width':.46,'stroke-linecap':'round',opacity:.65,filter:'url(#court-soil-soft)'},world);
}
export function scenery(svg:SVGSVGElement,scene:ReturnType<typeof sceneLayout>){
  const layer=node('g',{'pointer-events':'none','data-scenery':'',transform:`translate(${scene.origin.x} ${scene.origin.y}) scale(${scene.scale})`},svg);
  for(const [name,file] of ([['house','ruta-house'],['gate','garden-gate'],['ruta','ruta-idle']] as const).slice().sort((a,b)=>scene[a[0]].anchor.y-scene[b[0]].anchor.y)){
    const p:SpriteLayout=scene[name];
    if(name==='ruta')node('ellipse',{cx:p.anchor.x,cy:p.anchor.y,rx:.3,ry:.085,fill:'#3b402c',opacity:.22},layer);
    node('image',{id:name==='ruta'?'ruta-idle':`scene-${name}`,href:artUrl(file),x:p.x,y:p.y,width:p.width,height:p.height,'data-decoration':name,'data-anchor-x':p.anchor.x,'data-anchor-y':p.anchor.y,'aria-label':name==='ruta'?'Рута у начала дороги':name==='house'?'Дом Руты':'Калитка'},layer);
  }
}
// Only the material varies. Fragment edges and veins never define connectivity.
let materialId=0;
export function stoneDetail(parent:Element,h:Hex,r:number,x:number,y:number,variant=0,paved:ReadonlySet<string>=new Set()){
  const turn=((h.q*17+h.r*31)%6+6)%6*60;
  const g=node('g',{'pointer-events':'none',transform:`translate(${x} ${y}) scale(${r})`},parent);
  const hex='M 0 -1 L .8660254 -.5 L .8660254 .5 L 0 1 L -.8660254 .5 L -.8660254 -.5 Z';
  const outlineId=`charoite-${materialId++}`;
  const clip=node('clipPath',{id:outlineId},node('defs',{},g));node('path',{d:hex},clip);
  const top=node('g',{'clip-path':`url(#${outlineId})`},g);
  const pattern=node('g',{transform:`rotate(${turn})`},top);
  const fragments=[
    'M -.8660254 -.5 L .15 -.82 L .76 .25 L .15 .8 L -.8660254 .5 Z',
    'M -.8660254 -.5 L 0 -1 L .8660254 -.5 L .15 -.82 Z',
    'M .15 -.82 L .8660254 -.5 L .8660254 .5 L .76 .25 Z',
    'M -.8660254 .5 L .15 .8 L .76 .25 L .8660254 .5 L 0 1 Z',
  ];
  const palette=variant%2?['#9846cc','#ad69ce','#8646b6','#a363c5']:['#8539bd','#a35dca','#7333a9','#9854c4'];
  for(const [i,d] of fragments.entries()){
    const id=`charoite-${materialId++}`;
    const defs=node('defs',{},pattern),clip=node('clipPath',{id},defs);node('path',{d},clip);
    node('path',{d,fill:palette[i],stroke:'#48205f','stroke-width':.024,'stroke-linejoin':'bevel'},pattern);
    const fragment=node('g',{'clip-path':`url(#${id})`},pattern);
    const veins=node('g',{fill:'none','stroke-linecap':'round',transform:`rotate(${(i*37+h.q*13+h.r*19)%90-45})`},fragment);
    // Broad wisps beneath fine, irregular mineral veins; fixed by cell coordinates.
    for(let j=0;j<4;j++){
      const seed=Math.abs(Math.sin(h.q*127.1+h.r*311.7+i*47+j*83)*43758.5453)%1;
      const y0=-.95+j*.53+seed*.24;
      const bend=.12+seed*.4;
      const wave=`M -1 ${y0} C -.62 ${y0-bend} -.52 ${y0+bend*.7} -.18 ${y0+.12} S .12 ${y0-bend*1.4} .4 ${y0+.03} S .75 ${y0+bend} 1 ${y0-.04}`;
      node('path',{d:wave,stroke:j%2?'#e5b5ef':'#b27de2','stroke-width':.09,opacity:.2},veins);
      node('path',{d:wave,stroke:'#efd1f5','stroke-width':.013,opacity:.65},veins);
      node('path',{d:wave,transform:'translate(.02 .04)',stroke:'#d599ed','stroke-width':.023,opacity:.45},veins);
    }
    // Straight bevel highlights keep the fragments angular, despite the flowing veins.
    node('path',{d,fill:'none',stroke:'#e5b5dd','stroke-width':.01,opacity:.6},pattern);
  }
  const vertices=Array.from({length:6},(_,i)=>({x:Math.cos((i*60-90)*Math.PI/180),y:Math.sin((i*60-90)*Math.PI/180)}));
  const across=[directions[1],directions[0],directions[5],directions[4],directions[3],directions[2]];
  for(let i=0;i<6;i++)if(!paved.has(key(add(h,across[i])))){
    const a=vertices[i],b=vertices[(i+1)%6];
    node('path',{d:`M ${a.x} ${a.y} L ${b.x} ${b.y}`,fill:'none',stroke:i===2||i===3?'#49226d':'#b785d5','stroke-width':.025,'clip-path':`url(#${outlineId})`},g);
  }

}
