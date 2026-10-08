import scenes from './scene-v8.json' with {type:'json'};
import {hexCenter,type Hex} from './hex.ts';
import {project,type Projection} from './projection.ts';
export type SceneId=keyof typeof scenes;
export function sceneMetadata(id:string){return scenes[id as SceneId];}
export function scenePoint(id:string,h:Hex){
 const {camera}=sceneMetadata(id),c=project(hexCenter(h,camera.radius),{scale:camera.groundScale,pivotY:0,angle:camera.angle});
 return {x:c.x+camera.origin.x,y:c.y+camera.origin.y};
}
/** Original rectangle always fits; only newly drawn surroundings may be cropped. */
export function fitScene(id:string,width:number,height:number){
 const metadata=sceneMetadata(id),art=metadata.originalRect,camera=metadata.camera;
 const fit=Math.min(width/art.width,height/art.height),offset={x:(width-art.width*fit)/2,y:(height-art.height*fit)/2};
 const projection:Projection={scale:camera.groundScale,pivotY:0,angle:camera.angle};
 return {metadata,fit,offset,radius:camera.radius*fit,origin:{x:0,y:0},projection,translation:{x:offset.x+camera.origin.x*fit,y:offset.y+camera.origin.y*fit}};
}

/** Decorative sign anchors are separate from immutable puzzle endpoints. */
export function goalSignLayout(id:string,width:number,height:number){
 const scene=fitScene(id,width,height),anchor=scene.metadata.goalSign,goal=scene.metadata.groundAnchors.goal;
 return {x:scene.offset.x+anchor.x*scene.fit,y:scene.offset.y+anchor.y*scene.fit,size:Math.max(14,Math.min(24,scene.radius*.65)),angle:Math.atan2(goal.y-anchor.y,goal.x-anchor.x)*180/Math.PI};
}
