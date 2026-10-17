/** Strip puzzle affordances from a scene while retaining the player's actual road.
 * Works on a clone: the playable board, saved layout and focus targets are untouched. */
export function restoredScene(board: SVGSVGElement, levelName: string): SVGSVGElement {
 const scene=board.cloneNode(true) as SVGSVGElement;
 scene.removeAttribute('id');
 scene.setAttribute('role','img');
 scene.setAttribute('aria-label',`${levelName}: восстановленная дорога`);
 scene.setAttribute('class','completion-scene');
 scene.setAttribute('data-result-scene',levelName);
 for(const target of scene.querySelectorAll('[data-grid],[data-instance-outlines],#placement-preview,[data-goal-marker]'))target.remove();
 for(const cell of scene.querySelectorAll<SVGGElement>('[data-cell]')){
  // Empty cells and terrain symbols belong to puzzle interaction, not the result.
  if(!cell.getAttribute('data-owner')&&!cell.querySelector('[data-material]')){cell.remove();continue;}
  cell.removeAttribute('tabindex');cell.removeAttribute('role');
  cell.removeAttribute('aria-label');
  for(const polygon of cell.querySelectorAll('.cell')){
   polygon.classList.remove('path');polygon.setAttribute('opacity',polygon.classList.contains('bridge-cell')?'0':'1');
  }
 }
 // SVG fragment references are document-global. Give cloned clip/mask IDs their
 // own namespace so closing/reopening results cannot steal the live board's defs.
 const suffix=`-result-${++serial}`;
 const ids=new Map<string,string>();
 for(const element of scene.querySelectorAll('[id]')){
  const id=element.id;ids.set(id,id+suffix);element.id=id+suffix;
 }
 for(const element of [scene,...scene.querySelectorAll('*')])for(const attribute of [...element.attributes]){
  let value=attribute.value;
  for(const [id,replacement] of ids)value=value.replaceAll(`url(#${id})`,`url(#${replacement})`);
  if(ids.has(value.slice(1))&&value.startsWith('#'))value='#'+ids.get(value.slice(1));
  if(value!==attribute.value)element.setAttribute(attribute.name,value);
 }
 return scene;
}
let serial=0;

/** Narrative hiding uses display:none, never translucent puzzle tiles. A won
 * scene retains its actual restored road; ordinary story scenes hide all tiles. */
export function narrativePresentation(app:HTMLElement,active:boolean,restored:boolean){
 app.classList.toggle('narrative-scene',active);
 app.classList.toggle('narrative-restored',active&&restored);
}
