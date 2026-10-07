import specification from './chapter-1.story.json' with {type:'json'};
export type Dialogue={speaker:string;text:string};
export const chapter=specification.chapter;
// Stable engine IDs preserve existing calibration/render hooks. The source IDs stay in the story data.
const engineIds=['gate','garden','well','bakery','stream','mill','post','forest'];
export const stories=chapter.levels.map((scene,i)=>({...scene,engineId:engineIds[i]}));
export const storyFor=(id:string)=>stories.find(s=>s.engineId===id);
export const invitation=specification.invitation;
export const ending=specification.ending;
