import {hexCenter,type Hex} from './hex.ts';
export const sceneIds=['gate','garden','well','bakery','stream','mill','post','forest'];
export const artCamera={radius:70,origin:{x:140,y:330}};
/** Ground locations in original 1672×941 artwork pixels; manually reviewed, not color segmentation. */
export const artPoint=(h:Hex)=>{const c=hexCenter(h,artCamera.radius);return {x:(c.x+artCamera.origin.x)/1672,y:(c.y*.65+artCamera.origin.y)/941};};
export const artAnchors:Record<string,{entry:number[];goal:number[]}>= {
 gate:{entry:[.30,.47],goal:[.75,.74]},garden:{entry:[.27,.75],goal:[.76,.46]},well:{entry:[.29,.72],goal:[.71,.48]},bakery:{entry:[.26,.73],goal:[.73,.47]},stream:{entry:[.24,.58],goal:[.76,.46]},mill:{entry:[.22,.68],goal:[.81,.48]},post:{entry:[.27,.72],goal:[.72,.46]},forest:{entry:[.25,.73],goal:[.74,.39]},
};
/** Hand-traced, conservative foreground exclusion regions. */
export function artTerrain(id:string,h:Hex):'ground'|'house'|'tree'|'flower'|'water'{
 const {x,y}=artPoint(h);
 if(id==='forest'&&y<.39)return 'house';
 if(x<.17||x>.87||y<.32||y>.80)return 'house';
 if(['gate','garden'].includes(id)&&x<.34&&y<.49)return 'house';
 if(id==='garden'&&x>.35&&x<.71&&y<.67)return 'tree';
 if(id==='well'&&((x>.36&&x<.62&&y>.37&&y<.65)||(x>.68&&y<.47)))return x>.68?'house':'flower';
 if(['bakery','post'].includes(id)&&x>.66&&y<.45)return 'house';
 if(id==='stream'&&h.q+Math.floor(h.r/2)===[6,6,6,6,7,7,7][h.r])return 'water';
 if(id==='mill'){
  if(h.q+Math.floor(h.r/2)===[4,3,3,3,3,3,4][h.r])return 'water';
  if(x>.66&&y<.43)return 'house';
 }
 return 'ground';
}
