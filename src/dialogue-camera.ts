import type {fitScene} from './scene-camera.ts';
type Scene=ReturnType<typeof fitScene>;
export type NarrativeBounds={top:number;bottom:number};
export type NarrativeViewport={width:number;height:number;fullHeight:number;topInset?:number;bottomInset?:number};
/** Frame the actual conversation in the area above its paper panel. Every
 * scene layer uses this same fit/offset; the accepted ground camera is intact. */
export function frameDialogueScene(scene:Scene,view:NarrativeViewport,focus:readonly NarrativeBounds[],wide?:{width:number;height:number;x:number;y:number}):Scene{
 if(!focus.length||view.height<=0||view.width<=0)return scene;
 const m=scene.metadata,rect=m.originalRect,canvas=wide??{...m.canvas,x:rect.x,y:rect.y};
 const top=Math.min(view.topInset??64,view.height*.3),bottom=view.bottomInset??12;
 const low=Math.min(...focus.map(b=>b.top)),high=Math.max(...focus.map(b=>b.bottom));
 const fullFit=Math.min(view.width/rect.width,view.fullHeight/rect.height);
 const fit=Math.max(view.width/canvas.width,view.height/canvas.height,Math.min(fullFit,(view.height-top-bottom)/Math.max(1,high-low)));
 const x=(view.width-rect.width*fit)/2;
 const desired=(top+view.height-bottom)/2-(low+high)*fit/2;
 const y=Math.max(view.height-(canvas.height-canvas.y)*fit,Math.min(canvas.y*fit,desired));
 return {...scene,fit,offset:{x,y},radius:m.camera.radius*fit,translation:{x:x+m.camera.origin.x*fit,y:y+m.camera.origin.y*fit}};
}
