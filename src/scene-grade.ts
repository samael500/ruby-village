export type WholeSceneGrade={type:string;values:readonly number[];colorInterpolationFilters?:string};
const ns='http://www.w3.org/2000/svg';let serial=0;
/** Wrap the complete world once, so paint, actors and road share the lighting.
 * HUD lives outside the board SVG; native coordinates and hit targets are unchanged. */
export function applyWholeSceneGrade(svg:SVGSVGElement,grade?:WholeSceneGrade){
 if(!grade)return;
 if(grade.type!=='svg-feColorMatrix'||grade.values.length!==20||!grade.values.every(Number.isFinite))throw new Error('Invalid whole-scene lighting contract');
 const group=document.createElementNS(ns,'g');group.setAttribute('data-scene-grade','');
 group.append(...svg.childNodes);svg.append(group);
 const defs=document.createElementNS(ns,'defs'),filter=document.createElementNS(ns,'filter'),matrix=document.createElementNS(ns,'feColorMatrix'),id=`world-light-${serial++}`;
 filter.setAttribute('id',id);filter.setAttribute('x','0%');filter.setAttribute('y','0%');filter.setAttribute('width','100%');filter.setAttribute('height','100%');filter.setAttribute('color-interpolation-filters',grade.colorInterpolationFilters??'sRGB');
 matrix.setAttribute('type','matrix');matrix.setAttribute('values',grade.values.join(' '));filter.append(matrix);defs.append(filter);svg.prepend(defs);group.setAttribute('filter',`url(#${id})`);
}
