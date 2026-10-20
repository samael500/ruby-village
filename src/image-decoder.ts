/** Share in-flight image decodes, but let a later request retry a failed load. */
export function createImageDecoder(baseUrl:string,createImage:()=>HTMLImageElement=()=>new Image()){
 const images=new Map<string,Promise<HTMLImageElement>>();
 return function decoded(file:string){
  const cached=images.get(file);if(cached)return cached;
  const image=createImage();image.src=baseUrl+file;
  const pending=image.decode().then(()=>image).catch(error=>{
   if(images.get(file)===pending)images.delete(file);
   throw error;
  });
  images.set(file,pending);return pending;
 };
}
