import {levels as acceptedLevels} from './levels.ts';
import legacy from './chapter-1.legacy.json' with {type:'json'};
import type {Level,Terrain} from './model.ts';
// Atomic integration gate: switch only when all matching scene layers pass art review.
// #44 remains exported/tested independently; legacy art retains matching gameplay.
export const PRODUCTION_LAYOUT_VERSION=1;
export const productionLevels:readonly Level[]=acceptedLevels.map(level=>{
 const logical=legacy['chapter-1.logical.json'][level.id as keyof typeof legacy['chapter-1.logical.json']];
 const solution=legacy['art-solutions.json'][level.id as keyof typeof legacy['art-solutions.json']];
 return {...level,start:logical.start,goal:logical.goal,terrain:logical.terrain as Record<string,Terrain>,solution,pieces:level.pieces.filter(piece=>piece.id!=='gate-8')};
});
export const productionScenes=legacy['scene-v8.json'];
