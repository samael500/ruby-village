// Native coordinates of the accepted 1000×400 map. Entrances, not node labels.
// The map painting remains unchanged; dirt and restored charoite are progress layers.
const routes=[
 ['garden','M115 128 C160 166 218 171 270 165 S353 171 403 128'],
 ['well','M403 128 C445 165 514 172 550 156 S583 146 601 128'],
 ['bakery','M601 128 C650 167 721 169 767 160 S831 160 864 133'],
 ['stream','M864 133 C935 147 977 173 975 217 S958 267 932 292'],
 ['mill','M932 292 C908 351 843 368 784 360 S677 346 626 324'],
 ['post','M626 324 C570 352 510 363 459 349 S392 348 359 321'],
 ['forest','M359 321 C308 354 252 367 206 349 S147 340 112 315'],
] as const;
const ns='http://www.w3.org/2000/svg';
function node(tag:string,attrs:Record<string,string|number>,parent:Element){const element=document.createElementNS(ns,tag);for(const [k,v]of Object.entries(attrs))element.setAttribute(k,String(v));parent.append(element);return element;}
const noise=(i:number,seed:number)=>{const n=Math.sin(i*127.1+seed*311.7)*43758.5453;return n-Math.floor(n);};

/** Painted irregular silhouettes and individual paving stones, not connector lines. */
export function renderMapTrails(target:SVGElement,restored:ReadonlySet<string>){
 target.replaceChildren();
 routes.forEach(([id,d],routeIndex)=>{
  const group=node('g',{'data-map-trail':id,'data-complete':String(restored.has(id))},target);
  const guide=node('path',{d,fill:'none',stroke:'none'},group) as SVGPathElement;
  const length=guide.getTotalLength();
  const sample=(distance:number)=>guide.getPointAtLength(Math.max(0,Math.min(length,distance)));
  const edge=(side:number)=>Array.from({length:Math.ceil(length/3)+1},(_,i)=>{
   const s=Math.min(length,i*3),p=sample(s),a=sample(s-1),b=sample(s+1),n=Math.hypot(b.x-a.x,b.y-a.y)||1;
   const width=3.2+noise(i,routeIndex+side)*1.2;
   return `${p.x-side*(b.y-a.y)/n*width},${p.y+side*(b.x-a.x)/n*width}`;
  });
  node('polygon',{points:[...edge(1),...edge(-1).reverse()].join(' '),fill:'#c2a166',opacity:.66},group);
  // Tiny ochre/grass dabs soften the lane into the existing landscape.
  for(let i=3;i<length;i+=5){const p=sample(i);node('ellipse',{cx:p.x+(noise(i,3)-.5)*6,cy:p.y+(noise(i,4)-.5)*5,rx:1+noise(i,5),ry:.45,fill:noise(i,6)>.5?'#e2c78d':'#9b9c54',opacity:.55},group);}
  if(restored.has(id))for(let distance=4,index=0;distance<length-3;distance+=4.3+noise(index,18)*1.8,index++){
   const p=sample(distance),a=sample(distance-1),b=sample(distance+1),angle=Math.atan2(b.y-a.y,b.x-a.x)*180/Math.PI;
   const stone=node('g',{transform:`translate(${p.x} ${p.y}) rotate(${angle})`,'data-charoite-stone':index},group);
   const size=.85+noise(index,19)*.3;
   stone.setAttribute('transform',`translate(${p.x} ${p.y+(noise(index,20)-.5)*1.5}) rotate(${angle+(noise(index,21)-.5)*18}) scale(${size})`);
   node('path',{d:'M-2.8 -3.1 L.2 -3.6 3.1 -2 2.8 2.6 -.4 3.5 -3.2 1.2Z',fill:['#946aab','#a780b7','#89619c'][index%3],stroke:'#745681','stroke-width':.25},stone);
   node('path',{d:'M-2 -2.4 L0 -2.7 1.8 -1.8 M-.8 .8 L1.4 1.7',fill:'none',stroke:'#d4b6df','stroke-width':.55,opacity:.65},stone);
  }
  guide.remove();
 });
}
