import {hexCenter,type Hex} from './hex.ts';
const ns='http://www.w3.org/2000/svg';
/** One painted timber deck spanning the same three cells as the logical bridge.
 * Rotation happens before the shared ground projection, exactly like its cells. */
export function drawBridge(parent:Element,anchor:Hex,turns:number,radius:number,origin:{x:number;y:number}){
 const center=hexCenter(anchor,radius),group=document.createElementNS(ns,'g');
 group.setAttribute('data-painted-bridge','');group.setAttribute('pointer-events','none');
 group.setAttribute('transform',`translate(${center.x+origin.x} ${center.y+origin.y}) rotate(${turns*60})`);
 const deck=document.createElementNS(ns,'svg'),length=3*Math.sqrt(3)*radius;
 for(const [key,value]of Object.entries({x:-length/2,y:-radius*.6,width:length,height:radius*1.2,viewBox:'68 167 2033 359',preserveAspectRatio:'none',overflow:'hidden'}))deck.setAttribute(key,String(value));
 const image=document.createElementNS(ns,'image');image.setAttribute('href',`${import.meta.env.BASE_URL}assets/bridge-v1/deck-v1.png`);image.setAttribute('width','2170');image.setAttribute('height','725');
 deck.append(image);group.append(deck);parent.append(group);return group;
}
