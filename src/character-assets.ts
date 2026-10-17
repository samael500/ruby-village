import manifest from '../public/assets/characters-v1/delivery-manifest.json' with {type:'json'};

export function characterFile(file:string):string{
 return manifest.deliveries[file as keyof typeof manifest.deliveries]?.image??file;
}
export function characterUrl(file:string):string{
 return `${import.meta.env.BASE_URL}assets/characters-v1/${characterFile(file)}`;
}
/** Delivery resizing preserves scene height and rescales both native foot coordinates. */
export function characterFrame<T extends {image:string;frameSize:readonly number[];footAnchor:readonly number[]|null}>(frame:T):T{
 const delivery=manifest.deliveries[frame.image as keyof typeof manifest.deliveries];
 if(!delivery)return frame;
 return {...frame,image:delivery.image,frameSize:delivery.frameSize,footAnchor:delivery.footAnchor} as T;
}
