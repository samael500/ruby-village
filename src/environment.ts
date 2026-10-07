import type {Point,SpriteLayout} from './scene-layout.ts';
/** All lengths are unit hex radii, independent of CSS viewport size. */
export const courtyard={
  ground:{asset:'grass-ground',period:20,opacity:.72},
  boundaries:{postSpacing:1.55,height:.62},
  decorations:{shrubHeight:.38,flowerRadius:.035},
  attachments:{gateLeft:{x:.10,y:.88},gateRight:{x:.90,y:.51}},
  presets:{landscape:{inset:.16,verticalMargin:Infinity},portrait:{inset:.3,verticalMargin:1.2}},
} as const;
const attachment=(s:SpriteLayout,p:Point):Point=>({x:s.x+s.width*p.x,y:s.y+s.height*p.y});
export function fenceRoute(gate:SpriteLayout,bounds:{left:number;right:number;top:number;bottom:number},viewport:{left:number;right:number;top:number;bottom:number},portrait:boolean){
  const inset=courtyard.presets[portrait?'portrait':'landscape'].inset;
  const left=Math.min(bounds.left-.25,viewport.left+inset),right=Math.max(bounds.right+.3,viewport.right-inset);
  const margin=courtyard.presets[portrait?'portrait':'landscape'].verticalMargin;
  const top=Math.max(bounds.top-margin,Math.min(bounds.top-.3,viewport.top+.9));
  const bottom=Math.min(bounds.bottom+margin,Math.max(bounds.bottom+.85,viewport.bottom-inset));
  const a=attachment(gate,courtyard.attachments.gateLeft),b=attachment(gate,courtyard.attachments.gateRight);
  return [a,{x:a.x-.3,y:bottom},{x:left,y:bottom},{x:left,y:top},{x:right,y:top},{x:right,y:b.y+.45},b];
}
/** Shared vertices appear once. Gate owns the first/last posts. */
export function fencePosts(route:Point[],spacing=courtyard.boundaries.postSpacing):Point[]{
  const result:Point[]=[route[0]];
  for(let i=1;i<route.length;i++){
    const a=route[i-1],b=route[i],n=Math.ceil(Math.hypot(b.x-a.x,b.y-a.y)/spacing);
    for(let j=1;j<=n;j++)result.push({x:a.x+(b.x-a.x)*j/n,y:a.y+(b.y-a.y)*j/n});
  }
  return result;
}
