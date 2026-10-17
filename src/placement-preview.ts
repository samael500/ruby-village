import type {Hex} from './hex.ts';
import type {Layout,Level} from './model.ts';
import {validPlacement} from './game.ts';
export type PlacementPreview={selected:string|null;anchor:Hex|null;turns:number;pinned:boolean};
const copy=(p:PlacementPreview):PlacementPreview=>({...p,anchor:p.anchor?{...p.anchor}:null});
/** Pointerup keeps a provisional destination; cancellation restores the gesture snapshot. */
export function releasePreview(current:PlacementPreview,before:PlacementPreview,destination:Hex|null,cancelled:boolean,moved:boolean):PlacementPreview {
 if(cancelled||!moved)return copy(before);
 const anchor=destination??current.anchor;
 return {...copy(current),anchor:anchor?{...anchor}:null,pinned:!!anchor};
}
/** Only this boundary can convert a preview to confirmed, serializable placement data. */
export function confirmedPreview(level:Level,layout:Layout,preview:PlacementPreview):Layout|null {
 if(!preview.selected||!preview.anchor)return null;
 const placement={anchor:{...preview.anchor},turns:preview.turns};
 if(!validPlacement(level,preview.selected,placement,layout))return null;
 return {...layout,[preview.selected]:placement};
}
