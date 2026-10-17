import mapPaint from '../public/assets/chapter-map-v2/manifest.json' with {type:'json'};
const ns='http://www.w3.org/2000/svg';
/** Paths are painted into the map. Progress swaps in matching painted paving
 * pixels from one charoite source; no vector beads or independent road strip. */
export function renderMapTrails(target:SVGElement,restored:ReadonlySet<string>){
 target.replaceChildren();
 for(const [id,patch]of Object.entries(mapPaint.layers.completedRoads)){
  const group=document.createElementNS(ns,'g');group.setAttribute('data-map-trail',id);group.setAttribute('data-complete',String(restored.has(id)));target.append(group);
  if(!restored.has(id))continue;
  const image=document.createElementNS(ns,'image');image.setAttribute('data-painted-progress',id);image.setAttribute('href',`${import.meta.env.BASE_URL}assets/chapter-map-v2/${patch.file}`);image.setAttribute('width',String(patch.canvas[0]));image.setAttribute('height',String(patch.canvas[1]));group.append(image);
 }
}
